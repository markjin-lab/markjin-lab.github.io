# 产业链接段与“产业与经济数据”小节：写作说明 / Writing notes for industry links and the “Industry and economic data” section

依据：路线图 v1.12 第 15.2 节（docs/roadmap.md）。本说明只讲写法和模板用法；规则以路线图为准，二者不一致时照路线图。

## 中文

### 写法
- 只写作用在哪一端（需求端、成本端或利润端），不写会怎样变。
- 来源没有测量的联系，用自然的话写成句子的一部分，标明是推断（模板见下文 `inference`），不用固定括注。
- 不评论宏观走势，不预测涨跌。
- 说不出作用在哪一端的条目（“无”档），不写产业链接段，不硬套；也不向读者说明“这一条不写产业链接段”。
- 说不出对应整体经济哪一块，或没有对照数据时，写到产业这一层为止，不写整体经济的判断。
- 每条判断都要有证据链接：产业链接段正文里的量要标出处；对照序列要标它在原始发布机构处的出处。
- 产业数据条目（“产业与经济数据”小节）同时满足以下条件才写，缺一条就整个小节缺席，不复述旧数：
  1. 是路线图第 15.3 节的产业序列；
  2. 过去 48 小时内有新发布；
  3. 原件已存档进 raw/；
  4. 已批准公开，且已通过公开门禁。其余机构的数只作线索，不进公开稿。
- 2026-10-22 的例外：当天的产业内容只写产业链接段，不写任何数值，不用“产业与经济数据”小节；也不写 BEA 的数值，不放 BEA 的链接。
- 分段（下一期读数的区间）的限制：
  1. 只在第六节“产业分段分支”的前提满足后、且该序列可作观测变量时才写；写了就全部登记。
  2. 日度现货价格序列的条目始终只写事实与计算值，不写分段。
  模板里没有写分段的位置；需要写分段时另行处理，不能塞进数据条目。
- 第七节写作纪律照旧：正文不出现内部分类标签和内部用语，术语给白话解释（标明“本站补充的通用解释”）；美国数据写明“美国”，不拿美国数推断中国；只有作者确认是宽口径的数据，才写明它不专指本条所说的环节（模板见下文 `broad`）。

### 模板用法
产业链接段放在条目的“为什么重要”之后：

```
{{< industry-link item="2" industry="semiconductors" side="demand" inference="这些订单是否转化为实际出货" >}}来源里的哪个量对应这个产业的哪项需求、成本或利润 [2]。{{< /industry-link >}}
```

- `item`：所在条目的编号，只用作段落锚点 `industry-link-<编号>`，不显示。
- `industry`：`energy`、`semiconductors`、`ai`、`manufacturing`（试点四个产业）；`side`：`demand`、`cost`、`profit`。
- `inference`：可选；只填来源没有测量、有待判断的那个联系，不带句末标点，如“这些订单是否转化为实际出货”。渲染成“来源没有测量这些订单是否转化为实际出货；这一联系是推断。”
- `economy`、`series`、`publisher`、`frequency`、`series_cite`：可选，五项同给，缺一项构建失败；只给 `economy` 不给对照序列也构建失败。没有对照序列时全部省略，段落写到产业这一层为止。
  - `economy`：`investment`、`consumption`、`prices`、`credit`、`housing`、`external`、`fiscal`、`employment`；
  - `series`、`publisher`、`frequency`：对照序列名、原始发布机构、频率（`daily`、`weekly`、`monthly`、`quarterly`、`annual`）；
  - `series_cite`：该序列在原始发布机构处的出处编号（一个正整数），本页须有对应的引用定义。
  - 渲染成“放到整体经济中看，这与<…>有关。可对照的公开数据是<序列名>（<发布机构>，<频率>）[<出处>]。”
- `broad`：可选，只能写 `broad="true"`，且须给对照序列；作者确认该序列是宽口径时才写，渲染时附“这个指标覆盖范围较广，不专指本条所说的环节。”不是宽口径就省略。

“产业与经济数据”小节只在满足上述条件、有可写的数据时用，里面只能放数据条目：

```
{{< industry-data >}}
{{< industry-datum series="美国……" publisher="原始发布机构" frequency="monthly" period="……" value="……" released="YYYY-MM-DD" cite="4" >}}
{{< /industry-data >}}
```

- 数据条目只渲染发布值，以及可选的计算值（`calc`、`calc_value`、`formula` 三项同给）；没有正文，也没有写走势或分段的位置。
- `value`、`calc_value` 是数字，千分位须规范（如 `1,234.5`；`1,2`、`1,,2` 构建失败）；`released` 须是真实存在的日期。
- `formula` 只能含数字、运算符、括号、等号、约等号和百分号；四舍五入的结果用“≈”，不写成“=”，如 `(102.3/101.1-1)×100%≈1.2%`。
- `broad`：可选，只能写 `broad="true"`；作者确认是宽口径时才写，渲染时附“这个指标覆盖范围较广，不专指某个产业环节。”
- 小节标题取 i18n，中文为“产业与经济数据”，英文为“Industry and economic data”。不用这些模板的页面上不出现这个小节。

### 出处编号
- 正文和对照序列的出处编号 `[n]` 按本页的引用定义“`[n]: 地址`”渲染成链接，写法与现有出处链接一致。
- 只处理正文文字里独立的 `[n]`：代码（`<code>`、`<pre>`）里、HTML 标签属性里、紧跟字母或数字的方括号原样保留。
- 引用定义只认代码围栏以外的；地址只接受 `http://` 或 `https://` 开头，其余（如 `javascript:`、相对地址）构建失败。
- 参数不合规时构建失败（`tests/test_industry_section.py` 列出了各种情形）。

## English

### How to write
- Say only which side the item acts on (demand, cost or profit); do not say how it will change.
- When the source did not measure a connection, say so in plain words as part of a sentence and mark it as an inference (see `inference` below); do not use a fixed bracketed note.
- No commentary on macroeconomic trends and no predictions of rises or falls.
- If no side can be named for an item, write no industry link; do not force one, and do not tell readers that the item has no industry link.
- If no part of the wider economy can be named, or there is no comparison data, stop at the industry level and make no economy-wide statement.
- Every statement needs an evidence link: cite the quantity in the industry link text, and cite the comparison series at its original publisher.
- Write data entries (the “Industry and economic data” section) only when all of the following hold; if any one fails, leave the whole section out and do not repeat old figures:
  1. the series is one of the industry series in section 15.3 of the roadmap;
  2. it had a new release within the past 48 hours;
  3. the original release has been archived in raw/;
  4. the figure is approved for publication and has cleared the public gate. Figures from any other agency are leads only and never appear in a published piece.
- Exception for 2026-10-22: that day's industry content is industry links only, with no figures at all and no “Industry and economic data” section; write no BEA values and include no BEA links.
- Limits on segments (ranges for the next reading):
  1. Write segments only after the prerequisites of the “industry segment branch” in section 6 are met and the series can serve as an observed variable; when segments are written, register all of them.
  2. Entries for daily spot price series always give only facts and computed values, never segments.
  The templates have no slot for segments; do not put them in data entries.
- Existing writing rules still apply: no internal labels or internal terms in the text, and plain-language explanations for technical terms (marked as the site's general explanation); label US data as US and do not infer China from US figures; say that a series is not specific to the activity in the item only when the author has confirmed it is a broad series (see `broad` below).

### Template usage
Place the industry link after the item's “Why it matters” paragraph:

```
{{< industry-link item="2" industry="semiconductors" side="demand" inference="these orders turn into actual shipments" >}}Which quantity in the source maps to which item of this industry [2].{{< /industry-link >}}
```

- `item` is the item number, used only for the paragraph anchor `industry-link-<number>`; it is not shown.
- `industry`: `energy`, `semiconductors`, `ai` or `manufacturing` (the four pilot industries); `side`: `demand`, `cost` or `profit`.
- `inference` is optional. Give only the connection still to be judged, with no closing punctuation, e.g. “these orders turn into actual shipments”. It renders as “The source did not measure whether these orders turn into actual shipments; this connection is an inference.”
- `economy`, `series`, `publisher`, `frequency` and `series_cite` are optional but go together; a missing one fails the build, and `economy` without a comparison series also fails the build. Without a comparison series, leave them all out and the paragraph stops at the industry level. `series_cite` is a single source number for the series at its original publisher and needs a reference definition on the page. The sentence renders as “In the wider economy, this relates to <…>. One public measure for comparison is <series> (<publisher>, <frequency>) [<source>].”
- `broad` is optional, accepts only `broad="true"` and needs a comparison series. Use it only when the author has confirmed the series is broad; it adds “This measure covers a broad range of activity, rather than the specific activity in this story.”

Use the “Industry and economic data” section only when the conditions above are met and there is data to report, and put only data entries in it (`industry-data` containing `industry-datum`, as in the Chinese notes). Data entries render the released value and, optionally, a computed value with its formula; they have no free-text body and no slot for trends or segments. `value` and `calc_value` must be numbers with valid thousands separators; `released` must be a real date; a rounded result in `formula` uses “≈”, not “=”. `broad="true"` on a data entry, used only when confirmed, adds “This measure covers a broad range of activity, rather than any one part of an industry.”

Source numbers `[n]` are linked only in body text, using reference definitions outside code fences; brackets in code, in HTML attributes or right after a letter or digit are left alone, and only `http://` or `https://` addresses are accepted. Invalid parameters fail the build.
