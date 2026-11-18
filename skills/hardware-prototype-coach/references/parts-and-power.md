# Parts, electronics budget and power

These notes come from one device taken from concept to a printable, fully bought-in layout on 18 November 2026: a sloped desk console with a 4.3-inch display, four mechanical keys with small OLED labels, two microphones and a battery. Adapt them; do not copy their numbers.

## Replace the envelopes that set the size

An assumed envelope unblocks the first CAD view. It should not survive into a printable enclosure for any part that sets the size or the layout: the display, the battery, the largest boards, every connector, and the plug that enters each connector. In that session the real display module was 8.8 mm thick against an assumed 4.0 mm, and a 0.66-inch OLED glass was 18.46 mm wide against an assumed 16.7 mm, which made the planned keycap impossible. Both were found only after four revisions on assumed parts.

- Take outline, thickness, active area, active-area offset and connector positions from the manufacturer's drawing; an active area is often off-centre on the connector side.
- A total thickness from a product page does not say how it splits between glass, board and rear parts; record the split as an assumption.
- Model the plug, not only the receptacle. A right-angle USB-C plug needs roughly 12 mm beyond the board edge; in that session it set the minimum case width.
- Record the part, the source link and the date in the design file next to each dimension.

## Bought parts only

When the person wants every internal part bought ready-made, look for a module that removes a custom part before redesigning the custom part:

- A breakout board with key sockets and its own bus interface replaces a hand-wired key matrix, a key plate and an I/O expander; it also fixes the key pitch (19.05 mm for MX-style boards), which fixes the width of the key row.
- A display board that carries the microcontroller, radio and battery charger replaces three separate modules.
- Standard keycaps cannot hold a display; a display beside or above the key is the bought-in form. A key with a built-in display exists as a single part, at a much higher price.

## Electronics budget

Count before the CAD grows around a choice:

- **Pins.** Free pins on the chosen board against everything wired: keys, audio, displays, buses. An all-in-one display board can leave three to five free pins; a bus expander or a key board with its own interface then carries the keys.
- **Bus addresses.** Identical displays usually share one fixed address, often with at most two choices; a multiplexer separates them. Check the addresses of parts already on the board's bus.
- **Radios.** Many controller modules already have Wi-Fi and Bluetooth; say so before adding a radio module. Keep metal and the battery away from the module's antenna.
- **USB roles.** A single native USB port has a limited number of endpoints; check that the classes you plan (keyboard, serial, audio) fit together.

## Power, runtime and heat

A battery changes the layout and adds a heat budget. Name each number below as an estimate.

- **Runtime:** battery energy in Wh times converter efficiency, divided by the board's power. 3.7 V × 2.5 Ah = 9.25 Wh; × 0.85 / 2.25 W ≈ 3.5 h at full backlight.
- **Heat inside a closed case:** nearly all electrical power ends as heat inside. Surface temperature rise ≈ P / (h × A), with A the outer surface area from the CAD and h about 10 W/m²K for still air (convection plus radiation, assumed). Air inside runs hotter than the surface; a factor of about 2 is a working assumption. Add charger losses while charging: charge power × (1 − efficiency).
- Compare the result with the battery's charging limit, commonly 45 °C for a lithium-polymer cell; read the cell's datasheet. Report the highest room temperature at which the estimate still passes. Local heating at chips is not covered by this estimate; the first physical check is a thermocouple on the battery while it charges with the device running.
- Give the device a defined state when the battery is nearly empty: stop recording, type nothing, ask for the charger, and return when charging starts. Replay that state with the rest of the behaviour.
