import json
import os
import traceback
import time

import paho.mqtt.client as mqtt
import requests as requests

from utils.listFiles import listFiles
from utils.stringConvert import str_to_bool, str_to_int
import config


class Devices:
    devices = []
    devices_mqtt_info = {}
    userId = 'demo_user'
    def __init__(self):
        self.__get_device()

        self.__initMqttClient()


    def __initMqttClient(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect

        self.client.on_message = self.__mqtt_message
        self.client.username_pw_set(config.Mqtt.username, config.Mqtt.password)

        self.client.connect(config.Mqtt.host, config.Mqtt.port, 60)

        self.client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        for device in self.devices:
            for instance, mqttSetting in device['mqtt'].items():
                client.subscribe(mqttSetting["listen"])
                matching_capabilities = []
                for capability in device['capabilities']:
                    state_instance = capability.get('state', {}).get('instance')
                    parameters_instance = capability.get('parameters', {}).get('instance')

                    if state_instance == instance or parameters_instance == instance:
                        matching_capabilities.append(capability)

                self.devices_mqtt_info.setdefault(mqttSetting["listen"], []).append({
                    "id": device['id'],
                    "capabilities": matching_capabilities
                })

        print(f"Connected with result code {rc}")

    def __mqtt_message(self, client, userdata, msg):
        url = f'https://dialogs.yandex.net/api/v1/skills/{config.YandexClient.IDDIALOG}/callback/state'
        headers = {
            'Authorization': f'OAuth {config.YandexClient.TOKEN_USER}',
            'Content-Type': 'application/json',
        }
        data = {
            "ts": time.time(),
            "payload": {
                "user_id": "admin",
                "devices": []
            }
        }
        for device in  self.devices_mqtt_info[msg.topic]:
            message = msg.payload.decode('utf-8')


            for capabilites in device['capabilities']:
                if (capabilites['state']['instance'] == 'on'):
                    message = str_to_bool(message)
                elif (capabilites['state']['instance'] == "brightness"):
                    message = int(message)
                elif (capabilites['state']['instance'] == "temperature"):
                    message = int(message)
                capabilites['state']['value'] = message
            data['payload']['devices'].append(device)
        print(data)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.text, response.status_code)

    def getDevices(self):
        return self.devices

    def sendMQTTQuery(self, device, instance, new_value):
        print(new_value)
        if instance == 'on':
             new_value = int(new_value)

        self.client.publish(device["mqtt"][instance]['set'], new_value)

    def actionMethod(self, update_device, logger):
        result = {'id': update_device['id'], 'capabilities': []}
        device = self.__get_device_by_id(update_device['id'])
        for update_capability in update_device['capabilities']:
            type = update_capability['type']
            instance = update_capability['state']['instance']
            for device_capability in device['capabilities']:
                # Если типы способностей совпадают
                if update_capability['type'] == device_capability['type']:
                    new_value = update_capability['state']['value']
                    print(new_value)
                    # Тогда обновляем значение
                    device_capability['state']['value'] = new_value
                    self.sendMQTTQuery(device, instance, new_value)

            try:
                result['capabilities'].append({
                    'type': type,
                    'state': {
                        "instance": instance,
                        "action_result": {
                            "status": 'DONE'
                        }
                    }
                })

            except Exception as ex:
                logger.error(traceback.format_exc())
                result['capabilities'].append({
                    'type': type,
                    'state': {
                        "instance": instance,
                        "action_result": {
                            "status": "ERROR",
                            "error_code": "INTERNAL_ERROR",
                            "error_message": f"{type(ex).__name__}: {str(ex)}"
                        }
                    }
                })

        return result

    def getDeviceInfo(self, id):
        result = {'id': id, 'capabilities': []}
        # Load device config
        device_info = self.__get_device_by_id(id)

        for capability in device_info['capabilities']:
            result['capabilities'].append(capability)
        return result

    def __get_device_by_id(self, id):
        for device in self.devices:
            if device['id'] == id:
                return device
        return None

#Получает устройства из файлов
    def __get_device(self):

        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

        file_paths = listFiles(directory)

        for file_path in file_paths:
            print(file_path)
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding="utf-8") as file:
                    device = json.load(file)
                    device_id = os.path.splitext(os.path.basename(file_path))[0]  # Extract id from filename
                    device['id'] = device_id  # Add id to device
                    print(device)
                    self.devices.append(device)

    def __del__(self):

        self.client.loop_stop()


