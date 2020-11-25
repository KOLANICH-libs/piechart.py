__all__ = ("piechart",)

# pylint:disable=too-many-function-args

import typing
import sys
import math
from codecs import encode

fc = math.pi * 2

VecT = typing.Tuple[float, float]
ColorTupleT = typing.Tuple[int, int, int]
ColorT = typing.Union[ColorTupleT, str]


def computeCoords(center: VecT, phase: float, r: float) -> VecT:
	return (center[0] + r * math.cos(phase), center[1] + r * math.sin(phase))


def dumpCoords(coord: VecT) -> str:
	return " ".join((num2str(coord[0]), num2str(coord[1])))


def Move(coord: VecT) -> str:
	return " ".join(("M", dumpCoords(coord)))


def Line(coord: VecT) -> str:
	return " ".join(("L", dumpCoords(coord)))


def arc(r: float, offset: int, angle: float, end: VecT) -> str:
	return " ".join(("A", dumpCoords((r, r)), num2str(offset), "0" if abs(angle) < 180 else "1", "1", dumpCoords(end)))


def makeSectorPath(center: VecT, r: float, percentage: float, offset: float = 0) -> str:
	startPhase = offset * fc
	endPhase = (offset + percentage) * fc
	start = computeCoords(center, startPhase, r)
	end = computeCoords(center, endPhase, r)
	commands = [Move(center), Line(start), arc(r, offset * 360, percentage * 360, end), "Z"]
	return "".join(commands)


def num2str(n: typing.Union[int, float]):
	if isinstance(n, float) and n.is_integer():
		return str(int(n))
	return str(n)


def color2hex(args):
	return "#" + str(encode(bytes(args), "hex"), encoding="ascii")


def rgb255(rgb10):
	return tuple(int(round(el * 255)) for el in rgb10)


def createColors(count: int):
	import colorsys  # pylint:disable=import-outside-toplevel

	res = [None] * count
	piece = 1 / count
	for i in range(count):
		res[i] = rgb255(colorsys.hsv_to_rgb(i * piece, 1, 1))

	return res


def piechart(shares: typing.Tuple[float] = (0.35,), colors=None, podColor: typing.Optional[str] = "transparent", placeText: typing.Optional[typing.Union[str, bool]] = None, size: float = 30) -> str:
	"""Creates a pie chart.
	`shares` is a tuple of shares.
	`colors` is a tuple of colors. `None` means autogeneration. A color is either a tuple of RGB, or a string suitable for CSS.
	`podColor` is the pie ***pod*** color.
	`placeText` a text to place into the middle of the pie. By default percentage, if 1 share is displayed. Set to `False` to disable.
	"""

	r = size / 2
	center = (r, r)

	if placeText is None:
		placeText = len(shares) == 1

	if placeText is True:
		if len(shares) > 1:
			raise ValueError("Text is only placed if only 1 value must be displayed")

		placeText = str(round(shares[0] * 100)) + "%"

	if colors is None:
		colors = createColors(len(shares))

	items = []

	offset = 0
	for share, color in zip(shares, colors):
		if isinstance(color, tuple):
			color = color2hex(color)

		items.append('<path d="' + makeSectorPath(center, r, share, offset) + '" fill="' + color + '"/>')
		offset += share

	if placeText:
		items += '<text x="' + num2str(center[0]) + '" y="' + num2str(center[0]) + '" text-anchor="middle" dominant-baseline="middle" font-size="' + num2str(size / 3) + 'px" font-family="monospace">' + placeText + "</text>"

	return r'<?xml version="1.0" encoding="utf-8"?><svg xmlns="http://www.w3.org/2000/svg" width="' + num2str(size) + '" height="' + num2str(size) + '"><circle cx="' + num2str(r) + '" cy="' + num2str(r) + '" r="' + num2str(r) + '" fill="' + podColor + '"/>' + "".join(items) + "</svg>"


if __name__ == "__main__":
	print(piechart(tuple((float(n) for n in sys.argv[1:]))), file=sys.stdout)
