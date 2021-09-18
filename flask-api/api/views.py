from flask import Blueprint, jsonify, request

main = Blueprint('main', __name__)

@main.route('/add', methods=['POST'])
def add():

    return 'Done', 201

@main.route('/get')
def get():
    stuff = []

    return jsonify({'stuff' : stuff})