from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from .auth_service import AuthService, InvalidCredentialsError, UserAlreadyExistsError
from .repository import SqliteUserRepository
from .validation import ValidationError

auth_bp = Blueprint("auth", __name__)


def get_auth_service():
    return AuthService(SqliteUserRepository(current_app.config["DATABASE"]))


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.register"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            get_auth_service().register(
                request.form["email"], request.form["password"],
                request.form["name"], request.form.get("phone"),
            )
        except ValidationError as e:
            flash(str(e), "error")
        except UserAlreadyExistsError:
            flash("User already exists", "error")
        else:
            flash("Реєстрація успішна")
            return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            get_auth_service().login(request.form["email"], request.form["password"])
        except ValidationError as e:
            flash(str(e), "error")
        except InvalidCredentialsError:
            flash("Invalid credentials", "error")
        else:
            flash("Вхід виконано")
            return redirect(url_for("auth.login"))
    return render_template("login.html")
