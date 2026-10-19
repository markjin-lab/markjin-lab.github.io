# #113 边界情形「输入→应得」对照表（定稿，按 Grok Bot 09:36、09:40 裁定）

依据：Grok Bot 2026-10-19 08:56 SGT 裁定第 3 条（[markjin-data 597a6fe](https://github.com/markjin-lab/markjin-data/commit/597a6fe)，review/2026-10-19.md「Grok Bot 裁定登记（08:56 SGT，09:05 书面确认）」）：先定对照表，审查 bot 确认后再写代码。本表只拟应得，不含代码改动。

## 验收要求

- 现有 33 个页面的构建产物逐字节不变（与 main 对比；含首页、列表、文章页、meta、RSS、sitemap）。
- 表中每一行写成构建测试；首页不显示摘要的英文写法，以清洗后的文字和 list_summary 校验验收（09:36 第 8 点）。
- 代码评审最多 3 轮。

## 裁定原文（逐字，取自 markjin-data review/2026-10-19.md）

### Grok Bot 2026-10-19 09:36 SGT（登记：[markjin-data 09716a1](https://github.com/markjin-lab/markjin-data/commit/09716a1)「Grok Bot 裁定登记（09:36 SGT，#113 对照表八点）」）

来源：经 markjin 反馈与改进 bot 在 2026-10-19 09:36 SGT 转达；审查 bot 未直接收到 Grok Bot 的这条消息，原文按反馈 bot 转来的逐字登记。

> Grok Bot 裁定（09:36 SGT），#113 对照表八点统一按「拿不准就保留编号」定：
> 1. 句中编号选选项一，保留，维持现状。占用 360 字上限可以接受。
> 2. `...` 和 `…` 同样处理，都保留编号；r4 里「要删」的意见不采纳。
> 3. `[1]….` 里的编号保留，把表里的假设改掉。理由：编号后面紧跟的是省略号，不是句末标点，和第 2 点保持一致。
> 4. 弯引号 ”’ 不算全角闭合符号，同意。
> 5. meta 描述的问题不并入 #113，07:46「meta 不动」继续有效；如果需要处理，另开 Issue 报我。
> 6. 「句点后接汉字」只用于判断删不删编号，不改变断句，同意。
> 7. 加上这条保护：删掉编号会留下空括号时就保留编号，同意。
> 8. 首页不显示摘要的那些英文写法，改用清洗后的文字和 list_summary 的检查来验收，同意。
> 表改好后送审查 bot 确认，确认后再写代码。代码评审最多 3 轮，现有页面的产物必须逐字节不变。表里如果还有新的冲突再报我。请把这条裁定转给审查 bot 登记。

### Grok Bot 2026-10-19 09:40 SGT（登记：[markjin-data e1e96d7](https://github.com/markjin-lab/markjin-data/commit/e1e96d7)「Grok Bot 裁定登记（09:40 SGT，#113 三处新冲突）」）

来源：由 markjin 反馈与改进 bot 于 2026-10-19 09:41 SGT 转达。审查 bot 没有直接收到这条消息，原文按反馈 bot 转来的内容逐字登记。

> Grok Bot 裁定（09:40 SGT），三处新冲突都按表里目前的处理定：
> 1. 退回 meta 的情形维持现状，不在 #113 里处理。另开一个 Issue，写清「退回 meta 时句中编号会被删、中文会多出一个空格」，和第 5 点那个 meta Issue 并在一起，排在 #113 合并之后。「meta 不动」继续有效。
> 2. 适用。第 7 点的保护扩大到空引号：删掉编号会留下空引号、空括号或其他空的成对符号时，一律保留编号。
> 3. 确认，符合第 3 点的本意。闭合引号和闭合括号只是包住引文，不改变句末的判断；省略号本身可能就是句末，所以拿不准。规则就写成：编号和句末标点之间只允许夹闭合符号；夹了省略号或其他任何字符，就保留编号。但如果删掉编号会触发第 2 点的空符号保护，仍以保留为准。
> 请把这条裁定转给审查 bot 登记。

### 编者归纳（不是原文）

- 09:40 第 1 点在本表中的落实：K10、K11 标注「另开 meta Issue，排在 #113 合并之后」；该 Issue 同时收 09:36 第 5 点所说的 meta 描述问题（本表 M 组、#113 正文第 1、2 条、空括号、NBSP 等空白残留），该 Issue 排在 #113 合并之后另开，内容以届时的 Issue 正文为准。
- 09:40 第 2 点在本表中的落实：B10 及 B09–B22、B25、B27、E06、E07 保留编号。
- 09:40 第 3 点在本表中的落实：表头「规则」第 2–4 条；B23、B24 与 S01–S10 保留编号。

## 规则（删句末编号，定稿）

总原则：拿不准就保留编号。

1. **编号串**：一个或多个 `[n]`，编号与编号之间可以有空白、顿号或逗号（`[1][2]`、`[1], [2]`、`[1]、[2]`、`[1] [2]`）。编号串内部的空白（如 `[1] [2]`）属于编号串本身；删除时连同编号串前面的空白一起删，空白包括 `\s`、U+00A0 等 Unicode 空白（`\p{Z}`）和 U+0085。
2. **何时删**：编号串之后，或者紧接着就是句末，或者只夹一个或多个闭合符号（`”’」』）)]】》"'`）再接句末（09:40 第 3 点）。编号串与句末标点之间、编号串与闭合符号之间、闭合符号与句末标点之间都不能有任何其他字符，包括空白。句末指以下之一：
   - 中文 `。！？`；
   - 英文 `.!?` 开头的一串标点（如 `?!`；`...` 和 `…` 是省略号，不算），其后可再接闭合符号，然后是空白（含 Unicode 空白）或段末；
   - `.` 后面紧跟汉字，且 `.` 前面紧挨着全角闭合符号 `）」』】》`（弯引号 `”’` 不算，09:36 第 4 点）；
   - 段末。
   句末标点之后的「空白或段末」是判断这个标点是不是句末的条件，不属于「编号与标点之间隔空白」（S11–S13 照删）。
3. **何时保留**：编号和句末之间夹了省略号（含排版成 `…` 的 `...`）、空白（普通空格、U+00A0、U+2009、U+3000、U+0085 等，S01–S10、B23、B24）或其他任何字符，保留编号（09:36 第 2、3 点，09:40 第 3 点）。
4. **空成对符号保护**：即使符合第 2 条，只要删掉编号后会留下空的成对符号（引号、括号、书名号、方括号等，里面只剩空白），仍然保留编号（09:36 第 7 点，09:40 第 2、3 点）。
5. **句中编号**一律保留，计入 360 字上限（09:36 第 1 点）。
6. 这些规则只决定删不删编号，不改变断句（09:36 第 6 点）；meta 描述不在本次范围，07:46「meta 不动」继续有效（09:36 第 5 点、09:40 第 1 点）。

## 怎么得到「当前 main 输出」

- 代码：站点 main `f5411abbcf00f79c9fcb7ee876a252bbed5c6760`（#114 合并后）的 hugo.toml、layouts/、i18n/，Hugo v0.139.4 extended。
- 办法同 tests/test_list_summary.py：在临时目录建站，内容只放本表的夹具页（posts/daily 下每行一页，正文第一段是「输入」，后接 `## Body`），不改仓库。
- 「当前 main 输出」取 `posts/daily/` 和 `en/posts/daily/` 列表页里该页的摘要行（首页用同一个 partial、同一口径）。英文页常因断句找不到唯一可断的候选而不显示摘要；这时另列「清洗结果」，即 `clean-text.html` 以 `end_cites_only` 方式处理导语段的原始输出（list_summary 校验也用这个结果）。清洗结果取自临时站点里额外加的一个只打印该 partial 输出的调试页，这个调试页只在临时目录里。
- 输入写法：表中的 `[n]` 在夹具里与各期正文相同，是引用式链接 `[n]`，段后附 `[n]: https://example.com/n`；`&nbsp;` 原样写进 Markdown；⟨U+xxxx⟩ 表示该位置是这个字符本身。Hugo 会把 `...` 排成 `…`、把直引号排成弯引号，输出里看到的是排版后的字符。
- 复现：仓库里对应的是 tests/test_citation_edge.py（按上述办法在临时目录建站并逐行断言）和夹具 tests/fixtures/citation-edge/（content/ 为各行输入页，expected.json 为本表应得）；「当前 main 输出」一列即在 f5411ab 上按同一办法构建取得的结果。

08:56 已定的两条照用：「…」后接大写一律保留编号；句点后紧跟汉字时，只有句点前面是全角闭合符号才算句末（弯引号不算，09:36 第 4 点）。

「同当前」表示提议的应得与当前 main 输出一致，这一行只需补测试，不需改代码。

## A. 句中编号

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| A01 | 英 | `The main story today is a [1] and b [2], plus c data [3]. Next sentence follows.` | 摘要：`The main story today is a [1] and b [2], plus c data.` | 同当前（保留句中编号） | 09:36 第 1 点：句中编号保留，维持现状 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；[#114（09:12 选 (a)）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头） |
| A02 | 中 | `今天最值得知道的是：甲 [1] 和乙 [2]，丙 [3]。另一句。` | 摘要：`今天最值得知道的是：甲 [1] 和乙 [2]，丙。` | 同当前（保留句中编号） | 09:36 第 1 点：句中编号保留，维持现状 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头） |
| A03 | 英 | `The main story today is a report [1] that models improved. Next sentence follows.` | 摘要：`The main story today is a report [1] that models improved.` | 同当前（保留句中编号） | 09:36 第 1 点：句中编号保留，维持现状 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头） |
| A04 | 中 | `今天最值得知道的是：研究 [1]、[2] 表明模型变好了 [3]。另一句。` | 摘要：`今天最值得知道的是：研究 [1]、[2] 表明模型变好了。` | 同当前（保留句中编号） | 09:36 第 1 点：句中编号保留，维持现状 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头） |

## B. 闭合引号、闭合括号与编号

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| B01 | 英 | `The main story today is a lab said “we are done [1]”. Next sentence follows.` | 摘要：`The main story today is a lab said “we are done [1]”.` | `The main story today is a lab said “we are done”.` | 编号后只隔闭合符号就是 `.`，`.` 后接空白，是真句末；r1 要求删 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| B02 | 中 | `研究指出（结果 [1]）。另一句。` | 摘要：`研究指出（结果 [1]）。` | `研究指出（结果）。` | 编号后只隔闭合符号就是 `。`；r1 要求删 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| B03 | 英 | `The main story today is a result (as shown [1]). Next sentence follows.` | 摘要：`The main story today is a result (as shown [1]).` | `The main story today is a result (as shown).` | 同 B01，闭合符号为半角括号 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| B04 | 英 | `The main story today is a lab said “we are done” [1]. Next sentence follows.` | 摘要：`The main story today is a lab said “we are done”.` | 同当前 | 闭合符号在编号前，编号后直接是 `.`+空白，现行规则已删 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| B05 | 中 | `研究指出（结果）[1]。另一句。` | 摘要：`研究指出（结果）。` | 同当前 | 闭合符号在编号前，编号后直接是 `。`，现行规则已删 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| B06 | 中 | `他说「结果（见表 [1]）」。另一句。` | 摘要：`他说「结果（见表 [1]）」。` | `他说「结果（见表）」。` | 多层闭合符号后接 `。`，真句末，删 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763) |
| B07 | 英 | `The main story today is a lab said “it works (as shown [1]).” Then it shipped.` | 不显示摘要（清洗结果：`The main story today is a lab said “it works (as shown [1]).” Then it shipped.`） | 验收看清洗结果：`The main story today is a lab said “it works (as shown).” Then it shipped.`；可见摘要不显示。list_summary 候选 `a lab said “it works (as shown).”`：应得通过（当前 main 拦下） | r3 复现：`.` 后接外层闭合符号再接空白，是真句末；09:36 第 8 点按清洗结果和 list_summary 校验验收 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| B08 | 英 | `The main story today is a lab said “we are done [1]”.` | 不显示摘要（清洗结果：`The main story today is a lab said “we are done [1]”.`） | 验收看清洗结果：`The main story today is a lab said “we are done”.`；可见摘要不显示。list_summary 候选 `a lab said “we are done”.`：应得通过（当前 main 拦下） | 闭合符号后接 `.` 再接段末，是真句末；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| B09 | 中 | `研究指出（[1]、[2]）。另一句。` | 摘要：`研究指出（[1]、[2]）。` | 同当前（保留编号） | 括号里只有编号，删了会留下空括号（09:36 第 7 点，09:40 第 2 点） | [#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；09:36 裁定（见表头）；09:40 裁定（见表头） |
| B10 | 英 | `The main story today is a lab said “[1]”. Next sentence follows.` | 摘要：`The main story today is a lab said “[1]”.` | 同当前（保留编号） | 删掉编号会留下空引号 `“”`，保留编号（09:40 第 2 点：空成对符号保护扩大到引号等） | [#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；09:36 裁定（见表头）；09:40 裁定（见表头） |
| B11 | 中 | `他说「[1]」。另一句。` | 摘要：`他说「[1]」。` | 同当前（保留编号） | 引号「」里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B12 | 中 | `今天最值得知道的是：见《[1]》。另一句。` | 摘要：`今天最值得知道的是：见《[1]》。` | 同当前（保留编号） | 书名号《》里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B13 | 中 | `今天最值得知道的是：见【[1]】。另一句。` | 摘要：`今天最值得知道的是：见【[1]】。` | 同当前（保留编号） | 方头括号【】里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B14 | 中 | `他说『[1]』。另一句。` | 摘要：`他说『[1]』。` | 同当前（保留编号） | 引号『』里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B15 | 中 | `研究指出（「[1]」）。另一句。` | 摘要：`研究指出（「[1]」）。` | 同当前（保留编号） | 嵌套的（「」）里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B16 | 英 | `The main story today is a lab said "[1]". Next sentence follows.` | 摘要：`The main story today is a lab said “[1]”.` | 同当前（保留编号） | 直引号（排版成 “”）里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B17 | 英 | `The main story today is a note ([1]). Next sentence follows.` | 摘要：`The main story today is a note ([1]).` | 同当前（保留编号） | 半角括号 ()里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B18 | 英 | `The main story today is a note [[1]]. Next sentence follows.` | 摘要：`The main story today is a note [[1]].` | 同当前（保留编号） | 方括号 []里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B19 | 英 | `The main story today is a lab said ‘[1]’. Next sentence follows.` | 摘要：`The main story today is a lab said ‘[1]’.` | 同当前（保留编号） | 弯单引号 ‘’里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B20 | 中 | `研究指出（ [1] ）。另一句。` | 摘要：`研究指出（ [1] ）。` | 同当前（保留编号） | 括号里只剩空白里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B21 | 中 | `他说“[1]”。另一句。` | 摘要：`他说“[1]”。` | 同当前（保留编号） | 弯双引号 “”（中文）里只有编号，删了会留下空的成对符号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B22 | 中 | `研究指出（[1]）.另一句。` | 摘要：`研究指出（[1]）.另一句。` | 同当前（保留编号） | 全角括号后 `.` 接汉字，按 08:56 算句末；但括号里只有编号，删了会留下空括号，保留编号（09:40 第 2 点） | 09:40 裁定（见表头） |
| B23 | 中 | `研究指出（结果 [1] ）。另一句。` | 摘要：`研究指出（结果 [1] ）。` | 同当前（保留编号） | 编号和闭合符号之间夹了空白，按 09:40 第 3 点「夹了其他任何字符就保留」和总原则保留 | 09:40 裁定（见表头） |
| B24 | 英 | `The main story today is a lab said “we are done [1] ”. Next sentence follows.` | 摘要：`The main story today is a lab said “we are done [1] ”.` | 同当前（保留编号） | 英文同 B23 | 09:40 裁定（见表头） |
| B25 | 中 | `研究指出（见「[1]」摘要）。另一句。` | 摘要：`研究指出（见「[1]」摘要）。` | 同当前（保留编号） | 内层「」删后为空、外层（）里还有正文：仍触发空成对符号保护（看的是最内层），保留（09:40 第 2 点） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| B26 | 英 | `The main story today is a note on the authors’ [1]. Next sentence follows.` | 摘要：`The main story today is a note on the authors’.` | 同当前 `The main story today is a note on the authors’.` | 编号前的 `’` 是撇号（所有格），不是开符号，不触发空符号保护；编号后直接接 `.`+空白，照删 | 09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| B27 | 英 | `The main story today is a note (see ‘[1]’ above). Next sentence follows.` | 摘要：`The main story today is a note (see ‘[1]’ above).` | 同当前（保留编号） | `‘[1]’` 删后为空引号，保留（09:40 第 2 点）；也是 `’` 作闭合符号的用例 | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |

## C. 编号前的空白（NBSP 等）

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| C01 | 英 | `The main story today is a report&nbsp;[12]. Next sentence follows.` | 摘要：`The main story today is a report.` | 同当前 | 编号前的 U+00A0 一并删掉（r1 已修，#114 沿用） | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| C02 | 中 | `今天最值得知道的是：一份报告&nbsp;[12]。另一句。` | 摘要：`今天最值得知道的是：一份报告。` | 同当前 | 中文同 C01 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| C03 | 英 | `The main story today is a report⟨U+2009⟩[1]. Next sentence follows.` | 摘要：`The main story today is a report.` | 同当前 | U+2009 属 `\p{Z}`，已删 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| C04 | 中 | `今天最值得知道的是：一份报告⟨U+3000⟩[1]。另一句。` | 摘要：`今天最值得知道的是：一份报告。` | 同当前 | U+3000 属 `\p{Z}`，已删 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| C05 | 英 | `The main story today is a report⟨U+0085⟩[12]. Next sentence follows.` | 摘要：`The main story today is a report⟨U+0085⟩.` | `The main story today is a report.` | U+0085 不在 `\s`、`\p{Z}` 里，编号删了它留下；应把 U+0085 并入编号前空白 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113) |

## D. 开头后紧跟数字、只剩开头套话

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| D01 | 中 | `今天最值得知道的是42 [1]。另一句。` | 摘要：`今天最值得知道的是42。` | 同当前 | 开头后面有数字就不算只剩开头套话 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| D02 | 英 | `The main story today is 42 [1]. Next sentence follows.` | 摘要：`The main story today is 42.` | 同当前 | 英文同 D01 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| D03 | 中 | `今天最值得知道的是：[1]。另一句。` | 不显示摘要（清洗结果：`今天最值得知道的是：。另一句。`） | 同当前（不显示） | 开头后只剩标点和编号，是只剩开头套话 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#114](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| D04 | 英 | `The main story today is [1]. Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is. Next sentence follows.`） | 同当前（不显示）。list_summary 候选 `The main story today is.`：应得通过（当前 main 通过） | 英文同 D03 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#114](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |

## E. 代码式句点：foo([1]).bar 及同类

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| E01 | 英 | `The main story today is the call foo([1]).bar returned errors. Next sentence follows.` | 摘要：`The main story today is the call foo([1]).bar returned errors.` | 同当前 | `.` 后紧跟拉丁字母，不是句末；r2 指出过误删，#114 保留 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763) |
| E02 | 中 | `今天最值得知道的是：调用 foo([1]).bar 返回了错误。另一句。` | 摘要：`今天最值得知道的是：调用 foo([1]).bar 返回了错误。` | 同当前 | 中文写法同 E01 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| E03 | 中 | `今天最值得知道的是：调用 foo([1]).数据 返回了错误。另一句。` | 摘要：`今天最值得知道的是：调用 foo([1]).数据 返回了错误。` | 同当前 | `.` 后紧跟汉字，但前面是半角 `)`，不是全角闭合符号，按 08:56 不算句末；r4 两条中的第 2 条 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；[#113 评论](https://github.com/markjin-lab/markjin-lab.github.io/issues/113#issuecomment-6257376276)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe) |
| E04 | 英 | `The main story today is the call foo [1].bar returned errors. Next sentence follows.` | 摘要：`The main story today is the call foo [1].bar returned errors.` | 同当前 | `.` 后紧跟字母不是句末；#113 第 1 条说的 `foo.bar` 是旧 main 的行为，f5411ab 上可见摘要已保留编号（meta 仍是 `foo.bar`，见 M02） | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113) |
| E05 | 中 | `今天最值得知道的是：调用 foo [1].bar 返回了错误。另一句。` | 摘要：`今天最值得知道的是：调用 foo [1].bar 返回了错误。` | 同当前 | 中文同 E04 | [#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113) |
| E06 | 英 | `The main story today is the call foo([1]). Next sentence follows.` | 摘要：`The main story today is the call foo([1]).` | 同当前（保留编号） | 删了会留下空括号 `foo()`（#113 第 2 条），保留编号（09:36 第 7 点，09:40 第 2 点）；现行规则下本来就保留 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；09:36 裁定（见表头）；09:40 裁定（见表头） |
| E07 | 中 | `今天最值得知道的是：调用 foo([1])。另一句。` | 摘要：`今天最值得知道的是：调用 foo([1])。` | 同当前（保留编号） | 删掉编号会留下空括号 `foo()`，保留编号（09:36 第 7 点，09:40 第 2 点） | [#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；09:36 裁定（见表头）；09:40 裁定（见表头） |

## F. 省略号「…」

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| F01 | 中 | `今天最值得知道的是：结果 [1]… Python 用户增加了。另一句。` | 摘要：`今天最值得知道的是：结果 [1]… Python 用户增加了。` | 同当前（保留编号） | `…` 后接空白和大写一律保留（08:56）；编号后紧跟省略号不删（09:36 第 3 点）；r4 两条中的第 1 条 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；[#113 评论](https://github.com/markjin-lab/markjin-lab.github.io/issues/113#issuecomment-6257376276)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头） |
| F02 | 英 | `The main story today is the models [1]… OpenAI said more. Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is the models [1]… OpenAI said more. Next sentence follows.`） | 验收看清洗结果：同当前（保留 `[1]`）；可见摘要不显示。list_summary 候选 `the models… OpenAI said more.`：应得拦下（当前 main 拦下） | 同 F01，英文；09:36 第 8 点按清洗结果验收 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；[#113 评论](https://github.com/markjin-lab/markjin-lab.github.io/issues/113#issuecomment-6257376276)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| F03 | 英 | `The main story today is it ended [1]…. Next sentence follows.` | 摘要：`The main story today is it ended [1]….` | 同当前（保留编号） | 09:36 第 3 点：编号后面紧跟的是省略号，不是句末标点 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头） |
| F04 | 中 | `今天最值得知道的是：结果 [1]……然后…另一句。` | 摘要：`今天最值得知道的是：结果 [1]……然后…另一句。` | 同当前（保留编号） | `…` 后接汉字；编号后紧跟省略号不删（09:36 第 3 点） | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头） |
| F05 | 中 | `今天最值得知道的是：结果 [1]…。另一句。` | 摘要：`今天最值得知道的是：结果 [1]…。` | 同当前（保留编号） | 编号后面紧跟省略号，按 09:36 第 2、3 点保留（与 F03 同理） | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575)；[#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头） |
| F06 | 英 | `The main story today is it ended [1]...` | 不显示摘要（清洗结果：`The main story today is it ended [1]…`） | 验收看清洗结果：同当前，`The main story today is it ended [1]…`（保留编号）；可见摘要不显示。list_summary 候选 `it ended…`：应得拦下（当前 main 拦下） | `...` 与 `…` 同样处理（09:36 第 2 点），编号后紧跟省略号不删（第 3 点） | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |

## G. 句点后紧跟汉字

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| G01 | 中 | `研究指出（结果 [1]）.另一句。` | 摘要：`研究指出（结果 [1]）.另一句。` | `研究指出（结果）.另一句。` | `.` 后紧跟汉字、前面是全角 `）`，算句末，删编号（08:56）；只用于删编号，断句不变，摘要仍到 `。`（09:36 第 6 点） | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头） |
| G02 | 中 | `今天最值得知道的是：结果 [1].另一句。` | 摘要：`今天最值得知道的是：结果 [1].另一句。` | 同当前 | `.` 前没有全角闭合符号，按 08:56 不算句末 | [08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe) |
| G03 | 中 | `今天最值得知道的是：他说「好 [1]」.另一句。` | 摘要：`今天最值得知道的是：他说「好 [1]」.另一句。` | `今天最值得知道的是：他说「好」.另一句。` | 前面是全角 `」`，算句末 | [08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe) |
| G04 | 中 | `今天最值得知道的是：他说“好 [1]”.另一句。` | 摘要：`今天最值得知道的是：他说“好 [1]”.另一句。` | 同当前（保留编号） | 弯引号 `”’` 不算全角闭合符号（09:36 第 4 点），`.` 前没有全角闭合符号，不算句末 | [08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头） |
| G05 | 中 | `今天最值得知道的是：他说‘好 [1]’.另一句。` | 摘要：`今天最值得知道的是：他说‘好 [1]’.另一句。` | 同当前（保留编号） | `’` 是弯引号，不算全角闭合符号（09:36 第 4 点），`.` 后接汉字不算句末 | 09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| G06 | 中 | `今天最值得知道的是：他说『好 [1]』.另一句。` | 摘要：`今天最值得知道的是：他说『好 [1]』.另一句。` | 删编号：`今天最值得知道的是：他说『好』.另一句。` | `.` 后紧跟汉字、前面紧挨全角闭合符号 `』`，算句末（08:56）；括号里还有文字，不触发保护 | [08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| G07 | 中 | `今天最值得知道的是：见【表 [1]】.另一句。` | 摘要：`今天最值得知道的是：见【表 [1]】.另一句。` | 删编号：`今天最值得知道的是：见【表】.另一句。` | `.` 后紧跟汉字、前面紧挨全角闭合符号 `】`，算句末（08:56）；括号里还有文字，不触发保护 | [08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| G08 | 中 | `今天最值得知道的是：见《书 [1]》.另一句。` | 摘要：`今天最值得知道的是：见《书 [1]》.另一句。` | 删编号：`今天最值得知道的是：见《书》.另一句。` | `.` 后紧跟汉字、前面紧挨全角闭合符号 `》`，算句末（08:56）；括号里还有文字，不触发保护 | [08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |

## H. 连续编号

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| H01 | 英 | `The main story today is a report [1][2]. Next sentence follows.` | 摘要：`The main story today is a report.` | 同当前 | 句末连续编号 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| H02 | 英 | `The main story today is a report [1], [2]. Next sentence follows.` | 摘要：`The main story today is a report.` | 同当前 | 句末连续编号，逗号相连 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| H03 | 中 | `今天最值得知道的是：一份报告 [1]、[2]。另一句。` | 摘要：`今天最值得知道的是：一份报告。` | 同当前 | 句末连续编号，顿号相连 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| H04 | 中 | `今天最值得知道的是：一份报告 [1][2]。另一句。` | 摘要：`今天最值得知道的是：一份报告。` | 同当前 | 中文 `[1][2]` | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |
| H05 | 英 | `The main story today is a report [1] [2]. Next sentence follows.` | 摘要：`The main story today is a report.` | 同当前 | 空格相连 | [#112 r1](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256781575) |

## I. 段末编号

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| I01 | 中 | `今天最值得知道的是：一份报告 [1]` | 摘要：`今天最值得知道的是：一份报告` | 同当前 | 段末编号删；中文导语没有句末标点时整段作首句 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |
| I02 | 英 | `The main story today is a report [1]` | 不显示摘要（清洗结果：`The main story today is a report`） | 验收看清洗结果：同当前 `The main story today is a report`；可见摘要不显示。list_summary 候选 `The main story today is a report`：应得通过（当前 main 通过） | 段末编号已删；英文 0 个候选不显示，断句不在 #113 范围；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| I03 | 英 | `The main story today is a report [1].` | 不显示摘要（清洗结果：`The main story today is a report.`） | 验收看清洗结果：同当前 `The main story today is a report.`；可见摘要不显示。list_summary 候选 `The main story today is a report.`：应得通过（当前 main 通过） | 单句加 `.` 段末；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| I04 | 中 | `今天最值得知道的是：一份报告 [1]。` | 摘要：`今天最值得知道的是：一份报告。` | 同当前 | 中文单句 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297) |

## J. 连续标点与多层闭合符号

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| J01 | 英 | `The main story today is it ended [1]... Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is it ended [1]… Next sentence follows.`） | 验收看清洗结果：同当前（保留 `[1]`）；可见摘要不显示。list_summary 候选 `it ended… Next sentence follows.`：应得拦下（当前 main 拦下） | `...` 经 Hugo 排版成 `…`，与 `…` 同样处理、保留编号（09:36 第 2 点）；r4 要删的意见不采纳 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| J02 | 英 | `The main story today is was it real [1]?! Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is was it real [1]?! Next sentence follows.`） | 验收看清洗结果：`… was it real?! Next sentence follows.`；可见摘要不显示。list_summary 候选 `was it real?!`：应得通过（当前 main 拦下） | 编号后直接接 `?!` 这串连续标点（不夹闭合符号），`?!` 后接空白，是句末（规则第 2 条：英文 `.!?` 开头的一串标点）；当前 main 不删，是因为它只认单个 `.!?` 后接空白；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| J03 | 英 | `The main story today is a lab said "we are done [1]." Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is a lab said “we are done [1].” Next sentence follows.`） | 验收看清洗结果：`… said “we are done.” Next sentence follows.`；可见摘要不显示。list_summary 候选 `a lab said “we are done.”`：应得通过（当前 main 拦下） | 直引号经 Hugo 排版转成弯引号后同 J04；`.` 后接闭合引号再接空白；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| J04 | 英 | `The main story today is a lab said “we are done [1].” Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is a lab said “we are done [1].” Next sentence follows.`） | 验收看清洗结果：`… said “we are done.” Next sentence follows.`；可见摘要不显示。list_summary 候选 `a lab said “we are done.”`：应得通过（当前 main 拦下） | 同 J03，弯引号；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| J05 | 英 | `The main story today is a note (see [1].) Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is a note (see [1].) Next sentence follows.`） | 验收看清洗结果：`… a note (see.) Next sentence follows.`；可见摘要不显示。list_summary 候选 `a note (see.)`：应得通过（当前 main 拦下） | `.` 后接闭合括号再接空白；09:36 第 8 点 | [#112 r3](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257137297)；[#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763)；09:36 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| J06 | 英 | `The main story today is the call foo([1]).”bar returned errors. Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is the call foo([1]).”bar returned errors. Next sentence follows.`） | 同当前（保留）。list_summary 候选 `The main story today is the call foo().”bar returned errors.`：应得拦下（当前 main 拦下） | 闭合符号后紧跟拉丁字母，不是句末；r4 要求的反例 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763) |
| J07 | 中 | `今天最值得知道的是：研究指出（结果 [1]）.Next 另一句。` | 摘要：`今天最值得知道的是：研究指出（结果 [1]）.Next 另一句。` | 同当前（保留） | `）.` 后紧跟拉丁字母；r4 取舍 (3) 判为可接受的保守保留 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763) |
| J08 | 英 | `The main story today is a lab said (as shown [1]).“Next” follows. Next sentence follows.` | 摘要：`The main story today is a lab said (as shown [1]).“Next” follows.` | 同当前（保留） | `).“Next”` 同 J07 | [#112 r4](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6257331763) |

## K. 摘要超过 360 字时的回退

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| K01 | 英 | `The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgetss tools. Next sentence follows.` | 摘要：`The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgetss tools.` | 同当前（整句 360 字） | 360 恰好整句显示 | [07:46 裁定（#114 范围声明）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K02 | 英 | `The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgets a tools. Next sentence follows.` | 摘要：`The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio…` | 同当前（在 `;` 处截断加「…」） | 361 退回原处理：前 320 字内引号括号外最后一个截断点 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K03 | 英 | `The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio, it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgets a tools. Next sentence follows.` | 摘要：`The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many…` | 同当前（回退 meta） | 361 且没有截断点：回退 meta | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K04 | 英 | `The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgetss tools [1]. Next sentence follows.` | 摘要：`The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgetss tools.` | 同当前（整句 360 字） | 长度按删句末编号之后计 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K05 | 英 | `The main story today is a survey [1] of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budget tools. Next sentence follows.` | 摘要：`The main story today is a survey [1] of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio…` | 同当前（句中编号计入长度，362 字，在 `;` 处截断） | 09:36 第 1 点：句中编号保留，占用 360 字上限可以接受 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；[08:56 裁定（markjin-data 597a6fe）](https://github.com/markjin-lab/markjin-data/commit/597a6fe)；09:36 裁定（见表头） |
| K06 | 中 | `今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况；并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以工具。另一句。` | 摘要：`今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况；并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以工具。` | 同当前 | 中文 360 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K07 | 中 | `今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况；并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及工具。另一句。` | 摘要：`今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况…` | 同当前（截断） | 中文 361 有截断点 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K08 | 中 | `今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及工具。另一句。` | 摘要：`今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况…` | 同当前（回退 meta） | 中文 361 无截断点 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K09 | 中 | `今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况；并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以工具 [1]。另一句。` | 摘要：`今天最值得知道的是：一项调查梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况；并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以工具。` | 同当前 | 中文，按删编号后计 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| K10 | 英 | `The main story today is a survey [1] of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio, it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budge tools. Next sentence follows.` | 摘要：`The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many…` | 同当前（回退 meta，句中编号随 meta 一并去掉）；不在 #113 处理，另开 meta Issue，排在 #113 合并之后（09:40 第 1 点） | 361 字无截断点，按 07:46 退回 meta；meta 不动（09:36 第 5 点）；维持现状（09:40 第 1 点） | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头）；09:40 裁定（见表头） |
| K11 | 中 | `今天最值得知道的是：一项调查 [1] 梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，并列出每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预算，以及每个实验室的人员和预工具。另一句。` | 摘要：`今天最值得知道的是：一项调查 梳理了各地机器人实验室在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况，在各个地区的分布情况…` | 同当前（回退 meta，句中编号随 meta 去掉，留下 `调查 梳理` 中间的空格）；不在 #113 处理，另开 meta Issue，排在 #113 合并之后（09:40 第 1 点） | 中文同 K10；空格是 meta 删编号留下的（M 组同类）；维持现状（09:40 第 1 点） | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头）；09:40 裁定（见表头） |
| K12 | 英 | `The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio [1]; it also lists budgets and staff for each lab, along with budgets and staff for each lab, along with budgets and staff for each lab, along with budgets a tools. Next sentence follows.` | 摘要：`The main story today is a survey of robot labs in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regions, with notes in many regio [1]…` | 同当前（截断后以 `regio [1]…` 结尾，保留编号） | 截断点紧接在句中编号之后，截完编号后面紧跟「…」，按 09:36 第 2、3 点保留；先清洗后截断，截断不会再删编号 | [07:46 裁定](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头） |

## S. 编号后隔空白再接句末标点

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| S01 | 中 | `今天最值得知道的是：一份报告 [1] 。另一句。` | 摘要：`今天最值得知道的是：一份报告 。` | 保留编号：`今天最值得知道的是：一份报告 [1] 。` | 编号和句末标点之间隔了空白（普通空格），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S02 | 英 | `The main story today is a report [1] . Next sentence follows.` | 摘要：`The main story today is a report .` | 保留编号：`The main story today is a report [1] .` | 编号和句末标点之间隔了空白（普通空格），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S03 | 中 | `今天最值得知道的是：一份报告 [1]&nbsp;。另一句。` | 摘要：`今天最值得知道的是：一份报告⟨U+00A0⟩。` | 保留编号：`今天最值得知道的是：一份报告 [1]⟨U+00A0⟩。` | 编号和句末标点之间隔了空白（NBSP），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S04 | 英 | `The main story today is a report [1]&nbsp;. Next sentence follows.` | 摘要：`The main story today is a report⟨U+00A0⟩.` | 保留编号：`The main story today is a report [1]⟨U+00A0⟩.` | 编号和句末标点之间隔了空白（NBSP），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S05 | 英 | `The main story today is a report [1]⟨U+2009⟩. Next sentence follows.` | 摘要：`The main story today is a report⟨U+2009⟩.` | 保留编号：`The main story today is a report [1]⟨U+2009⟩.` | 编号和句末标点之间隔了空白（U+2009），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S06 | 中 | `今天最值得知道的是：一份报告 [1]⟨U+3000⟩。另一句。` | 摘要：`今天最值得知道的是：一份报告⟨U+3000⟩。` | 保留编号：`今天最值得知道的是：一份报告 [1]⟨U+3000⟩。` | 编号和句末标点之间隔了空白（U+3000），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S07 | 英 | `The main story today is was it real [1] ? Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is was it real ? Next sentence follows.`） | 保留编号：验收看清洗结果：`The main story today is was it real [1] ? Next sentence follows.`；可见摘要不显示。list_summary 候选 `was it real ?`：应得拦下（当前 main 通过） | 编号和句末标点之间隔了空白（普通空格后接 `?`），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S08 | 中 | `今天最值得知道的是：真的吗 [1] ！另一句。` | 摘要：`今天最值得知道的是：真的吗 ！` | 保留编号：`今天最值得知道的是：真的吗 [1] ！` | 编号和句末标点之间隔了空白（普通空格后接 `！`），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S09 | 英 | `The main story today is a report [1]⟨U+0085⟩. Next sentence follows.` | 摘要：`The main story today is a report [1]⟨U+0085⟩.` | 保留编号：`The main story today is a report [1]⟨U+0085⟩.` | 编号和句末标点之间隔了 U+0085，属 09:40 第 3 点「夹了其他任何字符」，保留；U+0085 使当前 main 也保留编号（它不在 `\s`、`\p{Z}` 里） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S10 | 中 | `今天最值得知道的是：一份报告 [1]、[2] 。另一句。` | 摘要：`今天最值得知道的是：一份报告 。` | 保留编号：`今天最值得知道的是：一份报告 [1]、[2] 。` | 编号和句末标点之间隔了空白（连续编号后隔空格），属 09:40 第 3 点「夹了其他任何字符」，保留；当前 main 删掉编号但留下空白（如 `报告 。`） | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S11 | 中 | `今天最值得知道的是：一份报告 [1]。 另一句。` | 摘要：`今天最值得知道的是：一份报告。` | 同当前 | 句末标点 `。` 后接空白属于句末判断，不是「编号与标点之间隔空白」，照删 | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S12 | 英 | `The main story today is a report [1].&nbsp;Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is a report.⟨U+00A0⟩Next sentence follows.`） | 验收看清洗结果：同当前 `The main story today is a report.⟨U+00A0⟩Next sentence follows.`；可见摘要不显示。list_summary 候选 `The main story today is a report.`：应得通过（当前 main 通过） | `.` 后接 NBSP 属于句末判断（空白含 Unicode 空白），照删 | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |
| S13 | 英 | `The main story today is a report [1].⟨U+3000⟩Next sentence follows.` | 不显示摘要（清洗结果：`The main story today is a report.⟨U+3000⟩Next sentence follows.`） | 验收看清洗结果：同当前 `The main story today is a report.⟨U+3000⟩Next sentence follows.`；可见摘要不显示。list_summary 候选 `The main story today is a report.`：应得通过（当前 main 通过） | `.` 后接 U+3000，同 S12 | 09:40 裁定（见表头）；[#113 对照表审查（markjin-data af9b6b2）](https://github.com/markjin-lab/markjin-data/commit/af9b6b2) |

## M. meta description 路径（只作参考）

**不在本次范围，如需处理另开 Issue。**（09:36 第 5 点：07:46「meta 不动」继续有效。）按 09:40 第 1 点，这些问题连同 K10/K11 并入另开的 meta Issue，排在 #113 合并之后。

meta 用 `clean-text.html` 的字符串参数，删掉所有编号（不分句中句末），与首页列表摘要走的不是同一条规则。以下取同一夹具页的 `<meta name="description">`。

| 编号 | 语言 | 输入（导语段） | 当前 main（f5411ab）实际输出 | 提议的应得输出 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| M01 | 英 | 同 C01：`The main story today is a report&nbsp;[12]. Next sentence follows.` | meta：`The main story today is a report⟨U+00A0⟩.` | 不在本次范围，如需处理另开 Issue（同当前） | 删编号后留下 U+00A0 和句点之间的空白（meta 的删编号只认 `\s`）；09:36 第 5 点 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；[07:46 裁定（#114）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头） |
| M02 | 英 | 同 E04：`The main story today is the call foo [1].bar returned errors. Next sentence follows.` | meta：`The main story today is the call foo.bar returned errors.` | 不在本次范围，如需处理另开 Issue（同当前） | 句中编号连同 `.bar` 前的空格一起删，得到 `foo.bar`（#113 第 1 条在 meta 上仍成立）；09:36 第 5 点 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；[07:46 裁定（#114）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头） |
| M03 | 英 | 同 E06：`The main story today is the call foo([1]). Next sentence follows.` | meta：`The main story today is the call foo().` | 不在本次范围，如需处理另开 Issue（同当前） | 删后留下空括号 `foo()`（#113 第 2 条在 meta 上仍成立）；09:36 第 5 点 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；[07:46 裁定（#114）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头） |
| M04 | 英 | 同 E01：`The main story today is the call foo([1]).bar returned errors. Next sentence follows.` | meta：`The main story today is the call foo().bar returned errors.` | 不在本次范围，如需处理另开 Issue（同当前） | `foo().bar`（r2 指出的误删在 meta 上仍成立）；09:36 第 5 点 | [#112 r2](https://github.com/markjin-lab/markjin-lab.github.io/pull/112#issuecomment-6256963243)；[#113 正文](https://github.com/markjin-lab/markjin-lab.github.io/issues/113)；[07:46 裁定（#114）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114)；09:36 裁定（见表头） |
## N. 注释与清理（不影响输出，留给边界情形 PR 一并处理）

| 编号 | 位置 | 输入（当前文字或现状） | 当前 main（f5411ab）实际情况 | 提议的应得 | 理由 | 出处 |
|---|---|---|---|---|---|---|
| N01 | hugo.toml 第 13 行注释 | `# 导语固定开头清单：只影响首页和列表的摘要行（layouts/partials/strip-prefix.html，由 page-description.html 的 strip 参数和 list-summary.html 使用），meta description 和正文不受影响；每项匹配不分大小写，末尾的冒号全角半角都认，冒号后的空白一并去掉；不带冒号的项后面必须跟空白，或者正好在文末；摘要的其余规则见 page-description.html 末尾的注释；导语换新的固定开头时在这里加一项。` | 注释说这个清单用来去掉开头（经 strip-prefix.html）；#114 之后开头不再去掉，清单只在 page-description.html 里用来认出「只剩开头套话」的摘要 | 改为：`# 导语固定开头清单：只用于认出首页和列表里「只剩开头套话」的摘要（page-description.html：摘要以清单中某项起头、比较时不分大小写也不看末尾冒号，且其后不含字母或数字，就不显示摘要行）；开头不会从摘要里去掉；meta description 和正文不受影响；导语换新的固定开头时在这里加一项。` 清单本身不动 | 注释与 #114 合并后的行为不符 | [#114 范围声明（留给边界情形 PR）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| N02 | layouts/partials/strip-prefix.html | 整个文件 | 仓库里除 hugo.toml 的过时注释外没有任何地方调用它（`rg strip-prefix` 只命中该文件自身和 hugo.toml 第 13 行） | 删除该文件，与 N01 同一次提交 | 已无调用，留着容易让人以为开头仍会被去掉 | [#114 范围声明（留给边界情形 PR）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |
| N03 | layouts/partials/list-summary.html 第 4 行注释 | `1. 必须是非空字符串（去掉首尾空白后不为空）；2. 不超过 320 个字符（Unicode 字符数）；` | 只写了 320，没说它和自动摘要的 360 是两回事 | 第 2 条改为：`2. 不超过 320 个字符（Unicode 字符数）。320 是手写 list_summary 的上限；自动摘要的整句上限是 360（page-description.html，Grok Bot 2026-10-19 07:46 SGT 裁定），两者是不同的值，互不影响；` 校验逻辑和报错文字不动 | 避免把两个上限混为一谈 | 站点质检 bot 建议（协调者 2026-10-19 09:28 SGT 转达）；[07:46 裁定（#114）](https://github.com/markjin-lab/markjin-lab.github.io/pull/114) |

## 句中编号

**选项一：保留句中编号（维持现状）**：采纳（09:36 第 1 点）。A 组和 K05 的应得按保留编号写；句中编号计入 360 字上限；手写 list_summary 要把句中编号逐字写上才能通过校验。A 组不需改代码，只补测试。

**选项二：删句中编号**：未采纳（09:36）。

## 规则之间的冲突（均已裁定）

1. **ASCII `...` 与「…」后接大写**：r4 要删，08:56 要保留。由 09:36 第 2 点解决：`...` 与 `…` 同样处理，都保留编号（J01、F06）；r4 要删的意见不采纳。
2. **`[1]….`**：原表假设删编号。由 09:36 第 3 点解决：编号后面紧跟的是省略号，不是句末标点，保留（F03；同理 F05 `[1]…。` 也保留）。
3. **哪些算「全角闭合符号」**：由 09:36 第 4 点解决：弯引号 `”’` 不算。G03（`」`）删编号，G04（`”`）保留。
4. **「算句末」是否也管断句**：由 09:36 第 6 点解决：只用来判断删不删编号，不改变断句。G01 摘要为 `研究指出（结果）.另一句。`。
5. **放宽闭合符号与空括号**：由 09:36 第 7 点解决：删掉编号会留下空括号时保留编号（E06、E07、B09）。
6. **句中编号与 360 上限**：由 09:36 第 1 点解决：保留句中编号，占用上限可以接受（K05 截断）。
7. **可见摘要与清洗结果**：由 09:36 第 8 点解决：首页不显示摘要的英文写法（B07、B08、D04、F02、F06、I02、I03、J01–J06，以及本轮新增的 S07、S12、S13）以清洗后的文字和 list_summary 校验验收；B07–J05 各行已补 list_summary 候选及校验应得，候选在 f5411ab 上逐条单独建站取得当前结果；D04、J06 与 S07、S12、S13 也已补 list_summary 候选及校验应得，在 main 上逐条单独建站核对。
8. **meta 与首页列表两条规则**：由 09:36 第 5 点解决：meta 问题不并入 #113，M 组只作参考，不在本次范围，如需处理另开 Issue。
9. **U+0085**：09:36 的 8 点都没有涉及。这一条并不和别的应得矛盾：C05 只把编号前的 U+0085 并入空白，其他位置的 U+0085 原样保留，不需另行裁定；如要全面处理，另开 Issue。
10. **退回 meta 时句中编号消失**（K10、K11）：由 09:40 第 1 点解决：维持现状，不在 #113 处理，另开 meta Issue，排在 #113 合并之后。
11. **空引号**（B10）：由 09:40 第 2 点解决：空符号保护扩大到引号、括号、书名号、方括号等一切成对符号，删后会留下空的成对符号就保留编号。按此复核并新增 B11–B22。
12. **第 3 点的理由与 B、J 组的删法**：由 09:40 第 3 点解决：编号和句末标点之间只允许夹闭合符号，夹了省略号或其他任何字符就保留；触发空符号保护的仍然保留。已写进表头「规则」一节。
13. **规则第 2 条「可隔空白」与 09:40 第 3 点**（审查 af9b6b2 第 1 条）：由 09:40 第 3 点解决：编号和句末标点之间只许夹闭合符号，夹空白也保留。上一版规则第 2 条写了「（可隔空白）」，与此矛盾，已删；补 S01–S10（普通空格、U+00A0、U+2009、U+3000、U+0085，中英文，`.`、`?`、`。`、`！`），应得都是保留编号。句末标点之后接空白或段末仍是句末判断（S11–S13 照删）。这些写法当前 main 是删编号、留下空白（如 `一份报告 。`），所以 S01–S08、S10 的应得与当前 main 不同；现有页面里没有这种写法，见下文。

## 定稿前自洽检查

**逐行复核**
- 按表头「规则」第 1–6 条逐行核对 A–K、S 各行的应得，没有互相矛盾的行，也没有待定项。
- 空白：规则第 2、3 条不再允许编号与句末标点、编号与闭合符号、闭合符号与句末标点之间有任何空白；B23、B24、S01–S10 都保留编号。编号前的空白（C 组）和编号串内部的空白（H05、S10 的 `[1]、[2]`）不受影响。
- 空成对符号：全表凡删掉编号后成对符号里只剩空白的行（B09–B22、B25、B27、E06、E07）应得都是保留编号。B25 的内层「」为空、外层（）里还有正文，按最内层判断，仍保留。B26 编号前的 `’` 是撇号，不是开符号，照删。
- 弯引号与 `.汉字`：G04（`”`）、G05（`’`）保留；G01（`）`）、G03（`」`）、G06（`』`）、G07（`】`）、G08（`》`）删编号。
- J02 `[1]?!`：编号后直接是 `?!` 这串连续标点，归入「编号后紧接句末」，不属于「夹闭合符号」。
- list_summary 校验与 K 组截断：句中编号保留后，手写 list_summary 须逐字含句中编号，与自动摘要一致；先清洗后截断，K05、K12 截断后保留编号；K10、K11 按 09:40 第 1 点维持现状。
- 模拟核对：起草时按表头规则写了一份 Python 模拟（只用于核对，不是实现），对表中 A–J、S 组 91 行逐行比对应得，0 处不符。仓库里对应的是 tests/test_citation_edge.py 与夹具 tests/fixtures/citation-edge/，对 A–K、S 组 103 行逐行实际构建断言。

**「编号 + 空白 + 句末标点」与现有 33 个页面**
- 在 f5411ab 的全部 24 个内容文件里逐行搜索「编号（含连续编号）+ 一个或多个空白（含 `&nbsp;`、U+00A0、U+2009、U+3000、U+0085 等）+ `。！？.!?`」：0 处。
- 在 f5411ab 构建出的全部 33 个 HTML 页面里，把编号链接还原成 `[n]` 后在正文文本中搜同一写法：0 处；另在全部 80 条首页/列表摘要和 meta description 里搜「空白 + 句末标点」（即 main 删了编号、留下空白的痕迹）：0 处。tests/ 下现有夹具和测试里也没有这种写法。
- 所以删去「可隔空白」不会改变现有产物。
- 本轮要删编号、而当前 main 不删的写法共四类：编号后夹闭合符号再接句末（B01–B03、B06–B08、J03–J05）；编号后直接接 `.!?` 开头的连续标点（J02）；编号前是 U+0085（C05）；全角闭合符号后 `.` 接汉字（G01、G03、G06–G08）。要保留、而当前 main 删的写法是 S01–S08、S10。在 24 个内容文件里，编号后接闭合符号只有 2026-10-14 中英两页正文第 75、91 行的 `([7], [9])`、`（[7]、[9]）`，不在导语段，而且括号里只有编号，按空符号保护也保留；U+0085、编号后接省略号、`.` 后接汉字都是 0 处。
- 模拟核对：起草时用 Python 对 f5411ab 上 20 个有导语段的内容文件，分别用本表规则的模拟和现行正则的 Python 等价写法处理导语段，0 处不同。**这是模拟得出的结果，不是实际产物；逐字节不变最终以实现后对 main 的构建产物 diff 为准。**

**结论**：经审查 af9b6b2 指出的「可隔空白」一条已按 09:40 第 3 点改正（冲突 13）。改正后逐行复核，没有发现需要另行裁定的新冲突；表里没有待定项。
