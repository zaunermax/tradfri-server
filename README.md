## Personal Web server abstraction for Fyrtur blinds

This is a small project which aims to make controlling my Fyrtur blinds as easy as calling a rest api.

## Installation

To install the necessary dependencies, execute the script in the `scripts` folder.

Then you just need to install the lib via: `pip3 install pytradfri`.

## Config

You need to pass the config via environment variables (the easiest way is by adding a .env file in the root of the 
project):

The config must be in this form:

```
TRADFRI_ID = <key-identity>
TRADFRI_PSK = <pre-shared-key>
TRADFRI_IP = <bridge-ip>
```

You also need to create an api user on your gateway. After you installed all dependencies from the `pytradfri` package, 
you can simply use the now installed `coap-client` to create one.

```
coap-client -m post -u "Client_identity" -k "SECURITY_CODE" -e '{"9090":"IDENTITY"}' "coaps://IP_ADDRESS:5684/15011/9063"
# SECURITY_CODE = the security code under the gateway
# IDENTITY      = your api user
```

#### Important note

When deploying the project on production, the `FLASK_ENV` env variable must be set to `production` to configure the 
host to `0.0.0.0`. That way, the server binds itself to the ip of the host machine.