#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api")
app_auth = Blueprint("app_auth", __name__, url_prefix="/auth")

from api.views.branch import *
from api.views.auth import *
from api.views.drug import *
from api.views.employee import *
from api.views.transfer import *
from api.views.sale import *
from api.views.order import *

# from api.views.order import *
