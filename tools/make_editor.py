#!/usr/bin/env python3
"""Builds the offline Etsy 'Trade Website Builder' from preview/index.html.
Usage: python3 tools/make_editor.py <output.html>"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "preview/index.html").read_text()
tpl = (ROOT / "assets/callout-template.js").read_text()
inline = "<script>" + tpl.replace("</script>", "<\\/script>") + "</script>\n<script>window.CALLOUT_CONFIG={DEMO_MODE:true};</script>"
src = re.sub(r"<!--TEMPLATE-->.*?<!--/TEMPLATE-->", lambda m: inline, src, flags=re.S)
start = src.index('<div class="order" id="order">'); end = src.index("</form>", start)
dl = '''<div class="order" id="order">
      <span class="label">Step 2 · Save your website</span>
      <p class="note">When you're happy, download your finished website. It's one file called index.html. The included guide shows how to put it online for free in about 10 minutes.</p>
      <label for="formEmail">Email for quote requests <small>enquiries from your site's form are sent here</small><input id="formEmail" type="email" placeholder="you@example.co.uk"></label>
      <button class="btn" type="submit" id="go">Download my website</button>
      <div id="msg" role="status"></div>
    </div>
  '''
src = src[:start] + dl + src[end:]
s2 = src.index('$("f").addEventListener("submit"'); e2 = src.index("render();\n})();", s2)
handler = '''$("f").addEventListener("submit",e=>{e.preventDefault();const c=cfg();if(!c.name){$("msg").innerHTML='<p class="note warn">Add your business name first.</p>';return;}
  const html=T.buildSite({...c,photos,formEmail:$("formEmail").value.trim()},{placeholders:false});
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([html],{type:"text/html"}));a.download="index.html";document.body.appendChild(a);a.click();a.remove();
  $("msg").innerHTML='<p class="note">Saved index.html to your downloads. Follow the guide to put it online.</p>';});
'''
src = src[:s2] + handler + src[e2:]
for a, b in [
    ('["p1","p2","p3"].forEach((id,i)=>{ $(id).textContent', '["p1","p2","p3"].forEach((id,i)=>{ if($(id)) $(id).textContent'),
    ("<title>Instant Website Preview for Tradespeople | Callout Web</title>", "<title>Trade Website Builder | Callout Web</title>"),
    ('<link rel="canonical" href="https://calloutweb.co.uk/preview/">', ""),
    ('<nav><a class="logo" href="../"><b>CALLOUT</b> web</a><span class="label">Instant preview · free</span></nav>',
     '<nav><span class="logo"><b>CALLOUT</b> web</span><span class="label">Trade website builder · works offline</span></nav>'),
    ('<span class="label">Step 1 of 2</span>', '<span class="label">Step 1 · Your details</span>'),
    ("When you're happy, order it and we'll put it live on your own address, usually within one working day.",
     "When you're happy, download it and put it online free using the guide."),
]:
    src = src.replace(a, b)
pathlib.Path(sys.argv[1]).write_text(src)
print("wrote", sys.argv[1])
