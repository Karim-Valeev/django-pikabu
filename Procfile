release: python3 src/manage.py migrate && python src/manage.py loaddata src/main/fixtures/*.json
web: cd src && gunicorn django_pikabu.wsgi --log-file -
