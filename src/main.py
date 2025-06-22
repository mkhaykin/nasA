import threading

from admin_app import create_app as create_app_admin
from user_app import create_app as create_app_user

if __name__ == "__main__":
    app_admin = create_app_admin()
    app_user = create_app_user()

    threading.Thread(
        target=app_user.run,
        kwargs={"host": "127.0.0.1", "port": 46032},
    ).start()

    threading.Thread(
        target=app_admin.run,
        kwargs={"host": "127.0.0.1", "port": 3000},
    ).start()
