<h1 align="center">Star Citizen — Steam Controller 2026</h1>

<p align="center">
  <a href="https://github.com/youpi0214/Star-Citizen-Steam-Input/releases/latest">
    <img src="https://img.shields.io/github/v/release/youpi0214/Star-Citizen-Steam-Input" alt="Latest release">
  </a>
  <img src="https://img.shields.io/badge/Star%20Citizen-4.10.3-blue" alt="Supported Star Citizen version: 4.10.3">
</p>

A Steam Input configuration for **Star Citizen** built around the **Steam Controller 2026**.

The layout is designed to make both on-foot and flight gameplay practical from the controller without trying to reproduce every keyboard binding. It uses two dedicated Steam Input Action Sets, a shared **L4 modifier layer**, gyro-assisted aiming, trackpad menus, and direct mode switching.

## Status

FPS and Flight Mode layouts are implemented, including L4 modifier layers, gyro aiming, and R4 mode switching. The FPS left trackpad is intentionally unassigned.

| OS | Distribution / version | Desktop environment | Validation |
| --- | --- | --- | --- |
| Linux | CachyOS | KDE Plasma 6.8.2 | Tested |
| Windows | — | — | Not validated |

## Setup and installation

1. [Set up RSI Launcher in Steam](docs/setup.md): add the non-Steam shortcut, name it `rsi launcher`, and configure Steam Input.
2. [Install the controller layout](docs/installation.md): use **Community Layouts (recommended)**, or manually install the VDF from the [latest release](https://github.com/youpi0214/Star-Citizen-Steam-Input/releases/latest).
3. Configure the required in-game bindings below, then test the layout in Arena Commander or another safe environment.

If Steam activates desktop controls while playing, see [Linux troubleshooting](docs/troubleshooting.md).

## Required in-game setup

Configure these custom bindings to use the corresponding controller actions:

| In-game action | Key | Controller input |
| --- | --- | --- |
| Inspect Item | Letter `O` | FPS: M1 + R3 hold |
| Cycle mouse mode (VJoy / Relative) | `.` | Flight: R5 press |

See [in-game setup instructions](docs/game-settings.md#required-in-game-bindings) for the menu paths and how to use a different key.

## Quick controls

- **FPS Mode:** on-foot movement, combat, interaction, and inventory.
- **Flight Mode:** ships and ground vehicles, including movement, combat, targeting, and vehicle systems.
- Hold **L4** for the current mode's modifier layer; press **R4** to switch modes.
- In Flight Mode, hold **L5** for cruise control and speed-limiter adjustment.

### Input notation

| Notation | Meaning |
| --- | --- |
| Regular | Normal button press |
| `[H]` | Long Press / physical hold where noted |
| `[2]` | Double Press |
| `M1` | Hold **L4** while using the control |
| Touch | Capacitive right-stick touch |

> A Steam Input Regular Press mapped to a keyboard key remains held while the physical control remains held. This is used where Star Citizen itself distinguishes between tapping and holding the same key.

### Shared controls

These controls are shared between FPS and Flight Mode.

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| START | Regular | Menu | `Esc` |
| BACK | Regular | mobiGlas | `F1` |
| BACK | `[H]` | Map | `F2` |
| L4 | Regular / hold | Hold L4 Modifier layer | Steam Input Action Set Layer |
| R4 | Regular | Switch FPS / Flight Mode | Steam Input Change Action Set |
| M1 + BACK | Regular | Accept invite | `[` |
| M1 + START | Regular | Decline invite | `]` |

## Control references

- [FPS controls and modifier mappings](docs/controls/fps.md)
- [Flight controls, trackpads, and modifier mappings](docs/controls/flight.md)
- SVG sheets: [FPS Mode](templates/steam-controller-2026-fps.svg) · [Flight Mode — Base Controls](templates/steam-controller-2026-flight-base-controls.svg) · [Flight Mode — Mining and Salvage](templates/steam-controller-2026-flight-mining-and-salvage.svg)
- [Download PNG reference sheets from the latest release](https://github.com/youpi0214/Star-Citizen-Steam-Input/releases/latest)

## Further reading

- [Suggested quality-of-life settings](docs/game-settings.md#suggested-quality-of-life-settings)
- [Development, rendering, and releases](docs/development.md)
