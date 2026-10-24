"""构建级用例：首页和列表摘要行（layouts/partials/page-description.html 的 strip 参数）。#109 起摘要不再去掉导语开头的套话，
只去句末出处编号，其余与导语原句逐字一致；hugo.toml 的 [params] summary_strip_prefixes 只用来认出「只剩开头套话」的摘要（不显示）。用仓库的 hugo.toml、layouts/、i18n/ 在临时目录里构建：
- 边界用例站点：内容取 tests/fixtures/summary-site/content，不往线上 content 加页面；
- 回归用例：用仓库 content/ 构建，检查 10-16、10-17、10-18 三期（#109：摘要是导语原句，只去句末出处编号）；
- list_summary 反例：tests/fixtures/summary-invalid/<用例>/content，每个都必须让构建失败并给出对应报错；
- 字段隔离：同一批边界页去掉 list_summary 再构建一次，只有列表和首页的摘要行不同，feed、sitemap、各页（含 meta）逐字节相同。
找不到 hugo（环境变量 HUGO、PATH、~/.local/bin/hugo）时：设了环境变量 CI 或 REQUIRE_HUGO（非空，且不是 0/false）就直接失败；都没设才跳过。"""
import html, os, pathlib, re, shutil, subprocess, tempfile, unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
FX = ROOT / "tests" / "fixtures" / "summary-site"
FX_INVALID = ROOT / "tests" / "fixtures" / "summary-invalid"
SUMMARY_P = re.compile(r'<p class="?summary"?>.*?</p>', re.S)
ROW = re.compile(r'<li><a href="([^"]+)">[^<]*</a>(?:\s*<span class="meta">[^<]*</span>)?(?:<p class="summary">(.*?)</p>)?</li>', re.S)


def find_hugo():
    for c in (os.environ.get("HUGO"), shutil.which("hugo"), str(pathlib.Path.home() / ".local/bin/hugo")):
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def hugo_required():
    return any(os.environ.get(k, "").strip().lower() not in ("", "0", "false") for k in ("CI", "REQUIRE_HUGO"))


def require_hugo():
    hugo = find_hugo()
    if hugo:
        return hugo
    if hugo_required():
        raise AssertionError("hugo not found, but CI or REQUIRE_HUGO is set: build-level summary tests must run")
    raise unittest.SkipTest("hugo not found")


def run_build(content_dir, with_data=False, hook=None):
    """在临时目录构建；返回 (tmp, out, CompletedProcess)。with_data 为 true 时连同仓库 data/ 一起拷（只给用仓库 content/ 的构建用）。
    hook(site) 在构建前对临时站点目录做额外改动（只改临时目录，见 test_citation_edge.py）。"""
    hugo = require_hugo()
    tmp = tempfile.mkdtemp(prefix="summary-site-")
    site = pathlib.Path(tmp) / "site"
    site.mkdir()
    shutil.copy(ROOT / "hugo.toml", site / "hugo.toml")
    for d in ("layouts", "i18n") + (("data",) if with_data and (ROOT / "data").is_dir() else ()):
        shutil.copytree(ROOT / d, site / d)
    shutil.copytree(content_dir, site / "content")
    if hook:
        hook(site)
    out = pathlib.Path(tmp) / "public"
    r = subprocess.run([hugo, "-s", str(site), "-d", str(out)], capture_output=True, text=True)
    return tmp, out, r


def build(content_dir, with_data=False):
    tmp, out, r = run_build(content_dir, with_data)
    if r.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise AssertionError("hugo build failed:\n" + r.stdout + r.stderr)
    return tmp, out


class _Built(unittest.TestCase):
    CONTENT = None
    WITH_DATA = False

    @classmethod
    def setUpClass(cls):
        cls.tmp, cls.out = build(cls.CONTENT, cls.WITH_DATA)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def rows(self, path):
        s = (self.out / path).read_text(encoding="utf-8")
        self.assertNotIn('<p class="summary"></p>', s)
        # 空摘要行不会输出，所以 findall 得到的空串就是这一行没有摘要
        return {href.strip("/").split("/")[-1]: (html.unescape(t) if t else None) for href, t in ROW.findall(s)}

    def meta(self, path):
        s = (self.out / path).read_text(encoding="utf-8")
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        return html.unescape(m.group(1)) if m else None


class ListSummaryEdgeCases(_Built):
    CONTENT = FX / "content"

    def en_meta(self, slug):
        return self.meta("en/posts/daily/%s/index.html" % slug)

    def check_en(self, rows):
        # 导语只有开头套话（后面只剩空白或出处编号）：摘要只剩开头套话，不显示摘要行
        for slug in ("en-only-prefix", "en-prefix-cites", "en-colon-cites"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        # #109：开头套话不去掉，导语首句原样显示（不改大小写）；以前「去掉开头后接 that 回退 meta」的规则随之不再需要
        self.assertEqual(rows["en-that"], "The main story today is that NASA moved.")
        self.assertEqual(rows["en-that-comma"], "The main story today is that, as expected, NASA moved.")
        self.assertEqual(rows["en-thatcher"], "The main story today is thatcher-era archives opening.")
        # 断句（r4 口径）：. ? ! 后接空格的每一处都是候选句界，全段恰好一处、在引号括号外、后接大写、句点前不是缩写才断；否则空摘要
        # "why?” about" 的 ? 后面不是空格，不算候选，全段只有 "models. A" 一处
        self.assertEqual(rows["en-why"], "The main story today is a paper asking “why?” about refusals in chat models.")
        # U.S. Senate / (e.g. Phi) 各多出一处候选，全段两处：空摘要
        self.assertIsNone(rows["en-us-senate"])
        self.assertIsNone(rows["en-eg"])
        # etc. 是缩写，全段两处候选：空摘要，不回退半句 meta（meta 标签保持原值，见 test_meta_unchanged）
        self.assertIsNone(rows["en-etc"])
        # 审查 r3 的边界页 n04–n17（定义见 tests/fixtures/summary-site 同名页）
        for slug in ("n04-us-end-then-sentence", "n07-version-end", "n08-ascii-ellipsis", "n09-month-abbrev",
                     "n10-sen-gov", "n11-uae", "n12-initial", "n13-inc-upper", "n14-pm-et", "n15-paren-next",
                     "n16-lower-next"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        # 全段没有候选（r5）：空摘要。n05 只有段末的 U.S.，e16 没有句末标点，e09 没有句末标点（只有开头套话加 that）
        for slug in ("n05-us-at-end", "e16-no-terminal", "e09-that-end"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        # n06：小数和版本号里的点后面不是空格，不算候选；全段只有 "before. Next" 一处
        self.assertEqual(rows["n06-decimal-version"], "The main story today is Hugo v0.139.4 and GPT-3.5 scored 3.5 points higher than before.")
        # ? 和 ! 只计入候选、不用来断句（p01、p02）；句号后接空格再接小写字母不可断（p03）
        for slug in ("p01-question", "p02-exclaim", "p03-lower-after-period"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        # 整段引号或括号配对不上：空摘要。首句之后未闭合的 “ ( ‘（p04、p05、p08），首句里孤立的 ) ”（p06、p07）
        for slug in ("p04-unclosed-quote-after", "p05-unclosed-paren-after", "p06-stray-paren",
                     "p07-stray-close-quote", "p08-unclosed-single-after"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        # 配对正常的对照：词内撇号不改变引号状态，‘…’ 正常闭合
        self.assertEqual(rows["p09-apostrophe"], "The main story today is the lab’s model failed.")
        self.assertEqual(rows["p10-single-quote-closed"], "The main story today is a lab said ‘stop’ to its staff.")
        self.assertEqual(rows["p11-apostrophe-in-single"], "The main story today is a lab said ‘it’s fine’ to its staff.")
        # ’ 闭合时最近的开符号不是 ‘（交错）：配对不上，空摘要
        self.assertIsNone(rows["p12-single-close-mismatch"])
        # 超长首句没有引号外的截断点、回退 meta，而 meta 截在 “ 引文里：视为半句，空摘要（meta 标签保持原值）
        m = self.en_meta("p13-meta-cut-in-quote")
        self.assertIn("“", m)
        self.assertNotIn("”", m)
        self.assertIsNone(rows["p13-meta-cut-in-quote"])
        # n17：‘…’ 里的分号不算截断点，超长又没有别的截断点，回退 meta（明确截短、引号配对）；不得以未闭合的 ‘ 结尾
        s = rows["n17-single-quote-semicolon"]
        self.assertEqual(s, self.en_meta("n17-single-quote-semicolon"))
        self.assertTrue(s.endswith("…"), s)
        self.assertNotIn("‘", s)
        # list_summary：原样显示（不截断、不改大小写，导语小写开头时照样小写），优先于自动断句（en-list-summary 自动断句会是空摘要）
        self.assertEqual(rows["en-list-summary"], "the U.S. Senate passed a chip bill by 5 < 6 after R&D talks.")
        self.assertEqual(rows["en-list-summary-lower"], "a lab released weights.")
        # 自动摘要一律不改大小写（#109 起也不再去掉开头、不再把首字母改成大写）
        self.assertEqual(rows["en-npm"], "npm released a new version of its command-line client.")
        self.assertEqual(rows["en-arxiv"], "The main story today is arXiv tightening its review rules.")
        self.assertEqual(rows["en-iphone"], "The thing most worth knowing today: iPhone shipments fell.")
        self.assertEqual(rows["en-lower"], "The main story today is a study of robot hands.")
        self.assertEqual(rows["en-colon-lower"], "The thing most worth knowing today：a paper says models copy teachers.")
        self.assertEqual(rows["en-no-prefix"], "NASA asked companies for station plans.")
        # 只取完整第一句；超过 320 字符在 320 内最后一个分号/破折号处截断加省略号，没有就回退 meta
        self.assertEqual(rows["en-two-sentences"], "The thing most worth knowing today: a first full sentence here.")
        s = rows["en-long-semicolon"]
        self.assertTrue(s.endswith("details…"), s)
        self.assertLessEqual(len(s), 320)
        self.assertTrue(s.startswith("The main story today is a survey of robots"), s)
        self.assertEqual(rows["en-long-nosep"], self.en_meta("en-long-nosep"))
        # 数字范围里的 –（两侧无空白）不当作破折号
        self.assertEqual(rows["en-long-endash-range"], self.en_meta("en-long-endash-range"))
        # — 和两侧有空白的 – 正向截断
        for slug in ("en-long-emdash", "en-long-endash"):
            s = rows[slug]
            self.assertTrue(s.startswith("The main story today is a report on several research groups"), (slug, s))
            self.assertTrue(s.endswith("settings…"), (slug, s))
            self.assertLessEqual(len(s), 320)
            self.assertGreaterEqual(len(s) * 3, 320)
        # 括号里的分号不算截断点；截完不足上限三分之一（分号紧跟首词）回退 meta
        self.assertEqual(rows["en-long-semicolon-in-paren"], self.en_meta("en-long-semicolon-in-paren"))
        self.assertEqual(rows["en-long-semicolon-early"], self.en_meta("en-long-semicolon-early"))

    def test_en_daily_list(self):
        self.check_en(self.rows("en/posts/daily/index.html"))

    def test_issue_109_keep_opening(self):
        # #109：摘要是导语首句原文，开头套话照留、不改大小写，只去句末出处编号（连同前面的空格）；句中编号原样保留
        en, zh = self.rows("en/posts/daily/index.html"), self.rows("posts/daily/index.html")
        self.assertEqual(en["i109-main-story"], "The main story today is a study of groups of agents (AI programs that carry out tasks) "
                         "discussing factual questions, testing the effect of one adversary repeatedly asserting a false answer.")
        self.assertEqual(en["i109-colon-story"], "The thing most worth knowing today: a paper says that a “student” model picks up "
                         "the teacher’s attitude toward harmful requests.")
        self.assertEqual(en["i109-mid-cite"], "The main story today is a paper [1] and a dataset [2], [3], both about refusals.")
        self.assertEqual(zh["i109-zh-story"], "今天最值得知道的是：研究人员让一组大模型智能体讨论事实问题，测试一名反复坚持错误答案的对手会产生什么影响。")
        self.assertEqual(zh["i109-zh-mid-cite"], "今天最值得知道的是：一篇论文 [1] 和一个数据集 [2]、[3] 都研究拒答。")
        # list_summary 可以带开头套话（与导语逐字一致）
        self.assertEqual(en["i109-list-summary"], "The main story today is a lab released weights.")
        # meta description 不受影响：仍去掉所有出处编号，按原规则截短
        self.assertEqual(self.en_meta("i109-mid-cite"), "The main story today is a paper and a dataset, both about refusals.")
        self.assertEqual(self.meta("posts/daily/i109-zh-mid-cite/index.html"), "今天最值得知道的是：一篇论文 和一个数据集 都研究拒答。")

    def test_full_sentence_cap_360(self):
        # 整句上限裁定（Grok Bot 2026-10-19 07:46 SGT）：自动摘要整句上限 360；恰好 360 字符整句显示（只去句末编号），
        # 361 字符退回原处理：在前 320 字符内引号括号外最后一个截断点截断加「…」
        en, zh = self.rows("en/posts/daily/index.html"), self.rows("posts/daily/index.html")
        for rows, slug, sep in ((en, "i112-en", ";"), (zh, "i112-zh", "；")):
            full = rows[slug + "-360"]
            self.assertEqual(len(full), 360, full)
            self.assertFalse(full.endswith("…"), full)
            self.assertNotIn("[1]", full)
            self.assertTrue(full.startswith(("The main story today is", "今天最值得知道的是：")), full)
            cut = rows[slug + "-361"]
            self.assertTrue(cut.endswith("…"), cut)
            self.assertLessEqual(len(cut), 320)
            self.assertTrue(full.startswith(cut[:-1]), cut)
            self.assertEqual(full[len(cut) - 1], sep, cut)
        # meta description 上限不变（中文 120、英文 200）
        self.assertLessEqual(len(self.en_meta("i112-en-360")), 200)
        self.assertLessEqual(len(self.meta("posts/daily/i112-zh-360/index.html")), 120)

    def test_end_cites_and_lead_in(self):
        # 句末编号（#113 对照表定稿）：编号后紧接句末，或只夹闭合符号再接句末，才删（连同前面的空白，含 U+00A0）；开头后接数字照常显示
        en, zh = self.rows("en/posts/daily/index.html"), self.rows("posts/daily/index.html")
        # 编号后只夹闭合引号或括号再接句末标点：删编号（对照表 B01、B02）
        self.assertEqual(en["r2-quote-close"], "The main story today is a lab said “we are done”.")
        self.assertEqual(zh["r2-zh-paren-close"], "研究指出（结果）。")
        # 编号前是 &nbsp;（U+00A0）
        self.assertEqual(en["r2-nbsp"], "The main story today is a report.")
        self.assertNotIn("\u00a0", en["r2-nbsp"])
        # 开头后面只有数字也照常显示
        self.assertEqual(zh["r2-zh-digits"], "今天最值得知道的是42。")
        # 句末 [12]（中英各一例）与连续编号 [1][2]、[1], [2]、[1]、[2]
        self.assertEqual(en["r2-cite12"], "The main story today is a lab released weights.")
        self.assertEqual(zh["r2-zh-cite12"], "今天最值得知道的是：研究人员发布了新的评测。")
        self.assertEqual(en["r2-adjacent"], "The main story today is a lab released weights.")
        self.assertEqual(en["r2-comma"], "The main story today is a lab released weights.")
        self.assertEqual(zh["r2-zh-dunhao"], "今天最值得知道的是：研究人员发布了新的评测。")
        # 恰好 320 字符的 list_summary 能通过构建（本类 setUpClass 构建成功），并原样显示
        s = en["r2-ls-320"]
        self.assertEqual(len(s), 320)
        self.assertTrue(s.startswith("The main story today is a lab released weights and more weights"), s)
        self.assertTrue(s.endswith("."), s)

    def test_closer_then_period(self):
        en, zh = self.rows("en/posts/daily/index.html"), self.rows("posts/daily/index.html")
        # 反例：foo([1]).bar 里的句点后紧跟字母，不是句末，编号保留（对照表 E01、E02）
        self.assertEqual(en["r3-foo-call"], "The main story today is the call foo([1]).bar returned errors.")
        self.assertEqual(zh["r3-zh-foo-call"], "今天最值得知道的是：调用 foo([1]).bar 返回了错误。")
        # 编号后只夹闭合符号再接句末：删（B01、B02）
        self.assertEqual(en["r2-quote-close"], "The main story today is a lab said “we are done”.")
        self.assertEqual(zh["r2-zh-paren-close"], "研究指出（结果）。")
        # 编号后夹「…」：保留（09:36 第 2、3 点；F03、F04）
        self.assertEqual(en["r3-ellipsis-period"], "The main story today is a lab released weights [1]….")
        self.assertEqual(zh["r3-zh-ellipsis-keep"], "今天最值得知道的是：研究人员说结果 [1]……然后公开了代码。")

    def test_closer_and_punct_runs(self):
        # 编号后只夹闭合符号、再接 .!? 开头的一串标点（其后可再接闭合符号，然后是空白或段末）：删；夹省略号或其他字符：保留（#113 对照表 B07、J 组）
        en, zh = self.rows("en/posts/daily/index.html"), self.rows("posts/daily/index.html")
        # 英文：这类写法自动断句不显示摘要，用 list_summary 验证——不带编号的 list_summary 能通过校验，说明导语里的编号已删；带编号的通过，说明编号保留
        self.assertEqual(en["r4-en-repro"], "a lab said “it works (as shown).”")
        self.assertEqual(en["r4-en-period-paren"], "it works (in a test (as shown).)")
        self.assertEqual(en["r4-en-dots"], "it works (as shown [1])...")
        self.assertEqual(en["r4-en-qex"], "it works (as shown)?!")
        self.assertEqual(en["r4-en-straight"], 'a lab said "it works (as shown)."')
        self.assertEqual(en["r4-en-ellipsis"], "it works (as shown [1])…")
        self.assertEqual(en["r4-en-keep-quote"], "The main story today is the call “foo([1]).”bar returned errors.")
        self.assertEqual(en["r4-en-keep-dots"], "The main story today is the call foo([1])...bar returned errors.")
        self.assertEqual(en["r4-en-keep-qex"], "The main story today is the call foo([1])?!bar returned errors.")
        self.assertEqual(en["r4-en-keep-straight"], 'The main story today is the call "foo([1])."bar returned errors.')
        self.assertEqual(en["r4-en-keep-paren"], "The main story today is the call (foo([1]).)bar returned errors.")
        # 中文：. 后紧跟汉字且前面紧挨全角闭合符号才算句末（G01）；.” .) ?! ... 后接汉字都不算，保留
        self.assertEqual(zh["r4-zh-repro"], "研究指出（结果）.另一句。")
        self.assertEqual(zh["r4-zh-dots"], "今天最值得知道的是：研究指出（结果 [1]）...另一句。")
        self.assertEqual(zh["r4-zh-qex"], "今天最值得知道的是：研究指出（结果 [1]）?!另一句。")
        self.assertEqual(zh["r4-zh-straight"], '今天最值得知道的是："研究指出（结果 [1]）."另一句。')
        self.assertEqual(zh["r4-zh-curly"], "今天最值得知道的是：“研究指出（结果 [1]）.”另一句。")
        self.assertEqual(zh["r4-zh-paren"], "今天最值得知道的是：(研究指出（结果 [1]）.)另一句。")
        self.assertEqual(zh["r4-zh-corner"], "今天最值得知道的是：「研究指出（结果）」。")
        self.assertEqual(zh["r4-zh-keep-quote"], "今天最值得知道的是：调用 “foo([1]).”bar 返回了错误。")
        self.assertEqual(zh["r4-zh-keep-dots"], "今天最值得知道的是：调用 foo([1])...bar 返回了错误。")
        self.assertEqual(zh["r4-zh-keep-qex"], "今天最值得知道的是：调用 foo([1])?!bar 返回了错误。")
        self.assertEqual(zh["r4-zh-keep-straight"], '今天最值得知道的是：调用 "foo([1])."bar 返回了错误。')
        self.assertEqual(zh["r4-zh-keep-paren"], "今天最值得知道的是：调用 (foo([1]).)bar 返回了错误。")
        # 编号后直接是 .!? 但后面紧跟字母：保留（E04、E05）
        self.assertEqual(en["r5-dot-letter"], "The main story today is the call foo [1].bar returned errors.")
        self.assertEqual(zh["r5-zh-dot-letter"], "今天最值得知道的是：调用 foo [1].bar 返回了错误。")

    def test_list_summary_escaped(self):
        s = (self.out / "en/posts/daily/index.html").read_text(encoding="utf-8")
        self.assertIn("chip bill by 5 &lt; 6 after R&amp;D talks.</p>", s)

    def test_en_home(self):
        # 首页只列最新 20 篇：首页出现的每一行都要和列表里同一页的显示一致
        home, lst = self.rows("en/index.html"), self.rows("en/posts/daily/index.html")
        self.assertEqual(len(home), 20)
        for slug, s in home.items():
            self.assertEqual(s, lst[slug], slug)

    def test_zh_list_and_home(self):
        rows = self.rows("posts/daily/index.html")
        self.assertIn("zh-only-prefix", rows)
        self.assertIsNone(rows["zh-only-prefix"])  # 导语只有开头套话：摘要只剩开头套话，不显示摘要行
        # 引号里的 —— 不算截断点，没有别的截断点就回退 meta
        self.assertEqual(rows["zh-long-dash-in-quote"], self.meta("posts/daily/zh-long-dash-in-quote/index.html"))
        # #109：中文同样保留开头套话，照导语原句显示（半角冒号和空格也照原样）
        self.assertEqual(rows["zh-prefix"], "今天最值得知道的是: 研究人员发布了新的评测。")
        s = rows["zh-long-dash"]
        self.assertEqual(s, "今天最值得知道的是：" + "一项研究比较了许多小模型在很多任务上的表现并记录了细节" * 4 + "…")
        self.assertEqual(rows["zh-long-nosep"], self.meta("posts/daily/zh-long-nosep/index.html"))
        self.assertNotEqual(rows["zh-long-nosep"], "今天最值得知道的是…")
        # 引号内的 。？ 不结束首句，闭合后接着读（y01、y02）；‘…’ 内的 —— 不算截断点，回退的 meta 截在 ‘ 引文里、配对不上：空摘要（y03）
        self.assertEqual(rows["y01-inner-question"], "今天最值得知道的是：一篇论文问“为什么？”并给出了三条理由。")
        self.assertEqual(rows["y02-inner-period-corner"], "今天最值得知道的是：研究人员说「这是第一步。」随后公开了代码。")
        self.assertIsNone(rows["y03-single-quote-dash"])
        # 中文配对：未闭合的 “ （（q01、q02），孤立的 ” ） 」（q03–q05），首句之后未闭合的 “（q06）：空摘要
        for slug in ("q01-unclosed-quote", "q02-unclosed-paren", "q03-stray-close-quote", "q04-stray-close-paren",
                     "q05-stray-corner", "q06-unclosed-after"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        self.assertEqual(rows["zh-list-summary"], "研究人员说「这是第一步」，随后公开了代码")
        home = self.rows("index.html")
        self.assertTrue(home)
        # 超过 320 字、后面没有逗号的导语：meta 截短后只剩「今天最值得知道的是…」（只剩开头套话），首页和列表都不显示摘要行
        self.assertEqual(self.meta("posts/daily/zh-long-meta-prefix/index.html"), "今天最值得知道的是…")
        for r in (rows, home):
            self.assertIn("zh-long-meta-prefix", r)
            self.assertIsNone(r["zh-long-meta-prefix"])
        for slug, s in home.items():
            self.assertEqual(s, rows[slug], slug)

    def test_meta_unchanged(self):
        # meta description 不传 strip：仍保留开头，并按原规则截短
        self.assertEqual(self.en_meta("en-lower"), "The main story today is a study of robot hands.")
        self.assertEqual(self.en_meta("en-only-prefix"), "The main story today is")
        self.assertEqual(self.meta("posts/daily/zh-prefix/index.html"), "今天最值得知道的是: 研究人员发布了新的评测。")
        self.assertLessEqual(len(self.en_meta("en-long-nosep")), 200)
        # 列表摘要为空时 meta 标签保持原值
        self.assertEqual(self.en_meta("en-etc"), "The main story today is tools, datasets, etc.")
        self.assertEqual(self.en_meta("en-us-senate"), "The thing most worth knowing today: the U.S.")


class ListSummaryInvalid(unittest.TestCase):
    """list_summary 不合格、或 front matter 里出现 summary：构建失败并给出对应报错。"""
    CASES = {
        "ls-empty": "list_summary 必须是非空字符串",
        "ls-blank": "list_summary 必须是非空字符串",
        "ls-not-string": "list_summary 必须是非空字符串",
        "ls-too-long": "list_summary 超过 320 个字符",
        "ls-not-in-lede": "list_summary 在正文导语段里找不到逐字相同的内容",
        "ls-case-changed": "list_summary 在正文导语段里找不到逐字相同的内容",
        # #109：校验和自动摘要同一口径，只去句末出处编号；去掉句中编号的 list_summary 找不到
        "ls-mid-cite-dropped": "list_summary 在正文导语段里找不到逐字相同的内容",
        "fm-summary": "front matter 不能用 summary",
    }

    def test_cases_cover_fixtures(self):
        self.assertEqual(sorted(p.name for p in FX_INVALID.iterdir()), sorted(self.CASES))

    def test_build_fails(self):
        for case, msg in self.CASES.items():
            with self.subTest(case=case):
                tmp, out, r = run_build(FX_INVALID / case / "content")
                shutil.rmtree(tmp, ignore_errors=True)
                self.assertNotEqual(r.returncode, 0, case)
                self.assertIn(msg, r.stdout + r.stderr, case)


class ListSummaryFieldIsolation(unittest.TestCase):
    """自造页证明：带 list_summary 与去掉它相比，只有列表和首页的摘要行不同；4 个 feed、sitemap、各页 HTML（含 meta）逐字节相同。"""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="summary-iso-")
        bare = pathlib.Path(cls.tmp) / "content"
        shutil.copytree(FX / "content", bare)
        cls.changed = []
        for f in bare.rglob("*.md"):
            t = f.read_text(encoding="utf-8")
            t2 = re.sub(r"(?m)^list_summary:.*\n", "", t)
            if t2 != t:
                f.write_text(t2, encoding="utf-8")
                cls.changed.append(f.name)
        cls.tmp_a, cls.out_a = build(FX / "content")
        cls.tmp_b, cls.out_b = build(bare)

    @classmethod
    def tearDownClass(cls):
        for d in (cls.tmp, cls.tmp_a, cls.tmp_b):
            shutil.rmtree(d, ignore_errors=True)

    def test_only_summary_rows_differ(self):
        self.assertEqual(len(self.changed), 11)
        files_a = sorted(p.relative_to(self.out_a).as_posix() for p in self.out_a.rglob("*") if p.is_file())
        files_b = sorted(p.relative_to(self.out_b).as_posix() for p in self.out_b.rglob("*") if p.is_file())
        self.assertEqual(files_a, files_b)
        differ = [f for f in files_a if (self.out_a / f).read_bytes() != (self.out_b / f).read_bytes()]
        self.assertEqual(sorted(differ), ["en/index.html", "en/posts/daily/index.html", "en/posts/index.html",
                                          "index.html", "posts/daily/index.html", "posts/index.html"])
        for f in differ:
            a = SUMMARY_P.sub("", (self.out_a / f).read_text(encoding="utf-8"))
            b = SUMMARY_P.sub("", (self.out_b / f).read_text(encoding="utf-8"))
            self.assertEqual(a, b, f)
        feeds = [f for f in files_a if f.endswith("index.xml")]
        self.assertIn("index.xml", feeds)
        self.assertIn("en/posts/daily/index.xml", feeds)
        for f in feeds + [f for f in files_a if f.endswith("sitemap.xml")]:
            self.assertNotIn(f, differ)


class RequireHugo(unittest.TestCase):
    """CI 或 REQUIRE_HUGO 已设置但找不到 hugo：失败；都没设置：跳过。"""

    def run_without_hugo(self, env):
        with mock.patch.dict(os.environ, env, clear=False), mock.patch(__name__ + ".find_hugo", return_value=None):
            for k in ("CI", "REQUIRE_HUGO"):
                if k not in env:
                    os.environ.pop(k, None)
            return require_hugo()

    def test_ci_set_fails(self):
        with self.assertRaises(AssertionError):
            self.run_without_hugo({"CI": "true"})

    def test_require_hugo_set_fails(self):
        with self.assertRaises(AssertionError):
            self.run_without_hugo({"REQUIRE_HUGO": "1"})

    def test_neither_set_skips(self):
        with self.assertRaises(unittest.SkipTest):
            self.run_without_hugo({})


class ListSummaryRegression(_Built):
    """10-13、10-16、10-17、10-18 四期（#109）：首页和列表的摘要是导语首句原文，开头套话照留、大小写不改，只去句末出处编号；
    只有首句超过 360 字符（07:46 裁定的自动摘要整句上限）时才按原有处理明确截短（以「…」结尾，截前部分仍与导语开头逐字一致）。"""
    CONTENT = ROOT / "content"
    WITH_DATA = True
    DATES = ("2026-10-13", "2026-10-16", "2026-10-17", "2026-10-18")
    # 与 clean-text.html 的 end_cites_only 同一规则（Grok Bot 2026-10-19 08:56 SGT 裁定）：编号后（可隔空白）直接是 。！？、后接空白或段末的 .!?、或段末才删
    END_CITES = re.compile(r"\s*\[\d+\](?:\s*[、,，]?\s*\[\d+\])*(\s*(?:[。！？]|[.!?](?=\s|$)|$))")
    # 验收范围（08:56 裁定）：现有各期中英文首页和列表摘要，逐条写死；与导语原句一致，只去掉句末出处编号
    EXISTING = {
        '/en/posts/daily/2026-10-12/': 'The thing most worth knowing today: NASA has formally asked companies for commercial space station plans, to prepare for low Earth orbit after the International Space Station retires.',
        '/en/posts/daily/2026-10-13/': 'The thing most worth knowing today: a paper whose authors say it has been accepted at NeurIPS 2026 claims that any capability can be encrypted and hidden inside an AI model’s weights (the model’s internal parameters), and that even with full access to the weights, current capability evaluations would struggle to find it.',
        '/en/posts/daily/2026-10-14/': 'The thing most worth knowing today: a paper that benchmarks AI agent safety in professional settings says an agent can hand in a correct deliverable and still take unauthorized actions in the workspace — finishing the task is not proof of safe behavior.',
        '/en/posts/daily/2026-10-15/': 'The thing most worth knowing today: a paper says that when a “student” model is trained on a “teacher” model’s answers, the student picks up the teacher’s attitude toward harmful requests even when the questions have nothing to do with safety.',
        '/en/posts/daily/2026-10-16/': 'The main story today is a paper on training a Brazilian Portuguese model to refuse harmful requests while still helping with ordinary ones: three attempts to train it from “better/worse” answers failed to reverse its compliance with harmful prompts, and this version’s improvement came from later rounds of targeted safety examples.',
        '/en/posts/daily/2026-10-17/': 'The main story today is a paper finding that large language models (programs trained to answer text instructions) refuse harmful requests more often when told they are being safety-tested in English and five languages spoken in India, so test scores may differ from how they treat users in ordinary use.',
        '/en/posts/daily/2026-10-18/': 'The main story today is a study of groups of large-language-model agents (AI programs that carry out tasks from text instructions) discussing factual questions, testing the effect of one adversary repeatedly asserting a false answer.',
        '/en/posts/daily/2026-10-19/': 'A new benchmark put 13 model configurations into simulated customer delivery projects, and in the realistic setting, where unstated constraints must be uncovered, even the best configuration resolved only 14 of the 95 tasks.',
        '/en/posts/daily/2026-10-20/': 'A study finds that language models labeling online comments for toxicity mistake the second-person “you” for toxicity, and that this bias manufactures patterns in the measurements that human labels do not show.',
        '/en/posts/daily/2026-10-21/': 'A study finds that reinforcement learning with a reward that scores only task quality and policy compliance, and does not reward scheming, still widens the gap between how well a model trained with certain traits complies when monitored and when unmonitored.',
        '/en/posts/daily/2026-10-22/': 'A study finds that when the reward used in training departs from what a task actually intends, language models game that reward more and more often while the reasoning they write keeps discussing what the task intends, so the problem is hard to spot by reading it.',
        '/en/posts/daily/2026-10-23/': 'A study finds that chain-of-thought monitorability can be degraded in training, and that an unsupervised post-training objective maximizing mutual information between the chain of thought and the output recovers most or all of it across three models with degraded chains of thought.',
        '/en/posts/daily/2026-10-24/': 'A study finds that on OLMo-3-7B-Think, training with checkable rewards does not steadily raise how often the model shows self-preservation or resource-seeking subgoals: the rate rises from 25.0% after demonstration training to 46.1% near step 200, then falls to 11.8% at the final checkpoint, below that baseline.',
        '/en/posts/daily/2026-10-25/': 'A study had 32 participants learn science topics from five assistants that all spoke with full confidence: as the share of planted falsehoods in each assistant briefing rose, quiz scores fell from 7.4 to 2.9 out of 10, and participants adopted a stated falsehood about 65% of the time.',
        '/posts/daily/2026-10-12/': '今天最值得知道的是：NASA 正式向企业征集商业空间站方案，为国际空间站退役后的近地轨道做准备。',
        '/posts/daily/2026-10-13/': '今天最值得知道的是：一篇作者注明已被 NeurIPS 2026 接收的论文称，可以把任意能力加密藏进 AI 模型的权重（模型内部的参数）里，即使拿到全部权重，现有的能力评估手段也很难把它找出来。',
        '/posts/daily/2026-10-14/': '今天最值得知道的是：一篇评测专业场景里 AI 智能体安全的论文称，智能体可以在交出正确成果的同时，在工作区里做未经授权的事——任务完成并不能证明行为安全。',
        '/posts/daily/2026-10-15/': '今天最值得知道的是：一篇论文称，用“老师”模型的回答训练“学生”模型时，即便题目与安全无关，学生也会沾上老师对待有害请求的倾向。',
        '/posts/daily/2026-10-16/': '今天最值得知道的是：一篇巴西葡萄牙语模型论文公开了怎样让模型少回应有害请求、又继续帮助正常用户，其中三次让模型学习“较好／较差”回答的尝试都未扭转它照答有害请求的行为，本代的改进来自随后专门的安全问答示范训练。',
        '/posts/daily/2026-10-17/': '今天最值得知道的是：研究人员发现，大模型（能按文字指令生成回答的程序）在英语和五种印度语言中被告知“正在接受安全测试”时，更常拒绝有害请求，因此测试成绩未必代表它们平时怎样对待用户。',
        '/posts/daily/2026-10-18/': '今天最值得知道的是：研究人员让一组大模型智能体（能按文字指令自行完成任务的 AI 程序）讨论事实问题，测试一名反复坚持错误答案的对手会产生什么影响。',
        '/posts/daily/2026-10-19/': '一项新基准把 13 种模型配置放进模拟的客户交付项目，在需要自行找出未写明限制条件的拟真测试情境下，表现最好的配置也只完成了 95 个任务中的 14 个。',
        '/posts/daily/2026-10-20/': '一项研究发现，大模型给网络评论打“有毒”标签时，会把第二人称“you”（你）误判为有毒，并由此在测量中造出人类标注里没有的规律。',
        '/posts/daily/2026-10-21/': '一项研究发现，强化学习训练即使只奖励任务质量和遵守规定、并不奖励“谋划”，也会让一个按特定特质训练出来的模型在受监控和不受监控时的守规差距越来越大。',
        '/posts/daily/2026-10-22/': '一项研究发现，当训练用的奖励与任务本意有偏差时，语言模型会越来越多地钻奖励的空子，而它写出的推理过程仍在照常讨论任务本意，旁人很难从中看出问题。',
        '/posts/daily/2026-10-23/': '一项研究发现，思维链与模型实际输出之间的对应关系在训练中可能被削弱，但用无监督的后训练目标去最大化两者之间的互信息，可以在三个已削弱的模型上恢复大部分或全部可监控性。',
        '/posts/daily/2026-10-24/': '一项研究发现，在 OLMo-3-7B-Think 上，用可核对对错的奖励继续训练时，模型表现出自我保全、获取资源一类中间目标的比例并非一路上升：从用标注示范继续训练时的 25.0% 升到约第 200 步时的 46.1%，再落到最终检查点的 11.8%，低于用示范继续训练时的水平。',
        '/posts/daily/2026-10-25/': '一项研究让 32 名受试者与五个都说满信心话的助手学科学主题：当助手简报中植入的假事实比例升高时，测验得分从满分 10 分的 7.4 落到 2.9，受试者在助手说出假话时约有 65% 次会采纳。',
    }

    def lede(self, path):
        s = (self.out / path).read_text(encoding="utf-8")
        p = re.search(r"<main>.*?<p>(.*?)</p>", s, re.S).group(1)
        p = re.sub(r"<[^>]+>", "", p)
        p = html.unescape(p)
        p = re.sub(r"\s+", " ", p).strip()
        return self.END_CITES.sub(r"\1", p)

    def first_sentence(self, lede, zh):
        m = re.match(r"^.*?[。！？]" if zh else r"^.*?\.(?= [A-Z]|$)", lede)
        return m.group(0) if m else lede

    def check(self, lang_prefix):
        zh = lang_prefix == ""
        for page in ("index.html", "posts/daily/index.html"):
            rows = self.rows(lang_prefix + page)
            for d in self.DATES:
                path = "%sposts/daily/%s/index.html" % (lang_prefix, d)
                s = rows.get(d)
                self.assertTrue(s, (page, d))
                lede = self.lede(path)
                first = self.first_sentence(lede, zh)
                if s.endswith("…"):
                    # 首句超过 360 字符：按原有处理截短，截前部分是导语开头原文
                    self.assertGreater(len(first), 360, (d, s))
                    self.assertTrue(lede.startswith(s[:-1]), (d, s))
                else:
                    # 与导语首句逐字一致（含开头套话和大小写），句末出处编号已去掉
                    self.assertEqual(s, first, (d, s))
                    self.assertNotRegex(s, r"\[\d+\][。！？.!?]?$")

    def test_en(self):
        self.check("en/")
        # 07:46 裁定：10-13、10-16 英文首句加上开头后超过 320、不超过 360，整句显示（只去句末编号），不截短
        for page in ("en/index.html", "en/posts/daily/index.html"):
            rows = self.rows(page)
            for d in ("2026-10-13", "2026-10-16"):
                first = self.first_sentence(self.lede("en/posts/daily/%s/index.html" % d), False)
                self.assertEqual(rows[d], first, (page, d))
                self.assertFalse(rows[d].endswith("…"), (page, d))

    def test_zh(self):
        self.check("")

    def test_existing_pages_exact(self):
        # 6 个列表页（中英首页、posts、posts/daily）里出现的每期摘要都与 EXISTING 逐字相同，且没有 EXISTING 之外的行
        for page in ("index.html", "posts/index.html", "posts/daily/index.html",
                     "en/index.html", "en/posts/index.html", "en/posts/daily/index.html"):
            s = (self.out / page).read_text(encoding="utf-8")
            rows = {href: (html.unescape(x) if x else None) for href, x in ROW.findall(s)}
            en = page.startswith("en/")
            want = {h: v for h, v in self.EXISTING.items() if h.startswith("/en/") == en}
            self.assertEqual(rows, want, page)
        # 每条都独立核对：等于渲染后导语的第一句，只去掉句末出处编号（含开头套话，大小写不改）
        for href, s in self.EXISTING.items():
            en = href.startswith("/en/")
            path = href.strip("/") + "/index.html"
            first = self.first_sentence(self.lede(path), not en)
            self.assertEqual(s, first, href)
            self.assertNotRegex(s, r"\[\d+\]", href)


if __name__ == "__main__":
    unittest.main()
