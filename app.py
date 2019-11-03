from flask import Flask, request, Response, json
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json

app = Flask(__name__)

CONFIG_FILE = 'tradfri.conf'

config = load_json(CONFIG_FILE)
psk_id = config["identity"]
psk = config["key"]
host = config["host"]

api_factory = APIFactory(host=host, psk_id=psk_id, psk=psk)


@app.route('/blinds', methods=['PUT'])
def handle_blinds():
    action = request.args.get('action')

    if action is None:
        return Response(response='Error, no action defined.', status=400)

    if action != 'open' and action != 'close':
        return Response(response='Error, wrong action: [' + action + ']', status=400)

    api = api_factory.request
    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    blinds = [dev for dev in devices if dev.has_blind_control]
    state = 0

    if action == 'close':
        state = 100

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
    app.run()
