"""Checks the benchmark itself. Run with pytest, or as a script: python test_benchmark.py"""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import make_data
import with_recipe
from check import differences
from reference import answers

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "cards.csv"
SHA256 = "e4193f041c5880b5ef3197cf79175f6e57b8daad7c707c2a9e43e8c43b69d392"


class Benchmark(unittest.TestCase):
    def test_the_data_is_the_published_file(self):
        self.assertEqual(hashlib.sha256(DATA.read_bytes()).hexdigest(), SHA256)

    def test_the_generator_writes_it_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = make_data.write(Path(tmp) / "cards.csv")
            self.assertEqual(out.read_bytes(), DATA.read_bytes())
            other = make_data.write(Path(tmp) / "other.csv", seed=7)
            self.assertNotEqual(other.read_bytes(), DATA.read_bytes())

    def test_the_reference_gives_the_expected_answers(self):
        expected = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
        self.assertEqual(answers(DATA, "2026-10-31"), expected)
        self.assertEqual(sum(expected["by_validity"].values()), expected["cards_read"] - expected["excluded"])
        self.assertEqual(sum(expected["by_decision"].values()), sum(expected["by_level"].values()))

    def test_the_cutoff_changes_the_answers(self):
        self.assertNotEqual(answers(DATA, "2027-03-31"), answers(DATA, "2026-10-31"))

    def test_scoring_is_exact(self):
        expected = answers(DATA, "2026-10-31")
        self.assertEqual(differences(json.loads(json.dumps(expected)), expected), {})
        nearly = json.loads(json.dumps(expected))
        nearly["by_decision"]["renew"] += 1
        del nearly["letters"]
        nearly["extra"] = 1
        self.assertEqual(set(differences(nearly, expected)), {"by_decision.renew", "letters", "extra"})

    @unittest.skipUnless(shutil.which("recipe360"), "Recipe360 is not installed")
    def test_the_recipe_is_exact_and_always_the_same(self):
        self.assertEqual(with_recipe.main(["--runs", "3"]), 0)


if __name__ == "__main__":
    unittest.main()
