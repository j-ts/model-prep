import base64
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zlib


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "review_svg.py"
SVG = "{http://www.w3.org/2000/svg}"
INK = "{http://www.inkscape.org/namespaces/inkscape}"
SODI = "{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}"
LAYERS = (
    "original-reference",
    "working-outlines",
    "flat-colour-regions",
    "user-corrected-regions",
    "review-annotations",
)


def png(width=3, height=2):
    def chunk(kind, data):
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data))
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress((b"\0" + b"\xff\0\0" * width) * height))
        + chunk(b"IEND", b"")
    )


class ReviewSVGTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.image = self.directory / "reference.png"
        self.image.write_bytes(png())
        self.source = self.directory / "review.svg"
        self.overlay = self.directory / "overlay.svg"
        self.flat = self.directory / "flat.svg"

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True,
            text=True,
        )

    def init(self):
        result = self.run_cli(
            "init",
            "--image",
            self.image,
            "--output",
            self.source,
            "--palette",
            "#000000",
            "#ffffff",
            "#ff0000",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return ET.parse(self.source).getroot()

    def views(self):
        return self.run_cli(
            "views", self.source, "--overlay", self.overlay, "--flat", self.flat
        )

    def test_init_embeds_exact_raster_dimensions_palette_and_provenance(self):
        root = self.init()
        self.assertEqual(root.get("viewBox"), "0 0 3 2")
        layers = {node.get("id"): node for node in root.findall(SVG + "g")}
        self.assertEqual(set(layers), set(LAYERS))
        for node in layers.values():
            self.assertEqual(node.get(INK + "groupmode"), "layer")
        original = layers["original-reference"]
        self.assertEqual(original.get(SODI + "insensitive"), "true")
        raster = original.find(SVG + "image")
        self.assertEqual((raster.get("width"), raster.get("height")), ("3", "2"))
        self.assertEqual(base64.b64decode(raster.get("href").split(",", 1)[1]), png())
        metadata = root.find(SVG + "metadata")
        self.assertEqual(
            metadata.get("data-source-sha256"), hashlib.sha256(png()).hexdigest()
        )
        self.assertEqual(metadata.get("data-palette"), "#000000 #ffffff #ff0000")
        self.assertIn("PREVIEW ONLY", "".join(root.itertext()))
        self.assertEqual(root.findall(".//" + SVG + "path"), [])

    def test_views_preserve_paths_transforms_and_source_while_changing_visibility(self):
        root = self.init()
        for index, layer in enumerate(root.findall(SVG + "g")):
            if layer.get("id") != "original-reference":
                layer.set("transform", "translate(0.25,-2) scale(1.1)")
                layer.set("style", "opacity:0.8; display:none")
                group = ET.SubElement(layer, SVG + "g", {"transform": "rotate(-4 2 3)"})
                ET.SubElement(
                    group,
                    SVG + "path",
                    {
                        "id": "edited-" + str(index),
                        "d": "M 0.10,2 L3 4 Q 5,6 7,8",
                        "transform": "matrix(1,0,0,1,0.15,-0.5)",
                        "fill": "#ff0000",
                    },
                )
        ET.ElementTree(root).write(self.source, encoding="utf-8", xml_declaration=True)
        before = self.source.read_bytes()
        expected_paths = [node.attrib for node in root.findall(".//" + SVG + "path")]
        expected_geometry = [
            (node.get("id"), node.get("d"), node.get("transform"))
            for node in root.findall(".//" + SVG + "path")
        ]
        expected_transforms = [
            node.get("transform") for node in root.iter() if "transform" in node.attrib
        ]
        result = self.views()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.source.read_bytes(), before)
        for filename, visible in (
            (self.overlay, set(LAYERS)),
            (self.flat, {"flat-colour-regions", "user-corrected-regions"}),
        ):
            view = ET.parse(filename).getroot()
            self.assertEqual(
                [
                    (node.get("id"), node.get("d"), node.get("transform"))
                    for node in view.findall(".//" + SVG + "path")
                ],
                expected_geometry,
            )
            if filename == self.flat:
                self.assertEqual(
                    [node.attrib for node in view.findall(".//" + SVG + "path")],
                    expected_paths,
                )
            self.assertEqual(
                [
                    node.get("transform")
                    for node in view.iter()
                    if "transform" in node.attrib
                ],
                expected_transforms,
            )
            for layer in view.findall(SVG + "g"):
                display = "inline" if layer.get("id") in visible else "none"
                self.assertIn("display:" + display, layer.get("style"))
                if layer.get("id") != "original-reference":
                    self.assertIn("opacity:0.8", layer.get("style"))
            self.assertEqual(view.get("data-status"), "PREVIEW ONLY")
            self.assertEqual(
                view.get("data-review-sha256"), hashlib.sha256(before).hexdigest()
            )

    def test_overlay_shows_accepted_regions_as_stroke_only_without_changing_flat(self):
        root = self.init()
        expected = {}
        for layer_id in ("flat-colour-regions", "user-corrected-regions"):
            layer = root.find(SVG + f"g[@id='{layer_id}']")
            path = ET.SubElement(
                layer,
                SVG + "path",
                {
                    "id": layer_id + "-accepted",
                    "d": "M 0,0 L 3,0 3,2 0,2 Z",
                    "transform": "translate(0.25,0) scale(0.9)",
                    "fill": "#ff0000",
                    "style": "fill:#ff0000 !important;stroke:none;stroke-width:8;opacity:0.9",
                },
            )
            expected[path.get("id")] = dict(path.attrib)
        ET.ElementTree(root).write(self.source, encoding="utf-8", xml_declaration=True)
        before = self.source.read_bytes()
        result = self.views()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.source.read_bytes(), before)
        overlay = ET.parse(self.overlay).getroot()
        flat = ET.parse(self.flat).getroot()
        for layer_id in ("flat-colour-regions", "user-corrected-regions"):
            layer = overlay.find(SVG + f"g[@id='{layer_id}']")
            self.assertEqual(layer.get("display"), "inline")
            path = layer.find(SVG + "path")
            style = dict(
                part.strip().split(":", 1) for part in path.get("style").split(";")
            )
            self.assertEqual(style["fill"], "none !important")
            self.assertEqual(style["stroke"], "#00ffff !important")
            self.assertEqual(style["stroke-width"], "1 !important")
            self.assertEqual(style["opacity"], "0.9")
            for attribute in ("d", "transform"):
                self.assertEqual(
                    path.get(attribute), expected[path.get("id")][attribute]
                )
            flat_path = flat.find(".//" + SVG + f"path[@id='{path.get('id')}']")
            self.assertEqual(flat_path.attrib, expected[path.get("id")])

    def test_no_output_can_overwrite_any_existing_file(self):
        self.init()
        original = self.source.read_bytes()
        result = self.run_cli(
            "init",
            "--image",
            self.image,
            "--output",
            self.source,
            "--palette",
            "#000000",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.source.read_bytes(), original)
        self.flat.write_text("keep me", encoding="utf-8")
        result = self.views()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.overlay.exists())
        self.assertEqual(self.flat.read_text(encoding="utf-8"), "keep me")
        result = self.run_cli(
            "views",
            self.source,
            "--overlay",
            self.source,
            "--flat",
            self.directory / "unused.svg",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.source.read_bytes(), original)

    def test_views_require_distinct_output_paths(self):
        self.init()
        result = self.run_cli(
            "views", self.source, "--overlay", self.flat, "--flat", self.flat
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.flat.exists())

    def test_failed_second_output_reservation_leaves_no_partial_preview(self):
        self.init()
        result = self.run_cli(
            "views",
            self.source,
            "--overlay",
            self.overlay,
            "--flat",
            self.directory / "absent" / "flat.svg",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.overlay.exists())

    def test_missing_layer_is_clear_and_writes_nothing(self):
        root = self.init()
        root.remove(root.find(SVG + "g[@id='user-corrected-regions']"))
        ET.ElementTree(root).write(self.source)
        result = self.views()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("user-corrected-regions", result.stderr)
        self.assertFalse(self.overlay.exists())
        self.assertFalse(self.flat.exists())

    def test_unsafe_xml_and_external_resources_are_rejected(self):
        self.init()
        original = self.source.read_text(encoding="utf-8")
        injections = [
            '<!DOCTYPE svg [<!ENTITY danger "x">]>',
            "<script>alert(1)</script>",
            "<foreignObject><div /></foreignObject>",
            '<image href="https://example.com/image.png" />',
            '<image href="file:///private/reference.png" />',
            '<path onclick="alert(1)" d="M0 0" />',
            "<style>path {fill: url(https://example.com/style)}</style>",
            '<path style="fill: url(https://example.com/style)" d="M0 0" />',
        ]
        for injection in injections:
            with self.subTest(injection=injection):
                if injection.startswith("<!DOCTYPE"):
                    modified = injection + original[original.index("<svg") :]
                else:
                    modified = original.replace("</svg>", injection + "</svg>")
                self.source.write_text(modified, encoding="utf-8")
                result = self.views()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.overlay.exists())
                self.assertFalse(self.flat.exists())

    def test_raster_in_print_regions_is_rejected(self):
        root = self.init()
        flat = root.find(SVG + "g[@id='flat-colour-regions']")
        ET.SubElement(
            flat,
            SVG + "image",
            {"href": "data:image/png;base64," + base64.b64encode(png()).decode()},
        )
        ET.ElementTree(root).write(self.source)
        result = self.views()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("flat-colour-regions", result.stderr)
        self.assertFalse(self.flat.exists())

    def test_animation_elements_are_rejected_before_generating_views(self):
        self.init()
        original = self.source.read_bytes()
        for tag in ("animate", "animateMotion", "animateTransform", "set", "discard"):
            with self.subTest(tag=tag):
                for preview in (self.overlay, self.flat):
                    preview.unlink(missing_ok=True)
                root = ET.fromstring(original)
                layer = root.find(SVG + "g[@id='working-outlines']")
                ET.SubElement(
                    layer,
                    SVG + tag,
                    {
                        "attributeName": "href",
                        "to": "https://example.com/changed-resource",
                    },
                )
                ET.ElementTree(root).write(self.source)
                result = self.views()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(tag, result.stderr)
                self.assertFalse(self.overlay.exists())
                self.assertFalse(self.flat.exists())

    def test_init_rejects_non_png_and_non_hex_palette(self):
        for content, palette in (
            (b"not a PNG", "#000000"),
            (png(), "red"),
            (png(0, 1), "#000000"),
        ):
            with self.subTest(palette=palette, content=content[:16]):
                self.image.write_bytes(content)
                result = self.run_cli(
                    "init",
                    "--image",
                    self.image,
                    "--output",
                    self.source,
                    "--palette",
                    palette,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.source.exists())


if __name__ == "__main__":
    unittest.main()
