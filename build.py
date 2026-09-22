"""Builds index.html (and the CV PDF) from data/profile.json.

Run:  python build.py            # rebuild index.html
      python build.py --pdf      # also re-print assets/Tolulope_Gbenga_CV.pdf from cv.html

Every fact on the site comes from data/profile.json. Edit that file, rebuild, commit.
"""
import argparse
import json
import re
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
SITE = "https://toluwagbemiga.github.io"
CV_FILE = "Tolulope_Gbenga_CV.pdf"

# Which projects lead the grid, and how they're grouped.
FEATURED = {
    "Digital Twin: cost-aware memory agent (Qwen Hackathon)",
    "NexaCampus: school management suite for Betalean (in progress)",
    "Bivio: POS-integrated financial management app",
}
TAG_RULES = [
    ("AI & ML", r"\b(ai|llm|qwen|fraud|machine learning|memory agent)\b"),
    ("Mobile & fintech", r"\b(android|kotlin|compose|pos|banking|payments?|afripay|bivio)\b"),
    ("Web3", r"\b(web3|solidity|crypto|on-chain|paycircle|blockchain|paystack)\b"),
    ("Platforms & APIs", r"\b(saas|microservice|api|marketplace|platform|shortener|email marketing|school)\b"),
    ("Client sites", r"\b(website|wordpress|foundation|directory|legal|consult)\b"),
]


def tags_for(project: dict) -> list[str]:
    text = f"{project['name']} {project.get('description', '')} {' '.join(project.get('highlights', []))}".lower()
    found = [tag for tag, pattern in TAG_RULES if re.search(pattern, text)]
    return found or ["Platforms & APIs"]


def split_certification(text: str) -> dict:
    """"Name — Issuer, Date" -> parts, and flag ones that aren't earned yet."""
    name, _, meta = text.partition("—")
    scheduled = "scheduled" in text.lower()
    meta = re.sub(r"\(exam scheduled[^)]*\)", "", meta, flags=re.I).strip(" ,")
    return {"name": name.strip(), "meta": meta, "scheduled": scheduled}


def current_technical_company(experience: list[dict]) -> str:
    """The engineering job to name in the hero, not simply the newest row."""
    tech = re.compile(r"engineer|developer|qa|architect|founder", re.I)
    for role in experience:
        if role["end"].lower() in ("present", "current") and tech.search(role["title"]):
            return role["company"].split("(")[0].strip()
    return experience[0]["company"].split("(")[0].strip() if experience else ""


def build(profile: dict) -> str:
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    # keep the strongest few bullets per role: the CV carries the full list
    experience = [{**e, "highlights": e["highlights"][:4]} for e in profile["experience"] if e.get("highlights")]
    projects = sorted(
        ({**p, "tags": tags_for(p), "featured": p["name"] in FEATURED} for p in profile["public_projects"]),
        key=lambda p: (not p["featured"], p["name"]),
    )
    tags = ["All"] + sorted({t for p in projects for t in p["tags"]})
    summary = profile["summary"]
    sentences = re.split(r"(?<=\.)\s+", summary)
    about = [" ".join(sentences[:2]), " ".join(sentences[2:])] if len(sentences) > 2 else [summary]
    json_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": profile["name"],
            "jobTitle": profile["headline"],
            "email": f"mailto:{profile['contact']['email']}",
            "url": SITE,
            "address": {"@type": "PostalAddress", "addressLocality": profile["contact"]["location"]},
            "sameAs": [profile["contact"]["linkedin"], profile["contact"]["github"]],
            "knowsAbout": [i for g in profile["skills"] for i in g["items"]][:25],
        },
        indent=1,
    )
    return env.get_template("index.html.j2").render(
        p=profile,
        site=SITE,
        cv_file=CV_FILE,
        year=date.today().year,
        intro=sentences[0] if sentences else summary,
        meta_description=re.sub(r"\s+", " ", summary)[:180],
        about=[a for a in about if a],
        current_company=current_technical_company(experience),
        focus="Android, backend platforms and AI-assisted tooling",
        core_stack=["Kotlin", "Jetpack Compose", "Python", "FastAPI", "Laravel", "Next.js", "Go", "Solidity"],
        stats=[
            {"value": f"{profile['years_experience']}+", "label": "Years building software"},
            {"value": "2M+", "label": "Users on the banking app I ship for"},
            {"value": f"{len(profile['public_projects'])}", "label": "Public projects"},
        ],
        experience=experience,
        projects=projects,
        tags=tags,
        certifications=[split_certification(c) for c in profile["certifications"]],
        open_roles=", ".join(profile["open_to"]["roles"][:4]),
        json_ld=json_ld,
    )


def print_cv() -> None:
    import sys

    sys.path.insert(0, r"D:\development\job-bot\backend")
    from playwright.sync_api import sync_playwright

    from app.browser import launch  # the Edge fallback helper

    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page()
        page.goto((ROOT / "cv.html").as_uri(), wait_until="networkidle")
        page.pdf(path=str(ROOT / "assets" / CV_FILE), format="A4", print_background=True)
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", action="store_true", help="also re-print the CV PDF")
    args = parser.parse_args()
    profile = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
    (ROOT / "index.html").write_text(build(profile), encoding="utf-8")
    print("wrote index.html")
    if args.pdf:
        print_cv()
        print("wrote assets/" + CV_FILE)
