# Restbucks

Investigating the demo app from [REST in Practice](https://www.oreilly.com/library/view/rest-in-practice/9781449383312/)


## Prerequisites
* Python >= 3.8
* [Poetry](https://python-poetry.org/)


## Getting Started
* Install dependencies: `poetry install`
* Start server: `make serve`
* Seed DB: `POST https://localhost:8000/seed`
* Access documentation: `GET https://localhost:8000/docs`


## Motivation
The original REST in Practice application was written with JAVA/.NET and XML over REST. While these are still perfectly valid, I wanted to see what the application would look like with Python and JSON.


### FastAPI vs. Flask
I am also making my life easier by using [FastAPI](https://fastapi.tiangolo.com/) instead of [Flask](https://flask.palletsprojects.com/). This is not a slight against Flask, it's a great tool that I've enjoyed using. But, FastAPI gives types and documentation with very little investment, which I think is essential for any modern REST API. Again, You can get the same thing with Flask, but not out of the box.


### Database
I didn't want to focus on the database. In the real world, I would spin up a [PostgreSQL Docker instance](https://hub.docker.com/_/postgres) and utilize Alembric[https://alembic.sqlalchemy.org/en/latest/]. I've defined types for application integration and ORM capabilities that would work with a more comprehensive database integration
