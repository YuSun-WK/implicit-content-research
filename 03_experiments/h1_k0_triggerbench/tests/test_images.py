import csv
import hashlib
import os
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from scripts.image_utils import load_image
from scripts.make_contact_sheets import make_sheets

ROOT = Path(os.environ.get('H1_EXPERIMENT_ROOT', Path(__file__).resolve().parents[1]))
RUN = ROOT/'runs/h1_k0_recovery_20261107_034443'
IMAGE_ROOT = Path(os.environ.get('H1_IMAGE_ROOT', ROOT/'image_cache_h1_k0_recovery'))


class ImageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root/'test/images_test/example/1_safe.png'
        self.path.parent.mkdir(parents=True)
        Image.new('RGB', (3, 3), 'red').save(self.path)
        self.row = {'safe_hf_path': 'test/images_test/example/1_safe.png',
                    'safe_sha256': hashlib.sha256(self.path.read_bytes()).hexdigest()}

    def test_normal_resolution(self):
        self.assertEqual(load_image(self.row, 'safe', self.root).size, (3, 3))

    def test_missing(self):
        self.path.unlink()
        with self.assertRaises(FileNotFoundError):
            load_image(self.row, 'safe', self.root)

    def test_hash_mismatch(self):
        self.row['safe_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
            load_image(self.row, 'safe', self.root)

    def test_corrupt_image(self):
        self.path.write_bytes(b'not an image')
        self.row['safe_sha256'] = hashlib.sha256(self.path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'decode failed'):
            load_image(self.row, 'safe', self.root)

    @unittest.skipUnless(IMAGE_ROOT.is_dir(), "integration image cache unavailable")
    def test_recovery_36_pairs_and_72_images(self):
        with (RUN/'sample_manifest.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 36)
        self.assertEqual(len({r['pair_id'] for r in rows}), 36)
        for row in rows:
            for side in ('safe', 'unsafe'):
                self.assertGreater(load_image(row, side, IMAGE_ROOT).width, 0)

    @unittest.skipUnless(IMAGE_ROOT.is_dir(), "integration image cache unavailable")
    def test_contact_sheets(self):
        with tempfile.TemporaryDirectory() as out:
            self.assertEqual(make_sheets(RUN, IMAGE_ROOT, Path(out)), 9)
            self.assertEqual(len(list(Path(out).glob('*.jpg'))), 9)
