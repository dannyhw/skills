#!/usr/bin/env python3
"""Deterministic counter for the mechanical rules of british-plain-english.

Counts what a regex can catch: US spellings, negative contractions,
should/may/might, eg/ie/etc, semicolons, em dashes, "please", long sentences
and paragraphs, US-style dates and times, capitalised bullets, title-case and
question headings, bold, and AI-overused words. Code blocks, inline code and
URLs are removed first, so identifiers such as `color` never count.

It is a regex pass, not a parser. It cannot see passive voice, front-loading,
or whether a term was explained. Compare 2 texts with the same version of this
file. Do not read a score as a quality verdict.

Usage:
  python3 lint.py doc.md
  python3 lint.py --reply reply.txt
  cat text.md | python3 lint.py -
  python3 lint.py --self-test
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
APOS = "['’]"

# --- US spelling -----------------------------------------------------------
IZE = re.compile(r"\b([a-z]+?)(iz|yz)(e|es|ed|ing|ation|ations|er|ers|able)\b", re.I)
IZE_OK = {"s", "pr", "se", "caps", "ma", "ba", "res", "downs", "overs", "unders",
          "outs", "ups", "ups", "oversi", "cit", "w", "fr", "gr", "bl"}
US_WORDS = re.compile(r"\b(" + "|".join([
    r"colou?r(?<!colour)(s|ed|ful|ing)?", r"behavior(s|al)?", r"favor(s|ed|ite|ites|able)?",
    r"honor(s|ed)?", r"labor(s|ed)?", r"neighbor(s|hood)?", r"flavor(s|ed)?", r"humor",
    r"cent(er|ers|ered)", r"(lit|fib|theat)er(s)?", r"catalog(s|ed)?", r"defense", r"offense",
    r"(cancel|label|model|travel|signal|fuel|level|tunnel)(ed|ing|er|ers)",
    r"enrollment", r"fulfill(ment|s)?", r"skillful(ly)?", r"gray", r"aluminum", r"skeptic(al|ism)?",
    r"judgment", r"acknowledgment", r"toward", r"afterward", r"gotten", r"math",
    r"pediatric", r"maneuver(s)?", r"anesthe\w+", r"artifact(s)?", r"program(s)? of", r"programs? for (staff|users|customers)",
]) + r")\b", re.I)
# "license" as a noun: after a determiner or before a common noun-follower
LICENSE_NOUN = re.compile(r"\b(a|the|your|this|our|MIT|software|open[- ]source|valid|new)\s+license(s)?\b|\blicense\s+(key|file|fee|holder|terms|agreement)s?\b", re.I)

# --- grammar and punctuation ---------------------------------------------
NEG_CONTRACTION = re.compile(rf"\b\w+n{APOS}t\b|\b(should|could|would|must|might){APOS}ve\b", re.I)
MODAL = re.compile(r"\b(should|may|might)\b", re.I)
LATIN = re.compile(r"\b(e\.g\.|i\.e\.|etc\.?|eg|ie)(?=[\s,):;]|$)", re.I)
SEMICOLON = re.compile(r";")
EM_DASH = re.compile(r"—|(?<= )--(?= )")
PLEASE = re.compile(r"\b(please|kindly)\b", re.I)
MONTHS = r"(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sep(t|tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)"
US_DATE = re.compile(rf"\b{MONTHS}\s+\d{{1,2}}(st|nd|rd|th)?(,?\s+\d{{4}})?\b|\b\d{{1,2}}(st|nd|rd|th)\s+(of\s+)?{MONTHS}\b|\b{MONTHS}\s+\d{{1,2}}(st|nd|rd|th)?\b")
US_TIME = re.compile(r"\b\d{1,2}(:\d{2})?\s?(AM|PM|A\.M\.|P\.M\.|a\.m\.|p\.m\.)|\b\d{1,2}(:\d{2})?\s+(am|pm)\b|(?<![:\d])\b12\s?(noon|pm|am)\b|\b12\s?(NOON|Noon)\b")
BOLD = re.compile(r"\*\*[^*\n]+\*\*|__[^_\n]+__")
HEADER = re.compile(r"^\s*#{1,6}\s+(.*)$", re.M)
BULLET = re.compile(r"^\s*[-*+]\s+(.*)$", re.M)
NUMBERED = re.compile(r"^\s*\d+[.)]\s+", re.M)

OPENER = re.compile(r"^\s*\W*(certainly|great question|sure[,!]|absolutely|good question|happy to|of course)", re.I)
CLOSER = re.compile(r"(i hope this helps|let me know|feel free to|happy to help)", re.I)

GOVUK_AVOID = [
    "leverage", "utilise", "utilize", "empower", "facilitate", "streamline", "liaise",
    "incentivise", "disincentivise", "overarching", "going forward", "moving forward",
    "in order to", "one-stop shop", "ring-fenc", "robust", "seamless", "ensure",
    "prior to", "purchase", "assist", "approximately", "commence", "initiate",
]


def slop_pattern():
    terms = list(GOVUK_AVOID)
    tsv = HERE / "slop.tsv"
    if tsv.exists():
        for line in tsv.read_text(encoding="utf-8").splitlines():
            term = line.split("\t")[0].strip().lower()
            if term:
                terms.append(term)
    alts = sorted({re.escape(t).replace(r"\ ", r"\s+") for t in terms}, key=len, reverse=True)
    return re.compile(r"\b(" + "|".join(alts) + r")\w*", re.I)


SLOP = slop_pattern()
SMALL = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "by", "at", "from", "vs"}


def strip_code(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\A---\n.*?\n---\n", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", "CODESPAN", text)
    text = re.sub(r"https?://\S+", "URL", text)
    text = re.sub(r"^\s*\|[\s:|-]+\|\s*$", "", text, flags=re.M)
    return text


def us_spellings(prose):
    hits = []
    for m in IZE.finditer(prose):
        stem = m.group(1).lower()
        if stem in IZE_OK or m.group(0).lower().startswith(("citizen", "wizard", "frizz", "prize", "seize", "size")):
            continue
        hits.append(m.group(0))
    hits += [m.group(0) for m in US_WORDS.finditer(prose)]
    hits += [m.group(0) for m in LICENSE_NOUN.finditer(prose)]
    return hits


def prose_lines(prose):
    """Body text with headings removed and list markers stripped."""
    out = re.sub(r"^\s*#{1,6}\s.*$", "", prose, flags=re.M)
    out = re.sub(r"^\s*([-*+]|\d+[.)])\s+(.*?)\s*$", lambda m: m.group(2) + ("" if m.group(2).endswith((".", ":", "?", "!")) else ".") , out, flags=re.M)
    out = re.sub(r"^\s*>\s?", "", out, flags=re.M)
    out = re.sub(r"^\s*\|(.*)\|\s*$", lambda m: ". ".join(c.strip() for c in m.group(1).split("|") if c.strip()) + ".", out, flags=re.M)
    return out


def sentences(body):
    parts = re.split(r"(?<=[.!?])[\"'’)\]]*\s+|\n{2,}|\n(?=\S)", body)
    return [p.strip() for p in parts if len(p.strip().split()) >= 2]


def heading_issues(prose):
    title_case, question = [], []
    for m in HEADER.finditer(prose):
        h = m.group(1).strip().rstrip("#").strip()
        if h.endswith("?"):
            question.append(h)
        words = [w for w in re.findall(r"[A-Za-z][\w'-]*", h)][1:]
        caps = [w for w in words if w[0].isupper() and not w.isupper() and w.lower() not in SMALL]
        if len(words) >= 2 and len(caps) >= 2:
            title_case.append(h)
    return title_case, question


def bullet_caps(prose):
    hits = []
    for m in BULLET.finditer(prose):
        item = m.group(1).strip()
        first = re.match(r"[A-Za-z][\w'-]*", item)
        if first and first.group(0)[0].isupper() and not first.group(0).isupper() and not item.startswith("CODESPAN"):
            hits.append(item[:60])
    return hits


def lint(text, reply=False):
    prose = strip_code(text)
    body = prose_lines(prose)
    sents = sentences(body)
    paras = [prose_lines(p) for p in re.split(r"\n\s*\n", prose)
             if p.strip() and not (BULLET.search(p) or NUMBERED.search(p) or HEADER.search(p) or p.lstrip().startswith(("|", ">")))]
    title_case, question = heading_issues(prose)
    hits = {
        "us_spelling": us_spellings(prose),
        "negative_contraction": [m.group(0) for m in NEG_CONTRACTION.finditer(prose)],
        "should_may_might": [m.group(0) for m in MODAL.finditer(prose)],
        "eg_ie_etc": [m.group(0) for m in LATIN.finditer(prose)],
        "semicolon": [m.group(0) for m in SEMICOLON.finditer(body)],
        "em_dash": [m.group(0) for m in EM_DASH.finditer(prose)],
        "please": [m.group(0) for m in PLEASE.finditer(prose)],
        "us_date_or_time": [m.group(0) for m in US_DATE.finditer(prose)] + [m.group(0) for m in US_TIME.finditer(prose)],
        "sentence_over_25": [s[:70] for s in sents if len(s.split()) > 25],
        "paragraph_over_5": [p[:50] for p in paras if len(sentences(p)) > 5],
        "slop_word": [m.group(0) for m in SLOP.finditer(prose)],
        "bold": [m.group(0) for m in BOLD.finditer(prose)],
        "title_case_heading": title_case,
        "question_heading": question,
        "bullet_capital": bullet_caps(prose),
    }
    if reply:
        hits["header"] = [m.group(0).strip() for m in HEADER.finditer(prose)]
        hits["bullet"] = [m.group(0).strip()[:40] for m in BULLET.finditer(prose)]
        hits["opener"] = [m.group(0) for m in OPENER.finditer(prose)]
        hits["closer"] = [m.group(0) for m in CLOSER.finditer(prose)]
        for k in ("title_case_heading", "question_heading", "bullet_capital"):
            hits.pop(k)
    words = max(1, len(re.findall(r"\b\w[\w'-]*\b", body)))
    counts = {k: len(v) for k, v in hits.items()}
    total = sum(counts.values())
    return {"words": words, "sentences": len(sents), "counts": counts, "total": total,
            "per_100w": round(100 * total / words, 2), "hits": hits}


SLOP_DOC = """## Getting Started With Sqlpipe

Please note you should initialize the color settings — it's a robust way to leverage the organization's behavior; e.g. the canceled jobs.

- Install the license key
- Run it on June 3rd, 2026 at 5:30 PM

You can't skip this.
"""

CLEAN_DOC = """## Get started with sqlpipe

Set `color_mode` in the configuration before you run `initialize`. You can change it later.

You need:

- a licence key from the dashboard
- access to the organisation account

1. Run the job on 3 June 2026 at 5:30pm.
2. If the job is cancelled, start it again.

You cannot skip this step.
"""


def self_test():
    bad = lint(SLOP_DOC)["counts"]
    good = lint(CLEAN_DOC)["counts"]
    for k in ("us_spelling", "negative_contraction", "should_may_might", "eg_ie_etc", "semicolon",
              "em_dash", "please", "us_date_or_time", "slop_word", "title_case_heading", "bullet_capital"):
        assert bad[k] >= 1, (k, bad)
    assert bad["us_spelling"] >= 5, lint(SLOP_DOC)["hits"]["us_spelling"]
    assert sum(good.values()) == 0, lint(CLEAN_DOC)["hits"]
    r = lint("**Yes** — it is bad.\n\n## Why\n- Lag grows.\n\nI hope this helps!", reply=True)["counts"]
    assert r["bold"] == 1 and r["em_dash"] == 1 and r["header"] == 1 and r["bullet"] == 1 and r["closer"] == 1, r
    print("self-test passed")


def main(argv):
    if "--self-test" in argv:
        return self_test()
    reply = "--reply" in argv
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    text = sys.stdin.read() if not paths or paths[0] == "-" else pathlib.Path(paths[0]).read_text(encoding="utf-8")
    res = lint(text, reply=reply)
    if as_json:
        print(json.dumps(res, indent=1))
        return
    print(f"{res['words']} words, {res['sentences']} sentences, {res['total']} hits ({res['per_100w']}/100 words)")
    for k, v in res["hits"].items():
        if v:
            print(f"  {k}: {len(v)}  " + " | ".join(dict.fromkeys(str(x) for x in v[:6])))


if __name__ == "__main__":
    main(sys.argv[1:])
