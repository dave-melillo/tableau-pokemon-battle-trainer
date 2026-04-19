# Lesson 10: Mapping

**Day:** 2  
**Duration:** 45 min  
**Instructor workbook:** `instructor/workbooks/10_mapping_instructor.twbx`  
**Student answer key:** `student/workbooks/10_mapping_student.twbx`  
**Student blank:** `student/workbooks_blank/10_mapping_blank.twbx`  
**Dataset(s):** `venue.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `01 Symbol Map - Venues`
- **Mark:** `Automatic`
- **Rows:** `Avg([lat])`
- **Columns:** `Avg([lon])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Automatic` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `02 Symbol Map - Colored by Type`
- **Mark:** `Automatic`
- **Rows:** `Avg([lat])`
- **Columns:** `Avg([lon])`
- **Color:** `[venue_type]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Automatic` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `03 Symbol Map - Sized by Capacity`
- **Mark:** `Automatic`
- **Rows:** `Avg([lat])`
- **Columns:** `Avg([lon])`
- **Color:** `[Capacity Bucket]`
- **Size:** `Avg([capacity])`
- **Calc fields used:**
  - `Capacity Bucket` = `IF [capacity] >= 1500 THEN "Mega (1500+)"
ELSEIF [capacity] >= 1000 THEN "Large (1000-1499)"
ELSEIF [capacity] >= 500 THEN "Mid (500-999)"
ELSE "Small (<500)"
END`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Automatic` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `04 Map - Region Highlight`
- **Mark:** `Automatic`
- **Rows:** `Avg([lat])`
- **Columns:** `Avg([lon])`
- **Color:** `[region]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Automatic` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `05 Indoor vs Outdoor`
- **Mark:** `Automatic`
- **Rows:** `Avg([lat])`
- **Columns:** `Avg([lon])`
- **Color:** `[indoor_outdoor]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Automatic` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 6. Sheet `06 Bar Companion - Venues by Region`
- **Mark:** `Bar`
- **Rows:** `Count([venue_id])`
- **Columns:** `[region]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 7. Sheet `07 Bar Companion - Capacity by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([capacity])`
- **Columns:** `[venue_type]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 8. Sheet `08 Terrain Edge by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([terrain_edge_pct])`
- **Columns:** `[venue_type]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Calculated fields cheat sheet (every calc in this workbook)

- **`Capacity Bucket`** (string, dimension)
  ```
  IF [capacity] >= 1500 THEN "Mega (1500+)"
ELSEIF [capacity] >= 1000 THEN "Large (1000-1499)"
ELSEIF [capacity] >= 500 THEN "Mid (500-999)"
ELSE "Small (<500)"
END
  ```

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/10_mapping_blank.twbx`
2. Reproduce each of the 8 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/10_mapping_student.twbx`
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
