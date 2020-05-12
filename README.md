# Jahaji Data

This is an application to help interested parties to store and retrieve Bangladeshi shipping crew data.

## Table of Contents

* Clone 
* Installation
* Adding Features
* Team
* FAQ
* Support
* License

## Clone
Clone the application:
`git clone https://github.com/smrashel/jahaji.git`

## Installation
* Create Virtual environment:
`virtualenv venv`

* Activate venv:
`venv\scripts\activate`

* Install required packages (cd /path/to/requirements.txt):
`pip install requirements.txt`

* Setup Database:
Configure settings.py for Database credentials.

* Make Migrations:
`python manage.py makemigrations`

* Migrate:
`python manage.py migrate`

* Create Superuser:
`python manage.py createsuperuser`

* Serve the development server:
`python manage.py runserver`

## Create Groups:
* Login to the admin site with the superuser and create below groups. Add superuser to the admin group. Every user must be a member of one of the groups.
admin, ghat, jahaji, manager, vessel, viewer

* Import Essential Data:
Import District, GoodsType, MobileMoneyAccount, Position, Thana, VesselType data using admin site.

## Team
* [smrashel](https://smrashel.github.io/portfolio/)

## FAQ
* Please ask me if you have any questions regarding the project.

## Support
* Please support me.

## License
* Copyright 2020 © [smrashel](https://smrashel.github.io/portfolio/)
