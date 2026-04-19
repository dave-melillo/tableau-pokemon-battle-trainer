# Lesson 05: Joins + Advanced Visualizations

**Day:** 1  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/05_joins_advanced_instructor.twbx`  
**Student answer key:** `student/workbooks/05_joins_advanced_student.twbx`  
**Student blank:** `student/workbooks_blank/05_joins_advanced_blank.twbx`  
**Dataset(s):** `battle_participant.csv` (alias `battle_participant`), `pokemon.csv` (alias `pokemon`), `trainer.csv` (alias `trainer`)

**Joins configured in the workbook:**
- `battle_participant.pokemonid = pokemon.pokedex_number` (left join)
- `battle_participant.trainer_id = trainer.trainer_id` (left join)

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Avg Power by Pokemon Type`
- **Mark:** `Bar`
- **Rows:** `Avg([adjusted_power])`
- **Columns:** `[pokemon_type1]`
- **Color:** `[Legendary Label]`
- **Calc fields used:**
  - `Legendary Label` = `IIF([pokemon_is_legendary]=1, "Legendary", "Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Win Rate by Trainer Class`
- **Mark:** `Bar`
- **Rows:** `Avg([is_winner])`
- **Columns:** `[trainer_trainer_class]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Experience Tier Performance`
- **Mark:** `Bar`
- **Rows:** `Avg([is_winner])`
- **Columns:** `[trainer_experience_tier]`
- **Color:** `[Gym Leader Label]`
- **Calc fields used:**
  - `Gym Leader Label` = `IIF([trainer_is_gym_leader]=1, "Gym Leader", "Regular")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Region x Type Heat Map`
- **Mark:** `Square`
- **Rows:** `[pokemon_type1]`
- **Columns:** `[trainer_home_region]`
- **Color:** `Count([battle_participant_id])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Legendary MVP Rate`
- **Mark:** `Bar`
- **Rows:** `Avg([is_mvp_flag])`
- **Columns:** `[Legendary Label]`
- **Calc fields used:**
  - `Legendary Label` = `IIF([pokemon_is_legendary]=1, "Legendary", "Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Gym Leader Win Rate by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([is_winner])`
- **Columns:** `[pokemon_type1]`
- **Color:** `[Gym Leader Label]`
- **Calc fields used:**
  - `Gym Leader Label` = `IIF([trainer_is_gym_leader]=1, "Gym Leader", "Regular")`
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

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/05_joins_advanced_blank.twbx`
2. Reproduce each of the 6 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/05_joins_advanced_student.twbx`
4. Save your work as `<lesson>_<your_initials>.twbx`

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
