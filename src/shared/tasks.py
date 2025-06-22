from apscheduler.schedulers.background import BackgroundScheduler

from shared.tickets import release_expired


def init_scheduler() -> None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=release_expired,
        trigger="interval",
        minutes=5,
        id="release_reservations",
    )
    scheduler.start()
