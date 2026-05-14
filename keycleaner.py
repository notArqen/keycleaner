#!/usr/bin/env python3
"""
keycleaner; blocks your keyboard input so you can actually clean them 🙏
hold BOTH SHIFT keys for 5 seconds to unlock.

if you haven't already, run the following in another terminal:
      pip3 install pyobjc-framework-Quartz

keycleaner also needs accessibility permission (System Settings > Privacy & Security > Accessibility)
"""

import sys
import time
import threading

try:
    import Quartz
except ImportError:
    print("missing dependency. install with:")
    print("  pip3 install pyobjc-framework-Quartz")
    sys.exit(1)

UNLOCK_SECONDS = 5

left_shift_held = False
right_shift_held = False
both_held_since = None
tap_ref = [None]
loop_ref = [None]


def run_countdown(start_time):
    """Background thread: prints countdown and stops the run loop after UNLOCK_SECONDS."""
    last_tick = None
    while True:
        time.sleep(0.05)
        # Abort if shifts were released (both_held_since gets set to None or a new value)
        if both_held_since != start_time:
            return
        elapsed = time.time() - start_time
        remaining = UNLOCK_SECONDS - elapsed
        if remaining <= 0:
            print("\nunlocked", flush=True)
            Quartz.CFRunLoopStop(loop_ref[0])
            return
        # Print 5, 4, 3, 2, 1 once each as the countdown crosses each whole second
        tick = int(remaining) + 1
        if tick != last_tick:
            last_tick = tick
            print(f"  {tick}...", flush=True)


def callback(proxy, event_type, event, refcon):
    global left_shift_held, right_shift_held, both_held_since

    if event_type == Quartz.kCGEventTapDisabledByTimeout:
        if tap_ref[0]:
            Quartz.CGEventTapEnable(tap_ref[0], True)
        return event

    if event_type == Quartz.kCGEventFlagsChanged:
        keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        flags = Quartz.CGEventGetFlags(event)
        is_shift = bool(flags & Quartz.kCGEventFlagMaskShift)

        if keycode == 56:    # Left Shift
            left_shift_held = is_shift
        elif keycode == 60:  # Right Shift
            right_shift_held = is_shift

        if left_shift_held and right_shift_held:
            if both_held_since is None:
                both_held_since = time.time()
                print("\nboth shifts held; keep holding...", flush=True)
                threading.Thread(target=run_countdown, args=(both_held_since,), daemon=True).start()
        else:
            if both_held_since is not None:
                print("(released early; hold both shifts together for 5 seconds)", flush=True)
            both_held_since = None

    # Block all events by returning None
    return None


def main():
    mask = (
        (1 << Quartz.kCGEventKeyDown) |
        (1 << Quartz.kCGEventKeyUp) |
        (1 << Quartz.kCGEventFlagsChanged) |
        (1 << Quartz.kCGEventMouseMoved) |
        (1 << Quartz.kCGEventLeftMouseDown) |
        (1 << Quartz.kCGEventLeftMouseUp) |
        (1 << Quartz.kCGEventRightMouseDown) |
        (1 << Quartz.kCGEventRightMouseUp) |
        (1 << Quartz.kCGEventOtherMouseDown) |
        (1 << Quartz.kCGEventOtherMouseUp) |
        (1 << Quartz.kCGEventScrollWheel) |
        (1 << Quartz.kCGEventLeftMouseDragged) |
        (1 << Quartz.kCGEventRightMouseDragged)
    )

    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        mask,
        callback,
        None,
    )

    if tap is None:
        print("err: could not create event tap.")
        print("grant accessibility access to your terminal app:")
        print("  System Settings > Privacy & Security > Accessibility")
        sys.exit(1)

    tap_ref[0] = tap
    loop_ref[0] = Quartz.CFRunLoopGetCurrent()

    source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    Quartz.CFRunLoopAddSource(loop_ref[0], source, Quartz.kCFRunLoopDefaultMode)
    Quartz.CGEventTapEnable(tap, True)

    print("=" * 50)
    print("  keyboard and mouse LOCKED for cleaning")
    print("  hold BOTH SHIFT keys for 5 seconds to unlock")
    print("=" * 50, flush=True)

    Quartz.CFRunLoopRun()

    Quartz.CGEventTapEnable(tap, False)
    Quartz.CFRunLoopRemoveSource(loop_ref[0], source, Quartz.kCFRunLoopDefaultMode)
    print("keyboard and mouse restored. don't get them greasy again.")


if __name__ == "__main__":
    main()
