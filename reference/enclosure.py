"""Generate editable CAD and check nominal component envelopes. Units: mm."""
import argparse
import json
import math
from pathlib import Path

import cadquery as cq
from cadquery import exporters

ROOT = Path(__file__).resolve().parent


def box(w, d, h, x=0, y=0, z=0):
    return cq.Workplane("XY").box(w, d, h, centered=(True, True, False)).translate((x, y, z)).val()


def cylinder(r, h, x=0, y=0, z=0):
    return cq.Workplane("XY").circle(r).extrude(h).translate((x, y, z)).val()


def build(p):
    c = p["case"]
    w, d, h, t, floor, lt = (c[k] for k in ("width", "depth", "height", "wall", "floor", "lid"))
    outer = cq.Workplane("XY").box(w, d, h, centered=(True, True, False)).edges("|Z").fillet(3).val()
    cavity = cq.Workplane("XY").box(w-2*t, d-2*t, h, centered=(True, True, False)).edges("|Z").fillet(1).translate((0, 0, floor)).val()
    body = outer.cut(cavity)
    # The connector opening is a planning envelope, not a measured plug model.
    usb_access = box(12, 10.6, 6.6, -w/2, -8, 2.2)
    body = body.cut(usb_access)
    m, b = p["controller"], p["carrier"]
    # Supports touch board undersides; support holes still need a retention choice.
    for x in (m["x"]-6, m["x"]+6):
        for y in (m["y"]-6, m["y"]+6):
            body = body.fuse(cylinder(1.8, m["z"]-floor, x, y, floor))
    board = box(b["width"], b["depth"], b["thickness"], b["x"], b["y"], b["z"])
    for x in (-16, 16):
        for y in (3, 17):
            body = body.fuse(cylinder(2, b["z"]-floor, x, y, floor))
            board = board.cut(cylinder(1.2, 3, x, y, b["z"]-0.5))
            body = body.cut(cylinder(0.8, b["z"]-floor+1, x, y, floor))
    lid = cq.Workplane("XY").box(w, d, lt, centered=(True, True, False)).edges("|Z").fillet(3).translate((0, 0, h)).val()
    gap = c["lip_clearance"]
    lip = box(w-2*t-2*gap, d-2*t-2*gap, 2, z=h-2)
    lip = lip.cut(box(w-2*t-2*gap-2.4, d-2*t-2*gap-2.4, 4, z=h-3))
    lid = lid.fuse(lip)
    for x in p["leds"]["xs"]:
        lid = lid.cut(cylinder(p["leds"]["aperture_diameter"]/2, lt+4, x, p["leds"]["y"], h-2))
    bt = p["button"]
    lid = lid.cut(cylinder(bt["hole_diameter"]/2, lt+4, bt["x"], bt["y"], h-2))
    parts = {
        "controller": box(m["width"], m["depth"], m["height"], m["x"], m["y"], m["z"]),
        "carrier": board,
        "button-body": cylinder(bt["body_diameter"]/2, bt["body_height"], bt["x"], bt["y"], h-12),
        "button-neck": cylinder(6, lt+2, bt["x"], bt["y"], h-2),
        "button-cap": cylinder(8, 2, bt["x"], bt["y"], h+lt),
        "button-nut": cylinder(bt["nut_diameter"]/2, bt["nut_height"], bt["x"], bt["y"], h-2).cut(cylinder(6.1, bt["nut_height"]+2, bt["x"], bt["y"], h-3)),
        "header-J1": box(3, 13.2, 7, -11, 10, b["z"]-7),
        "header-J2": box(3, 5.6, 7, 11, 5, b["z"]-7),
    }
    for i, x in enumerate(p["leds"]["xs"]):
        parts[f"led-{i}"] = box(3.2, 1.6, 0.8, x, p["leds"]["y"], b["z"]+b["thickness"])
    return body, lid, parts, usb_access


def volume_intersection(a, b):
    return sum(s.Volume() for s in a.intersect(b).Solids())


def checks(p, body, lid, parts, usb_access):
    out = []
    def record(name, ok, measured, unit):
        out.append({"name": name, "passed": bool(ok), "measured": measured, "unit": unit})
    for name, s in {"body": body, "lid": lid}.items():
        record(name+"-valid-solid", s.isValid() and len(s.Solids()) == 1, len(s.Solids()), "solids")
    record("body-lid-interference", volume_intersection(body, lid) < 1e-5, round(volume_intersection(body, lid), 6), "mm3")
    record("usb-opening-clear", volume_intersection(body, usb_access) < 1e-5, round(volume_intersection(body, usb_access), 6), "mm3")
    for name, s in parts.items():
        for case_name, shell in (("body", body), ("lid", lid)):
            v = volume_intersection(s, shell)
            record(name+"-clear-of-"+case_name, v < 1e-5, round(v, 6), "mm3")
    # Internal parts can overlap even when both clear the enclosure.
    objects=list(parts.items())
    for i,(name,s) in enumerate(objects):
        for other_name,other in objects[i+1:]:
            v=volume_intersection(s,other)
            record(name+"-clear-of-"+other_name,v < 1e-5,round(v,6),"mm3")
    # Collision alone misses a component entirely outside a too-small case.
    c = p["case"]
    for name in (n for n in parts if n not in ("button-neck", "button-cap")):
        bb = parts[name].BoundingBox()
        margins = [bb.xmin+c["width"]/2-c["wall"], c["width"]/2-c["wall"]-bb.xmax,
                   bb.ymin+c["depth"]/2-c["wall"], c["depth"]/2-c["wall"]-bb.ymax]
        record(name+"-inside-cavity-xy", min(margins) >= 0, round(min(margins), 3), "mm clearance")
        z_margin=min(bb.zmin-c["floor"], c["height"]-bb.zmax)
        record(name+"-inside-cavity-z",z_margin >= -1e-6,round(z_margin,3),"mm clearance")
    insertion_gap=p["button"]["hole_diameter"]-p["button"]["body_diameter"]
    record("button-body-fits-through-panel",insertion_gap > 0,round(insertion_gap,3),"mm diameter clearance")
    return out


def render(body, lid, parts, p, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(12, 8), dpi=150, facecolor="#0c1725")
    ax = fig.add_subplot(111, projection="3d", facecolor="#0c1725")
    items = [(body, "#71bdc2", 1), (lid.translate((0, 0, 18)), "#c9d6e4", 0.94)]
    palette = ["#ed7068", "#e8bc66", "#81c7a1"]
    for name, shape in parts.items():
        color = "#235756" if name in ("controller", "carrier") else "#283244"
        if name.startswith("led-"):
            color = palette[int(name[-1])]
        items.append((shape, color, 1))
    all_triangles, all_colors = [], []
    import numpy as np
    light=np.array([0.5,-0.7,0.8]);light=light/np.linalg.norm(light)
    for shape, color, alpha in items:
        vertices, faces = shape.tessellate(0.15, 0.2)
        v = [a.toTuple() for a in vertices]
        triangles = [[v[i] for i in f] for f in faces]
        all_triangles.extend(triangles)
        rgb=np.array(matplotlib.colors.to_rgb(color))
        for triangle in triangles:
            a,b,c=(np.array(p) for p in triangle)
            normal=np.cross(b-a,c-a);length=np.linalg.norm(normal)
            brightness=0.5+0.5*abs(float(np.dot(normal/length,light))) if length else 0.6
            all_colors.append((*np.clip(rgb*brightness,0,1),1))
    poly = Poly3DCollection(all_triangles, facecolors=all_colors, linewidths=0, shade=False)
    ax.add_collection3d(poly)
    ax.set(xlim=(-45,45), ylim=(-29,29), zlim=(0,52))
    ax.set_box_aspect((90,58,52))
    ax.view_init(elev=38, azim=-58)
    ax.set_axis_off()
    fig.text(0.075,0.91,"Desk Timer",color="#f0f5fc",fontsize=28,weight="bold")
    fig.text(0.075,0.855,"EDITABLE CAD  /  NOMINAL COMPONENT ENVELOPES",color="#91adbf",fontsize=10)
    fig.text(0.075,0.08,f'Case: {p["case"]["width"]} × {p["case"]["depth"]} × {p["case"]["height"]+p["case"]["lid"]} mm · button cap adds 2 mm',color="#f0f5fc",fontsize=15)
    fig.text(0.075,0.042,"Digital design study · fit checks are not a physical assembly test",color="#91adbf",fontsize=10)
    plt.subplots_adjust(left=0.08,right=1,bottom=0.1,top=0.85)
    fig.savefig(out/"enclosure.png",facecolor=fig.get_facecolor())
    for text in fig.texts: text.set_visible(False)
    fig.savefig(out/"enclosure-model.png", facecolor=fig.get_facecolor(), bbox_inches=ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()))
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width",type=float)
    parser.add_argument("--output",type=Path,default=ROOT/"output")
    parser.add_argument("--no-render",action="store_true")
    args=parser.parse_args()
    p=json.loads((ROOT/"design.json").read_text())
    if args.width is not None: p["case"]["width"]=args.width
    args.output.mkdir(parents=True,exist_ok=True)
    body,lid,parts,usb_access=build(p)
    results=checks(p,body,lid,parts,usb_access)
    shapes=[body,lid,*parts.values()]
    bounds=[s.BoundingBox() for s in shapes]
    overall=[max(getattr(b,axis+'max') for b in bounds)-min(getattr(b,axis+'min') for b in bounds) for axis in ('x','y','z')]
    report={"units":"mm", "basis":"nominal envelope checks; see design.json evidence", "assembly_dimensions_mm":[round(x,3) for x in overall], "passed":all(x["passed"] for x in results), "checks":results}
    (args.output/"fit-report.json").write_text(json.dumps(report,indent=2)+"\n")
    failed=[x for x in results if not x['passed']]
    margins=sorted((x for x in results if x['name'].endswith('inside-cavity-xy')),key=lambda x:x['measured'])[:3]
    summary=["# Проверка номинальной геометрии", "",f"Результат: {sum(x['passed'] for x in results)} из {len(results)} проверок.",f"Общий габарит с кнопкой: {' × '.join(str(round(x,2)) for x in overall)} мм.", ""]
    summary += [f"- Не прошло: {x['name']} — {x['measured']} {x['unit']}." for x in failed]
    summary += [f"- Зазор: {x['name']} — {x['measured']} мм." for x in margins]
    summary += ["", "Это проверка заданных объёмов. Реальные детали и способ сборки ещё требуют проверки."]
    (args.output/"fit-summary.md").write_text('\n'.join(summary)+'\n')
    marker=args.output/'DO-NOT-PRINT.txt'
    if failed:marker.write_text('Generated by enclosure.py: this variant failed geometric checks. Do not send these exports for printing. Read fit-summary.md.\n')
    elif marker.exists() and marker.read_text().startswith('Generated by enclosure.py:'):marker.unlink()
    prefix='' if report['passed'] else 'FAILED-'
    for name,s in (("body",body),("lid",lid)):
        exporters.export(s,str(args.output/(prefix+name+".step")))
        exporters.export(s,str(args.output/(prefix+name+".stl")),tolerance=0.05,angularTolerance=0.1)
    assembly=cq.Assembly()
    assembly.add(body,name="body")
    assembly.add(lid,name="lid")
    for name,s in parts.items():assembly.add(s,name=name)
    assembly.save(str(args.output/(prefix+"assembly.step")))
    if not args.no_render:render(body,lid,parts,p,args.output)
    print(json.dumps({"passed":report["passed"], "passed_checks":sum(x["passed"] for x in results), "total_checks":len(results),"output":str(args.output)}))
    raise SystemExit(0 if report["passed"] else 1)


if __name__=="__main__":main()
