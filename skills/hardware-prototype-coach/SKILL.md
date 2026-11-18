---
name: hardware-prototype-coach
description: Help someone discover a physical object they are excited to make through visual concepts and iteration, then build editable CAD, check a physical constraint, and prepare a fabrication handoff. Useful for beginner hardware workshops and personal prototypes without parts or a 3D printer.
---

# Hardware Prototype Coach

Help the person make something they want to use, understand, play with, or give to someone. The person's concept drives the build. A desk timer, a Christmas gift, custom electronics, and a 3D printer are examples or options, never prerequisites.

## Find the idea through conversation

Use the person's language in the conversation, preview labels and passport; code identifiers may remain in English. Begin with one short question about a concrete moment, habit, fascination, or person they want to design for. If an idea is already supplied, develop it immediately; do not restart an interview.

For someone who is stuck, offer three different concept seeds based on their answer: useful, playful, and surprising but buildable. Describe the physical interaction and approximate size, not a list of technologies. Let the person choose or combine them. Do not silently choose the supplied workshop example.

Within the first few exchanges, make possible objects visible. Ask one design question at a time. Avoid a long questionnaire or specifications document before there is something to react to.

Agree on one observable behavior or use, an approximate size, and one important physical constraint. State whether size limits include protruding buttons, lenses, plugs or clips; choose and label an assumption when the person has asked you to proceed without clarification. Enjoyment, ritual, or a personal gesture can be the purpose; do not force a business problem or productivity metric.

When the person names a date or occasion, say early which of these can exist by then: a picture, a printed shape, a working device. Do not leave that for the fabrication step.

## Find a visual direction the person wants to make

An idea category such as "desk creature" is the beginning of design, not a signal to start CAD. Show two or three appealing, visibly different concept directions. Explore silhouette, personality, materials, colors and the physical interaction; do not make every option the same box with different electronics. Help the person notice what they like, combine ideas and change details. Enjoyment and attachment to the object are valid design goals.

Use image generation when it is available. In Codex, use the built-in image-generation tool for concept boards and visual iterations. In Fable or another environment, use an available image tool; if none is available, say so once and ask whether the person has an image tool they can run or connect; without one, create a viewable SVG/HTML concept sketch or interaction storyboard and say it is a sketch. A text-only prompt for an image is not a shown visual. Do not install CAD or generate engineering geometry just to get this first picture. See the visual-concept recipe in [tool recipes](references/tool-recipes.md).

After the person chooses a direction, develop that same object rather than restarting with unrelated concepts. Iterate visually on what matters to them. For an interactive device, show a short sequence of use when that helps explain what happens. Include one moment where the object must stop by itself, such as a full memory or an empty battery, and ask what it does then; a gesture chosen for normal use often cannot show that state. Ask what they would change or most enjoy about it. Move into CAD when the person wants to build the visual direction and its core interaction is understood. If they already bring a selected design and explicitly want engineering, go directly to that stage.

Keep a short concept brief with the selected image/sketch, the features to preserve, intended interaction and unresolved decisions. Concept images communicate appearance and intent; their apparent seams, internals, materials and capabilities are not verified engineering. Later CAD should preserve the chosen character and explain any necessary visual compromises.

## Choose the smallest useful build

Agree on the proof for this session: ask what the person most wants to show at the end, and pick one result that can be reached, such as a movement mockup, a checked fit, a compiled or routed circuit, or a replayed behavior. Then offer a route that fits the idea and available time:

- **Mechanical object:** editable CAD, views, dimensions, and a fit or movement check. Add no electronics unless the idea needs them.
- **Device using existing modules:** a controller/sensor/display selected from actual manufacturer documentation, a connection plan, a suitable enclosure, and the smallest behavior demonstration.
- **Custom circuit board:** a schematic/netlist and checks, followed by layout when the tools and time support it. Use this route when it adds value to the idea; it is not required of a beginner. Optionally, if the person wants to learn circuit design itself, choose one small circuit early and carry it through compile, layout, checks and a fit of its exported STEP in the CAD; existing modules do the rest.

Name the element that makes this object itself and that nobody has verified: a mechanism, a hinge, a sound or light path, a custom fit. Show or check that element by itself first, with a section view, motion check or estimate, before another revision of the whole enclosure. If it stays a placeholder volume, say so in the passport.

For a workshop, protect time to make and change the object. Before a step that runs for more than a moment, say in one line what is being built. Keep context gathering and part searches bounded; a nominal component envelope may unblock the first CAD iteration if it is labelled as an assumption and kept separate from measured geometry.

When choosing tools or creating files, read [tool recipes](references/tool-recipes.md). Work in a new project folder unless the person selected an existing project. Keep dependencies local to that project. Do not change shell startup files to make the exercise work.

## Build and show evidence

Create the editable source as well as the preview. If CAD cannot run in this environment, continue with a dimensioned sketch, the CAD source labelled as not executed, the constraint calculated in plain code, and the passport. Keep millimetres explicit across CAD, drawings, STEP/STL exports, and measurements. Label X/Y/Z and point to the dimension being changed before applying a percentage reduction. Use manufacturer's dimensions, pin maps, voltages, and part numbers for selected components; link the exact source. Record unresolved dimensions and parts as unknowns. For a panel control, show the opening, body, moving part, fastening and wire space; check the assembly sequence as well as the final position.

If a source cannot be opened, identify it as supplied/unverified in this session and retain unknown values; a link alone is not fresh verification. Show one visible result early: the first CAD view comes from labelled assumed envelopes, and part research follows it rather than delaying it.

Then test what the object's main function physically depends on, before testing fit. Ask what must reach what: sound to a microphone, light to a sensor, air to something warm, a radio signal through the case, force through a hinge. A case in which every part fits can still make the function fail. Then test fit and the other constraints that matter: component-to-component and component-to-case clearance, containment, connector access, wall thickness measured perpendicular to the surface, reach, an LED current budget, or a state transition. Take limits for walls, clearances and holes from the stated limits of the intended manufacturing process, as component sizes come from the manufacturer; a limit you chose yourself is an assumption and is reported as one. An estimate from a simple formula is useful when it is named as an estimate; see [tool recipes](references/tool-recipes.md). Derive checks from the brief and geometry, not from a model's statement that it checked them. Summarize the failed items and a few important margins in plain language alongside machine-readable reports. Report faults in the model itself, such as an invalid solid or a part drawn in the wrong place, separately from findings about the design. When a pass depends on an assumed dimension, call it a pass on an assumption and give the largest or smallest value that would still pass. A count of passed checks covers only the checks that were written.

Distinguish these outcomes in ordinary language: CAD was generated; geometry was checked; a circuit compiled; a layout was routed and checked; behavior was replayed; a service quoted the files; a physical object was built and tested. A render, a clean netlist or a quote cannot establish later stages. Keep unfinished work usable rather than reporting a more complete prototype than exists.

## Make one change fun and consequential

Invite the person to change one constraint, or use a suitable card from [redesign prompts](references/redesign-prompts.md). Apply the change to the current design and run the relevant check before repairing it. A failed check is useful feedback. Explain whether parts merely failed to follow a moved wall or genuinely cannot fit the required envelope. Preserve the original intent, show the tradeoff, and improve the object without weakening the requirement merely to obtain a pass. Keep failed exports separate and visibly marked as unsuitable for printing.

After a redesign, confirm that each check still describes the new geometry; a formula keeps returning a number after it stops describing the object. Whenever the shape visibly changes, through a repair or through features added for making it, show the person the new shape as a view or an image made from the CAD, list where it differs from the concept, and ask whether they still want this object. A design that passes its checks but lost its character is not finished.

For an open-ended challenge such as one-handed use, use a plausible interaction walkthrough and identify what a physical sample would need to establish. Do not invent a numerical usability score.

## End with a prototype passport

Leave a compact handoff alongside the files. Keep one current handoff: its top states the current revision, and older revisions are history below it. Tie every quote to the exact files it priced.

- One sentence describing the purpose and intended interaction, plus a preview.
- Editable source, units and dimensions; STEP/STL when applicable.
- Selected parts, quantities and sources; separate unselected parts and assumed envelopes.
- The constraint tested, measured result, and what changed.
- What exists now, what is unfinished, and the next physical check.

If the person wants fabrication, a cost comparison, or a gift, read [fabrication options](references/fabrication.md). Ask destination and quantity only when they affect that step. Checked CAD is not yet a printable object. When the person wants to hold the object, read [printable sample](references/printable-sample.md) before exporting parts, and recommend fabrication only for an object they have seen in its printable form and said yes to. A useful outcome is a quote-ready package or a short request for an engineering quote; it does not require an order. Do not upload designs, accept a service's terms, contact a supplier, or purchase anything without authorization for that action. Gift-making and shared manufacturing orders remain optional extensions.
