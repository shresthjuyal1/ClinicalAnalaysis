"""Generate the README figures from the fitted SAS model estimates.

Uses only the Python standard library and writes SVG files to figures/.
All numbers are taken directly from results/sas_output.pdf.

    python3 scripts/make_figures.py
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures"

FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
INK = "#1f2328"
MUTED = "#656d76"
GRID = "#d0d7de"
ACCENT = "#cf222e"  # significant at alpha = 0.05
NEUTRAL = "#57606a"

# Full model: (label, odds ratio, 95% lower, 95% upper, p-value)
ODDS_RATIOS = [
    ("Bird keeping (yes vs. no)", 3.906, 1.745, 8.747, 0.0009),
    ("Years smoked (+1 year)", 1.076, 1.021, 1.133, 0.0059),
    ("Cigarettes per day (+1)", 1.026, 0.976, 1.079, 0.3081),
    ("Age (+1 year)", 0.961, 0.896, 1.030, 0.2626),
    ("Sex (female vs. male)", 1.753, 0.619, 4.964, 0.2907),
    ("SES (high vs. low)", 1.111, 0.443, 2.785, 0.8221),
]

# Logistic model coefficients (full model)
B0, B_SEX, B_BIRD, B_AGE, B_YRS, B_CIG = -1.9375, 0.5613, 1.3626, -0.0398, 0.0729, 0.0260
MEAN_AGE = 56.9659864
MEAN_CIGS = 15.7482993


def svg_doc(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">\n'
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>\n'
        f"{body}</svg>\n"
    )


def text(x, y, s, size=13, fill=INK, anchor="start", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>\n'
    )


def forest_plot():
    width, height = 820, 400
    left, right = 230, 640  # plot area x-range
    top, row_h = 88, 44
    lo, hi = 0.25, 16.0  # log-scale axis limits

    def x_of(v):
        return left + (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo)) * (right - left)

    body = text(24, 34, "Adjusted odds ratios for lung cancer (full model)", 18, weight="600")
    body += text(24, 56, "Points are odds ratios; bars are 95% Wald confidence intervals. Log scale.", 12, MUTED)

    axis_y = top + row_h * len(ODDS_RATIOS)
    for tick in (0.25, 0.5, 1, 2, 4, 8, 16):
        x = x_of(tick)
        dash = "" if tick == 1 else ' stroke-dasharray="2,4"'
        color = INK if tick == 1 else GRID
        body += f'<line x1="{x:.1f}" y1="{top - 14}" x2="{x:.1f}" y2="{axis_y}" stroke="{color}"{dash}/>\n'
        label = f"{tick:g}"
        body += text(x, axis_y + 18, label, 12, MUTED, "middle")
    body += text((left + right) / 2, axis_y + 40, "Odds ratio", 12, MUTED, "middle")
    body += text(x_of(1) - 6, top - 20, "&#8592; lower odds", 11, MUTED, "end")
    body += text(x_of(1) + 6, top - 20, "higher odds &#8594;", 11, MUTED, "start")

    body += text(right + 24, top - 20, "OR (95% CI)", 11, MUTED, weight="600")
    for i, (label, or_, l, u, p) in enumerate(ODDS_RATIOS):
        y = top + row_h * i + row_h / 2 - 8
        color = ACCENT if p < 0.05 else NEUTRAL
        weight = "600" if p < 0.05 else "normal"
        body += text(left - 16, y + 4, label, 13, INK, "end", weight)
        body += f'<line x1="{x_of(l):.1f}" y1="{y}" x2="{x_of(u):.1f}" y2="{y}" stroke="{color}" stroke-width="2.5"/>\n'
        body += f'<circle cx="{x_of(or_):.1f}" cy="{y}" r="6" fill="{color}"/>\n'
        body += text(right + 24, y + 4, f"{or_:.2f} ({l:.2f}&#8211;{u:.2f})", 12, color, weight=weight)

    body += f'<circle cx="30" cy="{height - 22}" r="5" fill="{ACCENT}"/>\n'
    body += text(42, height - 18, "p &lt; 0.05", 12, MUTED)
    body += f'<circle cx="118" cy="{height - 22}" r="5" fill="{NEUTRAL}"/>\n'
    body += text(130, height - 18, "not significant", 12, MUTED)
    return svg_doc(width, height, body)


def predicted_probability(years_smoked, bird):
    """Woman of average age and low SES who smokes the sample-average
    number of cigarettes per day."""
    eta = B0 + B_SEX + B_BIRD * bird + B_AGE * MEAN_AGE + B_YRS * years_smoked + B_CIG * MEAN_CIGS
    return 1 / (1 + math.exp(-eta))


def probability_curve():
    width, height = 820, 420
    left, right, top, bottom = 80, 600, 80, 350
    x_max, y_max = 50, 1.0

    def px(v):
        return left + v / x_max * (right - left)

    def py(v):
        return bottom - v / y_max * (bottom - top)

    body = text(24, 34, "Predicted probability of lung cancer vs. years smoked", 18, weight="600")
    body += text(24, 56, "Woman of average age (57), low SES, smoking the sample mean of 15.7 cigarettes/day. Full model.", 12, MUTED)

    for yv in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        y = py(yv)
        body += f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}"/>\n'
        body += text(left - 10, y + 4, f"{yv:.0%}", 12, MUTED, "end")
    for xv in range(0, 51, 10):
        body += text(px(xv), bottom + 20, str(xv), 12, MUTED, "middle")
    body += text((left + right) / 2, bottom + 44, "Years smoked", 12, MUTED, "middle")

    for bird, color, label in ((1, ACCENT, "Keeps birds"), (0, NEUTRAL, "No birds")):
        pts = [(px(t), py(predicted_probability(t, bird))) for t in range(0, x_max + 1)]
        d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
        body += f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3"/>\n'
        p50 = predicted_probability(x_max, bird)
        body += text(right + 12, py(p50) + 4, f"{label}: {p50:.0%}", 13, color, weight="600")
        body += f'<circle cx="{px(x_max):.1f}" cy="{py(p50):.1f}" r="4" fill="{color}"/>\n'

    body += text(right + 12, py(0.5) + 4, "at 50 years", 12, MUTED)
    return svg_doc(width, height, body)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "odds_ratios.svg").write_text(forest_plot())
    (OUT / "predicted_probability.svg").write_text(probability_curve())
    print(f"Wrote figures to {OUT}")


if __name__ == "__main__":
    main()
