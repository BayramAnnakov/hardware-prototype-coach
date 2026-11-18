"""Acceptance replay of pure timer behavior, not a GPIO or hardware test."""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"firmware"))
from timer import Timer

t=Timer(1000)
events=[]
def record(label,mode,remaining):
    assert (t.mode,t.remaining_ms)==(mode,remaining),(label,t.mode,t.remaining_ms)
    assert sum(t.lights()) == 1
    events.append({"event":label,"mode":t.mode,"remaining_ms":t.remaining_ms,"lights":t.lights()})

record("idle", "idle",1000)
t.tap(); t.advance(350); record("start-and-elapse", "running",650)
t.tap(); t.advance(9000); record("pause-freezes-time", "paused",650)
t.tap(); t.advance(650); record("resume-to-exact-deadline", "done",0)
t.tap(); record("restart-after-completion", "running",1000)
t.advance(10000); record("long-step-clamped-at-zero", "done",0)
t.reset(); record("reset", "idle",1000)
try:
    t.advance(-1)
except ValueError:
    events.append({"event":"negative-time-rejected","passed":True})
else:
    raise AssertionError("negative time was accepted")

out=ROOT/"output"
out.mkdir(exist_ok=True)
(out/"behavior-replay.json").write_text(json.dumps({"basis":"pure timer state machine; no GPIO or physical hardware", "passed":True, "events":events},indent=2)+"\n")
print("Behavior replay: 8 acceptance observations passed; GPIO adapter remains untested on hardware.")
