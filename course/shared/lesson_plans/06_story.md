# Lesson 06: Day 1 Story Recap

**Day:** 1  
**Duration:** 45 min  
**Instructor workbook:** `instructor/workbooks/06_story_instructor.twbx`  
**Student answer key:** `student/workbooks/06_story_student.twbx`  
**Student blank:** `student/workbooks_blank/06_story_blank.twbx`  
**Dataset(s):** `battles.csv`

## Live demo flow (mirror the workbook sheet by sheet)

Open the instructor workbook. Walk these sheets in order — they are the demo script.

### 1. Sheet `Story Pt 1 - Activity Trend`
- **Mark:** `Line`
- **Rows:** `Count([battle_id])`
- **Columns:** `Month([battle_date])`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Line` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 2. Sheet `Story Pt 2 - Format Popularity`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `[battle_format]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 3. Sheet `Story Pt 3 - Home Field Advantage`
- **Mark:** `Bar`
- **Rows:** `Count([battle_id])`
- **Columns:** `[winning_side]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 4. Sheet `Story Pt 4 - Attendance vs Margin`
- **Mark:** `Circle`
- **Rows:** `Avg([attendance])`
- **Columns:** `Avg([winning_margin])`
- **Color:** `[battle_format]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Circle` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

### 5. Sheet `Story Pt 5 - Weather Effect`
- **Mark:** `Bar`
- **Rows:** `Avg([winning_margin])`
- **Columns:** `[weather_condition]`
- **Build steps:** drag the row fields → drag the column fields → set mark to `Bar` → add encodings.
- **Talking point:** _what does this answer? speak it aloud as you build._

## Student activity

1. Open the BLANK workbook: `student/workbooks_blank/06_story_blank.twbx`
2. Reproduce each of the 5 sheet(s) listed above.
3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/06_story_student.twbx`
4. Save your work as `<lesson>_<your_initials>.twbx`

## Common pitfalls

- Wrong aggregation (default SUM when AVG is needed)
- Date dimension on Columns as discrete vs continuous — toggle via right-click

## Talking points to memorize

- "Notice that we drag, never type — Tableau builds the query for us."
- "The shelf you drop a field on changes how Tableau treats it."
