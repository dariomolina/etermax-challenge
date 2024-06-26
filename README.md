# etermax-challenge

# Documentación del Microservicio de Precios de Bitcoin

## Introducción

Este documento describe la configuración y funcionalidad de un microservicio construido 
utilizando Docker y Docker Compose. El microservicio realiza llamadas recurrentes a un 
servicio REST externo para obtener el precio del Bitcoin en pesos argentinos, almacena los 
datos en una base de datos Redis y proporciona una API REST con varias funcionalidades. 
Además, incluye una suite de pruebas unitarias.

## Versiones de Software

### Docker

- **Versión:** 20.10.18

### Docker Compose

- **Versión:** v2.19.1

## Imágenes de Docker

### Python

- **Nombre de la imagen:** python
- **Etiqueta (tag):** 3.12.3

### Redis

- **Nombre de la imagen:** redis
- **Etiqueta (tag):** 7.2.5-alpine


## Framework API REST

Para el desarrollo de este proyecto, se usó Django REST Framework, que es una 
herramienta de Django que busca crear APIs Web robustas y eficientes.
La desición de usar este framework es su facilidad de uso, flexibilidad y conjunto 
de características extensas lo convierten en una opción preferida para el desarrollo 
de este microservicio.

## Persistencia de los datos

La base de datos seleccionada para almacenar la data del precio del Bitcoin y 
timestamp, fue Redis. La desición del uso de la misma fue que me resultó interesante
probar esta db y salir de lo tradicional para la persistencia de los datos (mongo por
ejemplo), para el desarrollo del proyecto. Claramente la db de redis, en algún lapso 
de tiempo muy extendido, habrá generado un volumen de datos muy grande y no es la 
mejor la opción para un marco de trabajo productivo. 
También usé Redis como broker de mensajería, donde recibe tareas de la aplicación y 
las pone en una cola.

## Librerías Usadas

- **Celery:** 5.4.0
- **Django:** 5.0.4
- **Django Rest Framework (DRF):** 3.15.1
- **Django Celery Beat:** 2.6.0
- **Django CORS Headers:** 4.3.1
- **Django Redis:** 5.4.0
- **Pytest:** 8.2.1
- **Python Dotenv:** 1.0.1
- **Requests:** 2.32.3

## Sobre Docker y docker-compose

El Proyecto se realizó aplicando un entorno de docker y docker-compose.

Docker es una plataforma de contenedorización que permite a los desarrolladores empaquetar 
aplicaciones y sus dependencias en contenedores.

Docker Compose es una herramienta para definir y ejecutar aplicaciones Docker 
multi-contenedor. Con Docker Compose, puedes utilizar un archivo YAML para configurar los 
servicios de tu aplicación, incluyendo contenedores, redes, y volúmenes.

Archivo de docker-compose.yml
```
version: '3.9'

services:
  etermax-api-service:
    container_name: etermax_api_service
    build:
      context: .
      dockerfile: compose/local/django/Dockerfile
    restart: always
    command: /start
    volumes:
      - ./etermax_api_service:/app
    ports:
      - 8000:8000
    env_file:
      - .env
    depends_on:
      - redis
    networks:
      etermax-network:
    stdin_open: true
    tty: true

  redis:
    container_name: redis
    image: redis:7.2.5-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/root/redis
      - redis.conf:/usr/local/etc/redis/redis.conf
    env_file:
      - .env
    networks:
      etermax-network:

  celery:
    container_name: celery
    build:
      context: .
      dockerfile: compose/local/django/Dockerfile
    command: /start-celeryworker
    volumes:
      - ./etermax_api_service:/app
    env_file:
      - .env
    depends_on:
      - redis
      - etermax-api-service
    networks:
      etermax-network:

  celery-beat:
    container_name: celery-beat
    build:
      context: .
      dockerfile: compose/local/django/Dockerfile
    command: /start-celerybeat
    env_file:
      - .env
    volumes:
      - ./etermax_api_service:/app
    depends_on:
      - redis
      - etermax-api-service
    networks:
      etermax-network:

volumes:
  etermax-api-service:
  redis_data:
  redis.conf:

networks:
  etermax-network:
```

Tenemos definidos 4 servicios: 
* etermax-api-service: que contiene y ejecuta el microservicio generado
* redis: servicio que usaremos para la persistencia de datos y también como broker de mensajería
* celery: servicio encargado de ejecutar los workers que realizan las tareas en segundo plano
* celery-beat: servicio destinado a programar las tareas


## Funcionalidad del Microservicio

### Llamada Recurrente al Servicio REST

El microservicio realiza una llamada recurrente cada 10 segundos al servicio REST para 
obtener el precio del Bitcoin en pesos argentinos:

- **URL:** [Buenbit API - Market Tickers](https://be.buenbit.com/api/market/tickers)

### Almacenamiento en Redis

Los datos obtenidos se almacenan en una base de datos Redis como pares clave-valor en la siguiente estructura:

- **Clave (key):** `"prices"`
- **Valor (value):** `{price:timestamp}`

### Definicion de herramientas usadas para la ejecución de tareas recurrentes

Celery es una biblioteca de Python utilizada para manejar la ejecución de tareas en segundo 
plano (asíncronas) de manera distribuida. Esto es especialmente útil para operaciones que 
requieren mucho tiempo de procesamiento, como el envío de correos electrónicos, procesamiento 
de imágenes, cálculos complejos, etc. Celery puede distribuir estas tareas entre múltiples 
trabajadores, lo que mejora la eficiencia y el rendimiento de la aplicación.

Celery Beat es un programador de tareas para Celery. Permite programar tareas que se ejecuten 
en intervalos regulares, como un cron job. Celery Beat se encarga de enviar mensajes a la cola 
de tareas de Celery en los intervalos definidos, y los trabajadores de Celery ejecutan las 
tareas.

Redis se utiliza comúnmente como broker de mensajes para Celery. El broker de mensajes es 
responsable de almacenar las tareas y entregarlas a los trabajadores. Redis es rápido y 
eficiente, lo que lo convierte en una opción popular para este propósito.

En resumen, el uso particular de este caso de uso:
* Celery: Ejecuta tareas asíncronas y distribuidas (corre en segundo plano la función de 
hacer un request a la api de buenbit y procesar la data y luego almacenarla en redis).
* Celery Beat: Programa tareas periódicas. (se encarga de programar la tarea de ejecución
de nuestro método para realizar la requesta a buenbit y almacenamiento posterior en redis)
* Redis: Actúa como broker de mensajes, gestionando la cola de tareas. (en nuestro caso,
se encarga del almacenamiento y gestión de las tareas programadas mensionadas anteriormente
y también cumple la función de almecenamiento de toda la data que proviene de la buenbit
luego de procesarla)


#### Almacenamiento de Precio de Bitcoin y proceso de ejecución tareas recurrentes

Cada 10 segundos, se obtiene el precio del Bitcoin en pesos argentinos en un cierto 
timestamp, usando la api de buenbit y se almacena en la base de datos Redis usando 
la librería `django-redis`.

Para lograr la recurrencia cada 10 segundo a la api de Buenbit y almacenarla en la base de 
datos de redis usamos celery, celery-beat y redis (para el almacenamiento de las tasks)

Los procesos que realizan son los siguientes:

1. Definición de Tareas: Las tareas que se desean ejecutar en segundo plano se definen en el 
código como funciones normales de Python. Estas funciones las anotamos con el decorador 
@shared_task o @task proporcionado por Celery.

2. Configuración del Broker: Celery necesita un broker de mensajes para comunicarse entre el
cliente (donde se definen las tareas) y los trabajadores (donde se ejecutan las tareas). 
Redis se configura como el broker de mensajes en el archivo de configuración de Celery, 
llamano celery_app.py en nuestro caso.

3. Envío de Tareas: Cuando una tarea se envía, Celery la pone en una cola en el 
broker (Redis). La tarea puede enviarse para ejecución inmediata o programada para 
ejecución futura.

4. Workers: Los workers de Celery son procesos que escuchan en la cola de tareas
y ejecutan las tareas cuando se entregan.

5. Celery Beat: Para tareas periódicas, Celery Beat envía tareas a la cola de Celery en 
intervalos de 10 segundos. Esto se configura en el archivo celery_app.py donde se define 
cuándo y con qué frecuencia deben ejecutarse las tareas.


### API REST con Django Rest Framework

La API REST proporcionada por el microservicio tiene las siguientes funcionalidades:

#### a) Obtener Promedio de Precio

Un endpoint que permite obtener el promedio de precio entre dos timestamps ingresados por 
parámetros.

#### b) Obtener Datos Paginados

Un endpoint para obtener de forma paginada los datos almacenados, con o sin filtro de 
timestamp.


## Ejecución y uso del Microservicio
Para levantar el proyecto, debemos ubicarnos en la carpeta donde se encuentra el 
archivo docker-compose.yml (en la carpeta principal) y ejecutar siguientes pasos

+ Ejecutar el comando para generar las imágenes del proyecto (se ejecuta solamente 
una única vez para construír la imágen e instalar todas las dependencias en ella)
```
docker-compose build
```

+ Para correr el proyecto
```
docker-compose up
```

## Endpoints

Luego de levantar el proyecto, podemos ingresar a los siguientes endpoints:


* ### Average price
Retorna el promedio de precio entre dos timestamps dados
Es requisito agregar los queryparams since y until para el funcionamiento correcto del endpoint
```
GET http://localhost:8000/api/ticker-average-price/?since=1717276416&until=1817135429
```
Respuesta:
```
{
    "average_price": 84873600.0
}
```

* ### Ticker price
Retorna un json con el valor del precio en el timestamp dado
```
GET http://localhost:8000/api/ticker-price/?timestamp=1717397498
```
Respuesta:
```
{
    "price": 86545000.0
}
```

* ### Ticker list
Retorna una lista paginada con toda la data relacionada al timestamp y al precio correspondiente

- page_size sirve para obtener una cantidad n de registros por cada página, en caso de no pasarle
ese argumento, por default se setea en 10
- page es usada pa la paginación y poder obtener info de una página u otra
- since y until son los filtros para el timestamp, con ellos obtenemos la info en relación los
datos que estén entre since y until. Estos queryparams son opcionales
```
http://localhost:8000/api/ticker-list/?page=1&since=1717137541&until=1817137589&page_size=5
```
Respuesta:
```
{
    "count": 11,
    "next": "http://localhost:8000/api/ticker-list/?page=2&page_size=5&since=1717137541&until=1817137589",
    "previous": null,
    "results": [
        {
            "timestamp": 1717184864,
            "price": 84873600.0
        },
        {
            "timestamp": 1717184874,
            "price": 84873100.0
        },
        {
            "timestamp": 1717184904,
            "price": 84850500.0
        },
        {
            "timestamp": 1717184914,
            "price": 84849600.0
        },
        {
            "timestamp": 1717184924,
            "price": 84823600.0
        }
    ]
}
```



## Tests
Se utilizó pytest como herramienta de testing para Python.

* Se realizaron tests de integración para los endpoints average-price y 
ticker-list de la API de Ticker. Se utilizaron unittest.mock, APITestCase y 
APIClient para simular y probar la funcionalidad de la API sin realizar conexiones 
reales a Redis. 
Estos tests se encuentran en la ruta etermax_api_service/ticker/tests.py

* Se realizaron tests de integración en postman para testear los endpoints average-price y 
ticker-list. En general validan que las respuestas sean 200, 400 y validaciones de campos
en las respuestas de los json. Uno de los test agregados espera 22 segundos para darle 
tiempo a los procesos de cargar datos en redis y validar que los resultados no traigan 
una lista de elementos vacia.
Estos tests se exportraron desde postman y se encuentran en la ruta 
etermax_api_service/etermax-integrations-tests.json

* Se generaron tests unitarios para los metodos que realizan las peticiones a la api de
buenbit. Se mockean la requests get para simular una respuesta de la api de buenbit y 
testear los casos exitos y excepciones. Estos tests se encuentran en la ruta 
etermax_api_service/services/buenbit/tests.py .

Se generaron 11 tests en le proyecto, más los test de integración en postman

Para poder ejecutar los tests debemos ubicarnos en la carpeta donde se en
cuentra el 
archivo tests.yml (en la carpeta principal) y correr el siguiente comando
```
docker-compose -f tests.yml run --rm pytest
```
