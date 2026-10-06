from __future__ import annotations

import json

from dqp.models import DatasetProfile


def render_text(profile: DatasetProfile) -> str:
    lines = [
        f"source: {profile.source}",
        f"rows: {profile.row_count}   columns: {profile.column_count}",
        "",
        f"{'column':<20}{'type':<10}{'nulls':>8}{'min':>12}{'max':>12}{'mean':>12}",
    ]
    for c in profile.columns:
        if c.numeric is not None:
            mn, mx, me = (f"{c.numeric.minimum:.2f}", f"{c.numeric.maximum:.2f}",
                         f"{c.numeric.mean:.2f}")
        else:
            mn = mx = me = "-"
        lines.append(
            f"{c.name:<20}{c.inferred_type.value:<10}{c.null_rate:>8.1%}"
            f"{mn:>12}{mx:>12}{me:>12}"
        )
    return "\n".join(lines)


def render_json(profile: DatasetProfile) -> str:
    payload = {
        "source": profile.source,
        "row_count": profile.row_count,
        "column_count": profile.column_count,
        "columns": [
            {
                "name": c.name,
                "type": c.inferred_type.value,
                "total_count": c.total_count,
                "null_count": c.null_count,
                "null_rate": round(c.null_rate, 4),
                "numeric": None if c.numeric is None else {
                    "min": c.numeric.minimum,
                    "max": c.numeric.maximum,
                    "mean": c.numeric.mean,
                },
            }
            for c in profile.columns
        ],
    }
    return json.dumps(payload, indent=2)
