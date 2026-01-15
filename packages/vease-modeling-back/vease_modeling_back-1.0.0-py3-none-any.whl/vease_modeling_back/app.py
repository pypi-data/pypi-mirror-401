# Standard library imports

# Third party imports
import flask
from opengeodeweb_back.app import create_app, run_server

# Local application imports
import vease_modeling_back.routes.blueprint_create as blueprint_create


def run_vease_modeling_back() -> flask.Flask:
    app = create_app(__name__)
    app.register_blueprint(
        blueprint_create.routes,
        url_prefix="/vease_modeling_back",
        name="create",
    )
    run_server(app)
    return app


if __name__ == "__main__":
    run_vease_modeling_back()
