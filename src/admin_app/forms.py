from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange


class SetupForm(FlaskForm):
    password = PasswordField(
        "Пароль администратора",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=50,
                message="Пароль должен быть не менее 8 символов и не более 50",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Подтверждение пароля",
        validators=[
            DataRequired(),
            EqualTo("password", message="Пароли должны совпадать"),
        ],
    )


class LoginForm(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class GenerateForm(FlaskForm):
    number = IntegerField(
        label="Count",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=99, message="от 1 до 99"),
        ],
        default=10,
    )
