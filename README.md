Documentation for MeetAndEat feature
---

**Django** web framework is used in combination with django rest framework  for development of REST APIs.

**Swagger** and **Redoc** API documentation is available.

A **DB schema** is also available here: [MeetnEatDBUML](docs/MeetnEatDBUML.png)

Docker compose is used to setup a development environment.

Installation:
(Requires Docker)
---
* Clone the Repo
* Create a .env file from env_sample. Define the values marked with todo.
* Run: `docker compose up`
* Create an Admin user account: 
  * Find the docker container ID if for "meetneat_apis" by running `docker ps`
  * Run `docker exec -it <container_id> python manage.py createsuperuser `
* API Swagger Documentation: `http://127.0.0.1:8000/api/docs`
* API Redoc Documentation: `http://127.0.0.1:8000/api/redocs/`
* Docwnload open-api documentation: `http://127.0.0.1:8000/api/openapi/`
* Admin Panel for data management: `http://127.0.0.1:8000/admin/`
* API documents document is available in ./docs folder

Entities:
---
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