import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

from resources.user import (
    UserRegister,
    User,
    UserLogin,
    UserLogout,
    TokenRefresh,
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.confirmaton import Confirmation, ConfirmationByUser
from blacklist import BLACKLIST

from ma import ma
from db import db

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)  # /auth


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    This method will check if a token is blacklisted, and will be called
    automatically when blacklist is enabled
    """
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(Confirmation, "/user_confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")


@app.route('/')
def index():
    return "Possible endpoints: <h1>/items</h1> <h2>stores</h2> "


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True, host='0.0.0.0')
