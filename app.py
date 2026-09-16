from flask import Flask, render_template, request, jsonify
from models import init_db, db
from controllers import user_bp, listing_bp, bids_bp
import os
from flask_cors import CORS
import threading
import webbrowser
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import atexit

app = Flask(__name__)
CORS(app)

from dotenv import load_dotenv
load_dotenv()

# app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# SQLite database configuration
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.sqlite3")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
init_db(app)

def call_api():
    print("Calling API...")
    try:
        response = requests.post("http://127.0.0.1:8080/bids/batch/upadteBidStatus")
        print("Status:", response.status_code)
    except Exception as e:
        print("Error:", e)

scheduler = BackgroundScheduler()
scheduler.add_job(func=call_api, trigger="interval", minutes=30)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))

# Create database file and tables if they don’t exist
with app.app_context():
    if not os.path.exists(DB_PATH):
        print("Database not found — creating new db.sqlite3...")
        db.create_all()
        print("Database and tables created successfully.")
    else:
        print("Database already exists — skipping creation. Path: ",app.config['SQLALCHEMY_DATABASE_URI'])
        print("Available tables: ",[t.name for t in db.metadata.sorted_tables])

# Register Blueprints for controllers
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(listing_bp, url_prefix='/api/list')
app.register_blueprint(bids_bp, url_prefix='/bids')

# UI screens rendering
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/createBid')
def createBid():
    return render_template('create_bid.html')

@app.route('/viewRecentBids')
def recentBids():
    return render_template('Recent_bids.html')

@app.route('/viewRecentQuotes')
def quotedBids():
    return render_template('quoted_bids.html')

@app.route('/bid/<bid_id>')
def bid_page(bid_id):
    return render_template("bid.html", bidId=bid_id)

@app.route('/wishlist')
def viewWishList():
    return render_template('user_wishlist.html')

@app.route('/resetPassowrd')
def resetPassword():
    return render_template('reset_password.html')

@app.route('/profile')
def fetchUserProfile():
    return render_template('profile.html')

def open_browser():
    """Open the default browser automatically."""
    webbrowser.open_new("http://127.0.0.1:8080/")

if __name__ == '__main__':
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 8080))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    threading.Timer(1, open_browser).start()
    # app.run(debug=True,use_reloader=False)
    app.run(host=host, port=port, debug=debug, use_reloader = True)
