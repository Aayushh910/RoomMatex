from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# ---------- SIGNUP ----------
@auth_bp.route("/api/signup", methods=["POST"])
def signup():
    data = request.json

    if not all(k in data for k in ("full_name", "email", "password", "role")):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role=data["role"],
        phone=data.get("phone"),
        city=data.get("city")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ---------- LOGIN ----------
@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get("email"), is_blocked=False).first()

    if not user or not check_password_hash(user.password_hash, data.get("password")):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.full_name,
            "role": user.role
        }
    }), 200
