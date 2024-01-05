CREATE TABLE "user" (
  id UUID PRIMARY KEY,
  login VARCHAR(255) UNIQUE,
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  middle_name VARCHAR(255),
  phone_number VARCHAR(255) UNIQUE,
  register_date timestamp,
  birthday DATE,
  country VARCHAR(255),
  region VARCHAR(255),
  city VARCHAR(255)
);

CREATE TABLE "boxer" (
  id UUID PRIMARY KEY,
  weight float,
  height float,
  athletic_distinction VARCHAR(255),
  user_id UUID,
  club_id UUID
);

CREATE TABLE "coach" (
  id UUID PRIMARY KEY,
  user_id UUID
);

CREATE TABLE "judge" (
  id UUID PRIMARY KEY,
  user_id UUID,
  judical_rank VARCHAR(255)
);

CREATE TABLE "organizer" (
  id UUID PRIMARY KEY,
  user_id UUID
);

CREATE TABLE "club" (
  id UUID PRIMARY KEY,
  coach_id UUID
);

CREATE TABLE "competition" (
  id UUID PRIMARY KEY,
  competition_name VARCHAR(255),
  organizer_id UUID
);

CREATE TABLE "fight" (
  id UUID PRIMARY KEY,
  competition_id UUID,
  fight_date timestamp,
  winner_id UUID
);

CREATE TABLE "fighter" (
  id UUID PRIMARY KEY,
  fighter_id UUID,
  fight_id UUID
);

CREATE TABLE "competition_boxer" (
  id UUID PRIMARY KEY,
  boxer_id UUID,
  competition_id UUID
);

CREATE TABLE "judge_fight" (
  id UUID PRIMARY KEY,
  judge_id UUID,
  fight_id UUID
);

CREATE TABLE score (
  id UUID PRIMARY KEY,
  fighter_id UUID,
  score_value int,
  judge_id UUID
);

ALTER TABLE "boxer" ADD FOREIGN KEY (user_id) REFERENCES "user" (id);

ALTER TABLE "coach" ADD FOREIGN KEY (user_id) REFERENCES "user" (id);

ALTER TABLE "judge" ADD FOREIGN KEY (user_id) REFERENCES "user" (id);

ALTER TABLE "organizer" ADD FOREIGN KEY (user_id) REFERENCES "user" (id);

ALTER TABLE "club" ADD FOREIGN KEY (coach_id) REFERENCES "coach" (id);

ALTER TABLE "boxer" ADD FOREIGN KEY (club_id) REFERENCES "club" (id);

ALTER TABLE "fight" ADD FOREIGN KEY (competition_id) REFERENCES "competition" (id);

ALTER TABLE "fighter" ADD FOREIGN KEY (fighter_id) REFERENCES "boxer" (id);

ALTER TABLE "competition_boxer" ADD FOREIGN KEY (competition_id) REFERENCES "competition" (id);

ALTER TABLE "competition_boxer" ADD FOREIGN KEY (boxer_id) REFERENCES "boxer" (id);

ALTER TABLE "judge_fight" ADD FOREIGN KEY (judge_id) REFERENCES "judge" (id);

ALTER TABLE "judge_fight" ADD FOREIGN KEY (fight_id) REFERENCES "fight" (id);

ALTER TABLE "fighter" ADD FOREIGN KEY (fight_id) REFERENCES "fight" (id);

ALTER TABLE "score" ADD FOREIGN KEY (judge_id) REFERENCES "judge" (id);

ALTER TABLE "competition" ADD FOREIGN KEY (organizer_id) REFERENCES "organizer" (id);

ALTER TABLE "score" ADD FOREIGN KEY (fighter_id) REFERENCES "fighter" (id);

ALTER TABLE "fight" ADD FOREIGN KEY (winner_id) REFERENCES "boxer" (id);
