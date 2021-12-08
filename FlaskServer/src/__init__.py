from flask import Flask, request, jsonify, make_response


def _initialize_blueprints(app) -> None:
    #Register Flask blueprints
    from src.resources.person import person
    app.register_blueprint(person)


def create_app() -> Flask:
    #Create an app by initializing components
    app = Flask(__name__)
    _initialize_blueprints(app) 

    
    #ping method to check if server is healthy
    @app.route("/_ping", methods=['HEAD'])
    def _ping():
    
        if request.method == "HEAD":
            return make_response(jsonify({}),200)
        else:
            return make_response(jsonify({}),405)
 
    return app
    



