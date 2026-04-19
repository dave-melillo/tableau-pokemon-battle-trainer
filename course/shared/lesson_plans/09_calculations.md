# Lesson 09: Calculations

**Day:** 2  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/09_calculations_instructor.twbx`  
**Student answer key:** `student/workbooks/09_calculations_student.twbx`  
**Student blank:** `student/workbooks_blank/09_calculations_blank.twbx`  
**Dataset(s):** `battle_participant.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Power Lift by Side (C01)`
- **Mark:** `Bar`
- **Rows:** `Avg([C01 Arithmetic - Power Lift])`
- **Columns:** `[team_side]`
- **Calc fields used:**
  - `C01 Arithmetic - Power Lift` = `[adjusted_power] - [base_power]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Power Class Mix (C05)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[C05 Logical - IF/ELSEIF Power Class]`
- **Calc fields used:**
  - `C05 Logical - IF/ELSEIF Power Class` = `IF [adjusted_power] >= 600 THEN "Dominant"
ELSEIF [adjusted_power] >= 500 THEN "Strong"
ELSEIF [adjusted_power] >= 400 THEN "Balanced"
ELSE "Underdog"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Slot Roles (C06)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[C06 Logical - CASE Slot Role]`
- **Color:** `[team_side]`
- **Calc fields used:**
  - `C06 Logical - CASE Slot Role` = `CASE [slot_number]
WHEN 1 THEN "Lead"
WHEN 2 THEN "Middle"
WHEN 3 THEN "Anchor"
ELSE "Reserve"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 MVP Wins (C07)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[C07 Logical - Compound Boolean]`
- **Calc fields used:**
  - `C07 Logical - Compound Boolean` = `IIF([is_winner]=1 AND [is_mvp_flag]=1, "MVP Win", "Other")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Trainer Prefix Distribution (C08)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[C08 String - Trainer Prefix]`
- **Calc fields used:**
  - `C08 String - Trainer Prefix` = `LEFT([trainer_id], 4)`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Win Rate Manual (C12)`
- **Mark:** `Bar`
- **Rows:** `[C12 Aggregate - Win Rate Manual]`
- **Columns:** `[team_side]`
- **Calc fields used:**
  - `C12 Aggregate - Win Rate Manual` = `SUM([is_winner]) / COUNT([battle_id])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `07 Unique Counts (C13/C14)`
- **Mark:** `Bar`
- **Rows:** `[C13 Aggregate - COUNTD Trainers]`
- **Columns:** `[team_side]`
- **Calc fields used:**
  - `C13 Aggregate - COUNTD Trainers` = `COUNTD([trainer_id])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 8. Sheet `08 MVP Power Total (C15)`
- **Mark:** `Bar`
- **Rows:** `[C15 Conditional Agg - MVP Power Sum]`
- **Columns:** `[team_side]`
- **Calc fields used:**
  - `C15 Conditional Agg - MVP Power Sum` = `SUM(IIF([is_mvp_flag]=1, [adjusted_power], 0))`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 9. Sheet `09 Lift Direction (C18)`
- **Mark:** `Bar`
- **Rows:** `Count([battle_participant_id])`
- **Columns:** `[C18 Sign Function - Lift Direction]`
- **Calc fields used:**
  - `C18 Sign Function - Lift Direction` = `SIGN([adjusted_power] - [base_power])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 10. Sheet `10 Power Class x Side`
- **Mark:** `Square`
- **Rows:** `[C05 Logical - IF/ELSEIF Power Class]`
- **Columns:** `[team_side]`
- **Color:** `Count([battle_participant_id])`
- **Calc fields used:**
  - `C05 Logical - IF/ELSEIF Power Class` = `IF [adjusted_power] >= 600 THEN "Dominant"
ELSEIF [adjusted_power] >= 500 THEN "Strong"
ELSEIF [adjusted_power] >= 400 THEN "Balanced"
ELSE "Underdog"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`C01 Arithmetic - Power Lift`** (real, measure)
  ```
  [adjusted_power] - [base_power]
  ```
- **`C02 Arithmetic - Power Ratio`** (real, measure)
  ```
  [adjusted_power] / [base_power]
  ```
- **`C03 Arithmetic - Power per Slot`** (real, measure)
  ```
  [adjusted_power] / [slot_number]
  ```
- **`C04 Logical - IIF Win Label`** (string, dimension)
  ```
  IIF([is_winner]=1, "Won", "Lost")
  ```
- **`C05 Logical - IF/ELSEIF Power Class`** (string, dimension)
  ```
  IF [adjusted_power] >= 600 THEN "Dominant"
ELSEIF [adjusted_power] >= 500 THEN "Strong"
ELSEIF [adjusted_power] >= 400 THEN "Balanced"
ELSE "Underdog"
END
  ```
- **`C06 Logical - CASE Slot Role`** (string, dimension)
  ```
  CASE [slot_number]
WHEN 1 THEN "Lead"
WHEN 2 THEN "Middle"
WHEN 3 THEN "Anchor"
ELSE "Reserve"
END
  ```
- **`C07 Logical - Compound Boolean`** (string, dimension)
  ```
  IIF([is_winner]=1 AND [is_mvp_flag]=1, "MVP Win", "Other")
  ```
- **`C08 String - Trainer Prefix`** (string, dimension)
  ```
  LEFT([trainer_id], 4)
  ```
- **`C09 String - ID Length`** (integer, measure)
  ```
  LEN([battle_id])
  ```
- **`C10 String - ID Upper`** (string, dimension)
  ```
  UPPER([team_side])
  ```
- **`C11 Type Convert - Slot as String`** (string, dimension)
  ```
  STR([slot_number])
  ```
- **`C12 Aggregate - Win Rate Manual`** (real, measure)
  ```
  SUM([is_winner]) / COUNT([battle_id])
  ```
- **`C13 Aggregate - COUNTD Trainers`** (integer, measure)
  ```
  COUNTD([trainer_id])
  ```
- **`C14 Aggregate - COUNTD Pokemon`** (integer, measure)
  ```
  COUNTD([pokemonid])
  ```
- **`C15 Conditional Agg - MVP Power Sum`** (real, measure)
  ```
  SUM(IIF([is_mvp_flag]=1, [adjusted_power], 0))
  ```
- **`C16 Conditional Agg - Wins Only`** (integer, measure)
  ```
  SUM(IIF([is_winner]=1, 1, 0))
  ```
- **`C17 Null-Safe ZN Power Lift`** (real, measure)
  ```
  ZN([adjusted_power]) - ZN([base_power])
  ```
- **`C18 Sign Function - Lift Direction`** (integer, measure)
  ```
  SIGN([adjusted_power] - [base_power])
  ```
- **`C19 ABS Function - Lift Magnitude`** (real, measure)
  ```
  ABS([adjusted_power] - [base_power])
  ```
- **`C20 ROUND - Power 2-decimal`** (real, measure)
  ```
  ROUND([adjusted_power], 2)
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/09_calculations_blank.twbx`
2. Reproduce each of the 10 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/09_calculations_student.twbx`
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
