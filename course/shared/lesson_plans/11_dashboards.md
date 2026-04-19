# Lesson 11: Dashboards

**Day:** 2  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/11_dashboards_instructor.twbx`  
**Student answer key:** `student/workbooks/11_dashboards_student.twbx`  
**Student blank:** `student/workbooks_blank/11_dashboards_blank.twbx`  
**Dataset(s):** `battle_participant.csv` (alias `battle_participant`), `pokemon.csv` (alias `pokemon`), `trainer.csv` (alias `trainer`), `battles.csv` (alias `battles`), `venue.csv` (alias `venue`)

**Joins configured in the workbook:**
- `battle_participant.pokemonid = pokemon.pokedex_number` (left join)
- `battle_participant.trainer_id = trainer.trainer_id` (left join)
- `battle_participant.battle_id = battles.battle_id` (left join)
- `battles.venue_id = venue.venue_id` (left join)

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `D1 Power by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([adjusted_power])`
- **Columns:** `[pokemon_type1]`
- **Color:** `[Legendary Label]`
- **Calc fields used:**
  - `Legendary Label` = `IIF([pokemon_is_legendary]=1, "Legendary", "Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `D2 Win Rate by Experience`
- **Mark:** `Bar`
- **Rows:** `Avg([is_winner])`
- **Columns:** `[trainer_experience_tier]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `D3 Wins Over Time`
- **Mark:** `Line`
- **Rows:** `Avg([is_winner])`
- **Columns:** `Month([battles_battle_date])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `D4 Region Participation`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[venue_region]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `D5 Format Mix`
- **Mark:** `Bar`
- **Rows:** `Countd([battle_id])`
- **Columns:** `[battles_battle_format]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `D6 Type x Venue Heat Map`
- **Mark:** `Square`
- **Rows:** `[pokemon_type1]`
- **Columns:** `[venue_venue_type]`
- **Color:** `Avg([is_winner])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Legendary Label`** (string, dimension)
  ```
  IIF([pokemon_is_legendary]=1, "Legendary", "Standard")
  ```

## Dashboard

- **Name:** `Battle Insights Dashboard`
- **Size:** 1400 × 1400
- **Sheets stacked vertically (top → bottom):**
  1. `D1 Power by Type`
  2. `D2 Win Rate by Experience`
  3. `D3 Wins Over Time`
  4. `D4 Region Participation`
  5. `D5 Format Mix`
  6. `D6 Type x Venue Heat Map`

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/11_dashboards_blank.twbx`
2. Reproduce each of the 6 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/11_dashboards_student.twbx`
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
