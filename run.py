import os
import logging.config

from api.restplus import api
from flask import Blueprint
from api.features_flag.endpoints.features import ns as features_namespace
from api.prices.endpoints.prices import ns as prices_namespace
from api.accounts.endpoints.accounts import ns as accounts_namespace
from api.favorites.endpoints.favorites import ns as favorites_namespace
from app import create_app
from config import settings


app = create_app()
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(features_namespace)
api.add_namespace(prices_namespace)
api.add_namespace(accounts_namespace)
api.add_namespace(favorites_namespace)
app.register_blueprint(blueprint)


def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
