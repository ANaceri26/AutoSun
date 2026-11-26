#!/bin/bash
# usage: export_build.sh <project_dir> <out_dir> <hand_solder_refs comma list>
P="$1"; O="$2"; HAND="$3"; K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"
"/c/Program Files/KiCad/10.0/bin/python.exe" -c "import pcbnew,sys; b=pcbnew.LoadBoard(sys.argv[1]); pcbnew.ZONE_FILLER(b).Fill(b.Zones()); b.Save(sys.argv[1])" "$P/solar_car.kicad_pcb" 2>/dev/null
if ! "$K" pcb drc --severity-error -o "$O.drc.txt" "$P/solar_car.kicad_pcb" >/dev/null || ! grep -q "Found 0 DRC violations" "$O.drc.txt"; then echo "DRC FAILED - not exporting"; exit 1; fi; rm -f "$O.drc.txt"
rm -rf "$O"; mkdir -p "$O/gerbers"
"$K" pcb export gerbers --layers F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts --subtract-soldermask --no-x2 -o "$O/gerbers/" "$P/solar_car.kicad_pcb" >/dev/null
"$K" pcb export drill --format excellon --drill-origin absolute --excellon-units mm --excellon-separate-th --generate-map --map-format gerberx2 -o "$O/gerbers/" "$P/solar_car.kicad_pcb" >/dev/null
"$K" pcb export pos --format csv --units mm --side front --exclude-dnp -o "$O/pos_raw.csv" "$P/solar_car.kicad_pcb" >/dev/null
"$K" sch export bom --fields "Value,Reference,Footprint,MPN,LCSC,QUANTITY" --labels "Comment,Designator,Footprint,MPN,LCSC Part #,Qty" --group-by "Value,Footprint,MPN" --ref-range-delimiter "" -o "$O/bom_raw.csv" "$P/solar_car.kicad_sch" >/dev/null
"$K" pcb render --side top --width 1000 --height 1125 --quality basic -o "$O/preview_top.png" "$P/solar_car.kicad_pcb" >/dev/null 2>&1
"$K" pcb render --side bottom --width 1000 --height 1125 --quality basic -o "$O/preview_bottom.png" "$P/solar_car.kicad_pcb" >/dev/null 2>&1
python -I - "$O" "$HAND" <<'PY'
import csv, zipfile, os, glob, sys
O=sys.argv[1]; HAND=set(sys.argv[2].split(','))
rows=list(csv.DictReader(open(O+'/bom_raw.csv',encoding='utf-8')))
hand=[]
with open(O+'/BOM_JLCPCB.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Comment','Designator','Footprint','MPN','LCSC Part #'])
    for r in rows:
        refs=[x for x in r['Designator'].split(',') if x]
        jl=[x for x in refs if x not in HAND and not x.startswith('H')]; hs=[x for x in refs if x in HAND]
        if jl: w.writerow([r['Comment'],','.join(jl),r['Footprint'].split(':')[-1],r['MPN'],r['LCSC Part #']])
        if hs: hand.append([r['Comment'],','.join(hs),r['Footprint'].split(':')[-1]])
with open(O+'/YOU_SOLDER_THESE.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Part','Designator','Footprint']); w.writerows(hand)
pos=list(csv.DictReader(open(O+'/pos_raw.csv',encoding='utf-8')))
with open(O+'/CPL_JLCPCB.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
    FIX={'J1':(1.0,0.345),'J5':(1.0,0.345),'J6':(1.0,0.345),'J2':(0.345,-1.0),'J3':(0.345,-1.0)}  # JST-PH: origin is pin 1, JLC wants body centre (offset already rotated)
    for p in pos:
        if p['Ref'] in HAND or p['Ref'].startswith('H'): continue
        x,y=float(p['PosX']),float(p['PosY'])
        if p['Ref'] in FIX: x+=FIX[p['Ref']][0]; y-=FIX[p['Ref']][1]
        w.writerow([p['Ref'],'%.6fmm'%x,'%.6fmm'%y,'Top',p['Rot']])
with zipfile.ZipFile(O+'/gerbers_upload_this.zip','w',zipfile.ZIP_DEFLATED) as z:
    for g in glob.glob(O+'/gerbers/*'): z.write(g,os.path.basename(g))
os.remove(O+'/bom_raw.csv'); os.remove(O+'/pos_raw.csv')
print(O, "BOM lines", sum(1 for _ in open(O+'/BOM_JLCPCB.csv'))-1, "| you solder:", [h[1] for h in hand])
PY
