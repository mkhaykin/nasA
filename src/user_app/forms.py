from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (
    FileField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length


class TicketForm(FlaskForm):
    ticket = StringField(
        "Ticket",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=50,
                message="Тикет должен быть не менее 3 символов и не более 50",
            ),
        ],
    )


class UploadForm(FlaskForm):
    file = FileField(
        "Выберите файл",
        validators=[
            FileRequired(message="Файл не выбран"),
            FileAllowed(
                ["jpg", "png", "pdf", "docx", "xlsx", "*"],
                message="Разрешены только jpg, png, pdf, docx, xlsx",
            ),
        ],
    )
    submit = SubmitField("Загрузить")
