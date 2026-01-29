"""Constants for Tapback server."""

SESSION_NAME = "tapback"

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Tapback</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,monospace;background:#0d1117;color:#c9d1d9;display:flex;flex-direction:column}
#h{padding:10px 14px;background:#161b22;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}
#h .t{color:#8b5cf6;font-weight:bold;font-size:18px}
#h .s{font-size:13px}
.on{color:#3fb950}.off{color:#f85149}
#term{flex:1;overflow-y:auto;padding:14px;font-size:13px;line-height:1.5;white-space:pre-wrap;word-break:break-all;min-height:0;font-family:monospace}
#in{padding:12px;background:#161b22;border-top:1px solid #30363d;flex-shrink:0}
.row{display:flex;gap:8px;align-items:center}
#txt{flex:1;padding:12px 14px;font-size:16px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:10px;min-width:0}
#txt:focus{outline:none;border-color:#8b5cf6}
.btn{padding:12px 18px;font-size:15px;font-weight:600;border:none;border-radius:10px;cursor:pointer}
.bsend{background:#8b5cf6;color:#fff}
.benter{background:#30363d;color:#c9d1d9}
.quick{margin-bottom:8px}
.bq{flex:1;background:#21262d;color:#c9d1d9}
</style></head>
<body>
<div id="h"><span class="t">Tapback</span><span class="s" id="st">...</span></div>
<div id="term"></div>
<div id="in">
<div class="row quick">
<button class="btn bq" data-v="0">0</button>
<button class="btn bq" data-v="1">1</button>
<button class="btn bq" data-v="2">2</button>
<button class="btn bq" data-v="3">3</button>
<button class="btn bq" data-v="4">4</button>
</div>
<div class="row">
<input type="text" id="txt" placeholder="Input..." autocomplete="off">
<button class="btn bsend" id="b4">Send</button>
</div>
</div>
<script>
const term=document.getElementById('term'),txt=document.getElementById('txt'),st=document.getElementById('st');
let ws,lastInput='';
function connect(){
const p=location.protocol==='https:'?'wss:':'ws:';
ws=new WebSocket(p+'//'+location.host+'/ws');
ws.onopen=()=>{st.textContent='Connected';st.className='s on';txt.value=lastInput};
ws.onmessage=(e)=>{const d=JSON.parse(e.data);if(d.t==='o'){term.textContent=d.c;term.scrollTop=term.scrollHeight}};
ws.onclose=()=>{st.textContent='Reconnecting...';st.className='s off';setTimeout(connect,2000)};
ws.onerror=()=>ws.close();
}
function send(v){if(ws&&ws.readyState===1)ws.send(JSON.stringify({t:'i',c:v}))}
document.getElementById('b4').onclick=()=>{lastInput=txt.value;send(txt.value);txt.value=''};
txt.onkeypress=(e)=>{if(e.key==='Enter'){lastInput=txt.value;send(txt.value);txt.value=''}};
document.querySelectorAll('.bq').forEach(b=>b.onclick=()=>send(b.dataset.v));
connect();
</script>
</body></html>"""

PIN_HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tapback</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:sans-serif;background:#0d1117;color:#c9d1d9;min-height:100vh;display:flex;align-items:center;justify-content:center}}
.c{{max-width:320px;width:100%;padding:20px;text-align:center}}
.l{{font-size:2rem;margin-bottom:1.5rem;color:#8b5cf6}}
.p{{width:100%;padding:1.2rem;font-size:2rem;text-align:center;letter-spacing:0.8rem;border:1px solid #30363d;border-radius:8px;background:#161b22;color:#c9d1d9;margin-bottom:1rem}}
.b{{width:100%;padding:1rem;font-size:1.1rem;border:none;border-radius:8px;background:#8b5cf6;color:#fff;cursor:pointer}}
.e{{color:#f85149;margin-top:1rem}}
</style></head>
<body><div class="c">
<div class="l">Tapback</div>
<form method="POST" action="/auth">
<input type="text" name="pin" class="p" maxlength="4" inputmode="numeric" placeholder="----" required autofocus>
<button type="submit" class="b">Auth</button>
</form>{error}
</div></body></html>"""
