#!/usr/bin/env python3
"""Create an empty PNG-backed review scaffold or presentation-only SVG views.

Uses the five direct-child layers it creates. No renderer, contour generation,
mask closure/palette audit, general SVG sanitization, or approval automation.
Overlay print-region outlines use a fixed width of 1 SVG user unit (source
pixel before any saved transforms); zoom and scaling can require manual review.
"""

import argparse
import base64
import copy
import hashlib
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET


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
PRINT_LAYERS = {"flat-colour-regions", "user-corrected-regions"}
ET.register_namespace("", SVG[1:-1])
ET.register_namespace("inkscape", INK[1:-1])
ET.register_namespace("sodipodi", SODI[1:-1])


def serialize(root):
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_new(outputs):
    """Reserve every destination before writing; never truncate existing files."""
    paths = [path.resolve() for path, _ in outputs]
    if len(set(paths)) != len(paths):
        raise ValueError("Output paths must be distinct")
    for path, _ in outputs:
        if path.exists() or path.is_symlink():
            raise ValueError(f"Refusing to overwrite: {path}")
    opened = []
    try:
        for path, data in outputs:
            opened.append((path, path.open("xb"), data))
        for _, stream, data in opened:
            stream.write(data)
        for _, stream, _ in opened:
            stream.close()
    except OSError:
        for path, stream, _ in opened:
            stream.close()
            path.unlink()
        raise


def init_review(image, output, palette):
    if not all(re.fullmatch(r"#[0-9a-fA-F]{6}", colour) for colour in palette):
        raise ValueError(
            "Palette entries must be six-digit hex colours such as #ff0000"
        )
    raster = image.read_bytes()
    if (
        len(raster) < 33
        or raster[:8] != b"\x89PNG\r\n\x1a\n"
        or raster[8:16] != b"\0\0\0\rIHDR"
    ):
        raise ValueError("Reference must be a PNG with an IHDR header")
    width, height = struct.unpack(">II", raster[16:24])
    if not width or not height:
        raise ValueError("PNG width and height must be positive")
    root = ET.Element(
        SVG + "svg",
        {
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "data-status": "PREVIEW ONLY",
        },
    )
    ET.SubElement(root, SVG + "title").text = "PREVIEW ONLY — empty review scaffold"
    ET.SubElement(root, SVG + "desc").text = (
        "No contours or colour masks have been authored or approved. "
        "Keep edits in the named layers; visually verify both views before review."
    )
    ET.SubElement(
        root,
        SVG + "metadata",
        {
            "data-source-name": image.name,
            "data-source-sha256": hashlib.sha256(raster).hexdigest(),
            "data-palette": " ".join(palette),
            "data-coordinate-units": "pixels",
        },
    )
    for layer_id in LAYERS:
        group = ET.SubElement(
            root,
            SVG + "g",
            {
                "id": layer_id,
                INK + "groupmode": "layer",
                INK + "label": layer_id.replace("-", " ").title(),
            },
        )
        if layer_id == "original-reference":
            group.set(SODI + "insensitive", "true")
            ET.SubElement(
                group,
                SVG + "image",
                {
                    "id": "original-raster",
                    "x": "0",
                    "y": "0",
                    "width": str(width),
                    "height": str(height),
                    "preserveAspectRatio": "none",
                    "href": "data:image/png;base64,"
                    + base64.b64encode(raster).decode("ascii"),
                },
            )
    write_new([(output, serialize(root))])


def read_review(source):
    content = source.read_bytes()
    text = content.decode("utf-8-sig")
    if "\0" in text or re.search(
        r"<!\s*(?:DOCTYPE|ENTITY)\b|<\?xml-stylesheet\b", text, re.I
    ):
        raise ValueError(
            "DTD, entities, XML stylesheets and non-UTF-8 SVG are unsupported"
        )
    root = ET.fromstring(text)
    if root.tag != SVG + "svg":
        raise ValueError("Input must be an SVG document")
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag.lower() in {
            "script",
            "foreignobject",
            "style",
            "animate",
            "animatemotion",
            "animatetransform",
            "set",
            "discard",
        }:
            raise ValueError(f"Unsupported SVG element: {tag}")
        for key, value in node.attrib.items():
            local = key.rsplit("}", 1)[-1].lower()
            if local.startswith("on"):
                raise ValueError("SVG event handlers are unsupported")
            if local == "href" and not (
                value.startswith("#")
                or (tag == "image" and value.startswith("data:image/png;base64,"))
            ):
                raise ValueError(
                    "External href resources are unsupported; embed PNG references"
                )
            for resource in re.findall(r"url\s*\((.*?)\)", value, re.I):
                if not resource.strip().strip("\"'").startswith("#"):
                    raise ValueError("External CSS resources are unsupported")
    for layer_id in LAYERS:
        matching = [node for node in root.iter() if node.get("id") == layer_id]
        if (
            len(matching) != 1
            or matching[0] not in list(root)
            or matching[0].tag != SVG + "g"
        ):
            raise ValueError(
                f"Required unique direct-child group missing or misplaced: {layer_id}"
            )
        if layer_id in PRINT_LAYERS:
            for node in matching[0].iter():
                if node.tag in {SVG + "image", SVG + "use", SVG + "text"}:
                    raise ValueError(
                        f"Keep raster references, clones and annotations outside {layer_id}"
                    )
    for node in root:
        if (
            node.tag.startswith(SVG)
            and node.tag
            not in {SVG + "title", SVG + "desc", SVG + "metadata", SVG + "defs"}
            and node.get("id") not in LAYERS
        ):
            raise ValueError("Keep drawing content inside the five named review groups")
    return root, hashlib.sha256(content).hexdigest()


def set_style(node, updates):
    declarations = [
        part.strip()
        for part in node.get("style", "").split(";")
        if part.strip() and part.split(":", 1)[0].strip().lower() not in updates
    ]
    node.set(
        "style",
        ";".join(
            declarations
            + [f"{key}:{value} !important" for key, value in updates.items()]
        ),
    )


def create_views(source, overlay, flat):
    original, source_hash = read_review(source)
    outputs = []
    for output, visible, name in (
        (overlay, set(LAYERS), "overlay"),
        (flat, PRINT_LAYERS, "flat-colour"),
    ):
        root = copy.deepcopy(original)
        root.set("data-status", "PREVIEW ONLY")
        root.set("data-presentation", name)
        root.set("data-review-sha256", source_hash)
        title = root.find(SVG + "title")
        if title is None:
            title = ET.SubElement(root, SVG + "title")
        title.text = f"PREVIEW ONLY — {name}; visually verify; no approval implied"
        for group in root.findall(SVG + "g"):
            layer_id = group.get("id")
            display = "inline" if layer_id in visible else "none"
            group.set("display", display)
            group.set("visibility", "visible")
            set_style(group, {"display": display, "visibility": "visible"})
            if name == "overlay" and layer_id in PRINT_LAYERS:
                for node in group.iter():
                    if node.tag in {
                        SVG + shape
                        for shape in (
                            "path",
                            "rect",
                            "circle",
                            "ellipse",
                            "line",
                            "polyline",
                            "polygon",
                        )
                    }:
                        set_style(
                            node,
                            {"fill": "none", "stroke": "#00ffff", "stroke-width": "1"},
                        )
        outputs.append((output, serialize(root)))
    write_new(outputs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create an empty PNG-backed SVG scaffold")
    init.add_argument("--image", type=Path, required=True)
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--palette", nargs="+", required=True, metavar="#RRGGBB")
    views = commands.add_parser(
        "views", help="Create two SVG previews from saved edited paths"
    )
    views.add_argument("input", type=Path)
    views.add_argument("--overlay", type=Path, required=True)
    views.add_argument("--flat", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            init_review(args.image, args.output, args.palette)
        else:
            create_views(args.input, args.overlay, args.flat)
    except (OSError, ValueError, ET.ParseError) as error:
        parser.exit(2, f"error: {error}\n")
    print(
        "PREVIEW ONLY. Visually verify the SVG; no masks, model or approval were generated."
    )


if __name__ == "__main__":
    main()
