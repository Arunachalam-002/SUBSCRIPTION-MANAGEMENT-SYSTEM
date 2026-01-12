from flask import Blueprint, render_template, request, redirect, session
from models.user_model import create_user, find_user_by_email, verify_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = find_user_by_email(email)
        if user and verify_password(user["password"], password):
            session["user_email"] = email
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin/dashboard")
            else:
                return redirect("/client/dashboard")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        create_user(
            request.form["name"],
            request.form["email"],
            request.form["password"]
        )
        return redirect("/")
    return render_template("register.html")
