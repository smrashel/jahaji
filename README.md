Clone the application:
git clone https://github.com/smrashel/jahaji.git

Create Virtual environment:
virtualenv venv

Activate venv:
vevn\scripts\activate

Install required packages (cd /path/to/requirements.txt):
pip install requirements.txt

Setup Database:
Configure settings.py for Database credentials.

Make Migrations:
python manage.py makemigrations

Migrate:
python manage.py migrate

Create Superuser:
python manage.py createsuperuser

Serve the development server:
python manage.py runserver

Create Groups:
Login to the admin site with the superuser and create below groups. Add superuser to the admin group. Every user must be a member of one of the groups.
admin, ghat, jahaji, manager, vessel, viewer

Import Essential Data:
Import District, GoodsType, MobileMoneyAccount, Position, Thana, VesselType data using admin site.
