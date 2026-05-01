-- BoardGameGeek relational schema (normalized for classifier filtering)
-- Target: PostgreSQL 14+

BEGIN;

CREATE TABLE IF NOT EXISTS games (
  bgg_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  year_published INTEGER,
  game_weight NUMERIC(8,4),
  avg_rating NUMERIC(8,5),
  bayes_avg_rating NUMERIC(8,5),
  std_dev NUMERIC(8,5),
  min_players INTEGER,
  max_players INTEGER,
  com_age_rec NUMERIC(8,3),
  language_ease NUMERIC(8,3),
  best_players INTEGER,
  good_players_text TEXT,
  num_owned INTEGER,
  num_want INTEGER,
  num_wish INTEGER,
  num_weight_votes INTEGER,
  mfg_playtime INTEGER,
  com_min_playtime INTEGER,
  com_max_playtime INTEGER,
  mfg_age_rec INTEGER,
  num_user_ratings INTEGER,
  num_comments INTEGER,
  num_alternates INTEGER,
  num_expansions INTEGER,
  num_implementations INTEGER,
  is_reimplementation BOOLEAN NOT NULL DEFAULT FALSE,
  family TEXT,
  kickstarted BOOLEAN NOT NULL DEFAULT FALSE,
  image_path TEXT,
  rank_boardgame INTEGER,
  rank_strategygames INTEGER,
  rank_abstracts INTEGER,
  rank_familygames INTEGER,
  rank_thematic INTEGER,
  rank_cgs INTEGER,
  rank_wargames INTEGER,
  rank_partygames INTEGER,
  rank_childrensgames INTEGER,
  cat_thematic BOOLEAN,
  cat_strategy BOOLEAN,
  cat_war BOOLEAN,
  cat_family BOOLEAN,
  cat_cgs BOOLEAN,
  cat_abstract BOOLEAN,
  cat_party BOOLEAN,
  cat_childrens BOOLEAN
);

CREATE TABLE IF NOT EXISTS mechanics (
  mechanic_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS themes (
  theme_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS subcategories (
  subcategory_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS artists (
  artist_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS designers (
  designer_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS publishers (
  publisher_id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS game_reduced_credit_flags (
  bgg_id INTEGER PRIMARY KEY REFERENCES games (bgg_id) ON DELETE CASCADE,
  has_low_exp_artist BOOLEAN NOT NULL DEFAULT FALSE,
  has_low_exp_designer BOOLEAN NOT NULL DEFAULT FALSE,
  has_low_exp_publisher BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS game_mechanics (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  mechanic_id BIGINT NOT NULL REFERENCES mechanics (mechanic_id) ON DELETE CASCADE,
  PRIMARY KEY (bgg_id, mechanic_id)
);

CREATE TABLE IF NOT EXISTS game_themes (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  theme_id BIGINT NOT NULL REFERENCES themes (theme_id) ON DELETE CASCADE,
  PRIMARY KEY (bgg_id, theme_id)
);

CREATE TABLE IF NOT EXISTS game_subcategories (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  subcategory_id BIGINT NOT NULL REFERENCES subcategories (subcategory_id) ON DELETE CASCADE,
  PRIMARY KEY (bgg_id, subcategory_id)
);

CREATE TABLE IF NOT EXISTS game_artists (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  artist_id BIGINT NOT NULL REFERENCES artists (artist_id) ON DELETE CASCADE,
  PRIMARY KEY (bgg_id, artist_id)
);

CREATE TABLE IF NOT EXISTS game_designers (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  designer_id BIGINT NOT NULL REFERENCES designers (designer_id) ON DELETE CASCADE,
  PRIMARY KEY (bgg_id, designer_id)
);

CREATE TABLE IF NOT EXISTS game_publishers (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  publisher_id BIGINT NOT NULL REFERENCES publishers (publisher_id) ON DELETE CASCADE,
  PRIMARY KEY (bgg_id, publisher_id)
);

CREATE TABLE IF NOT EXISTS ratings_distribution (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  rating_bucket NUMERIC(3,1) NOT NULL,
  rating_count INTEGER NOT NULL,
  PRIMARY KEY (bgg_id, rating_bucket),
  CHECK (rating_bucket >= 0.0 AND rating_bucket <= 10.0),
  CHECK (rating_count >= 0)
);

CREATE TABLE IF NOT EXISTS user_ratings (
  bgg_id INTEGER NOT NULL REFERENCES games (bgg_id) ON DELETE CASCADE,
  username TEXT NOT NULL,
  rating NUMERIC(3,1) NOT NULL,
  CHECK (rating >= 0.0 AND rating <= 10.0)
);

COMMIT;
