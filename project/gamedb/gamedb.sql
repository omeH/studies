--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE gamedb;
--
-- Name: gamedb; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE gamedb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ru_RU.UTF-8' LC_CTYPE = 'ru_RU.UTF-8';


ALTER DATABASE gamedb OWNER TO postgres;

\connect gamedb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: get_const_league_id(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION get_const_league_id(value integer) RETURNS smallint
    LANGUAGE sql
    AS $$
select id from const_league where rating_min < value and rating_max > value;
$$;


ALTER FUNCTION public.get_const_league_id(value integer) OWNER TO postgres;

--
-- Name: set_created_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION set_created_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin 
new.created := current_timestamp(0); return new;
end;
$$;


ALTER FUNCTION public.set_created_timestamp() OWNER TO postgres;

--
-- Name: set_player_league_id(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION set_player_league_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin 
new.league_id := get_const_league_id(new.rating);
return new;
end;
$$;


ALTER FUNCTION public.set_player_league_id() OWNER TO postgres;

--
-- Name: set_updated_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION set_updated_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
new.updated := current_timestamp(0);
return new;
end;
$$;


ALTER FUNCTION public.set_updated_timestamp() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: const_achievement; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE const_achievement (
    id smallint NOT NULL,
    achievement character varying(30),
    created timestamp(0) without time zone,
    updated timestamp(0) without time zone
);


ALTER TABLE public.const_achievement OWNER TO postgres;

--
-- Name: TABLE const_achievement; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE const_achievement IS 'List of possible achievements player';


--
-- Name: COLUMN const_achievement.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_achievement.id IS 'Achievement ID number';


--
-- Name: COLUMN const_achievement.achievement; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_achievement.achievement IS 'Discription of achievement';


--
-- Name: COLUMN const_achievement.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_achievement.created IS 'Time created row';


--
-- Name: COLUMN const_achievement.updated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_achievement.updated IS 'Time last updated row';


--
-- Name: const_achievement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE const_achievement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.const_achievement_id_seq OWNER TO postgres;

--
-- Name: const_achievement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE const_achievement_id_seq OWNED BY const_achievement.id;


--
-- Name: const_event_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE const_event_type (
    id smallint NOT NULL,
    type character varying(20),
    created timestamp(0) without time zone,
    updated timestamp(0) without time zone
);


ALTER TABLE public.const_event_type OWNER TO postgres;

--
-- Name: TABLE const_event_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE const_event_type IS 'List of possible event of game';


--
-- Name: COLUMN const_event_type.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_event_type.id IS 'Game type ID number';


--
-- Name: COLUMN const_event_type.type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_event_type.type IS 'Mode of game';


--
-- Name: COLUMN const_event_type.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_event_type.created IS 'Time created row';


--
-- Name: COLUMN const_event_type.updated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_event_type.updated IS 'Time last updated row';


--
-- Name: const_game_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE const_game_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.const_game_type_id_seq OWNER TO postgres;

--
-- Name: const_game_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE const_game_type_id_seq OWNED BY const_event_type.id;


--
-- Name: const_league; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE const_league (
    id smallint NOT NULL,
    league character varying(10),
    rating_min integer,
    rating_max integer,
    created timestamp(0) without time zone,
    updated timestamp(0) without time zone
);


ALTER TABLE public.const_league OWNER TO postgres;

--
-- Name: TABLE const_league; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE const_league IS 'List of names of leagues and their boundaries';


--
-- Name: COLUMN const_league.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league.id IS 'League ID number';


--
-- Name: COLUMN const_league.league; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league.league IS 'Name of the league';


--
-- Name: COLUMN const_league.rating_min; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league.rating_min IS 'The minimum number of points required for this league';


--
-- Name: COLUMN const_league.rating_max; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league.rating_max IS 'The maximun number of points allowed for this league';


--
-- Name: COLUMN const_league.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league.created IS 'Time created row';


--
-- Name: COLUMN const_league.updated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league.updated IS 'Time last updated row';


--
-- Name: const_league_bonus; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE const_league_bonus (
    id smallint NOT NULL,
    league_id smallint,
    points smallint,
    created timestamp(0) without time zone,
    updated timestamp(0) without time zone
);


ALTER TABLE public.const_league_bonus OWNER TO postgres;

--
-- Name: TABLE const_league_bonus; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE const_league_bonus IS 'List of relevant bonuses leagues';


--
-- Name: COLUMN const_league_bonus.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league_bonus.id IS 'League bonus ID number';


--
-- Name: COLUMN const_league_bonus.league_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league_bonus.league_id IS 'League ID number';


--
-- Name: COLUMN const_league_bonus.points; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league_bonus.points IS 'Number of points awarded for a victory in the game';


--
-- Name: COLUMN const_league_bonus.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league_bonus.created IS 'Time created row';


--
-- Name: COLUMN const_league_bonus.updated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_league_bonus.updated IS 'Time last updated row';


--
-- Name: const_league_bonuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE const_league_bonuses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.const_league_bonuses_id_seq OWNER TO postgres;

--
-- Name: const_league_bonuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE const_league_bonuses_id_seq OWNED BY const_league_bonus.id;


--
-- Name: const_league_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE const_league_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.const_league_id_seq OWNER TO postgres;

--
-- Name: const_league_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE const_league_id_seq OWNED BY const_league.id;


--
-- Name: const_platform; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE const_platform (
    id smallint NOT NULL,
    platform character varying(10),
    created timestamp(0) without time zone,
    updated timestamp(0) without time zone
);


ALTER TABLE public.const_platform OWNER TO postgres;

--
-- Name: TABLE const_platform; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE const_platform IS 'List of the supported platforms';


--
-- Name: COLUMN const_platform.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_platform.id IS 'Platform ID number';


--
-- Name: COLUMN const_platform.platform; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_platform.platform IS 'Name of the operating system';


--
-- Name: COLUMN const_platform.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_platform.created IS 'Time created row';


--
-- Name: COLUMN const_platform.updated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN const_platform.updated IS 'Time last updated row';


--
-- Name: const_platform_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE const_platform_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.const_platform_id_seq OWNER TO postgres;

--
-- Name: const_platform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE const_platform_id_seq OWNED BY const_platform.id;


--
-- Name: game_event; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE game_event (
    id integer NOT NULL,
    event_type_id smallint,
    event_data json,
    created timestamp(0) without time zone
);


ALTER TABLE public.game_event OWNER TO postgres;

--
-- Name: TABLE game_event; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE game_event IS 'Information about the game event';


--
-- Name: COLUMN game_event.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_event.id IS 'Game event ID number';


--
-- Name: COLUMN game_event.event_type_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_event.event_type_id IS 'Event type ID number';


--
-- Name: COLUMN game_event.event_data; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_event.event_data IS 'Information about event';


--
-- Name: COLUMN game_event.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_event.created IS 'Time created row';


--
-- Name: game_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE game_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_event_id_seq OWNER TO postgres;

--
-- Name: game_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE game_event_id_seq OWNED BY game_event.id;


--
-- Name: game_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE game_session (
    id integer NOT NULL,
    player_id integer,
    start_session timestamp(0) without time zone,
    end_session timestamp(0) without time zone,
    ip character varying(15),
    platform_id smallint,
    created timestamp(0) without time zone
);


ALTER TABLE public.game_session OWNER TO postgres;

--
-- Name: TABLE game_session; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE game_session IS 'Information about the game session';


--
-- Name: COLUMN game_session.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.id IS 'Game session ID number';


--
-- Name: COLUMN game_session.player_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.player_id IS 'Player ID number';


--
-- Name: COLUMN game_session.start_session; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.start_session IS 'The beginning of the game session';


--
-- Name: COLUMN game_session.end_session; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.end_session IS 'The end of the game session';


--
-- Name: COLUMN game_session.ip; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.ip IS 'IP-address of the player';


--
-- Name: COLUMN game_session.platform_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.platform_id IS 'Platform ID number';


--
-- Name: COLUMN game_session.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN game_session.created IS 'Time created row';


--
-- Name: game_session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE game_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_session_id_seq OWNER TO postgres;

--
-- Name: game_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE game_session_id_seq OWNED BY game_session.id;


--
-- Name: player; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE player (
    id integer NOT NULL,
    nickname character varying(20),
    game_count integer,
    victory_count integer,
    rating integer,
    league_id smallint,
    created timestamp(0) without time zone,
    updated timestamp(0) without time zone
);


ALTER TABLE public.player OWNER TO postgres;

--
-- Name: TABLE player; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE player IS 'Information about player';


--
-- Name: COLUMN player.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.id IS 'Player ID number';


--
-- Name: COLUMN player.nickname; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.nickname IS 'Nickname player';


--
-- Name: COLUMN player.game_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.game_count IS 'Number of games played';


--
-- Name: COLUMN player.victory_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.victory_count IS 'Number of games won';


--
-- Name: COLUMN player.rating; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.rating IS 'The number of points earned rankings';


--
-- Name: COLUMN player.league_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.league_id IS 'League ID number';


--
-- Name: COLUMN player.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.created IS 'Time created row';


--
-- Name: COLUMN player.updated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player.updated IS 'Time last updated row';


--
-- Name: player_achievement; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE player_achievement (
    id integer NOT NULL,
    player_id integer,
    achievement_id smallint,
    created timestamp(0) without time zone
);


ALTER TABLE public.player_achievement OWNER TO postgres;

--
-- Name: TABLE player_achievement; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE player_achievement IS 'Information about the complete player achievements';


--
-- Name: COLUMN player_achievement.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player_achievement.id IS 'Player achievement ID number';


--
-- Name: COLUMN player_achievement.player_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player_achievement.player_id IS 'Player ID number';


--
-- Name: COLUMN player_achievement.achievement_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player_achievement.achievement_id IS 'Achievement ID number';


--
-- Name: COLUMN player_achievement.created; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN player_achievement.created IS 'Time created row';


--
-- Name: player_achievement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE player_achievement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.player_achievement_id_seq OWNER TO postgres;

--
-- Name: player_achievement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE player_achievement_id_seq OWNED BY player_achievement.id;


--
-- Name: player_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.player_id_seq OWNER TO postgres;

--
-- Name: player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE player_id_seq OWNED BY player.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY const_achievement ALTER COLUMN id SET DEFAULT nextval('const_achievement_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY const_event_type ALTER COLUMN id SET DEFAULT nextval('const_game_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY const_league ALTER COLUMN id SET DEFAULT nextval('const_league_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY const_league_bonus ALTER COLUMN id SET DEFAULT nextval('const_league_bonuses_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY const_platform ALTER COLUMN id SET DEFAULT nextval('const_platform_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY game_event ALTER COLUMN id SET DEFAULT nextval('game_event_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY game_session ALTER COLUMN id SET DEFAULT nextval('game_session_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY player ALTER COLUMN id SET DEFAULT nextval('player_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY player_achievement ALTER COLUMN id SET DEFAULT nextval('player_achievement_id_seq'::regclass);


--
-- Data for Name: const_achievement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY const_achievement (id, achievement, created, updated) FROM stdin;
\.


--
-- Name: const_achievement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('const_achievement_id_seq', 1, false);


--
-- Data for Name: const_event_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY const_event_type (id, type, created, updated) FROM stdin;
2	player vs pc	2014-10-27 19:10:37	\N
3	player vs player	2014-10-27 19:10:37	\N
4	team vs team	2014-10-27 19:10:37	\N
5	all against all	2014-10-27 19:10:37	2014-10-28 10:09:44
\.


--
-- Name: const_game_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('const_game_type_id_seq', 5, true);


--
-- Data for Name: const_league; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY const_league (id, league, rating_min, rating_max, created, updated) FROM stdin;
1	novice	0	9	2014-10-27 20:06:46	2014-10-28 11:55:17
2	wooden	10	49	2014-10-27 20:06:46	2014-10-28 11:55:37
3	stony	50	99	2014-10-27 20:06:46	2014-10-28 11:55:55
4	bronzed	100	199	2014-10-27 20:06:46	2014-10-28 11:56:17
5	steely	200	499	2014-10-27 20:06:46	2014-10-28 11:56:34
6	silver	500	999	2014-10-27 20:06:46	2014-10-28 11:56:56
7	golden	1000	9999	2014-10-27 20:06:46	2014-10-28 11:57:19
8	platinum	10000	49999	2014-10-27 20:06:46	2014-10-28 11:57:57
9	diamond	50000	99999	2014-10-28 11:53:05	2014-10-28 11:58:11
\.


--
-- Data for Name: const_league_bonus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY const_league_bonus (id, league_id, points, created, updated) FROM stdin;
1	1	1	2014-10-29 19:40:15	\N
2	2	2	2014-10-29 19:40:15	\N
3	3	2	2014-10-29 19:40:15	\N
4	4	2	2014-10-29 19:40:15	\N
5	5	3	2014-10-29 19:40:15	\N
6	6	3	2014-10-29 19:40:15	\N
7	7	4	2014-10-29 19:40:15	\N
8	8	5	2014-10-29 19:40:15	\N
9	9	5	2014-10-29 19:40:15	\N
\.


--
-- Name: const_league_bonuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('const_league_bonuses_id_seq', 9, true);


--
-- Name: const_league_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('const_league_id_seq', 9, true);


--
-- Data for Name: const_platform; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY const_platform (id, platform, created, updated) FROM stdin;
1	unix	2014-10-27 20:22:16	\N
2	linux	2014-10-27 20:22:16	\N
3	bsd	2014-10-27 20:22:16	\N
4	other	2014-10-27 20:22:16	\N
\.


--
-- Name: const_platform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('const_platform_id_seq', 4, true);


--
-- Data for Name: game_event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY game_event (id, event_type_id, event_data, created) FROM stdin;
\.


--
-- Name: game_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('game_event_id_seq', 1, false);


--
-- Data for Name: game_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY game_session (id, player_id, start_session, end_session, ip, platform_id, created) FROM stdin;
\.


--
-- Name: game_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('game_session_id_seq', 1, false);


--
-- Data for Name: player; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY player (id, nickname, game_count, victory_count, rating, league_id, created, updated) FROM stdin;
1	testick	15	10	53	3	2014-10-28 15:41:00	2014-10-28 15:58:09
\.


--
-- Data for Name: player_achievement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY player_achievement (id, player_id, achievement_id, created) FROM stdin;
\.


--
-- Name: player_achievement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('player_achievement_id_seq', 1, false);


--
-- Name: player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('player_id_seq', 4, true);


--
-- Name: achievement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY const_achievement
    ADD CONSTRAINT achievement_pkey PRIMARY KEY (id);


--
-- Name: event_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY const_event_type
    ADD CONSTRAINT event_type_pkey PRIMARY KEY (id);


--
-- Name: game_event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY game_event
    ADD CONSTRAINT game_event_pkey PRIMARY KEY (id);


--
-- Name: game_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY game_session
    ADD CONSTRAINT game_session_pkey PRIMARY KEY (id);


--
-- Name: league_bonus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY const_league_bonus
    ADD CONSTRAINT league_bonus_pkey PRIMARY KEY (id);


--
-- Name: league_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY const_league
    ADD CONSTRAINT league_pkey PRIMARY KEY (id);


--
-- Name: platform_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY const_platform
    ADD CONSTRAINT platform_pkey PRIMARY KEY (id);


--
-- Name: player_achievement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY player_achievement
    ADD CONSTRAINT player_achievement_pkey PRIMARY KEY (id);


--
-- Name: player_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);


--
-- Name: const_achievement_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_achievement_created BEFORE INSERT ON const_achievement FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: const_achievement_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_achievement_updated BEFORE UPDATE ON const_achievement FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();


--
-- Name: const_event_type_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_event_type_created BEFORE INSERT ON const_event_type FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: const_event_type_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_event_type_updated BEFORE UPDATE ON const_event_type FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();


--
-- Name: const_league_bonuses_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_league_bonuses_created BEFORE INSERT ON const_league_bonus FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: const_league_bonuses_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_league_bonuses_updated BEFORE UPDATE ON const_league_bonus FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();


--
-- Name: const_league_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_league_created BEFORE INSERT ON const_league FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: const_league_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_league_updated BEFORE UPDATE ON const_league FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();


--
-- Name: const_platform_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_platform_created BEFORE INSERT ON const_platform FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: const_platform_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER const_platform_updated BEFORE UPDATE ON const_platform FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();


--
-- Name: game_event_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER game_event_created BEFORE INSERT ON game_event FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: game_session_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER game_session_created BEFORE INSERT ON game_session FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: player_achievement_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER player_achievement_created BEFORE INSERT ON player_achievement FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: player_created; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER player_created BEFORE INSERT ON player FOR EACH ROW EXECUTE PROCEDURE set_created_timestamp();


--
-- Name: player_set_league_id; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER player_set_league_id BEFORE INSERT OR UPDATE ON player FOR EACH ROW EXECUTE PROCEDURE set_player_league_id();


--
-- Name: player_updated; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER player_updated BEFORE UPDATE ON player FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();


--
-- Name: achievement_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY player_achievement
    ADD CONSTRAINT achievement_fkey FOREIGN KEY (achievement_id) REFERENCES const_achievement(id);


--
-- Name: event_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY game_event
    ADD CONSTRAINT event_type_fkey FOREIGN KEY (event_type_id) REFERENCES const_event_type(id);


--
-- Name: league_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY player
    ADD CONSTRAINT league_fkey FOREIGN KEY (league_id) REFERENCES const_league(id);


--
-- Name: league_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY const_league_bonus
    ADD CONSTRAINT league_fkey FOREIGN KEY (league_id) REFERENCES const_league(id);


--
-- Name: platform_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY game_session
    ADD CONSTRAINT platform_fkey FOREIGN KEY (platform_id) REFERENCES const_platform(id);


--
-- Name: player_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY game_session
    ADD CONSTRAINT player_fkey FOREIGN KEY (player_id) REFERENCES player(id);


--
-- Name: player_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY player_achievement
    ADD CONSTRAINT player_fkey FOREIGN KEY (player_id) REFERENCES player(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

