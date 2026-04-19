"""Generate a lesson-plan markdown file directly from an instructor workbook config.

Sheet names, mark types, shelf placements, calc-field formulas, and dashboard
contents are read straight from the JSON config so the LP is guaranteed in sync
with the workbook the instructor will demo.

Usage:
  python3 generate_lesson_plan.py <instructor_config.json> <output.md>
"""
from __future__ import annotations
import json
import sys
from pathlib import Path


LESSON_META = {
    "01_intro": {"title": "Intro to Tableau", "day": 1, "duration": "45 min"},
    "02_basic_visuals": {"title": "Basic Visuals", "day": 1, "duration": "60 min"},
    "03_advanced_visuals": {"title": "Advanced Visuals", "day": 1, "duration": "60 min"},
    "04_joins_intro": {"title": "Joins & Data Modeling Intro", "day": 1, "duration": "60 min"},
    "05_joins_advanced": {"title": "Joins + Advanced Visualizations", "day": 1, "duration": "60 min"},
    "06_story": {"title": "Day 1 Story Recap", "day": 1, "duration": "45 min"},
    "07_warmup": {"title": "Day 2 Warm-up", "day": 2, "duration": "30 min"},
    "08_groups_sets": {"title": "Groups & Sets", "day": 2, "duration": "60 min"},
    "09_calculations": {"title": "Calculations", "day": 2, "duration": "60 min"},
    "10_mapping": {"title": "Mapping", "day": 2, "duration": "45 min"},
    "11_dashboards": {"title": "Dashboards", "day": 2, "duration": "60 min"},
    "12_lod": {"title": "LOD Calculations", "day": 2, "duration": "60 min"},
    "13_master_reference": {"title": "Master Reference Workbook (Instructor Only)", "day": 2, "duration": "office hours"},
}


def fmt_field(f: dict) -> str:
    agg = f.get("agg", "None")
    if agg == "None":
        return f"`[{f['field']}]`"
    return f"`{agg}([{f['field']}])`"


def fmt_shelf(fields: list) -> str:
    if not fields:
        return "_(empty)_"
    return " · ".join(fmt_field(f) for f in fields)


def datasets_summary(cfg: dict) -> str:
    if "tables" in cfg:
        bits = []
        for t in cfg["tables"]:
            bits.append(f"`{Path(t['csv_path']).name}` (alias `{t['alias']}`)")
        return ", ".join(bits)
    return f"`{Path(cfg['data_csv']).name}`"


def joins_summary(cfg: dict) -> list[str]:
    out = []
    for j in cfg.get("joins", []):
        out.append(f"`{j['left_table']}.{j['left_col']} = {j['right_table']}.{j['right_col']}` ({j.get('join_type', 'inner')} join)")
    return out


def render(cfg: dict, slug: str) -> str:
    meta = LESSON_META.get(slug, {"title": slug, "day": "?", "duration": "?"})
    is_master = slug == "13_master_reference"

    lines = []
    lines.append(f"# Lesson {slug.split('_')[0]}: {meta['title']}\n")
    lines.append(f"**Day:** {meta['day']}  ")
    lines.append(f"**Duration:** {meta['duration']}  ")
    lines.append(f"**Instructor workbook:** `instructor/workbooks/{slug}_instructor.twbx`  ")
    if not is_master:
        lines.append(f"**Student answer key:** `student/workbooks/{slug}_student.twbx`  ")
        lines.append(f"**Student blank:** `student/workbooks_blank/{slug}_blank.twbx`  ")
    lines.append(f"**Dataset(s):** {datasets_summary(cfg)}\n")

    joins = joins_summary(cfg)
    if joins:
        lines.append("**Joins configured in the workbook:**")
        for j in joins:
            lines.append(f"- {j}")
        lines.append("")

    # ---- Live demo flow ----
    lines.append("## Live demo flow (mirror the workbook sheet by sheet)\n")
    lines.append("Open the instructor workbook. Walk these sheets in order — they are the demo script.\n")

    for i, ws in enumerate(cfg.get("worksheets", []), 1):
        lines.append(f"### {i}. Sheet `{ws['name']}`")
        lines.append(f"- **Mark:** `{ws.get('mark', 'Automatic')}`")
        if ws.get("rows"):
            lines.append(f"- **Rows:** {fmt_shelf(ws['rows'])}")
        if ws.get("cols"):
            lines.append(f"- **Columns:** {fmt_shelf(ws['cols'])}")
        for enc in ("color", "size", "shape", "text", "tooltip"):
            if enc in ws:
                lines.append(f"- **{enc.capitalize()}:** {fmt_field(ws[enc])}")
        # Identify any calc-field references on this sheet
        refs = set()
        for shelf in ("rows", "cols"):
            for f in ws.get(shelf, []):
                refs.add(f["field"])
        for enc in ("color", "size", "shape", "text", "tooltip"):
            if enc in ws:
                refs.add(ws[enc]["field"])
        used_calcs = [cf for cf in cfg.get("calculated_fields", []) if cf["caption"] in refs]
        if used_calcs:
            lines.append(f"- **Calc fields used:**")
            for cf in used_calcs:
                lines.append(f"  - `{cf['caption']}` = `{cf['formula']}`")
        lines.append(f"- **Build steps:** drag the row fields → drag the column fields → set mark to `{ws.get('mark', 'Automatic')}` → add encodings.")
        lines.append("- **Talking point:** _what does this answer? speak it aloud as you build._\n")

    # ---- Calc fields cheat sheet ----
    if cfg.get("calculated_fields"):
        lines.append("## Calculated fields cheat sheet (every calc in this workbook)\n")
        for cf in cfg["calculated_fields"]:
            lines.append(f"- **`{cf['caption']}`** ({cf['datatype']}, {cf.get('role','measure')})")
            lines.append(f"  ```")
            lines.append(f"  {cf['formula']}")
            lines.append(f"  ```")
        lines.append("")

    # ---- Dashboard ----
    if cfg.get("dashboard"):
        d = cfg["dashboard"]
        w, h = d.get("size", [1200, 800])
        lines.append("## Dashboard\n")
        lines.append(f"- **Name:** `{d['name']}`")
        lines.append(f"- **Size:** {w} × {h}")
        lines.append(f"- **Sheets stacked vertically (top → bottom):**")
        for i, s in enumerate(d["sheets"], 1):
            lines.append(f"  {i}. `{s}`")
        lines.append("")

    # ---- Activity / How to use ----
    if is_master:
        lines.append("## How to use this reference (instructor-only)\n")
        lines.append("- Office hours: when a student asks how to do X, find a sheet that does it and demo it live.")
        lines.append("- Module 4–5 questions → open joined sheets that show cross-table analysis")
        lines.append("- Module 9 questions → open the calc-fields cheat sheet above")
        lines.append("- Module 10 questions → open `Q2 Venue Map - Battle Counts`")
        lines.append("- Module 12 questions → open any FIXED LOD sheet (Q3, Q4, Q5, Q6, Q7)")
        lines.append("")
    else:
        lines.append("## Student activity\n")
        lines.append(f"1. Open the BLANK workbook: `student/workbooks_blank/{slug}_blank.twbx`")
        lines.append(f"2. Reproduce each of the {len(cfg.get('worksheets', []))} sheet(s) listed above.")
        lines.append(f"3. After 30 minutes (or when stuck), compare against the answer key: `student/workbooks/{slug}_student.twbx`")
        lines.append("4. Save your work as `<lesson>_<your_initials>.twbx`\n")

    # ---- Common pitfalls / talking points ----
    lines.append("## Common pitfalls\n")
    lines.append("- Wrong aggregation (default SUM when AVG is needed)")
    lines.append("- Date dimension on Columns as discrete vs continuous — toggle via right-click")
    if joins:
        lines.append("- Confusing relationship vs join — modern Tableau uses relationships by default")
        lines.append("- Forgetting that joined-table fields use the prefixed name (e.g. `venue_region`, not just `region`)")
    if cfg.get("calculated_fields"):
        lines.append("- Calc-field references use `[bracket_name]`, not the friendly caption")
        lines.append("- IIF(condition, true_value, false_value) — false_value is required")
    lines.append("")

    lines.append("## Talking points to memorize\n")
    lines.append("- \"Notice that we drag, never type — Tableau builds the query for us.\"")
    lines.append("- \"The shelf you drop a field on changes how Tableau treats it.\"")
    if joins:
        lines.append("- \"The join is configured in the data canvas. Once set, both tables' fields appear in the Data pane.\"")
    if cfg.get("calculated_fields"):
        lines.append("- \"Every calc field is just a formula — read it left to right like math.\"")
    lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("usage: generate_lesson_plan.py <instructor_config.json> <output.md>", file=sys.stderr)
        sys.exit(2)
    cfg_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    cfg = json.loads(cfg_path.read_text())
    slug = cfg_path.stem.replace("_instructor", "")
    md = render(cfg, slug)
    out_path.write_text(md)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
