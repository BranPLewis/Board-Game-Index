# Board Game Index: Database Tables & Row Counts

| Table Name | Description | Row Count |
| :--- | :--- | :--- |
| **`user_ratings`** | Every individual user's rating for every game | 18,942,054 |
| **`ratings_distribution`** | Breakdown of rating buckets (1s, 2s, 3s) per game | 485,707 |
| **`game_mechanics`** | Many-to-many mapping: Games to Mechanics | 68,080 |
| **`game_publishers`** | Many-to-many mapping: Games to Publishers | 51,846 |
| **`game_themes`** | Many-to-many mapping: Games to Themes | 32,379 |
| **`games`** | Core table: All board game metadata | 21,925 |
| **`game_artists`** | Many-to-many mapping: Games to Artists | 19,180 |
| **`game_designers`** | Many-to-many mapping: Games to Designers | 18,389 |
| **`game_reduced_credit_flags`** | Tracks games with obscure/low-experience creators | 12,595 |
| **`game_subcategories`** | Many-to-many mapping: Games to Subcategories | 11,810 |
| **`publishers`** | Dimension table: Unique publisher names | 1,865 |
| **`artists`** | Dimension table: Unique artist names | 1,680 |
| **`designers`** | Dimension table: Unique designer names | 1,593 |
| **`themes`** | Dimension table: Unique theme tags | 217 |
| **`mechanics`** | Dimension table: Unique mechanic tags | 157 |
| **`subcategories`** | Dimension table: Unique subcategory tags | 10 |

---
*Total Rows Across All Tables: ~19,669,487*