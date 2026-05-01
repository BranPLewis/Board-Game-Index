# 🎲 Board Game Index

![Board Game Index UI](BoardGameIndex.png)

**Live Demo:** [board-game-index.up.railway.app](https://board-game-index.up.railway.app)

## Overview
**Board Game Index** is a lightning-fast, cloud-hosted web application that allows you to explore, search, and filter a massive database of over 21,000 board games. 

Built with **Python**, **Streamlit**, and **PostgreSQL**, it parses an extensive BoardGameGeek dataset and normalizes it into a highly indexed relational database. This allows for instant, multi-faceted filtering across millions of data points—including mechanics, themes, player counts, ratings, and game complexity (weight).

## Features
- **Extensive Filtering**: Narrow down games by exact minimum/maximum player counts, average user rating, complexity (weight), and playtime.
- **Dynamic Tagging**: Multiselect dropdowns for **Mechanics**, **Themes**, and **Categories**. Selecting multiple tags acts as an `AND` filter (e.g., finding games that are *both* "Cooperative" and "Deck Building").
- **Live Search**: Text-based search to instantly find a game by its title.
- **Performance**: Powered by a cloud PostgreSQL database with custom indexes, allowing instantaneous queries across a dataset containing over 19 million user ratings.
- **Responsive UI**: A clean, single-page dashboard built with Streamlit that requires no scrolling to view the data.

## Example Use Cases

Here are a few ways you can use the filters to find the perfect game:

* **Heavy Strategy Night**
  * *Filters*: `Min Players: 4`, `Game Weight: 3.5 - 5.0`, `Mechanics: Worker Placement`
  * *Result*: Finds deep, complex games that accommodate your whole group.
  
* **Quick Family Fun**
  * *Filters*: `Max Playtime: 45`, `Game Weight: 1.0 - 2.0`, `Categories: Family Game`
  * *Result*: Light, fast-paced games perfect for playing with kids or casual gamers.
  
* **Highly Rated 2-Player Duel**
  * *Filters*: `Min Players: 2`, `Max Players: 2`, `Avg Rating: 8.0 - 10.0`
  * *Result*: The absolute best games specifically designed for exactly two players.
