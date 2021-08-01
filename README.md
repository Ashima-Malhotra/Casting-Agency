# Casting Agency Application

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

# Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https:/docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https:/packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http:/flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https:/www.sqlalchemy.org/) and [Flask-SQLAlchemy](https:/flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

## Running the server

First ensure that you are working using your created virtual environment.

Before running the application locally, make the following changes in the `app.py` file in root directory:
- Replace the following import statements
  ```
    from database.models import db_drop_and_create_all, setup_db, Actors, Movies
    from controllers.auth import AuthError, requires_auth
  ```
  with
  ```
    from .database.models import db_drop_and_create_all, setup_db, Actors, Movies
    from .controllers.auth import AuthError, requires_auth
  ```
- Also, uncomment the line `db_drop_and_create_all()` on the initial run to setup the required tables in the database.

To run the server, execute:

```bash
export DATABASE_URL=https:/fsnd-casting-agency-app.herokuapp.com/=<database-connection-https:/fsnd-casting-agency-app.herokuapp.com/>

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

Setting the `FLASK_APP` to app.py for directing flask to find and run the application.
The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started

Base https:/fsnd-casting-agency-app.herokuapp.com/ : This application can be run locally.The application is hosted at https:/fsnd-casting-agency-app.herokuapp.com/
Authentication : This application requires authenticated users to run the application. All users have different permissions in order to use the application.All endpoints require various permissions , except the root endpoint , that are passed via ` Bearer ` token. 

The application has three different roles,

- Casting Assistant
    - Can view actors and movies
    - has permissions `get:actors` , `get:movies` , `get:movie-details` , `get:actor-details`

- Casting Director
    - All permissions of a `Casting Assistant`
    - Add/Delete an actor
    - Modify actors or movies
    - has permissions `get:actors` , `get:movies` , `get:movie-details`,`get:actor-details`,`post:actor`, `patch:actor` ,`patch:movie` ,`post:movie`

- Executive Producer
    - Al permissions of a `Casting Director`
    - Add/Delete a movie
    - has permissions `get:actors` , `get:movies` , `get:movie-details`,`get:actor-details`,`post:actor` , `delete:actor` , `patch:actor`,  `patch:movie`,`delete:actor` , `delete:movie`



## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "The requested https:/fsnd-casting-agency-app.herokuapp.com/ was not found on the server. If you entered the https:/fsnd-casting-agency-app.herokuapp.com/ manually please check your spelling and try again.",
    "success": false
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request
 - 401: Unauthorized
 - 403 : Forbidden
 - 404: Not Found
 - 405: Method Not Allowed
 - 422: Unprocessable Entity
 - 500: Internal Server Error


## Endpoints

Root Endpoint 
#### GET/
- Root Endpoint 
- Public Endpoint requires no authentication
- Sample Request 
    `https:/fsnd-casting-agency-app.herokuapp.com/`
- Response Body
    {
    "Status": "Running!!"
    }


#### GET/actors
- Returns the list of actors 
- Requires `get:actors` permission 
- Sample Request 
    `https:/fsnd-casting-agency-app.herokuapp.com/actors` 
- Response Body

  {
    "actors": [
        {
            "id": 3,
            "name": "Tom Hanks"
        },
        {
            "id": 2,
            "name": "Anam Hanks"
        }
    ],
    "success": true
}   

#### GET/actors-details / {actor_id}
- Returns the full information of an actor 
- Requires `get:actor-details` permission 
- Sample Request 
    `https:/fsnd-casting-agency-app.herokuapp.com/actor-details/2` 
- Response Body  

    {
    "actor": [
        {
            "age": 50,
            "gender": "Female",
            "id": 2,
            "movies": [],
            "name": "Anam Hanks"
        }
    ],
    "success": true
}     

#### GET/movies
- Returns the list of movies 
- Requires `get:movies` permission 
- Sample Request 
    `https:/fsnd-casting-agency-app.herokuapp.com/movies` 
- Response Body

   {
    "movies": [
        {
            "id": 1,
            "release_year": 2019,
            "title": "Knives Out"
        }
    ],
    "success": true
}

#### GET/movie-details / {movie_id}
- Returns the full information of an movie 
- Requires `get:movie-details` permission 
- Sample Request 
    `https:/fsnd-casting-agency-app.herokuapp.com/movie-details/2` 
- Response Body
    {
        "movies" :
            {
            'title': "Greyhound",
            'release_year': 2023,
            'movie_rating':4.6,
            'cast' :[
                    "Brad Pitt" , "Tom Hary"
                ]
            },
        "success" : true
    }       

#### POST /movies
- Creates a new movie
- Requires `post:movie` permission
- Sample Request 
    `https:/fsnd-casting-agency-app.herokuapp.com/movies` 
 - Request Body
   - title: string, required
   - release_year: integer, required
   - movie_rating: float, required
   - cast: array of string, non-empty, required
 
 - NOTE
   - Actors passed in the `cast` array in request body must already exist in the database prior to making this request.
   - If not, the request will fail with code 422.
- Request Body
        {
            "title": "Knives Out",
            "release_year": 2019,
            "movie_rating": 4.6,
            "cast": ["Anad de Armas"]
        }

- Response Body
{
    "created_movie_id": 3,
    "success": true
}

#### PATCH /movies/{movie_id}
 - General
   - Updates the details for a movie
   - Requires `patch:movie` permission
 
 - Request Body (at least one of the following fields required)
   - title: string, optional
   - release_year: integer, optional
   - movie_rating: float, optional
   - cast: array of string, non-empty, optional
 
 - NOTE
   - Actors passed in the `cast` array in request body will completely replace the existing relationship.
   - So, if you want to append new actors to a movie, pass the existing actors also in the request.
 
 - Sample Request
   - `https:/fsnd-casting-agency-app.herokuapp.com/movies/3`
 - Request Body
       {
            "movie_rating": 8.1
       }

- Response Body       
{
    "movie": {
        "cast": [],
        "id": 1,
        "movie_rating": 8.1,
        "release_year": 2019,
        "title": "Knives Out"
    },
    "success": true
}


#### DELETE /movies/{movie_id}
- Deletes the movie
- Requires `delete:movie` permission
 
- Sample Request
   - `https:/fsnd-casting-agency-app.herokuapp.com/movies/3`

- Request Body
{
    "deleted_movie_id": 3,
    "success": true
}

#### DELETE /actors/{actor_id}
- Deletes the actors
- Requires `delete:actor` permission
 
- Sample Request
   - `https:/fsnd-casting-agency-app.herokuapp.com/actors/3`

- Request Body
{
    "deleted_actor_id": 2,
    "success": true
}

#### PATCH /actors/{actor_id}
- General
   - Updates the details for an actor
   - Requires `patch:actor` permission
- Request Body (at least one of the following fields required)
    - name: string, optional
    - age: Integer, optional
    - gender:string,optional
- Sample Request
   - `https:/fsnd-casting-agency-app.herokuapp.com/actors/3`
- Request Body
       {
            "name": "Tom Hanks"
       }
- Response Body       
{
    "actor": {
        "age": 70,
        "gender": "",
        "id": 3,
        "movies": [],
        "name": "Tom Hanks"
    },
    "success": true
}

#### POST /actors
- General
   - Creates a new actor
   - Requires `post:actor` permission
 
 - Request Body
   - name: string, required
   - age: Integer, required
   - gender: string,optional

- Sample Request
   - `https:/fsnd-casting-agency-app.herokuapp.com/actors`
- Request Body
        {
            "name": "Ana de Armas",
            "age": 50,
            "gender": "Female"
        }
- Response Body
{
    "created_actor_id": 4,
    "success": true
}



## Testing
For testing the backend, run the following commands (in the exact order):
```
dropdb casting_test
createdb casting_test
psql casting_test  database.sql
python test.py
```
