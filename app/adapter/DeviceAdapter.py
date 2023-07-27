from flask import request, jsonify
import json

from app import devicesService, app
from app.tokens.token import Token


def getDevices():
    devices = devicesService.getDevices()
    user_id = Token.get_id()
    if user_id == None:
        return "Access denied", 403
    request_id = request.headers.get('X-Request-Id')
    app.logger.debug(f"devices request #{request_id}")
    result = {'request_id': request_id, 'payload': {'user_id': user_id, 'devices': devices}}
    json_string = json.dumps(result, indent=4, ensure_ascii=False)
    print(json_string)
    app.logger.debug(f"devices response #{request_id}: \r\n{json_string}")
    return jsonify(result)

def query():
    user_id = Token.get_id()
    if user_id is None:
        return "Access denied", 403
    request_id = request.headers.get('X-Request-Id')
    r = request.get_json()
    app.logger.debug(f"query request #{request_id}: \r\n{json.dumps(r, indent=4)}")
    devices_request = r["devices"]
    result = {'request_id': request_id, 'payload': {'devices': []}}
    # For each requested device...
    for device in devices_request:
        try:
            device_info = devicesService.getDeviceInfo(device["id"])
            result['payload']['devices'].append(device_info)
        except:
            app.logger.warning("Пустое устройство, не хватает каких-либо полей, либо оно было удалено")
    app.logger.debug(f"query response #{request_id}: \r\n{json.dumps(result, indent=4)}")
    return jsonify(result)


def action():
    user_id = Token.get_id()
    if user_id is None:
        return "Access denied", 403
    request_id = request.headers.get('X-Request-Id')
    r = request.get_json()
    app.logger.debug(f"action request #{request_id}: \r\n{json.dumps(r, indent=4)}")
    devices_request = r["payload"]["devices"]
    result = {'request_id': request_id, 'payload': {'devices': []}}
    # For each requested device...
    for device in devices_request:
        # Check that user can access this device
        new_device = devicesService.actionMethod(device, app.logger)
        result['payload']['devices'].append(new_device)
    app.logger.debug(f"action response #{request_id}: \r\n{json.dumps(result, indent=4)}")
    return jsonify(result)