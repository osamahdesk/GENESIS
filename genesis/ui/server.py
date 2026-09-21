from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from genesis.core import Coordinator, PermissionPolicy


STYLE = """
:root{color-scheme:light;--bg:#f6f8fa;--panel:#fff;--ink:#1f2328;--muted:#656d76;--line:#d0d7de;--accent:#0969da;--green:#1a7f37;--orange:#9a6700;--purple:#8250df}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}header{height:64px;background:#24292f;color:#fff;display:flex;align-items:center;padding:0 32px;gap:18px}header b{font-size:20px}header span{color:#bdc4cc}.layout{display:grid;grid-template-columns:250px 1fr;max-width:1320px;margin:auto;min-height:calc(100vh - 64px)}aside{padding:28px 20px;border-right:1px solid var(--line);background:var(--panel)}aside h3{font-size:12px;text-transform:uppercase;color:var(--muted);letter-spacing:.08em}aside a{display:block;color:var(--ink);padding:9px 10px;border-radius:6px;text-decoration:none}aside a.active,aside a:hover{background:#ddf4ff;color:var(--accent)}main{padding:32px;max-width:1100px}.eyebrow{color:var(--muted);font-size:13px}.hero{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-bottom:28px}.hero h1{font-size:32px;margin:6px 0}.hero p{color:var(--muted);max-width:680px;line-height:1.6}.button{background:var(--green);color:white;border:0;padding:10px 16px;border-radius:6px;font-weight:600;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px}.card h4{margin:0 0 8px;color:var(--muted);font-size:12px;text-transform:uppercase}.value{font-size:25px;font-weight:650}.green{color:var(--green)}.section{margin-top:24px}.section h2{font-size:20px}.workflow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.step{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;cursor:help}.step:hover,.hintable:hover{outline:2px solid #54aeff66}.arrow{color:var(--muted)}.columns{display:grid;grid-template-columns:1.3fr 1fr;gap:16px}.code{background:#24292f;color:#e6edf3;border-radius:8px;padding:16px;overflow:auto;line-height:1.55}.hint{background:#ddf4ff;border:1px solid #54aeff66;padding:14px;border-radius:8px;color:#0550ae;line-height:1.5}.permission{background:#fff8c5;border:1px solid #d4a72c66;padding:14px;border-radius:8px;color:#633c00;line-height:1.5}.table{width:100%;border-collapse:collapse}.table td{border-top:1px solid var(--line);padding:10px 0}.badge{display:inline-block;border-radius:999px;padding:4px 9px;background:#dafbe1;color:var(--green);font-weight:600;font-size:12px}.bubble{position:fixed;z-index:10;max-width:310px;background:#24292f;color:#fff;padding:12px 14px;border-radius:8px;box-shadow:0 8px 24px #1f232855;line-height:1.45}.bubble:after{content:"";position:absolute;bottom:-7px;left:22px;border:7px solid transparent;border-top-color:#24292f;border-bottom:0}@media(max-width:850px){.layout{display:block}aside{display:none}main{padding:20px}.grid{grid-template-columns:repeat(2,1fr)}.columns{grid-template-columns:1fr}.hero{display:block}}
"""


def render_dashboard(record: dict[str, Any] | None, policy: PermissionPolicy | None = None) -> str:
    record = record or {}
    policy = policy or PermissionPolicy()
    evaluation = record.get("evaluation", {})
    experiment = record.get("experiment", record)
    score = float(evaluation.get("score", 0))
    status = experiment.get("status", "not-run")
    passed = evaluation.get("passed", 0)
    total = evaluation.get("total", 0)
    permission_json = html.escape(json.dumps(policy.__dict__ if hasattr(policy, "__dict__") else {"network": policy.network, "filesystem": policy.filesystem, "shell": policy.shell, "private_data": policy.private_data, "external_actions": policy.external_actions, "user_confirmed": policy.user_confirmed}, indent=2))
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>GENESIS Dashboard</title><style>{STYLE}</style></head><body>
<header><b>◈ GENESIS</b><span>Experiment Dashboard · click any highlighted element for a hint</span></header>
<div class='layout'><aside><h3>Workspace</h3><a class='active' href='/'>Overview</a><a href='#workflow'>Workflow</a><a href='#result'>Latest result</a><a href='#permissions'>Permissions</a><a href='#hints'>Getting started</a><h3>Project</h3><a href='https://github.com/osamahdesk/GENESIS'>Repository</a><a href='#'>Documentation</a></aside>
<main><div class='hero'><div><div class='eyebrow'>LOCAL EXPERIMENT WORKSPACE</div><h1>Measure improvement, don't guess it.</h1><p>GENESIS runs structured AI experiments with explicit workflows, independent evaluation, and an auditable result. Click any highlighted element to learn what it does.</p></div><button class='button hintable' data-hint='Refreshes the page and reads the latest saved experiment from SQLite.' onclick='location.reload()'>Refresh run</button></div>
<div class='grid'><div class='card hintable' data-hint='The final state of the latest experiment. Verified means it passed the configured evaluator.'><h4>Status</h4><div class='value green'>{html.escape(str(status))}</div></div><div class='card hintable' data-hint='The primary evaluator score. The first benchmark uses pass rate.'><h4>Score</h4><div class='value'>{score:.0%}</div></div><div class='card hintable' data-hint='How many benchmark cases passed. Hidden and validation cases are kept separate by the evaluator.'><h4>Tests</h4><div class='value'>{passed}/{total}</div></div><div class='card hintable' data-hint='Offline mode keeps the first run deterministic and does not require an API key.'><h4>Mode</h4><div class='value'>offline</div></div></div>
<section class='section' id='workflow'><h2>How GENESIS works</h2><div class='workflow'><div class='step' data-hint='The problem definition and benchmark version.'>Task</div><div class='arrow'>→</div><div class='step' data-hint='A testable claim about what strategy might help.'>Hypothesis</div><div class='arrow'>→</div><div class='step' data-hint='The Builder turns the strategy into an artifact.'>Build</div><div class='arrow'>→</div><div class='step' data-hint='The artifact runs in a bounded temporary workspace.'>Run safely</div><div class='arrow'>→</div><div class='step' data-hint='An independent evaluator decides the score.'>Evaluate</div><div class='arrow'>→</div><div class='step' data-hint='Only evidence-backed outcomes reach Verified.'>Verify</div></div></section>
<section class='section columns' id='result'><div class='card'><h2>Latest experiment</h2><table class='table'><tr><td>Experiment</td><td><b>{html.escape(str(experiment.get('id','—')))}</b></td></tr><tr><td>Task</td><td>{html.escape(str(experiment.get('task_id','—')))}</td></tr><tr><td>Strategy</td><td>{html.escape(str(experiment.get('strategy_id','—')))}</td></tr><tr><td>Decision</td><td><span class='badge'>{html.escape(str(status))}</span></td></tr></table></div><div class='card' id='hints'><h2>Quick hint</h2><div class='hint'><b>Start here:</b> run <code>genesis run</code>, then open this dashboard. The result is stored in SQLite and the generated artifact is saved under <code>.genesis/artifacts</code>.</div><h2>Next research step</h2><p>Replace the deterministic baseline with a provider-backed candidate, then compare both under the same benchmark and budget.</p></div></section>
<section class='section' id='permissions'><div class='card'><h2>Permission center</h2><div class='permission'><b>Safe by default.</b> GENESIS never grants direct host access just because the app opened. Permissions must be explicit, narrow, and user-confirmed. Current policy:</div><pre class='code'>{permission_json}</pre><p>To review or grant a limited permission from the terminal, use <code>genesis permissions</code>. The recommended first grant is project-only filesystem access, never the whole device.</p></div></section>
<section class='section'><h2>Evidence snapshot</h2><pre class='code'>{html.escape(json.dumps(evaluation, indent=2, default=str))}</pre></section></main></div><script>document.querySelectorAll('[data-hint]').forEach(function(el){{el.addEventListener('click',function(){{document.querySelectorAll('.bubble').forEach(function(x){{x.remove()}});var b=document.createElement('div');b.className='bubble';b.textContent=el.dataset.hint;document.body.appendChild(b);var r=el.getBoundingClientRect();b.style.left=Math.min(r.left,window.innerWidth-330)+'px';b.style.top=Math.max(74,r.bottom+10)+'px';setTimeout(function(){{b.remove()}},6500)}})}});</script></body></html>"""


def serve(root: str | Path = ".genesis", host: str = "127.0.0.1", port: int = 8765) -> None:
    coordinator = Coordinator(root)
    records = coordinator.db.list_experiments()
    policy = PermissionPolicy.load(Path(root) / "permissions.json")
    record = {"experiment": records[-1], "evaluation": records[-1].get("metadata", {}).get("evaluation", {})} if records else None

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            body = render_dashboard(record, policy).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    print(f"GENESIS dashboard: http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
