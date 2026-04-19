# Lesson 01: Intro to Tableau

**Day:** 1  
**Duration:** 45 min  
**Instructor workbook:** `instructor/workbooks/01_intro_instructor.twbx`  
**Student answer key:** `student/workbooks/01_intro_student.twbx`  
**Student blank:** `student/workbooks_blank/01_intro_blank.twbx`  
**Dataset(s):** `pokemon.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `Welcome - Avg HP by Type`
- **Mark:** `Bar`
- **Rows:** `Avg([hp])`
- **Columns:** `[type1]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/01_intro_blank.twbx`
2. Reproduce each of the 1 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/01_intro_student.twbx`
4. Save your work as `<lesson>_<your_initials>.twbx`

## Common pitfalls

- Wrong aggregation (default SUM when AVG is needed)
- Date dimension on Columns as discrete vs continuous — toggle via right-click

## Talking points to memorize

- "Notice that we drag, never type — Tableau builds the query for us."
- "The shelf you drop a field on changes how Tableau treats it."
