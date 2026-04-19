# Lesson 02: Basic Visuals

**Day:** 1  
**Duration:** 60 min  
**Instructor workbook:** `instructor/workbooks/02_basic_visuals_instructor.twbx`  
**Student answer key:** `student/workbooks/02_basic_visuals_student.twbx`  
**Student blank:** `student/workbooks_blank/02_basic_visuals_blank.twbx`  
**Dataset(s):** `pokemon.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Bar - Count by Type`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[type1]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Bar Sorted - Avg Attack by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([attack])`
- **Columns:** `[type1]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Side-by-Side - Att vs Def`
- **Mark:** `Bar`
- **Rows:** `Avg([attack])`
- **Columns:** `[type1]` · `[Legendary Label]`
- **Calc fields used:**
  - `Legendary Label` = `IIF([is_legendary]=1, "Legendary", "Standard")`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Stacked Bar - Type Mix by Gen`
- **Mark:** `Bar`
- **Rows:** `Count([name])`
- **Columns:** `[generation]`
- **Color:** `[type1]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Line - Avg Total by Gen`
- **Mark:** `Line`
- **Rows:** `Avg([base_total])`
- **Columns:** `[generation]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Area - Count by Gen`
- **Mark:** `Area`
- **Rows:** `Count([name])`
- **Columns:** `[generation]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Area` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `07 Scatter - Att vs Def`
- **Mark:** `Circle`
- **Rows:** `Avg([defense])`
- **Columns:** `Avg([attack])`
- **Color:** `[type1]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 8. Sheet `08 Bubble - Sized by HP`
- **Mark:** `Circle`
- **Rows:** `Avg([defense])`
- **Columns:** `Avg([attack])`
- **Color:** `[type1]`
- **Size:** `Avg([hp])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 9. Sheet `09 Heat Map - Type x Gen`
- **Mark:** `Square`
- **Rows:** `[type1]`
- **Columns:** `[generation]`
- **Color:** `Count([name])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 10. Sheet `10 Text Table - Stat Summary`
- **Mark:** `Text`
- **Rows:** `[type1]`
- **Columns:** `Avg([base_total])`
- **Text:** `Avg([base_total])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Text` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 11. Sheet `11 Treemap - Pokemon by Type`
- **Mark:** `Square`
- **Color:** `[type1]`
- **Size:** `Count([name])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Square` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Legendary Label`** (string, dimension)
  ```
  IIF([is_legendary]=1, "Legendary", "Standard")
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/02_basic_visuals_blank.twbx`
2. Reproduce each of the 11 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/02_basic_visuals_student.twbx`
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
