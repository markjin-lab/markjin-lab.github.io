"""构建级用例：#113 句末出处编号边界情形（对照表 docs/issue113-table.md 的 A–K、S 组，一行一条测试）。
内容取 tests/fixtures/citation-edge/content（每页正文第一段是对照表的「输入」），应得取 tests/fixtures/citation-edge/expected.json：
- row：首页和列表摘要行（posts/daily 列表页里该页的摘要，null 为不显示）；
- clean：layouts/partials/clean-text.html 以 end_cites_only 方式清洗导语段的结果（list_summary 校验用的也是它）。英文有一批写法首页不显示摘要，
  按 Grok Bot 2026-10-19 09:36 SGT 裁定第 8 点，以清洗结果和 list_summary 校验验收；清洗结果从临时站点里另加的一个调试页读出，调试页只写在临时目录里；
- meta：meta description，不在 #113 范围（07:46「meta 不动」），须与 main 相同。
list_summary 候选：每条单独建站，把候选写进该页 front matter，断言构建通过或被拦下。"""
import html, json, pathlib, re, shutil, unittest
from test_list_summary import ROOT, run_build

FX = ROOT / "tests" / "fixtures" / "citation-edge"
DATA = json.loads((FX / "expected.json").read_text(encoding="utf-8"))
DBG = ('{{ range where site.AllPages "Section" "posts" }}{{ if .IsPage }}<x id="{{ .Title }}">'
       '{{ with findRE `(?s)<p>.*?</p>` .Content 1 }}{{ partial "clean-text.html" (dict "text" (index . 0) "end_cites_only" true) }}{{ end }}</x>\n'
       '{{ end }}{{ end }}')


def add_debug_page(site):
    (site / "content" / "dbg").mkdir()
    (site / "content" / "dbg" / "_index.md").write_text("---\ntitle: dbg\n---\n", encoding="utf-8")
    (site / "layouts" / "dbg").mkdir()
    (site / "layouts" / "dbg" / "list.html").write_text(DBG, encoding="utf-8")


def page_file(row):
    return FX / "content" / "posts" / "daily" / ("%s%s.md" % (row["id"].lower(), ".en" if row["lang"] == "en" else ""))


class CitationEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp, cls.out, r = run_build(FX / "content", hook=add_debug_page)
        if r.returncode != 0:
            shutil.rmtree(cls.tmp, ignore_errors=True)
            raise AssertionError("hugo build failed:\n" + r.stdout + r.stderr)
        cls.rows = {}
        for lp in ("posts/daily/index.html", "en/posts/daily/index.html"):
            s = (cls.out / lp).read_text(encoding="utf-8")
            for li in re.findall(r"<li>.*?</li>", s, re.S):
                slug = re.search(r'href="([^"]+)"', li).group(1).strip("/").split("/")[-1]
                m = re.search(r'<p class="summary">(.*?)</p>', li, re.S)
                cls.rows[slug] = html.unescape(m.group(1)) if m else None
        dbg = (cls.out / "dbg" / "index.html").read_text(encoding="utf-8")
        cls.clean = {t.lower(): html.unescape(v) for t, v in re.findall(r'<x id="([^"]+)">(.*?)</x>', dbg, re.S)}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def meta(self, row):
        p = self.out / ("en/" if row["lang"] == "en" else "") / "posts" / "daily" / row["id"].lower() / "index.html"
        m = re.search(r'<meta name="description" content="([^"]*)"', p.read_text(encoding="utf-8"))
        return html.unescape(m.group(1)) if m else None

    def check(self, row):
        slug = row["id"].lower()
        self.assertIn(slug, self.rows)
        self.assertEqual(self.rows[slug], row["row"], "摘要行")
        self.assertEqual(self.clean[slug], row["clean"], "清洗结果")
        self.assertEqual(self.meta(row), row["meta"], "meta description（范围外，不得变化）")

    def test_every_fixture_has_a_row(self):
        files = {p.name for p in (FX / "content" / "posts" / "daily").glob("*.md") if not p.name.startswith("_")}
        self.assertEqual(files, {page_file(r).name for r in DATA["rows"]})


def _row_test(row):
    def t(self):
        self.check(row)
    t.__doc__ = "对照表 %s" % row["id"]
    return t


for _r in DATA["rows"]:
    setattr(CitationEdgeCases, "test_%s" % _r["id"], _row_test(_r))


class CitationEdgeListSummary(unittest.TestCase):
    """list_summary 候选：首页不显示摘要的英文写法按 09:36 第 8 点用 list_summary 校验验收。"""

    def build_with(self, cid, ls):
        row = next(r for r in DATA["rows"] if r["id"] == cid)
        src = page_file(row).read_text(encoding="utf-8")
        head, body = src.split("\n---\n", 1)
        page = "%s\nlist_summary: %s\n---\n%s" % (head, json.dumps(ls, ensure_ascii=False), body)

        def hook(site):
            d = site / "content" / "posts" / "daily"
            for p in d.glob("*.md"):
                if not p.name.startswith("_"):
                    p.unlink()
            (d / page_file(row).name).write_text(page, encoding="utf-8")
        tmp, out, r = run_build(FX / "content", hook=hook)
        shutil.rmtree(tmp, ignore_errors=True)
        return r


def _ls_test(item):
    def t(self):
        r = self.build_with(item["id"], item["list_summary"])
        if item["pass"]:
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        else:
            self.assertNotEqual(r.returncode, 0, "应被拦下：%s" % item["list_summary"])
            self.assertIn("list_summary 在正文导语段里找不到逐字相同的内容", r.stdout + r.stderr)
    t.__doc__ = "对照表 %s 的 list_summary 候选" % item["id"]
    return t


for _i in DATA["list_summary"]:
    setattr(CitationEdgeListSummary, "test_ls_%s" % _i["id"], _ls_test(_i))


if __name__ == "__main__":
    unittest.main()
