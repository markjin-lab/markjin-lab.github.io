"""构建级用例：日报小节“产业与经济数据 / Industry and economic data”和产业链接段（路线图 v1.12 第 15.2 节；
layouts/shortcodes/industry-link.html、industry-data.html、industry-datum.html，写法见 docs/industry-section.md）。
- 示例日报只放在 tests/fixtures/industry-section/content（不进仓库 content/），在临时目录构建：
  中英小节标题与 i18n 逐字一致、各出现一次；产业链接段的产业、端、推断标注、对照序列、引注链接按模板渲染；数据条目只有数值字段和固定的宽口径说明；
- 同一夹具里不用这些 shortcode 的日报、列表、首页和 feed 都不出现小节标题、产业链接段或推断标注；用仓库 content/ 构建时任何页面都不出现；
- 参数不合规（端、产业、条目编号、出处、小节里另写文字、数据条目放在小节外、数值字段写成文字等）时构建失败。"""
import html, re, shutil, tomllib, unittest
from test_list_summary import ROOT, build, run_build

FX = ROOT / "tests" / "fixtures" / "industry-section" / "content"
I18N = {lang: tomllib.loads((ROOT / "i18n" / ("%s.toml" % lang)).read_text(encoding="utf-8")) for lang in ("zh", "en")}
USED = {"zh": "posts/daily/2026-10-19/index.html", "en": "en/posts/daily/2026-10-19/index.html"}
UNUSED = ("posts/daily/2026-10-18/index.html", "en/posts/daily/2026-10-18/index.html")
MARKERS = ('class="industry-link"', 'class="industry-datum"', 'id="industry-link-',
           "产业与经济数据", "Industry and economic data", "产业链接：", "Industry link:",
           "（推断：来源没有测这一步）", "(Inference: the source did not measure this step)")
URL = {1: "https://example.org/one", 2: "https://example.org/two", 4: "https://example.org/four?a=1&amp;b=2", 5: "https://example.org/five"}


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
                         "这是交付效果的指标，不是付费需求。交付效果会不会影响客户对这类服务的需求（推断：来源没有测这一步）。" % cite(1))
        self.assertEqual(link_para(s, 2),
                         "产业链接：半导体与算力硬件，作用在需求端。来源报告的是新增的数据中心芯片订单量 %s，对应这个产业的芯片需求。"
                         "这些订单会不会落成实际出货（推断：来源没有测这一步）。往整体经济看，对应的是投资这一块；"
                         "可以对照的公开数据是美国示例工业生产指数（示例发布机构，月度；宽口径，不专指本条所说的环节）。" % cite(2))
        self.assertIsNone(link_para(s, 3))

    def test_link_paragraph_en(self):
        s = self.pages[USED["en"]]
        self.assertEqual(html.unescape(link_para(s, 1)), html.unescape(
            "Industry link: AI models and software services, on the demand side. The source measures how much an agent&rsquo;s "
            "delivery improves the customer&rsquo;s metric %s; this measures delivery results, not paying demand. Whether delivery "
            "results affect customer demand for such services is not known (Inference: the source did not measure this step)." % cite(1)))
        self.assertEqual(link_para(s, 2),
                         "Industry link: semiconductors and computing hardware, on the demand side. The source reports new data-centre chip "
                         "orders %s, which map to chip demand in this industry. Whether these orders turn into actual shipments is not known "
                         "(Inference: the source did not measure this step). For the economy as a whole it bears on investment; a public "
                         "series to compare against is a US example industrial production index (Example Publisher, monthly; a broad "
                         "series, not specific to this step)." % cite(2))
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

    def test_inference_marker_counts(self):
        self.assertEqual(self.pages[USED["zh"]].count("（推断：来源没有测这一步）"), 2)
        self.assertEqual(self.pages[USED["en"]].count("(Inference: the source did not measure this step)"), 2)

    def test_data_entries(self):
        zh = re.findall(r'<p class="industry-datum">(.*?)</p>', self.pages[USED["zh"]], re.S)
        self.assertEqual(zh, [
            "美国示例产出指数（示例发布机构，月度）：观测期 2026 年 9 月，发布值为 102.3，2026-10-17 发布 %s。"
            "同比为 1.2%%，算式：(102.3/101.1-1)×100=1.2，按发布值计算。宽口径，不专指某个具体环节。" % cite(4),
            "美国示例现货价（示例发布机构，日度）：观测期 2026-10-16，发布值为 71.25 美元/桶，2026-10-17 发布 %s、%s。"
            "宽口径，不专指某个具体环节。" % (cite(5), cite(4)),
        ])
        en = re.findall(r'<p class="industry-datum">(.*?)</p>', self.pages[USED["en"]], re.S)
        self.assertEqual(en, [
            "US example output index (Example Publisher, monthly): the released value for September 2026 is 102.3, published "
            "2026-10-17 %s. Year-over-year change: 1.2%%; formula: (102.3/101.1-1)×100=1.2, computed from the released values. "
            "A broad series, not specific to any single step." % cite(4),
            "US example spot price (Example Publisher, daily): the released value for 2026-10-16 is 71.25 US dollars per barrel, "
            "published 2026-10-17 %s, %s. A broad series, not specific to any single step." % (cite(5), cite(4)),
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
GOOD_DATUM = '{{< industry-datum series="美国示例" publisher="示例机构" frequency="monthly" period="2026 年 9 月" value="1.5" released="2026-10-17" cite="1" >}}'
BAD = {  # 用例名 → (正文片段, 报错里应有的文字)
    "side": (GOOD_LINK.replace('side="demand"', 'side="up"'), "side 只能是"),
    "industry": (GOOD_LINK.replace('industry="ai"', 'industry="finance"'), "industry 只能是"),
    "item": (GOOD_LINK.replace('item="1" ', ""), "item 必须是正整数"),
    "empty_body": ('{{< industry-link item="1" industry="ai" side="demand" >}} {{< /industry-link >}}', "缺少正文"),
    "missing_cite_def": (GOOD_LINK.replace("[1]", "[9]"), "没有对应的引用定义"),
    "economy": (GOOD_LINK.replace('side="demand"', 'side="demand" economy="growth"'), "economy 只能是"),
    "series_without_economy": (GOOD_LINK.replace('side="demand"', 'side="demand" series="s" publisher="p" frequency="monthly"'), "没有给 economy"),
    "partial_series": (GOOD_LINK.replace('side="demand"', 'side="demand" economy="investment" series="s"'), "须同时给出"),
    "datum_outside_section": (GOOD_DATUM, "只能放在 industry-data 小节里"),
    "empty_section": ("{{< industry-data >}}\n{{< /industry-data >}}", "没有 industry-datum"),
    "text_in_section": ("{{< industry-data >}}\n%s\n后市看涨。\n{{< /industry-data >}}" % GOOD_DATUM, "只能放 industry-datum"),
    "value_not_number": ("{{< industry-data >}}\n%s\n{{< /industry-data >}}" % GOOD_DATUM.replace('value="1.5"', 'value="走强"'), "value 必须是数字"),
    "calc_value_text": ("{{< industry-data >}}\n%s\n{{< /industry-data >}}" % GOOD_DATUM.replace('cite="1"', 'cite="1" calc="同比" calc_value="将继续上升" formula="1=1"'), "calc_value 只能是数字"),
    "formula_text": ("{{< industry-data >}}\n%s\n{{< /industry-data >}}" % GOOD_DATUM.replace('cite="1"', 'cite="1" calc="同比" calc_value="1%" formula="预计 1"'), "formula 只能含"),
    "datum_missing_cite": ("{{< industry-data >}}\n%s\n{{< /industry-data >}}" % GOOD_DATUM.replace(' cite="1"', ""), "缺少 cite"),
}


class InvalidUsageFailsBuild(unittest.TestCase):
    def test_valid_minimal_builds(self):
        self.check(GOOD_LINK + "\n\n{{< industry-data >}}\n%s\n{{< /industry-data >}}" % GOOD_DATUM, None)

    def test_invalid(self):
        for name, (body, msg) in BAD.items():
            with self.subTest(case=name):
                self.check(body, msg)

    def check(self, body, msg):
        def hook(site):
            d = site / "content" / "posts" / "daily"
            for f in list(d.glob("2026-*.md")):
                f.unlink()
            (d / "2026-10-01.md").write_text(
                "---\ntitle: t\ndate: 2026-10-01T05:00:00+08:00\n---\n导语 [1]。\n\n%s\n\n[1]: https://example.org/one\n" % body,
                encoding="utf-8")
        tmp, out, r = run_build(FX, hook=hook)
        try:
            if msg is None:
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            else:
                self.assertNotEqual(r.returncode, 0, "build should fail")
                self.assertIn(msg, r.stdout + r.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
