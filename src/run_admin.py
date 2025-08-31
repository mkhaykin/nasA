from admin_app import create_app

app = create_app()


def run_admin() -> None:
    app.run(host="0.0.0.0", port=8081, debug=False)  # noqa: S104


if __name__ == "__main__":
    run_admin()
