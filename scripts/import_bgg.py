#!/usr/bin/env python3
"""Import BoardGameGeek CSV extracts into PostgreSQL.

Usage example:
  python scripts/import_bgg.py \
    --dsn "postgresql://user:pass@localhost:5432/bgg" \
    --data-dir "/Users/risky/CS-4307/BGG/board-games-database-from-boardgamegeek/versions/4" \
    --include-user-ratings
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

import psycopg


def to_int(value: str) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return int(float(value))


def to_float(value: str) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return float(value)


def to_bool01(value: str) -> bool:
    return str(value).strip() == "1"


def batched_insert(
    cur: psycopg.Cursor, sql_text: str, rows: list[tuple], batch_size: int = 2000
) -> None:
    if not rows:
        return
    for idx in range(0, len(rows), batch_size):
        cur.executemany(sql_text, rows[idx : idx + batch_size])


def iter_games(game_csv: Path) -> Iterable[tuple]:
    with game_csv.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield (
                to_int(row["BGGId"]),
                row["Name"].strip(),
                row["Description"] or None,
                to_int(row["YearPublished"]),
                to_float(row["GameWeight"]),
                to_float(row["AvgRating"]),
                to_float(row["BayesAvgRating"]),
                to_float(row["StdDev"]),
                to_int(row["MinPlayers"]),
                to_int(row["MaxPlayers"]),
                to_float(row["ComAgeRec"]),
                to_float(row["LanguageEase"]),
                to_int(row["BestPlayers"]),
                row["GoodPlayers"] or None,
                to_int(row["NumOwned"]),
                to_int(row["NumWant"]),
                to_int(row["NumWish"]),
                to_int(row["NumWeightVotes"]),
                to_int(row["MfgPlaytime"]),
                to_int(row["ComMinPlaytime"]),
                to_int(row["ComMaxPlaytime"]),
                to_int(row["MfgAgeRec"]),
                to_int(row["NumUserRatings"]),
                to_int(row["NumComments"]),
                to_int(row["NumAlternates"]),
                to_int(row["NumExpansions"]),
                to_int(row["NumImplementations"]),
                to_bool01(row["IsReimplementation"]),
                row["Family"] or None,
                to_bool01(row["Kickstarted"]),
                row["ImagePath"] or None,
                to_int(row["Rank:boardgame"]),
                to_int(row["Rank:strategygames"]),
                to_int(row["Rank:abstracts"]),
                to_int(row["Rank:familygames"]),
                to_int(row["Rank:thematic"]),
                to_int(row["Rank:cgs"]),
                to_int(row["Rank:wargames"]),
                to_int(row["Rank:partygames"]),
                to_int(row["Rank:childrensgames"]),
                to_bool01(row["Cat:Thematic"]),
                to_bool01(row["Cat:Strategy"]),
                to_bool01(row["Cat:War"]),
                to_bool01(row["Cat:Family"]),
                to_bool01(row["Cat:CGS"]),
                to_bool01(row["Cat:Abstract"]),
                to_bool01(row["Cat:Party"]),
                to_bool01(row["Cat:Childrens"]),
            )


def load_games(conn: psycopg.Connection, game_csv: Path) -> list[int]:
    sql_text = """
    INSERT INTO games (
      bgg_id, name, description, year_published, game_weight, avg_rating,
      bayes_avg_rating, std_dev, min_players, max_players, com_age_rec,
      language_ease, best_players, good_players_text, num_owned, num_want,
      num_wish, num_weight_votes, mfg_playtime, com_min_playtime,
      com_max_playtime, mfg_age_rec, num_user_ratings, num_comments,
      num_alternates, num_expansions, num_implementations, is_reimplementation,
      family, kickstarted, image_path, rank_boardgame, rank_strategygames,
      rank_abstracts, rank_familygames, rank_thematic, rank_cgs, rank_wargames,
      rank_partygames, rank_childrensgames, cat_thematic, cat_strategy, cat_war,
      cat_family, cat_cgs, cat_abstract, cat_party, cat_childrens
    ) VALUES (
      %s, %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s,
      %s, %s, %s, %s,
      %s, %s, %s, %s,
      %s, %s, %s, %s,
      %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s
    )
    ON CONFLICT (bgg_id) DO UPDATE SET
      name = EXCLUDED.name,
      description = EXCLUDED.description,
      year_published = EXCLUDED.year_published,
      game_weight = EXCLUDED.game_weight,
      avg_rating = EXCLUDED.avg_rating,
      bayes_avg_rating = EXCLUDED.bayes_avg_rating,
      std_dev = EXCLUDED.std_dev,
      min_players = EXCLUDED.min_players,
      max_players = EXCLUDED.max_players,
      com_age_rec = EXCLUDED.com_age_rec,
      language_ease = EXCLUDED.language_ease,
      best_players = EXCLUDED.best_players,
      good_players_text = EXCLUDED.good_players_text,
      num_owned = EXCLUDED.num_owned,
      num_want = EXCLUDED.num_want,
      num_wish = EXCLUDED.num_wish,
      num_weight_votes = EXCLUDED.num_weight_votes,
      mfg_playtime = EXCLUDED.mfg_playtime,
      com_min_playtime = EXCLUDED.com_min_playtime,
      com_max_playtime = EXCLUDED.com_max_playtime,
      mfg_age_rec = EXCLUDED.mfg_age_rec,
      num_user_ratings = EXCLUDED.num_user_ratings,
      num_comments = EXCLUDED.num_comments,
      num_alternates = EXCLUDED.num_alternates,
      num_expansions = EXCLUDED.num_expansions,
      num_implementations = EXCLUDED.num_implementations,
      is_reimplementation = EXCLUDED.is_reimplementation,
      family = EXCLUDED.family,
      kickstarted = EXCLUDED.kickstarted,
      image_path = EXCLUDED.image_path,
      rank_boardgame = EXCLUDED.rank_boardgame,
      rank_strategygames = EXCLUDED.rank_strategygames,
      rank_abstracts = EXCLUDED.rank_abstracts,
      rank_familygames = EXCLUDED.rank_familygames,
      rank_thematic = EXCLUDED.rank_thematic,
      rank_cgs = EXCLUDED.rank_cgs,
      rank_wargames = EXCLUDED.rank_wargames,
      rank_partygames = EXCLUDED.rank_partygames,
      rank_childrensgames = EXCLUDED.rank_childrensgames,
      cat_thematic = EXCLUDED.cat_thematic,
      cat_strategy = EXCLUDED.cat_strategy,
      cat_war = EXCLUDED.cat_war,
      cat_family = EXCLUDED.cat_family,
      cat_cgs = EXCLUDED.cat_cgs,
      cat_abstract = EXCLUDED.cat_abstract,
      cat_party = EXCLUDED.cat_party,
      cat_childrens = EXCLUDED.cat_childrens
    """

    bgg_ids: list[int] = []
    batch: list[tuple] = []
    with conn.cursor() as cur:
        for game in iter_games(game_csv):
            bgg_ids.append(game[0])
            batch.append(game)
            if len(batch) >= 1000:
                batched_insert(cur, sql_text, batch)
                batch.clear()
        batched_insert(cur, sql_text, batch)
    conn.commit()
    return bgg_ids


def ensure_dimension_names(
    conn: psycopg.Connection, table_name: str, names: list[str]
) -> dict[str, int]:
    insert_sql = (
        f"INSERT INTO {table_name} (name) VALUES (%s) ON CONFLICT (name) DO NOTHING"
    )
    # Hack to handle plural names cleanly
    id_col = table_name[:-1] + "_id"
    if table_name == "subcategories":
        id_col = "subcategory_id"
    
    select_sql = f"SELECT name, {id_col} FROM {table_name}"

    with conn.cursor() as cur:
        cur.executemany(insert_sql, [(name,) for name in names])
        cur.execute(select_sql)
        rows = cur.fetchall()
    conn.commit()
    return {name: item_id for (name, item_id) in rows}


def load_binary_matrix(
    conn: psycopg.Connection,
    csv_path: Path,
    dim_table: str,
    join_table: str,
    join_dim_fk: str,
    ordered_bgg_ids: list[int],
    reduced_flag_column: str | None = None,
) -> None:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        explicit_bgg_id = header[0].strip().lower() == "bggid"
        names = header[1:] if explicit_bgg_id else header

        low_exp_positions = {
            idx for idx, value in enumerate(names) if "low-exp" in value.lower()
        }
        classifier_names = [
            name for idx, name in enumerate(names) if idx not in low_exp_positions
        ]
        dim_map = ensure_dimension_names(conn, dim_table, classifier_names)

        insert_join_sql = (
            f"INSERT INTO {join_table} (bgg_id, {join_dim_fk}) VALUES (%s, %s) "
            f"ON CONFLICT (bgg_id, {join_dim_fk}) DO NOTHING"
        )
        join_rows: list[tuple[int, int]] = []

        flag_rows: list[tuple[int, bool, bool, bool]] = []

        for idx, row in enumerate(reader):
            if explicit_bgg_id:
                bgg_id = int(row[0])
                values = row[1:]
            else:
                bgg_id = ordered_bgg_ids[idx]
                values = row

            for pos, raw_value in enumerate(values):
                if raw_value != "1":
                    continue
                if pos in low_exp_positions:
                    if reduced_flag_column == "has_low_exp_artist":
                        flag_rows.append((bgg_id, True, False, False))
                    elif reduced_flag_column == "has_low_exp_designer":
                        flag_rows.append((bgg_id, False, True, False))
                    elif reduced_flag_column == "has_low_exp_publisher":
                        flag_rows.append((bgg_id, False, False, True))
                    continue

                name = names[pos]
                join_rows.append((bgg_id, dim_map[name]))
                if len(join_rows) >= 10000:
                    with conn.cursor() as cur:
                        batched_insert(cur, insert_join_sql, join_rows, batch_size=5000)
                    conn.commit()
                    join_rows.clear()

        if join_rows:
            with conn.cursor() as cur:
                batched_insert(cur, insert_join_sql, join_rows, batch_size=5000)
            conn.commit()

        if flag_rows:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO game_reduced_credit_flags (
                      bgg_id,
                      has_low_exp_artist,
                      has_low_exp_designer,
                      has_low_exp_publisher
                    ) VALUES (%s, %s, %s, %s)
                    ON CONFLICT (bgg_id) DO UPDATE SET
                      has_low_exp_artist = game_reduced_credit_flags.has_low_exp_artist OR EXCLUDED.has_low_exp_artist,
                      has_low_exp_designer = game_reduced_credit_flags.has_low_exp_designer OR EXCLUDED.has_low_exp_designer,
                      has_low_exp_publisher = game_reduced_credit_flags.has_low_exp_publisher OR EXCLUDED.has_low_exp_publisher
                    """,
                    flag_rows,
                )
            conn.commit()


def load_ratings_distribution(conn: psycopg.Connection, distribution_csv: Path) -> None:
    with distribution_csv.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        buckets = [float(item) for item in header[1:-1]]

        sql_text = """
        INSERT INTO ratings_distribution (bgg_id, rating_bucket, rating_count)
        VALUES (%s, %s, %s)
        ON CONFLICT (bgg_id, rating_bucket) DO UPDATE
          SET rating_count = EXCLUDED.rating_count
        """

        rows: list[tuple[int, float, int]] = []
        for row in reader:
            bgg_id = int(row[0])
            for idx, bucket in enumerate(buckets, start=1):
                count = int(float(row[idx]))
                if count == 0:
                    continue
                rows.append((bgg_id, bucket, count))
            if len(rows) >= 25000:
                with conn.cursor() as cur:
                    batched_insert(cur, sql_text, rows, batch_size=5000)
                conn.commit()
                rows.clear()

        if rows:
            with conn.cursor() as cur:
                batched_insert(cur, sql_text, rows, batch_size=5000)
            conn.commit()


def load_user_ratings_copy(conn: psycopg.Connection, user_ratings_csv: Path) -> None:
    with conn.cursor() as cur:
        with user_ratings_csv.open("r", encoding="utf-8") as f:
            with cur.copy(
                "COPY user_ratings (bgg_id, rating, username) FROM STDIN WITH (FORMAT csv, HEADER true)"
            ) as copy:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    copy.write(chunk)
    conn.commit()


def truncate_all(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            TRUNCATE TABLE
              user_ratings,
              ratings_distribution,
              game_publishers,
              game_designers,
              game_artists,
              game_subcategories,
              game_themes,
              game_mechanics,
              publishers,
              designers,
              artists,
              subcategories,
              themes,
              mechanics,
              game_reduced_credit_flags,
              games
            RESTART IDENTITY CASCADE
            """
        )
    conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import BoardGameGeek CSV data into PostgreSQL"
    )
    parser.add_argument(
        "--dsn",
        required=True,
        help="PostgreSQL DSN, e.g. postgresql://user:pass@localhost:5432/bgg",
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Path to versions/4 directory containing CSV files",
    )
    parser.add_argument(
        "--include-user-ratings",
        action="store_true",
        help="Also import user_ratings.csv (~19M rows)",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Truncate all target tables before import",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    games_csv = data_dir / "games.csv"
    mechanics_csv = data_dir / "mechanics.csv"
    themes_csv = data_dir / "themes.csv"
    subcategories_csv = data_dir / "subcategories.csv"
    artists_csv = data_dir / "artists_reduced.csv"
    designers_csv = data_dir / "designers_reduced.csv"
    publishers_csv = data_dir / "publishers_reduced.csv"
    ratings_distribution_csv = data_dir / "ratings_distribution.csv"
    user_ratings_csv = data_dir / "user_ratings.csv"

    with psycopg.connect(args.dsn) as conn:
        if args.truncate:
            print("Truncating existing data...")
            truncate_all(conn)

        print("Loading games...")
        ordered_bgg_ids = load_games(conn, games_csv)

        print("Loading mechanics...")
        load_binary_matrix(
            conn,
            mechanics_csv,
            dim_table="mechanics",
            join_table="game_mechanics",
            join_dim_fk="mechanic_id",
            ordered_bgg_ids=ordered_bgg_ids,
        )

        print("Loading themes...")
        load_binary_matrix(
            conn,
            themes_csv,
            dim_table="themes",
            join_table="game_themes",
            join_dim_fk="theme_id",
            ordered_bgg_ids=ordered_bgg_ids,
        )

        print("Loading subcategories...")
        load_binary_matrix(
            conn,
            subcategories_csv,
            dim_table="subcategories",
            join_table="game_subcategories",
            join_dim_fk="subcategory_id",
            ordered_bgg_ids=ordered_bgg_ids,
        )

        print("Loading artists...")
        load_binary_matrix(
            conn,
            artists_csv,
            dim_table="artists",
            join_table="game_artists",
            join_dim_fk="artist_id",
            ordered_bgg_ids=ordered_bgg_ids,
            reduced_flag_column="has_low_exp_artist",
        )

        print("Loading designers...")
        load_binary_matrix(
            conn,
            designers_csv,
            dim_table="designers",
            join_table="game_designers",
            join_dim_fk="designer_id",
            ordered_bgg_ids=ordered_bgg_ids,
            reduced_flag_column="has_low_exp_designer",
        )

        print("Loading publishers...")
        load_binary_matrix(
            conn,
            publishers_csv,
            dim_table="publishers",
            join_table="game_publishers",
            join_dim_fk="publisher_id",
            ordered_bgg_ids=ordered_bgg_ids,
            reduced_flag_column="has_low_exp_publisher",
        )

        print("Loading ratings distribution...")
        load_ratings_distribution(conn, ratings_distribution_csv)

        if args.include_user_ratings:
            print("Loading user ratings (large table)...")
            load_user_ratings_copy(conn, user_ratings_csv)

    print("Import complete.")


if __name__ == "__main__":
    main()
