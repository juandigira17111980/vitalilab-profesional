"""Exercise additive entities only in the disposable CI database."""

from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.extensions import db
from app.models import (
    DailyCheckIn,
    Habit,
    HealthMeasurement,
    PersonalRoutine,
    RoutineCompletion,
    RoutineExercise,
    School,
    SchoolEnrollmentRequest,
    SchoolGroup,
    SchoolMembership,
    TeacherGroupAssignment,
    User,
    UserGoal,
    UserProfile,
)
from app.services.clock import local_day
from app.services.movement import register_routine
from app.services.school import seed_schools
from app.services.wellness import save_checkin, save_goal


def verify():
    application = create_app()
    with application.app_context():
        if db.engine.dialect.name != "postgresql" or db.engine.url.database != "vitalilab_test":
            raise RuntimeError("Refusing writes outside the disposable PostgreSQL CI database")
        tables = inspect(db.engine).get_table_names()
        assert len(tables) == 18  # Seventeen business tables plus Alembic metadata.
        legacy = db.session.scalar(
            db.select(User).where(User.email == "ci-before-migration@example.com")
        )
        assert legacy is not None and legacy.profile.grade == "Nota previa"
        assert legacy.profile.movement_goal == "center"
        assert legacy.profile.movement_preference == "adaptable"
        assert legacy.profile.measurement_consent_at is None
        assert legacy.profile.personalization_completed_at is None
        assert legacy.measurements[0].bmi_snapshot == Decimal("22.86")
        user = User(email="ci-release@example.com")
        user.set_password("CiFixtureOnly2026!")
        user.profile = UserProfile(display_name="Fixture CI")
        db.session.add(user)
        db.session.commit()
        assert user.profile.usage_mode == "personal"
        user.profile.usage_mode = "institutional"
        user.profile.institution_name = "Institución ficticia CI"
        user.profile.grade = "Grupo CI"
        db.session.commit()
        db.session.expire_all()
        assert user.profile.usage_mode == "institutional"
        assert user.profile.institution_name == "Institución ficticia CI"
        user.profile.usage_mode = "admin"
        _expect_constraint_error()
        assert seed_schools() == 2
        schools = list(db.session.scalars(db.select(School).order_by(School.id)))
        groups = [
            SchoolGroup(school_id=school.id, name="CI ficticio", academic_year=2026)
            for school in schools
        ]
        db.session.add_all(groups)
        db.session.commit()
        member = SchoolMembership(
            user_id=user.id,
            school_id=schools[0].id,
            group_id=groups[0].id,
            requested_role="teacher",
            status="pending",
        )
        db.session.add(member)
        db.session.commit()
        assignment = TeacherGroupAssignment(
            membership_id=member.id, school_id=schools[0].id, group_id=groups[0].id
        )
        db.session.add(assignment)
        db.session.commit()
        # Composite foreign keys reject cross-school relationships, even via direct SQL/ORM.
        member.group_id = groups[1].id
        _expect_constraint_error()
        assignment.group_id = groups[1].id
        _expect_constraint_error()
        db.session.add(
            HealthMeasurement(
                user_id=user.id,
                weight_kg=Decimal("14"),
                height_cm=Decimal("100"),
                bmi_snapshot=Decimal("14"),
                measured_on=local_day(user),
                age_months=90,
                reference_sex="male",
                reference_source="WHO-2007-LMS",
                growth_percentile=Decimal("50"),
            )
        )
        db.session.commit()
        user_id = user.id

        def concurrent_completion(_):
            with application.app_context():
                return register_routine(db.session.get(User, user_id), "fortalece-tu-centro")

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(concurrent_completion, range(2)))
        assert sum(result["created"] for result in results) == 1
        assert sum(result["points"] for result in results) == 15
        db.session.expire_all()
        assert db.session.scalar(db.select(db.func.count(RoutineCompletion.id))) == 1
        custom_user = User(email="ci-custom@example.com")
        custom_user.set_password("CiFixtureOnly2026!")
        custom_user.profile = UserProfile(display_name="Rutina privada CI")
        db.session.add(custom_user)
        db.session.flush()
        custom_user_id = custom_user.id
        personal = PersonalRoutine(user_id=custom_user.id, name="Mi rutina CI", goal="strength")
        db.session.add(personal)
        db.session.flush()
        exercise = RoutineExercise(
            routine_id=personal.id,
            position=0,
            name="Palmas",
            sets=2,
            duration_seconds=10,
            rest_seconds=30,
            instructions="A mi ritmo",
            visual="palms",
        )
        db.session.add(exercise)
        db.session.add(
            SchoolEnrollmentRequest(
                user_id=custom_user.id,
                school_name="Escrito CI",
                group_name="Grupo CI",
                requested_role="student",
            )
        )
        db.session.commit()
        slug = personal.slug

        def concurrent_personal(_):
            with application.app_context():
                return register_routine(db.session.get(User, custom_user_id), slug)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(concurrent_personal, range(2)))
        assert sum(result["created"] for result in results) == 1
        assert sum(result["points"] for result in results) == 15
        db.session.expire_all()
        exercise.duration_seconds = None
        _expect_constraint_error()
        assert user.profile.usage_mode == "institutional"
        habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
        assert save_goal(user, habit, 3)
        assert save_checkin(user, 2, 4)
        assert save_checkin(user, 4, 3)
        assert db.session.scalar(db.select(db.func.count(DailyCheckIn.id))) == 1
        db.session.add(UserGoal(user_id=user.id, habit_id=habit.id, target_days=3))
        _expect_constraint_error()
        db.session.add(DailyCheckIn(user_id=user.id, checked_on=local_day(user), energy=9, focus=2))
        _expect_constraint_error()
        print(
            "PostgreSQL: seventeen entities, previous data preserved, tenant FKs, "
            "growth snapshots, "
            "concurrent guided/private routine idempotence, dose constraints and goals verified."
        )


def _expect_constraint_error():
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    else:
        raise AssertionError("Expected database constraint rejection")


if __name__ == "__main__":
    verify()
