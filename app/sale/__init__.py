from flask import Blueprint

sale = Blueprint('sales', __name__)

from . import views