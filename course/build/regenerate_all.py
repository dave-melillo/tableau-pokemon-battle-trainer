"""One-command rebuild: every workbook, every lesson plan, the slide deck.

Usage:
    python3 course/build/regenerate_all.py

Discovers configs under instructor/configs/ and student/configs/, builds .twbx
files into instructor/workbooks/ and student/workbooks/, regenerates lesson
plans into shared/lesson_plans/, and rebuilds course_deck.pptx.
"""
from __future__ import annotations
import json
import sys
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent

INSTRUCTOR_CONFIGS = sorted((COURSE / "instructor" / "configs").glob("*.json"))
STUDENT_CONFIGS = sorted((COURSE / "student" / "configs").glob("*.json"))


def run(args, label):
    print(f"  → {label}")
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ✗ FAILED ({label}):\n{r.stderr}", file=sys.stderr)
        return False
    return True


def main():
    print("=== Workbooks ===")
    fails = 0
    for cfg in INSTRUCTOR_CONFIGS + STUDENT_CONFIGS:
        ok = run([str(HERE / "build_twbx.py"), str(cfg)], cfg.name)
        if not ok:
            fails += 1

    print("\n=== Lesson plans ===")
    for cfg in INSTRUCTOR_CONFIGS:
        slug = cfg.stem.replace("_instructor", "")
        out = COURSE / "shared" / "lesson_plans" / f"{slug}.md"
        ok = run([str(HERE / "generate_lesson_plan.py"), str(cfg), str(out)], slug)
        if not ok:
            fails += 1

    print("\n=== Slide deck ===")
    ok = run([str(HERE / "generate_course_deck.py")], "course_deck.pptx")
    if not ok:
        fails += 1

    if fails:
        print(f"\n{fails} failure(s)", file=sys.stderr)
        sys.exit(1)
    print("\nAll regenerated successfully.")


if __name__ == "__main__":
    main()
