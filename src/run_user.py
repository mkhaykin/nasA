from user_app import create_app

app = create_app()


def run_user() -> None:
    app.run(host="127.0.0.1", port=46032, debug=True)


if __name__ == "__main__":
    run_user()
