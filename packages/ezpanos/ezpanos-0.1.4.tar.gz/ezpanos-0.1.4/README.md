# EZPanos

#### An Ergonomic and lightweight PanOS Utility Tool

## Installation
``` bash 
pip install ezpanos
```

## Quick Start
``` python
from ezpanos.ezpanos import PanOS
import getpass

creds = {
    "username": input("Username: "),
    "password": getpass.getpass("Password: ")
}
endpoint = "<Management interface IP"
connection = PanOS(endpoint, username=creds["username"], password=creds["password"])
print(connection.execute("show system info"))

```

## Using an API token

By default, the PanOS class will use username/password to generate an authentication token from PanOS. This can however, be overridden if you already have it.

``` python
from ezpanos.ezpanos import PanOS

endpoint = "<Management interface IP"
connection = PanOS(endpoint, api_key="xxxxxxxxxxxx")
print(connection.execute("show system info"))

```



Currently not feature rich but an ideal platform for executing arbitrary PanOS commands against firewalls and Panorama instances for a wide variety of use cases.