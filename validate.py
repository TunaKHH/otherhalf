"""檢查 site/ 每個 HTML：標籤是否成對、頁內錨點是否存在、出處數量。用法：python3 validate.py"""
import os, re, glob
from html.parser import HTMLParser
VOID = {'meta','link','br','img','input','hr','rect','path','circle','polygon'}
class P(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append(t)
    def handle_endtag(s,t):
        if t in VOID: return
        if s.st and s.st[-1]==t: s.st.pop()
        else: s.err.append((t,s.getpos()))
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'site')
bad=0
for f in sorted(glob.glob(root+'/**/*.html',recursive=True)):
    t=open(f,encoding='utf-8').read(); p=P(); p.feed(t)
    ids=set(re.findall(r'id="([^"]+)"',t))
    miss=[h for h in re.findall(r'href="#([^"]+)"',t) if h not in ids]
    ok=not p.err and not p.st and not miss
    bad+=not ok
    print('OK ' if ok else 'ERR', os.path.relpath(f,root), '出處', t.count('<li id="s'), p.err[:3], p.st, miss)
raise SystemExit(1 if bad else 0)
