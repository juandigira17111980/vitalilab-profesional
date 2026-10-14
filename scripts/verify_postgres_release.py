"""Exercise additive entities only in the disposable CI database."""

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.extensions import db
from app.models import DailyCheckIn, Habit, User, UserGoal, UserProfile
from app.services.clock import local_day
from app.services.wellness import save_checkin, save_goal


def verify():
    application = create_app()
    with application.app_context():
        if db.engine.dialect.name != "postgresql" or db.engine.url.database != "vitalilab_test":
            raise RuntimeError("Refusing writes outside the disposable PostgreSQL CI database")
        tables = inspect(db.engine).get_table_names()
        assert len(tables) == 10  # Nine business tables plus Alembic metadata.
        user = User(email="ci-release@example.com")
        user.set_password("CiFixtureOnly2026!")
        user.profile = UserProfile(display_name="Fixture CI")
        db.session.add(user)
        db.session.commit()
        habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
        assert save_goal(user, habit, 3)
        assert save_checkin(user, 2, 4)
        assert save_checkin(user, 4, 3)
        assert db.session.scalar(db.select(db.func.count(DailyCheckIn.id))) == 1
        db.session.add(UserGoal(user_id=user.id, habit_id=habit.id, target_days=3))
        _expect_constraint_error()
        db.session.add(DailyCheckIn(user_id=user.id, checked_on=local_day(user), energy=9, focus=2))
        _expect_constraint_error()
        print("PostgreSQL: nine entities, constraints, idempotent reflection and goal verified.")


def _expect_constraint_error():
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    else:
        raise AssertionError("Expected database constraint rejection")


if __name__ == "__main__":
    verify()
