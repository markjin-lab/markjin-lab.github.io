"""构建级用例：首页和列表摘要行（layouts/partials/page-description.html 的 strip 参数；导语固定开头清单在
hugo.toml 的 [params] summary_strip_prefixes）。用仓库的 hugo.toml、layouts/、i18n/ 在临时目录里构建：
- 边界用例站点：内容取 tests/fixtures/summary-site/content，不往线上 content 加页面；
- 回归用例：用仓库 content/ 构建，检查 10-16、10-17、10-18 三期。
找不到 hugo（环境变量 HUGO、PATH、~/.local/bin/hugo）时：设了环境变量 CI 或 REQUIRE_HUGO（非空，且不是 0/false）就直接失败；都没设才跳过。"""
import html, os, pathlib, re, shutil, subprocess, tempfile, unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
FX = ROOT / "tests" / "fixtures" / "summary-site"
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


def build(content_dir):
    hugo = require_hugo()
    tmp = tempfile.mkdtemp(prefix="summary-site-")
    site = pathlib.Path(tmp) / "site"
    site.mkdir()
    shutil.copy(ROOT / "hugo.toml", site / "hugo.toml")
    for d in ("layouts", "i18n"):
        shutil.copytree(ROOT / d, site / d)
    shutil.copytree(content_dir, site / "content")
    out = pathlib.Path(tmp) / "public"
    r = subprocess.run([hugo, "--quiet", "-s", str(site), "-d", str(out)], capture_output=True, text=True)
    if r.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise AssertionError("hugo build failed:\n" + r.stdout + r.stderr)
    return tmp, out


class _Built(unittest.TestCase):
    CONTENT = None

    @classmethod
    def setUpClass(cls):
        cls.tmp, cls.out = build(cls.CONTENT)

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
        # 断句：句内的 "why?"、U.S.、(e.g. 不算句末；拿不准的缩写（etc. 后接大写）回退 meta
        self.assertEqual(rows["en-why"], "A paper asking “why?” about refusals in chat models.")
        self.assertEqual(rows["en-us-senate"], "The U.S. Senate passed a chip bill.")
        self.assertEqual(rows["en-eg"], "Small models (e.g. Phi) beat larger ones on math.")
        self.assertEqual(rows["en-etc"], self.en_meta("en-etc"))
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
        home = self.rows("index.html")
        self.assertTrue(home)
        for slug, s in home.items():
            self.assertEqual(s, rows[slug], slug)

    def test_meta_unchanged(self):
        # meta description 不传 strip：仍保留开头，并按原规则截短
        self.assertEqual(self.en_meta("en-lower"), "The main story today is a study of robot hands.")
        self.assertEqual(self.en_meta("en-only-prefix"), "The main story today is")
        self.assertEqual(self.meta("posts/daily/zh-prefix/index.html"), "今天最值得知道的是: 研究人员发布了新的评测。")
        self.assertLessEqual(len(self.en_meta("en-long-nosep")), 200)


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
