from Flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views