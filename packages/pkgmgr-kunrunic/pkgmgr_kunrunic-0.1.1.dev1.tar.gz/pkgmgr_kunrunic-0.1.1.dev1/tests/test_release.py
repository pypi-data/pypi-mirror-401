import json
import os
import sys
import tempfile
from importlib import import_module, reload
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

config = import_module("pkgmgr.config")
release = import_module("pkgmgr.release")
snapshot = import_module("pkgmgr.snapshot")
reload(config)
reload(release)
reload(snapshot)


def _setup_state_dir(monkeypatch, base_dir):
    state_dir = Path(base_dir) / "state"
    monkeypatch.setattr(config, "DEFAULT_STATE_DIR", str(state_dir))
    monkeypatch.setattr(snapshot, "STATE_DIR", str(state_dir))
    return state_dir


def _write_pkg_yaml(pkg_dir, pkg_id, include_releases):
    config.write_pkg_template(
        os.path.join(pkg_dir, "pkg.yaml"),
        pkg_id=pkg_id,
        pkg_root=pkg_dir,
        include_releases=include_releases,
        git_cfg={"keywords": []},
        collectors_enabled=["checksums"],
    )


def test_create_pkg_existing_dir_keeps_files_and_writes_pkg_yaml(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        _setup_state_dir(monkeypatch, base)
        pkg_root = base / "pkgs"
        pkg_id = "20240101"
        pkg_dir = pkg_root / pkg_id
        pkg_dir.mkdir(parents=True)
        keep_file = pkg_dir / "keep.txt"
        keep_file.write_text("keep")

        cfg = {"pkg_release_root": str(pkg_root)}
        release.create_pkg(cfg, pkg_id)

        assert keep_file.exists()
        assert keep_file.read_text() == "keep"
        assert (pkg_dir / "pkg.yaml").exists()


def test_create_pkg_missing_dir_creates_dir_and_pkg_yaml(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        _setup_state_dir(monkeypatch, base)
        pkg_root = base / "pkgs"
        pkg_id = "20240102"
        pkg_dir = pkg_root / pkg_id

        cfg = {"pkg_release_root": str(pkg_root)}
        release.create_pkg(cfg, pkg_id)

        assert pkg_dir.exists()
        assert (pkg_dir / "pkg.yaml").exists()


def test_update_pkg_first_release_includes_all_files(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        _setup_state_dir(monkeypatch, base)
        pkg_root = base / "pkgs"
        pkg_id = "20240103"
        pkg_dir = pkg_root / pkg_id
        pkg_dir.mkdir(parents=True)

        src_dir = pkg_dir / "src"
        src_dir.mkdir()
        (src_dir / "a.txt").write_text("alpha")
        (src_dir / "b.txt").write_text("bravo")

        _write_pkg_yaml(str(pkg_dir), pkg_id, ["src"])
        cfg = {"pkg_release_root": str(pkg_root)}

        out_path = release.update_pkg(cfg, pkg_id)
        data = json.loads(Path(out_path).read_text())

        bundles = data["release"]
        assert len(bundles) == 1
        bundle = bundles[0]
        assert set(bundle["copied"]) == {"a.txt", "b.txt"}
        release_dir = Path(bundle["release_dir"])
        assert (release_dir / "a.txt").exists()
        assert (release_dir / "b.txt").exists()


def test_update_pkg_skips_release_when_no_changes(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        _setup_state_dir(monkeypatch, base)
        pkg_root = base / "pkgs"
        pkg_id = "20240104"
        pkg_dir = pkg_root / pkg_id
        pkg_dir.mkdir(parents=True)

        src_dir = pkg_dir / "src"
        src_dir.mkdir()
        (src_dir / "a.txt").write_text("alpha")

        _write_pkg_yaml(str(pkg_dir), pkg_id, ["src"])
        cfg = {"pkg_release_root": str(pkg_root)}

        release.update_pkg(cfg, pkg_id)
        out_path = release.update_pkg(cfg, pkg_id)
        data = json.loads(Path(out_path).read_text())

        assert data["release"] == []
        release_root = pkg_dir / "release" / "src"
        versions = sorted(p.name for p in release_root.iterdir() if p.is_dir())
        assert versions == ["release.v0.0.1"]


def test_update_pkg_includes_new_and_modified_files(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        _setup_state_dir(monkeypatch, base)
        pkg_root = base / "pkgs"
        pkg_id = "20240105"
        pkg_dir = pkg_root / pkg_id
        pkg_dir.mkdir(parents=True)

        src_dir = pkg_dir / "src"
        src_dir.mkdir()
        (src_dir / "a.txt").write_text("alpha")
        (src_dir / "b.txt").write_text("bravo")

        _write_pkg_yaml(str(pkg_dir), pkg_id, ["src"])
        cfg = {"pkg_release_root": str(pkg_root)}

        release.update_pkg(cfg, pkg_id)

        (src_dir / "a.txt").write_text("alpha2")
        (src_dir / "c.txt").write_text("charlie")

        out_path = release.update_pkg(cfg, pkg_id)
        data = json.loads(Path(out_path).read_text())

        bundles = data["release"]
        assert len(bundles) == 1
        bundle = bundles[0]
        assert set(bundle["copied"]) == {"a.txt", "c.txt"}
        assert set(bundle["skipped"]) == {"b.txt"}
        release_dir = Path(bundle["release_dir"])
        assert (release_dir / "a.txt").exists()
        assert (release_dir / "c.txt").exists()
        assert not (release_dir / "b.txt").exists()
