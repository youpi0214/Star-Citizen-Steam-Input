# Star Citizen — Steam Controller 2026

A Steam Input configuration for **Star Citizen** built around the **Steam Controller 2026**.

The layout is designed to make both on-foot and flight gameplay practical from the controller without trying to reproduce every keyboard binding. It uses two dedicated Steam Input Action Sets, a shared **L4 modifier layer**, gyro-assisted aiming, trackpad menus, and direct mode switching.

## Overview

The configuration contains two primary Action Sets:

- **FPS Mode** — on-foot movement, combat, interaction and inventory controls.
- **Flight Mode** — ship movement, combat, targeting and common vehicle systems.

Hold **L4** to temporarily activate the mode-specific modifier layer. Long-press **RG** to switch between FPS and Flight Mode.

### Input notation

| Notation | Meaning |
| --- | --- |
| Regular | Normal button press |
| `[H]` | Long Press / physical hold where noted |
| `[2]` | Double Press |
| `M1` | Hold **L4** while using the control |
| Touch | Capacitive right-stick touch |

> A Steam Input Regular Press mapped to a keyboard key remains held while the physical control remains held. This is used where Star Citizen itself distinguishes between tapping and holding the same key.

> **Custom bind required:** Star Citizen Alpha 4.10 has no default keyboard binding for **Inspect Item**. Bind **Inspect Item** to `O` in Star Citizen → Options → Keybindings → Advanced Controls Customization → On Foot - All. The Steam layout then exposes it as **M1 + R3 [H]**.

## Global controls

These controls are shared between FPS and Flight Mode.

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| START | Regular | Menu | `Esc` |
| BACK | Regular | mobiGlas | `F1` |
| BACK | `[H]` | Map | `F2` |
| L4 | Regular / hold | Hold L4 Modifier layer | Steam Input Action Set Layer |
| RG | `[H]` | Switch FPS / Flight Mode | Steam Input Change Action Set |
| M1 + BACK | Regular | Accept invite | `[` |
| M1 + START | Regular | Decline invite | `]` |

---

# FPS Mode

FPS Mode keeps conventional shooter movement on the sticks while using the rear controls and L4 modifier for secondary Star Citizen actions.

## FPS mapping

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| Left Stick | — | Move | `WASD` |
| L3 | Regular | Sprint toggle | `Left Shift` |
| Right Stick | — | Aim / Look | Mouse |
| Right Stick Touch | Touch | Enable precision gyro aim | Gyro To Mouse |
| Right Stick Touch | `[2]` | Flashlight | `T` |
| R3 | Regular | Melee | Middle Mouse |
| R3 | `[2]` | Fire mode toggle | `B` |
| LT | Regular | ADS | Right Mouse |
| RT | Regular | Fire / Use | Left Mouse |
| LB | Regular | Lean left | `Q` press/release |
| RB | Regular | Lean right | `E` press/release |
| A | Regular | Jump | `Space` |
| B | Regular | Crouch | `C` |
| B | `[H]` | Prone | `Left Ctrl` |
| X | Regular | Reload / Holster | `R` |
| Y | Regular | Interact | `F` |
| Y | `[2]` | Hold interaction | `F` toggle |
| D-pad Right | Regular | Inventory | `I` |
| Right Trackpad ↑ | Regular | Scroll up | Mouse Wheel Up |
| Right Trackpad ↓ | Regular | Scroll down | Mouse Wheel Down |
| Left Trackpad | — | Unassigned | — |
| **L5** | Tap | Primary weapon | `1` |
| **L5** | Hold | Weapon wheel | `1` held |

## FPS — L4 modifier (`M1`)

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| M1 + A | Regular | Key B | `B` |
| M1 + X | Regular | Ammo backpack refill | `Left Alt + 1` |
| M1 + LB | Regular | Consumable / healing wheel | `4` |
| M1 + RB | Regular | Throwables radial | `G` |
| M1 + R3 | Regular | Customize weapon | `J` |
| M1 + R3 | `[H]` | Inspect item / weapon | `O`* |
| M1 + D-pad Up | Regular | Camera view | `F4` |
| M1 + D-pad Left | Regular | Toggle chat | `F12` |
| M1 + D-pad Down | Regular | Helmet on/off | `Left Alt + H` |
| M1 + BACK | Regular | Accept invite | `[` |
| M1 + START | Regular | Decline invite | `]` |

---

# Flight Mode

Flight Mode moves translational and rotational control onto the sticks/triggers while using the trackpads as dedicated targeting and ship-system clusters.

## Flight mapping

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| Right Stick | — | Pitch / Yaw | Mouse X/Y |
| Right Stick Touch | Touch | Precision aim | Gyro To Mouse |
| Right Stick Touch | `[2]` | Lights | `L` |
| LT | Regular | Reverse thrust | `S` |
| RT | Regular | Forward thrust | `W` |
| Left Stick Y | — | Strafe up / down | `Space` / `Left Ctrl` |
| Left Stick X | — | Roll left / right | `Q` / `E` |
| L3 | Regular | Boost | `Left Shift` |
| LB | Regular | Precision targeting / hold max zoom | Right Mouse |
| LB | `[2]` | Gimbal mode toggle | `G` |
| RB | Regular | Fire | Left Mouse |
| R3 | Regular | Next weapon preset | Mouse Wheel Down |
| A | Regular | NAV / Combat toggle | `B` |
| A | `[H]` | Engage Quantum Drive | Left Mouse |
| B | Regular | Spacebrake | `X` |
| X | Regular | Cycle operator mode | Middle Mouse |
| X | `[2]` | Ping | `Tab` |
| Y | Regular | VTOL | `K` |
| Y | `[2]` | Hold interaction | `F` toggle/hold equivalent |
| Y | `[H]` | Exit seat | `Y` |
| D-pad Down | Regular | Landing gear | `N` |
| D-pad Down | `[H]` | Autoland | `N` held |

## Flight — Right trackpad targeting

| Trackpad input | Action | Output |
| --- | --- | --- |
| ↑ | Target in view | `T` |
| ↓ | Unlock target | `Left Alt + T` |
| ← | Cycle attackers | `4` |
| → | Cycle hostiles | `5` |
| Center click | Cycle all / closest | `7` |

## Flight — Left trackpad systems

| Trackpad input | Action | Output |
| --- | --- | --- |
| ↑ | Power | `U` |
| ↓ | Engines | `I` |
| ← | Shields | `O` |
| → | Weapons | `P` |
| Center click | Toggle ship ports / doors | `Right Alt + K` |

## Flight — L4 modifier (`M1`)

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| M1 + Left Stick X | — | Strafe left / right | `A` / `D` |
| M1 + A | Regular | Decoupled toggle | `C` |
| M1 + LB | Regular | Decoy | `H` |
| M1 + RB | Regular | Noise | `J` |
| M1 + R3 | Regular | Freelook | `Z` |
| M1 + Right Stick Touch | `[2]` | LAMP | `Right Alt + L` |
| M1 + D-pad Up | Regular | Camera view | `F4` |
| M1 + D-pad Left | Regular | Toggle chat | `F12` |
| M1 + D-pad Down | Regular | Request landing | `Left Alt + N` |
| M1 + BACK | Regular | Accept invite | `[` |
| M1 + START | Regular | Decline invite | `]` |

---

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
```

The **VDF is the authoritative controller configuration**. `data/mappings.yaml` and the SVG sheets are documentation and should stay synchronized with it.

## Visual reference sheets

The repository includes separate visual mapping sheets for FPS and Flight Mode:

- `templates/steam-controller-2026-fps.svg`
- `templates/steam-controller-2026-flight.svg`

The Steam button and `...` button are intentionally omitted from the callouts because they are not intended to be mapped.

## Installing the Steam Input configuration

1. Add the RSI Launcher / Star Citizen to Steam as a non-Steam game if it is not already present.
2. Close Steam before replacing or importing controller configuration files.
3. Use `mapping/controller_configuration.vdf` as the Steam Input configuration source.
4. Restart Steam and verify that **FPS Mode**, **Flight Mode**, and their **L4 Modifier** layers are present.
5. Test the configuration in Arena Commander or another safe environment before relying on it in the Persistent Universe.

> Steam may associate local controller layouts with the Steam shortcut's app ID and local controller configuration state. Keep a backup before manually replacing Steam Input files.

## Design goals

This layout prioritizes:

- keeping movement and aiming available at all times;
- minimizing keyboard use during normal play;
- separating FPS and Flight controls instead of overloading one layout;
- using L4 as a temporary modifier rather than introducing additional persistent modes;
- retaining gyro precision aiming through right-stick touch;
- grouping targeting and ship-system controls spatially on the trackpads;
- keeping the reference sheets readable enough to use while learning the layout.

## Status

Flight Mode is fully mapped in the current configuration. FPS Mode is substantially complete, with a small number of secondary actions still awaiting final keyboard outputs in the documentation/configuration.
