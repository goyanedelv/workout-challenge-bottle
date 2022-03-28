DROP TABLE IF EXISTS challenge;
DROP TABLE IF EXISTS challenge_rules;
DROP TABLE IF EXISTS rule;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS photoworkout;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_teams;
DROP TABLE IF EXISTS challenge_teams;
DROP TABLE IF EXISTS challenge_photoworkouts;
DROP TABLE IF EXISTS photoworkouts_exercise;
DROP TABLE IF EXISTS photoworkouts_user;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS log_table;


CREATE TABLE challenge (
    challenge_id integer NOT NULL,
    creation_date text,
    updated_date text,
    starting_time text,
    ending_time text,
    challenge_name character,
    challenge_handle character,
    challenge_image text,
    prize_text text,
    number_of_teams smallint,
    PRIMARY KEY (challenge_id)
);

CREATE TABLE challenge_rules (
    challenge_id smallint NOT NULL,
    rule_id smallint NOT NULL,
    FOREIGN KEY (challenge_id) REFERENCES challenge(challenge_id),
    FOREIGN KEY (rule_id) REFERENCES rule(rule_id)
);

CREATE TABLE rule (
    rule_id smallint NOT NULL,
    user_removal smallint,
    new_user smallint,
    workout_per_day smallint,
    penalty text,
    workout_criteria text,
    PRIMARY KEY (rule_id)
);

CREATE TABLE admin (
    challenge_id smallint NOT NULL,
    user_id smallint NOT NULL,
    FOREIGN KEY (challenge_id) REFERENCES challenge(challenge_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE team (
    team_id smallint NOT NULL,
    creation_date text,
    updated_date text,
    team_name character,
    team_picture_locator text,
    PRIMARY KEY (team_id)
);

CREATE TABLE photoworkout (
    photoworkout_id smallint NOT NULL,
    creation_date text,
    updated_date text,
    caption text,
    likes_count smallint,
    photo_locator text,
    PRIMARY KEY (photoworkout_id)
);

CREATE TABLE user (
    user_id smallint NOT NULL,
    creation_date text,
    updated_date text,
    email character,
    digest character,
    premium smallint,
    profile_picture_locator text,
    bio text,
    user_handle character,
    display_name character,
    PRIMARY KEY (user_id), UNIQUE(email)
);

CREATE TABLE user_teams (
    team_id smallint NOT NULL,
    user_id smallint NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE challenge_teams (
    team_id smallint NOT NULL,
    challenge_id smallint NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (challenge_id) REFERENCES challenge(challenge_id)
);

CREATE TABLE challenge_photoworkouts (
    photoworkout_id smallint NOT NULL,
    challenge_id smallint NOT NULL,
    FOREIGN KEY (photoworkout_id) REFERENCES photoworkout(photoworkout_id),
    FOREIGN KEY (challenge_id) REFERENCES challenge(challenge_id)
);

CREATE TABLE photoworkouts_exercise (
    photoworkout_id smallint NOT NULL,
    exercise_id smallint NOT NULL,
    FOREIGN KEY (photoworkout_id) REFERENCES photoworkout(photoworkout_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
);

CREATE TABLE exercise (
    exercise_id smallint NOT NULL,
    exercise_name character,
    PRIMARY KEY (exercise_id)
);

CREATE TABLE photoworkouts_user (
    photoworkout_id smallint NOT NULL,
    user_id smallint NOT NULL,
    FOREIGN KEY (photoworkout_id) REFERENCES photoworkout(photoworkout_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE log_table (
    log_entry text
);

