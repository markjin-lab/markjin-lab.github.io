"""构建级用例：#81 评论入口提示。用仓库 content/ 在临时目录构建（同 test_list_summary.build）：
- 每篇日报页（posts/daily/<日期>/，中英）恰有一个评论区锚点 id="comments"，评论区上方有小标题和邀请语，日期行后有指向 #comments 的短链接，
  文案（反转义后）与 i18n 逐字一致；
- 其他页面（首页、列表、关于页、404 等）没有锚点、没有指向 #comments 的链接，也不出现这些文案；
- posts 下不在日报目录里的单页（只在临时站点里另加，不进仓库 content/）：照旧有 giscus 评论框，但没有入口提示。"""
import html, re, shutil, unittest
from test_list_summary import ROOT, build, run_build

COPY = {
    "zh": ("纠错与补充", "纠错 / 补充",
           "发现事实错误、哪句没看懂，或有更好的一手来源，欢迎在下面留言，点个表情也行。留言和点表情都需要先用 GitHub 账号登录。"),
    "en": ("Corrections & additions", "Corrections / additions",
           "Spotted a factual error, a sentence that didn't make sense, or a better primary source? "
           "Leave a note below, or just react. Both comments and reactions need a GitHub sign-in."),
}
DAILY = re.compile(r"^(en/)?posts/daily/\d{4}-\d{2}-\d{2}/index\.html$")
LINK = re.compile(r'<p class="meta">\d{4}-\d{2}-\d{2} · <a href="#comments"[^>]*>([^<]*)</a></p>')
SECTION = re.compile(r'<section class="comments" id="comments"[^>]*>\s*<h2>([^<]*)</h2>\s*<p>([^<]*)</p>\s*<div id="giscus-mount"')


class CommentEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp, cls.out = build(ROOT / "content", with_data=True)
        cls.pages = {p.relative_to(cls.out).as_posix(): p.read_text(encoding="utf-8")
                     for p in cls.out.rglob("*") if p.is_file() and p.suffix in (".html", ".xml")}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_daily_pages_have_entry(self):
        daily = sorted(k for k in self.pages if DAILY.match(k))
        self.assertGreaterEqual(len(daily), 2)
        for k in daily:
            with self.subTest(page=k):
                s = self.pages[k]
                heading, jump, invite = COPY["en" if k.startswith("en/") else "zh"]
                self.assertEqual(s.count('id="comments"'), 1)
                self.assertEqual(s.count('href="#comments"'), 1)
                m = LINK.search(s)
                self.assertIsNotNone(m, "date-line link")
                self.assertEqual(html.unescape(m.group(1)), jump)
                m = SECTION.search(s)
                self.assertIsNotNone(m, "heading + invitation above giscus")
                self.assertEqual((html.unescape(m.group(1)), html.unescape(m.group(2))), (heading, invite))
                self.assertLess(s.index('href="#comments"'), s.index('id="comments"'))

    def test_other_pages_have_no_entry(self):
        others = sorted(k for k in self.pages if not DAILY.match(k))
        self.assertIn("about/index.html", others)
        self.assertIn("en/about/index.html", others)
        words = [w for c in COPY.values() for w in c]
        for k in others:
            with self.subTest(page=k):
                s = html.unescape(self.pages[k])
                self.assertNotIn("#comments", s)
                self.assertNotIn('id="comments"', s)
                for w in words:
                    self.assertNotIn(w, s)


NON_DAILY = {  # 临时站点里另加的 posts 下非日报单页：相对 content/ 的路径 → 产物路径
    "posts/note-x.md": "posts/note-x/index.html",
    "posts/note-x.en.md": "en/posts/note-x/index.html",
    "posts/series/part-1.md": "posts/series/part-1/index.html",
    "posts/series/part-1.en.md": "en/posts/series/part-1/index.html",
}


def add_non_daily_posts(site):
    for rel in NON_DAILY:
        f = site / "content" / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("---\ntitle: note %s\ndate: 2026-10-19\n---\n\nbody text.\n" % f.stem, encoding="utf-8")


class NoEntryOutsideDaily(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp, out, r = run_build(ROOT / "content", with_data=True, hook=add_non_daily_posts)
        if r.returncode != 0:
            shutil.rmtree(cls.tmp, ignore_errors=True)
            raise AssertionError("hugo build failed:\n" + r.stdout + r.stderr)
        cls.out = out

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def check_no_entry(self, rel):
        s = html.unescape((self.out / rel).read_text(encoding="utf-8"))
        self.assertNotIn("#comments", s)
        self.assertNotIn('id="comments"', s)
        for w in [w for c in COPY.values() for w in c]:
            self.assertNotIn(w, s)
        return s

    def test_about_pages(self):
        for rel in ("about/index.html", "en/about/index.html"):
            with self.subTest(page=rel):
                self.check_no_entry(rel)

    def test_posts_outside_daily_dir(self):
        for rel in NON_DAILY.values():
            with self.subTest(page=rel):
                s = self.check_no_entry(rel)
                self.assertIn('id="giscus-mount"', s)          # 评论框仍按 posts 栏目显示
                self.assertIn('<p class="meta">2026-10-19</p>', s)  # 日期行在，但没有短链接

    def test_daily_pages_still_have_entry(self):
        rel = "posts/daily/2026-10-19/index.html"
        self.assertIn('href="#comments"', (self.out / rel).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
