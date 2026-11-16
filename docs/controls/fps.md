# FPS Mode

FPS Mode keeps conventional shooter movement on the sticks while using the rear controls and L4 modifier for secondary Star Citizen actions.

See [quick controls and input notation](../../README.md#quick-controls) for shared controls, and [required game setup](../game-settings.md#required-in-game-bindings) for custom bindings.

## Visual reference sheet

[FPS Mode](../../templates/steam-controller-2026-fps.svg) includes on-foot and EVA actions across the base layout and L4 modifier.

## FPS mapping

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| Left Stick | — | Move | `WASD` |
| L3 | Regular | Sprint toggle | `Left Shift` |
| Right Stick | — | Aim / Look | Mouse |
| Right Stick Touch | Touch | Enable precision gyro aim | Gyro To Mouse |
| Right Stick Touch | `[2]` | Flashlight | `T` |
| R3 | Hold | Melee / takedown | Middle Mouse |
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
| M1 + A | Regular | Change fire mode | `B` |
| M1 + X | Regular | Ammo backpack refill | `Left Alt + 1` |
| M1 + LB | Regular | Consumable / healing wheel | `4` |
| M1 + RB | Regular | Throwables radial | `G` |
| M1 + Right Trackpad ↑ | Scroll | Increase hand-mining laser power | Left Alt + Mouse Wheel Up |
| M1 + Right Trackpad ↓ | Scroll | Decrease hand-mining laser power | Left Alt + Mouse Wheel Down |
| M1 + R3 | Regular | Customize weapon | `J` |
| M1 + R3 | `[H]` | Inspect item / weapon | Letter `O` (custom bind) |
| M1 + D-pad Up | Regular | Camera view | `F4` |
| M1 + D-pad Left | Regular | Toggle chat | `F12` |
| M1 + D-pad Down | Regular | Helmet on/off | `Left Alt + H` |
| M1 + BACK | Regular | Accept invite | `[` |
| M1 + START | Regular | Decline invite | `]` |

## Contextual on-foot actions

These actions reuse the outputs above. Their effect depends on the equipped tool, inventory screen, or interaction context. A physical hold keeps the regular output held unless a Long Press is explicitly configured.

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| L3 while aiming | Press to toggle | Scope interaction / hold breath | `Left Shift` toggle |
| LT | Regular | Tool secondary action | Right Mouse |
| LT | Regular | Inject another player | Right Mouse |
| LT | Tap | Light right melee attack | Right Mouse |
| LT | Hold | Heavy right melee attack | Right Mouse held |
| LT | Hold | Underarm throw | Right Mouse held |
| LT | Hold while moving Right Stick | Orbit inventory camera | Right Mouse held + Mouse |
| RT | Regular | Tool primary action | Left Mouse |
| RT | Tap | Light left melee attack | Left Mouse |
| RT | Hold | Heavy left melee attack | Left Mouse held |
| RT | Hold | Overarm throw | Left Mouse held |
| LT + RT | Hold both | Block melee attacks | Right Mouse + Left Mouse held |
| LB | Regular while looting | Toggle weapon attachments | `Q` press/release |
| D-pad Right | Hold | Open loot screen | `I` held |
| R3 | Regular | Interaction focus | Middle Mouse |
| A | Hold | Climb ledge / activate jump thrusters | `Space` held |

L3 toggles Left Shift. Press L3 again to release sprint or breath holding.

## Right trackpad contextual actions

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| Right Trackpad ↑ | Scroll | Increase movement speed | Mouse Wheel Up |
| Right Trackpad ↓ | Scroll | Decrease movement speed | Mouse Wheel Down |
| Right Trackpad ↑ | Scroll | Increase tractor-beam distance | Mouse Wheel Up |
| Right Trackpad ↓ | Scroll | Decrease tractor-beam distance | Mouse Wheel Down |
| Right Trackpad ↑ | Scroll | Zoom in (view / interaction) | Mouse Wheel Up |
| Right Trackpad ↓ | Scroll | Zoom out (view / interaction) | Mouse Wheel Down |

## EVA controls

Use **FPS Mode** for EVA. These rows describe inputs available in that mode.

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| Left Stick Y | Move | Strafe forward / backward | `W` / `S` |
| Left Stick X | Move | Strafe left / right | `A` / `D` |
| L3 | Press to toggle | Boost | `Left Shift` toggle |
| Right Stick | Move | Look / turn | Mouse |
| A | Hold | Strafe up / launch from a surface | `Space` held |
| B | Hold after Long Press activates | Strafe down | `Left Ctrl` held |

[Back to README](../../README.md)
