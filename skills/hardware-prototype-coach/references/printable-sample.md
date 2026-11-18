# From checked CAD to a printable sample

Checked CAD shows that declared volumes fit. A printable sample is a set of separate solids that a service can make and a person can put together. This list comes from one object taken through that step on 18 November 2026: an 80 mm ball-shaped device shell in five parts, with CadQuery 2.6.1. Adapt it; do not copy its numbers.

## Decide what the sample is for

Say which question the sample answers: how the object looks and feels, whether bought parts fit, or whether a moving part works. Say what it will not have, such as springs, latches, electronics or retention of a loose part. A check that belongs to a later stage is still run and reported. It does not block a sample whose purpose it does not serve, and the report says so.

## What the parts need that checked CAD did not have

- **A wall of even thickness.** Offset the surface along its normal. A wall drawn as a radial or vertical offset becomes thin where the surface slopes: 3 mm drawn was about 1.1 mm at one place.
- **A joint between shells,** and a decision on which shell carries the lip. Put the split where the opening is widest, so that the largest internal part goes in without tilting.
- **Something that holds every internal part:** a seat, posts or rails. A part that passes a collision check can still float in mid-air.
- **An assembly order,** checked step by step: each part must pass through the opening that exists at that step.
- **The rest state of every moving part.** Without its spring, a part rests where gravity, friction and its stops put it; decide that position or state it as an assumption. Check the end positions and the closest poses of each moving part, in each state of the others.
- **Hardware:** pins, screws and nuts, with sizes, in the parts list.
- **One valid solid for each printed part,** exported separately, with the quantity of each. Import each exported file again and compare its size and volume with the report.

## Limits come from the process

Read the accuracy and the minimum wall that the service states for the chosen material, and derive the clearances from them. Two printed parts can each be off by the stated accuracy, so a sliding or push fit needs more than twice that accuracy on diameter. That is a simple stack; a first sample decides whether the fit runs. Accuracy does not give the smallest hole that stays open: read the minimum hole size for the process separately, or record it as unknown. Example values and their source are in [fabrication options](fabrication.md).

## Look before fabrication

Features added for printing change the object: lugs, seams, screw heads, feet. Show the printable parts from the front and from the side the person will see most. A hinge axis decides which face of a flap the viewer sees in each pose. When an image tool is available, an image made from the CAD view shows surface, colour and scale better than a CAD render does; list where it differs from the CAD. Get the person's yes to this object, not to the earlier concept.

## Still unknown after this

The tolerance of the real printed parts, whether supports mark a visible surface, how the joint feels, and anything that depends on a bought part that nobody has measured. Name the first physical measurement.
