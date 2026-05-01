-- Indexes for BoardGameGeek Database
-- Focuses on fast filtering by ratings, attributes, and reverse lookups for dimensions

BEGIN;

-- 1. User Ratings (19 million rows)
-- Essential for finding all ratings for a game, all ratings by a user, or filtering by rating value
CREATE INDEX IF NOT EXISTS idx_user_ratings_bgg_id ON user_ratings (bgg_id);
CREATE INDEX IF NOT EXISTS idx_user_ratings_username ON user_ratings (username);
CREATE INDEX IF NOT EXISTS idx_user_ratings_rating ON user_ratings (rating DESC);

-- 2. Games Table - Ratings and Popularity Filters
-- Useful for sorting and filtering top games
CREATE INDEX IF NOT EXISTS idx_games_avg_rating ON games (avg_rating DESC);
CREATE INDEX IF NOT EXISTS idx_games_bayes_avg_rating ON games (bayes_avg_rating DESC);
CREATE INDEX IF NOT EXISTS idx_games_num_user_ratings ON games (num_user_ratings DESC);

-- 3. Games Table - Common Gameplay Filters
CREATE INDEX IF NOT EXISTS idx_games_year_published ON games (year_published DESC);
CREATE INDEX IF NOT EXISTS idx_games_game_weight ON games (game_weight);
CREATE INDEX IF NOT EXISTS idx_games_min_players ON games (min_players);
CREATE INDEX IF NOT EXISTS idx_games_max_players ON games (max_players);
CREATE INDEX IF NOT EXISTS idx_games_mfg_playtime ON games (mfg_playtime);

-- 4. Reverse Lookup Indexes for Dimension Join Tables
-- The Primary Key covers (bgg_id, dimension_id) which is fast for finding a game's dimensions.
-- We need these indexes to quickly find all games that share a specific dimension (e.g., all games with "Auction" mechanic)
CREATE INDEX IF NOT EXISTS idx_game_mechanics_mechanic_id ON game_mechanics (mechanic_id);
CREATE INDEX IF NOT EXISTS idx_game_themes_theme_id ON game_themes (theme_id);
CREATE INDEX IF NOT EXISTS idx_game_subcategories_subcategory_id ON game_subcategories (subcategory_id);
CREATE INDEX IF NOT EXISTS idx_game_artists_artist_id ON game_artists (artist_id);
CREATE INDEX IF NOT EXISTS idx_game_designers_designer_id ON game_designers (designer_id);
CREATE INDEX IF NOT EXISTS idx_game_publishers_publisher_id ON game_publishers (publisher_id);

COMMIT;