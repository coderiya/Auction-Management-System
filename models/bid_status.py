from .database import db


class BidStatus(db.Model):
    __tablename__ = "BID_STATUS"

    ID = db.Column(db.String(64), primary_key=True)
    BID_ID = db.Column(db.String(64), nullable=False)
    STATUS = db.Column(db.String(64))  # ON_GOING or COMPLETED or NOT_STARTED
    BIDDER_ID = db.Column(db.String(64))  # seller id
    BIDDER_NAME = db.Column(db.String(64))  # seller name
    CURRENT_BID_AMOUNT = db.Column(db.Float)
    PURCHASED_BY_NAME = db.Column(db.String(64))
    PURCHASED_BY_ID = db.Column(db.String(64))
    FINAL_QUOTE = db.Column(db.Float)
    CREATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))
    UPDATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))

    def to_dict(self):
        """Serialize model object to dictionary (for JSON responses)"""
        return {
            "ID": self.ID,
            "BID_ID": self.BID_ID,
            "STATUS": self.STATUS,
            "BIDDER_ID": self.BIDDER_ID,
            "BIDDER_NAME": self.BIDDER_NAME,
            "CURRENT_BID_AMOUNT": self.CURRENT_BID_AMOUNT,
            "PURCHASED_BY_NAME": self.PURCHASED_BY_NAME,
            "PURCHASED_BY_ID": self.PURCHASED_BY_ID,
            "FINAL_QUOTE": self.FINAL_QUOTE,
            "CREATED_AT": self.CREATED_AT,
            "UPDATED_AT": self.UPDATED_AT,
        }
