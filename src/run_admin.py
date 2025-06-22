from admin_app import create_app

app = create_app()


def run_admin() -> None:
    app.run(host="127.0.0.1", port=3000, debug=True)


if __name__ == "__main__":
    run_admin()
