# 他們講一半，你別只聽一半

台灣兩岸與政黨議題的平衡資訊網站。

每篇文章的做法：
- 從一句政治人物真的說過的話出發。
- 把那句話「沒說的另一半」補回來。
- 每段附出處。
- 不替讀者下政黨結論。

目標：讓更多人有平衡的資訊來源。主要讀者從 IG 限時動態、LINE 點進來，以手機閱讀為主。

## 與使用者溝通

- 一律用**繁體中文**回答。
- 回覆開頭加上「尊敬的勇者大人」。
- 「文件」指 `.md` 檔。
- 用審視的眼光看使用者的需求。發現潛在問題就指出來，並給出他思考框架之外的建議，標上重要程度（1–10 分）。問題不明顯就不用說。

## 專案結構

```
build.py              唯一的產生器。所有內容、CSS、JS 都在這裡改
src/legacy-index.html 舊版單頁網站。build.py 從這裡擷取部分區塊（CSS、對話框、議題區塊、出處）
site/                 產出結果，可直接部署。不要手動修改，下次 build 會被覆蓋
  index.html          議題中心
  css/site.css
  js/site.js
  articles/*.html     9 篇文章
validate.py           檢查標籤是否成對、頁內錨點是否存在
docs/handoff-spec.md  設計規格：token、元件、狀態、響應式、無障礙
```

## 工作流程

1. 修改 `build.py`。
2. 執行 `uv run --no-project --python 3.12 build.py`。
3. 執行 `uv run --no-project --python 3.12 validate.py`，必須全部 OK。
4. 用瀏覽器開 `site/index.html` 檢查，手機寬度（約 390px）也要看。
5. commit，訊息寫清楚改了什麼、為什麼改（git log 同時是公開的修正紀錄）。
6. 需要上線時，依「部署」一節部署。

`build.py` 需要 Python 3.12 以上（f-string 裡用到反斜線）。macOS 內建的 `python3` 是 3.9，直接跑會出現 SyntaxError，所以一律透過 `uv` 執行。

**CSS 要寫在 `build.py` 裡的 `css` 字串**。直接改 `site/css/site.css` 會在下次 build 時被覆蓋。JS 的修改同理：寫成 `build.py` 裡的 `js.replace(...)`。

## build.py 重點

| 名稱 | 作用 |
|---|---|
| `sources` dict | 全站出處，key 是全域編號。目前用到 **107**，新出處從 108 開始（85 已停用）。每頁輸出時會自動重新編號成 1..n |
| `page(fname, title, desc, body, depth)` | 輸出一頁，負責重新編號出處，加上返回連結 `../index.html#card-<檔名>`、footer、名詞彈窗、script |
| `hero(marker, h1, verdict, tldr, after)` | 文章開頭。`tldr` 是 `(錨點, 標題, 內文)` 的清單，第一項自動加 `.key` 強調 |
| `close(h2, [問題1, 問題2], key)` | 結尾的深色帶。`key=None` 表示不放複製按鈕 |
| `btn(key, dark=False)` | 「複製提示詞，問你自己的 AI」按鈕，`key` 對應 `site.js` 裡的 `PROMPTS` |
| `cards` list | 首頁卡片的順序與文字。標題以「開頭時，卡片會自動顯示「沒說的另一半是？」 |
| `planned` list | 整理中的議題（虛線卡） |

內文中引用出處的寫法：`<sup><a href="#s105">105</a></sup>`，寫全域編號，`page()` 會換成該頁的編號。

## 新增一篇文章的步驟

1. 找一句**真的有人說過**的話當標題，並查證出處。如果不是逐字原話，要在 marker 和誰這樣說過裡標「報導轉述」。
2. 在 `build.py` 末尾新增 `# --- Article N`：
   - 用 `sources.update({...})` 加入新出處。
   - 依序寫 `hero(...)`、各個 section、`#said`「誰這樣說過」。
   - 最後呼叫 `page('articles/xxx.html', '「標題」沒說的另一半是？', 描述, ..., 1)`。
3. 在 `cards` 加首頁卡片。
4. 新增提示詞：
   - 在 `build.py` 裡加一行 `js=js.replace('    legislators: "','    newkey: "...",\n    legislators: "',1)`。
   - 提示詞最後要寫「請平衡呈現，不要替我下結論。」
5. 如果和既有文章相關，在那篇文章裡加 `a.hub-card` 互連卡。
6. 依照「工作流程」build、validate、目視檢查。

## 編輯原則（不可違反）

- **每個事實都要附出處**。來源沒寫的子句就刪掉，不要自己推論補上。
- **評論那句話，不評論說話的人**。
- 「誰這樣說過」要**藍綠對稱**。每位都有三欄：有根據的部分、這句話沒提到的、後來的補充（沒有就寫「目前沒有找到」）。
- **不用政黨色**。三黨同一樣式，這是中立性的要求。
- 不替讀者下政黨結論。結尾用問題收尾，例如「如果換成另一黨，你的答案會一樣嗎？」
- 結論寫在前面（`.verdict` 與 `tldr`），依據放在後面。
- 用語避免「像上課」：不要用「第一層、第二層」這類編號式說教。
- 政治事實會變動。寫之前先搜尋最新消息，頁面寫明資料日期。

## 目前文章與平衡狀態

| 檔案 | 標題 | 引言來自 |
|---|---|---|
| war | 嚇阻、和解，誰讓台灣更危險？ | 核心問題（非引言） |
| exchange | 「逢中必反、逢交流必擋」 | 國民黨聲明 |
| label | 「投藍白就是投共產黨！」 | 民進黨大罷免文宣 |
| anti-communism | 「假反共真戰爭」 | 朱立倫 |
| consensus | 「九二共識就是一國兩制」 | 鍾佳濱（民進黨） |
| budget | 「藍白拿預算當人質」 | 郭昱晴（民進黨，報導轉述） |
| legislators | 「明明抓到的共諜都是政府官員…」 | 牛煦庭（國民黨） |
| defense | 國防預算，到底在吵什麼？ | 議題（非引言） |
| infiltration | 防滲透，會不會管太多？ | 議題（非引言） |

引言類文章目前是藍 3 篇、綠 3 篇。新增文章時要維持平衡。

## 待辦（使用者尚未決定的建議）

- [x] **整理者署名**：已填「Tuna（Threads @tuna._run）」，連到 Threads 個人頁（2026-11-18）。
- [ ] 首頁加一段「為什麼最近一直在吵」：朝小野大的背景，讓整個網站有一條主線。
- [ ] budget：2025 年刪減 2075 億那段，補上藍白自己的說法（嚴格把關、還錢於民）。
- [ ] budget：標題「人質」是報導轉述，可以找有影片或逐字稿的原話替換。
- [x] war：冷戰美蘇案例已換成 1958 年八二三砲戰（出處 106、107，皆為國軍刊物，2026-11-18）。
- [ ] war：「推到極端」那段加上「整理者的分析」標示。
- [ ] exchange：可加副標「也就是常聽到的：民進黨都不交流」。exchange 的官方對話例子是藍 3 綠 1，需要補綠營的例子。
- [ ] 出處待確認：
  - war 引用的 Jervis 來源是 Defense Priorities，一個偏向克制路線的智庫，要註明立場或另找來源。
  - 1995/96 犯台時機的資料來自 2024 年美國報告，需要更新。
- [ ] 整理中的議題：「美國誰會理我們？」、「兩岸為什麼不能和平共處？」
- [ ] 找一位沒參與撰寫的人（或獨立的 subagent）再審一次平衡性與出處。
- [ ] UI（詳見 docs/handoff-spec.md 第 10 節）：
  - 出處上標點擊區太小（8/10）。
  - 頂部導覽按鈕高度不足 44px（6/10）。
  - 間距與圓角沒有 token 化（5/10）。
- [ ] IG 限時動態圖卡已經過時（還是舊主題「抗中保台只是口號」），需要依新網站重做。

## 部署

- 正式網址：**https://half-truth.pages.dev**（Cloudflare Pages 專案 `half-truth`，production branch `main`，2026-11-18 首次上線）。
- 部署指令（在專案根目錄執行，先 build、validate、commit）：

  ```
  pnpm dlx wrangler pages deploy site --project-name half-truth --branch main --commit-hash "$(git rev-parse HEAD)" --commit-message "$(git log -1 --format=%s)"
  ```

- 部署用 **wrangler**，這是使用者核准的例外：`cf` CLI 不支援舊版 Pages 部署（會回「Legacy Pages is not supported」），也沒有把登入權杖交給 wrangler 的方式。wrangler 有自己的 OAuth 登入（`pnpm dlx wrangler login`），已在這台電腦登入過。查詢帳號、專案等其他 Cloudflare 操作仍用 `cf`。
- 新建的 pages.dev 網域前幾分鐘可能回 522，等一下就正常。
- `.html` 網址會被 Pages 308 轉到無副檔名的網址（例如 `/articles/war`），站內連結照常可用。
- 舊版發布在 claude.ai artifact，Claude Code **無法更新那個連結**。IG 上已分享的舊連結需要另外處理。
