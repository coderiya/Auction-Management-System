from flask import Flask, Blueprint, request, jsonify
from models.user import User
from models.database import db
from models import Bid
import uuid

user_bp = Blueprint("user", __name__)


# login
@user_bp.route("/login", methods=["POST"])
def user_login():
    try:
        data = request.get_json() or {}

        userName = data.get("username")
        userPwd = data.get("password")

        if not userName or not userPwd:
            return jsonify({"error": "Missing username or password", "data": {}}), 500

        sql = "SELECT * FROM USERS WHERE USER_NAME = :userName AND USER_PWD = :userPwd"
        params = {"userName": userName, "userPwd": userPwd}

        result = db.session.execute(db.text(sql), params)
        user = result.fetchone()

        if user:
            user_data = dict(user._mapping)
            user_data.pop("USER_PWD", None)
            return jsonify({"message": "Login Successful", "data": user_data}), 200
        else:
            return jsonify({
                "message": "User not found or incorrect credentials", 
                "error": "User not found or incorrect credentials", 
                "data": {}
            }),404

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# add Users
@user_bp.route("/add", methods=["POST"])
def add_user():
    try:
        print('----------------start of add-------------')
        print(request)
        data = request.get_json(force=True) or {}
        print('datadatadata: ',data)
        if not data:
            return jsonify({"error": "No JSON received"}), 400
        payload = {
            "userId": str(uuid.uuid4()),
            "userName": data["userName"],
            "userEmail": data["userEmail"],
            "userPhone": data["userPhone"],
            "userAddress": data.get("userAddress",""),
            "userCity": data.get("userCity",""),
            "userState": data.get("userState",""),
            "userCountry": data.get("userCountry",""),
            "userZipcode": data.get("userZipcode",""),
            "userLat": data.get("userLat",""),
            "userLong": data.get("userLong",""),
            "userType": data.get("userType",""),
            "userPassword": data['userPassword']
        }

        sql = "INSERT INTO USERS (USER_ID,USER_NAME,USER_EMAIL,USER_PHONE,USER_ADDRESS,USER_CITY,USER_STATE,USER_COUNTRY,USER_ZIPCODE,USER_LAT,USER_LONG,USER_TYPE, USER_PWD) VALUES (:userId, :userName, :userEmail, :userPhone, :userAddress, :userCity, :userState, :userCountry, :userZipcode, :userLat, :userLong, :userType, :userPassword)"

        params = {
            "userId": payload.get("userId"),
            "userName": payload.get("userName"),
            "userEmail": payload.get("userEmail"),
            "userPhone": payload.get("userPhone"),
            "userAddress": payload.get("userAddress"),
            "userCity": payload.get("userCity"),
            "userState": payload.get("userState"),
            "userCountry": payload.get("userCountry"),
            "userZipcode": payload.get("userZipcode"),
            "userLat": payload.get("userLat"),
            "userLong": payload.get("userLong"),
            "userType": payload.get("userType"),
            "userPassword": payload.get("userPassword")
        }

        db.session.execute(db.text(sql), params)
        db.session.commit()

        print('---------end of add------')
        return jsonify({"message": "User Created Successfully", "data": "payload"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# update user's Profile
@user_bp.route("/update", methods=["PUT"])
def edit_user():
    try:
        data = request.get_json() or {}

        payload = {
            "userId": data["userId"],
            "userName": data["userName"],
            "userEmail": data["userEmail"],
            "userPhone": data["userPhone"],
            "userAddress": data["userAddress"],
            "userCity": data["userCity"],
            "userState": data["userState"],
            "userCountry": data["userCountry"],
            "userZipcode": data["userZipcode"],
            "userLat": data["userLat"],
            "userLong": data["userLong"],
            "userType": data["userType"],
        }

        sql = "UPDATE USERS SET USER_PHONE= :userPhone, USER_ADDRESS= :userAddress, USER_CITY= :userCity, USER_STATE= :userState, USER_COUNTRY= :userCountry, USER_ZIPCODE= :userZipcode, USER_LAT= :userLat, USER_LONG= :userLong WHERE USER_ID= :userId"

        db.session.execute(db.text(sql), payload)
        db.session.commit()

        return jsonify({"message": "User Created Successfully", "data": payload}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# disable/delete user profile
@user_bp.route("/disable", methods=["PUT"])
def delete_user():
    try:
        data = request.get_json() or {}
        sql = '''
            update USERS
            set isDeleted = 'Y'
            where USER_ID = :user_id or USER_NAME = :user_name
        '''
        params = {
            "user_id": data['user_id'],
            "user_name": data['user_name']
        }
        db.session.execute(db.text(sql), params)
        db.session.commit()
        return jsonify({"message": "", "data": ""}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# view user using user_name
@user_bp.route("/name/<string:user_name>", methods=["GET"])
def get_user_by_name(user_name):
    try:
        sql = "SELECT USER_ID, USER_NAME FROM USERS WHERE USER_NAME = :user_name;"
        params = {"user_name": user_name}
        print('db.text(sql): ', db.text(sql))
        result = db.session.execute(db.text(sql), params)
        print("result: ", result)
        db.session.commit()
        user = result.fetchone()
        if not user:
            return (jsonify({
                "message": "Internal Server Error: No user found",
                "data": {},}
                ),500)
        else:
            data = dict(user._mapping)
            return jsonify({"message": "User fetched successfully", "data": data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# view user using user_id
@user_bp.route("/<string:userId>", methods=["GET"])
def get_user(userId):
    try:
        sql = "SELECT * FROM USERS WHERE USER_ID = :userId;"
        params = {"userId": userId}
        result = db.session.execute(db.text(sql), params)
        db.session.commit()
        user = result.fetchone()
        if not user:
            return (jsonify({
                "message": "Internal Server Error: No user found",
                "data": {},}
                ),500)
        else:
            data = dict(user._mapping)
            return jsonify({"message": "User fetched successfully", "data": data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# logout user
@user_bp.route("/logout", methods=["POST"])
def user_logout():
    return True


# reset-password
@user_bp.route("/resetPassword", methods=["POST"])
def reset_password():
    try:
        data = request.get_json() or {}

        payload = {
            "userName": data["username"],
            "userPwd": data["password"],
        }

        sql = "UPDATE users SET USER_PWD = :userPwd WHERE USER_NAME = :userName;"

        db.session.execute(db.text(sql), payload)
        db.session.commit()

        return jsonify({"message": "Password Updated", "data": {}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500
