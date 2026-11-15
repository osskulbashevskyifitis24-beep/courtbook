from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from .auth_service import login_user, register_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.register"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        result = register_user(
            request.form["email"], request.form["password"],
            request.form["name"], request.form.get("phone"),
            current_app.config["DATABASE"],
        )
        if result["ok"]:
            flash("Реєстрація успішна")
            return redirect(url_for("auth.login"))
        flash(result["error"], "error")
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = login_user(
            request.form["email"], request.form["password"],
            current_app.config["DATABASE"],
        )
        if result["ok"]:
            flash("Вхід виконано")
            return redirect(url_for("auth.login"))
        flash(result["error"], "error")
    return render_template("login.html")
