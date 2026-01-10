from flask import Flask
from flask_cors import CORS
from extensions import db
from routes.auth_routes import auth_bp
from models.user import User

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
CORS(app)

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"status": "RoomMateX backend running"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
