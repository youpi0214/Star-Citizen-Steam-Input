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
  steam-controller-2026-flight-base-controls.svg
  steam-controller-2026-flight-mining-and-salvage.svg
  assets/
    steam-controller-2026.png

scripts/
  render.py                      PNG / SVG exporter
  build_reference_sheets.py      Rebuild context-aware SVG templates
  reference_sheets.py            Context selection and panel layout
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

The repository includes three context-based sheets:

- [FPS Mode](../templates/steam-controller-2026-fps.svg)
- [Flight Mode — Base Controls](../templates/steam-controller-2026-flight-base-controls.svg)
- [Flight Mode — Mining and Salvage](../templates/steam-controller-2026-flight-mining-and-salvage.svg)

Each sheet includes its relevant base and modifier actions. The controller diagram identifies physical controls; panels below it list contextual uses and output keys. The canvas grows vertically to preserve readable text. Exports default to 5120 pixels wide, with proportional height.

Export PNGs from the repository root:

```sh
python scripts/render.py --mode fps
python scripts/render.py --mode flight --sheet all
```

Outputs are `fps-mode.png`, `flight-base-controls.png`, and `flight-mining-and-salvage.png`. `--mode flight` alone exports Base Controls. Use `--sheet mining-salvage` for the profession sheet or `--sheet base` for general controls. Use `--output-dir` for multiple exports, or `--output` for one. `--format svg` exports a self-contained SVG; `--width 7680` increases PNG resolution.

PNG export needs `rsvg-convert` (librsvg; `librsvg2-bin` on Debian/Ubuntu). Rebuilding templates or exporting with YAML overrides also needs PyYAML (`python -m pip install PyYAML`).

After editing context data, rebuild the editable SVG templates:

```sh
python scripts/build_reference_sheets.py
```

The templates contain all labels and can be exported without loading YAML. Supplying `--data data/mappings.yaml` to the exporter regenerates a context sheet from that data before export, including text wrapping and canvas height. Rebuilding replaces template edits, so keep reusable layout changes in `scripts/reference_sheets.py`.

## Publishing a release

In GitHub Actions, select **Release controller mapping → Run workflow**, select the branch to release, and choose `minor` or `major`. The workflow must first be merged into the default branch for manual dispatch to be available ([GitHub documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)).

The workflow reads all Git tags and selects the highest numeric stable version, accepting `v1.2.3`, `1.2.3`, `v1.2`, or `1.2`. Unrelated tags and prerelease tags are ignored. Minor increments the minor number; major increments the major number and resets minor to zero. Patch is always zero. With no version tags, the first release is `v0.1.0` for minor or `v1.0.0` for major.

`scripts/release_version.py` updates only the VDF's `major_revision` and `minor_revision` fields. The workflow renders all three reference sheets at 5120 pixels wide in PNG, commits the VDF version update to the selected branch, and pushes that commit and its version tag together. The GitHub release attaches PNG versions of `fps-mode`, `flight-base-controls`, and `flight-mining-and-salvage`, plus `controller_configuration.vdf`, with generated release notes.

The workflow uses the built-in `GITHUB_TOKEN` with `contents: write`; repository rules must allow that token to push the version commit and release tag. Releases are serialized across branches to avoid duplicate version allocation.

To run the version script locally (this edits the VDF):

```sh
python scripts/release_version.py minor
```

## Context-aware mapping data

`data/mappings.yaml` keeps each physical binding's `action` and `output` in its existing location. Its `uses` list describes what that output does in different gameplay contexts. Each use has a registered `context` and an `action`; optional `input` and `note` fields explain tap/hold behavior or limitations. These entries document existing outputs and do not add Steam Input commands.

The top-level `sheets` definitions group contexts for **FPS Mode**, **Flight Mode — Base Controls**, and **Flight Mode — Mining and Salvage**. A sheet may use controls from several layers: Flight Base Controls includes L4 and L5, and the profession sheet includes base-button actions such as RB firing the mining laser. The reference PDF identifies its defaults as Alpha 4.10.2; context-dependent behavior still needs in-game verification.

The renderer uses these definitions when `--data` is supplied. The template builder uses the same selection and layout code, so static templates and data-driven exports show the same actions.

## Keeping documentation synchronized

When changing the VDF, update the corresponding YAML entries, SVG labels, and control guide. Update the in-game settings guide when a custom key changes. Keep shared controls in the README and link to them from each guide. Run rendering commands from the repository root.

[Back to README](../README.md)
