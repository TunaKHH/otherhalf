import os
ROOT=os.path.dirname(os.path.abspath(__file__))
import re, os
src=open(os.path.join(ROOT,'src','legacy-index.html'),encoding='utf-8').read()
def between(start,end):
    # 依標記擷取 legacy-index.html 的區塊（不含標記本身），找不到或不唯一就直接報錯
    assert src.count(start)==1, f'標記不唯一：{start}'
    i=src.index(start)+len(start); j=src.index(end,i)
    return src[i:j].strip('\n')
css=between('<style>\n','</style>')
# 彈窗的 CSS 在下方 GLOSS_CSS，插在 legacy CSS 的「/* 名詞說明彈窗 */」註解後面（維持 cascade 順序）
_gm='/* 名詞說明彈窗 */\n'; assert css.count(_gm)==1, '找不到彈窗 CSS 的插入標記'
_gs=css.index(_gm)+len(_gm)
# 提示詞按鈕的 JS：legacy 檔裡含 PROMPTS 的那個 <script>
_p=src.index('var PROMPTS')
js_prompts=src[src.rindex('<script>',0,_p)+len('<script>'):src.index('</script>',_p)].strip('\n')

# --- 名詞說明彈窗（glossary dialog）
# 觸發方式：<button type="button" class="term" data-term="KEY" aria-haspopup="dialog">名詞</button>
# 新增名詞：在下面 GLOSS_JS 的 TERMS 加一個 KEY。
dialog=r'''<dialog class="gloss" id="gloss" aria-labelledby="gloss-title">
  <div class="gloss-body">
    <div class="gloss-head">
      <div class="gloss-id">
        <div class="gloss-side"><span class="gloss-flag" id="gloss-flag"></span><span id="gloss-sidetext"></span></div>
        <h2 id="gloss-title"></h2>
        <p class="full" id="gloss-full"></p>
      </div>
      <button type="button" class="gloss-close" id="gloss-close" aria-label="關閉說明">×</button>
    </div>
    <dl id="gloss-list"></dl>
    <p class="note" id="gloss-note"></p>
  </div>
</dialog>'''
GLOSS_CSS=r'''.term { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; text-decoration: underline dotted; text-decoration-thickness: 2px; text-underline-offset: 4px; text-decoration-color: var(--accent); }
.quote .term { text-decoration-color: var(--band-accent); }
.term:hover { color: var(--accent); }
.quote .term:hover { color: var(--band-accent); }
.term:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px; }
.gloss { border: 1px solid var(--line); border-radius: 16px; padding: 0; width: min(520px, calc(100vw - 32px)); background: var(--surface); color: var(--ink); box-shadow: 0 24px 60px rgba(10, 20, 30, .25); }
.gloss::backdrop { background: rgba(10, 16, 22, .55); }
.gloss-body { padding: 28px 28px 24px; display: grid; gap: 16px; }
.gloss-head { display: flex; justify-content: space-between; align-items: start; gap: 16px; }
.gloss-id { display: grid; gap: 10px; }
.gloss-side { display: flex; align-items: center; gap: 12px; font-size: .85rem; font-weight: 700; letter-spacing: .08em; color: var(--muted); }
.gloss-flag { display: inline-flex; line-height: 0; border-radius: 4px; overflow: hidden; box-shadow: 0 0 0 1px var(--line); }
.gloss-flag svg { display: block; width: 60px; height: 40px; }
.gloss h2 { font-family: var(--display); font-weight: 900; font-size: 1.8rem; line-height: 1.2; }
.gloss .full { color: var(--muted); font-size: .92rem; margin-top: 6px; }
.gloss dl { margin: 0; display: grid; gap: 12px; }
.gloss dt { font-size: .78rem; letter-spacing: .1em; color: var(--accent); font-weight: 700; }
.gloss dd { margin: 2px 0 0; font-size: .97rem; line-height: 1.75; }
.gloss .note { font-size: .88rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 14px; }
.gloss-close { flex: none; width: 44px; height: 44px; border-radius: 999px; border: 1px solid var(--line); background: var(--ground); color: var(--ink); font-size: 1.3rem; line-height: 1; cursor: pointer; }
.gloss-close:hover { border-color: var(--accent); color: var(--accent); }
.gloss-close:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }'''
css=css[:_gs]+GLOSS_CSS+'\n'+css[_gs:]
GLOSS_JS=r'''(function () {
  var TERMS = {
    mac: {
      title: "陸委會",
      side: "台灣 · 中華民國",
      flag: '<svg viewBox="0 0 240 160" width="60" height="40" role="img" aria-label="中華民國國旗"><rect width="240" height="160" fill="#FE0000"/><rect width="120" height="80" fill="#000095"/><polygon fill="#FFFFFF" points="60.00,10.00 55.86,24.55 64.14,24.55"/><polygon fill="#FFFFFF" points="75.00,14.02 64.14,24.55 71.31,28.69"/><polygon fill="#FFFFFF" points="85.98,25.00 71.31,28.69 75.45,35.86"/><polygon fill="#FFFFFF" points="90.00,40.00 75.45,35.86 75.45,44.14"/><polygon fill="#FFFFFF" points="85.98,55.00 75.45,44.14 71.31,51.31"/><polygon fill="#FFFFFF" points="75.00,65.98 71.31,51.31 64.14,55.45"/><polygon fill="#FFFFFF" points="60.00,70.00 64.14,55.45 55.86,55.45"/><polygon fill="#FFFFFF" points="45.00,65.98 55.86,55.45 48.69,51.31"/><polygon fill="#FFFFFF" points="34.02,55.00 48.69,51.31 44.55,44.14"/><polygon fill="#FFFFFF" points="30.00,40.00 44.55,44.14 44.55,35.86"/><polygon fill="#FFFFFF" points="34.02,25.00 44.55,35.86 48.69,28.69"/><polygon fill="#FFFFFF" points="45.00,14.02 48.69,28.69 55.86,24.55"/><circle cx="60" cy="40" r="17" fill="#000095"/><circle cx="60" cy="40" r="15" fill="#FFFFFF"/></svg>',
      full: "中華民國行政院大陸委員會",
      items: [
        ["是什麼", "台灣政府負責兩岸事務的部會，隸屬行政院。"],
        ["做什麼", "統籌兩岸政策，主管《兩岸人民關係條例》，訂定與執行兩岸交流的相關規範，並定期舉行記者會說明政府立場。"],
        ["在北京的對口", "國台辦。兩者之間的聯繫機制自 2016 年起停擺。"],
        ["和海基會的關係", "海基會是陸委會委託的民間團體，負責與北京的海協會進行事務性協商。"]
      ],
      note: "陸委會的說法代表台灣政府（行政院）的立場，不一定代表所有政黨的看法。"
    },
    tao: {
      title: "國台辦",
      side: "北京 · 中華人民共和國",
      flag: '<svg viewBox="0 0 30 20" width="60" height="40" role="img" aria-label="中華人民共和國國旗"><rect width="30" height="20" fill="#EE1C25"/><polygon fill="#FFFF00" points="5.000,2.000 5.674,4.073 7.853,4.073 6.090,5.354 6.763,7.427 5.000,6.146 3.237,7.427 3.910,5.354 2.147,4.073 4.326,4.073"/><polygon fill="#FFFF00" points="9.143,2.514 9.619,1.966 9.246,1.343 9.914,1.628 10.391,1.080 10.328,1.803 10.996,2.088 10.288,2.251 10.224,2.975 9.851,2.352"/><polygon fill="#FFFF00" points="11.010,4.141 11.662,3.821 11.560,3.102 12.065,3.624 12.718,3.304 12.378,3.946 12.884,4.467 12.168,4.343 11.829,4.985 11.726,4.266"/><polygon fill="#FFFF00" points="11.038,6.725 11.765,6.699 11.964,6.001 12.213,6.683 12.939,6.657 12.367,7.105 12.616,7.787 12.014,7.382 11.442,7.830 11.641,7.131"/><polygon fill="#FFFF00" points="9.219,8.375 9.899,8.632 10.353,8.064 10.319,8.790 10.999,9.046 10.298,9.239 10.265,9.964 9.865,9.357 9.165,9.550 9.618,8.982"/></svg>',
      full: "中國國務院台灣事務辦公室",
      items: [
        ["是什麼", "北京負責對台政策的政府機關。同時也是中共中央台灣工作辦公室，一個機構、兩塊牌子。"],
        ["做什麼", "制定與執行對台政策，並定期舉行記者會，由發言人說明北京對台灣議題的立場。"],
        ["在台灣的對口", "行政院大陸委員會（陸委會）。兩者之間的聯繫機制自 2016 年起停擺。"]
      ],
      note: "國台辦發言人的說法代表北京官方立場，本頁引用是為了呈現北京怎麼定義交流。"
    }
  };
  var dlg = document.getElementById("gloss");
  var lastTrigger = null;
  function render(key) {
    var t = TERMS[key];
    if (!t) return false;
    document.getElementById("gloss-title").textContent = t.title;
    document.getElementById("gloss-flag").innerHTML = t.flag || "";
    document.getElementById("gloss-sidetext").textContent = t.side || "";
    document.getElementById("gloss-full").textContent = t.full;
    document.getElementById("gloss-note").textContent = t.note || "";
    var list = document.getElementById("gloss-list");
    list.textContent = "";
    t.items.forEach(function (it) {
      var wrap = document.createElement("div");
      var dt = document.createElement("dt"); dt.textContent = it[0];
      var dd = document.createElement("dd"); dd.textContent = it[1];
      wrap.appendChild(dt); wrap.appendChild(dd); list.appendChild(wrap);
    });
    return true;
  }
  function open(key, trigger) {
    if (!render(key)) return;
    lastTrigger = trigger;
    if (typeof dlg.showModal === "function") { try { dlg.showModal(); } catch (e) { dlg.setAttribute("open", ""); } }
    else { dlg.setAttribute("open", ""); }
    document.addEventListener("keydown", onKey);
    document.getElementById("gloss-close").focus();
  }
  function onKey(e) { if (e.key === "Escape") { close(); } }
  function close() {
    document.removeEventListener("keydown", onKey);
    if (typeof dlg.close === "function") dlg.close(); else { dlg.removeAttribute("open"); if (lastTrigger) lastTrigger.focus(); }
  }
  dlg.addEventListener("close", function () { if (lastTrigger) lastTrigger.focus(); });
  document.getElementById("gloss-close").addEventListener("click", close);
  dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
  document.querySelectorAll(".term[data-term]").forEach(function (b) {
    b.addEventListener("click", function () { open(b.getAttribute("data-term"), b); });
  });
})();'''
js=GLOSS_JS+'\n'+js_prompts
open(os.path.join(ROOT,'site','css','site.css'),'w',encoding='utf-8').write(css+'''
.backnav a.home { font-weight: 700; }
.hub-list { display: grid; gap: 14px; }
.hub-card { display: grid; gap: 8px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 24px 26px; text-decoration: none; color: var(--ink); }
a.hub-card:hover { border-color: var(--accent); }
.hub-card .tag { font-size: .78rem; font-weight: 700; letter-spacing: .08em; color: var(--muted); }
.hub-card h2 { font-family: var(--display); font-weight: 900; font-size: clamp(1.4rem, 4vw, 1.9rem); line-height: 1.35; }
.hub-card p { color: var(--muted); }
.hub-card .half { font-weight: 700; color: var(--accent); font-size: 1.02rem; margin-top: -4px; }
.hub-card { scroll-margin-top: 24px; }
.hub-card:target { border-color: var(--accent); box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 22%, transparent); }
.hub-card .go { color: var(--accent); font-weight: 700; }
.hub-card.planned { border-style: dashed; background: transparent; }
.method { display: grid; gap: 10px; }
.hero .marker { letter-spacing: .04em; line-height: 1.6; flex-wrap: wrap; }
.hero .marker a { color: var(--accent); font-weight: 700; text-decoration: none; }
.method ul { margin: 0; padding-left: 1.2em; display: grid; gap: 6px; }
.defs-grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
@media (max-width: 760px) { .defs-grid.two { grid-template-columns: minmax(0, 1fr); } }
.table-wrap { overflow-x: auto; }
.ends { width: 100%; border-collapse: separate; border-spacing: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; font-size: .97rem; }
.ends th, .ends td { padding: 14px 18px; text-align: left; vertical-align: top; border-bottom: 1px solid var(--line); line-height: 1.7; }
.ends tr:last-child th, .ends tr:last-child td { border-bottom: 0; }
.ends thead th { font-family: var(--display); font-size: 1.05rem; background: var(--ground); }
.ends tbody th { font-size: .85rem; color: var(--muted); white-space: nowrap; }
.said .who { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; }
.said .who strong { font-family: var(--display); font-size: 1.35rem; }
.said .who span { font-size: .85rem; color: var(--muted); }
.said-group { font-family: var(--display); font-weight: 900; font-size: 1.3rem; margin-top: 8px; }
.said-q { margin: 0; padding: 14px 18px; border-left: 3px solid var(--line); background: var(--ground); border-radius: 0 10px 10px 0; font-size: 1.02rem; line-height: 1.75; }
''')
js=js.replace('    parity: "','    legislators: "行政院 2025 年 12 月通過的《兩岸人民關係條例》修正草案，要求立委赴中國須經許可、接觸中共黨政軍須返台公開揭露。請幫我整理：（1）草案的具體內容與目前立法進度；（2）支持方的理由，包括防止洩密與讓選民監督；（3）反對方的理由，包括民意代表的角色、權力分立與是否針對特定政黨；（4）其他民主國家對國會議員訪問敵對或競爭國家有沒有類似規範。請平衡呈現，不要替我下結論。",\n    war: "有人說「民進黨的路線會導致戰爭」。請幫我分別整理：（1）支持這個說法的主要論點與證據，例如 2016 年後兩岸關係的變化；（2）質疑這個說法的主要論點與證據，例如北京在不同執政黨時期對使用武力的立場、中國對其他鄰國的施壓；（3）如果台灣改走接受「九二共識」的路線，北京、國民黨、民進黨各自認為會有什麼結果與代價。請平衡呈現，不要替我下結論。",\n    parity: "',1)
js=js.replace('    legislators: "','    budget: "有人說「藍白拿預算當人質」。請幫我整理 2025 到 2026 年立法院處理中央政府總預算與國防特別條例的經過：（1）兩案各被擋了多久、在野提出的條件是什麼；（2）行政院沒有編列軍人加薪、警消退休金預算的理由，以及釋憲進度；（3）在野與執政黨各自的說法；（4）過去其他政黨在野時有沒有類似的杯葛先例。請平衡呈現，不要替我下結論。",\n    legislators: "',1)
# 每個提示詞都以「請平衡呈現，不要替我下結論。」結尾（legacy 的舊提示詞沒有，這裡統一補上）
_END='請平衡呈現，不要替我下結論。'
js=re.sub(r'^(    \w+: ")(.*?)(",?)$',lambda m:m.group(1)+m.group(2)+('' if m.group(2).endswith(_END) else _END)+m.group(3),js,flags=re.M)
js=js+"""
(function () {
  function toTop() {
    if (location.hash) return;
    var nav = null;
    try { nav = performance.getEntriesByType("navigation")[0]; } catch (e) {}
    if (nav && nav.type === "back_forward") return;
    window.scrollTo(0, 0);
  }
  toTop();
  window.addEventListener("load", function () { toTop(); setTimeout(toTop, 60); });
})();
"""
open(os.path.join(ROOT,'site','js','site.js'),'w',encoding='utf-8').write(js)

sources={}
for m in re.finditer(r'<li id="s(\d+)"><a href="([^"]+)">([^<]+)</a></li>',src):
    sources[int(m.group(1))]=(m.group(2),m.group(3))
sources.update({63:('https://cna.com.tw/news/aipl/202610100056.aspx','中央社：賴清德國慶演說（2026/10/10）'),64:('https://newtalk.tw/news/view/2024-01-12/904783','新頭殼：馬英九接受德國之聲專訪談習近平與武力'),65:('https://www.thenewslens.com/article/197377','關鍵評論網：馬英九稱任內台海平靜'),66:('https://www.stheadline.com/china-politics/3589589/','星島：中國海警在台灣以東、與那國島以南巡航，日本抗議')})
sources[67]=('https://udn.com/news/story/6656/9379856','聯合報：賴清德稱不需另外宣布獨立')
sources[57]=('https://newtalk.tw/news/view/2026-04-20/1030800','新頭殼：鄭習會後中國宣布十項措施，國民黨回應')
sources[62]=('https://wantrich.chinatimes.com/news/20250721900073-420501','旺得富：朱立倫批民進黨「假反共真戰爭」（2025/7）')
def block(start_marker, end_marker, start_from=0):
    i=src.index(start_marker,start_from); j=src.index(end_marker,i)+len(end_marker); return src[i:j]
layers=block('  <section id="layers"','  </section>')
facts=block('  <section id="facts"','  </section>')
iss=block('  <section id="issues"','  </section>')
parts=iss.split('    <div class="issue">')
infil='    <div class="issue">'+parts[1].rstrip()
defense='    <div class="issue">'+parts[2].rstrip()
speech='    <div class="issue">'+parts[3].split('  </section>')[0].rstrip()
faqs=re.findall(r'      <article class="faq-item">.*?      </article>',src,re.S)
faq_spies,faq_label,faq_real=faqs
TAO='<button type="button" class="term" data-term="tao" aria-haspopup="dialog">國台辦</button>'

def btn(k,dark=False):
    return f'<div class="ask-ai-wrap"><button type="button" class="ask-ai{" on-dark" if dark else ""}" data-prompt="{k}"><span class="ask-ai-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg></span><span class="ask-ai-label">複製提示詞，問你自己的 AI</span></button><span class="ask-ai-status" role="status" aria-live="polite"></span></div>'

def page(fname,title,desc,body,depth):
    pre='../' if depth else ''
    # renumber sources
    order=[]
    for n in re.findall(r'href="#s(\d+)"',body):
        n=int(n)
        if n not in order: order.append(n)
    mp={o:i+1 for i,o in enumerate(order)}
    body=re.sub(r'<a href="#s(\d+)">\d+</a>',lambda m:f'<a href="#s{mp[int(m.group(1))]}">{mp[int(m.group(1))]}</a>',body)
    refs=''
    if order:
        items='\n'.join(f'    <li id="s{mp[o]}"><a href="{sources[o][0]}">{sources[o][1]}</a></li>' for o in order)
        refs=f'''
<section id="refs" class="shell sources" aria-labelledby="h-refs">
  <h2 id="h-refs">出處</h2>
  <ol>
{items}
  </ol>
</section>'''
    nav=f'''<nav class="topnav backnav" aria-label="導覽">
  <div class="shell">
    <a class="home" href="{pre}index.html{'#card-'+os.path.basename(fname)[:-5] if fname.startswith('articles/') else ''}">← 所有議題</a>
    {'<a href="#refs">出處</a>' if order else ''}
  </div>
</nav>''' if fname!='index.html' else ''
    html=f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}css/site.css">
</head>
<body>
{nav}
<main>
{body}
{refs}
<footer class="shell sources">
  <div class="foot">
    <p>整理方式：只收錄有報導可查的作為與各方公開說明的理由，不收錄未經證實的指控。資料截至 2026 年 11 月 18 日。</p>
    <p class="author">整理者：<a href="https://www.threads.com/@tuna._run" target="_blank" rel="noopener">Tuna（Threads @tuna._run）</a></p>
    <p>發現錯誤或漏掉的觀點，歡迎到 Threads 私訊整理者，或到 <a href="https://github.com/TunaKHH/otherhalf/issues" target="_blank" rel="noopener">GitHub 開 issue</a> 指正。</p>
    <p>本站原始碼公開，每次修正都留有紀錄：<a href="https://github.com/TunaKHH/otherhalf" target="_blank" rel="noopener">GitHub 原始碼</a>・<a href="https://github.com/TunaKHH/otherhalf/commits/main" target="_blank" rel="noopener">修正紀錄</a></p>
  </div>
</footer>
{dialog}
<script src="{pre}js/site.js"></script>
</body>
</html>
'''
    open(os.path.join(ROOT,'site',fname),'w',encoding='utf-8').write(html)

def hero(marker,h1,verdict,tldr,after):
    lis='\n'.join(f'      <li{" class=\"key\"" if i==0 else ""}><a class="tldr-head" href="{h}">{t}</a><span>{d}</span></li>' for i,(h,t,d) in enumerate(tldr))
    return f'''  <section class="shell hero" aria-labelledby="title">
    <div class="marker">{marker}</div>
    <h1 id="title">{h1}</h1>
    <p class="verdict">{verdict}</p>
    <ol class="tldr">
{lis}
    </ol>
    <p class="after">{after}</p>
  </section>
'''
def close(h,qs,k):
    q='\n'.join(f'      <li>{x}</li>' for x in qs)
    return f'''
<section id="ask" class="close" aria-labelledby="h-ask">
  <div class="shell">
    <div class="marker">換你想想</div>
    <h2 id="h-ask">{h}</h2>
    <ol>
{q}
    </ol>
    {btn(k,True) if k else ''}
    <p>每個人在意的東西不一樣，答案本來就會不同。想聊的話，歡迎拿這頁去找想法不一樣的朋友。</p>
  </div>
</section>'''
def faqsec(title,intro,items):
    return f'''  <section id="faq" class="shell chapter" aria-labelledby="h-faq">
    <header>
      <div class="marker">常聽到的說法</div>
      <h2 id="h-faq">{title}</h2>
      <p class="intro">{intro}</p>
    </header>
    <div class="faq">
{chr(10).join(items)}
    </div>
  </section>
'''
def relabel(sec,label):
    return re.sub(r'<div class="marker">\d\d</div>',f'<div class="marker">{label}</div>',sec,count=1)

# ===== 誰這樣說過（exchange article）=====
extra_src={
38:("https://newtalk.tw/news/view/2026-06-22/1042532","新頭殼：鄭麗文新竹談話（2026/6/21）"),
39:("https://www.cna.com.tw/news/ahel/202306200127.aspx","中央社：中國恢復台灣釋迦輸入，饒慶鈴致謝（2023/6）"),
40:("https://www.cna.com.tw/news/aipl/202212110159.aspx","中央社：中國禁止台灣農漁產品時間軸"),
41:("https://www.ctee.com.tw/news/20260124700523-431401","工商時報：ECFA 早收中止，鳳梨釋迦外銷受衝擊"),
42:("https://www.storm.mg/article/11151307","風傳媒：梁文傑稱兩岸條例未限制農漁團體與陸方簽約"),
43:("https://www.ettoday.net/news/20260617/3185067.htm","ETtoday：邱垂正稱政府只禁海峽論壇（2026/6/17）"),
44:("https://www.worldjournal.com/wj/story/121220/9230331","世界日報：國民黨團批限縮公務員赴中"),
45:("https://news.pts.org.tw/article/751495","公視：陸委會建議地方勿出席海峽論壇，南投縣長回應"),
46:("https://news.ltn.com.tw/amp/news/politics/breakingnews/5504913","自由時報：民眾黨青年團赴中，陸委會表示祝福"),
47:("https://news.pts.org.tw/article/787966","公視：鄭麗文籲賴清德接受九二共識，民進黨回應"),
48:("https://www.taiwannews.com.tw/zh/news/5076698","台灣英文新聞：馬英九強調拒絕一國兩制、主張一中各表"),
49:("https://n.yam.com/Article/20260205984813","蕃新聞：「國共論壇」與國民黨聲明（2026/2）"),
50:("https://udn.com/news/story/6656/9135987","聯合報：國民黨團主張立院兩岸小組"),
51:("https://www.thenewslens.com/article/42808","關鍵評論網：國台辦宣布兩岸聯繫溝通機制停擺（2016）"),
}
sources.update(extra_src)
said='''
  <section id="said" class="shell chapter" aria-labelledby="h-said">
    <header>
      <div class="marker">誰這樣說過</div>
      <h2 id="h-said">兩邊都只講了一半</h2>
      <p class="intro">這裡只看那句話少了什麼，不評論說話的人。每則都附原始報導，可以自己點開看完整脈絡。</p>
    </header>
    <h3 class="said-group">官方對話：為什麼談不起來</h3>
    <div class="faq">
      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>鄭麗文</strong><span>國民黨主席 · 2026 年 6 月 21 日 · 報導轉述</span></div>
        <blockquote class="said-q">賴政府執政兩年完全不與對岸對話，難道一定要打仗嗎？<sup><a href="#s38">38</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>兩岸官方對話確實停擺，陸委會與國台辦、海基會與海協會之間沒有正式協商。<sup><a href="#s3">3</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>停擺不是從賴政府開始，而是 2016 年起就中斷。<sup><a href="#s51">51</a></sup>北京的條件是先承認九二共識，否則對話「無從談起」<sup><a href="#s19">19</a></sup>；陸委會則要求不設前提的對話。<sup><a href="#s4">4</a></sup></p></div>
        </div>
        <p class="analogy">她在其他場合說過完整的條件：賴清德「只要接受九二共識、下架台獨黨綱」，就可能比她更早見到習近平。<sup><a href="#s47">47</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>鍾佳濱</strong><span>民進黨立委 · 回應鄭麗文 · 公開發言</span></div>
        <blockquote class="said-q">「九二共識就是一國兩制……因此在台灣沒有人會接受。」<sup><a href="#s47">47</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>北京 2019 年把九二共識定調為「同屬一個中國，共同努力謀求國家統一」，並與「和平統一、一國兩制」一起提出。<sup><a href="#s28">28</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>國民黨對九二共識的解讀是「一中各表」，並明確表示拒絕一國兩制<sup><a href="#s29">29</a></sup><sup><a href="#s48">48</a></sup>；「沒有人會接受」也不精確，國民黨就是主張接受九二共識的一方。</p></div>
        </div>
        <p class="analogy">民進黨中央同時表示：只要對等尊嚴，當然願意跟中國官方交流。<sup><a href="#s47">47</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>國民黨</strong><span>黨聲明 · 2026 年 2 月 · 報導轉述</span></div>
        <blockquote class="said-q">民進黨自己放棄兩岸溝通及談判的責任，不接觸、不溝通，反而怪國民黨的溝通接觸。<sup><a href="#s49">49</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>民進黨政府不接受九二共識，官方之間確實沒有溝通談判。<sup><a href="#s47">47</a></sup><sup><a href="#s3">3</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>「不接觸」的原因是北京把承認九二共識設為對話前提，不承認就「無從談起」<sup><a href="#s19">19</a></sup>；陸委會的立場是願意在不設前提下對話。<sup><a href="#s4">4</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：目前沒有找到。</p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>林沛祥</strong><span>國民黨立委 · 主張成立立法院兩岸小組時 · 報導轉述</span></div>
        <blockquote class="said-q">賴總統一句「中國大陸是境外敵對勢力」是赤裸裸的敵意，導致與大陸溝通、協調、交涉管道都沒有。<sup><a href="#s50">50</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>政府與北京之間的溝通、交涉管道確實不通。<sup><a href="#s3">3</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>官方聯繫機制在 2016 年就已停擺，早於賴清德擔任總統，也早於「境外敵對勢力」這個說法；北京當時的理由是台灣未確認九二共識。<sup><a href="#s51">51</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：國民黨團同時提議由立法院成立兩岸小組，與對岸交涉、解決問題。<sup><a href="#s50">50</a></sup></p>
      </article>
    </div>

    <h3 class="said-group">民間交流：誰在擋</h3>
    <div class="faq">
      <article class="faq-item said" id="said-kmt">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>國民黨</strong><span>黨聲明 · 2026 年 4 月 20 日</span></div>
        <blockquote class="said-q">民進黨政府應務實推動有利人民與產業的兩岸措施，而不是「逢中必反、逢交流必擋」。<sup><a href="#s57">57</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>政府確實收緊了不少交流：禁止公職人員參加海峽論壇、團客赴陸的禁團令未解除，政院草案也讓公務員赴陸全面改為許可制。<sup><a href="#s27">27</a></sup><sup><a href="#s26">26</a></sup><sup><a href="#s7">7</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>政府表示支持雙城論壇、兩湖論壇等交流<sup><a href="#s43">43</a></sup>；陸客自由行是北京 2019 年片面暫停的，政府要求恢復須經雙方觀光協會協商。<sup><a href="#s24">24</a></sup> 另外，民間往來 2025 年仍超過 500 萬人次。<sup><a href="#s5">5</a></sup></p></div>
        </div>
        <p class="analogy">背景：這份聲明是在國民黨主席訪陸、北京宣布十項交流措施之後發出的。<sup><a href="#s57">57</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>鄭麗文</strong><span>國民黨主席 · 2026 年 6 月 21 日 · 報導轉述</span></div>
        <blockquote class="said-q">批評民進黨政府阻擋台東鳳梨釋迦銷往中國，是在「跟台灣農民過不去」。<sup><a href="#s38">38</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>政府今年禁止地方首長出席海峽論壇，台東縣長的申請被拒。<sup><a href="#s18">18</a></sup> 2023 年台東縣長在海峽論壇上爭取後，北京隨即宣布恢復釋迦輸入。<sup><a href="#s39">39</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>釋迦賣不進中國，起因是北京 2021 年 9 月以檢出害蟲為由暫停輸入<sup><a href="#s40">40</a></sup>；2024 年起北京又分批中止 ECFA 早收優惠、恢復關稅。<sup><a href="#s41">41</a></sup> 陸委會也表示，兩岸條例並未限制農漁團體與陸方簽約。<sup><a href="#s42">42</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：目前沒有找到。</p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">民進黨政府</span>
        <div class="who"><strong>邱垂正</strong><span>陸委會主委 · 2026 年 6 月 17 日 · 報導轉述</span></div>
        <blockquote class="said-q">政府對於兩岸之間對等、尊嚴、健康有序的交流，都持續給予支持與協助，只禁止海峽論壇這類統戰平台。<sup><a href="#s43">43</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>雙城論壇今年仍有舉辦<sup><a href="#s44">44</a></sup>；民眾黨青年團、國民黨主席赴陸，陸委會也表示給予祝福。<sup><a href="#s46">46</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>「健康有序」由政府認定。同一時期政府也在收緊：政院草案讓公務員赴陸全面改為許可制<sup><a href="#s7">7</a></sup>，團客赴陸的禁團令仍未解除<sup><a href="#s26">26</a></sup>；國民黨團批評雙城論壇被刁難、時程縮短<sup><a href="#s44">44</a></sup>；南投縣長也表示，與杭州合辦的兩湖論壇因政策要縮小規模。<sup><a href="#s45">45</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：邱垂正同時說明，國人赴陸遭盤查、失聯的案件增加，政府有責任提醒風險。<sup><a href="#s43">43</a></sup></p>
      </article>
    </div>
  </section>
'''

# --- Article 1: exchange
src_hero=block('  <section class="shell hero"','  </section>')
h1=src_hero.replace('<div class="marker">你可能聽過這句話</div>','<div class="marker">國民黨聲明的原話（2026 年 4 月）<a href="#said-kmt">看出處 ↓</a></div>').replace('<h1 id="title">「民進黨都不交流！」</h1>','<h1 id="title">「逢中必反、逢交流必擋」</h1>').replace('<a class="tldr-head" href="#facts">','<a class="tldr-head" href="anti-communism.html">').replace('    <div class="stack">\n      <p class="meta"><span>資料截至 2026 年 11 月 18 日</span><span>每段附報導出處</span><span>不打算告訴你該支持誰</span></p>\n    </div>\n','')
a1=h1+'\n\n'+relabel(layers,'依據').replace('所以「民進黨都不交流」對了一半','所以「逢中必反、逢交流必擋」對了一半')+'\n'+said
a1_close=close('你怎麼看這個前提？',['北京以承認「九二共識」作為官方對話的前提，而各方對九二共識的定義不同。你可以接受這個前提嗎？為什麼？'],'parity')
page('articles/exchange.html','「逢中必反、逢交流必擋」沒說的另一半是？','「逢中必反、逢交流必擋」對了一半。兩岸交流卡在哪裡、雙方各自的限制、九二共識的三種定義，每段附出處。',a1+'</main>\n<!--x-->'+a1_close.replace('\n<section','<section',1),1)

# --- Article 2: anti-communism
a2h=hero('時任國民黨主席朱立倫的原話（2025 年 7 月）<a href="#said-zhu">看出處 ↓</a>','「假反共真戰爭」','這句話混了好幾件事。',[
 ('#facts','滲透是真的，而且不分藍綠','共諜案起訴人數從 2021 年 16 人增加到 2024 年 64 人，六成以上是軍人；增加的原因之一是修法擴大罪名。<sup><a href="#s1">1</a></sup><sup><a href="#s20">20</a></sup><sup><a href="#s2">2</a></sup>'),
 ('#facts','口號有沒有被操作，各方看法不同','大罷免全數未通過後，有分析認為抗中保台的論述需要重建；也有評論認為點名協力者能提高警覺。<sup><a href="#s30">30</a></sup><sup><a href="#s31">31</a></sup><sup><a href="#s36">36</a></sup>'),
 ('#faq','民進黨的防範有漏洞','執政核心多次有人涉案；二審判決變輕，在野黨批評判太輕。<sup><a href="#s21">21</a></sup><sup><a href="#s23">23</a></sup>')],
 '「真戰爭」這半句另外整理在下面：動機查不到，但「路線會不會導致戰爭」可以討論。滲透是不是真的，可以查證；口號有沒有被濫用，答案在你。依據都在下面 ↓')
fs=facts.replace('<h2 id="h-facts">那「反共」是假議題嗎？</h2>','<h2 id="h-facts">拆開來看</h2>')
WAR='''
  <section id="war" class="shell chapter" aria-labelledby="h-war">
    <header>
      <div class="marker">另一半句</div>
      <h2 id="h-war">「真戰爭」這半句怎麼看</h2>
      <p class="intro">這半句可以有兩種讀法。一種講動機，一種講後果，能討論的程度不一樣。</p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>讀法一：民進黨「想要」戰爭</b>
        <p>這是動機，查不到</p>
        <ul class="ev">
          <li>民進黨的公開說法是：增加國防投資是為了嚇阻戰爭，強化防衛不是放棄對話。<sup><a href="#s63">63</a></sup></li>
          <li>民進黨也表示不會另外宣布台灣獨立，只要對等尊嚴，願意與中國官方交流。<sup><a href="#s67">67</a></sup><sup><a href="#s47">47</a></sup></li>
          <li>但公開說法一樣證明不了真正的動機。動機這一題，兩邊都只能各說各話。</li>
        </ul>
      </div>
      <div class="q">
        <b>讀法二：民進黨的路線「會導致」戰爭</b>
        <p>這是因果，可以討論</p>
        <ul class="ev">
          <li>批評者認為，民進黨的台獨路線刺激北京採取軍事威脅。<sup><a href="#s49">49</a></sup></li>
          <li>馬英九強調，他執政 8 年台海平靜。<sup><a href="#s65">65</a></sup></li>
          <li>2016 年後官方對話停擺，兩岸緊張確實升高。<sup><a href="#s51">51</a></sup></li>
        </ul>
      </div>
    </div>

    <div class="defs">
      <h3>「導致」要成立，需要兩個條件</h3>
      <div class="defs-grid two">
        <div><b>條件一：壓力主要是衝著民進黨來？</b><p>支持的一方指出 2016 年後緊張升高。<sup><a href="#s51">51</a></sup> 質疑的一方指出，北京在國民黨執政時也沒有放棄武力<sup><a href="#s64">64</a></sup>；中國海警近年也在日本與那國島附近海域宣示主權，日本多次抗議。<sup><a href="#s66">66</a></sup></p></div>
        <div><b>條件二：換一條路線，就能避免？</b><p>另一條路線的條件是接受九二共識。<sup><a href="#s19">19</a></sup> 北京 2019 年後的定義是「同屬一個中國，共同努力謀求國家統一」<sup><a href="#s28">28</a></sup>；國民黨則主張九二共識是一中各表。<sup><a href="#s29">29</a></sup></p></div>
      </div>
    </div>

    <p class="callout">所以這一題最後會變成取捨：降低緊張的條件，是接受北京定義的前提；而這個前提未來會不會鬆動，目前沒有人能保證。</p>
    <a class="hub-card" href="war.html"><span class="tag">完整整理</span><h2>嚇阻、和解，誰讓台灣更危險？</h2><p>嚇阻路線與和解路線，各自的主張、理由與被批評之處。</p><span class="go">閱讀 →</span></a>
    '''+btn('war')+'''
  </section>
'''
a2=a2h+'\n'+relabel(fs,'依據')+'\n'+WAR+'\n'+faqsec('常聽到的說法','共諜的話題，兩邊都有常聽到的說法。拆開來看：哪裡有根據，哪裡說過頭了。',[re.sub(r'\s*<div class="ask-ai-wrap">.*?</div>','',faq_spies,flags=re.S),'''      <article class="faq-item said" id="said-zhu">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>朱立倫</strong><span>時任國民黨主席 · 2025 年 7 月 20 日 · 報導轉述</span></div>
        <blockquote class="said-q">民進黨罷免號稱反共，但共諜都在綠營，是「假反共真戰爭」。<sup><a href="#s62">62</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>2025 年確實有多名民進黨前幕僚、黨工涉共諜案，遭起訴、除名。<sup><a href="#s23">23</a></sup><sup><a href="#s21">21</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>共諜不只在綠營：國民黨前議員助理也有案件在查，國民黨背景人士因收中資介選被判刑定讞；2024 年起訴的 64 人中，六成以上是現役或退役軍人。<sup><a href="#s2">2</a></sup><sup><a href="#s35">35</a></sup><sup><a href="#s1">1</a></sup></p></div>
        </div>
        <p class="analogy">他同時強調，「反對共產主義是國民黨的黨章」。<sup><a href="#s62">62</a></sup></p>
      </article>''','''      <a class="hub-card" href="label.html">
        <span class="tag">另一邊常聽到的說法</span>
        <h2>「投藍白就是投共產黨！」</h2>
        <p>這句話另外整理成一篇：藍營和北京的往來、法院判決、政黨立場與選民想法。</p>
        <span class="go">閱讀 →</span>
      </a>'''])
page('articles/anti-communism.html','「假反共真戰爭」沒說的另一半是？','「假反共真戰爭」混了好幾件事：滲透是否存在、口號是否被操作、防範是否有漏洞。共諜數據、各方說法與出處。',a2+'</main>\n<!--x-->'+close('你會分開判斷嗎？',['「政黨把議題當口號」和「威脅是否真實存在」，你會分開判斷嗎？','黨內有人涉案，你會怎麼看那個政黨？要看人數，還是看怎麼處理？'],None),1)

# --- Article 3: defense
a3h=hero('2026 國防特別條例','國防預算，到底在吵什麼？','三黨都支持對美軍購，吵的是錢怎麼花、怎麼管。',[
 ('#t-defense','分歧在金額、國內產業與監督方式','政院版 1.25 兆、8 年；藍白合推的版本上限 7800 億，比政院版少約 4700 億，並排除國內委製與商購。<sup><a href="#s12">12</a></sup><sup><a href="#s15">15</a></sup>'),
 ('#t-defense','雙方都有批評','國防部批評在野版本缺乏戰略構想，美國國務院稱延後經費是對中共讓步；在野則認為未定項目不宜空白授權、要加強監督。<sup><a href="#s14">14</a></sup><sup><a href="#s15">15</a></sup><sup><a href="#s13">13</a></sup>'),
 ('#faq','背後是兩種策略','一種主張避免刺激、交流降溫；一種主張投資不對稱戰力，提高對方動武的代價。<sup><a href="#s12">12</a></sup>')],
 '預算規模與監督怎麼取捨，答案在你。依據都在下面 ↓')
d=defense.replace('<div class="issue">','<div class="issue" id="t-defense">',1)
a3=a3h+'\n  <section class="shell chapter" aria-labelledby="h-def">\n    <header>\n      <div class="marker">依據</div>\n      <h2 id="h-def">三黨各自的版本</h2>\n      <p class="intro">每一黨都看兩件事：實際主張什麼，以及他們自己怎麼解釋。</p>\n    </header>\n'+d+'\n  </section>\n\n'+faqsec('常聽到的一句','國防的話題，常會聽到這一句。',[faq_real])
k=a3.rindex('</section>')
a3=a3[:k]+'''    <a class="hub-card" href="budget.html"><span class="tag">預算攻防</span><h2>「藍白拿預算當人質」</h2><p>國防條例在程序委員會被擋了 7 次，總預算卡了 200 多天：在野開的條件是什麼？</p><span class="go">閱讀 →</span></a>
  '''+a3[k:]
page('articles/defense.html','國防預算，到底在吵什麼？','2026 國防特別條例：政院版 1.25 兆與藍白版 7800 億的差別、各方理由與批評，每段附出處。',a3+'</main>\n<!--x-->'+close('你比較在意哪一個？',['國防規模和預算監督，如果只能優先一個，你會選哪個？','「認清現實」之後，你覺得台灣該往哪個方向走？'],None),1)

# --- Article 4: infiltration & speech
a4h=hero('防滲透與言論管制','防滲透，會不會管太多？','各黨都說要防滲透，分歧在要給政府多大的權力。',[
 ('#t-infil','民進黨擴大管制，國民黨反對現行版本','政院草案讓公務員赴陸全面許可、立委納管；國民黨認為抓到的共諜多是政府官員，卻立法限制民代不合理。<sup><a href="#s7">7</a></sup><sup><a href="#s9">9</a></sup>'),
 ('#t-speech','言論入罰最有爭議','政院版擬處罰鼓吹武力犯台的言論；支持者說這是民主國家共識，反對者擔心箝制言論自由。草案仍在審查中。<sup><a href="#s16">16</a></sup><sup><a href="#s17">17</a></sup>'),
 ('#t-infil','也有共識的時候','2022 年國安法增訂經濟間諜罪，朝野協商同意禁止採購中國軍品。<sup><a href="#s11">11</a></sup>')],
 '國安和自由怎麼取捨，答案在你。依據都在下面 ↓')
inf=infil.replace('<div class="issue">','<div class="issue" id="t-infil">',1)
sp=speech.replace('<div class="issue">','<div class="issue" id="t-speech">',1)
a4=a4h+'\n  <section class="shell chapter" aria-labelledby="h-inf">\n    <header>\n      <div class="marker">依據</div>\n      <h2 id="h-inf">三黨各自的立場</h2>\n      <p class="intro">每一黨都看兩件事：實際做了什麼，以及他們自己怎麼解釋。</p>\n    </header>\n'+inf+'\n    <a class="hub-card" href="legislators.html"><span class="tag">立委赴陸許可制</span><h2>「明明抓到的共諜都是政府官員，現在卻立法限制民代」</h2><p>草案的兩個理由：防洩密，和讓選民知道立委去了哪裡、見了誰。</p><span class="go">閱讀 →</span></a>\n\n'+sp+'\n  </section>\n'
page('articles/infiltration.html','防滲透，會不會管太多？','防範中共滲透與言論管制：三黨各自做了什麼、怎麼解釋，每段附出處。',a4+'</main>\n<!--x-->'+close('你最不能讓步的是哪一個？',['國家安全、言論自由、行動自由，如果要取捨，你最不能讓步的是哪一個？','管制對象該到哪裡為止：公務員、民意代表，還是一般人？'],None),1)

# --- Hub
cards=[
 ('articles/war.html','核心問題','嚇阻、和解，誰讓台灣更危險？','兩邊都說要和平，吵的是怎麼得到：嚇阻路線與和解路線，各自的理由與代價。'),
 ('articles/exchange.html','兩岸交流','「逢中必反、逢交流必擋」','對了一半：民間往來沒斷，雙方都設了限制；官方對話卡在北京要求先承認九二共識。'),
 ('articles/label.html','政黨標籤','「投藍白就是投共產黨！」','把好幾件事綁在一起：藍營和北京確實往來密切，但被判刑的是個人，政黨立場也不同。'),
 ('articles/anti-communism.html','共諜與口號','「假反共真戰爭」','混了好幾件事：滲透是真的、不分藍綠；口號有沒有被操作，各方看法不同。'),
 ('articles/consensus.html','九二共識','「九二共識就是一國兩制」','說的是北京的版本：北京已把九二共識和統一綁在一起，國民黨則主張一中各表、拒絕一國兩制。'),
 ('articles/budget.html','預算攻防','「藍白拿預算當人質」','預算確實被擋了很久；沒說的是在野的條件：總預算要行政院先編軍警消預算，國防條例要總統先來報告。'),
 ('articles/legislators.html','立委赴陸','「明明抓到的共諜都是政府官員，現在卻立法限制民代」','回應了一個理由，沒回應另一個：草案要防洩密，也要讓選民知道立委去了哪裡、見了誰。'),
 ('articles/defense.html','國防預算','國防預算，到底在吵什麼？','三黨都支持對美軍購，吵的是金額、國內產業與監督方式。'),
 ('articles/infiltration.html','防滲透與言論','防滲透，會不會管太多？','各黨都說要防滲透，分歧在要給政府多大的權力。'),
]
planned=[('美國與台灣','「美國誰會理我們？」'),('兩岸關係','「兩岸為什麼不能和平共處？」')]
cs='\n'.join(f'''      <a class="hub-card" id="card-{h.split('/')[-1][:-5]}" href="{h}">
        <span class="tag">{t}</span>
        <h2>{ti}</h2>
        {'<span class="half">沒說的另一半是？</span>' if ti.startswith('「') else ''}
        <p>{d}</p>
        <span class="go">閱讀 →</span>
      </a>''' for h,t,ti,d in cards)
ps='\n'.join(f'''      <div class="hub-card planned">
        <span class="tag">{t} · 整理中</span>
        <h2>{ti}</h2>
      </div>''' for t,ti in planned)
hub=f'''  <section class="shell hero" aria-labelledby="title">
    <div class="marker">兩岸與國安</div>
    <h1 id="title">他們講一半，你別只聽一半</h1>
    <p class="after">藍綠都有只講一半的時候。每篇從一句常聽到的話出發，把被省略的那一半補回來，每段附出處，不替你下結論。</p>
  </section>

  <section class="shell chapter" aria-labelledby="h-list">
    <header>
      <div class="marker">議題</div>
      <h2 id="h-list">目前整理好的</h2>
    </header>
    <div class="hub-list">
{cs}
{ps}
    </div>
  </section>

  <section class="shell chapter method" aria-labelledby="h-method">
    <header>
      <div class="marker">整理原則</div>
      <h2 id="h-method">怎麼整理的</h2>
    </header>
    <ul>
      <li>每一句事實都附報導出處，點編號就能查。</li>
      <li>各黨的理由用他們自己公開說過的話，不替任何一方改寫。</li>
      <li>藍綠兩邊常聽到的說法都拆，用同一套方式。</li>
      <li>不收錄未經證實的指控；查不到的就標「資料不足」。</li>
      <li>每篇都有「複製提示詞」按鈕，可以拿去問你自己的 AI 交叉查證。</li>
    </ul>
  </section>
'''
page('index.html','他們講一半，你別只聽一半','藍綠都有只講一半的時候。從常聽到的說法出發，把被省略的那一半補回來，每段附出處，不替你下結論。',hub+'</main>\n',0)


# --- Article 5: label (green claim)
sources.update({
52:("https://www.thenewslens.com/article/255836","關鍵評論網（轉載德國之聲）：大罷免與「反共」訴求、民調"),
53:("https://newtalk.tw/news/view/2025-06-27/978715","新頭殼：民進黨中國部批國民黨照抄國台辦"),
54:("https://www.thenewslens.com/article/255376","關鍵評論網：罷免理由與立委答辯書"),
55:("https://newtalk.tw/news/view/2026-03-04/1022584","新頭殼：民進黨發言人韓瑩批鄭麗文投書"),
56:("https://udn.com/news/story/6656/9561979","聯合報：鄭麗文接受美國公共廣播專訪"),
57:("https://newtalk.tw/news/view/2026-04-20/1030800","新頭殼：鄭習會後中國宣布十項措施，國民黨回應"),
58:("https://udn.com/news/story/124750/9307045","聯合報：國共智庫論壇共同意見，陸委會批配合統戰"),
})
a5h=hero('民進黨大罷免文宣：「罷免投同意，反共更有力」<a href="#said">看出處 ↓</a>','「投藍白就是投共產黨！」','這句話把好幾件事綁在一起了。',[
 ('#ties','藍營和北京確實往來密切','國民黨主席會見習近平、立委組團訪北京、出席海峽論壇；也有國民黨背景人士因收中資介選被判刑定讞。<sup><a href="#s57">57</a></sup><sup><a href="#s52">52</a></sup><sup><a href="#s35">35</a></sup>'),
 ('#stance','但被判刑的是個人，政黨立場也不同','國民黨表示拒絕一國兩制、主張一中各表；藍白版國防條例也包含對美軍購。<sup><a href="#s48">48</a></sup><sup><a href="#s29">29</a></sup><sup><a href="#s12">12</a></sup>'),
 ('#voters','選民也會分開判斷','民調中近七成反感中共，但其中不到一半認為投同意罷免才更能反共；大罷免 31 案全數未通過。<sup><a href="#s52">52</a></sup><sup><a href="#s30">30</a></sup>')],
 '「和北京往來」算不算「投共」，答案在你。依據都在下面 ↓')
a5body='''
  <section class="shell chapter" aria-labelledby="h-l5">
    <header>
      <div class="marker">依據</div>
      <h2 id="h-l5">拆開來看</h2>
      <p class="intro">這句話裡至少有四件事：和北京的往來、法院的判決、政黨的正式立場，以及選民怎麼想。</p>
    </header>
    <div class="qpair">
      <div class="q" id="ties">
        <b>和北京的往來</b>
        <p>有根據的部分</p>
        <ul class="ev">
          <li>2024 年 4 月，國民黨團總召傅崐萁率 16 位立委訪北京，會晤中國全國政協主席王滬寧。<sup><a href="#s52">52</a></sup></li>
          <li>2026 年國民黨主席鄭麗文訪陸會見習近平，北京隨後宣布十項交流措施。<sup><a href="#s57">57</a></sup></li>
          <li>國共智庫論壇的共同意見，包括推動解除政府對兩岸人員往來的限制；陸委會批評這是配合中共統戰。<sup><a href="#s58">58</a></sup></li>
          <li>國民黨副主席率團出席政府定位為統戰平台的海峽論壇。<sup><a href="#s18">18</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>法院判了什麼</b>
        <p>有根據，但限於個人</p>
        <ul class="ev">
          <li>曾代表國民黨參選的地方人士，因收中國資助招待村里長赴中旅遊、介入選舉，被判刑定讞。<sup><a href="#s35">35</a></sup></li>
          <li>涉入共諜案的也不只一黨，民進黨前幕僚黨工也有人被判刑。<sup><a href="#s2">2</a></sup></li>
        </ul>
      </div>
      <div class="q" id="stance">
        <b>政黨的正式立場</b>
        <p>這句話沒提到的</p>
        <ul class="ev">
          <li>國民黨主張九二共識是「一中各表」，並表示拒絕一國兩制。<sup><a href="#s29">29</a></sup><sup><a href="#s48">48</a></sup></li>
          <li>藍白合推的國防條例版本，內容就是對美軍購。<sup><a href="#s12">12</a></sup><sup><a href="#s14">14</a></sup></li>
          <li>國民黨被罷免的立委答辯時表示，赴中是為地方爭取觀光與農漁產品，並稱罷免是政治鬥爭。<sup><a href="#s54">54</a></sup></li>
        </ul>
      </div>
      <div class="q" id="voters">
        <b>選民怎麼想</b>
        <p>這句話沒提到的</p>
        <ul class="ev">
          <li>2025 年 6 月的民調，69.8% 民眾反感中國共產黨，但其中只有 47.4% 認為投同意罷免，台灣才更有力量反抗中共。<sup><a href="#s52">52</a></sup></li>
          <li>2025 年大罷免 31 個選區全數未通過。<sup><a href="#s30">30</a></sup></li>
          <li>有評論認為，點名「在地協力者」能提高警覺，但濫用就會變成標籤政治。<sup><a href="#s36">36</a></sup></li>
        </ul>
      </div>
    </div>
    '''+btn('label')+'''
  </section>

  <section id="said" class="shell chapter" aria-labelledby="h-said5">
    <header>
      <div class="marker">誰這樣說過</div>
      <h2 id="h-said5">把整個政黨等同中共的說法</h2>
      <p class="intro">這個說法主要出現在民進黨的文宣與發言。這裡只看那句話少了什麼，不評論說話的人。</p>
    </header>
    <div class="faq">
      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>民進黨大罷免文宣</strong><span>2025 年 · 宣傳口號</span></div>
        <blockquote class="said-q">「罷免投同意，反共更有力」<sup><a href="#s52">52</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>被罷免的部分國民黨立委，曾組團訪北京會晤中共高層。<sup><a href="#s52">52</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>罷免的是個別立委，罷免理由也包括國會法案與預算爭議；反感中共的民眾中，不到一半認同這個說法。<sup><a href="#s52">52</a></sup></p></div>
        </div>
        <p class="analogy">後來的結果：大罷免 31 案全數未通過。<sup><a href="#s30">30</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>民進黨中國事務部</strong><span>2025 年 6 月 27 日 · 臉書發文</span></div>
        <blockquote class="said-q">國民黨的反應「完全照抄國台辦的新聞稿」，是只會當「中國留聲機」的政黨。<sup><a href="#s53">53</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>國台辦確實公開評論大罷免，呼籲台灣民眾反對民進黨的「政治操弄」。<sup><a href="#s53">53</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>和國台辦立場相同，不等於照抄或受指示。國民黨反對罷免的理由，是認為這是政治鬥爭、赴中是為地方爭取觀光與農漁產品。<sup><a href="#s54">54</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：目前沒有找到。</p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>韓瑩</strong><span>民進黨發言人 · 2026 年 3 月 4 日 · 報導轉述</span></div>
        <blockquote class="said-q">鄭麗文表面上說「不選邊」，實際上卻是選擇站在中共那邊。<sup><a href="#s55">55</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>鄭麗文主張九二共識、反對台獨，並在 2026 年會見習近平。<sup><a href="#s47">47</a></sup><sup><a href="#s57">57</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>鄭麗文那篇投書的主張，是台灣不必在美中之間被迫選邊、要保有戰略自主。<sup><a href="#s55">55</a></sup> 她也表示國民黨支持國防，並先通過對美軍售。<sup><a href="#s56">56</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：目前沒有找到。</p>
      </article>
    </div>
  </section>
'''
page('articles/label.html','「投藍白就是投共產黨！」沒說的另一半是？','「投藍白就是投共產黨」把好幾件事綁在一起：和北京的往來、法院判決、政黨立場與選民想法。各方說法與出處。',a5h+a5body+'</main>\n<!--x-->'+close('界線在哪裡？',['「和北京往來」和「替北京做事」，你覺得界線在哪裡？','一個政黨裡有人被判刑，能代表整個政黨嗎？反過來也一樣嗎？'],None),1)

# --- Article 6: consensus (green claim)
sources.update({
59:("https://www.cna.com.tw/news/acn/201902270358.aspx","中央社：陸否認一中各表，學者稱不再允許戰略模糊（2019）"),
60:("https://newtalk.tw/news/view/2019-01-09/192007","新頭殼：蔡英文說明不接受九二共識，吳敦義回應（2019）"),
61:("https://www.nownews.com/news/6845986","NOWnews：鄭麗文談一中憲法與九二共識"),
})
a6h=hero('民進黨立委鍾佳濱的原話<a href="#said">看出處 ↓</a>','「九二共識就是一國兩制」','這句話說的是北京的版本。',[
 ('#bj','北京的九二共識，已經和統一綁在一起','2019 年習近平定調為「同屬一個中國，共同努力謀求國家統一」，並與「和平統一、一國兩制」一起提出；北京官媒強調其中沒有「各表」。<sup><a href="#s28">28</a></sup><sup><a href="#s29">29</a></sup>'),
 ('#kmt','國民黨的九二共識是「一中各表」','國民黨表示拒絕一國兩制，並主張一國兩制的台灣方案不是九二共識的內涵。<sup><a href="#s29">29</a></sup><sup><a href="#s48">48</a></sup><sup><a href="#s60">60</a></sup>'),
 ('#bj','卡在北京不承認「各表」','前國台辦副主任說，國民黨把九二共識解釋為一中各表是扭曲原意。<sup><a href="#s59">59</a></sup> 所以爭議不只是定義，還有北京接受哪一個版本。')],
 '北京不承認「各表」時，接受九二共識代表什麼，答案在你。依據都在下面 ↓')
a6body='''
  <section class="shell chapter" aria-labelledby="h-c6">
    <header>
      <div class="marker">依據</div>
      <h2 id="h-c6">三方各自怎麼說</h2>
      <p class="intro">同一個詞，三方講的是不同的東西。</p>
    </header>
    <div class="qpair">
      <div class="q" id="bj">
        <b>北京</b>
        <p>同屬一中，謀求統一</p>
        <ul class="ev">
          <li>2019 年習近平定調九二共識為「海峽兩岸同屬一個中國，共同努力謀求國家統一」，並以「和平統一、一國兩制」為目標。<sup><a href="#s28">28</a></sup></li>
          <li>國台辦表示，共同努力謀求國家統一是九二共識的「應有之義」；前國台辦副主任說，一中各表是扭曲原意。<sup><a href="#s59">59</a></sup></li>
          <li>2022 年北京官媒強調，九二共識只有「一中」，沒有「各表」。<sup><a href="#s29">29</a></sup></li>
        </ul>
      </div>
      <div class="q" id="kmt">
        <b>國民黨</b>
        <p>一中各表，拒絕一國兩制</p>
        <ul class="ev">
          <li>國民黨團表示，九二共識就是「一中各表」，北京官媒的說法是斷章取義，國民黨不會接受。<sup><a href="#s29">29</a></sup></li>
          <li>2019 年時任主席吳敦義表示，一國兩制台灣方案並非九二共識的內涵，兩者並不相干。<sup><a href="#s60">60</a></sup></li>
          <li>現任主席鄭麗文主張回到「九二共識、反對台獨」，並以中華民國憲法為基礎。<sup><a href="#s61">61</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>民進黨</b>
        <p>不接受北京定義的九二共識</p>
        <ul class="ev">
          <li>承認 1992 年香港會談的歷史事實，但不承認存在「九二共識」。<sup><a href="#s28">28</a></sup></li>
          <li>2019 年蔡英文表示，不接受的根本原因是北京所定義的九二共識，就是一個中國、一國兩制。<sup><a href="#s60">60</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>這代表什麼</b>
        <p>爭議在「哪一個版本」</p>
        <ul class="ev">
          <li>北京與國民黨用同一個詞，但一方強調統一、一方強調各表；北京近年明確不承認各表。<sup><a href="#s29">29</a></sup><sup><a href="#s59">59</a></sup></li>
          <li>有學者分析，北京認為「各表」讓中華民國保有存在空間，因此不再允許這種模糊。<sup><a href="#s59">59</a></sup></li>
        </ul>
      </div>
    </div>
    '''+btn('parity')+'''
  </section>

  <section id="said" class="shell chapter" aria-labelledby="h-said6">
    <header>
      <div class="marker">誰這樣說過</div>
      <h2 id="h-said6">兩邊都只講了一半</h2>
      <p class="intro">這裡只看那句話少了什麼，不評論說話的人。</p>
    </header>
    <div class="faq">
      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>鍾佳濱</strong><span>民進黨立委 · 回應鄭麗文 · 公開發言</span></div>
        <blockquote class="said-q">「九二共識就是一國兩制……因此在台灣沒有人會接受。」<sup><a href="#s47">47</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>北京確實把九二共識與統一、一國兩制綁在一起提出。<sup><a href="#s28">28</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>這是北京的版本。國民黨的版本是一中各表、拒絕一國兩制<sup><a href="#s29">29</a></sup><sup><a href="#s48">48</a></sup>；國民黨也正是主張接受九二共識的一方，「沒有人會接受」並不精確。</p></div>
        </div>
        <p class="analogy">對照：同一個立場，蔡英文 2019 年的說法加上了「北京所定義的」這個前提。<sup><a href="#s60">60</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>曾銘宗</strong><span>時任國民黨團總召 · 2022 年 9 月 · 公開發言</span></div>
        <blockquote class="said-q">「當然有『九二共識，一中各表』。」<sup><a href="#s29">29</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>國民黨長期以來確實以一中各表理解九二共識，並拒絕一國兩制。<sup><a href="#s29">29</a></sup><sup><a href="#s48">48</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>北京並不承認「各表」：官媒強調只有一中、沒有各表<sup><a href="#s29">29</a></sup>，前國台辦副主任也說一中各表是扭曲原意。<sup><a href="#s59">59</a></sup> 只有一方承認的「各表」，能不能在兩岸對話中成立，是另一個問題。</p></div>
        </div>
        <p class="analogy">他同時表示，北京若只片面擷取一段，國民黨不會接受，台灣民眾也不會接受。<sup><a href="#s29">29</a></sup></p>
      </article>
    </div>
  </section>
'''
page('articles/consensus.html','「九二共識就是一國兩制」沒說的另一半是？','「九二共識就是一國兩制」說的是北京的版本。北京、國民黨、民進黨各自怎麼定義九二共識，以及爭議卡在哪裡，每段附出處。',a6h+a6body+'</main>\n<!--x-->'+close('你怎麼看？',['如果北京不承認「各表」，你覺得接受九二共識代表什麼？','討論九二共識時，你會先問對方指的是哪一個版本嗎？'],None),1)

# --- Article 7: war/peace
sources.update({
68:("https://www.nownews.com/news/6340920","NOWnews：賴清德選前國際記者會談和平與嚇阻（2024/1）"),
69:("https://udn.com/news/story/6656/9592503","聯合報：鄭麗文稱「和平是唯一的選擇」"),
70:("https://n.yam.com/Article/20260521329968","蕃新聞：軍事嚇阻還是政治和解？台海和平路徑如何抉擇"),
71:("https://news.tvbs.com.tw/politics/3088328","TVBS：賴清德元旦談話，投資國防等於投資和平"),
72:("https://www.nownews.com/news/6733281","NOWnews：賴清德稱和平靠實力，國防預算目標"),
73:("https://news.tvbs.com.tw/politics/2522055","TVBS：馬辦批「引戰總統」，賴清德回應"),
108:("https://n.yam.com/Article/20260520613559","上報（蕃新聞轉載）：賴清德就職 2 週年談話全文（2026/5/20）"),
74:("https://news.pts.org.tw/article/824936","公視：2026 中共軍力報告書，登陸作戰能力仍不足"),
75:("https://newtalk.tw/news/view/2025-12-24/1011427","新頭殼：國防部引美方報告談 2027，王定宇批藍白擋預算"),
76:("https://news.tvbs.com.tw/politics/2974360","TVBS：中共軍力報告列出可能犯台時機"),
77:("https://udn.com/news/story/124870/9506331","聯合報：川普稱不希望有人走向獨立"),
78:("https://www.ettoday.net/news/20260520/3168899.htm","ETtoday：美駐中大使稱不支持台獨、也不想見到脅迫"),
79:("https://www.ettoday.net/news/20260516/3167004.htm","ETtoday：學者認為川普「獨立」說法被曲解"),
80:("https://news.tvbs.com.tw/politics/3207112","TVBS：張榮恭稱川普拒絕「倚美謀獨」"),
81:("https://money.udn.com/money/story/6721/9367078","經濟日報（中央社）：訪談 149 名美中台菁英，台海戰爭可能性低"),
83:("https://www.defensepriorities.org/wp-content/uploads/2025/10/DEFP_Grand_strategy_Deterrence.pdf","Defense Priorities：嚇阻與螺旋模型（引 Jervis 1976）"),
84:("https://encyclopedia.ushmm.org/content/zh/article/neville-chamberlain","美國大屠殺紀念館百科：張伯倫與綏靖政策"),
106:("https://www.mnd.gov.tw/File/29432","國防部網站：高旻生〈八二三砲戰勝利 60 週年－作戰整備之研究〉（2018）"),
107:("https://www.mnd.gov.tw/File/29455","陸軍學術雙月刊第 560 期：〈紀念金門「八二三」砲戰勝利 60 周年之體認與啟示〉（2018/8）"),
86:("https://www.ettoday.net/news/20180606/1184915.htm","ETtoday：1996 台海飛彈危機，美國派兩艘航母"),
87:("https://www.britannica.com/print/article/434415","大英百科：西德東方政策（Ostpolitik）"),
88:("https://newtalk.tw/news/view/2022-08-12/800794","新頭殼：回顧 1995–96 台海飛彈危機的起因與經過"),
89:("https://www.thenewslens.com/article/2019","關鍵評論網：兩岸關係大事記（辜汪會談等）"),
90:("https://www.chinatimes.com/opinion/20210820001913-262107","中國時報投書：1995 年海協會推遲兩會協商的回顧"),
})
a7h=hero('國民黨主席鄭麗文：「和平是唯一的選擇」 · 總統賴清德：「和平靠實力」<a href="#said">看出處 ↓</a>','嚇阻、和解，誰讓台灣更危險？','兩邊都說要和平，吵的是怎麼得到。',[
 ('#routes','兩邊都說和平是唯一選項','賴清德 2024 年也說過「和平是唯一的選項」，但主張靠國防嚇阻；國民黨主張回到九二共識、靠交流降低衝突。<sup><a href="#s68">68</a></sup><sup><a href="#s69">69</a></sup><sup><a href="#s70">70</a></sup>'),
 ('#facts7','北京的武力選項，在兩條路線下都在','國防部評估共軍演訓朝封鎖與登陸發展，但登陸能力仍不足；北京在國民黨執政時也沒有放棄武力。<sup><a href="#s74">74</a></sup><sup><a href="#s64">64</a></sup>'),
 ('#facts7','美國的態度，兩邊都拿來用','川普說不希望有人走向獨立、台灣不要期待無條件軍事支持；美方也表示對台政策沒變、不想見到脅迫。<sup><a href="#s77">77</a></sup><sup><a href="#s78">78</a></sup>')],
 '嚇阻和和解哪一條比較安全，沒有人能事先證明。依據都在下面 ↓')
a7body='''
  <section id="routes" class="shell chapter" aria-labelledby="h-r7">
    <header>
      <div class="marker">依據</div>
      <h2 id="h-r7">兩條路線</h2>
      <p class="intro">每條路線都看三件事：主張什麼、為什麼、被怎麼批評。</p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>嚇阻路線 · 民進黨政府</b>
        <p>和平要靠實力</p>
        <ul class="ev">
          <li><strong>主張</strong>：增加國防投資，賴清德說「投資國防，就等於在投資和平」；國防預算目標 2030 年前達 GDP 5%。<sup><a href="#s71">71</a></sup><sup><a href="#s72">72</a></sup>也說「台灣願意在對等、尊嚴的原則下，與中國展開健康有序的交流」，但拒絕「以和平包裝統一」。<sup><a href="#s108">108</a></sup></li>
          <li><strong>理由</strong>：和平不能寄望侵略者的善意；接受一個中國原則的主張，「不是真正的和平」。<sup><a href="#s72">72</a></sup><sup><a href="#s68">68</a></sup></li>
          <li><strong>被批評</strong>：馬英九辦公室批評賴清德是「引戰的總統」<sup><a href="#s73">73</a></sup>；也有分析認為，純粹對抗可能引發螺旋上升的危機。<sup><a href="#s70">70</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>和解路線 · 國民黨</b>
        <p>降低衝突保和平</p>
        <ul class="ev">
          <li><strong>主張</strong>：回到「九二共識、反對台獨」，重新執政後全面重啟兩岸交流、建立互信機制；也表示支持國防，先通過對美軍售。<sup><a href="#s61">61</a></sup><sup><a href="#s56">56</a></sup></li>
          <li><strong>理由</strong>：北京無法接受法理台獨，持續強化「互不隸屬」只會讓北京覺得統一時機流失，提高衝突風險。<sup><a href="#s70">70</a></sup></li>
          <li><strong>被批評</strong>：賴清德認為沒有主權的和平是「假和平」<sup><a href="#s68">68</a></sup>；北京 2019 年後的九二共識定義包含「謀求國家統一」<sup><a href="#s28">28</a></sup>；也有分析認為，純粹讓步容易受經濟脅迫。<sup><a href="#s70">70</a></sup></li>
        </ul>
      </div>
    </div>
    '''+btn('war')+'''
  </section>


  <section id="history" class="shell chapter" aria-labelledby="h-hist">
    <header>
      <div class="marker">歷史能告訴我們什麼</div>
      <h2 id="h-hist">兩邊都找得到歷史案例</h2>
      <p class="intro">國際關係學者 Robert Jervis 在 1976 年就指出，戰爭有兩種常見的成因：「嚇阻失敗」和「螺旋升級」。兩種都真的發生過，哪一種比較適用，取決於怎麼判斷對方的意圖。<sup><a href="#s83">83</a></sup></p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>嚇阻派常引用的案例</b>
        <p>讓步只會招來更多要求</p>
        <ul class="ev">
          <li><strong>1938 年慕尼黑協定</strong>：英法為避免戰爭，同意納粹德國併吞捷克的蘇台德區，結果沒能阻止二戰，綏靖政策因此通常被認為是失敗的。<sup><a href="#s84">84</a></sup></li>
          <li><strong>1958 年八二三砲戰</strong>：共軍 44 天內對金門發射約 44 萬發砲彈，國軍持續運補固守，美國沒有直接參戰，只以第七艦隊協助護航運補。<sup><a href="#s106">106</a></sup> 10 月 6 日北京宣布暫停砲擊 7 天，條件是美軍不再護航，之後改為「單打雙不打」，直到 1979 年美中建交才停止砲擊。國軍刊物的回顧認為，是守軍堅守讓北京轉而找下台階。<sup><a href="#s107">107</a></sup> 中共官方說法則是：砲擊用意在警告美國，後期調整射擊時間與停火是出於人道考量與毛澤東的戰略思維，並非戰敗。同一份國軍研究也記載，毛澤東砲擊金門的用意之一是牽制美國、聲援中東。<sup><a href="#s106">106</a></sup></li>
          <li><strong>1996 年台海飛彈危機</strong>：北京在台灣首次總統直選前試射飛彈，美國派出兩個航母戰鬥群到台灣附近海域，危機最後沒有擴大。<sup><a href="#s86">86</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>和解派常引用的案例</b>
        <p>互相加碼會失控</p>
        <ul class="ev">
          <li><strong>1914 年第一次世界大戰</strong>：各國都說自己在防衛，互相擴軍結盟，最後演變成大戰。學者常用它說明「螺旋模型」。<sup><a href="#s83">83</a></sup></li>
          <li><strong>1993 年辜汪會談</strong>：兩岸分治 40 多年後首次高層會談，雙方擱置政治爭議、簽下四項事務性協議。<sup><a href="#s89">89</a></sup> 但 1995 年李登輝訪美後，海協會推遲了兩會協商。<sup><a href="#s90">90</a></sup></li>
          <li><strong>2008–2016 年馬英九執政</strong>：兩岸簽署 23 項協議，馬英九強調任內台海平靜。<sup><a href="#s65">65</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>同一件事，兩種讀法</b>
        <p>1995–96 年台海危機</p>
        <ul class="ev">
          <li>起因是李登輝 1995 年訪美後，北京在台灣周邊試射飛彈。<sup><a href="#s88">88</a></sup> 和解派會說：這是刺激北京的後果。</li>
          <li>嚇阻派會說：美國航母到場後危機收場，證明嚇阻有效。<sup><a href="#s86">86</a></sup></li>
          <li>時任美國國防部長裴瑞事後表示，他判斷北京的目的是恫嚇、影響選舉，不是真的要攻擊台灣。<sup><a href="#s86">86</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>每個案例都有限制</b>
        <p>歷史不會原樣重演</p>
        <ul class="ev">
          <li>馬英九時期北京也沒有放棄武力<sup><a href="#s64">64</a></sup>，所以「平靜」也可能是北京當時認為情勢對它有利。</li>
          <li>常被引用的西德「東方政策」和台灣差異很大：東西德互相承認、西德與蘇聯簽約放棄使用武力<sup><a href="#s87">87</a></sup>；北京不承認中華民國，也不放棄武力。</li>
          <li>也有分析認為，成功的案例多半是「實力加對話」並行。<sup><a href="#s70">70</a></sup></li>
          <li>台灣和這些案例都不一樣：北京主張台灣是它的領土，爭的不只是安全，還有主權。</li>
        </ul>
      </div>
    </div>
    <p class="callout">所以兩條路線真正的分歧，是怎麼判斷北京的意圖：如果北京本來就想擴張，讓步會被當成軟弱；如果北京主要是怕台灣走向獨立，加碼嚇阻可能讓雙方越升越高。你比較相信哪一種？</p>
  </section>


  <section id="ends" class="shell chapter" aria-labelledby="h-ends">
    <header>
      <div class="marker">推到極端</div>
      <h2 id="h-ends">兩條路線的最好與最壞</h2>
      <p class="intro">常聽到的說法是「選和解就是選被統一，選嚇阻就是選戰爭」。把兩條路線的結局都攤開來看，會發現兩條路都不只通往一個極端。</p>
    </header>
    <div class="table-wrap">
      <table class="ends">
        <thead><tr><th scope="col"></th><th scope="col">嚇阻路線</th><th scope="col">和解路線</th></tr></thead>
        <tbody>
          <tr><th scope="row">最好的結果</th><td>北京判斷代價太高，維持現狀</td><td>緊張降低，維持現狀</td></tr>
          <tr><th scope="row">最壞的結果之一</th><td>嚇阻失敗，爆發戰爭</td><td>一步步讓步，最後被吸收</td></tr>
          <tr><th scope="row">最壞的結果之二</th><td>打了仗而且輸了：戰爭加上被統一</td><td>讓步後北京仍不滿意：還是可能被威脅動武</td></tr>
        </tbody>
      </table>
    </div>
    <div class="qpair">
      <div class="q">
        <b>兩邊怕的其實一樣</b>
        <ul class="ev">
          <li>打仗不保證能保住民主，和解也不保證不會打仗；北京從未承諾放棄武力。<sup><a href="#s64">64</a></sup></li>
          <li>兩邊的支持者都不想要戰爭，也都不想被統一。</li>
        </ul>
      </div>
      <div class="q">
        <b>分歧在機率</b>
        <ul class="ev">
          <li>嚇阻派認為：讓步會讓「被吸收」的機率大幅升高，嚇阻能把戰爭機率壓低。</li>
          <li>和解派認為：嚇阻會讓戰爭機率升高，交流不必然導致被吸收。</li>
          <li>這些機率沒有人算得出來，所以爭論才會一直持續。</li>
        </ul>
      </div>
    </div>
    <p class="callout">兩岸的現狀已經維持了 70 多年，兩個極端都沒有發生。兩條路線真正爭的，是怎麼讓現狀繼續下去。</p>
  </section>

  <section id="facts7" class="shell chapter" aria-labelledby="h-f7">
    <header>
      <div class="marker">兩條路線都要面對的事實</div>
      <h2 id="h-f7">北京、美國，和其他人怎麼看</h2>
    </header>
    <div class="qpair">
      <div class="q">
        <b>北京的能力</b>
        <ul class="ev">
          <li>國防部 2026 年報告：共軍演訓朝海空封鎖、聯合登陸發展，但登陸作戰能力仍不足。<sup><a href="#s74">74</a></sup></li>
          <li>國防部引述美方報告：中共 2027 年具備對台發動軍事行動的能力。<sup><a href="#s75">75</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>北京的立場</b>
        <ul class="ev">
          <li>不放棄使用武力，國民黨執政時也一樣；馬英九也轉述過習近平這個立場。<sup><a href="#s64">64</a></sup></li>
          <li>美方報告列出的可能犯台時機，包括「台灣正式宣布獨立」，也包括「不斷推遲兩岸和平統一對話進程」。<sup><a href="#s76">76</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>美國的態度</b>
        <ul class="ev">
          <li>川普 2026 年 5 月表示，不希望有人走向獨立，台灣不要期待無條件的軍事支持。<sup><a href="#s77">77</a></sup></li>
          <li>美國駐中大使表示，美國對台政策沒變，不支持台獨，但也不想見到兩岸之間的脅迫。<sup><a href="#s78">78</a></sup> 也有學者認為，川普所說的「獨立」被翻譯得過頭了。<sup><a href="#s79">79</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>其他觀察</b>
        <ul class="ev">
          <li>一項訪談 149 名美中台菁英的研究認為，兩岸戰爭的可能性低。<sup><a href="#s81">81</a></sup></li>
          <li>有分析指出，多數台灣民眾希望維持現狀，但對「現狀」的解釋也分裂；成功的案例多半是「實力加對話」並行。<sup><a href="#s70">70</a></sup></li>
        </ul>
      </div>
    </div>
  </section>

  <section id="said" class="shell chapter" aria-labelledby="h-said7">
    <header>
      <div class="marker">誰這樣說過</div>
      <h2 id="h-said7">兩邊都只講了一半</h2>
      <p class="intro">這裡只看那句話少了什麼，不評論說話的人。</p>
    </header>
    <div class="faq">
      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>張榮恭</strong><span>國民黨副主席 · 2026 年 5 月 18 日 · 報導轉述</span></div>
        <blockquote class="said-q">川普結束北京行程後，公開示警台灣不得「倚美謀獨」。<sup><a href="#s80">80</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>川普確實說不希望有人走向獨立，並提醒台灣不要期待無條件的軍事支持。<sup><a href="#s77">77</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>美國駐中大使同時表示對台政策沒變，也不想見到兩岸之間的脅迫<sup><a href="#s78">78</a></sup>；也有學者認為，川普的「獨立」不一定是指台灣宣布獨立。<sup><a href="#s79">79</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：目前沒有找到。</p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>王定宇</strong><span>民進黨立委 · 2025 年 12 月 24 日 · 報導轉述</span></div>
        <blockquote class="said-q">台灣當前面臨的真正困難，不是中國軍力提升，也不是對外軍購的難度，而是國內政治因素：藍白毫無理由地阻擋國防預算。<sup><a href="#s75">75</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>政院版國防條例確實被延宕多時，最後通過的版本比政院版少約 4700 億。<sup><a href="#s15">15</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>藍白後來通過的 7800 億版本，內容就是對美軍購<sup><a href="#s12">12</a></sup>；在野黨也提出了理由，例如預算監督與不宜空白授權，不是「毫無理由」。<sup><a href="#s13">13</a></sup><sup><a href="#s14">14</a></sup></p></div>
        </div>
        <p class="analogy">後來的結果：條例在 2026 年 5 月以 7800 億上限通過。<sup><a href="#s15">15</a></sup></p>
      </article>
    </div>
  </section>
'''
page('articles/war.html','嚇阻、和解，誰讓台灣更危險？','兩邊都說要和平，吵的是怎麼得到：嚇阻路線與和解路線各自的主張、理由與被批評之處，以及北京與美國的態度，每段附出處。',a7h+a7body+'</main>\n<!--x-->'+close('你願意承擔多少？',['為了維持現狀，你願意承擔多少戰爭風險？又願意在主權的說法上讓步多少？','哪一條路，比較能同時避開戰爭和被統一？為什麼？'],None),1)

# --- Article 8: legislators
sources.update({
91:("https://www.gvm.com.tw/article/126890","遠見（中央社）：政院通過兩岸條例修正草案，立委赴中須經許可"),
92:("https://www.thenewslens.com/article/262918","關鍵評論網（中央社）：政院修赴陸規範，邱垂正、李慧芝說明理由"),
93:("https://udn.com/news/story/6656/9227475","聯合報：牛煦庭回應立委赴陸許可制"),
94:("https://www.chinatimes.com/opinion/20260104002470-262110","中國時報評論：赴陸許可制劍指藍白政治人物"),
95:("https://www.mirrormedia.mg/story/20251226edi063","鏡報：翁曉玲批無聊，鍾佳濱稱立法院自找的"),
})
a8h=hero('國民黨立委牛煦庭的原話（2025 年 12 月）<a href="#said">看出處 ↓</a>','「明明抓到的共諜都是政府官員，現在卻立法限制民代」','這句話回應了一個理由，沒回應另一個。',[
 ('#bill','草案是「事前許可」，不只是報備','立委赴陸須經內政部聯審會許可；接觸中共黨政軍機構，返台後還要公開揭露。草案仍在立法院，尚未付委審查。<sup><a href="#s91">91</a></sup><sup><a href="#s17">17</a></sup>'),
 ('#reasons','支持的理由有兩個：防洩密、讓選民監督','陸委會說立委經常接觸國安機密；草案說明則指出，民選公職赴陸的資訊不透明，民眾無從監督。<sup><a href="#s92">92</a></sup><sup><a href="#s91">91</a></sup>'),
 ('#reasons','反對的理由：共諜是官員、民代不該被行政權管','牛煦庭認為被抓的共諜都是政府官員；也有評論認為草案劍指藍白政治人物。<sup><a href="#s9">9</a></sup><sup><a href="#s94">94</a></sup>')],
 '要防洩密、要透明，還是都不需要立法，答案在你。依據都在下面 ↓')
a8body='''
  <section id="bill" class="shell chapter" aria-labelledby="h-b8">
    <header>
      <div class="marker">依據</div>
      <h2 id="h-b8">草案寫了什麼</h2>
      <p class="intro">2025 年 12 月 26 日行政院通過《兩岸人民關係條例》修正草案，送立法院審議。和立委有關的部分如下。</p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>事前許可</b>
        <ul class="ev">
          <li>立委，以及因業務知悉國家機密的人員赴陸，須經內政部聯審會許可。聯審會由內政部會同國安局、法務部、陸委會組成。<sup><a href="#s91">91</a></sup></li>
          <li>涉密人員未經許可赴陸，罰新台幣 200 萬到 1000 萬元。<sup><a href="#s91">91</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>事後揭露</b>
        <ul class="ev">
          <li>民選公職人員赴陸，如接觸中共黨務、軍事、行政或政治性機關團體，返台後要提供時間、地點、事由與過程，由權責機關公開揭露。<sup><a href="#s91">91</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>同一份草案的其他內容</b>
        <ul class="ev">
          <li>公務員赴陸全面改為許可制；曾任正副總統、國安會諮委等人，不得出席妨害國家尊嚴的中共活動。<sup><a href="#s92">92</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>目前進度</b>
        <ul class="ev">
          <li>現行法律並未規範立委赴陸。<sup><a href="#s91">91</a></sup> 陸委會 2026 年 4 月表示，這份修法仍卡在立法院程序委員會，尚未付委審查。<sup><a href="#s17">17</a></sup></li>
        </ul>
      </div>
    </div>
  </section>

  <section id="reasons" class="shell chapter" aria-labelledby="h-r8">
    <header>
      <div class="marker">兩個理由</div>
      <h2 id="h-r8">防洩密，和讓選民知道</h2>
      <p class="intro">支持草案的理由其實有兩個，反對的論點主要回應了第一個。</p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>理由一：防止洩密</b>
        <ul class="ev">
          <li><strong>支持</strong>：陸委會主委邱垂正說，立委問政經常接觸國安機密，若未完整納管，恐會形成漏洞。<sup><a href="#s92">92</a></sup></li>
          <li><strong>反對</strong>：牛煦庭認為，被抓到的共諜都是政府官員，和國會無關。<sup><a href="#s93">93</a></sup></li>
          <li><strong>補充事實</strong>：2025 年的共諜案中，涉案者也包括前立法院長辦公室的助理。<sup><a href="#s23">23</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>理由二：讓選民監督</b>
        <ul class="ev">
          <li><strong>支持</strong>：草案說明指出，民選公職赴陸的交流資訊不透明，民眾無從監督。<sup><a href="#s91">91</a></sup> 沈伯洋說，不是不能去，而是要透明。<sup><a href="#s8">8</a></sup></li>
          <li><strong>例子</strong>：2024 年 4 月有 17 名國民黨立委赴中；北京開放文旦柚進口後，國台辦把功勞歸給特定立委。<sup><a href="#s9">9</a></sup></li>
          <li><strong>反對</strong>：牛煦庭認為，民意代表經選舉產生，權利不應被隨意限制<sup><a href="#s9">9</a></sup>；也有評論認為，這是在強化國安的名義下限制藍白政治人物參與交流。<sup><a href="#s94">94</a></sup></li>
        </ul>
      </div>
    </div>
    <p class="callout">兩個理由需要的工具不一樣：防洩密需要事前審查，讓選民監督只需要事後公開。如果只要求公開揭露、不要求事前許可，兩邊能不能接受？</p>
    '''+btn('legislators')+'''
  </section>

  <section id="said" class="shell chapter" aria-labelledby="h-said8">
    <header>
      <div class="marker">誰這樣說過</div>
      <h2 id="h-said8">兩邊都只講了一半</h2>
      <p class="intro">這裡只看那句話少了什麼，不評論說話的人。</p>
    </header>
    <div class="faq">
      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>牛煦庭</strong><span>國民黨立委 · 2025 年 12 月 · 公開發言</span></div>
        <blockquote class="said-q">「明明抓到的共諜都是政府官員，現在卻立法限制民代，並不合理。」<sup><a href="#s9">9</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>2025 年曝光的共諜案，涉案者多是總統府、外交部長、黨部的幕僚與助理。<sup><a href="#s21">21</a></sup><sup><a href="#s23">23</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>涉案者也包括前立法院長辦公室的助理<sup><a href="#s23">23</a></sup>；而且草案的另一個理由是讓選民知道立委去了哪裡、見了誰，這和有沒有抓到共諜無關。<sup><a href="#s91">91</a></sup></p></div>
        </div>
        <p class="analogy">他同時表示，若民意代表真的出賣台灣、被抓到是共諜，「槍斃不要客氣」。<sup><a href="#s93">93</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>鍾佳濱</strong><span>民進黨立委 · 2025 年 12 月 26 日 · 報導轉述</span></div>
        <blockquote class="said-q">五院裡只有立法院沒有相關規定，立法院自己不訂、行政院幫你訂，也是立法院自找的。<sup><a href="#s95">95</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>現行《兩岸人民關係條例》確實沒有規範立委赴陸；綠營過去提案也被藍白否決。<sup><a href="#s91">91</a></sup><sup><a href="#s95">95</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>依草案，審查立委行程的是內政部聯審會，也就是由行政機關決定民選立委能不能去<sup><a href="#s91">91</a></sup>；反對者擔心的正是這一點，認為把公務員的規範套用到民意代表身上已經越線。<sup><a href="#s9">9</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：目前沒有找到。</p>
      </article>
    </div>
  </section>
'''
page('articles/legislators.html','「明明抓到的共諜都是政府官員」沒說的另一半是？','立委赴陸許可制草案：支持的理由有防洩密與讓選民監督兩個，反對的論點主要回應了第一個。草案內容、各方說法與出處。',a8h+a8body+'</main>\n<!--x-->'+close('你在意的是哪一個？',['你比較在意防洩密，還是讓選民知道立委去了哪裡、見了誰？','如果只要求返台公開揭露、不要求事前許可，你能接受嗎？'],None),1)

# --- Article 9: budget
sources.update({
96:("https://www.businesstoday.com.tw/article/category/183027/post/202601060041/","今周刊：國防特別預算六度遭擋，羅智強、沈伯洋、郭昱晴說法"),
97:("https://news.pts.org.tw/article/790433","公視：國防特別條例第 7 度在程序委員會遭擋"),
98:("https://news.pts.org.tw/article/793282","公視：會期最後院會，總預算未付委創憲政首例"),
99:("https://money.udn.com/money/story/7307/9449587","經濟日報：總預算卡關原因與 4 月 15 日朝野協商"),
100:("https://www.ctee.com.tw/news/20251005700291-430101","工商時報（中央社）：國民黨團擬提復議，政院稱已聲請釋憲"),
101:("https://newtalk.tw/news/view/2026-01-05/1013287","新頭殼：鄭麗文與民進黨吳崢對總預算卡關的說法"),
102:("https://www.thenewslens.com/article/269682","關鍵評論網：115 年度總預算三讀，刪減率 1.69%"),
103:("https://news.pts.org.tw/article/734837","公視：114 年度總預算刪減 2075 億元"),
104:("https://www.taiwannews.com.tw/zh/news/6215960","台灣英文新聞（中央社）：民眾黨團提復議，卓榮泰回應"),
105:("https://www.businesstoday.com.tw/article/category/183027/post/202604210027/","今周刊：115 年總預算 4 月 21 日付委"),
})
a9h=hero('民進黨立委郭昱晴的說法（2026 年 1 月，報導轉述）<a href="#said">看出處 ↓</a>','「藍白拿預算當人質」','預算確實被擋了很久；這句話沒說的，是在野開出的條件。',[
 ('#facts','總預算和國防條例都被擋過','115 年度總預算 2025 年 8 月送進立法院，擋了 200 多天才在 2026 年 4 月 21 日付委；國防特別條例在程序委員會至少被暫緩列案 7 次。<sup><a href="#s105">105</a></sup><sup><a href="#s97">97</a></sup>'),
 ('#why','總預算：在野要行政院先編軍警消預算','立法院三讀、總統公布的軍人加薪與警消退休金，行政院沒編進總預算，理由是有違憲疑慮、已聲請釋憲。<sup><a href="#s99">99</a></sup><sup><a href="#s100">100</a></sup>'),
 ('#why','國防條例：在野要總統先到立法院報告','國民黨說賴清德願意到立法院報告就排付委；民進黨說總統報告和審預算是兩回事。<sup><a href="#s96">96</a></sup>')],
 '擋預算算是監督、施壓，還是拿人民當人質，答案在你。依據都在下面 ↓')
a9body='''
  <section id="facts" class="shell chapter" aria-labelledby="h-f9">
    <header>
      <div class="marker">依據</div>
      <h2 id="h-f9">到底擋了多久</h2>
      <p class="intro">先看時間順序，再看雙方的理由。</p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>前一年：114 年度總預算</b>
        <ul class="ev">
          <li>2025 年 1 月三讀，刪減約 2075 億元，占歲出 6.64%。行政院長卓榮泰批評這是癱瘓政府。<sup><a href="#s103">103</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>115 年度總預算</b>
        <ul class="ev">
          <li>2025 年 8 月 29 日送進立法院。<sup><a href="#s102">102</a></sup></li>
          <li>2025 年 10 月 7 日民眾黨團提復議、國民黨團支持，總預算卡住。<sup><a href="#s99">99</a></sup></li>
          <li>2026 年 1 月會期結束仍未付委，是憲政史上第一次。<sup><a href="#s98">98</a></sup></li>
          <li>2026 年 4 月 21 日付委；8 月 14 日三讀，刪減約 480 億元，刪減率 1.69%，近十年最低。<sup><a href="#s105">105</a></sup><sup><a href="#s102">102</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>國防特別條例（1.25 兆）</b>
        <ul class="ev">
          <li>2025 年 11 月底送進立法院後，在程序委員會一再被暫緩列案；2026 年 1 月 13 日是第 7 次，表決 10 比 8。<sup><a href="#s97">97</a></sup></li>
          <li>後來立法院通過的是藍白合推、上限 7800 億的版本，細節見<a href="defense.html">國防預算那篇</a>。<sup><a href="#s12">12</a></sup></li>
        </ul>
      </div>
    </div>
    <p class="callout">「擋了多久」也有兩種算法：從送案到三讀共 351 天；國民黨則指出，從付委到三讀只有 115 天，和過去幾年的 104 到 152 天差不多。<sup><a href="#s102">102</a></sup></p>
  </section>

  <section id="why" class="shell chapter" aria-labelledby="h-w9">
    <header>
      <div class="marker">在野的條件</div>
      <h2 id="h-w9">兩個案子，兩種條件</h2>
      <p class="intro">「人質」這個說法沒提到的，是在野要的是什麼。</p>
    </header>
    <div class="qpair">
      <div class="q">
        <b>總預算：先編軍警消預算</b>
        <ul class="ev">
          <li><strong>在野</strong>：軍人待遇條例、警察人員人事條例已經三讀並由總統公布，行政院卻沒編進總預算；國民黨團認為依法編列是行政院的憲政義務，不能因為覺得違憲就先不編。<sup><a href="#s99">99</a></sup></li>
          <li><strong>行政院</strong>：這些條文有違憲疑慮，已聲請釋憲；如果憲法法庭認為合憲，會馬上調整並追溯補齊。<sup><a href="#s100">100</a></sup> 卓榮泰也說，立法院要大幅增加支出，應先徵詢行政院、共同找出財源。<sup><a href="#s104">104</a></sup></li>
          <li><strong>怎麼解開的</strong>：2026 年 4 月朝野協商，請卓榮泰到立法院報告軍人加薪、警消退休金的處理情形，報告完就付委。<sup><a href="#s99">99</a></sup></li>
        </ul>
      </div>
      <div class="q">
        <b>國防條例：總統先來報告</b>
        <ul class="ev">
          <li><strong>國民黨</strong>：羅智強說，讓預算被擋 6 次的是賴清德；賴總統願意到立法院報告，就會立刻安排付委。<sup><a href="#s96">96</a></sup></li>
          <li><strong>民進黨</strong>：沈伯洋說，要求總統到立法院即問即答已被憲法法庭宣告違憲；郭昱晴說，總統報告和審不審預算是兩回事。<sup><a href="#s96">96</a></sup></li>
        </ul>
      </div>
    </div>
    <p class="callout">兩個條件不太一樣：總預算的條件和預算內容本身有關，國防條例的條件是請總統來報告。你覺得哪一個算監督，哪一個算施壓？</p>
    '''+btn('budget')+'''
  </section>

  <section id="said" class="shell chapter" aria-labelledby="h-said9">
    <header>
      <div class="marker">誰這樣說過</div>
      <h2 id="h-said9">兩邊都只講了一半</h2>
      <p class="intro">這裡只看那句話少了什麼，不評論說話的人。</p>
    </header>
    <div class="faq">
      <article class="faq-item said">
        <span class="faq-tag">民進黨</span>
        <div class="who"><strong>郭昱晴</strong><span>民進黨立委 · 2026 年 1 月 6 日 · 報導轉述</span></div>
        <blockquote class="said-q">總統報告和審不審預算根本是兩回事，藍白持續拿預算當人質要脅。<sup><a href="#s96">96</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>國防條例被擋時，國民黨開的條件確實是總統到立法院報告；總預算卡關期間，上千億元的新興計畫無法動用。<sup><a href="#s96">96</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>總預算卡住的理由不是總統報告，而是行政院沒編立法院通過的軍人加薪、警消退休金預算；不編也是行政院自己的選擇。<sup><a href="#s99">99</a></sup><sup><a href="#s100">100</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：總預算 2026 年 4 月 21 日付委，8 月 14 日三讀，刪減率 1.69%。<sup><a href="#s102">102</a></sup></p>
      </article>

      <article class="faq-item said">
        <span class="faq-tag">國民黨</span>
        <div class="who"><strong>鄭麗文</strong><span>國民黨主席 · 2026 年 1 月 5 日 · 報導轉述</span></div>
        <blockquote class="said-q">總預算沒辦法順利付委，是因為賴清德不尊重立法院三讀通過的法案。<sup><a href="#s101">101</a></sup></blockquote>
        <div class="split">
          <div><b>有根據的部分</b><p>行政院確實沒把已三讀、公布的軍人待遇與警消相關預算編進總預算。<sup><a href="#s99">99</a></sup></p></div>
          <div><b>這句話沒提到的</b><p>行政院已聲請釋憲，並承諾合憲就追溯補齊<sup><a href="#s100">100</a></sup>；而同一時間被擋的國防條例，國民黨開的條件是總統來報告，和這些法案無關。<sup><a href="#s96">96</a></sup></p></div>
        </div>
        <p class="analogy">後來的補充：2026 年 4 月朝野協商後，總預算在卓榮泰報告完付委。<sup><a href="#s99">99</a></sup></p>
      </article>
    </div>
  </section>
'''
page('articles/budget.html','「藍白拿預算當人質」沒說的另一半是？','2025–2026 年總預算與國防特別條例被擋的經過：擋了多久、在野開的條件、行政院的理由，每段附出處。',a9h+a9body+'</main>\n<!--x-->'+close('擋預算，算不算監督？',['立法院可以用不付委來逼行政院讓步嗎？如果換成另一黨在野，你的答案會一樣嗎？','行政院認為法律違憲時，可以先不編預算、等釋憲結果嗎？'],None),1)
