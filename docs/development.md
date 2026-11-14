# Development and Releases

Maintenance instructions for the controller configuration and its documentation.

## Design goals

This layout prioritizes:

- keeping movement and aiming available at all times;
- minimizing keyboard use during normal play;
- separating FPS and Flight controls instead of overloading one layout;
- using L4 as a temporary modifier rather than introducing additional persistent modes;
- retaining gyro precision aiming through right-stick touch;
- grouping targeting and ship-system controls spatially on the trackpads;
- keeping the reference sheets readable enough to use while learning the layout.

## Repository structure

```text
mapping/
  controller_configuration.vdf   Steam Input configuration

data/
  mappings.yaml                  Human-readable mapping data

templates/
  steam-controller-2026-fps.svg
  steam-controller-2026-flight.svg
  assets/
    steam-controller-2026.png

scripts/
  render.py                      SVG mapping renderer
  release_version.py             Release version and VDF revision updater

docs/
  setup.md                       RSI Launcher shortcut and Steam settings
  installation.md                Community and manual layout installation
  troubleshooting.md             Linux Desktop Layout workaround
  controls/                      FPS and Flight control references
  game-settings.md               Required bindings and optional settings
  development.md                 Maintenance and release instructions
  images/                        Documentation images
```

The **VDF is the authoritative controller configuration**. `data/mappings.yaml` and the SVG sheets are documentation and should stay synchronized with it.

## Visual reference sheets

The repository includes separate visual mapping sheets for FPS and Flight Mode:

- [FPS SVG template](../templates/steam-controller-2026-fps.svg)
- [Flight SVG template](../templates/steam-controller-2026-flight.svg)

The Steam button and `...` button are intentionally omitted from the callouts because they are not intended to be mapped.

Export the finished templates from the repository root:

```sh
python scripts/render.py --mode fps
python scripts/render.py --mode flight --format jpeg
```

The default export is a 5120 × 2880 PNG. The controller image is included in the exported pixels, and the finished template labels are preserved. Use `--width 7680` for a larger export, or `--output output/fps.jpg` to choose a filename and format. Raster exports use `rsvg-convert` (provided by librsvg); JPEG export also requires Pillow. Install these dependencies before exporting; on Debian/Ubuntu, `rsvg-convert` is provided by `librsvg2-bin`, and Pillow can be installed with `python -m pip install Pillow`.

Use `--data data/mappings.yaml` when you want to replace the template's bound labels with YAML values. This optional step requires PyYAML. `--format svg` exports a self-contained SVG with its controller image embedded. Paths are relative to the current working directory.

## Publishing a release

In GitHub Actions, select **Release controller mapping → Run workflow**, select the branch to release, and choose `minor` or `major`. The workflow must first be merged into the default branch for manual dispatch to be available ([GitHub documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)).

The workflow reads all Git tags and selects the highest numeric stable version, accepting `v1.2.3`, `1.2.3`, `v1.2`, or `1.2`. Unrelated tags and prerelease tags are ignored. Minor increments the minor number; major increments the major number and resets minor to zero. Patch is always zero. With no version tags, the first release is `v0.1.0` for minor or `v1.0.0` for major.

`scripts/release_version.py` updates only the VDF's `major_revision` and `minor_revision` fields. The workflow renders both finished templates at 5120 × 2880 in PNG and JPEG, commits the VDF version update to the selected branch, and pushes that commit and its version tag together. The GitHub release attaches `fps.png`, `flight.png`, `fps.jpeg`, `flight.jpeg`, and `controller_configuration.vdf`, with generated release notes.

The workflow uses the built-in `GITHUB_TOKEN` with `contents: write`; repository rules must allow that token to push the version commit and release tag. Releases are serialized across branches to avoid duplicate version allocation.

To run the version script locally (this edits the VDF):

```sh
python scripts/release_version.py minor
```

## Keeping documentation synchronized

When changing the VDF, update the corresponding YAML entries, SVG labels, and control guide. Update the in-game settings guide when a custom key changes. Keep shared controls in the README and link to them from each guide. Run rendering commands from the repository root.

[Back to README](../README.md)
