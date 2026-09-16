from .database import db
from datetime import datetime
class User(db.Model):
    __tablename__ = 'USERS'

    USER_ID = db.Column(db.String(255), primary_key=True)
    USER_NAME = db.Column(db.String(80), unique=True, nullable=False)
    USER_EMAIL = db.Column(db.String(120), unique=True, nullable=False)
    USER_PWD = db.Column(db.String(255))
    USER_PHONE = db.Column(db.String(20))
    USER_ADDRESS = db.Column(db.Text)
    USER_CITY = db.Column(db.String(100))
    USER_STATE = db.Column(db.String(100))
    USER_COUNTRY = db.Column(db.String(100))
    USER_ZIPCODE = db.Column(db.String(20))
    USER_LAT = db.Column(db.Float)
    USER_LONG = db.Column(db.Float)
    USER_TYPE = db.Column(db.String(20), default="B") # B -> buyer; A -> Admin
    CREATED_AT = db.Column(db.String(50), default=datetime.now().isoformat())
    UPDATED_AT = db.Column(db.String(50), default=datetime.now().isoformat())

    def to_dict(self):
        return {
            "USER_ID": self.USER_ID,
            "USER_NAME": self.USER_NAME,
            "USER_EMAIL": self.USER_EMAIL,
            "USER_PWD": self.USER_PWD,
            "USER_PHONE": self.USER_PHONE,
            "USER_ADDRESS": self.USER_ADDRESS,
            "USER_CITY": self.USER_CITY,
            "USER_STATE": self.USER_STATE,
            "USER_COUNTRY": self.USER_COUNTRY,
            "USER_ZIPCODE": self.USER_ZIPCODE,
            "USER_LAT": self.USER_LAT,
            "USER_LONG": self.USER_LONG,
            "USER_TYPE": self.USER_TYPE,
            "CREATED_AT": self.CREATED_AT,
            "UPDATED_AT": self.UPDATED_AT,
        }

    def __repr__(self):
        return f"<User {self.username}>"
