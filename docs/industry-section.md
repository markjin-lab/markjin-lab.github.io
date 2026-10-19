# 产业链接段与“产业与经济数据”小节：写作说明 / Writing notes for industry links and the “Industry and economic data” section

依据：路线图 v1.12 第 15.2 节（docs/roadmap.md）。本说明只讲写法和模板用法；规则以路线图为准，二者不一致时照路线图。

## 中文

### 写法
- 只写作用在哪一端（需求端、成本端或利润端），不写会怎样变。
- 来源没有测的一步，要标明是推断。
- 不评论宏观走势，不预测涨跌。
- 说不出作用在哪一端的条目（“无”档），不写产业链接段，不硬套。
- 数据只用已批准公开、且已通过公开门禁的数；其余机构的数只作线索，不进公开稿。
- 没有合适的数，就只写产业链接段；“产业与经济数据”小节整个不出现，不复述旧数。
- 第七节写作纪律照旧：正文不出现内部分类标签和内部用语，术语给白话解释；美国数据写明“美国”，不拿美国数推断中国；宽口径数据写明它不专指本条所说的环节。

### 模板用法
产业链接段放在条目的“为什么重要”之后：

```
{{< industry-link item="1" industry="ai" side="demand" inference="来源没有测的那一步" >}}来源里的哪个量对应这个产业的哪项需求、成本或利润 [1]。{{< /industry-link >}}
```

- `item`：所在条目的编号，只用作段落锚点 `industry-link-<编号>`，不显示。
- `industry`：`energy`、`semiconductors`、`ai`、`manufacturing`（试点四个产业）；`side`：`demand`、`cost`、`profit`。
- `inference`：可选；渲染时后接“（推断：来源没有测这一步）”。
- `economy`（可选）：`investment`、`consumption`、`prices`、`credit`、`housing`、`external`、`fiscal`、`employment`；说不出对应哪一块时省略，段落写到产业这一层为止。
- `series`、`publisher`、`frequency`：可选，三项同给且须给 `economy`；渲染时固定附“宽口径，不专指本条所说的环节”。

“产业与经济数据”小节只在有可写的数据时用，里面只能放数据条目：

```
{{< industry-data >}}
{{< industry-datum series="美国……" publisher="原始发布机构" frequency="monthly" period="……" value="……" released="YYYY-MM-DD" cite="4" >}}
{{< /industry-data >}}
```

- 数据条目只渲染发布值，以及可选的计算值（`calc`、`calc_value`、`formula` 三项同给）；没有正文，也没有写走势或分段的位置。
- 小节标题取 i18n，中文为“产业与经济数据”，英文为“Industry and economic data”。不用这些模板的页面上不出现这个小节。
- 参数不合规时构建失败（`tests/test_industry_section.py` 列出了各种情形）。

## English

### How to write
- Say only which side the item acts on (demand, cost or profit); do not say how it will change.
- Mark any step the source did not measure as an inference.
- No commentary on macroeconomic trends and no predictions of rises or falls.
- If no side can be named for an item, write no industry link; do not force one.
- Use only figures that are approved for publication and have cleared the public gate. Figures from any other agency are leads only and never appear in a published piece.
- If there is no suitable figure, write the industry link alone; leave out the “Industry and economic data” section entirely and do not repeat old figures.
- Two limits on segments (ranges for the next reading):
  1. Do not write segments until the ledger can reconcile them by group.
  2. Never write segments for daily price series.
- Existing rules still apply: no internal labels or internal terms in the text, and plain-language explanations for technical terms; label US data as US and do not infer China from US figures; say when a broad series is not specific to the step the item describes.

### Template usage
Place the industry link after the item's “Why it matters” paragraph:

```
{{< industry-link item="1" industry="ai" side="demand" inference="The step the source did not measure" >}}Which quantity in the source maps to which item of this industry [1].{{< /industry-link >}}
```

- `item` is the item number, used only for the paragraph anchor `industry-link-<number>`; it is not shown.
- `industry`: `energy`, `semiconductors`, `ai` or `manufacturing` (the four pilot industries); `side`: `demand`, `cost` or `profit`.
- `inference` is optional and is followed by “(Inference: the source did not measure this step).”
- `economy`, `series`, `publisher` and `frequency` work as in the Chinese notes above; without `economy` the paragraph stops at the industry level.

Use the “Industry and economic data” section only when there is data to report, and put only data entries in it (`industry-data` containing `industry-datum`, as above). Data entries render the released value and, optionally, a computed value with its formula; they have no free-text body and no slot for trends or segments. Invalid parameters fail the build.
