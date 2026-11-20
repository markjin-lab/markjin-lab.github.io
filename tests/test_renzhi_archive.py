"""The archive follows the published date pointer in both languages."""
import json
import re
import shutil
import unittest
from pathlib import Path


from test_list_summary import FX, run_build


class RenzhiArchiveTests(unittest.TestCase):
    def build(self, latest):
        def prepare(site):
            root = Path(__file__).resolve().parents[1]
            for content in (root / "content").glob("renzhi-archive*.md"):
                shutil.copy(content, site / "content")
            data = site / "data" / "renzhi"
            data.mkdir(parents=True)
            (data / "latest.json").write_text(json.dumps({"date": latest}))

            release = (
                "https://github.com/markjin-lab/markjin-lab.github.io/releases/download/"
            )
            for stamp, asset in (
                ("20261117", "renzhi-20261117/renzhi-20261117.mp4"),
                ("20261118", "renzhi-20261118-r3/renzhi-20261118-r3.mp4"),
                ("20261119", "renzhi-20261119/renzhi-20261119.mp4"),
                ("20261120", "renzhi-20261120/renzhi-20261120.mp4"),
                ("20261121", "renzhi-20261121/renzhi-20261121.mp4"),
                ("20261116", "untagged-draft/renzhi-20261116.mp4"),
                ("20261115", None),
                ("20260230", "renzhi-20260230/renzhi-20260230.mp4"),
                ("20261114-preview", "renzhi-20261114/renzhi-20261114.mp4"),
                ("20261113", "renzhi-20261114/renzhi-20261114.mp4"),
                ("20261111", "renzhi-20261111/renzhi-20261111.mp4"),
                ("20261112", "renzhi-20261112/renzhi-20261112.mp4"),
            ):
                folder = site / f"static/tests/video-delivery-{stamp}"
                folder.mkdir(parents=True)
                if stamp == "20261112":
                    (folder / "index.html").mkdir()
                elif asset:
                    attr = "data-src" if stamp == "20261111" else "src"
                    (folder / "index.html").write_text(
                        f'<video><source {attr}="{release}{asset}" type="video/mp4"></video>'
                    )

        tmp, out, result = run_build(FX / "content", hook=prepare)
        self.addCleanup(shutil.rmtree, tmp)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return out

    def assert_links(self, out, latest, expected):
        for prefix, label in (("", "往期视频"), ("en/", "Past videos")):
            with self.subTest(language=prefix):
                home = (out / f"{prefix}index.html").read_text()
                self.assertIn(f'href="/{prefix}renzhi/archive/">{label}</a>', home)
                current = latest.replace("-", "")
                self.assertIn(f'href="/tests/video-delivery-{current}/"', home)
                archive = (out / f"{prefix}renzhi/archive/index.html").read_text()
                dates = re.findall(r'href="/tests/video-delivery-(\d+)/"', archive)
                self.assertEqual(dates, expected)
                for date in dates:
                    self.assertTrue((out / f"tests/video-delivery-{date}/index.html").is_file())

    def test_public_history_in_descending_order(self):
        self.assert_links(
            self.build("2026-11-20"), "2026-11-20", ["20261119", "20261118", "20261117"]
        )

    def test_publishing_next_episode_moves_previous_latest_into_history(self):
        self.assert_links(
            self.build("2026-11-21"), "2026-11-21",
            ["20261120", "20261119", "20261118", "20261117"]
        )

    def test_bad_date_or_missing_latest_file_leaves_archive_empty(self):
        for latest in ("2026-02-30", "2026-11-22"):
            with self.subTest(latest=latest):
                out = self.build(latest)
                for prefix in ("", "en/"):
                    archive = (out / f"{prefix}renzhi/archive/index.html").read_text()
                    self.assertNotIn("/tests/video-delivery-", archive)
