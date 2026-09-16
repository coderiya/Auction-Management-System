from .database import db


class BidderHistory(db.Model):
    __tablename__ = "BIDDER_HISTORY"

    ID = db.Column(db.String(64), primary_key=True)
    BID_ID = db.Column(db.String(64), nullable=False)
    STATUS = db.Column(db.String(64))  # ON_GOING or COMPLETED - MOSTLY THIS WONT BE REQUIRED AS WE ARE STORING BID STATUS IN BID MAIN TABLE - CHECK ONCE BEFORE REMOVING
    CURRENT_BID_AMOUNT = db.Column(db.Float)  # current on going bid amount
    BIDDER_ID = db.Column(db.String(64))  # user id of the bidder
    BIDDER_NAME = db.Column(db.String(64)) # user-name of the bidder
    BID_AMOUNT = db.Column(db.Float)  # how much amount did the bidder bid
    CREATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))
    UPDATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))

    def to_dict(self):
        """Serialize model object to dictionary (for JSON responses)"""
        return {
            "ID": self.ID,
            "BID_ID": self.BID_ID,
            "STATUS": self.STATUS,
            "CURRENT_BID_AMOUNT": self.CURRENT_BID_AMOUNT,
            "BIDDER_ID": self.BIDDER_ID,
            "BIDDER_NAME": self.BIDDER_NAME,
            "BID_AMOUNT": self.BID_AMOUNT,
            "CREATED_AT": self.CREATED_AT,
            "UPDATED_AT": self.UPDATED_AT,
        }
