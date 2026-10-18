"""构建级用例：首页和列表摘要行（layouts/partials/page-description.html 的 strip 参数；导语固定开头清单在
hugo.toml 的 [params] summary_strip_prefixes）。用仓库的 hugo.toml、layouts/、i18n/ 在临时目录里构建：
- 边界用例站点：内容取 tests/fixtures/summary-site/content，不往线上 content 加页面；
- 回归用例：用仓库 content/ 构建，检查 10-16、10-17、10-18 三期；
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
PREFIXES = ("今天最值得知道的是", "the thing most worth knowing today", "the main story today is")


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


def run_build(content_dir, with_data=False):
    """在临时目录构建；返回 (tmp, out, CompletedProcess)。with_data 为 true 时连同仓库 data/ 一起拷（只给用仓库 content/ 的构建用）。"""
    hugo = require_hugo()
    tmp = tempfile.mkdtemp(prefix="summary-site-")
    site = pathlib.Path(tmp) / "site"
    site.mkdir()
    shutil.copy(ROOT / "hugo.toml", site / "hugo.toml")
    for d in ("layouts", "i18n") + (("data",) if with_data and (ROOT / "data").is_dir() else ()):
        shutil.copytree(ROOT / d, site / d)
    shutil.copytree(content_dir, site / "content")
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
        # 去掉开头后为空、只剩空白或出处编号：回退 meta；这几页的 meta 本身就只是那句开头，去掉开头什么都不剩，所以不显示摘要行
        for slug in ("en-only-prefix", "en-prefix-cites", "en-colon-cites"):
            self.assertIn(slug, rows)
            self.assertIsNone(rows[slug], slug)
        # 不带冒号的开头后接 that（含 "that,"）的半句：回退 meta；thatcher 不算 that
        self.assertEqual(rows["en-that"], self.en_meta("en-that"))
        self.assertEqual(rows["en-that"], "The main story today is that NASA moved.")
        self.assertEqual(rows["en-that-comma"], self.en_meta("en-that-comma"))
        self.assertEqual(rows["en-that-comma"], "The main story today is that, as expected, NASA moved.")
        self.assertEqual(rows["en-thatcher"], "Thatcher-era archives opening.")
        # 断句（r4 口径）：. ? ! 后接空格的每一处都是候选句界，全段恰好一处、在引号括号外、后接大写、句点前不是缩写才断；否则空摘要
        # "why?” about" 的 ? 后面不是空格，不算候选，全段只有 "models. A" 一处
        self.assertEqual(rows["en-why"], "A paper asking “why?” about refusals in chat models.")
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
        # 唯一的候选不满足 a)/b) 或全段没有候选：n05 没有候选（U.S. 在段末），整段即第一句；n06 小数和版本号里的点后面不是空格
        self.assertEqual(rows["n05-us-at-end"], "A new chip rule was issued by the U.S.")
        self.assertEqual(rows["n06-decimal-version"], "Hugo v0.139.4 and GPT-3.5 scored 3.5 points higher than before.")
        # n17：‘…’ 里的分号不算截断点，超长又没有别的截断点，回退 meta（明确截短、引号配对）；不得以未闭合的 ‘ 结尾
        s = rows["n17-single-quote-semicolon"]
        self.assertEqual(s, self.en_meta("n17-single-quote-semicolon"))
        self.assertTrue(s.endswith("…"), s)
        self.assertNotIn("‘", s)
        # list_summary：原样显示（不截断、不改大小写，导语小写开头时照样小写），优先于自动断句（en-list-summary 自动断句会是空摘要）
        self.assertEqual(rows["en-list-summary"], "the U.S. Senate passed a chip bill by 5 < 6 after R&D talks.")
        self.assertEqual(rows["en-list-summary-lower"], "a lab released weights.")
        # 没有去掉开头的不改大小写
        self.assertEqual(rows["en-npm"], "npm released a new version of its command-line client.")
        # 第 3 条：首词是大小写混合的词（arXiv、iPhone）不改；普通小写首词大写
        self.assertEqual(rows["en-arxiv"], "arXiv tightening its review rules.")
        self.assertEqual(rows["en-iphone"], "iPhone shipments fell.")
        self.assertEqual(rows["en-lower"], "A study of robot hands.")
        self.assertEqual(rows["en-colon-lower"], "A paper says models copy teachers.")
        self.assertEqual(rows["en-no-prefix"], "NASA asked companies for station plans.")
        # 第 4 条：只取完整第一句；超过 320 字符在 320 内最后一个分号/破折号处截断加省略号，没有就回退 meta
        self.assertEqual(rows["en-two-sentences"], "A first full sentence here.")
        s = rows["en-long-semicolon"]
        self.assertTrue(s.endswith("details…"), s)
        self.assertLessEqual(len(s), 320)
        self.assertTrue(s.startswith("A survey of robots"))
        self.assertEqual(rows["en-long-nosep"], self.en_meta("en-long-nosep"))
        # 数字范围里的 –（两侧无空白）不当作破折号
        self.assertEqual(rows["en-long-endash-range"], self.en_meta("en-long-endash-range"))
        # — 和两侧有空白的 – 正向截断
        for slug in ("en-long-emdash", "en-long-endash"):
            s = rows[slug]
            self.assertTrue(s.startswith("A report on several research groups"), (slug, s))
            self.assertTrue(s.endswith("settings…"), (slug, s))
            self.assertLessEqual(len(s), 320)
            self.assertGreaterEqual(len(s) * 3, 320)
        # 括号里的分号不算截断点；截完不足上限三分之一（分号紧跟首词）回退 meta
        self.assertEqual(rows["en-long-semicolon-in-paren"], self.en_meta("en-long-semicolon-in-paren"))
        self.assertEqual(rows["en-long-semicolon-early"], self.en_meta("en-long-semicolon-early"))

    def test_en_daily_list(self):
        self.check_en(self.rows("en/posts/daily/index.html"))

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
        self.assertIsNone(rows["zh-only-prefix"])  # meta 只是开头，去掉后不剩，不显示摘要行
        # 引号里的 —— 不算截断点，没有别的截断点就回退 meta
        self.assertEqual(rows["zh-long-dash-in-quote"], self.meta("posts/daily/zh-long-dash-in-quote/index.html"))
        self.assertEqual(rows["zh-prefix"], "研究人员发布了新的评测。")
        s = rows["zh-long-dash"]
        self.assertEqual(s, "一项研究比较了许多小模型在很多任务上的表现并记录了细节" * 4 + "…")
        self.assertEqual(rows["zh-long-nosep"], self.meta("posts/daily/zh-long-nosep/index.html"))
        self.assertNotEqual(rows["zh-long-nosep"], "今天最值得知道的是…")
        # 引号内的 。？ 不结束首句，闭合后接着读（y01、y02）；‘…’ 内的 —— 不算截断点，回退的 meta 截在 ‘ 引文里、配对不上：空摘要（y03）
        self.assertEqual(rows["y01-inner-question"], "一篇论文问“为什么？”并给出了三条理由。")
        self.assertEqual(rows["y02-inner-period-corner"], "研究人员说「这是第一步。」随后公开了代码。")
        self.assertIsNone(rows["y03-single-quote-dash"])
        self.assertEqual(rows["zh-list-summary"], "研究人员说「这是第一步」，随后公开了代码")
        home = self.rows("index.html")
        self.assertTrue(home)
        # 超过 320 字、后面没有逗号的导语：meta 截短后只剩「今天最值得知道的是…」，首页和列表都不显示摘要行
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
        self.assertEqual(len(self.changed), 3)
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
    """10-16、10-17、10-18 三期：列表里显示的是完整句子，或者是该页的 meta。"""
    CONTENT = ROOT / "content"
    WITH_DATA = True
    DATES = ("2026-10-16", "2026-10-17", "2026-10-18")

    def lede(self, path):
        s = (self.out / path).read_text(encoding="utf-8")
        p = re.search(r"<main>.*?<p>(.*?)</p>", s, re.S).group(1)
        p = re.sub(r"<[^>]+>", "", p)
        p = html.unescape(p)
        p = re.sub(r"\s*\[\d+\](\s*[、,，]?\s*\[\d+\])*", "", p)
        return re.sub(r"\s+", " ", p).strip()

    def check(self, lang_prefix):
        for page in ("index.html", "posts/daily/index.html"):
            rows = self.rows(lang_prefix + page)
            for d in self.DATES:
                path = "%sposts/daily/%s/index.html" % (lang_prefix, d)
                s = rows.get(d)
                self.assertTrue(s, (page, d))
                if s == self.meta(path):
                    continue
                self.assertFalse(s.lower().startswith(PREFIXES), (d, s))
                self.assertRegex(s, r"[。！？.!?][”’」』）)\"']*$|…$", (d, s))
                body = s[:-1] if s.endswith("…") else s
                lede = self.lede(path)
                # 摘要是导语的原文（去开头、首字母大写之外不改字），且是导语开头的那一句
                self.assertIn(body[1:], lede, (d, s))
                self.assertLess(lede.index(body[1:]), 40, (d, s))
                if not s.endswith("…"):
                    rest = lede[lede.index(body[1:]) + len(body) - 1:]
                    self.assertTrue(rest == "" or rest.startswith(" ") or lang_prefix == "", (d, rest[:20]))

    def test_en(self):
        self.check("en/")

    def test_zh(self):
        self.check("")


if __name__ == "__main__":
    unittest.main()
