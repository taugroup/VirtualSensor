echo ‘Starting DjangoQ’
#nohup python manage.py qcluster | tee /dev/stdout &
echo ‘Starting server’
python manage.py runserver 0.0.0.0:8888
#exec gunicorn django.wsgi:application -w 5 -b :8000 --capture-output --log-level=info --reload
