## Personal Web server abstraction for Fyrtur blinds

This is a small project which aims to make controlling my Fyrtur blinds as easy as calling a rest api.

## Installation

To install the necessary dependencies, go over to [this](https://github.com/ggravlingen/pytradfri) project and follow the installation instructions there.

Then you just need to install the lib via: `pip3 install pytradfri`.

## Config

You need a config file in the root of your project: `tradfri.conf`

The config must be in this form:

```
{
    "identity": "<identity>",
    "key": "<pre-shared-key>",
    "host": "<gateway-ip>"
}
```

You also need to create an api user on your gateway. After you installed all dependencies from the `pytradfri` package, 
you can simply use the now installed `coap-client` to create one.

```
coap-client -m post -u "Client_identity" -k "SECURITY_CODE" -e '{"9090":"IDENTITY"}' "coaps://IP_ADDRESS:5684/15011/9063"
# SECURITY_CODE = the security code under the gateway
# IDENTITY      = your api user
```