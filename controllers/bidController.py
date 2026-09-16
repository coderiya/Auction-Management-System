from flask import Blueprint, jsonify, request
from models.user import User
from models.database import db
from models import Bid
import uuid
from datetime import datetime
from sqlalchemy import bindparam, text

bids_bp = Blueprint('bids', __name__)

# create bid item
@bids_bp.route('/',methods=['POST'])
def createBid():
    try:
        data = request.get_json() or {}
        headers = dict(request.headers)
        payload = {
            "bidId":str(uuid.uuid4()),
            "bidName": data['bidName'],
            "bidingStartPrice": data['bidingStartPrice'],
            "biddingOnGoingPrice": 0,
            "bidDesc": data['bidDesc'],
            "bidItemCond":"",
            "bidItemCatName": data['bidItemCatName'],
            "bidItemCatCode": data['bidItemCatName'].upper(),
            "bidStartTime": data["bidStartTime"] if data['bidStartTime'] else datetime.datetime.now(),
            "bidEndTime": data["bidEndTime"] if data['bidEndTime'] else datetime.datetime.now(),
            "numOfBids":0,
            "bidShippingCharges": data["bidShippingCharges"] if data['bidShippingCharges'] else datetime.datetime.now(),
            "imageURL": "",
            "minimumBidAmount": data["minimumBidAmount"],
            "sellerInfo":{
                "sellerName":headers.get('User-Name'),
                "sellerId": headers.get('User-Id'),
                "sellerLocLat": headers.get('LOCLAT'),
                "sellerLocLon": headers.get('LOCLON')
            }
        }
        end = datetime.strptime(payload["bidEndTime"], "%Y-%m-%dT%H:%M:%S")
        start = datetime.strptime(payload["bidStartTime"], "%Y-%m-%dT%H:%M:%S")
        payload['bidTotDurationInSec'] = (
            end - start
        ).total_seconds()

        # validateBidDetails(payload)

        sql = "INSERT INTO bids (BID_ID, BID_NAME, BID_START_PRICE, BID_ONGOING_PRICE, BID_DESC, BID_ITEM_COND, BID_START_TIME, BID_END_TIME, BID_TOTAL_DURATION_IN_SEC, NUM_OF_BIDS,BID_SHIPPING_CHARGES, IMAGE_URL, MINIMUM_BID_AMOUNT,SELLER_NAME, SELLER_ID, SELLER_LOC_LAT, SELLER_LOC_LON, BID_ITEM_CATEGORY_NAME, BID_ITEM_CATEGORY_CODE) VALUES (:bidId, :bidName, :bidingStartPrice, :biddingOnGoingPrice, :bidDesc, :bidItemCond,:bidStartTime, :bidEndTime, :bidTotDurationInSec, :numOfBids,:bidShippingCharges, :imageURL, :minimumBidAmount,:sellerName, :sellerId, :sellerLocLat, :sellerLocLon, :bidItemCatName, :bidItemCatCode)"

        params = {
            "bidId": payload.get("bidId"),
            "bidName": payload.get("bidName"),
            "bidingStartPrice": payload.get("bidingStartPrice"),
            "biddingOnGoingPrice": payload.get("biddingOnGoingPrice"),
            "bidDesc": payload.get("bidDesc"),
            "bidItemCond": payload.get("bidItemCond"),
            "bidStartTime": payload.get("bidStartTime"),
            "bidEndTime": payload.get("bidEndTime"),
            "bidItemCatName": payload.get('bidItemCatName'),
            "bidItemCatCode": payload.get("bidItemCatCode"),
            "bidTotDurationInSec": payload.get("bidTotDurationInSec"),
            "numOfBids": payload.get("numOfBids"),
            "bidShippingCharges": payload.get("bidShippingCharges"),
            "imageURL": payload.get("imageURL"),
            "minimumBidAmount": payload.get("minimumBidAmount"),
            "sellerName": payload.get("sellerInfo", {}).get("sellerName"),
            "sellerId": payload.get("sellerInfo", {}).get("sellerId"),
            "sellerLocLat": payload.get("sellerInfo", {}).get("sellerLocLat"),
            "sellerLocLon": payload.get("sellerInfo", {}).get("sellerLocLon")
        }

        db.session.execute(db.text(sql), params)
        db.session.commit()

        # insert bid status in to bid_status
        bid_status_params = {
            "ID": str(uuid.uuid4()),
            "BID_ID": params['bidId'],
            "STATUS": 'NOT_STARTED',
            "BIDDER_ID": params['sellerId'],
            "BIDDER_NAME": params['sellerName'],
            "CURRENT_BID_AMOUNT": 0
        }
        sql = '''
            INSERT INTO BID_STATUS (ID, BID_ID, STATUS, BIDDER_ID, BIDDER_NAME, CURRENT_BID_AMOUNT) VALUES (:ID, :BID_ID,:STATUS, :BIDDER_ID,:BIDDER_NAME,:CURRENT_BID_AMOUNT)
        '''
        db.session.execute(db.text(sql), bid_status_params)
        db.session.commit()

        return({
            "message": "Bid Created Successfully",
            "data": payload
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# view Bid
@bids_bp.route('/<string:bidId>',methods=['GET'])
def getBid(bidId):
    try:
        if(not bidId):
            return jsonify({
                "message":"Invalid Bid",
                "data":[]
            }),500

        sql = 'SELECT * FROM BIDS WHERE BID_ID = :bidId;'
        params={"bidId": bidId}
        result = db.session.execute(db.text(sql), params)
        db.session.commit()
        bid = result.fetchone()
        if not bid:
            return jsonify({
                "message": "Internal Server Error: No bid found with id {bidId}",
                "data": {}
            }), 500
        else:
            data = dict(bid._mapping)
            return jsonify({
                "message": "Bid fetched successfully",
                "data": data
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Add Bid to Watchlist
@bids_bp.route('/watchlist/add/<string:bidId>',methods=['POST'])
def add_bid_to_watchlist(bidId):
    try:
        if(not bidId):
            return jsonify({
                "message":"Invalid Bid",
                "data":[]
            }),500
        headers = dict(request.headers)
        params = {
            "id": str(uuid.uuid4()),
            "user_id": headers.get('User-Id'),
            "bidId": bidId,
            "isDeleted": "N"
        }
        # check if that bid is already in wishlist
        sql = '''
            SELECT * from USER_WISHLIST WHERE USER_ID = :user_id AND BID_ID = :bid_id and ISDELETED = 'N'
        '''
        res = db.session.execute(db.text(sql), {"user_id":params['user_id'], "bid_id": params['bid_id']})
        doesExists = [dict(row) for row in res.mappings().all()]
        if len(doesExists) > 0:
            return jsonify({
                "message": "Bid already added in wishlist"
            }), 200
        # if bid is not in wishlist, add it
        print(params)
        sql = '''
            INSERT INTO USER_WISHLIST (ID, USER_ID, BID_ID, ISDELETED) VALUES (:id, :user_id, :bidId,:isDeleted)
        '''
        db.session.execute(db.text(sql), params)
        db.session.commit()

        return({
            "message": "Bid added to Wishlist",
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Remove bid from watchlist
@bids_bp.route('/watchlist/remove/<string:bidId>',methods=['POST'])
def remove_bid_from_watchlist(bidId):
    try:
        if(not bidId):
            return jsonify({
                "message":"Invalid Bid",
                "data":[]
            }),500
        params = {
            "bidId": bidId,
            "user_id": request.headers.get('User-Id'),
            "isDeleted":"N"
        }

        sql = '''
            UPDATE USER_WISHLIST
            SET ISDELETED = :isDeleted
            WHERE USER_ID = :user_id AND BID_ID = :bidId
        '''

        db.session.execute(db.text(sql), params)
        db.session.commit()

        return({
            "message": "Bid removed from Wishlist",
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# fetch max quote for a bid
@bids_bp.route('/:bidId', methods=['GET'])
def fetchMaxQuote(bidId):
    try:
        if(not bidId):
            return jsonify({
                "message": "Invalid Bid Details",
                "data":[]
            }), 500
        sql = '''
            SELECT * from BIDDER_HISTORY
            WHERE BID_ID = :bid_id
            ORDER BY BID_AMOUNT DESC
            LIMIT 1
        '''
        result = db.session.execute(db.text(sql),{'bid_id': bidId})
        db.session.commit()
        bidDet = [dict(row) for row in result.mappings().all()]
        return bidDet
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "error": f"Internal Server Error : {str(e)}"
        }), 500

@bids_bp.route('/quote/<string:bidId>', methods=['POST'])
def quote_bid(bidId):
    try:
        if not bidId:
            return jsonify({"message": "Invalid Bid", "data": []}), 500

        data = request.get_json() or {}
        headers = dict(request.headers)

        # Fetch the bid details
        sql = "SELECT * FROM BIDS WHERE BID_ID = :bidId"
        result = db.session.execute(db.text(sql), {"bidId": bidId})
        bid = [dict(row) for row in result.mappings().all()]

        if not bid:
            return jsonify({"message": "Missing bid details", "data": []}), 500

        # Validate min amount using max quote
        maxQuote = fetchMaxQuote(bidId)
        if len(maxQuote) > 0:
            if maxQuote and maxQuote["data"] and maxQuote["data"][0]["BID_AMOUNT"] >= data["bid_amount"]:
                return jsonify({
                    "message": "Quoted amount must be more than current bid",
                }), 400
        # Insert into BIDDER_HISTORY
        params = {
            "ID": str(uuid.uuid4()),
            "bidId": bidId,
            "bid_amount": data["bid_amount"],
            "bidderId": headers.get("User-Id"),
            "current_bid_amount": bid[0]["BID_ONGOING_PRICE"],
        }

        sql = """
            INSERT INTO BIDDER_HISTORY (ID, BID_ID, CURRENT_BID_AMOUNT, BIDDER_ID, BID_AMOUNT)
            VALUES (:ID, :bidId, :current_bid_amount, :bidderId, :bid_amount)
        """
        db.session.execute(db.text(sql), params)
        db.session.commit()

        # Update ongoing bid price
        update_sql = """
            UPDATE BIDS SET BID_ONGOING_PRICE = :bid_amount WHERE BID_ID = :bidId
        """
        db.session.execute(db.text(update_sql), params)
        db.session.commit()

        return jsonify({"message": "Bid Quoted Successfully!", "data": params}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

    
# quote for a bid
@bids_bp.route('/batch/upadteBidStatus',methods=['POST'])
def updateBidStatus():
    try:
        print('---------function call------------')
        # fetch all active bids have end time less that now() and make them completed.
        # for all the bid ids where status is being updated, update final quoted value and the person who purchased that.
        sql = '''
            SELECT b.BID_ID FROM BIDS b INNER JOIN BID_STATUS bs on b.BID_ID = bs.BID_ID
            WHERE b.BID_END_TIME < datetime('now') 
            AND bs.STATUS = 'ON_GOING'
        '''
        # print(sql)
        res = db.session.execute(db.text(sql))
        activeBids = [dict(row) for row in res.mappings().all()]
        # print(activeBids)

        bidIds = [item.get('BID_ID') for item in activeBids if 'BID_ID' in item]
        # print(bidIds)
        if len(bidIds) > 0: 
            in_clause  = "(" + ",".join(f"'{bid}'" for bid in bidIds) + ")"

            # fetch the person who quoted the most and store the purchase details for every bid fetched above
            sql = text('''
                SELECT A.BID_AMOUNT, A.ID, BH.BIDDER_ID, A.BID_ID, BH.BIDDER_NAME
                FROM (
                    SELECT ID, BID_ID, MAX(BID_AMOUNT) AS BID_AMOUNT FROM BIDDER_HISTORY BH
                    WHERE BH.BID_ID IN :in_clause
                    GROUP BY BID_ID 
                ) A INNER JOIN BIDDER_HISTORY BH ON A.ID = BH.ID
            ''').bindparams(bindparam("in_clause", expanding=True))
            res = db.session.execute(sql, {"in_clause":in_clause})
            maxQuoteOfEachBid = [dict(row) for row in res.mappings().all()]
        
            # update bidStatus as completed
            for maxQuote in maxQuoteOfEachBid:
                params = {
                    "status": 'COMPLETED',
                    "purchasedByID": maxQuote['BIDDER_ID'],
                    "finalQuote": maxQuote['BID_AMOUNT'],
                    "purchasedByName": maxQuote['BIDDER_NAME'],
                    "bid_id": maxQuote['BID_ID']
                }
                sql = '''
                    UPDATE BIDS_STATUS
                    SET STATUS = 'COMPLETED', PURCHASED_BY_NAME = :purchasedByName, PURCHASED_BY_ID = :purchasedByID,
                    FINAL_QUOTE = :finalquote
                    where BID_ID = :bid_id
                '''
                res = db.session.execute(db.text(sql), params)
                db.session.commit()
        
        # start not_started bids
        sql = '''
            SELECT b.BID_ID FROM BIDS b INNER JOIN BID_STATUS bs on b.BID_ID = bs.BID_ID
            WHERE b.BID_START_TIME < datetime('now') 
            AND bs.STATUS = 'NOT_STARTED'
        '''
        res = db.session.execute(db.text(sql))
        bids_yet_to_start = [dict(row) for row in res.mappings().all()]
        # print(bids_yet_to_start)

        bidIds = [item.get('BID_ID') for item in bids_yet_to_start if 'BID_ID' in item]
        # print(bidIds)
        if len(bidIds) > 0:
            in_clause  = "(" + ",".join(f"'{bid}'" for bid in bidIds) + ")"

            sql = text('''
                UPDATE BID_STATUS
                SET STATUS = 'ON_GOING'
                WHERE BID_ID IN :in_clause
            ''').bindparams(bindparam("in_clause", expanding=True))
            db.session.execute(sql, {"in_clause": in_clause})
            db.session.commit()

        return jsonify({
            "message": "Batch Executed Successfully",
        }), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "error":f"Internal Server Error: {str(e)}",
        }), 500

def updateFinalQuote(bidIds):
    try:
        for bidId in bidIds:
            # fetch the latest quote
            sql = '''
                SELECT BID_ID, BIDDER_ID, BID_AMOUNT FROM BIDDER_HISTORY WHERE BID_ID = :bidId
            '''
        return True
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error":f"Internal Server Error: {str(e)}",
        }), 500

@bids_bp.route('/temp/add',methods=['GET'])
def updateBids():
    try:
        sql = '''
            SELECT b.BID_ID FROM BIDS b LEFT JOIN BID_STATUS bs ON bs.BID_ID = b.BID_ID
            WHERE bs.BID_ID IS NULL
        '''
        res = db.session.execute(db.text(sql))
        bidIds = [dict(row) for row in res.mappings().all()]
        for id in bidIds:
            bid_status_params = {
                "ID": str(uuid.uuid4()),
                "BID_ID": id['BID_ID'],
                "STATUS": 'NOT_STARTED',
                "BIDDER_ID": '1995a249-ab26-4e22-b834-cf20617dfe92',
                "BIDDER_NAME": 'magi',
                "CURRENT_BID_AMOUNT": 0
            }
            sql = '''
                INSERT INTO BID_STATUS (ID, BID_ID, STATUS, BIDDER_ID, BIDDER_NAME, CURRENT_BID_AMOUNT) VALUES (:ID, :BID_ID,:STATUS, :BIDDER_ID,:BIDDER_NAME,:CURRENT_BID_AMOUNT)
            '''
            db.session.execute(db.text(sql), bid_status_params)
            db.session.commit()
        return jsonify({
            "message": "Success"
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Error occured",
        }), 500