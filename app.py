from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Actors, Movies
from controllers.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # Uncomment the following line on the initial run to setup
    # the required tables in the database

    # db_drop_and_create_all()

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/')
    def health():
        return jsonify({'Status': 'Running!!'}), 200

    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actors(payload):
        actors = list(map(Actors.short, Actors.query.all()))

        return jsonify({
            "success": True,
            "actors": actors
        }), 200

    @app.route('/actor-details/<int:actor_id>')
    @requires_auth("get:actor-details")
    def get_actor_by_id(payload, actor_id):
        actor = list(
            map(Actors.long, Actors.query.filter(Actors.id == actor_id)))
        if not actor:
            abort(404)
        else :       
            return jsonify({
                "success": True,
                "actor": actor
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actor")
    def create_actor(payload):
        request_body = request.get_json()
        try:

            if 'name' not in request_body \
                    or 'age' not in request_body:
                raise KeyError

            if request_body['name'] == '' \
                    or request_body['age'] == '':
                raise ValueError

            gender = ''
            if 'gender' in request_body:
                gender = request_body["gender"]

            new_actor = Actors(request_body['name'], request_body['age'],
                               gender)
            new_actor.insert()

            return jsonify({
                "success": True,
                "created_actor_id": new_actor.id
            }), 200

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def update_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        request_body = request.get_json()
        if not actor:
            abort(404)
        try:
            if not bool(request_body):
                raise TypeError

            if "name" in request_body:
                if request_body["name"] == "":
                    raise ValueError

                actor.name = request_body["name"]

            if "gender" in request_body:
                if request_body["gender"] == "":
                    raise ValueError

                actor.gender = request_body["gender"]

            if 'age' in request_body:
                if request_body["age"] == "":
                    raise ValueError

                actor.date_of_birth = request_body["age"]

            actor.update()

            return jsonify({
                "success": True,
                "actor": actor.long()
            }), 200

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if not actor:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted_actor_id": actor.id
            }), 200

        except Exception:
            abort(400)

    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movies(payload):
        movies_query = Movies.query.order_by(Movies.id).all()
        movies = [movie.short() for movie in movies_query]

        return jsonify({
            "success": True,
            "movies": movies
        }), 200

    @app.route('/movie-details/<int:movie_id>')
    @requires_auth("get:movie-details")
    def get_movie_by_id(payload, movie_id):
        movie = list(
            map(Movies.long, Movies.query.filter(Movies.id == movie_id)))
        if not movie:
            abort(404)
        else:        
            return jsonify({
                "success": True,
                "movie": movie
            }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movie")
    def create_movie(payload):
        request_body = request.get_json()

        try:
            if 'title' not in request_body \
                    or 'release_year' not in request_body \
                    or 'movie_rating' not in request_body \
                    or 'cast' not in request_body:
                raise KeyError

            if request_body['title'] == '' \
                    or request_body['release_year'] <= 0 \
                    or request_body['movie_rating'] < 0 \
                    or request_body["movie_rating"] > 10 \
                    or len(request_body["cast"]) == 0:
                raise TypeError

            actors = Actors.query.filter(
                Actors.name.in_(request_body["cast"])).all()

            if len(request_body["cast"]) == len(actors):
                new_movie = Movies(
                    title=request_body['title'],
                    release_year=request_body['release_year'],
                    movie_rating=request_body['movie_rating'],
                )
                new_movie.cast = actors
                new_movie.insert()
            else:
                raise ValueError

            return jsonify({
                "success": True,
                "created_movie_id": new_movie.id
            }), 200

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def update_movie(payload, movie_id):
        request_body = request.get_json()
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            if not bool(request_body):
                raise TypeError

            if "title" in request_body:
                if request_body["title"] == "":
                    raise ValueError

                movie.title = request_body["title"]

            if "release_year" in request_body:
                if request_body["release_year"] <= 0:
                    raise ValueError

                movie.release_year = request_body["release_year"]

            if "movie_rating" in request_body:
                if request_body["movie_rating"] < 0 \
                        or request_body["movie_rating"] > 10:
                    raise ValueError

                movie.movie_rating = request_body["movie_rating"]

            if "cast" in request_body:
                if len(request_body["cast"]) == 0:
                    raise ValueError

                actors = Actors.query.filter(
                    Actors.name.in_(request_body["cast"])).all()

                if len(request_body["cast"]) == len(actors):
                    movie.cast = actors
                else:
                    raise ValueError

                movie.update()

            return jsonify({
                "success": True,
                "movie": movie.long()
            }), 200

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted_movie_id": movie.id
            }), 200

        except Exception:
            abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unauthorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": 'Forbidden Access'
        }), 500
    return app


app = create_app()
