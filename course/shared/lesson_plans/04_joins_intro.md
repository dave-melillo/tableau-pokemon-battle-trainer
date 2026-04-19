# Lesson 04: Joins & Data Modeling Intro

**Day:** 1  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/04_joins_intro_instructor.twbx`  
**Student answer key:** `student/workbooks/04_joins_intro_student.twbx`  
**Student blank:** `student/workbooks_blank/04_joins_intro_blank.twbx`  
**Dataset(s):** `battles.csv` (alias `battles`), `venue.csv` (alias `venue`)

**Joins configured in the workbook:**
- `battles.venue_id = venue.venue_id` (left join)

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Battles by Region (joined field)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `[venue_region]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Avg Attendance by Venue Type`
- **Mark:** `Bar`
- **Rows:** `Avg([attendance])`
- **Columns:** `[venue_venue_type]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Fill Rate by Prestige Tier`
- **Mark:** `Bar`
- **Rows:** `Avg([Fill Rate])`
- **Columns:** `[venue_prestige_tier]`
- **Calc fields used:**
  - `Fill Rate` = `[attendance] / [venue_capacity]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Indoor vs Outdoor Margin`
- **Mark:** `Bar`
- **Rows:** `Avg([winning_margin])`
- **Columns:** `[venue_indoor_outdoor]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Battles by Venue Name (top 10)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `[venue_venue_name]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Format Mix by Region`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `[venue_region]`
- **Color:** `[battle_format]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Fill Rate`** (real, measure)
  ```
  [attendance] / [venue_capacity]
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/04_joins_intro_blank.twbx`
2. Reproduce each of the 6 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/04_joins_intro_student.twbx`
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
