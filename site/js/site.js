(function () {
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
})();
(function () {
  var TAIL = "\n\n請用繁體中文回答，每個重點附上可查證的來源連結，並盡量平衡呈現不同立場；資料不確定或可能過時的地方請明確說明。";
  var PROMPTS = {
    exchange: "我想查證一個說法：「民進黨都不交流」。請幫我說明：（1）兩岸民間交流（觀光、經商、求學）目前的狀況，以及台灣政府（例如團客赴陸限制、公務員赴陸許可、禁止公職參加海峽論壇）與北京（例如 2019 年暫停陸客自由行）各自設了哪些限制；（2）政黨交流（例如國共論壇、海峽論壇）與官方對話（陸委會與國台辦、海基會與海協會）是否需要以承認「九二共識」為前提，官方聯繫從什麼時候、為什麼停擺；（3）北京、民進黨、國民黨、民眾黨各自對這件事的看法。",
    spies: "有人說「反共是假議題，民進黨自己就抓出一堆共諜」。請幫我把這句話拆成兩個問題分別查證：（1）台灣近年共諜案起訴人數的變化與涉案者身分（例如國安局統計），以及人數變化是否與修法有關；（2）民進黨執政期間黨內人士涉入共諜案的情況、民進黨的處理方式，以及在野黨的批評。最後請說明這句話哪些部分有證據支持、哪些部分沒有。",
    infiltration: "請比較民進黨、國民黨、民眾黨對「防範中共滲透」相關立法的立場與各自提出的理由，包括 2019 年《反滲透法》、《兩岸人民關係條例》修正（例如立委赴中國須事先許可）。請說明支持與反對的主要論點，例如國家安全、程序正義、兩岸交流、言論與行動自由。",
    defense: "請說明 2026 年台灣國防特別條例的立法過程：行政院 1.25 兆元版本、國民黨版本、民眾黨版本，以及最後通過的版本有什麼差異？各黨分別提出了什麼理由？各方對不同版本的主要批評是什麼（例如國防部、美國政府對在野版本的批評，以及在野黨對政院版預算規模、監督與空白授權的批評）？",
    speech: "台灣《國家安全法》修正草案擬將「支持、鼓吹以武力對台發動戰爭」的言論納入處罰。請說明這個草案的內容與目前進度、各政黨的立場與理由，以及「國家安全」和「言論自由」兩方面的主要論點。",
    realism: "有人說「兩岸武力、人力差距很大，台灣要認清現實」。請說明兩岸軍力差距的公開數據（請註明資料來源與年份），以及面對這個差距的不同策略主張，例如交流降溫、避免刺激、發展不對稱戰力嚇阻等，各自的支持論點與主要批評。",
    label: "有人說「投藍白就是投共產黨，國民黨和民眾黨都是中共在地協力者」。請幫我查證：（1）近年有哪些國民黨、民眾黨相關人士因接受中國資助或介入選舉被起訴或判刑，結果如何；（2）政黨層級的兩岸交流（例如出席海峽論壇、國共論壇）的實際內容，以及各方的評價；（3）支持與批評「在地協力者」「中共同路人」這類說法的主要論點。最後請說明這句話哪些部分有證據支持、哪些部分沒有。",
    budget: "有人說「藍白拿預算當人質」。請幫我整理 2025 到 2026 年立法院處理中央政府總預算與國防特別條例的經過：（1）兩案各被擋了多久、在野提出的條件是什麼；（2）行政院沒有編列軍人加薪、警消退休金預算的理由，以及釋憲進度；（3）在野與執政黨各自的說法；（4）過去其他政黨在野時有沒有類似的杯葛先例。請平衡呈現，不要替我下結論。",
    legislators: "行政院 2025 年 12 月通過的《兩岸人民關係條例》修正草案，要求立委赴中國須經許可、接觸中共黨政軍須返台公開揭露。請幫我整理：（1）草案的具體內容與目前立法進度；（2）支持方的理由，包括防止洩密與讓選民監督；（3）反對方的理由，包括民意代表的角色、權力分立與是否針對特定政黨；（4）其他民主國家對國會議員訪問敵對或競爭國家有沒有類似規範。請平衡呈現，不要替我下結論。",
    war: "有人說「民進黨的路線會導致戰爭」。請幫我分別整理：（1）支持這個說法的主要論點與證據，例如 2016 年後兩岸關係的變化；（2）質疑這個說法的主要論點與證據，例如北京在不同執政黨時期對使用武力的立場、中國對其他鄰國的施壓；（3）如果台灣改走接受「九二共識」的路線，北京、國民黨、民進黨各自認為會有什麼結果與代價。請平衡呈現，不要替我下結論。",
    parity: "北京以承認「九二共識」、「兩岸同屬一個中國」作為兩岸官方對話的前提。請說明：「九二共識」在北京、國民黨、民進黨各自的定義有什麼差異？支持台灣接受這個前提、與反對接受的主要論點分別是什麼？這樣的對話條件算不算「對等」，各方怎麼看？"
  };
  function flash(btn, text) {
    var label = btn.querySelector(".ask-ai-label");
    var orig = label.getAttribute("data-orig") || label.textContent;
    label.setAttribute("data-orig", orig);
    label.textContent = text;
    btn.classList.add("done");
    var st = btn.parentNode.querySelector(".ask-ai-status"); if (st) { st.textContent = "提示詞已複製"; setTimeout(function () { st.textContent = ""; }, 2400); }
    clearTimeout(btn._t);
    btn._t = setTimeout(function () { label.textContent = orig; btn.classList.remove("done"); }, 2400);
  }
  function fallback(btn, text) {
    var wrap = btn.parentNode;
    var ta = wrap.querySelector("textarea");
    if (!ta) {
      var hint = document.createElement("p");
      hint.className = "ask-ai-hint";
      hint.textContent = "無法自動複製，請長按或全選下方文字後複製：";
      ta = document.createElement("textarea");
      ta.className = "ask-ai-fallback";
      ta.readOnly = true;
      ta.setAttribute("aria-label", "提示詞");
      wrap.appendChild(hint);
      wrap.appendChild(ta);
    }
    ta.value = text;
    ta.focus();
    ta.select();
    try { ta.setSelectionRange(0, text.length); } catch (e) {}
    var st = wrap.querySelector(".ask-ai-status"); if (st) st.textContent = "請手動複製下方文字";
  }
  document.querySelectorAll(".ask-ai[data-prompt]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var p = PROMPTS[btn.getAttribute("data-prompt")];
      if (!p) return;
      var text = p + TAIL;
      try {
        navigator.clipboard.writeText(text).then(function () {
          flash(btn, "已複製，貼到你的 AI 就能問");
        }, function () { fallback(btn, text); });
      } catch (e) { fallback(btn, text); }
    });
  });
})();
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
