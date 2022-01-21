release: python manage.py migrate
web: daphne socialiga.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A socialiga worker --pool=solo -L info
celerybeat: celery -A socialiga beat -L INFO
celeryworker: celery -A socialiga worker & celery -A socialiga beat -L INFO & wait -n