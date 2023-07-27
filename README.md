# alice-smart-home

## Установка

### Настройка навыка
* Склонируйте репозиторий к себе на сервер
* Идём на https://dialogs.yandex.ru/ и нажимаем "Создать навык" -> "Создать диалог" -> "Умный дом"
* Заполняем название (не принципиально)
* Заполняем Endpoint URL: https://_ваш-домен_/
* Не показывать в каталоге -> ставим галочку
* Официальный навык -> нет
* Заполняем остальные поля и загружаем иконку
#### Связка аккаунтов
* Придумываем, запоминаем и вписываем идентификатор приложения и секрет
* URL авторизации: https://_ваш-домен_/auth/
* URL для получения токена: https://_ваш-домен_/token/
* "Опубликовать" на странице "Настройки"
### config.py 
  * Отредактируйте __config.py__ и введите __IDAPP__ и __SECRET__, 
  которые вы указали, также укажите __IDDIALOG__(В навыке вкладка "общие сведения",
__TOKEN_USER__(https://yandex.ru/dev/dialogs/smart-home/doc/reference-alerts/resources-alerts.html
внизу страницы есть ссылка на получение, так же  Http настройки, там где будет запущен python сервис,
Mqtt, то что мы будем слушать, и куда слать сообщения


* Создайте файл _имя-устройства_.json в директории __devices/data__ (имя устроства должно быть уникальным)
можно для удобства внутри папки data создавать подпапки, но это не обязательно, считывания json файлов
идет рекурсивно. Внутри файла напишите JSON с описанием устройства в соответствии с документацией Яндекса: https://yandex.ru/dev/dialogs/alice/doc/smart-home/concepts/device-types-docpage/.
####Важно:
    * В capabilities указаны свойства, которые меняются с помощью яндекса, в них есть параметры 
state/instance содержимое которых должно совпадать с названием в mqtt/"то что указано в instance".
"set", то куда мы будем слать результат с яндекса, а listen, откуда будем принимать изменения свойств с устройств.

  Например:
```json
{
    "name": "Свет",
    "room": "Комната",
    "type": "devices.types.light",
    "mqtt": {
        "on": {
            "set": "/devices/yandex/controls/light2/on",
            "listen": "/devices/yandex/controls/light2/on/out"
        },
        "rgb": {
            "set": "/devices/yandex/controls/light2/rgb",
            "listen": "/devices/yandex/controls/light2/rgb/out"
        },
        "brightness": {
            "set": "/devices/yandex/controls/light2/brightness",
            "listen": "/devices/yandex/controls/light2/brightness/out"
        },
        "temperature_k" : {
             "set": "/devices/yandex/controls/light2/temperature_k",
            "listen": "/devices/yandex/controls/light2/temperature_k/out"
        }
    },
    "capabilities": [
        {
            "type": "devices.capabilities.on_off",
            "retrievable": true,
            "state": {
                "instance": "on",
                "value": true
            }
        },
        {
            "type": "devices.capabilities.range",
            "retrievable": true,
            "parameters": {
                "instance": "brightness",
                "unit": "unit.percent",
                "range": {
                    "min": 0,
                    "max": 100,
                    "precision": 1
                }
            },
            "state": {
                "instance": "brightness",
                "value": 10
            }
        },
        {
            "type": "devices.capabilities.color_setting",
            "retrievable": true,
            "parameters": {
                "color_model": "rgb",
                "temperature_k": {
                    "min": 2000,
                    "max": 8500,
                    "precision": 500
                }
            },
            "state": {
                "instance": "rgb",
                "value": 0
            }
        }
    ]
}
```



* Откройте вкладку "Тестирование" в панели управления Яндекс диалогами и попробуйте связать аккаунты, используя ваши имя пользователя и пароль
* Проверяйте, должно работать как в панели для тестирования, так и на всех устройствах привязанных к вашему аккаунту

## Информация
* Запускать alice.py
я создал 40 лампочек для тестирования, у одной половины ссылки на mqtt брокера одинаковые, и у другой, поэтому не пугайтесь если по одному запросу половина лампочек включается или выключается)
так же есть термостат с меняющейся температурой, и режимом работы для примера.
* ##### user для авторизации в сервисе
  *  **username: admin** 
  * **password: admin**
# Класс Devices
* Метод отвечающий за обработку сообщения с mqtt __mqtt_message
* Метод отвечающий за отправку сообщений actionMethod
* я 