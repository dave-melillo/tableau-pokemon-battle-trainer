# Tableau Pokémon Trainer

```
 _____  _    ____  _     _____    _    _   _
|_   _|/ \  | __ )| |   | ____|  / \  | | | |
  | | / _ \ |  _ \| |   |  _|   / _ \ | | | |
  | |/ ___ \| |_) | |___| |___ / ___ \| |_| |
  |_/_/   \_\____/|_____|_____/_/   \_\\___/

 ____   ___  _  _______ __  __  ___  _   _
|  _ \ / _ \| |/ / ____|  \/  |/ _ \| \ | |
| |_) | | | | ' /|  _| | |\/| | | | |  \| |
|  __/| |_| | . \| |___| |  | | |_| | |\  |
|_|    \___/|_|\_\_____|_|  |_|\___/|_| \_|

 _____ ____    _    ___ _   _ _____ ____
|_   _|  _ \  / \  |_ _| \ | | ____|  _ \
  | | | |_) |/ _ \  | ||  \| |  _| | |_) |
  | | |  _ </ ___ \ | || |\  | |___|  _ <
  |_| |_| \_\_/   \_\___|_| \_|_____|_| \_\

         ╔═══════╗
         ║ ◆ ◆ ◆ ║  bar chart
         ║ ◆ ◆   ║
         ║ ◆     ║
         ╚═══════╝

         ╭─╮  ╭─╮
        ╱   ╲╱   ╲   line chart
       ╱           ╲
      ╱             ╲

       •     •  •
      • • •      •   scatter
       •    • •
            •
```

A 2-day Tableau course built entirely on a Pokémon battle dataset. 13 lessons, instructor + student workbooks, lesson plans, and a slide deck — all regeneratable from JSON configs.

> **Gotta visualize 'em all.**

---

## What's in the box

```
pokemon/
└── course/
    ├── instructor/
    │   ├── configs/                   13 JSON configs (source of truth)
    │   └── workbooks/                 13 instructor .twbx files (the demos)
    ├── student/
    │   ├── configs/                   12 student answer-key configs
    │   ├── workbooks/                 12 fully-built answer keys
    │   └── workbooks_blank/           12 blank starter workbooks
    ├── shared/
    │   ├── lesson_plans/              13 markdown LPs (the script)
    │   ├── raw_data/                  5 source CSVs
    │   └── images/                    12 Pokémon artwork files
    ├── slides/
    │   └── course_deck.pptx           ONE deck for instructors AND students
    └── build/
        ├── regenerate_all.py          one-command rebuild
        ├── build_twbx.py              .twbx generator (handles single + multi-table)
        ├── csv_to_hyper.py            CSV → Hyper extract converter
        ├── generate_lesson_plan.py    LP generator (mirrors workbook configs)
        ├── generate_course_deck.py    slide-deck generator
        ├── inspect_data.py            CSV column profiler
        └── prejoin.py                 (legacy helper, kept for reference)
```

---

## How to teach with it

For each lesson, you have **three things in sync**:

| Component | Where | Role |
|---|---|---|
| Instructor workbook | `course/instructor/workbooks/<NN>_<slug>_instructor.twbx` | The demo you click through |
| Lesson plan | `course/shared/lesson_plans/<NN>_<slug>.md` | Your script, sheet by sheet |
| Slide deck | `course/slides/course_deck.pptx` | What the room sees on the screen |

Open all three side by side. Read the LP, click the workbook, the slide narrates for the room.

For students:

| Component | Where | Role |
|---|---|---|
| Blank starter | `course/student/workbooks_blank/<NN>_<slug>_blank.twbx` | What students open to attempt |
| Answer key | `course/student/workbooks/<NN>_<slug>_student.twbx` | What they compare against after attempting |

---

## The 13 lessons

### Day 1 — Foundations
1. **Intro to Tableau** — interface tour, dimensions vs measures
2. **Basic Visuals** — bar, line, scatter, pie, treemap, heatmap, 11 chart types total
3. **Advanced Visuals** — time series, multi-encoding marks, first calculated field
4. **Joins & Data Modeling Intro** — join battles + venue inside Tableau
5. **Joins + Advanced Visualizations** — three-table join: battle_participant + pokemon + trainer
6. **Day 1 Story Recap** — Tableau Stories

### Day 2 — Advanced Techniques
7. **Warm-up: Trainers** — exploratory analysis on trainer.csv
8. **Groups & Sets** — segmentation with groups, sets, and calc-field equivalents
9. **Calculations** — 20 calc fields covering arithmetic, IIF, IF/ELSEIF, CASE, COUNTD, conditional aggregates, string ops, math helpers
10. **Mapping** — geographic visualization on venue lat/lon
11. **Dashboards** — combine multiple sheets into an interactive dashboard
12. **LOD Calculations** — 14 LODs covering FIXED, INCLUDE, EXCLUDE, nested LODs
13. **Master Reference** — instructor's apex workbook, 12 sheets answering every business question

---

## The dataset

| File | What it is | Rows |
|---|---|---|
| `pokemon.csv` | Pokémon dimension (name, type, stats, generation) | 801 |
| `battles.csv` | Battle fact table | 10,000 |
| `battle_participant.csv` | Bridge: battle ↔ trainer ↔ pokemon | 36,451 |
| `trainer.csv` | Trainer dimension (class, region, ratings) | 180 |
| `venue.csv` | Venue dimension with lat/lon | 54 |

All synthetic. The simulator builds in **venue-type bias** — Pokémon matching the venue's elemental theme have a statistical edge. A trainer's preferred type and home region also influence outcomes. Real signals to discover.

Star-schema joins:
- `battles.venue_id = venue.venue_id`
- `battle_participant.battle_id = battles.battle_id`
- `battle_participant.trainer_id = trainer.trainer_id`
- `battle_participant.pokemonid = pokemon.pokedex_number`

---

## Regenerating everything

If you edit any config (workbook layouts, calc fields, sheets), regenerate the artifacts:

```bash
cd pokemon
python3 course/build/regenerate_all.py
```

This rebuilds:
- All 25 `.twbx` workbooks
- All 13 `.md` lesson plans (mirroring the configs)
- The single `course_deck.pptx`

### Requirements

```bash
pip install pandas tableauhyperapi python-pptx
```

Tested on Python 3.11. `tableauhyperapi` is the official Hyper extract API — required for Tableau Public to accept the workbooks.

---

## Editing the course

The configs at `course/instructor/configs/*.json` are the **source of truth**. Each describes:
- The dataset (or multi-table joined dataset)
- Calculated fields (with formulas)
- Worksheets (mark type, rows, cols, encodings)
- Optional dashboard layout

To add a sheet to lesson 9, edit `course/instructor/configs/09_calculations_instructor.json`, add a new entry to `worksheets`, then run `regenerate_all.py`. The workbook updates, the LP updates, the slide deck updates. They stay in sync.

---

## License

Pokémon and all related characters are © Nintendo / Game Freak. The dataset here is **simulated synthetic data** that uses Pokémon names and types for educational pedagogy. No real Pokémon were harmed in the making of this course.

The course material (configs, scripts, LPs, slides) is yours to use, modify, and teach.

```
  ____    ___    _____  _____  _       _
 / ___|  / _ \  |_   _||_   _|/ \     | |
| |  _  | | | |   | |    | | / _ \    | |
| |_| | | |_| |   | |    | |/ ___ \   |_|
 \____|  \___/    |_|    |_/_/   \_\  (_)

__     __ ___   ____  _   _     _     _      ___   _____
\ \   / /|_ _| / ___|| | | |   / \   | |    |_ _| |__  /
 \ \ / /  | |  \___ \| | | |  / _ \  | |     | |    / /
  \ V /   | |   ___) | |_| | / ___ \ | |___  | |   / /_
   \_/   |___| |____/ \___/ /_/   \_\|_____|___| /____|

 _____ __  __    _    _     _     _
| ____|  \/  |  / \  | |   | |   | |
|  _| | |\/| | / _ \ | |   | |   | |
| |___| |  | |/ ___ \| |___| |___|_|
|_____|_|  |_/_/   \_\_____|_____(_)
```
