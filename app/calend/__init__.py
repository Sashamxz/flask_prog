from flask import Blueprint

calend = Blueprint('calend', __name__)

from . import views