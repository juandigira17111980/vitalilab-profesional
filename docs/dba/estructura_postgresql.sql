-- SOLO ESTRUCTURA: no contiene filas, roles ni contrasenas.
-- Restaurar UNICAMENTE en una base de estudio VACIA; public ya debe existir.
--
-- PostgreSQL database dump
--


-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--



--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: announcements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.announcements (
    id integer NOT NULL,
    author_user_id integer NOT NULL,
    title character varying(150) NOT NULL,
    body text NOT NULL,
    status character varying(20) NOT NULL,
    published_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_announcements_valid_status CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'published'::character varying, 'archived'::character varying])::text[])))
);


--
-- Name: announcements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.announcements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: announcements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.announcements_id_seq OWNED BY public.announcements.id;


--
-- Name: audit_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_events (
    id integer NOT NULL,
    actor_user_id integer,
    action character varying(80) NOT NULL,
    entity_type character varying(50) NOT NULL,
    entity_id character varying(80),
    metadata_redacted json NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: audit_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.audit_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.audit_events_id_seq OWNED BY public.audit_events.id;


--
-- Name: daily_checkins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.daily_checkins (
    id integer NOT NULL,
    user_id integer NOT NULL,
    checked_on date NOT NULL,
    energy integer NOT NULL,
    focus integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_daily_checkins_valid_energy CHECK (((energy >= 1) AND (energy <= 5))),
    CONSTRAINT ck_daily_checkins_valid_focus CHECK (((focus >= 1) AND (focus <= 5)))
);


--
-- Name: daily_checkins_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.daily_checkins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: daily_checkins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.daily_checkins_id_seq OWNED BY public.daily_checkins.id;


--
-- Name: habit_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.habit_entries (
    id integer NOT NULL,
    user_id integer NOT NULL,
    habit_id integer NOT NULL,
    completed_on date NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: habit_entries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.habit_entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: habit_entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.habit_entries_id_seq OWNED BY public.habit_entries.id;


--
-- Name: habits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.habits (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(280) NOT NULL,
    category character varying(50) NOT NULL,
    icon character varying(20) NOT NULL,
    points integer NOT NULL,
    active boolean NOT NULL,
    sort_order integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_habits_valid_points CHECK (((points >= 1) AND (points <= 100)))
);


--
-- Name: habits_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.habits_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: habits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.habits_id_seq OWNED BY public.habits.id;


--
-- Name: health_measurements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.health_measurements (
    id integer NOT NULL,
    user_id integer NOT NULL,
    weight_kg numeric(5,2) NOT NULL,
    height_cm numeric(5,2) NOT NULL,
    bmi_snapshot numeric(5,2) NOT NULL,
    measured_on date NOT NULL,
    created_at timestamp without time zone NOT NULL,
    age_months integer,
    reference_sex character varying(12),
    reference_source character varying(32),
    growth_percentile numeric(5,2),
    CONSTRAINT ck_health_measurements_valid_bmi CHECK (((bmi_snapshot >= (5)::numeric) AND (bmi_snapshot <= (100)::numeric))),
    CONSTRAINT ck_health_measurements_valid_growth_percentile CHECK (((growth_percentile IS NULL) OR ((growth_percentile >= (0)::numeric) AND (growth_percentile <= (100)::numeric)))),
    CONSTRAINT ck_health_measurements_valid_height CHECK (((height_cm >= (50)::numeric) AND (height_cm <= (250)::numeric))),
    CONSTRAINT ck_health_measurements_valid_measurement_reference_sex CHECK (((reference_sex IS NULL) OR ((reference_sex)::text = ANY ((ARRAY['male'::character varying, 'female'::character varying])::text[])))),
    CONSTRAINT ck_health_measurements_valid_weight CHECK (((weight_kg >= (10)::numeric) AND (weight_kg <= (500)::numeric)))
);


--
-- Name: health_measurements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.health_measurements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: health_measurements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.health_measurements_id_seq OWNED BY public.health_measurements.id;


--
-- Name: personal_routines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.personal_routines (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying(80) NOT NULL,
    description character varying(500) NOT NULL,
    goal character varying(12) NOT NULL,
    active boolean NOT NULL,
    revision integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_personal_routines_valid_routine_goal CHECK (((goal)::text = ANY ((ARRAY['center'::character varying, 'energy'::character varying, 'strength'::character varying])::text[]))),
    CONSTRAINT ck_personal_routines_valid_routine_revision CHECK ((revision >= 1))
);


--
-- Name: personal_routines_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.personal_routines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: personal_routines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.personal_routines_id_seq OWNED BY public.personal_routines.id;


--
-- Name: routine_completions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.routine_completions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    routine_slug character varying(60) NOT NULL,
    habit_id integer NOT NULL,
    completed_on date NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: routine_completions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.routine_completions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: routine_completions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.routine_completions_id_seq OWNED BY public.routine_completions.id;


--
-- Name: routine_exercises; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.routine_exercises (
    id integer NOT NULL,
    routine_id integer NOT NULL,
    "position" integer NOT NULL,
    name character varying(80) NOT NULL,
    sets integer NOT NULL,
    repetitions integer,
    duration_seconds integer,
    rest_seconds integer NOT NULL,
    instructions character varying(280) NOT NULL,
    visual character varying(12) NOT NULL,
    CONSTRAINT ck_routine_exercises_exercise_has_dose CHECK (((repetitions IS NOT NULL) OR (duration_seconds IS NOT NULL))),
    CONSTRAINT ck_routine_exercises_valid_exercise_duration CHECK (((duration_seconds IS NULL) OR ((duration_seconds >= 5) AND (duration_seconds <= 3600)))),
    CONSTRAINT ck_routine_exercises_valid_exercise_position CHECK ((("position" >= 0) AND ("position" <= 11))),
    CONSTRAINT ck_routine_exercises_valid_exercise_reps CHECK (((repetitions IS NULL) OR ((repetitions >= 1) AND (repetitions <= 200)))),
    CONSTRAINT ck_routine_exercises_valid_exercise_rest CHECK (((rest_seconds >= 0) AND (rest_seconds <= 600))),
    CONSTRAINT ck_routine_exercises_valid_exercise_sets CHECK (((sets >= 1) AND (sets <= 20))),
    CONSTRAINT ck_routine_exercises_valid_exercise_visual CHECK (((visual)::text = ANY ((ARRAY['posture'::character varying, 'march'::character varying, 'palms'::character varying, 'shoulders'::character varying, 'wall'::character varying, 'walk'::character varying, 'breathing'::character varying, 'custom'::character varying])::text[])))
);


--
-- Name: routine_exercises_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.routine_exercises_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: routine_exercises_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.routine_exercises_id_seq OWNED BY public.routine_exercises.id;


--
-- Name: school_enrollment_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.school_enrollment_requests (
    id integer NOT NULL,
    user_id integer NOT NULL,
    school_name character varying(160) NOT NULL,
    group_name character varying(80) NOT NULL,
    requested_role character varying(12) NOT NULL,
    status character varying(12) NOT NULL,
    reviewed_at timestamp without time zone,
    reviewed_by_user_id integer,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_school_enrollment_requests_valid_enrollment_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'resolved'::character varying, 'rejected'::character varying, 'cancelled'::character varying])::text[]))),
    CONSTRAINT ck_school_enrollment_requests_valid_requested_role CHECK (((requested_role)::text = ANY ((ARRAY['student'::character varying, 'teacher'::character varying])::text[])))
);


--
-- Name: school_enrollment_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.school_enrollment_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: school_enrollment_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.school_enrollment_requests_id_seq OWNED BY public.school_enrollment_requests.id;


--
-- Name: school_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.school_groups (
    id integer NOT NULL,
    school_id integer NOT NULL,
    name character varying(80) NOT NULL,
    academic_year integer NOT NULL,
    active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_school_groups_valid_academic_year CHECK (((academic_year >= 2020) AND (academic_year <= 2100)))
);


--
-- Name: school_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.school_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: school_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.school_groups_id_seq OWNED BY public.school_groups.id;


--
-- Name: school_memberships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.school_memberships (
    id integer NOT NULL,
    user_id integer NOT NULL,
    school_id integer NOT NULL,
    group_id integer,
    requested_role character varying(12) NOT NULL,
    status character varying(12) NOT NULL,
    allow_aggregate boolean NOT NULL,
    aggregate_since timestamp without time zone,
    reviewed_at timestamp without time zone,
    reviewed_by_user_id integer,
    authorization_confirmed boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_school_memberships_valid_membership_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying, 'revoked'::character varying])::text[]))),
    CONSTRAINT ck_school_memberships_valid_school_role CHECK (((requested_role)::text = ANY ((ARRAY['student'::character varying, 'teacher'::character varying])::text[])))
);


--
-- Name: school_memberships_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.school_memberships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: school_memberships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.school_memberships_id_seq OWNED BY public.school_memberships.id;


--
-- Name: schools; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schools (
    id integer NOT NULL,
    code character varying(60) NOT NULL,
    name character varying(160) NOT NULL,
    active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: schools_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.schools_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: schools_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.schools_id_seq OWNED BY public.schools.id;


--
-- Name: teacher_group_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teacher_group_assignments (
    id integer NOT NULL,
    membership_id integer NOT NULL,
    school_id integer NOT NULL,
    group_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: teacher_group_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.teacher_group_assignments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: teacher_group_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.teacher_group_assignments_id_seq OWNED BY public.teacher_group_assignments.id;


--
-- Name: user_goals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_goals (
    id integer NOT NULL,
    user_id integer NOT NULL,
    habit_id integer NOT NULL,
    target_days integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_user_goals_valid_target_days CHECK (((target_days >= 1) AND (target_days <= 7)))
);


--
-- Name: user_goals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_goals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_goals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_goals_id_seq OWNED BY public.user_goals.id;


--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_profiles (
    user_id integer NOT NULL,
    display_name character varying(80) NOT NULL,
    birth_date date,
    grade character varying(80),
    timezone character varying(50) NOT NULL,
    privacy_version character varying(20) NOT NULL,
    privacy_accepted_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    usage_mode character varying(20) DEFAULT 'personal'::character varying NOT NULL,
    institution_name character varying(160),
    reference_sex character varying(12) DEFAULT 'unspecified'::character varying NOT NULL,
    movement_goal character varying(12) DEFAULT 'energy'::character varying NOT NULL,
    movement_preference character varying(12) DEFAULT 'adaptable'::character varying NOT NULL,
    personalization_completed_at timestamp without time zone,
    measurement_consent_at timestamp without time zone,
    CONSTRAINT ck_user_profiles_valid_movement_goal CHECK (((movement_goal)::text = ANY ((ARRAY['center'::character varying, 'energy'::character varying, 'strength'::character varying])::text[]))),
    CONSTRAINT ck_user_profiles_valid_movement_preference CHECK (((movement_preference)::text = ANY ((ARRAY['adaptable'::character varying, 'seated'::character varying, 'supported'::character varying, 'standing'::character varying])::text[]))),
    CONSTRAINT ck_user_profiles_valid_reference_sex CHECK (((reference_sex)::text = ANY ((ARRAY['unspecified'::character varying, 'female'::character varying, 'male'::character varying])::text[]))),
    CONSTRAINT ck_user_profiles_valid_usage_mode CHECK (((usage_mode)::text = ANY ((ARRAY['personal'::character varying, 'institutional'::character varying])::text[])))
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    last_login_at timestamp without time zone,
    failed_login_count integer NOT NULL,
    locked_until timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT ck_users_valid_role CHECK (((role)::text = ANY ((ARRAY['user'::character varying, 'admin'::character varying])::text[]))),
    CONSTRAINT ck_users_valid_status CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: announcements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announcements ALTER COLUMN id SET DEFAULT nextval('public.announcements_id_seq'::regclass);


--
-- Name: audit_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_events ALTER COLUMN id SET DEFAULT nextval('public.audit_events_id_seq'::regclass);


--
-- Name: daily_checkins id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_checkins ALTER COLUMN id SET DEFAULT nextval('public.daily_checkins_id_seq'::regclass);


--
-- Name: habit_entries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habit_entries ALTER COLUMN id SET DEFAULT nextval('public.habit_entries_id_seq'::regclass);


--
-- Name: habits id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habits ALTER COLUMN id SET DEFAULT nextval('public.habits_id_seq'::regclass);


--
-- Name: health_measurements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.health_measurements ALTER COLUMN id SET DEFAULT nextval('public.health_measurements_id_seq'::regclass);


--
-- Name: personal_routines id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personal_routines ALTER COLUMN id SET DEFAULT nextval('public.personal_routines_id_seq'::regclass);


--
-- Name: routine_completions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_completions ALTER COLUMN id SET DEFAULT nextval('public.routine_completions_id_seq'::regclass);


--
-- Name: routine_exercises id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_exercises ALTER COLUMN id SET DEFAULT nextval('public.routine_exercises_id_seq'::regclass);


--
-- Name: school_enrollment_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_enrollment_requests ALTER COLUMN id SET DEFAULT nextval('public.school_enrollment_requests_id_seq'::regclass);


--
-- Name: school_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_groups ALTER COLUMN id SET DEFAULT nextval('public.school_groups_id_seq'::regclass);


--
-- Name: school_memberships id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships ALTER COLUMN id SET DEFAULT nextval('public.school_memberships_id_seq'::regclass);


--
-- Name: schools id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schools ALTER COLUMN id SET DEFAULT nextval('public.schools_id_seq'::regclass);


--
-- Name: teacher_group_assignments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teacher_group_assignments ALTER COLUMN id SET DEFAULT nextval('public.teacher_group_assignments_id_seq'::regclass);


--
-- Name: user_goals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goals ALTER COLUMN id SET DEFAULT nextval('public.user_goals_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: announcements pk_announcements; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT pk_announcements PRIMARY KEY (id);


--
-- Name: audit_events pk_audit_events; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_events
    ADD CONSTRAINT pk_audit_events PRIMARY KEY (id);


--
-- Name: daily_checkins pk_daily_checkins; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_checkins
    ADD CONSTRAINT pk_daily_checkins PRIMARY KEY (id);


--
-- Name: habit_entries pk_habit_entries; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habit_entries
    ADD CONSTRAINT pk_habit_entries PRIMARY KEY (id);


--
-- Name: habits pk_habits; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habits
    ADD CONSTRAINT pk_habits PRIMARY KEY (id);


--
-- Name: health_measurements pk_health_measurements; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.health_measurements
    ADD CONSTRAINT pk_health_measurements PRIMARY KEY (id);


--
-- Name: personal_routines pk_personal_routines; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personal_routines
    ADD CONSTRAINT pk_personal_routines PRIMARY KEY (id);


--
-- Name: routine_completions pk_routine_completions; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_completions
    ADD CONSTRAINT pk_routine_completions PRIMARY KEY (id);


--
-- Name: routine_exercises pk_routine_exercises; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_exercises
    ADD CONSTRAINT pk_routine_exercises PRIMARY KEY (id);


--
-- Name: school_enrollment_requests pk_school_enrollment_requests; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_enrollment_requests
    ADD CONSTRAINT pk_school_enrollment_requests PRIMARY KEY (id);


--
-- Name: school_groups pk_school_groups; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_groups
    ADD CONSTRAINT pk_school_groups PRIMARY KEY (id);


--
-- Name: school_memberships pk_school_memberships; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT pk_school_memberships PRIMARY KEY (id);


--
-- Name: schools pk_schools; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT pk_schools PRIMARY KEY (id);


--
-- Name: teacher_group_assignments pk_teacher_group_assignments; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teacher_group_assignments
    ADD CONSTRAINT pk_teacher_group_assignments PRIMARY KEY (id);


--
-- Name: user_goals pk_user_goals; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goals
    ADD CONSTRAINT pk_user_goals PRIMARY KEY (id);


--
-- Name: user_profiles pk_user_profiles; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT pk_user_profiles PRIMARY KEY (user_id);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- Name: habit_entries uq_habit_daily; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habit_entries
    ADD CONSTRAINT uq_habit_daily UNIQUE (user_id, habit_id, completed_on);


--
-- Name: habits uq_habits_code; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habits
    ADD CONSTRAINT uq_habits_code UNIQUE (code);


--
-- Name: routine_completions uq_routine_daily; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_completions
    ADD CONSTRAINT uq_routine_daily UNIQUE (user_id, routine_slug, completed_on);


--
-- Name: routine_exercises uq_routine_exercise_position; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_exercises
    ADD CONSTRAINT uq_routine_exercise_position UNIQUE (routine_id, "position");


--
-- Name: school_enrollment_requests uq_school_enrollment_requests_user_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_enrollment_requests
    ADD CONSTRAINT uq_school_enrollment_requests_user_id UNIQUE (user_id);


--
-- Name: school_groups uq_school_group_id_school; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_groups
    ADD CONSTRAINT uq_school_group_id_school UNIQUE (id, school_id);


--
-- Name: school_groups uq_school_group_year_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_groups
    ADD CONSTRAINT uq_school_group_year_name UNIQUE (school_id, academic_year, name);


--
-- Name: school_memberships uq_school_membership_id_school; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT uq_school_membership_id_school UNIQUE (id, school_id);


--
-- Name: school_memberships uq_school_memberships_user_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT uq_school_memberships_user_id UNIQUE (user_id);


--
-- Name: schools uq_schools_code; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT uq_schools_code UNIQUE (code);


--
-- Name: teacher_group_assignments uq_teacher_group; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teacher_group_assignments
    ADD CONSTRAINT uq_teacher_group UNIQUE (membership_id, group_id);


--
-- Name: daily_checkins uq_user_daily_checkin; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_checkins
    ADD CONSTRAINT uq_user_daily_checkin UNIQUE (user_id, checked_on);


--
-- Name: user_goals uq_user_goal_habit; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goals
    ADD CONSTRAINT uq_user_goal_habit UNIQUE (user_id, habit_id);


--
-- Name: ix_announcements_author_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcements_author_user_id ON public.announcements USING btree (author_user_id);


--
-- Name: ix_announcements_published_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcements_published_at ON public.announcements USING btree (published_at);


--
-- Name: ix_announcements_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcements_status ON public.announcements USING btree (status);


--
-- Name: ix_announcements_status_published_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcements_status_published_at ON public.announcements USING btree (status, published_at);


--
-- Name: ix_assignment_group; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_assignment_group ON public.teacher_group_assignments USING btree (group_id);


--
-- Name: ix_audit_events_action; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_events_action ON public.audit_events USING btree (action);


--
-- Name: ix_audit_events_actor_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_events_actor_user_id ON public.audit_events USING btree (actor_user_id);


--
-- Name: ix_audit_events_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_events_created_at ON public.audit_events USING btree (created_at);


--
-- Name: ix_enrollment_status_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_enrollment_status_created ON public.school_enrollment_requests USING btree (status, created_at);


--
-- Name: ix_habit_entries_completed_on; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_habit_entries_completed_on ON public.habit_entries USING btree (completed_on);


--
-- Name: ix_habit_entries_habit_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_habit_entries_habit_id ON public.habit_entries USING btree (habit_id);


--
-- Name: ix_habit_entries_user_completed_on; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_habit_entries_user_completed_on ON public.habit_entries USING btree (user_id, completed_on);


--
-- Name: ix_habit_entries_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_habit_entries_user_id ON public.habit_entries USING btree (user_id);


--
-- Name: ix_health_measurements_measured_on; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_health_measurements_measured_on ON public.health_measurements USING btree (measured_on);


--
-- Name: ix_health_measurements_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_health_measurements_user_id ON public.health_measurements USING btree (user_id);


--
-- Name: ix_health_measurements_user_measured_on; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_health_measurements_user_measured_on ON public.health_measurements USING btree (user_id, measured_on);


--
-- Name: ix_membership_group_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_membership_group_status ON public.school_memberships USING btree (group_id, status);


--
-- Name: ix_personal_routines_user_active; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_personal_routines_user_active ON public.personal_routines USING btree (user_id, active);


--
-- Name: ix_routine_completions_habit_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_routine_completions_habit_id ON public.routine_completions USING btree (habit_id);


--
-- Name: ix_routine_completions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_routine_completions_user_id ON public.routine_completions USING btree (user_id);


--
-- Name: ix_school_enrollment_requests_reviewed_by_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_school_enrollment_requests_reviewed_by_user_id ON public.school_enrollment_requests USING btree (reviewed_by_user_id);


--
-- Name: ix_school_groups_school_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_school_groups_school_id ON public.school_groups USING btree (school_id);


--
-- Name: ix_school_memberships_reviewed_by_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_school_memberships_reviewed_by_user_id ON public.school_memberships USING btree (reviewed_by_user_id);


--
-- Name: ix_school_memberships_school_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_school_memberships_school_id ON public.school_memberships USING btree (school_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: announcements fk_announcements_author_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT fk_announcements_author_user_id_users FOREIGN KEY (author_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: teacher_group_assignments fk_assignment_group_school; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teacher_group_assignments
    ADD CONSTRAINT fk_assignment_group_school FOREIGN KEY (group_id, school_id) REFERENCES public.school_groups(id, school_id) ON DELETE RESTRICT;


--
-- Name: teacher_group_assignments fk_assignment_membership_school; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teacher_group_assignments
    ADD CONSTRAINT fk_assignment_membership_school FOREIGN KEY (membership_id, school_id) REFERENCES public.school_memberships(id, school_id) ON DELETE CASCADE;


--
-- Name: audit_events fk_audit_events_actor_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_events
    ADD CONSTRAINT fk_audit_events_actor_user_id_users FOREIGN KEY (actor_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: daily_checkins fk_daily_checkins_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_checkins
    ADD CONSTRAINT fk_daily_checkins_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: habit_entries fk_habit_entries_habit_id_habits; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habit_entries
    ADD CONSTRAINT fk_habit_entries_habit_id_habits FOREIGN KEY (habit_id) REFERENCES public.habits(id) ON DELETE RESTRICT;


--
-- Name: habit_entries fk_habit_entries_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.habit_entries
    ADD CONSTRAINT fk_habit_entries_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: health_measurements fk_health_measurements_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.health_measurements
    ADD CONSTRAINT fk_health_measurements_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: personal_routines fk_personal_routines_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personal_routines
    ADD CONSTRAINT fk_personal_routines_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: routine_completions fk_routine_completions_habit_id_habits; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_completions
    ADD CONSTRAINT fk_routine_completions_habit_id_habits FOREIGN KEY (habit_id) REFERENCES public.habits(id) ON DELETE RESTRICT;


--
-- Name: routine_completions fk_routine_completions_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_completions
    ADD CONSTRAINT fk_routine_completions_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: routine_exercises fk_routine_exercises_routine_id_personal_routines; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routine_exercises
    ADD CONSTRAINT fk_routine_exercises_routine_id_personal_routines FOREIGN KEY (routine_id) REFERENCES public.personal_routines(id) ON DELETE CASCADE;


--
-- Name: school_enrollment_requests fk_school_enrollment_requests_reviewed_by_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_enrollment_requests
    ADD CONSTRAINT fk_school_enrollment_requests_reviewed_by_user_id_users FOREIGN KEY (reviewed_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: school_enrollment_requests fk_school_enrollment_requests_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_enrollment_requests
    ADD CONSTRAINT fk_school_enrollment_requests_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: school_groups fk_school_groups_school_id_schools; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_groups
    ADD CONSTRAINT fk_school_groups_school_id_schools FOREIGN KEY (school_id) REFERENCES public.schools(id) ON DELETE RESTRICT;


--
-- Name: school_memberships fk_school_membership_group_school; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT fk_school_membership_group_school FOREIGN KEY (group_id, school_id) REFERENCES public.school_groups(id, school_id) ON DELETE RESTRICT;


--
-- Name: school_memberships fk_school_memberships_reviewed_by_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT fk_school_memberships_reviewed_by_user_id_users FOREIGN KEY (reviewed_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: school_memberships fk_school_memberships_school_id_schools; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT fk_school_memberships_school_id_schools FOREIGN KEY (school_id) REFERENCES public.schools(id) ON DELETE RESTRICT;


--
-- Name: school_memberships fk_school_memberships_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.school_memberships
    ADD CONSTRAINT fk_school_memberships_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_goals fk_user_goals_habit_id_habits; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goals
    ADD CONSTRAINT fk_user_goals_habit_id_habits FOREIGN KEY (habit_id) REFERENCES public.habits(id) ON DELETE RESTRICT;


--
-- Name: user_goals fk_user_goals_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goals
    ADD CONSTRAINT fk_user_goals_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_profiles fk_user_profiles_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT fk_user_profiles_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


