docker-compose run --rm --service-port django
docker-compose run --rm -p 8000 django-vixem

docker-compose down --remove-orphans

docker-compose run django pytest -s -vv --disable-warnings billings/tests/test_rates_v2/test_domicilio.py::HomeDeliveryQueryTests

docker exec -i clicoh_dario_database_1  mysql -uclicohuser -pclicohpass clicohapp < compose/local/db/data/dump.sql

docker-compose run --rm django-vixem python vixem/manage.py startapp user
docker-compose run --rm django-vixem python vixem/manage.py startapp product


docker-compose run --rm django-vixem python vixem/manage.py createsuperuser
ocker-compose run --rm django-vixem python vixem/manage.py makemigrations
ocker-compose run --rm django-vixem python vixem/manage.py migrate








## Prompt discriminator
´´´
`_### Historial de Conversación (Vendedor/Cliente) ###
{HISTORY}

### Intenciones del Usuario ###

**HABLAR**: Selecciona esta acción si el cliente parece querer hacer una pregunta o necesita más información.
**COMPRAR**: Selecciona esta acción si el cliente muestra intención de realizar una compra.

### Instrucciones ###

Por favor, clasifica la siguiente conversación según la intención del usuario._`

´´´