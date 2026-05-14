# keycleaner · keyboard lock for cleaning

> a tiny macOS utility that locks your keyboard and mouse so you can actually clean them without firing off 47 slack messages to your boss.

---

## table of contents

- [overview](#overview)
- [features](#features)
- [getting started](#getting-started)
- [usage](#usage)
- [technical notes](#technical-notes)
- [license](#license)

---

## overview

**keycleaner** is a single Python script that intercepts and blocks all keyboard and mouse input at the system level, giving you a clean window to wipe down your peripherals without your computer doing anything about it. no GUI, no installer, no fuss.

to unlock, hold both shift keys together for 5 seconds. that's it. that's the whole app.

---

## features

- blocks all keyboard input while active — keys, modifiers, the works
- blocks mouse input too — clicks, scrolls, drags
- simple two-shift-key unlock sequence with a live countdown
- zero dependencies beyond one pip install
- single script, under 100 lines

---

## getting started

### prerequisites

- macOS (uses the Quartz event tap API — sorry, Windows people)
- Python 3 (if it's not already on your mac then you must not have a real mac)
- accessibility permission for your terminal app

### install dependency

```bash
pip3 install pyobjc-framework-Quartz
```

### grant accessibility access

keycleaner needs to intercept system-level input events, which requires explicit permission.

`System Settings > Privacy & Security > Accessibility` → enable your terminal app

without this, the script will tell you so and exit cleanly.

### run it

```bash
python3 keycleaner.py
```

---

## usage

### locking

run the script. your keyboard and mouse are now locked. clean away.

```
==================================================
  keyboard and mouse LOCKED for cleaning
  hold BOTH SHIFT keys for 5 seconds to unlock
==================================================
```

### unlocking

hold the left shift and right shift keys simultaneously. a countdown will appear:

```
both shifts held; keep holding...
  5...
  4...
  3...
  2...
  1...

unlocked
```

if you release early, it tells you and resets. no drama.

---

## technical notes

- **event tap** — uses `CGEventTapCreate` via Quartz to intercept events at the session level before they reach any application
- **blocked events** — keydown, keyup, flags changed, mouse moved, all mouse buttons, scroll wheel, and mouse drags
- **unlock detection** — monitors `kCGEventFlagsChanged` events for left shift (keycode 56) and right shift (keycode 60) held simultaneously
- **tap keepalive** — re-enables the tap automatically if it times out (`kCGEventTapDisabledByTimeout`)
- **countdown thread** — runs in a daemon thread so it exits cleanly when the run loop stops

---

## license

[MIT](LICENSE)

---

<p align="center">built for people who eat at their desks.</p>
