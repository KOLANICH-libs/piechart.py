#!/usr/bin/env python3
import typing
import sys
import unittest
from collections import OrderedDict
from pathlib import Path

dict = OrderedDict

thisDir = Path(__file__).parent
sys.path.insert(0, str(thisDir.parent))
from piechart import piechart

testImagesDir = thisDir / "images"


class Tests(unittest.TestCase):
	maxDiff = None

	def test_simple(self) -> None:
		count = 10
		for i in range(1, count):
			share = i / count
			with self.subTest(share=share):
				self.assertEqual(piechart((share, 0.1)).strip(), (testImagesDir / ("0." + str(i) + ".svg")).read_text().strip())


if __name__ == "__main__":
	unittest.main()
