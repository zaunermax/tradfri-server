from flask import Flask, request, Response, json
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json
from os import environ

app = Flask(__name__)

CONFIG_FILE = 'tradfri.conf'

config = load_json(CONFIG_FILE)
psk_id = config["identity"]
psk = config["key"]
host = config["host"]

api_factory = APIFactory(host=host, psk_id=psk_id, psk=psk)


def safeParseInt(string):
    try:
        return int(string)
    except ValueError:
        return None


@app.route('/blinds', methods=['PUT'])
def handle_blinds():
    state = safeParseInt(request.args.get('state'))

    if state is None or state < 0 or state > 100:
        return Response(response='Error, no or wrong state defined.', status=400)

    api = api_factory.request
    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    blinds = [dev for dev in devices if dev.has_blind_control]

    for blind in blinds:
        api(blind.blind_control.set_state(state))

    return Response(status=204)


@app.route('/blinds', methods=['GET'])
def get_blind_status():
    api = api_factory.request
    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    blinds = [dev for dev in devices if dev.has_blind_control]
    status = {}

    for blind in blinds:
        status[blind.name] = {
            'battery': blind.device_info.battery_level,
            'position': blind.blind_control.blinds[0].current_cover_position
        }

    return Response(response=json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    host = '0.0.0.0' if environ.get('FLASK_ENV') == 'production' else '127.0.0.1'
    app.run(host=host, port=5000)
