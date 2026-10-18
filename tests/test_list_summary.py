"""构建级用例：首页和列表摘要行去掉导语固定开头（layouts/partials/page-description.html 的 strip 参数，
清单在 hugo.toml 的 [params] summary_strip_prefixes）。用仓库的 hugo.toml、layouts/、i18n/ 加 tests/fixtures/summary-site/content
在临时目录里构建一个测试站点，不往线上 content 加页面。找不到 hugo（环境变量 HUGO、PATH、~/.local/bin/hugo）时跳过。"""
import html, os, pathlib, re, shutil, subprocess, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
FX = ROOT / "tests" / "fixtures" / "summary-site"


def find_hugo():
    for c in (os.environ.get("HUGO"), shutil.which("hugo"), str(pathlib.Path.home() / ".local/bin/hugo")):
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


ROW = re.compile(r'<li><a href="([^"]+)">[^<]*</a>(?:\s*<span class="meta">[^<]*</span>)?(?:<p class="summary">(.*?)</p>)?</li>', re.S)


class ListSummaryBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hugo = find_hugo()
        if not hugo:
            raise unittest.SkipTest("hugo not found")
        cls.tmp = tempfile.mkdtemp(prefix="summary-site-")
        site = pathlib.Path(cls.tmp) / "site"
        site.mkdir()
        shutil.copy(ROOT / "hugo.toml", site / "hugo.toml")
        for d in ("layouts", "i18n"):
            shutil.copytree(ROOT / d, site / d)
        shutil.copytree(FX / "content", site / "content")
        cls.out = pathlib.Path(cls.tmp) / "public"
        r = subprocess.run([hugo, "--quiet", "-s", str(site), "-d", str(cls.out)], capture_output=True, text=True)
        if r.returncode != 0:
            raise AssertionError("hugo build failed:\n" + r.stdout + r.stderr)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def rows(self, path):
        s = (self.out / path).read_text(encoding="utf-8")
        self.assertNotIn('<p class="summary"></p>', s)  # 空摘要行不输出，所以下面 findall 的空串就是没有摘要行
        return {href.strip("/").split("/")[-1]: (html.unescape(t) if t else None) for href, t in ROW.findall(s)}

    def meta(self, path):
        s = (self.out / path).read_text(encoding="utf-8")
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        return html.unescape(m.group(1)) if m else None

    def check_en(self, rows):
        # 1) 去掉开头后什么也不剩，或只剩出处编号和空白：不输出摘要行
        self.assertIsNone(rows["en-only-prefix"])
        self.assertIsNone(rows["en-prefix-cites"])
        self.assertIsNone(rows["en-colon-cites"])
        # 2) 不带冒号的开头后接 that：保留原开头；thatcher 不算 that
        self.assertEqual(rows["en-that"], "The main story today is that NASA moved.")
        self.assertEqual(rows["en-thatcher"], "Thatcher-era archives opening.")
        # 3) 首词含大写（arXiv、iPhone）不大写；普通小写首词大写
        self.assertEqual(rows["en-arxiv"], "arXiv tightening its review rules.")
        self.assertEqual(rows["en-iphone"], "iPhone shipments fell.")
        self.assertEqual(rows["en-lower"], "A study of robot hands.")
        self.assertEqual(rows["en-colon-lower"], "A paper says models copy teachers.")
        # 没有清单里开头的原样显示
        self.assertEqual(rows["en-no-prefix"], "NASA asked companies for station plans.")

    def test_en_daily_list(self):
        self.check_en(self.rows("en/posts/daily/index.html"))

    def test_en_home(self):
        self.check_en(self.rows("en/index.html"))

    def test_zh_list(self):
        rows = self.rows("posts/daily/index.html")
        self.assertIsNone(rows["zh-only-prefix"])
        self.assertEqual(rows["zh-prefix"], "研究人员发布了新的评测。")
        self.assertEqual(self.rows("index.html"), rows)

    def test_meta_keeps_prefix(self):
        # meta description 不传 strip，仍保留开头
        self.assertEqual(self.meta("en/posts/daily/en-lower/index.html"), "The main story today is a study of robot hands.")
        self.assertEqual(self.meta("en/posts/daily/en-only-prefix/index.html"), "The main story today is")
        self.assertEqual(self.meta("posts/daily/zh-prefix/index.html"), "今天最值得知道的是: 研究人员发布了新的评测。")


if __name__ == "__main__":
    unittest.main()
