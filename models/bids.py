from .database import db


class Bid(db.Model):
    __tablename__ = "BIDS"

    BID_ID = db.Column(db.String(64), primary_key=True)  # Unique ID for the bid
    BID_NAME = db.Column(db.String(255), nullable=False)  # Bid title
    BID_START_PRICE = db.Column(db.Float, nullable=False)  # Starting price
    BID_ONGOING_PRICE = db.Column(db.Float)  # Ongoing/current bid
    BID_DESC = db.Column(db.Text)  # Description of the item
    BID_ITEM_COND = db.Column(db.String(50))  # Item condition (New/Used/etc.)
    BID_ITEM_CATEGORY_NAME = db.Column(db.String(100)) # category name of the bid item
    BID_ITEM_CATEGORY_CODE = db.Column(db.String(100)) # category code of the bid item
    BID_START_TIME = db.Column(db.String(50), nullable=False)  # Start time (ISO string)
    BID_END_TIME = db.Column(db.String(50), nullable=False)  # End time (ISO string)
    BID_TOTAL_DURATION_IN_SEC = db.Column(db.Integer)  # Duration in seconds
    NUM_OF_BIDS = db.Column(db.Integer, default=0)  # Number of bids placed
    BID_SHIPPING_CHARGES = db.Column(db.Float, default=0.0)  # Shipping charges
    IMAGE_URL = db.Column(db.Text)  # Image URL
    MINIMUM_BID_AMOUNT = db.Column(db.Float)  # Minimum next bid increment
    SELLER_NAME = db.Column(db.String(100))  # Seller's name
    SELLER_ID = db.Column(db.String(100))  # Seller's unique ID
    SELLER_LOC_LAT = db.Column(db.Float)  # Seller's latitude
    SELLER_LOC_LON = db.Column(db.Float)  # Seller's longitude
    CREATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))
    UPDATED_AT = db.Column(db.String(50), server_default=db.text("datetime('now')"))

    def to_dict(self):
        """Serialize model object to dictionary (for JSON responses)"""
        return {
            "BID_ID": self.BID_ID,
            "BID_NAME": self.BID_NAME,
            "BID_START_PRICE": self.BID_START_PRICE,
            "BID_ONGOING_PRICE": self.BID_ONGOING_PRICE,
            "BID_DESC": self.BID_DESC,
            "BID_ITEM_COND": self.BID_ITEM_COND,
            "BID_ITEM_CATEGORY_NAME": self.BID_ITEM_CATEGORY_NAME,
            "BID_ITEM_CATEGORY_CODE": self.BID_ITEM_CATEGORY_CODE,
            "BID_START_TIME": self.BID_START_TIME,
            "BID_END_TIME": self.BID_END_TIME,
            "BID_TOTAL_DURATION_IN_SEC": self.BID_TOTAL_DURATION_IN_SEC,
            "NUM_OF_BIDS": self.NUM_OF_BIDS,
            "BID_SHIPPING_CHARGES": self.BID_SHIPPING_CHARGES,
            "IMAGE_URL": self.IMAGE_URL,
            "MINIMUM_BID_AMOUNT": self.MINIMUM_BID_AMOUNT,
            "SELLER_NAME": self.SELLER_NAME,
            "SELLER_ID": self.SELLER_ID,
            "SELLER_LOC_LAT": self.SELLER_LOC_LAT,
            "SELLER_LOC_LON": self.SELLER_LOC_LON,
            "CREATED_AT": self.CREATED_AT,
            "UPDATED_AT": self.UPDATED_AT,
        }
