Documentation for MeetAndEat feature

This code was written in 2017 as a part of my Praktikum @TUM during my MS degree

Django web framework is used in combination with djangorestframework plugin for development of REST APIs.
Swagger is used for API documentation. A secondary documentation in .doc format is available here: [MeetnEat_API_doc](docs/MeetnEat_API_doc.pdf)
A DB schema is also available here: [MeetnEatDBUML](docs/MeetnEatDBUML.png)
The code is compaitble with Python3.

Installation:
    * Clone the Repo
    * Create Virtual Env with Python 3.5
    * Install requirements: pip install -r requirements
    * Install MariaDB and provide database details in foodgroups/setting.py file
    * Run Django Migration: python manage.py migrate
    * Run Development Server: python manage.py runserver
    * Create an Admin user account: python manage.py createsuperuser
    * API Swagger Documentation: localhost:8000/api/docs/
    * Admin Panel for data management: localhost:8000/admin/
    * API documents document is available in foodgroups/docs folder

Entities:
User:
    * User represents either students or staff members in the University

Events:
    * An Event represents a meetup of People/Users to cook/eat food together
    * An Event is created by one of the users and joined by others.
    * Users can add Messages in Event to communicate with other users
    * Users can add Meals in Event on which people can vote
    * Users can add ShoppingItems which they needs to buy for the Event

Preferences:
    * A Food Preferences represents the quality a user wants in the food e.g. high-protein, low-fat etc
    * User can choose from the list of preferences
    * Users will be displayed Events according to their preferences