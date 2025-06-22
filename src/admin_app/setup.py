from typing import Union

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from werkzeug import Response

from admin_app import is_system_configured  # , db
from admin_app.forms import SetupForm
from shared.service import add_admin

setup_bp = Blueprint("setup", __name__)


@setup_bp.route("/setup", methods=["GET", "POST"])
def setup() -> Union[Response, str]:
    if is_system_configured():
        return redirect(url_for("admin.dashboard"))

    form: SetupForm = SetupForm()
    if form.validate_on_submit():
        # Создаём администратора
        add_admin(
            user_name="admin",
            password=form.password.data,
        )

        flash("Настройка завершена!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("setup.html", form=form)
