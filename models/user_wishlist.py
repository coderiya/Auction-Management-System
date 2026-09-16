from .database import db


class UserWishlist(db.Model):
    __tablename__ = "USER_WISHLIST"

    ID = db.Column(db.String(64), primary_key=True)
    USER_ID = db.Column(db.String(64), nullable= False)
    BID_ID = db.Column(db.String(64), nullable=False)
    ISDELETED = db.Column(db.String(64), server_default=db.text('N'))  # Y(in wishlist) or N (removed from wishlist)
    CREATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))
    UPDATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))

    def to_dict(self):
        """Serialize model object to dictionary (for JSON responses)"""
        return {
            "ID": self.ID,
            "BID_ID": self.BID_ID,
            "USER_ID": self.USER_ID,
            "ISDELETED": self.ISDELETED,
            "CREATED_AT": self.CREATED_AT,
            "UPDATED_AT": self.UPDATED_AT,
        }
