from user_app import create_app

app = create_app()


def run_user() -> None:
    app.run(host="0.0.0.0", port=8080, debug=False)  # noqa: S104


if __name__ == "__main__":
    run_user()
