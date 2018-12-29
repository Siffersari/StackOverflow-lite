CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    first_name character varying(20) NOT NULL,
    last_name character varying(20) NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(30) NOT NULL,
    password character varying(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    question_id serial PRIMARY KEY NOT NULL,
    user_id numeric NOT NULL,
    title character varying(256) NOT NULL,
    description character varying(1000)
);

CREATE TABLE IF NOT EXISTS answers(
    answer_id serial PRIMARY KEY NOT NULL,
    question_id numeric NOT NULL,
    user_id numeric NOT NULL,
    answer character varying(1000),
    upvotes numeric DEFAULT 0,
    accepted boolean DEFAULT false
);