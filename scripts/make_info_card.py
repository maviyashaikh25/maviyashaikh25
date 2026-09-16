#!/usr/bin/env python3
"""
Generate info-card.svg -- a neofetch-style dark terminal card for Maviya Shaikh.
"""
import os

STATIC = bool(os.environ.get("STATIC"))

HERE = os.path.dirname(__file__)
OUT_PATH = os.path.join(HERE, "..", "info-card.svg")

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

BG1 = "#0d1117"
BG2 = "#111722"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TITLE_TXT = "#8b949e"
TEXT = "#c9d1d9"
KEY = "#ffa657"
SEC = "#58a6ff"
GREEN = "#3fb950"
CYAN = "#39d3ee"

TITLEBAR_H = 34
PAD = 26
DOTS = ["#ff5f56", "#ffbd2e", "#27c93f"]

ROWS = [
    ("host",),
    ("kv", "Role", "AI Full Stack Intern @ Birbals Inc."),
    ("kv", "Education", "B.E. Computer Science (9.5 CGPA)"),
    ("kv", "Location", "Mumbai, India"),
    ("kv", "Email", "maviyaskh25@gmail.com"),
    ("kv", "GitHub", "/maviyashaikh25"),
    ("kv", "LinkedIn", "/in/maviyashk25"),
    ("kv", "LeetCode", "/u/maviya25 (200+ solved)"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "GenAI", "LangGraph, LangChain, RAG Pipelines, Multi-Agent Systems"),
    ("kv", "ML / DL", "PyTorch, Transformers, BERT Fine-tuning, SHAP, CNNs"),
    ("kv", "Backend", "FastAPI, Node.js, Express, PostgreSQL, Pinecone, FAISS"),
    ("kv", "Frontend", "React.js, Tailwind CSS, WebSockets"),
    ("kv", "DevOps", "Docker, AWS EC2, GitHub Actions, CI/CD, MLOps"),
    ("gap",),
    ("sec", "Focus"),
    ("bul", "Multi-agent systems, agentic RAG & low-latency LLM architectures"),
    ("bul", "Production full-stack AI engineering, microservices & scalable APIs"),
]

ROW_STEP = 26
GAP_STEP = 14
FS = 14
KEY_COL_X = 118

STAGGER = 0.12
FADE = 0.5


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def measure_height():
    y = TITLEBAR_H + 40
    for row in ROWS:
        if row[0] == "gap":
            y += GAP_STEP
        else:
            y += ROW_STEP
    return y + PAD


CANVAS_W = 660
CANVAS_H = measure_height()


def render():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="{FONT}">',
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" '
        f'stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]
    for i, dot in enumerate(DOTS):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TXT}" font-size="12" '
        f'text-anchor="middle">maviya@github: ~$ neofetch</text>'
    )

    y = TITLEBAR_H + 40
    idx = 0
    for row in ROWS:
        kind = row[0]
        if kind == "gap":
            y += GAP_STEP
            continue

        begin = idx * STAGGER
        idx += 1
        opacity0 = "1" if STATIC else "0"
        inner = []
        if kind == "host":
            inner.append(
                f'<text x="{PAD}" y="{y}" font-size="{FS}" font-weight="700">'
                f'<tspan fill="{GREEN}">maviya</tspan>'
                f'<tspan fill="{MUTED}">@</tspan>'
                f'<tspan fill="{CYAN}">github</tspan></text>'
            )
        elif kind == "kv":
            _, key, val = row
            inner.append(
                f'<text x="{PAD}" y="{y}" font-size="{FS}">'
                f'<tspan fill="{KEY}" font-weight="700">{esc(key)}</tspan>'
                f'<tspan fill="{MUTED}">:</tspan></text>'
            )
            inner.append(
                f'<text x="{PAD + KEY_COL_X}" y="{y}" font-size="{FS}" '
                f'fill="{TEXT}">{esc(val)}</text>'
            )
        elif kind == "sec":
            _, title = row
            inner.append(
                f'<text x="{PAD}" y="{y}" font-size="{FS}" fill="{SEC}" '
                f'font-weight="700">{esc(title)}</text>'
            )
            rule_x = PAD + KEY_COL_X - 40
            inner.append(
                f'<line x1="{rule_x}" y1="{y - 4}" x2="{CANVAS_W - PAD}" y2="{y - 4}" '
                f'stroke="{SEC}" stroke-opacity="0.35"/>'
            )
        elif kind == "bul":
            _, text = row
            inner.append(f'<circle cx="{PAD + 4}" cy="{y - 4}" r="3.5" fill="{GREEN}"/>')
            inner.append(
                f'<text x="{PAD + 16}" y="{y}" font-size="{FS}" '
                f'fill="{TEXT}">{esc(text)}</text>'
            )

        g = [f'<g opacity="{opacity0}">']
        if not STATIC:
            g.append(
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin:.2f}s" dur="{FADE}s" fill="freeze"/>'
            )
            g.append(
                f'<animateTransform attributeName="transform" type="translate" '
                f'from="0 5" to="0 0" begin="{begin:.2f}s" dur="{FADE}s" fill="freeze"/>'
            )
        g.extend(inner)
        g.append('</g>')
        parts.append("".join(g))
        y += ROW_STEP

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    svg = render()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    size = os.path.getsize(OUT_PATH)
    print(f"wrote {os.path.abspath(OUT_PATH)} ({size} bytes)")
