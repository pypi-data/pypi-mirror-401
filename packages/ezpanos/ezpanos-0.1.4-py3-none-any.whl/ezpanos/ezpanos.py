from random import random
import urllib
import requests
import getpass

import requests
from urllib3.exceptions import InsecureRequestWarning
import re
import json

"""
PanOS API integration
"""

def parse_xml_response(xml_response: str) -> dict:
    """
    Parses a simple XML response into a dictionary.

    Args:
        xml_response (str): XML response string.

    Returns:
        dict: Parsed key-value pairs.
    """
    from xml.etree import ElementTree as ET
    root = ET.fromstring(xml_response)
    result = {}
    for child in root:
        result[child.tag] = child.text
    return result

def prettyprint_xml(xml_str: str, shorten=True) -> None:
    """
    Pretty prints an XML string in a tabular format, showing each tag and its content.

    Args:
        xml_str (str): XML string to pretty print.
    """
    # this method needs a lint roller.
    def print_element(element, indent=0):
        prefix = "  " * indent
        if list(element):
            print(f"{prefix}{element.tag}:")
            for child in element:
                print_element(child, indent + 1)
        else:
            text = element.text.strip() if element.text else ""
            print(f"{prefix}{element.tag}: {text}")

    from xml.etree import ElementTree as ET
    # default response is always <response><result>...</result></response>
    # If shorten is True, only print the contents of <result> or <msg> if present
    try:
        root = ET.fromstring(xml_str)
        if shorten:
            # Try to find <result> or <msg> under <response>
            result = root.find("result")
            msg = root.find("msg")
            if result is not None:
                print_element(result)
                return
            elif msg is not None:
                print("Error Message:")
                print_element(msg)
                return
    except Exception:
        pass  # Fallback to full pretty print if parsing fails

    try:
        root = ET.fromstring(xml_str)
        print_element(root)
    except Exception as e:
        print("Failed to parse XML:", e)


def is_network_location(ip_address: str) -> bool:
    """
    Determines if the given IP address is a network location (i.e., matches regex).

    Args:
        ip_address (str): The IP address to check.
    Returns:
        bool: True if it's a network location, False otherwise.
    """
    # Regex for IPv4 address
    ip_pattern = r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}"
    fqdn_pattern = r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?"
    return (
        re.match(ip_pattern, ip_address) is not None
    ) or (
        re.match(fqdn_pattern, ip_address) is not None
    )


def build_xml_from_command(command_str: str) -> str:
    """
    Converts a space-separated command string into nested XML tags.
    Handles special cases like variables (starting with $) which are treated as values.

    Example:
        "show system info"
        -> "<show><system><info></info></system></show>"

        "show devices deviceid $DEVICE_ID"
        -> "<show><devices><deviceid>$DEVICE_ID</deviceid></devices></show>"

    Args:
        command_str (str): Command string.

    Returns:
        str: XML API Command string.
    """
    parts = command_str.strip().split()
    xml = ""
    stack = []

    i = 0
    while i < len(parts):
        part = parts[i]
        # If next part is a variable, treat as value
        if (i + 1 < len(parts)) and parts[i + 1].startswith("$"):
            xml += f"<{part}>{parts[i + 1]}</{part}>"
            i += 2
        else:
            xml += f"<{part}>"
            stack.append(part)
            i += 1

    # Close all opened tags
    while stack:
        xml += f"</{stack.pop()}>"

    return xml


class PanOS:
    def __init__(self, endpoint, username=None, password=None, api_key=None):
        # Disable warnings about insecure connections
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.api_key = api_key

        if not self.api_key:
            if self.username is None and self.password is None:
                # prompts user for creds
                if self.username is None or self.password is None:
                    self.username = input("Username: ")
                    self.password = getpass.getpass("Password: ")

            # Gets API key with credentials if api_key not overridden
            params = {
                "type": "keygen",
                "user": self.username,
                "password": self.password
            }
            url = f"https://{self.endpoint}/api?{urllib.parse.urlencode(params)}"
            self.api_key = requests.get(url, verify=False)
            if self.api_key.status_code == 200:
                # parse out API key from XML response
                from xml.etree import ElementTree as ET
                root = ET.fromstring(self.api_key.text)
                self.api_key = root.find(".//key").text
                    
            else:
                print("Failed to retrieve API key.")
                self.api_key = None

    def execute(self, command: str, prettyprint=False) -> str:
        xml_cmd = build_xml_from_command(command)
        try:
            responses = self.batch_execute([xml_cmd])
            if prettyprint:
                for response in responses:
                    prettyprint_xml(response)
            return "\n".join(responses)

        except Exception as e:
            print("Error:", e)

    '''
    Batch executes xml encoded Panorama commands
    '''
    def batch_execute(self, xml_commands: list[str], api_type: str = "op", api_action: str = None, api_xpath: str = None) -> list[str]:
        """
        Executes a batch of XML API commands (as strings) and returns their responses.

        Args:
            xml_commands (list[str]): List of XML-encoded command strings.
            api_type (str): API type parameter (default "op").
            api_action (str): API action parameter (optional).
            api_xpath (str): API xpath parameter (optional).

        Returns:
            list[str]: List of XML responses as strings.
        """
        headers = {
            "Content-Type": "application/xml"
        }
        responses = []
        for xml_cmd in xml_commands:

            params = {
                "type": api_type,
                "cmd": xml_cmd,
                "key": self.api_key
            }
            if api_action:
                params["action"] = api_action
            
            url = f"https://{self.endpoint}/api?{urllib.parse.urlencode(params)}"

            resp = requests.post(url, data=xml_cmd.encode('utf-8'), headers=headers, verify=False)
            # need to raise for status.
            resp.raise_for_status()
            responses.append(resp.text)
        return responses



if __name__ == "__main__":
    import sys
    # if cli parameter is '--interactive', run interactive CLI on target.
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        if len(sys.argv) > 2 and sys.argv[2] is not None:
            endpoint = sys.argv[2]
        else:
            endpoint = input("Enter PanOS/Panorama IP/FQDN: ")

        try:
            creds = {
                "username": input("Username: "),
                "password": getpass.getpass("Password: ")
            }
            pano = PanOS(endpoint, username=creds["username"], password=creds["password"])

            print("Interactive PanOS CLI. Type 'exit' to quit.")

            while True:
                cmd = input(f"{creds.get('username')}@{endpoint}> ")
                if cmd.strip().lower() in ['exit', 'quit']:
                    break
                if not cmd.strip():
                    continue
                xml_cmd = build_xml_from_command(cmd)
                try:
                    responses = pano.batch_execute([xml_cmd])
                    for response in responses:
                        prettyprint_xml(response)
                except Exception as e:
                    print("Error:", e)
        except KeyboardInterrupt:
            print("\nExiting interactive CLI.")

    else:
        # print usage
        print("Script Usage: python3 panorama.py --interactive")