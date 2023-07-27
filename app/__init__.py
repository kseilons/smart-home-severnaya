
from flask import Flask

from utils.logger import setup_logger
from config import Http

app = Flask(__name__)
setup_logger(app)

from app.devices.devices import Devices
from app.users import user
devicesService = Devices()
userService = user

from app.adapter import DeviceAdapter
from app.adapter.UserAdapter import UserAdapter
deviceAdapter = DeviceAdapter
userAdapter = UserAdapter()

from app import router

app.run(host=Http.host, port=Http.port)
