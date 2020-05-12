Setup Database:
Configure settings.py for Database credentials.
Make Migrations:
python manage.py makemigrations
Migrate:
python manage.py migrate
Create Superuser:
python manage.py createsuperuser
Create Groups:
Login to the admin site with the superuser and create below groups. Add superuser to the admin group. Every user must be a member of one of the groups.
admin, ghat, jahaji, manager, vessel, viewer
Import Essential Data:
Import District, GoodsType, MobileMoneyAccount, Position, Thana, VesselType data using admin site.
