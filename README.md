# Hardware Prototype Coach

A skill for a coding agent (Claude Code, Codex and similar) that helps a person with no hardware experience invent a physical object they want, see it, get editable CAD, test one real physical constraint, change one thing and see what breaks, and leave with an honest record of what exists.

It was made for a 50-minute session of the AI Natives meetup on 18 November 2026. No parts and no 3D printer are needed. The idea for the session came from Anthropic's write-up on [electronics design with Claude](https://www.anthropic.com/research/claude-electronics-design).

## Use it

1. Clone this repository and open a new agent session in its folder. The agent needs to create files and run Python.
2. Paste this, and add your idea if you have one:

```text
Read skills/hardware-prototype-coach/SKILL.md and use that process to help
me invent and make my own digital prototype of a physical object. I am new
to hardware design. We have about 50 minutes. Start with a short
conversation about what I would like to make. If I do not know yet, help me
choose an idea. Show visual concepts first and help me find an object that
I want to make. Do not go straight to CAD. Create files in the folder
my-prototype.
```

[START-HERE.md](START-HERE.md) is the participant handout, in Russian, with the same prompt.

## What is inside

- `skills/hardware-prototype-coach/SKILL.md` - the process the agent follows.
- `skills/hardware-prototype-coach/references/` - tool recipes (CadQuery, Diode `pcb`, quick physical estimates, images from an image API, an interactive model page), redesign cards, the step from checked CAD to a printable sample, fabrication options, parts and power (real envelopes, pin and bus budget, runtime, heat), and a bill of materials with cost.
- `reference/` - a finished example, a desk timer: enclosure source, STEP and STL exports, a small circuit, a behaviour replay and its passport.

## What it does and does not establish

The skill separates these outcomes and asks the agent to say which one was reached: CAD was generated; geometry was checked; a circuit compiled; a layout was routed; behaviour was replayed; a service quoted the files; a physical object was built and tested.

Everything in this repository stops before the last one. The checks are computed on declared volumes and simple estimates. They are not a physical test, a simulation or a manufacturability review.

## Status

The skill was rehearsed with two agents on macOS and run once end to end on a real idea, through a printable sample and an instant quote from a print service. Lessons from that run are in the references. Windows was not tested. Service capabilities and prices in `references/fabrication.md` carry the date they were read and will go stale.

## License

MIT. See [LICENSE](LICENSE).
