"""构建级用例：日报小节“产业与经济数据 / Industry and economic data”和产业链接段（路线图 v1.12 第 15.2 节；
layouts/shortcodes/industry-link.html、industry-data.html、industry-datum.html，写法见 docs/industry-section.md）。
- 示例日报只放在 tests/fixtures/industry-section/content（不进仓库 content/），在临时目录构建：
  中英小节标题与 i18n 逐字一致、各出现一次；产业链接段的产业、端、推断句、对照序列及其出处、引注链接按模板渲染；
  数据条目只有数值字段；宽口径说明只在作者写了 broad="true" 时出现；没有对照序列时段落写到产业这一层为止；
- 同一夹具里不用这些 shortcode 的日报、列表、首页和 feed 都不出现小节标题、产业链接段或推断标注；用仓库 content/ 构建时任何页面都不出现；
- 参数不合规（端、产业、条目编号、出处、只给 economy 不给对照序列、缺 series_cite、broad 取值、推断带句末标点、小节里另写文字、
  数据条目放在小节外、数值字段写成文字、千分位不规范、日期不存在、引用定义地址不是 HTTP(S)、代码围栏里的伪定义等）时构建失败；
- 出处标记只在正文文字里替换：<code>、链接文字、标签属性（含引号里的 >）、注释里的方括号和紧跟字母数字的 [n] 原样保留；
- 引用定义按 CommonMark 逐行认：代码围栏（同符号、长度不短于开栏才闭栏）、HTML 块里和接在段落文字后的“定义”不算。"""
import html, re, shutil, tomllib, unittest
from test_list_summary import ROOT, build, run_build

FX = ROOT / "tests" / "fixtures" / "industry-section" / "content"
I18N = {lang: tomllib.loads((ROOT / "i18n" / ("%s.toml" % lang)).read_text(encoding="utf-8")) for lang in ("zh", "en")}
USED = {"zh": "posts/daily/2026-10-19/index.html", "en": "en/posts/daily/2026-10-19/index.html"}
UNUSED = ("posts/daily/2026-10-18/index.html", "en/posts/daily/2026-10-18/index.html")
MARKERS = ('class="industry-link"', 'class="industry-datum"', 'id="industry-link-',
           "产业与经济数据", "Industry and economic data", "产业链接：", "Industry link:",
           "这一联系是推断", "this connection is an inference", "这个指标覆盖范围较广", "This measure covers a broad range")
URL = {1: "https://example.org/one", 2: "https://example.org/two", 4: "https://example.org/four?a=1&amp;b=2",
       5: "https://example.org/five", 6: "https://example.org/six", 7: "https://example.org/seven"}
OLD_INFERENCE = ("（推断：来源没有测这一步）", "(Inference: the source did not measure this step)", "is not known")


def cite(n):
    return '[<a href="%s">%d</a>]' % (URL[n], n)


def link_para(s, item):
    m = re.search(r'<p class="industry-link" id="industry-link-%d">(.*?)</p>' % item, s, re.S)
    return m.group(1) if m else None


class IndustrySectionRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp, cls.out = build(FX)
        cls.pages = {p.relative_to(cls.out).as_posix(): p.read_text(encoding="utf-8")
                     for p in cls.out.rglob("*") if p.is_file() and p.suffix in (".html", ".xml")}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_heading_from_i18n(self):
        self.assertEqual(I18N["zh"]["industry_data_heading"], "产业与经济数据")
        self.assertEqual(I18N["en"]["industry_data_heading"], "Industry and economic data")
        for lang, rel in USED.items():
            with self.subTest(lang=lang):
                s = self.pages[rel]
                heads = [html.unescape(h) for h in re.findall(r"<h2[^>]*>([^<]*)</h2>", s)]
                self.assertEqual(heads.count(I18N[lang]["industry_data_heading"]), 1)
                other = I18N["en" if lang == "zh" else "zh"]["industry_data_heading"]
                self.assertNotIn(other, s)
                # 小节在“出处”之前，只含两条数据
                sec = s.split(">%s</h2>" % I18N[lang]["industry_data_heading"], 1)[1].split("<h2", 1)[0]
                self.assertEqual(len(re.findall(r'<p class="industry-datum">', sec)), 2)
                self.assertEqual(re.sub(r'(?s)<p class="industry-datum">.*?</p>', "", sec).strip(), "")

    def test_link_paragraph_zh(self):
        s = self.pages[USED["zh"]]
        self.assertEqual(link_para(s, 1),
                         "产业链接：AI 模型与软件服务，作用在需求端。来源测的是智能体的交付让客户指标提高了多少 %s，"
                         "这是交付效果的指标，不是付费需求。来源没有测量交付效果是否影响客户对这类服务的需求；这一联系是推断。" % cite(1))
        self.assertEqual(link_para(s, 2),
                         "产业链接：半导体与算力硬件，作用在需求端。来源报告的是新增的数据中心芯片订单量 %s，对应这个产业的芯片需求。"
                         "来源没有测量这些订单是否转化为实际出货；这一联系是推断。放到整体经济中看，这与投资有关。"
                         "可对照的公开数据是美国示例工业生产指数（示例发布机构，月度）%s。"
                         "这个指标覆盖范围较广，不专指本条所说的环节。" % (cite(2), cite(6)))
        self.assertIsNone(link_para(s, 3))

    def test_link_paragraph_en(self):
        s = self.pages[USED["en"]]
        self.assertEqual(html.unescape(link_para(s, 1)), html.unescape(
            "Industry link: AI models and software services, on the demand side. The source measures how much an agent&rsquo;s "
            "delivery improves the customer&rsquo;s metric %s; this measures delivery results, not paying demand. The source did "
            "not measure whether delivery results affect customer demand for such services; this connection is an inference." % cite(1)))
        self.assertEqual(link_para(s, 2),
                         "Industry link: semiconductors and computing hardware, on the demand side. The source reports new data-centre chip "
                         "orders %s, which map to chip demand in this industry. The source did not measure whether these orders turn into "
                         "actual shipments; this connection is an inference. In the wider economy, this relates to investment. One public "
                         "measure for comparison is a US example industrial production index (Example Publisher, monthly) %s. This measure "
                         "covers a broad range of activity, rather than the specific activity in this story." % (cite(2), cite(6)))
        self.assertIsNone(link_para(s, 3))

    def test_link_follows_why_it_matters(self):
        for lang, rel in USED.items():
            s = self.pages[rel]
            why = "为什么重要：" if lang == "zh" else "Why it matters:"
            for item in (1, 2):
                with self.subTest(lang=lang, item=item):
                    head = re.search(r"<p><strong>(第 %d 条|Item %d)：?:?" % (item, item), s)
                    self.assertIsNotNone(head)
                    rest = s[head.end():]
                    self.assertLess(rest.index(why), rest.index('id="industry-link-%d"' % item))

    def test_inference_sentence_counts(self):
        # 推断是完整句的一部分，不再用固定括注；英文不再重复“is not known”
        self.assertEqual(self.pages[USED["zh"]].count("；这一联系是推断。"), 2)
        self.assertEqual(self.pages[USED["en"]].count("; this connection is an inference."), 2)
        for rel in USED.values():
            for w in OLD_INFERENCE:
                self.assertNotIn(w, self.pages[rel])

    def test_item_without_link(self):
        # 第 3 条标题不向读者说明“不写产业链接段”，但确实没有链接段
        for lang, rel in USED.items():
            with self.subTest(lang=lang):
                s = self.pages[rel]
                self.assertIn("<strong>第 3 条：示例条目三。</strong>" if lang == "zh" else "<strong>Item 3: example item three.</strong>", s)
                self.assertIsNone(link_para(s, 3))
                self.assertNotIn("产业链接段", s)
                self.assertNotIn("no industry link", s)

    def test_industry_level_only_without_series(self):
        # 第 1 条没有对照序列：段落写到产业这一层为止，不出现整体经济的判断
        self.assertNotIn("整体经济", link_para(self.pages[USED["zh"]], 1))
        self.assertNotIn("wider economy", link_para(self.pages[USED["en"]], 1))

    def test_data_entries(self):
        zh = re.findall(r'<p class="industry-datum">(.*?)</p>', self.pages[USED["zh"]], re.S)
        self.assertEqual(zh, [
            "美国示例产出指数（示例发布机构，月度）：2026 年 9 月，发布值为102.3；发布于2026-10-17 %s。"
            "同比为1.2%%；按发布值计算：(102.3/101.1-1)×100%%≈1.2%%。这个指标覆盖范围较广，不专指某个产业环节。" % cite(4),
            # 现货价没有写 broad="true"：不附宽口径说明
            "美国示例现货价（示例发布机构，日度）：2026-10-16，发布值为71.25 美元/桶；发布于2026-10-17 %s、%s。" % (cite(5), cite(4)),
        ])
        en = re.findall(r'<p class="industry-datum">(.*?)</p>', self.pages[USED["en"]], re.S)
        self.assertEqual(en, [
            "US example output index (Example Publisher, monthly): the reported value for September 2026 was 102.3, released on "
            "2026-10-17 %s. Year-over-year change: 1.2%% (calculated from the reported values: (102.3/101.1-1)×100%%≈1.2%%). "
            "This measure covers a broad range of activity, rather than any one part of an industry." % cite(4),
            "US example spot price (Example Publisher, daily): the reported value for 2026-10-16 was 71.25 US dollars per barrel, "
            "released on 2026-10-17 %s, %s." % (cite(5), cite(4)),
        ])

    def test_absent_where_unused(self):
        others = [k for k in self.pages if k not in USED.values() and not k.endswith(".xml")]
        for rel in UNUSED:
            self.assertIn(rel, others)
        for k in others:
            with self.subTest(page=k):
                s = html.unescape(self.pages[k])
                for w in MARKERS:
                    self.assertNotIn(html.unescape(w), s)

    def test_absent_in_feed_items_of_unused_pages(self):
        # feed 里用到小节的那一篇的 <description> 是它自己的摘要，可以含产业链接段；其他条目不得出现
        seen = 0
        for k in (k for k in self.pages if k.endswith(".xml")):
            for item in re.findall(r"<item>.*?</item>", self.pages[k], re.S):
                if "/posts/daily/2026-10-19/" in item:
                    continue
                seen += 1
                with self.subTest(feed=k):
                    s = html.unescape(item)
                    for w in MARKERS:
                        self.assertNotIn(html.unescape(w), s)
        self.assertGreater(seen, 0)


class RepoContentUnchanged(unittest.TestCase):
    """仓库 content/ 没有用这些 shortcode：构建产物里任何页面都不出现小节或产业链接段。"""

    def test_no_markers(self):
        tmp, out = build(ROOT / "content", with_data=True)
        try:
            pages = [p for p in out.rglob("*") if p.is_file() and p.suffix in (".html", ".xml")]
            self.assertGreater(len(pages), 5)
            for p in pages:
                s = html.unescape(p.read_text(encoding="utf-8"))
                for w in MARKERS:
                    self.assertNotIn(html.unescape(w), s, p.relative_to(out).as_posix())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


GOOD_LINK = '{{< industry-link item="1" industry="ai" side="demand" >}}来源测的是某个量 [1]。{{< /industry-link >}}'
SERIES = 'economy="investment" series="美国示例序列" publisher="示例机构" frequency="monthly" series_cite="2"'
GOOD_SERIES_LINK = GOOD_LINK.replace('side="demand"', 'side="demand" ' + SERIES)
GOOD_DATUM = '{{< industry-datum series="美国示例" publisher="示例机构" frequency="monthly" period="2026 年 9 月" value="1.5" released="2026-10-17" cite="1" >}}'


def section(datum):
    return "{{< industry-data >}}\n%s\n{{< /industry-data >}}" % datum


def datum_with(old, new):
    return section(GOOD_DATUM.replace(old, new))


L7 = GOOD_LINK.replace("[1]", "[7]")
NODEF = "出处编号 [7] 在正文里没有对应的引用定义"
CALC = 'cite="1" calc="同比" calc_value="1%" formula="1/1≈1"'
BAD = {  # 用例名 → (正文片段, 报错里应有的文字[, 页面末尾另加的文字])
    "side": (GOOD_LINK.replace('side="demand"', 'side="up"'), "side 只能是"),
    "industry": (GOOD_LINK.replace('industry="ai"', 'industry="finance"'), "industry 只能是"),
    "item": (GOOD_LINK.replace('item="1" ', ""), "item 必须是正整数"),
    "empty_body": ('{{< industry-link item="1" industry="ai" side="demand" >}} {{< /industry-link >}}', "缺少正文"),
    "missing_cite_def": (GOOD_LINK.replace("[1]", "[9]"), "没有对应的引用定义"),
    "inference_trailing_punct": (GOOD_LINK.replace('side="demand"', 'side="demand" inference="这些订单是否转化为实际出货。"'), "不带句末标点"),
    # 只给 economy、不给对照序列：不能输出整体经济判断
    "economy_only": (GOOD_LINK.replace('side="demand"', 'side="demand" economy="investment"'), "没有对照序列"),
    "economy_bad": (GOOD_SERIES_LINK.replace('economy="investment"', 'economy="growth"'), "economy 只能是"),
    "series_without_economy": (GOOD_SERIES_LINK.replace('economy="investment" ', ""), "缺少 economy"),
    "partial_series": (GOOD_SERIES_LINK.replace('publisher="示例机构" ', ""), "缺少 publisher"),
    "frequency_bad": (GOOD_SERIES_LINK.replace('frequency="monthly"', 'frequency="hourly"'), "frequency 只能是"),
    # 对照序列必须有自己的出处
    "series_cite_missing": (GOOD_SERIES_LINK.replace(' series_cite="2"', ""), "缺少 series_cite"),
    "series_cite_not_number": (GOOD_SERIES_LINK.replace('series_cite="2"', 'series_cite="2,3"'), "series_cite 必须是一个出处编号"),
    "series_cite_no_def": (GOOD_SERIES_LINK.replace('series_cite="2"', 'series_cite="8"'), "出处编号 [8] 在正文里没有对应的引用定义"),
    # 宽口径说明只能由作者确认
    "link_broad_without_series": (GOOD_LINK.replace('side="demand"', 'side="demand" broad="true"'), "给了 broad，但没有对照序列"),
    "link_broad_bad_value": (GOOD_SERIES_LINK.replace('series_cite="2"', 'series_cite="2" broad="yes"'), "broad 只能写"),
    "datum_broad_bad_value": (datum_with('cite="1"', 'cite="1" broad="maybe"'), "broad 只能写"),
    "datum_outside_section": (GOOD_DATUM, "只能放在 industry-data 小节里"),
    "empty_section": ("{{< industry-data >}}\n{{< /industry-data >}}", "没有 industry-datum"),
    "text_in_section": ("{{< industry-data >}}\n%s\n后市看涨。\n{{< /industry-data >}}" % GOOD_DATUM, "只能放 industry-datum"),
    "value_not_number": (datum_with('value="1.5"', 'value="走强"'), "value 必须是数字"),
    "value_double_comma": (datum_with('value="1.5"', 'value="1,,2"'), "value 必须是数字"),
    "value_bad_grouping": (datum_with('value="1.5"', 'value="1,2"'), "value 必须是数字"),
    "value_bad_grouping_long": (datum_with('value="1.5"', 'value="12,34,567"'), "value 必须是数字"),
    "released_not_date": (datum_with('released="2026-10-17"', 'released="2026-99-99"'), "真实存在的日期"),
    "released_feb30": (datum_with('released="2026-10-17"', 'released="2026-02-30"'), "真实存在的日期"),
    "released_feb29_nonleap": (datum_with('released="2026-10-17"', 'released="2027-02-29"'), "真实存在的日期"),
    "released_day_zero": (datum_with('released="2026-10-17"', 'released="2026-10-00"'), "真实存在的日期"),
    "calc_value_text": (datum_with('cite="1"', 'cite="1" calc="同比" calc_value="将继续上升" formula="1=1"'), "calc_value 只能是数字"),
    "calc_value_bad_grouping": (datum_with('cite="1"', 'cite="1" calc="同比" calc_value="1,2%" formula="1=1"'), "calc_value 只能是数字"),
    "formula_text": (datum_with('cite="1"', 'cite="1" calc="同比" calc_value="1%" formula="预计 1"'), "formula 只能含"),
    "datum_missing_cite": (datum_with(' cite="1"', ""), "缺少 cite"),
    # 引用定义：只接受 HTTP(S)；代码围栏里的“定义”不算
    "javascript_url": (GOOD_LINK.replace("[1]", "[7]"), "只能是 http:// 或 https://", "\n[7]: javascript:alert(1)\n"),
    "javascript_url_upper": (GOOD_LINK.replace("[1]", "[7]"), "只能是 http:// 或 https://", "\n[7]: <JavaScript:alert(1)>\n"),
    "data_url": (datum_with('cite="1"', 'cite="7"'), "只能是 http:// 或 https://", "\n[7]: data:text/html,x\n"),
    "relative_url": (GOOD_LINK.replace("[1]", "[7]"), "只能是 http:// 或 https://", "\n[7]: /posts/\n"),
    "def_in_backtick_fence": (GOOD_LINK.replace("[1]", "[7]"), "出处编号 [7] 在正文里没有对应的引用定义", "\n```\n[7]: https://example.org/seven\n```\n"),
    "def_in_tilde_fence": (GOOD_LINK.replace("[1]", "[7]"), "出处编号 [7] 在正文里没有对应的引用定义", "\n~~~text\n[7]: https://example.org/seven\n~~~\n"),
    # 代码围栏按 CommonMark 逐行判断：同一符号、长度不短于开栏的行才闭栏；围栏里的伪定义不算
    "def_in_4backtick_fence_after_lone_3": (L7, NODEF, "\n````\n```\n[7]: https://evil.example/fake\n````\n"),
    "def_in_4tilde_fence_after_backticks": (L7, NODEF, "\n~~~~\n````\n[7]: https://evil.example/fake\n~~~~\n"),
    "def_in_fence_after_closer_with_info": (L7, NODEF, "\n```\n``` x\n[7]: https://evil.example/fake\n```\n"),
    "def_in_fence_after_4space_closer": (L7, NODEF, "\n```\n    ```\n[7]: https://evil.example/fake\n```\n"),
    "def_in_indented_fence": (L7, NODEF, "\n   ```\n[7]: https://evil.example/fake\n   ```\n"),
    "def_in_unclosed_fence": (L7, NODEF, "\n````\n```\n[7]: https://evil.example/fake\n"),
    "def_in_list_item_fence": (L7, NODEF, "\n- ```\n  [7]: https://evil.example/fake\n  ```\n"),
    # HTML 块里的“定义”不算；接在段落文字后面的不是引用定义
    "def_in_html_comment_block": (L7, NODEF, "\n<!-- note >\n[7]: https://evil.example/fake\n-->\n"),
    "def_in_html_block": (L7, NODEF, "\n<div>\n[7]: https://evil.example/fake\n</div>\n"),
    "def_after_paragraph_text": (L7, NODEF, "\n段落文字\n[7]: https://evil.example/fake\n"),
}


class InvalidUsageFailsBuild(unittest.TestCase):
    def test_valid_minimal_builds(self):
        s = self.check(GOOD_LINK + "\n\n" + section(GOOD_DATUM), None)
        self.assertIn('<p class="industry-link" id="industry-link-1">产业链接：AI 模型与软件服务，作用在需求端。来源测的是某个量 %s。</p>' % cite(1), s)
        self.assertIn('<p class="industry-datum">美国示例（示例机构，月度）：2026 年 9 月，发布值为1.5；发布于2026-10-17 %s。</p>' % cite(1), s)

    def test_invalid(self):
        for name, case in BAD.items():
            with self.subTest(case=name):
                self.check(case[0], case[1], *case[2:])

    def test_series_without_broad(self):
        # 对照序列不是宽口径时（没写 broad）：有序列及其出处，没有宽口径说明
        s = self.check(GOOD_SERIES_LINK, None)
        self.assertIn("产业链接：AI 模型与软件服务，作用在需求端。来源测的是某个量 %s。放到整体经济中看，这与投资有关。"
                      "可对照的公开数据是美国示例序列（示例机构，月度）%s。</p>" % (cite(1), cite(2)), s)
        self.assertNotIn("覆盖范围较广", s)

    def test_series_with_broad(self):
        s = self.check(GOOD_SERIES_LINK.replace('series_cite="2"', 'series_cite="2" broad="true"'), None)
        self.assertIn("（示例机构，月度）%s。这个指标覆盖范围较广，不专指本条所说的环节。</p>" % cite(2), s)

    def test_datum_strict_values_accepted(self):
        s = self.check(section(GOOD_DATUM.replace('value="1.5"', 'value="1,234.5"').replace('released="2026-10-17"', 'released="2028-02-29"')
                               .replace('cite="1"', 'cite="1" calc="同比" calc_value="-1,000.25%" formula="(1/2-1)×100%≈-50%"')), None)
        self.assertIn("发布值为1,234.5；发布于2028-02-29", s)
        self.assertIn("同比为-1,000.25%；按发布值计算：(1/2-1)×100%≈-50%。</p>", s)
        self.assertNotIn("覆盖范围较广", s)

    def test_cites_only_in_body_text(self):
        # <code> 里、属性里、紧跟字母数字的 [n] 不当出处标记；它们没有引用定义也不报错，原样保留
        body = ('来源测的是某个量 [1]，代码 `[9]` 与[链接](https://example.org/two "见 [9]")，数组 a[9]。'
                '<span title="[9]">x</span>')
        s = self.check('{{< industry-link item="1" industry="ai" side="demand" >}}%s{{< /industry-link >}}' % body, None)
        para = link_para(s, 1)
        self.assertIn("某个量 %s" % cite(1), para)
        self.assertIn("<code>[9]</code>", para)
        self.assertIn('title="见 [9]"', para)
        self.assertIn("a[9]", para)
        self.assertNotIn("example.org/nine", para)
        self.assertEqual(para.count("<a "), 2)

    def test_fence_def_ignored_real_def_used(self):
        # 代码围栏里的伪定义不算，用围栏外的真实定义
        s = self.check(GOOD_LINK.replace("[1]", "[7]"), None,
                       "\n```\n[7]: https://evil.example/fake\n```\n\n[7]: https://example.org/seven\n")
        self.assertIn('[<a href="https://example.org/seven">7</a>]', link_para(s, 1))
        self.assertNotIn('href="https://evil.example', s)

    def test_fence_closers_follow_commonmark(self):
        # 闭栏行可缩进最多 3 个空格、后面可带空格；闭栏后的真实定义有效，围栏里的伪定义不算
        cases = {
            "4backtick": "\n````\n```\n[7]: https://evil.example/fake\n````\n\n[7]: https://example.org/seven\n",
            "longer_closer_trailing_spaces": "\n```\n[7]: https://evil.example/fake\n   `````   \n[7]: https://example.org/seven\n",
            "tilde": "\n~~~ text\n[7]: https://evil.example/fake\n~~~\n\n[7]: https://example.org/seven\n",
            "list_item_fence": "\n- ```\n  [7]: https://evil.example/fake\n  ```\n\n[7]: https://example.org/seven\n",
            "html_comment": "\n<!-- a > b\n[7]: https://evil.example/fake\n-->\n[7]: https://example.org/seven\n",
            "inline_backticks_not_fence": "\n```a``` 不是围栏\n\n[7]: https://example.org/seven\n",
        }
        for name, tail in cases.items():
            with self.subTest(case=name):
                s = self.check(L7, None, tail)
                self.assertIn('[<a href="https://example.org/seven">7</a>]', link_para(s, 1))
                self.assertNotIn('href="https://evil.example', s)

    def test_tags_skipped_quote_aware(self):
        # 原样 HTML（临时站点打开 unsafe）：属性值里的 > 和 [9]、注释里的 > 和 [9] 都不当正文出处；
        # [9] 有定义时也不能把链接写进属性
        body = ('来源测的是某个量 [1]，<span title="a > [9]">甲</span><span title=\'b > [9]\'>乙</span>'
                '<span data-x=[9]>丙</span><!-- c > [9] --><abbr title="d &gt; [9]">丁</abbr>。')
        for tail in ("", "\n[9]: https://example.org/nine\n"):
            with self.subTest(defined=bool(tail)):
                s = self.check('{{< industry-link item="1" industry="ai" side="demand" >}}%s{{< /industry-link >}}' % body, None,
                               tail, unsafe=True)
                para = link_para(s, 1)
                self.assertIn("某个量 %s" % cite(1), para)
                for frag in ('<span title="a > [9]">甲</span>', "<span title='b > [9]'>乙</span>",
                             "<span data-x=[9]>丙</span>", "<!-- c > [9] -->", '<abbr title="d &gt; [9]">丁</abbr>'):
                    self.assertIn(frag, para)
                self.assertNotIn("example.org/nine", para)
                self.assertEqual(para.count("<a "), 1)

    def test_link_text_not_relinked(self):
        # 链接文字里的 [9] 原样保留，不在链接里再套链接
        s = self.check('{{< industry-link item="1" industry="ai" side="demand" >}}量 [1]，见[\\[9\\]](https://example.org/two)。{{< /industry-link >}}',
                       None)
        para = link_para(s, 1)
        self.assertIn('<a href="https://example.org/two">[9]</a>', para)
        self.assertEqual(para.count("<a "), 2)

    def check(self, body, msg, tail="", unsafe=False):
        def hook(site):
            d = site / "content" / "posts" / "daily"
            for f in list(d.glob("2026-*.md")):
                f.unlink()
            (d / "2026-10-01.md").write_text(
                "---\ntitle: t\ndate: 2026-10-01T05:00:00+08:00\n---\n导语 [1]。\n\n%s\n\n"
                "[1]: https://example.org/one\n[2]: https://example.org/two\n%s" % (body, tail),
                encoding="utf-8")
            if unsafe:
                with open(site / "hugo.toml", "a", encoding="utf-8") as f:
                    f.write("\n[markup.goldmark.renderer]\nunsafe = true\n")
        tmp, out, r = run_build(FX, hook=hook)
        try:
            if msg is None:
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                return (out / "posts" / "daily" / "2026-10-01" / "index.html").read_text(encoding="utf-8")
            self.assertNotEqual(r.returncode, 0, "build should fail")
            self.assertIn(msg, r.stdout + r.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
