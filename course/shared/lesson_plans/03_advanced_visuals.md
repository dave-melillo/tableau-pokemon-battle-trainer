# Lesson 03: Advanced Visuals

**Day:** 1  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/03_advanced_visuals_instructor.twbx`  
**Student answer key:** `student/workbooks/03_advanced_visuals_student.twbx`  
**Student blank:** `student/workbooks_blank/03_advanced_visuals_blank.twbx`  
**Dataset(s):** `battles.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Time Series - Battles by Month`
- **Mark:** `Line`
- **Rows:** `Count([battle_id])`
- **Columns:** `Month([battle_date])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Discrete Time - Battles by Quarter`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `Quarter([battle_date])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Heat Map - Format x Weather`
- **Mark:** `Square`
- **Rows:** `[battle_format]`
- **Columns:** `[weather_condition]`
- **Color:** `Count([battle_id])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Box Plot Data - Margin by Format`
- **Mark:** `Circle`
- **Rows:** `[winning_margin]`
- **Columns:** `[battle_format]`
- **Color:** `[winning_side]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Stacked Bar - Wins by Side and Format`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `[battle_format]`
- **Color:** `[winning_side]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Scatter - Turns vs Margin`
- **Mark:** `Circle`
- **Rows:** `Avg([winning_margin])`
- **Columns:** `[battle_turns]`
- **Color:** `[Margin Tier]`
- **Size:** `Avg([attendance])`
- **Calc fields used:**
  - `Margin Tier` = `IF [winning_margin] >= 100 THEN "Blowout"
ELSEIF [winning_margin] >= 50 THEN "Decisive"
ELSEIF [winning_margin] >= 20 THEN "Solid"
ELSE "Close"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `07 Trend - Avg Attendance Over Time`
- **Mark:** `Line`
- **Rows:** `Avg([attendance])`
- **Columns:** `Month([battle_date])`
- **Color:** `[battle_format]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 8. Sheet `08 Bullet-style - Title vs Regular`
- **Mark:** `Bar`
- **Rows:** `Avg([attendance])`
- **Columns:** `[Title Match Label]`
- **Calc fields used:**
  - `Title Match Label` = `IIF([title_match_flag]=1, "Title Match", "Regular")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 9. Sheet `09 Slope - Margin by Weather`
- **Mark:** `Line`
- **Rows:** `Avg([winning_margin])`
- **Columns:** `[weather_condition]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 10. Sheet `10 Highlight Table - Format x Margin Tier`
- **Mark:** `Square`
- **Rows:** `[Margin Tier]`
- **Columns:** `[battle_format]`
- **Color:** `Count([battle_id])`
- **Calc fields used:**
  - `Margin Tier` = `IF [winning_margin] >= 100 THEN "Blowout"
ELSEIF [winning_margin] >= 50 THEN "Decisive"
ELSEIF [winning_margin] >= 20 THEN "Solid"
ELSE "Close"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Title Match Label`** (string, dimension)
  ```
  IIF([title_match_flag]=1, "Title Match", "Regular")
  ```
- **`Margin Tier`** (string, dimension)
  ```
  IF [winning_margin] >= 100 THEN "Blowout"
ELSEIF [winning_margin] >= 50 THEN "Decisive"
ELSEIF [winning_margin] >= 20 THEN "Solid"
ELSE "Close"
END
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/03_advanced_visuals_blank.twbx`
2. Reproduce each of the 10 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/03_advanced_visuals_student.twbx`
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
