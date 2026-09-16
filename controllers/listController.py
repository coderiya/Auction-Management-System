from flask import Blueprint, jsonify, request
from models.user import User
from models.database import db
from models import Bid

listing_bp = Blueprint('listing', __name__)

# Fetch statistics of total num of active Bids, purchase History and total number of bids in progress
@listing_bp.route('/stats',methods=['GET'])
def getStats():
    try:
        headers = dict(request.headers)
        sql = '''
            SELECT
                SUM(CASE 
                    WHEN b.STATUS = 'ON_GOING' AND b.BID_ID IS NOT NULL THEN 1
                    ELSE 0
                END) AS activeBids,
                SUM(CASE 
                    WHEN b.STATUS = 'ON_GOING' AND w.BID_ID IS NOT NULL AND w.USER_ID = :user_id THEN 1
                    ELSE 0
                END) AS watchlist,
                SUM(CASE WHEN b.STATUS = 'COMPLETED' THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN b.STATUS = 'NOT_STARTED' THEN 1 ELSE 0 END) AS not_started
            FROM BID_STATUS b
            LEFT JOIN user_wishlist w ON b.BID_ID = w.BID_ID;
        '''
        # add purchase history logic
        result = db.session.execute(db.text(sql), {"user_id": headers.get("USER_ID")})
        db.session.commit()
        stats = [dict(row) for row in result.mappings().all()]
        return jsonify({"message": "Fetched Successfully", "data": stats, "status": 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500 

# Fetch the list of categories and total bids
@listing_bp.route('/categories',methods=["GET"])
def getCategories():
    try:
        sql = """
            SELECT COUNT(BID_ITEM_CATEGORY_CODE) AS ITEM_COUNT, BID_ITEM_CATEGORY_CODE AS LABEL_CODE, BID_ITEM_CATEGORY_NAME AS LABEL_NAME
            FROM BIDS 
            WHERE BID_ITEM_CATEGORY_CODE IS NOT NULL
            GROUP BY BID_ITEM_CATEGORY_CODE, BID_ITEM_CATEGORY_NAME;
        """
        result = db.session.execute(db.text(sql))
        data = [dict(row) for row in result.mappings().all()]
        return jsonify({
            "message": "Fetched Successfully",
            "count": len(data),
            "data": data
        }),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Fetch the list of categories
@listing_bp.route('/listings',methods=['POST'])
def getList():
    try:
        print('------start-------')
        payload = request.get_json(force=True) or {}

        sql =  "SELECT * FROM BIDS"
        sql = addListingParameters(sql, payload)
        print(sql)
        result = db.session.execute(db.text(sql))
        data = [dict(row) for row in result.mappings().all()]

        sql = "SELECT COUNT(*) AS total_count FROM BIDS"
        sql = addListingParameters(sql, payload)
        res = db.session.execute(db.text(sql))
        tot = [dict(row) for row in res.mappings().all()]

        return jsonify({
            "message":"Bids fetched Successfully",
            "result":{
                "data": data,
                "total": tot[0]['total_count']
            }
        }),200
       
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    
# fetch wishlist
@listing_bp.route('/wishlist/',methods=['POST'])
def fetch_wishlist():
    try:
        payload = request.get_json() or {}
        headers = dict(request.headers)
        user_id = headers.get('User-Id')
        if user_id is None:
            return jsonify({
                "message":"Missing User Details",
                "data":[]
            }), 500
        sql = "SELECT UW.USER_ID, UW.BID_ID, BS.STATUS, B.BID_NAME, B.BID_START_PRICE, B.BID_START_TIME, B.BID_END_TIME,B.NUM_OF_BIDS,B.MINIMUM_BID_AMOUNT,BS.CURRENT_BID_AMOUNT,B.BID_ONGOING_PRICE, B.BID_DESC, B.BID_ITEM_COND, B.BID_ITEM_CATEGORY_NAME, B.BID_ITEM_CATEGORY_CODE, B.SELLER_ID, B.SELLER_NAME FROM USER_WISHLIST UW INNER JOIN BIDS B ON UW.BID_ID = B.BID_ID INNER JOIN BID_STATUS BS ON B.BID_ID = BS.BID_ID"
        payload['search']['UW.USER_ID'] = user_id
        payload['search']['UW.ISDELETED'] = 'N'
        payload['user_id'] = user_id
        sql = addListingParameters(sql, payload)
        result = db.session.execute(db.text(sql))
        data = [dict(row) for row in result.mappings().all()]

        return jsonify({
            "message": f"Wishlist fetched successfully for user",
            "status": 200,
            "result": {
                "total": len(data),
                "data": data
            }
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Error fetching wishlist",
            "error": str(e),
            "status": 500
        }), 500 

# Fetch list of Created Bids
@listing_bp.route('/list',methods=['POST'])
def get_bids_history():
    try:
        payload = request.get_json() or {}
        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        user = User.query.filter_by(USER_ID=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        sql = '''
            SELECT * FROM BIDS b inner join BIDS_STATUS bs on b.BID_ID = bs.BID_ID
            WHERE SELLER_ID = :user_id
        '''
        sql = addListingParameters(sql, payload)
        
        result = db.session.execute(db.text(sql), {user_id:user_id})
        db.session.commit()
        data = [dict(row) for row in result.mappings().all()]
        #Dummy bids history data for now
        bids_history = [
            {
                "bid_id": 201,
                "bid_name": "iPhone 14 Pro",
                "category": "Electronics",
                "start_price": 800.00,
                "current_price": 950.00,
                "status": "active",
                "bid_start_time": "2025-10-20T10:00:00Z",
                "bid_end_time": "2025-10-29T20:00:00Z",
                "num_of_bids": 14
            },
            {
                "bid_id": 202,
                "bid_name": "Smartwatch Garmin 965",
                "category": "Wearables",
                "start_price": 250.00,
                "current_price": 340.00,
                "status": "closed",
                "bid_start_time": "2025-09-10T10:00:00Z",
                "bid_end_time": "2025-09-17T20:00:00Z",
                "num_of_bids": 9
            }
        ]

        return jsonify({
            "message": f"Bids created by user {user_id} fetched successfully",
            "status": 200,
            "data": bids_history
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Error fetching bids history",
            "error": str(e),
            "status": 500
        }), 500

# Fetch all the quotes for a bid
@listing_bp.route('/quotes',methods=['POST'])
def get_all_quotes():
    try:
        payload = request.get_json() or {}
        bid_id = payload.get("bid_id")
        headers = dict(request.headers)
        if not bid_id:
            return jsonify({"error": "bid_id is required"}), 400
        
        params = {
            "userid": headers.get('User-Id'),
            "bid_id": payload['bid_id']
        }
        sql = '''
            SELECT * from BID_QUOTES where bid_id = :bid_id and user_id=:user_id
            sort by CREATED_AT desc
        '''
        result = db.session.execute(db.text(sql), params)
        db.session.commit()
        quotes_data = [dict(row) for row in result.mappings().all()]
        #Dummy quotes data for now
        quotes_data = [
            {
                "quote_id": 1,
                "bid_id": bid_id,
                "user_id": "user_123",
                "quote_amount": 1200.00,
                "quote_time": "2025-10-26T14:30:00Z"
            },
            {
                "quote_id": 2,
                "bid_id": bid_id,
                "user_id": "user_456",
                "quote_amount": 1250.00,
                "quote_time": "2025-10-26T15:00:00Z"
            }
        ]

        return jsonify({
            "message": f"Quotes fetched successfully for bid {bid_id}",
            "status": 200,
            "data": quotes_data
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Error fetching quotes",
            "error": str(e),
            "status": 500
        }), 500
 
# Fetch all the quotes for a bid
@listing_bp.route('/user/quotes',methods=['POST'])
def get_all_quotes_by_user():
    try:
        payload = request.get_json() or {}
        headers = dict(request.headers)
        params = {
            "user_id": headers.get("User-Id"),
        }
        sql = '''
            SELECT BH.BID_AMOUNT, BH.BIDDER_NAME, B.BID_DESC, B.BID_NAME, B.SELLER_NAME, B.BID_ITEM_CATEGORY_NAME, 
            B.BID_ONGOING_PRICE, B.BID_START_PRICE, B.BID_ITEM_CATEGORY_NAME, B.BID_START_TIME, B.BID_END_TIME, B.NUM_OF_BIDS,
            BS.STATUS, BS.CURRENT_BID_AMOUNT
            from BIDDER_HISTORY BH INNER JOIN BIDS B ON BH.BID_ID = B.BID_ID
            INNER JOIN BID_STATUS BS ON BS.BID_ID = B.BID_ID
        '''
        payload['filter']['BH.BIDDER_ID'] = params['user_id']
        sql = addListingParameters(sql, payload)
        result = db.session.execute(db.text(sql), params)
        db.session.commit()
        quotes_data = [dict(row) for row in result.mappings().all()]

        sql = '''
            SELECT COUNT(*) as totalQuotes
            from BIDDER_HISTORY BH INNER JOIN BIDS B ON BH.BID_ID = B.BID_ID
            INNER JOIN BID_STATUS BS ON BS.BID_ID = B.BID_ID
        '''
        sql = addListingParameters(sql, params, 'Y')
        result = db.session.execute(db.text(sql), params)
        db.session.commit()
        totalQuotes = [dict(row) for row in result.mappings().all()]

        return jsonify({
            "message": f"Quotes fetched successfully",
            "status": 200,
            "result":{
                "data": quotes_data,
                "total": totalQuotes[0]['totalQuotes']
            }
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Error fetching quotes",
            "error": str(e),
            "status": 500
        }), 500


def addListingParameters(sql, params, forCnt = 'N'):
    try:
        search_clauses = []
        # search
        if params.get('serach'):
            search_value = params.get('search')
            search_clauses.append(f"(BID_NAME LIKE %{search_value}% OR BID_DESC LIKE %{search_value})")
        # filter
        if params.get('filter'):
            for key, value in params['filter'].items():
                # search_clauses.append(f"{key} LIKE '%{value}%'")
                search_clauses.append(f"{key} = '{value}'")

        if len(search_clauses) > 0:
            sql += " WHERE " + " AND ".join(search_clauses)

        if forCnt == 'Y':
            return sql
        # sorting
        if params.get('sort'):
            orderbyQuery = ' ORDER BY '
            for obj in params['sort']:
                orderbyQuery += obj['key']
                orderbyQuery += ' DESC, ' if obj['value'] == -1 else ' ASC, '
            orderbyQuery = orderbyQuery.rstrip(', ')
            sql += orderbyQuery
        # pagination
        if params.get('limit') is not None:
            sql += f' limit {params['limit']}'
        if params.get('skip') is not None:
            sql += f' offset {params['skip']}'
        sql += ';'
        return sql
    except Exception as e:
        raise ValueError(f"Error building SQL: {str(e)}")