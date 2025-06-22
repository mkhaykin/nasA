from typing import Union

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug import Response

from admin_app.forms import GenerateForm, LoginForm
from shared.service import get_user_by_name
from shared.tickets import generate_tickets, get_tickets

bp = Blueprint("admin", __name__, template_folder="templates")


@bp.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    """login page"""
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_name(request.form.get("user_name", ""))

        if user and user.check_password(password=form.password.data):
            login_user(user, force=True)
            flash("You have been logged in!", "success")
            return redirect(request.args.get("next") or url_for("admin.dashboard"))
        else:
            flash(
                "Login Unsuccessful. Please check username and password",
                "danger",
            )

    return render_template("login.html", title="Login", form=form)


@login_required
@bp.route("/logout")
def logout() -> Union[Response, str]:
    logout_user()
    return redirect(url_for("admin.login"))


@login_required
@bp.route("/")
def dashboard() -> Union[Response, str]:
    return render_template("index.html", tickets=get_tickets())


@login_required
@bp.route("/generate", methods=["GET", "POST"])
def generate() -> Union[Response, str]:

    form: GenerateForm = GenerateForm()
    if request.method == "POST":
        count = int(form.number.data)
        tickets = generate_tickets(count)

        if tickets:
            return render_template("generated.html", tickets=tickets)

        flash("Ошибка при генерации тикетов")
        return redirect(url_for("admin.dashboard"))
    return render_template("generate.html", form=form)
