# Lesson 13: Master Reference Workbook (Instructor Only)

**Day:** 2  
**Duration:** office hours  
**Instructor workbook:** `instructor/workbooks/13_master_reference_instructor.twbx`  
**Dataset(s):** `battle_participant.csv` (alias `battle_participant`), `pokemon.csv` (alias `pokemon`), `trainer.csv` (alias `trainer`), `battles.csv` (alias `battles`), `venue.csv` (alias `venue`)

**Joins configured in the workbook:**
- `battle_participant.pokemonid = pokemon.pokedex_number` (left join)
- `battle_participant.trainer_id = trainer.trainer_id` (left join)
- `battle_participant.battle_id = battles.battle_id` (left join)
- `battles.venue_id = venue.venue_id` (left join)

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `Q1 Best Type per Venue Type`
- **Mark:** `Square`
- **Rows:** `[pokemon_type1]`
- **Columns:** `[venue_venue_type]`
- **Color:** `Avg([Type x Venue Win Rate])`
- **Calc fields used:**
  - `Type x Venue Win Rate` = `{ FIXED [pokemon_type1], [venue_venue_type] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `Q2 Venue Map - Battle Counts`
- **Mark:** `Automatic`
- **Rows:** `Avg([venue_lat])`
- **Columns:** `Avg([venue_lon])`
- **Color:** `[venue_venue_type]`
- **Size:** `Avg([Venue Battles (FIXED)])`
- **Calc fields used:**
  - `Venue Battles (FIXED)` = `{ FIXED [battles_venue_id] : COUNTD([battle_id]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Automatic` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `Q3 Trainer Win Rate by Type`
- **Mark:** `Square`
- **Rows:** `[trainer_id]`
- **Columns:** `[pokemon_type1]`
- **Color:** `Avg([Trainer x Type Win Rate])`
- **Calc fields used:**
  - `Trainer x Type Win Rate` = `{ FIXED [trainer_id], [pokemon_type1] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `Q4 Win Rate Over Time`
- **Mark:** `Line`
- **Rows:** `Avg([is_winner])`
- **Columns:** `Month([battles_battle_date])`
- **Color:** `[trainer_experience_tier]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `Q5 Type Win Rate Over Time`
- **Mark:** `Line`
- **Rows:** `Avg([is_winner])`
- **Columns:** `Quarter([battles_battle_date])`
- **Color:** `[pokemon_type1]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `Q6 Most Successful Pokemon`
- **Mark:** `Bar`
- **Rows:** `Avg([Pokemon Win Rate (FIXED)])`
- **Columns:** `[pokemon_name]`
- **Color:** `[Legendary Label]`
- **Calc fields used:**
  - `Legendary Label` = `IIF([pokemon_is_legendary]=1, "Legendary", "Standard")`
  - `Pokemon Win Rate (FIXED)` = `{ FIXED [pokemon_name] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `Q7 Most Successful Pokemon Type`
- **Mark:** `Bar`
- **Rows:** `Avg([Pokemon Type Win Rate (FIXED)])`
- **Columns:** `[pokemon_type1]`
- **Calc fields used:**
  - `Pokemon Type Win Rate (FIXED)` = `{ FIXED [pokemon_type1] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 8. Sheet `Q8 Power Tier Mix by Type`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[pokemon_type1]`
- **Color:** `[Power Tier]`
- **Calc fields used:**
  - `Power Tier` = `IF [adjusted_power] >= 600 THEN "S-Tier"
ELSEIF [adjusted_power] >= 500 THEN "A-Tier"
ELSEIF [adjusted_power] >= 400 THEN "B-Tier"
ELSE "C-Tier"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 9. Sheet `Q9 Type Advantage Effect`
- **Mark:** `Bar`
- **Rows:** `Avg([is_winner])`
- **Columns:** `[Type Advantage Match]`
- **Calc fields used:**
  - `Type Advantage Match` = `IIF([pokemon_type1]=[venue_venue_type], "Aligned", "Not Aligned")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 10. Sheet `Q10 MVP Pokemon by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([MVP Win Rate])`
- **Columns:** `[pokemon_type1]`
- **Calc fields used:**
  - `MVP Win Rate` = `{ FIXED [pokemon_name] : AVG([is_mvp_flag]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 11. Sheet `Q11 Power Boost by Match`
- **Mark:** `Bar`
- **Rows:** `Avg([Power Boost])`
- **Columns:** `[venue_type_match_flag]`
- **Calc fields used:**
  - `Power Boost` = `[adjusted_power] - [base_power]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 12. Sheet `Q12 Region Performance`
- **Mark:** `Bar`
- **Rows:** `Avg([is_winner])`
- **Columns:** `[venue_region]`
- **Color:** `[Legendary Label]`
- **Calc fields used:**
  - `Legendary Label` = `IIF([pokemon_is_legendary]=1, "Legendary", "Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Legendary Label`** (string, dimension)
  ```
  IIF([pokemon_is_legendary]=1, "Legendary", "Standard")
  ```
- **`Gym Leader Label`** (string, dimension)
  ```
  IIF([trainer_is_gym_leader]=1, "Gym Leader", "Regular")
  ```
- **`Power Tier`** (string, dimension)
  ```
  IF [adjusted_power] >= 600 THEN "S-Tier"
ELSEIF [adjusted_power] >= 500 THEN "A-Tier"
ELSEIF [adjusted_power] >= 400 THEN "B-Tier"
ELSE "C-Tier"
END
  ```
- **`Type Advantage Match`** (string, dimension)
  ```
  IIF([pokemon_type1]=[venue_venue_type], "Aligned", "Not Aligned")
  ```
- **`Power Boost`** (real, measure)
  ```
  [adjusted_power] - [base_power]
  ```
- **`Pokemon Win Rate (FIXED)`** (real, measure)
  ```
  { FIXED [pokemon_name] : AVG([is_winner]) }
  ```
- **`Pokemon Type Win Rate (FIXED)`** (real, measure)
  ```
  { FIXED [pokemon_type1] : AVG([is_winner]) }
  ```
- **`Trainer Win Rate (FIXED)`** (real, measure)
  ```
  { FIXED [trainer_id] : AVG([is_winner]) }
  ```
- **`Type x Venue Win Rate`** (real, measure)
  ```
  { FIXED [pokemon_type1], [venue_venue_type] : AVG([is_winner]) }
  ```
- **`Trainer x Type Win Rate`** (real, measure)
  ```
  { FIXED [trainer_id], [pokemon_type1] : AVG([is_winner]) }
  ```
- **`Venue Battles (FIXED)`** (integer, measure)
  ```
  { FIXED [battles_venue_id] : COUNTD([battle_id]) }
  ```
- **`MVP Win Rate`** (real, measure)
  ```
  { FIXED [pokemon_name] : AVG([is_mvp_flag]) }
  ```

## Dashboard

- **Name:** `Pokemon Battle Universe - Apex Dashboard`
- **Size:** 1600 × 2400
- **Sheets stacked vertically (top → bottom):**
  1. `Q1 Best Type per Venue Type`
  2. `Q2 Venue Map - Battle Counts`
  3. `Q3 Trainer Win Rate by Type`
  4. `Q4 Win Rate Over Time`
  5. `Q5 Type Win Rate Over Time`
  6. `Q6 Most Successful Pokemon`
  7. `Q7 Most Successful Pokemon Type`
  8. `Q8 Power Tier Mix by Type`
  9. `Q9 Type Advantage Effect`
  10. `Q10 MVP Pokemon by Type`
  11. `Q11 Power Boost by Match`
  12. `Q12 Region Performance`

## How to use this reference (instructor-only)

- Office hours: when a student asks how to do X, find a sheet that does it and demo it live.
- Module 4–5 questions → open joined sheets that show cross-table analysis
- Module 9 questions → open the calc-fields cheat sheet above
- Module 10 questions → open `Q2 Venue Map - Battle Counts`
- Module 12 questions → open any FIXED LOD sheet (Q3, Q4, Q5, Q6, Q7)

## Common pitfalls

- Wrong aggregation (default SUM when AVG is needed)
- Date dimension on Columns as discrete vs continuous — toggle via right-click
- Confusing relationship vs join — modern Tableau uses relationships by default
- Forgetting that joined-table fields use the prefixed name (e.g. `venue_region`, not just `region`)
- Calc-field references use `[bracket_name]`, not the friendly caption
- IIF(condition, true_value, false_value) — false_value is required

## Talking points to memorize

- "Notice that we drag, never type — Tableau builds the query for us."
- "The shelf you drop a field on changes how Tableau treats it."
- "The join is configured in the data canvas. Once set, both tables' fields appear in the Data pane."
- "Every calc field is just a formula — read it left to right like math."
