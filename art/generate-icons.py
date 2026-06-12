#!/usr/bin/env python3
"""
Modern Termux icon generation tool.

This is a cross-platform replacement for the legacy shell helpers:
- generate-launcher-images.sh
- generate-big-icon.sh
- generate-feature-graphic.sh
- generate-tv-banner.sh
- copy-to-other-apps.sh

Required runtime dependencies for image generation:
    python -m pip install cairosvg pillow

Optional optimization:
    Install an oxipng Python package or make the oxipng CLI available on PATH.
    If neither is available, Pillow's built-in PNG optimizer is used.

Commands like --help do not require image-generation dependencies.
"""
from __future__ import annotations

import argparse
import io
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional


@dataclass(frozen=True)
class Density:
    name: str
    size: int


DENSITIES: tuple[Density, ...] = (
    Density("mdpi", 48),
    Density("hdpi", 72),
    Density("xhdpi", 96),
    Density("xxhdpi", 144),
    Density("xxxhdpi", 192),
)

FEATURE_GRAPHIC_SIZE = (1024, 500)
TV_BANNER_PLAY_STORE_SIZE = (1280, 720)
TV_BANNER_APP_SIZE = (320, 180)
BIG_ICON_SIZE = 512

OTHER_APPS: tuple[str, ...] = ("api", "boot", "styling", "tasker", "widget")


def require_file(path: Path, label: str = "file") -> Path:
    path = path.expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Required {label} not found: {path}")
    return path


def require_dir(path: Path, label: str = "directory") -> Path:
    path = path.expanduser()
    if not path.is_dir():
        raise FileNotFoundError(f"Required {label} not found: {path}")
    return path


def load_image_dependencies() -> tuple[Any, Any]:
    """Load CairoSVG and Pillow only when image generation is requested."""
    try:
        import cairosvg
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            f"Missing image-generation dependency: {exc}.\n"
            "Install required dependencies with:\n"
            "  python -m pip install cairosvg pillow"
        ) from exc

    return cairosvg, Image


def load_optional_oxipng() -> Any:
    try:
        import oxipng
    except ImportError:
        return None
    return oxipng


def load_png_from_bytes(png_bytes: bytes) -> Any:
    """Load image eagerly so it does not keep a closed BytesIO handle."""
    _, Image = load_image_dependencies()
    with io.BytesIO(png_bytes) as buffer:
        image = Image.open(buffer)
        image.load()
        return image


def render_svg_file(
    svg_path: Path,
    width: int,
    height: int,
    background_color: Optional[str] = None,
) -> Any:
    svg_path = require_file(svg_path, "SVG source")
    return render_svg_bytes(svg_path.read_bytes(), width, height, background_color)


def render_svg_text(
    svg_text: str,
    width: int,
    height: int,
    background_color: Optional[str] = None,
) -> Any:
    return render_svg_bytes(svg_text.encode("utf-8"), width, height, background_color)


def render_svg_bytes(
    svg_bytes: bytes,
    width: int,
    height: int,
    background_color: Optional[str] = None,
) -> Any:
    cairosvg, _ = load_image_dependencies()
    png_bytes = cairosvg.svg2png(
        bytestring=svg_bytes,
        output_width=width,
        output_height=height,
        background_color=background_color,
    )
    return load_png_from_bytes(png_bytes)


def save_png(image: Any, png_path: Path, optimize: bool = False) -> None:
    png_path = png_path.expanduser()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(png_path, "PNG")
    if optimize:
        optimize_png(png_path)


def optimize_png(png_path: Path, level: int = 4) -> None:
    """Losslessly optimize a PNG, preferring oxipng and falling back to Pillow."""
    png_path = require_file(png_path, "PNG output")

    oxipng_module = load_optional_oxipng()
    if oxipng_module is not None and hasattr(oxipng_module, "optimize"):
        try:
            oxipng_module.optimize(str(png_path), level=level)
            return
        except Exception as exc:  # pragma: no cover - optional dependency variance
            print(f"warning: oxipng module failed ({exc}); falling back", file=sys.stderr)

    oxipng_bin = shutil.which("oxipng")
    if oxipng_bin:
        try:
            subprocess.run(
                [oxipng_bin, f"-o{level}", "--strip", "safe", str(png_path)],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            return
        except subprocess.CalledProcessError as exc:
            print(f"warning: oxipng CLI failed ({exc}); falling back", file=sys.stderr)

    _, Image = load_image_dependencies()
    with Image.open(png_path) as image:
        image.save(png_path, "PNG", optimize=True)


def generate_launcher(svg_dir: Path, out_res_dir: Path, optimize: bool = True) -> None:
    """Generate density-scaled launcher and round launcher PNGs."""
    svg_dir = require_dir(svg_dir, "SVG directory")
    out_res_dir = out_res_dir.expanduser()

    for density in DENSITIES:
        output_dir = out_res_dir / f"mipmap-{density.name}"
        output_dir.mkdir(parents=True, exist_ok=True)

        for icon_name in ("ic_launcher", "ic_launcher_round"):
            svg_path = svg_dir / f"{icon_name}.svg"
            if not svg_path.exists():
                print(f"warning: skipping missing source: {svg_path}")
                continue

            output_path = output_dir / f"{icon_name}.png"
            image = render_svg_file(svg_path, density.size, density.size)
            save_png(image, output_path, optimize=optimize)
            print(f"ok: {output_path} ({density.size}x{density.size})")


def generate_big_icon(svg_path: Path, out_dir: Path, optimize: bool = True) -> None:
    """Generate 512x512 Play Store icons, transparent and square black variants."""
    svg_path = require_file(svg_path, "launcher SVG")
    out_dir = out_dir.expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    svg_text = svg_path.read_text(encoding="utf-8")
    adjusted_svg = svg_text.replace('viewBox="0 0 48 48"', 'viewBox="18 18 72 72"')

    transparent_path = out_dir / "ic_launcher_512.png"
    transparent = render_svg_text(adjusted_svg, BIG_ICON_SIZE, BIG_ICON_SIZE)
    save_png(transparent, transparent_path, optimize=optimize)
    print(f"ok: {transparent_path}")

    square_path = out_dir / "ic_launcher_square_512.png"
    square = render_svg_text(adjusted_svg, BIG_ICON_SIZE, BIG_ICON_SIZE, background_color="black")
    save_png(square, square_path, optimize=optimize)
    print(f"ok: {square_path}")


def generate_feature_graphic(svg_path: Path, out_dir: Path, optimize: bool = True) -> None:
    """Generate the 1024x500 Play Store feature graphic."""
    out_dir = out_dir.expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    width, height = FEATURE_GRAPHIC_SIZE
    image = render_svg_file(svg_path, width, height)
    output_path = out_dir / "feature-graphic.png"
    save_png(image, output_path, optimize=optimize)
    print(f"ok: {output_path}")


def generate_tv_banner(
    svg_path: Path,
    out_dir: Path,
    app_res_dir: Path,
    optimize: bool = True,
) -> None:
    """Generate Play Store and in-app TV banners."""
    out_dir = out_dir.expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    play_width, play_height = TV_BANNER_PLAY_STORE_SIZE
    play_image = render_svg_file(svg_path, play_width, play_height)
    play_path = out_dir / "tv-banner.png"
    save_png(play_image, play_path, optimize=optimize)
    print(f"ok: {play_path}")

    app_width, app_height = TV_BANNER_APP_SIZE
    app_image = render_svg_file(svg_path, app_width, app_height)
    app_path = app_res_dir.expanduser() / "drawable" / "banner.png"
    save_png(app_image, app_path, optimize=optimize)
    print(f"ok: {app_path}")


def copy_to_other_apps(source_app_dir: Path, target_root: Path) -> None:
    """Copy shared icon XML assets from termux-app into sibling Termux app repos."""
    source_app_dir = require_dir(source_app_dir, "source termux-app directory")
    target_root = require_dir(target_root, "target parent directory")

    source_drawable = source_app_dir / "app/src/main/res/drawable"
    source_anydpi = source_app_dir / "app/src/main/res/drawable-anydpi-v26"

    for app_name in OTHER_APPS:
        target_app_dir = target_root / f"termux-{app_name}"
        if not target_app_dir.is_dir():
            print(f"warning: skipping missing target repo: {target_app_dir}")
            continue

        copy_xml_files(
            source_drawable,
            target_app_dir / "app/src/main/res/drawable",
            ("ic_foreground.xml", "ic_launcher.xml"),
            app_name,
        )
        copy_xml_files(
            source_anydpi,
            target_app_dir / "app/src/main/res/drawable-anydpi-v26",
            ("ic_launcher.xml",),
            app_name,
        )


def copy_xml_files(source_dir: Path, target_dir: Path, filenames: Iterable[str], app_name: str) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    for filename in filenames:
        source_path = source_dir / filename
        if not source_path.is_file():
            print(f"warning: missing source asset: {source_path}")
            continue
        target_path = target_dir / filename
        shutil.copy2(source_path, target_path)
        print(f"ok: copied {filename} -> termux-{app_name}")


def add_common_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("~/termux-icons"),
        help="Output directory for generated store assets",
    )
    parser.add_argument("--no-optimize", action="store_true", help="Skip PNG optimization")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Termux launcher and store icon assets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python art/generate-icons.py launcher --svg-dir art --out app/src/main/res
  python art/generate-icons.py big-icon --svg art/ic_launcher.svg
  python art/generate-icons.py feature --svg art/feature-graphic.svg
  python art/generate-icons.py tv-banner --svg art/tv-banner.svg --app-res app/src/main/res
  python art/generate-icons.py copy --from . --to ..
  python art/generate-icons.py all --svg-dir art --from . --to ..
""",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    launcher = subparsers.add_parser("launcher", help="Generate density-scaled launcher icons")
    launcher.add_argument("--svg-dir", type=Path, default=Path("art"))
    launcher.add_argument("--out", type=Path, default=Path("app/src/main/res"))
    launcher.add_argument("--no-optimize", action="store_true", help="Skip PNG optimization")

    big_icon = subparsers.add_parser("big-icon", help="Generate 512x512 Play Store icons")
    big_icon.add_argument("--svg", type=Path, required=True)
    add_common_output_args(big_icon)

    feature = subparsers.add_parser("feature", help="Generate the Play Store feature graphic")
    feature.add_argument("--svg", type=Path, default=Path("art/feature-graphic.svg"))
    add_common_output_args(feature)

    tv_banner = subparsers.add_parser("tv-banner", help="Generate TV banner assets")
    tv_banner.add_argument("--svg", type=Path, default=Path("art/tv-banner.svg"))
    tv_banner.add_argument("--app-res", type=Path, default=Path("app/src/main/res"))
    add_common_output_args(tv_banner)

    copy = subparsers.add_parser("copy", help="Copy shared icon XML assets to sibling Termux repos")
    copy.add_argument("--from", type=Path, required=True, dest="source")
    copy.add_argument("--to", type=Path, required=True, dest="target_root")

    all_cmd = subparsers.add_parser("all", help="Run all generation steps")
    all_cmd.add_argument("--svg-dir", type=Path, default=Path("art"))
    all_cmd.add_argument("--from", type=Path, required=True, dest="source")
    all_cmd.add_argument("--to", type=Path, dest="target_root")
    all_cmd.add_argument("--out", type=Path, default=Path("~/termux-icons"))
    all_cmd.add_argument("--no-optimize", action="store_true", help="Skip PNG optimization")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    optimize = not getattr(args, "no_optimize", False)

    try:
        if args.command == "launcher":
            generate_launcher(args.svg_dir, args.out, optimize=optimize)
        elif args.command == "big-icon":
            generate_big_icon(args.svg, args.out, optimize=optimize)
        elif args.command == "feature":
            generate_feature_graphic(args.svg, args.out, optimize=optimize)
        elif args.command == "tv-banner":
            generate_tv_banner(args.svg, args.out, args.app_res, optimize=optimize)
        elif args.command == "copy":
            copy_to_other_apps(args.source, args.target_root)
        elif args.command == "all":
            res_dir = args.source.expanduser() / "app/src/main/res"
            generate_launcher(args.svg_dir, res_dir, optimize=optimize)
            generate_big_icon(args.svg_dir / "ic_launcher.svg", args.out, optimize=optimize)
            generate_feature_graphic(args.svg_dir / "feature-graphic.svg", args.out, optimize=optimize)
            generate_tv_banner(args.svg_dir / "tv-banner.svg", args.out, res_dir, optimize=optimize)
            if args.target_root:
                copy_to_other_apps(args.source, args.target_root)
        else:
            raise ValueError(f"Unsupported command: {args.command}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
