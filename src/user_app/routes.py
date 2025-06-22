import os
from typing import Union

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug import Response

from shared.tickets import reserve_ticket, use_ticket, validate_ticket
from user_app.forms import TicketForm, UploadForm

bp = Blueprint("user", __name__)


@bp.before_app_request
def make_session_permanent() -> None:
    session.permanent = True


@bp.route("/", methods=["GET", "POST"])
def index() -> Union[Response, str]:
    form = TicketForm()
    if request.method == "POST":
        ticket_value = form.ticket.data
        ticket = validate_ticket(ticket_value)
        if ticket:
            reserved_ticket = reserve_ticket(ticket.ticket_id)
            if reserved_ticket:
                session["ticket_id"] = ticket.ticket_id
                return redirect(url_for("user.upload"))
            else:
                flash("Ticket already in use")
        else:
            flash("Invalid or used ticket")
    return render_template("index.html", form=form)


@bp.route("/upload", methods=["GET", "POST"])
def upload() -> Union[Response, str]:
    # TODO правильнее таскать не ticket_id, а непосредственно хэш. Так безопаснее.
    if "ticket_id" not in session:
        return redirect(url_for("user.index"))

    form = UploadForm()
    if request.method == "POST":
        f = request.files["file"]
        if f and f.filename:
            filename = f.filename
            path = os.path.join(current_app.config["SHARED_FOLDER"], filename)
            f.save(path)
            use_ticket(session.pop("ticket_id"))

            return render_template("upload_complete.html")
    return render_template("upload.html", form=form)
