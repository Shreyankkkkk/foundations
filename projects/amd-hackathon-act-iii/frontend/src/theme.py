"""Shared visual style. Both front-end builders import from here."""
import html, re
INK, GROUND, STEEL, WARN = "#12222F", "#EEF1F0", "#5E7080", "#E8590C"  # three colours plus one warning colour
esc = html.escape
CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&display=swap');
:root{--ink:#12222F;--steel:#5E7080;--warn:#E8590C}
@property --n{syntax:'<integer>';inherits:false;initial-value:0}
@keyframes count{to{--n:var(--to)}}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes tape{to{background-position:56px 0}}
@keyframes ping{0%{box-shadow:0 0 0 0 rgba(18,34,47,.45)}100%{box-shadow:0 0 0 .8rem rgba(18,34,47,0)}}
@keyframes sweep{to{background-size:100% 100%,100% 4px}}
@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.stApp,.stMarkdown,.stMarkdown *,label,[data-baseweb="select"] *{font-family:'Archivo',system-ui,sans-serif}
header[data-testid="stHeader"]{display:none}
.block-container{max-width:1180px;padding:3rem 2.2rem 5rem}
[data-testid="stSidebar"]{background:#E1E8EA}
.rise{animation:rise .65s cubic-bezier(.2,.7,.2,1) both}
[data-testid="stColumn"]:nth-child(2) .rise{animation-delay:.09s}
[data-testid="stColumn"]:nth-child(3) .rise{animation-delay:.18s}
[data-testid="stColumn"]:nth-child(4) .rise{animation-delay:.27s}
[data-testid="stPlotlyChart"]{animation:wipe 1.1s cubic-bezier(.6,0,.2,1) .15s both}
h1.q{font-weight:800;font-size:2.7rem;letter-spacing:-.025em;line-height:1.1;margin:0 0 .6rem}
.sub{color:var(--steel);font-size:1.08rem;max-width:60ch;margin-bottom:1.8rem;line-height:1.5}
.banner{position:relative;padding:1.05rem 1.1rem .8rem;background:#fff;border-left:6px solid var(--ink);font-weight:600;margin-bottom:2.2rem}
.banner.demo{border-left-color:var(--warn)}
.banner .tape{position:absolute;left:0;right:0;top:0;height:7px;background:linear-gradient(45deg,var(--ink) 25%,var(--warn) 25% 50%,var(--ink) 50% 75%,var(--warn) 75%);background-size:56px 56px;animation:tape 2.6s linear infinite}
.dot{display:inline-block;width:.7rem;height:.7rem;border-radius:50%;background:var(--ink);margin-right:.7rem;animation:ping 1.8s infinite}
.big{--bigsize:3.8rem;font-weight:800;font-size:var(--bigsize);line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.cnt{font-size:0;display:inline-block;counter-reset:n var(--n);animation:count 1.5s cubic-bezier(.2,.7,.2,1) .2s forwards}
.cnt::after{content:counter(n) attr(data-s);font-size:var(--bigsize)}
.lbl{color:var(--steel);margin-top:.55rem;font-size:.95rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
h3.sec{font-weight:800;font-size:1.5rem;margin:3rem 0 1rem}
.plate{display:inline-grid;place-items:center;min-width:2.3rem;height:2.3rem;background:var(--ink);color:#fff;font-weight:800;margin-right:.7rem}
.row{display:grid;grid-template-columns:3.2rem 1fr 3.5rem 8rem;align-items:center;gap:1rem;padding:1.1rem 0;border-top:2px solid var(--ink);transition:transform .25s}
.row:hover{transform:translateX(6px)}
.nm{font-weight:600;font-size:1.15rem}
.bar{height:.5rem;background:#D5DDE0;margin-top:.55rem}
.bar i{display:block;height:100%;background:var(--ink);transform-origin:left;animation:grow 1.2s cubic-bezier(.2,.7,.2,1) .35s both}
.ct{font-weight:800;font-size:2rem;text-align:right}.tr{font-weight:600;color:var(--steel)}.tr.up{color:var(--warn)}
.flag,.card{background:#fff;padding:1.2rem 1.4rem;margin-bottom:1rem;transition:transform .25s,box-shadow .25s}
.flag:hover,.card:hover{transform:translateY(-3px);box-shadow:0 12px 26px -14px rgba(18,34,47,.55)}
.flag blockquote{margin:.7rem 0;padding-left:1rem;border-left:5px solid var(--warn);font-size:1.15rem}
.meta{color:var(--steel);font-size:.95rem}
.chip{display:inline-block;padding:.1rem .6rem;border:2px solid var(--ink);font-weight:600;font-size:.85rem;margin:0 .4rem .4rem 0}
.chip.ok{background:var(--ink);color:#fff}.chip.low,.chip.bad{border-color:var(--warn);background:#FFE9DC}
.stepbox{background:#fff;padding:1rem 1.3rem;margin:.6rem 0 1.4rem;line-height:1.5}
.note{background:#fff;padding:1.4rem 1.5rem;font-size:1.25rem;line-height:1.75;margin:.6rem 0 .8rem}
mark.hl{color:inherit;font-weight:600;padding:.05rem .15rem;background:linear-gradient(rgba(232,89,12,.3),rgba(232,89,12,.3)),linear-gradient(var(--warn),var(--warn));background-repeat:no-repeat;background-position:0 0,0 100%;background-size:0% 100%,0% 4px;animation:sweep 1s cubic-bezier(.6,0,.2,1) .6s forwards}
.draft{position:relative;margin-top:1.4rem;padding:1.5rem 1.2rem 1.1rem;border:2px dashed var(--ink);background:#fff;line-height:1.5}
.draft .tag{position:absolute;top:-.85rem;left:.9rem;background:var(--ink);color:#fff;font-weight:800;font-size:.75rem;letter-spacing:.08em;padding:.2rem .6rem;text-transform:uppercase}
.stButton>button{border-radius:0;border:2px solid var(--ink);font-weight:600;transition:transform .15s}
.stButton>button:hover{transform:translateY(-2px);border-color:var(--ink)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.cnt{--n:var(--to)}mark.hl{background-size:100% 100%,100% 4px}}
</style>"""

def title(question, sub):
    return f"<h1 class='q rise'>{esc(question)}</h1><div class='sub rise' style='animation-delay:.1s'>{esc(sub)}</div>"

def big(value, label):
    m = re.fullmatch(r"(\d+)(%?)", str(value).replace(",", ""))  # whole numbers and percents count up
    v = f"<span class='cnt' style='--to:{m[1]}' data-s='{m[2]}'>{value}</span>" if m else esc(str(value))
    return f"<div class='rise'><div class='big'>{v}</div><div class='lbl'>{esc(label)}</div></div>"

def banner(mode):
    if mode == "live":
        return "<div class='banner rise'><span class='dot'></span>Live mode: showing results from the running pipeline.</div>"
    return "<div class='banner demo rise'><span class='tape'></span>Demo mode: showing saved results. All data is synthetic.</div>"
