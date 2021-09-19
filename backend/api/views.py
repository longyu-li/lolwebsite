from flask import Blueprint, jsonify, request
#from sqlalchemy.ext.declarative.api import as_declarative
from . import db 
from .models import Summoner
from flask_cors import CORS
import apimain

main = Blueprint('main', __name__)

@main.route('/<input_region>/<input_name>')
def search(input_region, input_name):
    
    return run_api(input_name, input_region), 201