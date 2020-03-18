import traceback
from flask_restful import Resource
from flask import request
from schemas.user import UserSchema
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from models.confirmation import ConfirmationModel
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from libs.strings import gettext

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        # no try except thanks to handle_marshmallow_validation
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_username_exists")}, 400

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, 400

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": gettext("user_registered")}, 201
        except MailGunException as e:
            # send confirmation email failed - delete user from db
            user.delete_from_db()
            return {"message": str(e)}, 500
        except:  # noqa: E722
            traceback.print_exc()
            user.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want
    to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are
    manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # no try except thanks to handle_marshmallow_validation
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))
        # partial - marshmallow will ignore email field during validation

        user = UserModel.find_by_username(user_data.username)
        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                # identity= is what the identity()
                # function did in security.py—now stored in the JWT
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token,
                        "refresh_token": refresh_token, }, 200
            return {"message": gettext("user_not_confirmed").format(
                user.username)}, 400
        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is JWT ID - uid for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
