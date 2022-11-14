#!/bin/bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
mv -f db.sqlite3 db.sqlite3.save
./manage.py makemigrations
./manage.py migrate
rm -f dash.tar
rm -rf media/users
rm -f dash.tar
#./manage.py loaddata static/initial/sites.json static/initial/projects.json static/initial/users.json
./manage.py loaddata static/initial/users.json
