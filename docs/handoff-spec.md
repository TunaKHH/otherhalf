# Handoff Spec：「他們講一半，你別只聽一半」

> 依據：線上版本 `1794994307-f99b` 的 `css/site.css`、`js/site.js`、`index.html`、`articles/*.html`。
> 純靜態網站，沒有後端、沒有框架，HTML 由 `build.py` 產生。
> 資料截至 2026-11-18。

---

## 1. 概覽

一個議題中心頁加上 9 篇文章。每篇從一句政治人物常說的話出發，把「沒說的另一半」補回來，每段都附出處。

讀者的使用情境：
- 主要從 IG 限時動態、LINE 點連結進來，**以手機為主**。
- 讀者可能原本就相信標題那句話，所以版面刻意安靜、不用政黨色，避免一進來就覺得被說教。

設計原則（寫在 CSS 開頭）：
- 冷灰紙面、深墨藍、單一藍色強調。
- 大號襯線標題是唯一的視覺張力，其餘元素保持安靜。
- **三黨同一樣式，不用政黨色。** 這是編輯中立性的要求，不是美術偏好，請勿為了「好區分」加上藍綠白色。

---

## 2. 版面

| 項目 | 規格 | 原因 |
|---|---|---|
| 內容容器 `.shell` | `max-width: 1040px`，左右 `padding-inline: 20px`，置中 | 寬螢幕上行長不要過長 |
| 內文行長 | `.intro`、`.close ol/p` 限 `62ch`；`.hero .after` 限 `60ch`；`.tldr` 限 `760px` | 中文閱讀舒適行長 |
| 欄格 | CSS Grid，2 欄（`.qpair` `.split` `.quotes` `.sides`）或 3 欄（`.parties` `.summary` `.defs-grid`），一律寫成 `minmax(0, 1fr)` | `minmax(0,…)` 防止長網址撐破欄位 |
| 章節分隔 | `.chapter`：上框線 `3px solid var(--ink)`，上下 padding 64px | 用粗線取代卡片陰影，保持報紙感 |

### 頁面結構（文章頁）

```
nav.backnav        ← 所有議題（連回 ../index.html#card-<檔名>）
main
  header.hero      marker（出處＋看出處↓）→ h1 → .verdict → ol.tldr（第 1 項 .key）→ .after
  section.chapter  #facts / #bill / #reasons / #why …（依文章不同）
  section.chapter  #said「誰這樣說過」
section.close      深色帶：問題 h2 + ol 兩題 + 說明
section.sources    出處 ol（每頁重新編號 1..n，id="sN"）
footer.foot        整理方式、整理者、資料日期
dialog.gloss       名詞說明彈窗（國台辦 / 陸委會）
```

---

## 3. Design Tokens

目前只有**顏色與字型**是 token，間距與圓角仍是寫死的數值（見第 9 節建議）。

### 顏色

| Token | 淺色 | 深色 | 用途 |
|---|---|---|---|
| `--ground` | `#eef1f4` | `#12181e` | 頁面底色、`.said-q` 引言底 |
| `--surface` | `#ffffff` | `#1a2229` | 卡片底色 |
| `--ink` | `#15202b` | `#e8edf1` | 主要文字、章節粗線 |
| `--muted` | `#4a5866` | `#a3b0bc` | 次要文字、標籤 |
| `--line` | `#c9d1d9` | `#2c3742` | 邊框、分隔線 |
| `--accent` | `#1f4e79` | `#8fb8d6` | 連結、強調、`.verdict`、按鈕 |
| `--ok` | `#2f6b4f` | `#8cc5a6` | 「已複製」成功狀態 |
| `--band` | `#15202b` | `#0b1015` | 深色帶（`.close`、`.callout`、`.quote`） |
| `--band-ink` | `#eef1f4` | `#e8edf1` | 深色帶上的文字 |
| `--band-muted` | `#a9b6c2` | `#93a1ae` | 深色帶上的次要文字 |
| `--band-accent` | `#8fb8d6` | `#8fb8d6` | 深色帶上的強調 |

深色模式的啟用條件：
- 跟隨 `prefers-color-scheme: dark`。
- 也可以用 `:root[data-theme="dark|light"]` 強制指定。目前頁面上**沒有切換按鈕**。

### 字型

| Token | 字體堆疊 | 用途 |
|---|---|---|
| `--display` | `"Noto Serif TC", "Songti TC", serif` | h1、h2、`.verdict`、`.big`、引言 |
| `--body` | `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif` | 內文 |

注意：目前**沒有載入 webfont**，完全依賴系統字型。Android 若沒有 Noto Serif TC，標題會退回預設襯線字。

### 字級

| 元素 | 大小 | 字重 / 行高 |
|---|---|---|
| body | `17px` | 400 / 1.8 |
| `.hero h1` | `clamp(2.6rem, 8.5vw, 5.4rem)` | 900 / 1.22 |
| `.chapter h2` | `clamp(1.9rem, 5vw, 2.8rem)` | 900 / 1.3 |
| `.close h2` | `clamp(2.2rem, 7vw, 4rem)` | 900 / 1.25 |
| `.verdict` | `clamp(1.5rem, 4.5vw, 2.2rem)` | 900，顏色 `--accent` |
| `.hub-card h2` | `clamp(1.4rem, 4vw, 1.9rem)` | 900 / 1.35 |
| `.tldr li.key .tldr-head` | `clamp(1.25rem, 3.6vw, 1.55rem)` | 900 / 1.45 |
| `.marker` | `.85rem`，`letter-spacing .2em`（hero 內改為 `.04em`） | 500 |
| 標籤（`.tag` `.faq-tag` `.split b`） | `.78–.85rem`，`letter-spacing .08–.15em` | 700 |
| 出處上標 `sup a` | `.7em` | — |

### 圓角與間距（目前寫死的數值）

| 數值 | 出現位置 |
|---|---|
| 圓角 `14px` | 大部分卡片（`.q` `.panel` `.faq-item` `.hub-card` `.callout` `.quote`） |
| 圓角 `12px` | `.tldr li` |
| 圓角 `10px` | `.sides > div`、`.said-q`、fallback textarea |
| 圓角 `999px` | 膠囊：`.topnav a`、`.pill`、`.faq-tag`、`.ask-ai` |
| 卡片內距 | `26px 28px`，次要卡片用 `22px 24px` |
| 格線間距 | `12 / 14 / 16px` |
| 區塊間距 | 章節內 `gap: 28px`；章節上下 `64px`（手機 `48px`） |

---

## 4. 元件

| 元件 | Class | 變體 | 說明 |
|---|---|---|---|
| 議題卡 | `a.hub-card` | 預設；`.planned`（虛線框、透明底、不可點） | 標題以「開頭時，額外顯示 `.half`「沒說的另一半是？」。`id="card-<檔名>"` 供返回時定位 |
| 章節標記 | `.marker` | hero 內可換行，並帶「看出處 ↓」連結 | `::before` 是 36×4px 的 accent 色條 |
| 結論 | `.verdict` | — | 每篇一句，放在 h1 下方 |
| 重點清單 | `ol.tldr` | 第 1 項加 `.key`（加粗框、淡藍底、襯線大字） | 每項是「錨點標題 ↓ ＋ 一句話＋出處」 |
| 正反卡 | `.qpair > .q` | — | `b` 為小標，內含 `ul.ev` 證據清單 |
| 誰這樣說過 | `article.faq-item.said` | `.faq-tag` 寫政黨名（同色，不用政黨色） | `.who`、`blockquote.said-q`、`.split`（有根據 / 沒提到）、`.analogy`（後來的補充） |
| 深色提示框 | `p.callout` | — | 一段讓讀者自己想的問題 |
| 複製提示詞 | `button.ask-ai[data-prompt]` | `.on-dark`（深色帶上使用）；`.done`（成功） | 外層 `.ask-ai-wrap`，含 `.ask-ai-status`（`aria-live`） |
| 名詞彈窗 | `button.term[data-term]` → `dialog.gloss` | `tao`（國台辦，五星旗）、`mac`（陸委會，中華民國國旗） | 點虛線底線的名詞開啟 |
| 極端對照表 | `table.ends` | — | 外層 `.table-wrap` 可水平捲動 |
| 文章互連卡 | 文章內的 `a.hub-card` | — | 與首頁卡同樣式 |
| 結尾帶 | `section.close` | — | 深色、全寬 |

---

## 5. 狀態與互動

| 元素 | 狀態 | 行為 |
|---|---|---|
| 連結（全部） | focus-visible | `outline: 2px solid var(--accent)`，offset 3px |
| `.hub-card` | hover | 邊框變 `--accent` |
| `.hub-card` | `:target`（從文章返回） | accent 邊框，加 3px 22% 透明度光暈 |
| `.topnav a` | hover | 邊框與文字變 `--accent` |
| `.tldr-head` | 預設 / hover | 結尾自動加「 ↓」；hover 變 accent 色。點擊捲到對應章節 |
| `.term` | 預設 / hover | 點狀底線（2px，offset 4px）；hover 文字變 accent。在深色 `.quote` 內改用 `--band-accent` |
| `.ask-ai` | hover | 底色混入 10% accent |
| `.ask-ai` | 成功 | 加 `.done`（綠色），按鈕文字暫時換掉；`.ask-ai-status` 顯示「提示詞已複製」。**2.4 秒**後還原 |
| `.ask-ai` | 剪貼簿失敗 | 在按鈕下方插入唯讀 `textarea.ask-ai-fallback` 並全選，附提示文字，讓使用者手動複製 |
| `dialog.gloss` | 開啟 | 優先用 `showModal()`；不支援時改加 `open` 屬性 |
| `dialog.gloss` | 關閉 | 三種方式：× 按鈕、點背景、Esc。關閉後焦點回到觸發的名詞按鈕 |
| `sources li` | `:target` | 點上標跳過去時，整行加淡藍底 |

### 換頁捲動（`js/site.js` 最後一段）

- 進入新頁：一律捲到最上方。
- 例外 1：網址帶 `#hash` 時不捲，讓瀏覽器定位到錨點。
- 例外 2：用上一頁/下一頁回來時不捲，保留瀏覽器原本的位置。
- 「← 所有議題」連到 `index.html#card-<檔名>`，回首頁時會停在剛才讀的那張卡，並觸發 `:target` 光暈。

---

## 6. 響應式

| 斷點 | 變化 |
|---|---|
| > 760px | 預設：2 欄 / 3 欄格線；出處清單分 2 欄 |
| ≤ 760px | 所有多欄格線（`.qpair` `.stat-grid` `.parties` `.summary` `.split` `.quotes` `.sides` `.defs-grid`）改為單欄<br>出處改 1 欄<br>`.hero` 上下 padding 改 48/44px，`.chapter` 改 48px<br>`.layer` 的編號縮小、膠囊靠左 |

- 字級全部用 `clamp()` 隨視窗縮放，沒有另外設斷點。
- `.topnav` 在窄螢幕可水平捲動，捲軸隱藏。

**為什麼只有一個斷點**：讀者主要用手機，內容是線性閱讀，平板直接沿用桌面的 2 欄就足夠。

---

## 7. 動態

| 元素 | 觸發 | 動畫 | 時長 | Easing |
|---|---|---|---|---|
| `.hero > *` | 頁面載入 | `rise`：`translateY(10px)`、`opacity .55` 變成原位、`1` | 700ms，第 2–4 個子元素依序延遲 80 / 160 / 240ms | `cubic-bezier(.2,.7,.2,1)` |
| 錨點捲動 | 點 `.tldr-head`、上標 | `scroll-behavior: smooth`；`scroll-margin-top: 72px` 避開頂部 | 瀏覽器預設 | — |

- 兩者都只在 `prefers-reduced-motion: no-preference` 時啟用。
- 起始 `opacity` 是 `.55` 不是 `0`：動畫沒跑完或被中斷時，內容仍然看得到。

---

## 8. 邊界情況

| 情況 | 現況 |
|---|---|
| 長網址（出處） | `overflow-wrap: anywhere`，不會撐破版面 |
| 長標題 | `text-wrap: balance` 讓各行長度平均；目前沒有截斷，**也不應截斷**（標題就是原話） |
| 出處很多 | 每頁重新編號；`break-inside: avoid` 避免一條出處被拆成兩欄 |
| 寬表格 | `.table-wrap` 讓表格在容器內水平捲動 |
| 未完成的議題 | `.hub-card.planned`：虛線框、不是連結 |
| 剪貼簿 API 不可用（非 HTTPS、IG/LINE 內建瀏覽器） | 改用 textarea，讓使用者手動複製 |
| `<dialog>` 不支援 | 改用 `open` 屬性，並自行處理 Esc |
| 無 JS | 文章與出處都能正常閱讀；名詞彈窗和複製按鈕失效 |
| 載入、錯誤、空狀態 | 純靜態頁，沒有這三種狀態 |
| 慢速連線 | 沒有圖片也沒有 webfont，只有一支 CSS 和一支 JS |

---

## 9. 無障礙

- **焦點順序**：backnav → hero 的「看出處」→ tldr 各項 → 內文連結、名詞按鈕、上標 → 複製按鈕 → 出處 → footer。順序和 DOM 一致，沒有使用 `tabindex`。
- **彈窗**：`<dialog>` 加 `showModal()` 會自動鎖住焦點；關閉後焦點回到觸發的按鈕。關閉按鈕 44×44px。
- **複製狀態**：`.ask-ai-status` 是 `aria-live`，螢幕閱讀器會念出「提示詞已複製」。
- **語意標記**：
  - 每個 `section` 都有 `aria-labelledby` 指向自己的 h2。
  - 引言用 `blockquote`。
  - 名詞是 `button`，不是 `span`。
- **對比**（約略值）：
  - `--muted` 對 `--ground` 約 6.3:1。
  - `--band-muted` 對 `--band` 約 8:1。
  - 兩者都超過 AA 標準。

---

## 10. 已知問題與建議（依重要程度）

| # | 問題 | 重要程度 | 建議 |
|---|---|---|---|
| 1 | 出處上標 `sup a` 只有 `.7em`，手機上點擊區大約 10px，很難點中 | 8/10 | 用 padding 把點擊區撐到至少 24×24px，視覺大小不變 |
| 2 | `.topnav a` 高度約 33px，低於 44px 的觸控建議 | 6/10 | 上下 padding 改成 10px，或加上 `min-height: 44px` |
| 3 | 間距、圓角沒有 token，同類數值有 10、12、14、16 四種 | 5/10 | 收斂成 `--radius-sm/md/lg`、`--space-1..6`，之後改版才不會越改越亂 |
| 4 | 沒有載入 webfont，Android 標題字型不一致 | 5/10 | 只載入 Noto Serif TC 900 的子集，或接受系統字型的差異 |
| 5 | 有 `data-theme`，但沒有切換按鈕 | 3/10 | 不需要就刪掉 `data-theme` 相關的規則，減少維護負擔 |
| 6 | 「修正版新增」等區塊是逐次追加的，CSS 規則散落各處 | 3/10 | 依元件重新排序；目前不影響功能 |
