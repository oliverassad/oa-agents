#!/usr/bin/env python3
"""
Themed SVG figure verifier (Skill svg-figures)
Validates presentation SVGs against sanitiser and slide presentation constraints.
"""

import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

STANDARD_VIEWBOXES = {
    (1600, 900): "16:9 Standard Slide",
    (2100, 900): "21:9 Wide Pipeline",
    (1200, 900): "4:3 Single Focus",
    (900, 900): "1:1 Badge / Icon",
}

FORBIDDEN_TAGS = {"script", "foreignobject", "iframe"}

FLOOR = 24
SIZE_RE = re.compile(r"\s*(\d+(?:\.\d+)?)(?:px)?\s*")


def local(el) -> str:
    return el.tag.split("}")[-1].lower()


def check_root(tree, errors, warnings):
    if local(tree) != "svg":
        errors.append(f"Root element must be <svg>, found <{local(tree)}>")
    for a in ("width", "height"):
        if a in tree.attrib:
            errors.append(f"Root <svg> must NOT set '{a}' attribute (found: {tree.attrib[a]}). Slide viewer sizes dynamically.")
    viewbox = tree.attrib.get("viewBox", "")
    parts = [float(x) for x in re.split(r"[\s,]+", viewbox.strip()) if x]
    if len(parts) != 4:
        errors.append(f"Missing or invalid viewBox attribute: '{viewbox}'")
    elif (int(parts[2]), int(parts[3])) not in STANDARD_VIEWBOXES:
        warnings.append(f"Non-standard viewBox '{viewbox}'. Recommended heights are 900 units: 1600x900, 2100x900, 1200x900, or 900x900.")
    if not any(local(el) == "title" for el in tree):
        warnings.append("Missing <title> child element in root <svg> (Rule 6).")
    return viewbox


def check_forbidden(tree, errors):
    for el in tree.iter():
        t = local(el)
        if t in FORBIDDEN_TAGS:
            errors.append(f"Forbidden element <{t}> detected (Rule 12).")
        for attr, val in el.attrib.items():
            if attr.lower().startswith("on"):
                errors.append(f"Forbidden event handler '{attr}' on <{t}> (Rule 12).")
            if "javascript:" in val.lower():
                errors.append(f"Forbidden javascript URI in {attr}='{val}' (Rule 12).")


def check_urls_css(raw, errors, warnings):
    urls = re.findall(r'https?://[^\s"\'<>)]+', raw)
    ext = [u for u in urls if not any(ns in u for ns in ["w3.org/2000/svg", "w3.org/1999/xlink"])]
    if ext:
        errors.append(f"Forbidden external resources detected: {ext[:3]} (Rule 13).")
    if re.search(r":root\s*\{", raw):
        errors.append("Do NOT declare ':root' block in SVG. Tokens come from page ground (Rule 3).")
    if re.search(r"(@font-face|\bposition\s*:\s*fixed|\bz-index\b)", raw):
        errors.append("Forbidden CSS detected (@font-face, position: fixed, or z-index) (Rules 8, 16).")
    naked = re.findall(r"var\(\s*(--[a-zA-Z0-9_-]+)\s*\)", raw)
    if naked:
        warnings.append(f"Variables missing fallback: {list(set(naked))[:4]}. Use var(--token, fallback) (Rule 2).")


def check_paint(raw, errors):
    for i, line in enumerate(raw.splitlines(), 1):
        hexes = re.findall(r"#[0-9a-fA-F]{3,8}\b", re.sub(r"var\([^)]+\)", "", line))
        if hexes and ":root" not in line:
            errors.append(f"Line {i}: Raw hex color '{hexes[0]}' used without var(--token, fallback) (Rule 1).")
            return
    if re.search(r'<rect[^>]+width=["\']100%["\'][^>]+height=["\']100%["\']', raw):
        errors.append("Opaque background <rect width='100%' height='100%'> forbidden. Canvas must be transparent (Rule 18).")
    if ("@keyframes" in raw or "<animate" in raw) and "prefers-reduced-motion" not in raw:
        errors.append("Animation present but missing '@media (prefers-reduced-motion: reduce)' guard (Rule 10).")


def parse_size(value, errors):
    m = SIZE_RE.fullmatch(value)
    if not m:
        errors.append(f"Unparseable font-size '{value.strip()}': use a plain number or px (Rule 28).")
        return None
    return float(m.group(1))


def font_sizes(text_elements, raw, errors):
    values = [el.attrib["font-size"] for el in text_elements if "font-size" in el.attrib]
    values += re.findall(r"font-size:\s*([^;}\"'<]+)", raw)
    return [n for n in (parse_size(v, errors) for v in values) if n is not None]


def check_text(tree, raw, errors, warnings):
    texts = [el for el in tree.iter() if local(el) == "text"]
    if len(texts) > 8:
        warnings.append(f"Text count is {len(texts)} (Rule 27 recommends at most 8 text items per slide figure).")
    for el in texts:
        content = "".join(el.itertext()).strip()
        if len(content.split()) > 4:
            warnings.append(f"Text '{content[:20]}...' has {len(content.split())} words (Rule 27 recommends max 4 words per label).")
    sizes = font_sizes(texts, raw, errors)
    if sizes and min(sizes) < FLOOR:
        errors.append(f"Smallest font size is {min(sizes)} units (Rule 28: minimum {FLOOR} units floor for slide presentation).")
    return len(texts), sizes


def report(path, viewbox, count, sizes, errors, warnings):
    status = "FAIL" if errors else ("PASS (WITH WARNINGS)" if warnings else "PASS (CLEAN)")
    print(f"\n{'=' * 55}\nVERIFICATION REPORT: {path.name}\n{'=' * 55}")
    print(f"ViewBox:        {viewbox or 'NONE'}")
    print(f"Text Items:     {count}")
    print(f"Min Font Size:  {min(sizes) if sizes else 'N/A'} units")
    print(f"Status:         {status}\n{'-' * 55}")
    for title, items, mark in (("ERRORS (Must fix):", errors, "[X]"), ("WARNINGS (Advisory):", warnings, "[!]")):
        if items:
            print(title)
            print("\n".join(f"  {mark} {m}" for m in items))
    if not errors and not warnings:
        print("All svg-figures rules satisfied.")
    print(f"{'=' * 55}\n")


def verify_svg(filepath: str) -> bool:
    if filepath in ("-h", "--help"):
        print("Usage: python3 verify_svg.py <path/to/figure.svg>")
        return True
    path = Path(filepath)
    if not path.is_file():
        print(f"FAIL: File not found: {filepath}")
        return False
    raw = path.read_text(encoding="utf-8")
    try:
        tree = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"FAIL: XML Parse Error in {filepath}: {e}")
        return False
    errors, warnings = [], []
    viewbox = check_root(tree, errors, warnings)
    check_forbidden(tree, errors)
    check_urls_css(raw, errors, warnings)
    check_paint(raw, errors)
    count, sizes = check_text(tree, raw, errors, warnings)
    report(path, viewbox, count, sizes, errors, warnings)
    return not errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify_svg.py <path/to/figure.svg>")
        sys.exit(1)
    sys.exit(0 if verify_svg(sys.argv[1]) else 1)
