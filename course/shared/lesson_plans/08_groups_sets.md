# Lesson 08: Groups & Sets

**Day:** 2  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/08_groups_sets_instructor.twbx`  
**Student answer key:** `student/workbooks/08_groups_sets_student.twbx`  
**Student blank:** `student/workbooks_blank/08_groups_sets_blank.twbx`  
**Dataset(s):** `pokemon.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Type Family Counts`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[Type Family (Group)]`
- **Calc fields used:**
  - `Type Family (Group)` = `IF [type1]="fire" OR [type1]="water" OR [type1]="grass" THEN "Starter Element"
ELSEIF [type1]="dragon" OR [type1]="psychic" OR [type1]="ghost" OR [type1]="dark" THEN "Mystical"
ELSEIF [type1]="fighting" OR [type1]="rock" OR [type1]="steel" OR [type1]="ground" THEN "Physical"
ELSEIF [type1]="electric" OR [type1]="ice" OR [type1]="fairy" OR [type1]="flying" THEN "Air & Energy"
ELSE "Common"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Avg Total by Type Family`
- **Mark:** `Bar`
- **Rows:** `Avg([base_total])`
- **Columns:** `[Type Family (Group)]`
- **Color:** `[Legendary Set]`
- **Calc fields used:**
  - `Type Family (Group)` = `IF [type1]="fire" OR [type1]="water" OR [type1]="grass" THEN "Starter Element"
ELSEIF [type1]="dragon" OR [type1]="psychic" OR [type1]="ghost" OR [type1]="dark" THEN "Mystical"
ELSEIF [type1]="fighting" OR [type1]="rock" OR [type1]="steel" OR [type1]="ground" THEN "Physical"
ELSEIF [type1]="electric" OR [type1]="ice" OR [type1]="fairy" OR [type1]="flying" THEN "Air & Energy"
ELSE "Common"
END`
  - `Legendary Set` = `IIF([is_legendary]=1, "In - Legendary", "Out - Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Speed Bucket Distribution`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[Speed Bucket (Group)]`
- **Color:** `[Power Tier]`
- **Calc fields used:**
  - `Speed Bucket (Group)` = `IF [speed] >= 110 THEN "Lightning"
ELSEIF [speed] >= 80 THEN "Fast"
ELSEIF [speed] >= 50 THEN "Average"
ELSE "Slow"
END`
  - `Power Tier` = `IF [base_total] >= 600 THEN "S-Tier"
ELSEIF [base_total] >= 500 THEN "A-Tier"
ELSEIF [base_total] >= 400 THEN "B-Tier"
ELSE "C-Tier"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 S-Tier Pokemon Set`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[Top Tier Set (S-Tier)]`
- **Color:** `[type1]`
- **Calc fields used:**
  - `Top Tier Set (S-Tier)` = `IIF([base_total] >= 600, "In - S-Tier", "Out")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Heavy Hitters by Type`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[type1]`
- **Color:** `[Heavy Hitter Set]`
- **Calc fields used:**
  - `Heavy Hitter Set` = `IIF([attack] >= 100 AND [defense] >= 100, "In - Heavy Hitter", "Out")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Generation Group x Power Tier`
- **Mark:** `Square`
- **Rows:** `[Generation Group]`
- **Columns:** `[Power Tier]`
- **Color:** `Count([name])`
- **Calc fields used:**
  - `Power Tier` = `IF [base_total] >= 600 THEN "S-Tier"
ELSEIF [base_total] >= 500 THEN "A-Tier"
ELSEIF [base_total] >= 400 THEN "B-Tier"
ELSE "C-Tier"
END`
  - `Generation Group` = `IF [generation] <= 2 THEN "Classic (Gen 1-2)"
ELSEIF [generation] <= 4 THEN "Modern (Gen 3-4)"
ELSE "Recent (Gen 5+)"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `07 Legendaries by Type Family`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[Type Family (Group)]`
- **Color:** `[Legendary Set]`
- **Calc fields used:**
  - `Type Family (Group)` = `IF [type1]="fire" OR [type1]="water" OR [type1]="grass" THEN "Starter Element"
ELSEIF [type1]="dragon" OR [type1]="psychic" OR [type1]="ghost" OR [type1]="dark" THEN "Mystical"
ELSEIF [type1]="fighting" OR [type1]="rock" OR [type1]="steel" OR [type1]="ground" THEN "Physical"
ELSEIF [type1]="electric" OR [type1]="ice" OR [type1]="fairy" OR [type1]="flying" THEN "Air & Energy"
ELSE "Common"
END`
  - `Legendary Set` = `IIF([is_legendary]=1, "In - Legendary", "Out - Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Type Family (Group)`** (string, dimension)
  ```
  IF [type1]="fire" OR [type1]="water" OR [type1]="grass" THEN "Starter Element"
ELSEIF [type1]="dragon" OR [type1]="psychic" OR [type1]="ghost" OR [type1]="dark" THEN "Mystical"
ELSEIF [type1]="fighting" OR [type1]="rock" OR [type1]="steel" OR [type1]="ground" THEN "Physical"
ELSEIF [type1]="electric" OR [type1]="ice" OR [type1]="fairy" OR [type1]="flying" THEN "Air & Energy"
ELSE "Common"
END
  ```
- **`Legendary Set`** (string, dimension)
  ```
  IIF([is_legendary]=1, "In - Legendary", "Out - Standard")
  ```
- **`Top Tier Set (S-Tier)`** (string, dimension)
  ```
  IIF([base_total] >= 600, "In - S-Tier", "Out")
  ```
- **`Speed Bucket (Group)`** (string, dimension)
  ```
  IF [speed] >= 110 THEN "Lightning"
ELSEIF [speed] >= 80 THEN "Fast"
ELSEIF [speed] >= 50 THEN "Average"
ELSE "Slow"
END
  ```
- **`Power Tier`** (string, dimension)
  ```
  IF [base_total] >= 600 THEN "S-Tier"
ELSEIF [base_total] >= 500 THEN "A-Tier"
ELSEIF [base_total] >= 400 THEN "B-Tier"
ELSE "C-Tier"
END
  ```
- **`Heavy Hitter Set`** (string, dimension)
  ```
  IIF([attack] >= 100 AND [defense] >= 100, "In - Heavy Hitter", "Out")
  ```
- **`Generation Group`** (string, dimension)
  ```
  IF [generation] <= 2 THEN "Classic (Gen 1-2)"
ELSEIF [generation] <= 4 THEN "Modern (Gen 3-4)"
ELSE "Recent (Gen 5+)"
END
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/08_groups_sets_blank.twbx`
2. Reproduce each of the 7 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/08_groups_sets_student.twbx`
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
