#!/usr/bin/env python3
"""Weekly health check for the Second Brain vault.

Usage:
    python vault_check.py <vault-path> [--fix] [--today YYYY-MM-DD]

Prints a JSON report to stdout. Standard library only.

--fix applies only the safe, mechanical fixes:
  * add a missing `type` property based on the note's folder
  * add a missing `personal`/`work` tag based on the note's folder
  * repoint a broken [[link]] when exactly one note matches it after
    normalising case, spaces and underscores
Everything else is reported for Claude / the user to decide.
"""
import json
import os
import re
import sys
from datetime import date, datetime

SKIP_DIRS = {".obsidian", ".git", ".trash", "80-Skills", "skill-packages", "Templates", "claude-code", "hooks"}
NO_LINK_RULES = {"daily", "review", "system", "inbox"}  # not flagged as orphans
FOLDER_TYPES = [
    ("00-Inbox", "inbox"),
    ("10-Sessions/Daily", "daily"),
    ("10-Sessions", "session"),
    ("20-Research", "research"),
    ("30-Experiments", "experiment"),
    ("40-Projects", "project"),
    ("50-Work/Daily", "daily"),
    ("50-Work/Sessions", "session"),
    ("50-Work/Research", "research"),
    ("50-Work/Projects", "project"),
    ("50-Work/Reviews", "review"),
    ("90-System/Reviews", "review"),
]
VALID_TYPES = {"inbox", "session", "daily", "research", "experiment", "project", "review", "system"}
ROOT_NAME_OK = {"CLAUDE.md", "Home.md", "README.md"}
LINK_RE = re.compile(r"!?\[\[([^\]\|#\^]+)(#[^\]\|]*)?(\|[^\]]*)?\]\]")
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def norm(s):
    return re.sub(r"[\s_]+", "-", s.strip().lower())


def parse_fm(text):
    """Tiny YAML-frontmatter reader: scalars, inline [a, b] lists and '- item' lists."""
    m = FM_RE.match(text)
    if not m:
        return None, text
    fm, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+-\s", line) and key:
            item = line.strip()[2:].strip().strip("'\"")
            if not isinstance(fm.get(key), list):
                fm[key] = []
            fm[key].append(item)
            continue
        km = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            else:
                fm[key] = val.strip("'\"")
    return fm, text[m.end():]


def parse_date(v):
    if not v or not isinstance(v, str):
        return None
    try:
        return datetime.strptime(v[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def expected_type(rel):
    for prefix, t in FOLDER_TYPES:
        if rel == prefix or rel.startswith(prefix + "/"):
            return t
    return None


def area_of(rel):
    return "work" if rel.startswith("50-Work/") else "personal"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    vault = os.path.abspath(args[0])
    fix = "--fix" in args
    today = date.today()
    if "--today" in args:
        today = parse_date(args[args.index("--today") + 1])

    notes, all_files = {}, {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, vault).replace(os.sep, "/")
            all_files.setdefault(f.lower(), []).append(rel)
            if f.endswith(".md"):
                notes[rel] = full
    # .base files live under 90-System/Bases and are link targets too
    for root, _, files in os.walk(os.path.join(vault, "90-System")):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), vault).replace(os.sep, "/")
            if rel not in all_files.get(f.lower(), []):
                all_files.setdefault(f.lower(), []).append(rel)

    by_stem, by_norm = {}, {}
    for rel in notes:
        stem = os.path.basename(rel)[:-3]
        by_stem.setdefault(stem.lower(), []).append(rel)
        by_norm.setdefault(norm(stem), []).append(rel)

    def resolves(target):
        t = target.strip()
        low = t.lower()
        if low.endswith(".md"):
            low = low[:-3]
        if "/" in low:  # path-style link
            return any(r.lower()[:-3] == low or r.lower()[:-3].endswith("/" + low) for r in notes) or any(
                low in [p.lower() for p in v] for v in all_files.values())
        return low in by_stem or low in all_files

    report = {k: [] for k in [
        "broken_links", "orphans", "missing_frontmatter", "missing_type", "invalid_type",
        "type_folder_mismatch", "missing_area_tag", "work_tag_outside_work", "bad_filename",
        "inbox_stale", "experiments_stuck", "ideas_old", "session_stubs", "research_old",
        "daily_missing_session_link"]}
    fixed = []
    incoming = {rel: 0 for rel in notes}
    outgoing = {}
    meta = {}

    for rel, full in notes.items():
        with open(full, encoding="utf-8") as fh:
            text = fh.read()
        fm, body = parse_fm(text)
        meta[rel] = fm or {}
        changed = False
        exp = expected_type(rel)
        is_root = "/" not in rel
        name = os.path.basename(rel)

        if not (is_root and name in ROOT_NAME_OK) and (" " in name or name != name.lower()):
            report["bad_filename"].append(rel)

        if fm is None:
            if exp and not is_root:
                if fix:
                    tag = area_of(rel)
                    made = date.fromtimestamp(os.path.getmtime(full)).isoformat()
                    text = f"---\ntype: {exp}\ncreated: {made}\ntags: [{tag}]\n---\n" + text
                    fm = {"type": exp, "tags": [tag]}
                    meta[rel] = fm
                    changed = True
                    fixed.append({"note": rel, "fix": f"added frontmatter (type: {exp})"})
                else:
                    report["missing_frontmatter"].append(rel)
            elif not is_root:
                report["missing_frontmatter"].append(rel)
        if fm is not None:
            t = fm.get("type")
            if not t:
                if exp and fix:
                    text = FM_RE.sub(lambda m: m.group(0).replace("---\n", f"---\ntype: {exp}\n", 1), text, count=1)
                    fm["type"] = exp
                    changed = True
                    fixed.append({"note": rel, "fix": f"added type: {exp}"})
                else:
                    report["missing_type"].append(rel)
            elif t not in VALID_TYPES:
                report["invalid_type"].append({"note": rel, "type": t})
            elif exp and t != exp:
                report["type_folder_mismatch"].append({"note": rel, "type": t, "folder_expects": exp})

            tags = fm.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            tags = [x.lstrip("#") for x in tags]
            if "personal" not in tags and "work" not in tags:
                want = area_of(rel)
                if fix and "tags" not in fm:
                    text = FM_RE.sub(lambda m: m.group(0).replace("\n---", f"\ntags: [{want}]\n---", 1)
                                     if m.group(0).count("\n---") else m.group(0), text, count=1)
                    fixed.append({"note": rel, "fix": f"added tags: [{want}]"})
                    changed = True
                else:
                    report["missing_area_tag"].append(rel)
            if "work" in tags and not rel.startswith("50-Work/"):
                report["work_tag_outside_work"].append(rel)

        # links (ignore code)
        scan = CODE_RE.sub("", text)
        outs = []
        for m in LINK_RE.finditer(scan):
            target = m.group(1).strip()
            outs.append(target)
            if resolves(target):
                low = target.lower()[:-3] if target.lower().endswith(".md") else target.lower()
                for r in by_stem.get(low.split("/")[-1], []):
                    if r != rel:
                        incoming[r] += 1
                continue
            cands = by_norm.get(norm(target.split("/")[-1]), [])
            if fix and len(cands) == 1:
                new = os.path.basename(cands[0])[:-3]
                text = text.replace(f"[[{target}", f"[[{new}")
                incoming[cands[0]] += 1
                changed = True
                fixed.append({"note": rel, "fix": f"relinked [[{target}]] -> [[{new}]]"})
            else:
                report["broken_links"].append({"note": rel, "link": target,
                                               "candidates": [os.path.basename(c)[:-3] for c in cands]})
        outgoing[rel] = outs
        if changed:
            with open(full, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)

    # per-note age checks
    for rel, fm in meta.items():
        t = fm.get("type")
        st = fm.get("status")
        created = parse_date(fm.get("created")) or parse_date(fm.get("date"))
        mtime = date.fromtimestamp(os.path.getmtime(notes[rel]))
        if rel.startswith("00-Inbox/"):
            age = (today - (created or mtime)).days
            if age > 7:
                report["inbox_stale"].append({"note": rel, "days": age, "type": t})
        if t == "experiment":
            if st == "trying":
                started = parse_date(fm.get("started")) or created or mtime
                days = (today - started).days
                if days > 14:
                    report["experiments_stuck"].append({"note": rel, "days_trying": days})
            elif st == "idea":
                days = (today - (created or mtime)).days
                if days > 60:
                    report["ideas_old"].append({"note": rel, "days": days})
        if t == "session" and st == "stub":
            report["session_stubs"].append(rel)
        if t == "research" and st == "current":
            upd = parse_date(fm.get("updated")) or created or mtime
            days = (today - upd).days
            if days > 180:
                report["research_old"].append({"note": rel, "days_since_update": days})
        if t not in NO_LINK_RULES and "/" in rel and incoming.get(rel, 0) == 0 and not outgoing.get(rel):
            report["orphans"].append(rel)

    # sessions missing from their daily note
    for rel, fm in meta.items():
        if fm.get("type") != "session":
            continue
        d = fm.get("date", "")[:10]
        daily_dir = "50-Work/Daily" if rel.startswith("50-Work/") else "10-Sessions/Daily"
        daily = f"{daily_dir}/{d}.md"
        stem = os.path.basename(rel)[:-3]
        if daily not in notes or f"[[{stem}" not in open(notes[daily], encoding="utf-8").read():
            report["daily_missing_session_link"].append({"session": rel, "daily": daily,
                                                         "time": fm.get("time", "")})

    counts = {"notes": len(notes)}
    for t in VALID_TYPES:
        counts[t] = sum(1 for m in meta.values() if m.get("type") == t)
    out = {"vault": vault, "today": today.isoformat(), "counts": counts, "fixed": fixed,
           "issues": {k: v for k, v in report.items() if v}}
    # split for the report writer: anything under 50-Work stays in the work report
    def is_work(item):
        s = json.dumps(item)
        return "50-Work/" in s
    out["work_issue_count"] = sum(1 for v in report.values() for i in v if is_work(i))
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
