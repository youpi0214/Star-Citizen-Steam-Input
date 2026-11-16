# Flight Mode

Flight Mode is used for both **ships and ground vehicles**. It places movement controls on the sticks/triggers and uses the trackpads for targeting and vehicle systems. Ship-specific actions apply when piloting a ship.

See [quick controls and input notation](../../README.md#quick-controls) for shared controls, and [required game setup](../game-settings.md#required-in-game-bindings) for custom bindings.

Hold **L4 (`M1`)** for mining, salvage, and secondary controls. Hold **L5** for advanced flight controls. Release either button to leave its modifier layer.

## Visual reference sheets

- [Flight Mode — Base Controls](../../templates/steam-controller-2026-flight-base-controls.svg): general vehicle actions across base, L4, and L5.
- [Flight Mode — Mining and Salvage](../../templates/steam-controller-2026-flight-mining-and-salvage.svg): profession actions and supporting vehicle controls across all layers.

The sheets group actions by gameplay context, not by modifier. Each entry identifies the input and any required L4/L5 hold.

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
| RB | Hold in quantum mode | Engage Quantum Drive | Left Mouse held |
| R5 | Regular | Cycle mouse mode (custom in-game bind; see [QoL settings](../game-settings.md)) | `.` |
| L5 | Hold | Hold L5 Modifier layer | Steam Input Action Set Layer |
| R3 | Regular | Next weapon preset | Mouse Wheel Down |
| A | `[H]` | NAV / Combat toggle | `B` |
| B | Regular | Spacebrake | `X` |
| X | Regular | Cycle operator mode | Middle Mouse |
| X | `[2]`; hold second press to charge | Ping | `Tab` |
| Y | Regular | VTOL | `K` |
| Y | `[2]` | Hold interaction | `F` toggle/hold equivalent |
| Y | `[H]` | Exit seat | `Y` |
| D-pad Down | Regular | Landing gear | `N` |
| D-pad Down | `[H]` | Autoland | `N` held |

For charged ping, hold the second **X** press. **Freelook** uses **M1 + R3** as a toggle; press again to disable it.

Holding **RB** holds the regular Left Mouse binding. Star Citizen uses that hold to engage Quantum Drive in quantum mode; no separate Steam Input Long Press activator is needed. Likewise, holding **D-pad Down** holds `N` for Autoland without a separate Long Press activator.

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
| M1 + X | Regular | Switch mining laser | Left Alt + Left Mouse |
| M1 + LB | Regular | Decoy | `H` |
| M1 + RB | Regular | Noise | `J` |
| M1 + R3 | Regular | Freelook toggle (press again to disable) | `Z` |
| M1 + Right Stick Touch | `[2]` | LAMP | `Right Alt + L` |
| M1 + D-pad Up | Regular | Camera view | `F4` |
| M1 + D-pad Left | Regular | Toggle chat | `F12` |
| M1 + D-pad Down | Regular | Request landing | `Left Alt + N` |
| M1 + BACK | Regular | Accept invite | `[` |
| M1 + START | Regular | Decline invite | `]` |

### L4 — Right trackpad: mining modules and power

Hold L4 while using the right trackpad. Scrolling adjusts mining laser power or salvage beam spacing, depending on the active operator mode.

| Trackpad input | Action | Output |
| --- | --- | --- |
| ↑ | Increase mining power | Mouse Wheel Up |
| ↓ | Decrease mining power | Mouse Wheel Down |
| ← | Activate mining module 1 | `Left Alt + 1` |
| Center click | Activate mining module 2 | `Left Alt + 2` |
| → | Activate mining module 3 | `Left Alt + 3` |

### L4 — Left trackpad: salvage tools and aim mode

Hold L4 while using the left trackpad.

| Trackpad input | Action | Output |
| --- | --- | --- |
| ↑ | Fire fracture tool | `Right Alt + W` |
| ↓ | Fire disintegration tool | `Right Alt + S` |
| ← | Fire left salvage tool | `Right Alt + A` |
| → | Fire right salvage tool | `Right Alt + D` |
| Center click | Cycle aim mode | `Right Alt + G` |

## Flight — L5 modifier: advanced flight controls

Hold L5 while using the right trackpad.

| Trackpad input | Action | Output |
| --- | --- | --- |
| ↑ | Increase speed limiter | Left Alt + Mouse Wheel Up |
| ↓ | Decrease speed limiter | Left Alt + Mouse Wheel Down |
| Center click | Toggle cruise control | `Left Alt + C` |

## Combat, quantum, and scanning contexts

These actions reuse the same physical outputs in different vehicle modes. Hold **L4 (`M1`)** for every M1 row.

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| LB | `[2]` | Increase armed missile count | `G` |
| M1 + LB | Hold | Set and launch decoy burst | `H` held |
| RB | Tap | Launch missiles | Left Mouse |
| RB | Tap in quantum mode | Request quantum jump | Left Mouse |
| RB | Hold in scanning mode | Activate scanning | Left Mouse held |
| R3 | Regular | Next missile type | Mouse Wheel Down |
| R3 | Regular in scanning mode | Decrease scanning angle | Mouse Wheel Down |
| Right Trackpad ↑ | Hold | Toggle auto-targeting | `T` held |
| M1 + Right Trackpad ↑ | Scroll | Previous weapon preset / missile type | Mouse Wheel Up |
| M1 + Right Trackpad ↓ | Scroll | Next weapon preset / missile type | Mouse Wheel Down |
| M1 + Right Trackpad ↑ | Scroll | Increase scanning angle | Mouse Wheel Up |
| M1 + Right Trackpad ↓ | Scroll | Decrease scanning angle | Mouse Wheel Down |
| M1 + Right Trackpad ↑ | Scroll | Zoom in | Mouse Wheel Up |
| M1 + Right Trackpad ↓ | Scroll | Zoom out | Mouse Wheel Down |
| M1 + Right Trackpad ← | Regular | Pin / unpin target slot 1 | `Left Alt + 1` |
| M1 + Right Trackpad Center | Click | Pin / unpin target slot 2 | `Left Alt + 2` |
| M1 + Right Trackpad → | Regular | Pin / unpin target slot 3 | `Left Alt + 3` |
| B | Regular | Release throttle trim | `X` |

## Ground vehicle contexts

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| LT | Regular | Drive backward | `S` |
| RT | Regular | Drive forward | `W` |
| M1 + Left Stick X | Move | Steer left / right | `A` / `D` |
| Left Stick ↑ | Move | Horn | `Space` |
| M1 + A | Regular | Toggle auto-braking on idle | `C` |
| B | Hold | Brake | `X` held |

L3 also provides ground-vehicle boost through the existing Left Shift binding.

## Turret contexts

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| LT | Regular | Change turret position | `S` |
| Left Stick ← | Move | Cycle turret mouse mode | `Q` |
| Left Stick → | Move | Toggle stabilization | `E` |
| M1 + Left Stick ← | Move | Previous remote turret | `A` |
| M1 + Left Stick → | Move | Next remote turret | `D` |
| M1 + A | Hold | Recenter turret | `C` held |
| Y | `[H]` | Exit remote turret | `Y` |

The unmodified left-stick Q/E outputs control turret modes here; they do not steer the turret. L5 speed-limiter scrolling also applies to turret speed.

## Inventory and focus contexts

Double-press **Y** to toggle the existing F interaction hold. Double-press again to release it.

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| Left Trackpad ↓ | Regular during interaction | Inventory | `I` |
| Left Trackpad ↓ | Hold during interaction | Loot screen | `I` held |
| X | Regular | Interaction focus | Middle Mouse |

## Mining, salvage, and tractor-beam contexts

| Control | Input | Action | Output |
| --- | --- | --- | --- |
| LB | Regular in salvage mode | Cycle focused salvage modifiers | Right Mouse |
| LB | `[2]` in salvage mode | Toggle salvage gimbal | `G` |
| RB | Tap or hold in mining mode | Fire mining laser | Left Mouse |
| RB | Tap or hold in salvage mode | Fire focused salvage tool | Left Mouse |
| R3 | Regular in mining mode | Decrease mining laser power | Mouse Wheel Down |
| R3 | Regular in salvage mode | Decrease salvage beam spacing | Mouse Wheel Down |
| R3 | Regular with tractor beam | Decrease tractor-beam distance | Mouse Wheel Down |
| M1 + Right Trackpad ↑ | Scroll | Increase tractor-beam distance | Mouse Wheel Up |
| M1 + Right Trackpad ↓ | Scroll | Decrease tractor-beam distance | Mouse Wheel Down |
| M1 + Right Trackpad ↑ | Scroll in salvage mode | Increase salvage beam spacing | Mouse Wheel Up |
| M1 + Right Trackpad ↓ | Scroll in salvage mode | Decrease salvage beam spacing | Mouse Wheel Down |

[Back to README](../../README.md)
