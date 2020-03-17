from flask import request, url_for
from requests import Response, post
from db import db

MAILGUN_DOMAIN = "sandbox95fec4d8db0e4fa19c93aaef1e714033.mailgun.org"
MAILGUN_API_KEY = "ff9c9ef496b1a6fb4b8f547cb5481099-9a235412-4e280db7"
FROM_TITLE = "My REST API"
FROM_EMAIL = "postmaster@sandbox95fec4d8db0e4fa19c93aaef1e714033.mailgun.org"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        # http://127.0.0.1:5000/
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                  "to": self.email,
                  "subject": "Registration Confirmation",
                  "text": f"Please click the "
                          f"link to finish registration:{link}!"})

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
