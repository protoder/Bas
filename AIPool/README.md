# Система распознавания тонущих людей в бассейне

## Содержание  

- [Модель распознавания](#модель-распознавания)  
- [Стрим-сервер](#стрим-сервер)  
- [WEB-сервер](#web-сервер)   
- [Docker](#docker)  

## Модель распознавания

![](https://img.shields.io/badge/python-3.10.9-blue)
![](https://img.shields.io/badge/torch-1.13.1-red)
![](https://img.shields.io/badge/yolo-8-purple)

Каталог моделей находится в директории `/model`

За использование модели отвечают переменные окружения:

```
set MODEL_NAME=yolo5
set MODEL_BEST=yolo5m.pt
```

## Установка

Установите необходимые зависимости  `pip install -r model/requirements.txt`

- Пример распознавания

Создаём экземпляр класса:

```
from bass import Bass_detect
detect = Bass_detect()
```

Запускаем распознавание данных:

```
result = detect.detect_human('./test/imgt4297.jpg')
```

На выходе получаем данные в виде словаря и флага.

```
result = [['5_Water', 627.50439453125, 0.0, 1882.718017578125, 1440.0],
 ['2_HumanHorizontal_HeadAboveWater', 1601.5428466796875, 849.74267578125, 512.1766357421875, 526.805419921875], 
 ['2_HumanHorizontal_HeadAboveWater', 1057.7447509765625, 255.93756103515625, 300.33447265625, 383.01837158203125]]
```

## Примечание

- Хотелось бы грузить модель в бэк торча, без установки всех зависимостей:

```
self.model = torch.load("best.pt")
```

- Обучить YOLOv8.

# Стрим-сервер

![](https://img.shields.io/badge/python-3.10.9-blue)
![](https://img.shields.io/badge/fastapi-0.95.0-red)
![](https://img.shields.io/badge/opencv-python-4.6.0.66-yellow)

Каталог с сервером находится в директории `back`

## Установка

- Создайте виртуальное окружение:

```
python -m venv venv
```

Активируйте его:

```
#Windows
venv/Script/activate
```

```
#Linux
venv/bin/activate
```

- Устанавливаем необходимые библиотеки:

```
pip install -r back/requirements.txt
```

## Запуск

- Задайте **rtsp** для видео: 

```
#Windows
set STREAM_SRC=rtsp://...
```

```
#Linux
export STREAM_SRC=rtsp://...
```

- Запуск сервера

```
python back
```

```
#Windows
start.bat
```


## Переменные окружения

* STREAM_SRC - исходный источник, примеры: `rtsp://...` или `0` - web-камера
* STREAM_QUALITY - параметр качества сжатия, от 1 до 100, где 100 наилучшее качество, по умолчанию 50
* APP_DEBUG - флаг запуска Flask с дебагом
* APP_HOST - задается хост сервиса, по умолчанию любой `0.0.0.0`
* APP_PORT - порт запуска сервиса, по умолчанию 8000.
* APP_PUB, APP_SEC - пути до ssl-сертификатов (.crt, .key).


# WEB-сервер

![](https://img.shields.io/badge/vue.js-3.2.4-green)
![](https://img.shields.io/badge/vuetify-3.1.6-blue)
![](https://img.shields.io/badge/vuex-4.0.0-green)
![](https://img.shields.io/badge/materialdesignicons-6.1.95-yellow)

Фронтовая часть базируется на хостинге reg.ru.

## На reg.ru

- Виртуальное окружение `/opt/python/python-3.10.1/bin/python -m venv aipool`.
- Настроен Flask и окружение.
- Базовая добавлен фрон: лендинг (пока пустой) и демопанель.


# Docker

## Запуск

```
docker-compose up --build
```

