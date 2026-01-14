from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from jinja2 import Template


HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Syncy Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    .summary { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
    .card { padding: 1rem; border: 1px solid #ddd; border-radius: 6px; min-width: 12rem; background: #fff; }
    .fail { color: #b30000; font-weight: 600; }
    .pass { color: #0a7f00; font-weight: 600; }
    .muted { color: #666; font-size: 0.9em; }
    .actions { margin: 0 0 1rem 0; display:flex; gap:.75rem; align-items:center; }
    .btn { display:inline-block; padding:.4rem .7rem; border:1px solid #ddd; border-radius:6px; background:#f7f7f7; color:#222; text-decoration:none; cursor:pointer; }
    .btn:hover { background:#eee; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 1.5rem; border: 1px solid #c8c8c8; }
    th, td { border: 1px solid #c8c8c8; padding: 0.5rem; text-align: left; vertical-align: top; }
    th { background: #f2f2f2; }
    .badge { display: inline-block; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.85em; margin-right: 0.25rem; background: #f0f2f4; color: #333; border: 1px solid #d9d9d9; }
    .section-header { display:flex; align-items:center; gap:.5rem; }
    .toggle { cursor:pointer; color:#0366d6; font-size: .95em; }
    .kv { margin-top: .25rem; }
    .kv code { background:#f6f8fa; padding:.1rem .3rem; border:1px solid #eee; border-radius:4px; }
    .tables-two { display:flex; gap:1rem; flex-wrap:wrap; }
    .subcard { flex:1 1 18rem; border:1px solid #ddd; border-radius:6px; padding:.5rem; background:#fff; }
    .subcard h3 { margin-top:0; }

    /* Print-friendly adjustments */
    @media print {
      .actions, .toggle { display:none !important; }
      a { text-decoration:none; color:#000; }
      body { margin: 0.5in; }
      th, td { border: 1px solid #ccc; }
    }
  </style>
  <script>
    function toggle(id){
      var x = document.getElementById(id);
      x.style.display = (x.style.display === 'none') ? 'block' : 'none';
    }
  </script>
  </head>
<body>
  <h1>Syncy Report</h1>

  <div class="actions">
    <button class="btn" onclick="window.print()">Save as PDF</button>
    <a class="btn" href="summary.json" download>Download JSON</a>
  </div>

  <div class="summary">
    <div class="card"><strong>Status</strong><div class="{{ status_class }}">{{ status }}</div></div>
    <div class="card"><strong>Coverage</strong><div>{{ coverage_pct }}% ({{ compared }}/{{ total }})</div></div>
    <div class="card"><strong>Findings</strong><div>Rules: {{ rule_hits }} &nbsp; Mismatch: {{ mismatches }} &nbsp; Missing: {{ missing }}</div></div>
    <div class="card"><strong>Thresholds</strong><div>{{ thresholds_status }}</div>{% if thresholds_reasons %}<div class="kv"><em>Reasons:</em> {{ thresholds_reasons }}</div>{% endif %}</div>
  </div>

  <div class="section-header">
    <h2>Overview</h2>
    <span class="toggle" onclick="toggle('overview')">show/hide</span>
  </div>
  <div id="overview">
    <p class="muted">Connection context, schema scope, behaviour settings, and threshold configuration for this run.</p>
    <table>
      <tbody>
        <tr><th>Source Database</th><td>{{ source_engine }}{% if source_version %} — <span class="muted">{{ source_version }}</span>{% endif %}</td></tr>
        <tr><th>Target Database</th><td>{{ target_engine }}{% if target_version %} — <span class="muted">{{ target_version }}</span>{% endif %}</td></tr>
        <tr><th>Source URL</th><td><code>{{ source_url }}</code></td></tr>
        <tr><th>Target URL</th><td><code>{{ target_url }}</code></td></tr>
        <tr><th>Include Schemas</th><td>{{ include_schemas or '-' }}</td></tr>
        <tr><th>Exclude Schemas</th><td>{{ exclude_schemas or '-' }}</td></tr>
        <tr><th>Behaviour</th><td>Row limit: {{ behaviour_limit }}; Timeout: {{ behaviour_timeout_s }}s</td></tr>
        <tr><th>Thresholds Config</th><td>Fail on findings: {{ fail_on_findings }}; Min coverage: {{ min_coverage }}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="section-header">
    <h2>Findings</h2>
    <span class="toggle" onclick="toggle('findings')">show/hide</span>
  </div>
  <div id="findings">
    <p class="muted">Per-object validation status. Rule badges indicate detected cross-engine differences; hover to see a description and fix hint.</p>
    <table>
      <thead>
        <tr><th>Object</th><th>Status</th><th>Rules</th></tr>
      </thead>
      <tbody>
        {{ rows | safe }}
      </tbody>
    </table>
  </div>

  {% if legend_rows %}
  <div class="section-header">
    <h2>Rule Legend</h2>
    <span class="toggle" onclick="toggle('legend')">show/hide</span>
  </div>
  <div id="legend">
    <p class="muted">Rules encountered in this run, with practical guidance on how to resolve them.</p>
    <table>
      <thead>
        <tr><th>Rule</th><th>Description</th><th>Hint</th></tr>
      </thead>
      <tbody>
        {{ legend_rows | safe }}
      </tbody>
    </table>
  </div>
  {% endif %}

  <div class="section-header">
    <h2>Objects</h2>
    <span class="toggle" onclick="toggle('objects')">show/hide</span>
  </div>
  <div id="objects">
    <p class="muted">Inventory of all discovered objects. "missing_in_target" means source-only; "missing_in_source" means target-only.</p>
    <div class="tables-two">
      <div class="subcard">
        <h3>Source</h3>
        <table>
          <thead><tr><th>Object</th><th>Status</th></tr></thead>
          <tbody>
            {{ source_objects_rows | safe }}
          </tbody>
        </table>
      </div>
      <div class="subcard">
        <h3>Target</h3>
        <table>
          <thead><tr><th>Object</th><th>Status</th></tr></thead>
          <tbody>
            {{ target_objects_rows | safe }}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  {% if behaviour_rows %}
  <div class="section-header">
    <h2>Behaviour</h2>
    <span class="toggle" onclick="toggle('behaviour')">show/hide</span>
  </div>
  <div id="behaviour">
    <p class="muted">Read-only sampling for views. Compares shape (column counts) and a small sample of rows between source and target.</p>
    <table>
      <thead>
        <tr><th>Object</th><th>Status</th><th>Source rows</th><th>Target rows</th><th>Source cols</th><th>Target cols</th></tr>
      </thead>
      <tbody>
        {{ behaviour_rows | safe }}
      </tbody>
    </table>
  </div>
  {% endif %}

  <p class="muted">Generated by Syncy v{{ version }} at {{ runtime }}</p>
</body>
</html>
"""


def generate_reports(results: Dict[str, Any], out_dir: Path) -> None:
    """Write JSON summary and simple HTML dashboard to the output directory."""
    # JSON
    summary_path = out_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # HTML
    coverage = results.get("coverage", {})
    finding_counts = results.get("finding_counts", {}) or {}
    thresholds = results.get("thresholds", {}) or {}

    def badge(rule: Dict[str, Any]) -> str:
        rid = rule.get("id", "?")
        desc = rule.get("desc", "")
        hint = rule.get("hint", "")
        title = desc if not hint else f"{desc} — {hint}"
        return f"<span class=\"badge\" title=\"{title}\">{rid}</span>"

    def fmt_row(obj_key: str, item: Dict[str, Any]) -> str:
        status = item.get("status", "?")
        rules = item.get("rules", []) or []
        if rules:
            rule_str = " ".join(badge(r) for r in rules)
        else:
            rule_str = "-"
        return f"<tr><td>{obj_key}</td><td>{status}</td><td>{rule_str}</td></tr>"

    # Findings rows and legend
    rows = []
    legend: Dict[str, Dict[str, Any]] = {}
    source_inventory: List[str] = []
    target_inventory: List[str] = []
    for k, v in (results.get("findings", {}) or {}).items():
        rows.append(fmt_row(k, v))
        for r in (v.get("rules") or []):
            rid = r.get("id")
            if not rid:
                continue
            legend[rid] = {
                "desc": r.get("desc", ""),
                "hint": r.get("hint", ""),
            }
        status = v.get("status", "?")
        # Source inventory: everything except target-only
        if status != "missing_in_source":
            source_inventory.append(f"<tr><td>{k}</td><td>{status}</td></tr>")
        # Target inventory: everything except source-only
        if status != "missing_in_target":
            target_inventory.append(f"<tr><td>{k}</td><td>{status}</td></tr>")

    legend_rows: List[str] = []
    for rid in sorted(legend.keys()):
        rinfo = legend[rid]
        legend_rows.append(
            f"<tr><td><span class=\"badge\">{rid}</span></td><td>{rinfo.get('desc','')}</td><td>{rinfo.get('hint','')}</td></tr>"
        )

    # Behaviour rows
    behaviour_rows: List[str] = []
    for k, v in (results.get("behaviour", {}) or {}).items():
        behaviour_rows.append(
            f"<tr><td>{k}</td><td>{v.get('status','?')}</td><td>{v.get('src_rows',0)}</td>"
            f"<td>{v.get('tgt_rows',0)}</td><td>{v.get('src_cols',0)}</td><td>{v.get('tgt_cols',0)}</td></tr>"
        )

    # Threshold display
    reasons = thresholds.get("fail_reasons") or []
    thresholds_status = (
        "OK" if not reasons else ("Failed: " + "; ".join(str(x) for x in reasons))
    )

    status = results.get("status", "unknown")
    template = Template(HTML_TEMPLATE)
    html = template.render(
        status=status,
        status_class="pass" if status == "pass" else "fail",
        coverage_pct=round(coverage.get("coverage_pct", 0.0), 2),
        compared=coverage.get("compared_objects", 0),
        total=coverage.get("total_objects", 0),
        rule_hits=finding_counts.get("rule_hits", 0),
        mismatches=finding_counts.get("mismatches", 0),
        missing=finding_counts.get("missing", 0),
        thresholds_status=thresholds_status,
        thresholds_reasons=", ".join(str(x) for x in reasons) if reasons else "",
        rules_source=results.get("rules_source", ""),
        source_url=results.get("source_url", ""),
        target_url=results.get("target_url", ""),
        source_engine=(results.get("source_info", {}) or {}).get("engine", ""),
        source_version=(results.get("source_info", {}) or {}).get("version", ""),
        target_engine=(results.get("target_info", {}) or {}).get("engine", ""),
        target_version=(results.get("target_info", {}) or {}).get("version", ""),
        include_schemas=", ".join(results.get("params", {}).get("include_schemas", []) or []) if isinstance((results.get("params", {}).get("include_schemas")), list) else (results.get("params", {}).get("include_schemas") or ""),
        exclude_schemas=", ".join(results.get("params", {}).get("exclude_schemas", []) or []) if isinstance((results.get("params", {}).get("exclude_schemas")), list) else (results.get("params", {}).get("exclude_schemas") or ""),
        behaviour_limit=results.get("params", {}).get("behaviour_limit", ""),
        behaviour_timeout_s=results.get("params", {}).get("behaviour_timeout_s", ""),
        fail_on_findings=thresholds.get("fail_on_findings", ""),
        min_coverage=thresholds.get("min_coverage", ""),
        rows="\n".join(rows),
        legend_rows="\n".join(legend_rows),
        behaviour_rows="\n".join(behaviour_rows),
        source_objects_rows="\n".join(source_inventory) or "<tr><td colspan='2'>None</td></tr>",
        target_objects_rows="\n".join(target_inventory) or "<tr><td colspan='2'>None</td></tr>",
        version=results.get("version", ""),
        runtime=results.get("runtime_utc", ""),
    )

    html_path = out_dir / "index.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
