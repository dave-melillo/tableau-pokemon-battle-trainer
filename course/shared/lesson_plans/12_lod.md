# Lesson 12: LOD Calculations

**Day:** 2  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/12_lod_instructor.twbx`  
**Student answer key:** `student/workbooks/12_lod_student.twbx`  
**Student blank:** `student/workbooks_blank/12_lod_blank.twbx`  
**Dataset(s):** `battle_participant.csv` (alias `battle_participant`), `pokemon.csv` (alias `pokemon`), `trainer.csv` (alias `trainer`), `battles.csv` (alias `battles`), `venue.csv` (alias `venue`)

**Joins configured in the workbook:**
- `battle_participant.pokemonid = pokemon.pokedex_number` (left join)
- `battle_participant.trainer_id = trainer.trainer_id` (left join)
- `battle_participant.battle_id = battles.battle_id` (left join)
- `battles.venue_id = venue.venue_id` (left join)

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Trainer Win Rate Distribution (L03)`
- **Mark:** `Bar`
- **Rows:** `Countd([trainer_id])`
- **Columns:** `[L03 FIXED Trainer - Win Rate]`
- **Calc fields used:**
  - `L03 FIXED Trainer - Win Rate` = `{ FIXED [trainer_id] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Trainer vs Overall (L11)`
- **Mark:** `Bar`
- **Rows:** `Avg([L11 Comparison - Trainer vs Overall])`
- **Columns:** `[trainer_experience_tier]`
- **Calc fields used:**
  - `L11 Comparison - Trainer vs Overall` = `{ FIXED [trainer_id] : AVG([adjusted_power]) } - { FIXED : AVG([adjusted_power]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Power vs Trainer Avg (L10)`
- **Mark:** `Bar`
- **Rows:** `Avg([L10 Comparison - Power vs Trainer Avg])`
- **Columns:** `[slot_number]`
- **Color:** `[team_side]`
- **Calc fields used:**
  - `L10 Comparison - Power vs Trainer Avg` = `[adjusted_power] - { FIXED [trainer_id] : AVG([adjusted_power]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Pokemon Win Rate (L04)`
- **Mark:** `Bar`
- **Rows:** `Avg([L04 FIXED Pokemon - Win Rate])`
- **Columns:** `[pokemon_type1]`
- **Calc fields used:**
  - `L04 FIXED Pokemon - Win Rate` = `{ FIXED [pokemonid] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Type x Venue Win Rate (L07)`
- **Mark:** `Square`
- **Rows:** `[pokemon_type1]`
- **Columns:** `[venue_venue_type]`
- **Color:** `Avg([L07 FIXED VType - Type Win Rate])`
- **Calc fields used:**
  - `L07 FIXED VType - Type Win Rate` = `{ FIXED [venue_venue_type], [pokemon_type1] : AVG([is_winner]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 % of Total Power (L13)`
- **Mark:** `Bar`
- **Rows:** `[L13 % of Total via FIXED]`
- **Columns:** `[team_side]`
- **Calc fields used:**
  - `L13 % of Total via FIXED` = `SUM([adjusted_power]) / { FIXED : SUM([adjusted_power]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `07 Battles per Venue (L05)`
- **Mark:** `Bar`
- **Rows:** `Avg([L05 FIXED Venue - Battles])`
- **Columns:** `[battles_venue_id]`
- **Calc fields used:**
  - `L05 FIXED Venue - Battles` = `{ FIXED [battles_venue_id] : COUNTD([battle_id]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 8. Sheet `08 Battles per Trainer (L14)`
- **Mark:** `Bar`
- **Rows:** `Avg([L14 Trainer Battle Count (FIXED)])`
- **Columns:** `[trainer_experience_tier]`
- **Calc fields used:**
  - `L14 Trainer Battle Count (FIXED)` = `{ FIXED [trainer_id] : COUNTD([battle_id]) }`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`L01 FIXED - Overall Avg Power`** (real, measure)
  ```
  { FIXED : AVG([adjusted_power]) }
  ```
- **`L02 FIXED Trainer - Avg Power`** (real, measure)
  ```
  { FIXED [trainer_id] : AVG([adjusted_power]) }
  ```
- **`L03 FIXED Trainer - Win Rate`** (real, measure)
  ```
  { FIXED [trainer_id] : AVG([is_winner]) }
  ```
- **`L04 FIXED Pokemon - Win Rate`** (real, measure)
  ```
  { FIXED [pokemonid] : AVG([is_winner]) }
  ```
- **`L05 FIXED Venue - Battles`** (integer, measure)
  ```
  { FIXED [battles_venue_id] : COUNTD([battle_id]) }
  ```
- **`L06 FIXED Trainer+Type - Win Rate`** (real, measure)
  ```
  { FIXED [trainer_id], [pokemon_type1] : AVG([is_winner]) }
  ```
- **`L07 FIXED VType - Type Win Rate`** (real, measure)
  ```
  { FIXED [venue_venue_type], [pokemon_type1] : AVG([is_winner]) }
  ```
- **`L08 INCLUDE Battle - Avg Power`** (real, measure)
  ```
  { INCLUDE [battle_id] : AVG([adjusted_power]) }
  ```
- **`L09 EXCLUDE Side - Avg Power`** (real, measure)
  ```
  { EXCLUDE [team_side] : AVG([adjusted_power]) }
  ```
- **`L10 Comparison - Power vs Trainer Avg`** (real, measure)
  ```
  [adjusted_power] - { FIXED [trainer_id] : AVG([adjusted_power]) }
  ```
- **`L11 Comparison - Trainer vs Overall`** (real, measure)
  ```
  { FIXED [trainer_id] : AVG([adjusted_power]) } - { FIXED : AVG([adjusted_power]) }
  ```
- **`L12 Nested - Trainer Avg of Battle Avg`** (real, measure)
  ```
  { FIXED [trainer_id] : AVG({ INCLUDE [battle_id] : AVG([adjusted_power]) }) }
  ```
- **`L13 % of Total via FIXED`** (real, measure)
  ```
  SUM([adjusted_power]) / { FIXED : SUM([adjusted_power]) }
  ```
- **`L14 Trainer Battle Count (FIXED)`** (integer, measure)
  ```
  { FIXED [trainer_id] : COUNTD([battle_id]) }
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/12_lod_blank.twbx`
2. Reproduce each of the 8 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/12_lod_student.twbx`
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
