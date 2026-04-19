# Lesson 07: Day 2 Warm-up

**Day:** 2  
**Duration:** 30 min  
**Instructor workbook:** `instructor/workbooks/07_warmup_instructor.twbx`  
**Student answer key:** `student/workbooks/07_warmup_student.twbx`  
**Student blank:** `student/workbooks_blank/07_warmup_blank.twbx`  
**Dataset(s):** `trainer.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Trainers by Region`
- **Mark:** `Bar`
- **Rows:** `Count([trainer_id])`
- **Columns:** `[home_region]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Strategy vs Aggression`
- **Mark:** `Circle`
- **Rows:** `Avg([aggression_rating])`
- **Columns:** `Avg([strategy_rating])`
- **Color:** `[experience_tier]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Preferred Types`
- **Mark:** `Bar`
- **Rows:** `Count([trainer_id])`
- **Columns:** `[preferred_type]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Gym Leader Stats`
- **Mark:** `Bar`
- **Rows:** `Avg([Avg Rating])`
- **Columns:** `[Gym Leader Label]`
- **Calc fields used:**
  - `Gym Leader Label` = `IIF([is_gym_leader]=1, "Gym Leader", "Regular")`
  - `Avg Rating` = `([strategy_rating]+[adaptability_rating]+[aggression_rating])/3`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Years vs Avg Rating`
- **Mark:** `Circle`
- **Rows:** `Avg([Avg Rating])`
- **Columns:** `[years_experience]`
- **Color:** `[experience_tier]`
- **Calc fields used:**
  - `Avg Rating` = `([strategy_rating]+[adaptability_rating]+[aggression_rating])/3`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Gym Leader Label`** (string, dimension)
  ```
  IIF([is_gym_leader]=1, "Gym Leader", "Regular")
  ```
- **`Avg Rating`** (real, measure)
  ```
  ([strategy_rating]+[adaptability_rating]+[aggression_rating])/3
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/07_warmup_blank.twbx`
2. Reproduce each of the 5 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/07_warmup_student.twbx`
4. Save your work as `<lesson>_<your_initials>.twbx`

## Common pitfalls

- Wrong aggregation (default SUM when AVG is needed)
- Date dimension on Columns as discrete vs continuous — toggle via right-click
- Calc-field references use `[bracket_name]`, not the friendly caption
- IIF(condition, true_value, false_value) — false_value is required

## Talking points to memorize

- "Notice that we drag, never type — Tableau builds the query for us."
- "The shelf you drop a field on changes how Tableau treats it."
- "Every calc field is just a formula — read it left to right like math."
