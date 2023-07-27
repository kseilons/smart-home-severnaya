import logging

class Http:
    host = '0.0.0.0'
    port = 5000
class Mqtt:
    host = 'localhost'
    port = 1883
    username = 'kseilons'
    password = '8713177'

class YandexClient:
    IDAPP = "severnayaClient"
    SECRET = "severnayaClient"
    IDDIALOG = 'a577880f-a282-444d-ab3e-cfb97b808227'
    TOKEN_USER = 'y0_AgAAAAASP8LaAAT7owAAAADoOVQCVsIXj6fbRBCMh1Kv7rk0osCt6jI'


class LogConfig:
    # Uncomment to tune logging
    #FILE = "/var/log/alice.log"
    LEVEL = logging.DEBUG
    # FORMAT = "[%(asctime)s] [%(levelname)s] [%(remote_addr)s] [%(user)s]: %(message)s"
    # DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
