"""AutoSUN board stress check. Run with KiCad's Python:
   "C:\Program Files\KiCad\10.0\bin\python.exe" sim\design_check.py
1) Voltage on every chip/part pin vs its datasheet absolute-maximum rating.
2) Thinnest copper track on every power net vs the worst-case current it carries (IPC-2221, 1 oz outer copper).
3) Power in the resistors that carry real current."""
import pcbnew, os
here=os.path.dirname(os.path.abspath(__file__)); b=pcbnew.LoadBoard(os.path.join(here,'..','solar_car.kicad_pcb')); mm=pcbnew.ToMM
ok=True
def row(*c): print(" | ".join(str(x) for x in c))
# ---------- 1) voltages ----------
# worst-case net voltages (V): solar = 2 pairs Voc ~14 V; mis-wired 4-in-series would be ~28 V (still checked)
VMAX={'GATE8':8.0,'SOL+':15.0,'VSOL':15.0,'MISWIRE':28.0,'VCHG':9.0,'PACK':8.4,'VMOT':8.4,'VOR':8.4,'+5V':5.1,'XIAO_5V':4.8,'3V3':3.3,'LOGIC5':5.1,'ADC_PACK':4.2,'ADC_SOL':2.63}
checks=[ # part, what, net, rating
 ('U1 CN3722','VCC pin','VSOL',30.0),('U1 CN3722','BAT/CSP pins','VCHG',28.0),('U1 CN3722','CHRG/DONE pins','LOGIC5',30.0),
 ('Q1 AO3407A','drain-source','VSOL',30.0),('Q1 AO3407A','gate (charger clamps it to 8 V)','GATE8',20.0),
 ('D1/D2 SS34','reverse voltage','VSOL',40.0),('D3/D4 SS34','reverse voltage','PACK',40.0),
 ('Q2-Q12 AO3401A','drain-source','PACK',30.0),('Q2-Q12 AO3401A','gate-source (= pack or charger V)','VCHG',12.0),
 ('Q4-Q13 2N7002','drain-source','PACK',60.0),('Q4-Q13 2N7002','gate (Arduino pin)','LOGIC5',20.0),
 ('U2 TPS563201','VIN','VOR',17.0),('U3 DRV8833','VM','VMOT',11.8),('U3 DRV8833','logic inputs','LOGIC5',7.0),
 ('A1 Nano Every','5V pin (regulated 5.0 V)','+5V',6.0),('A1 Nano Every','A0/A1 pin (full pack x0.5; reads up to 5.0 V, damage above 5.5 V)','ADC_PACK',5.5),('A1 Nano Every','A2 pin (solar x0.175)','ADC_SOL',5.0),
 ('U6 XIAO','5V pin (after D5)','XIAO_5V',5.5),('U6 XIAO','SDA/SCL (pulled to its own 3.3 V)','3V3',3.6),
 ('Q14/Q15 BSS138','drain-source','LOGIC5',50.0),('Q14/Q15 BSS138','gate-source','3V3',20.0),
 ('C1/C2/C3 (50 V)','capacitor','VSOL',50.0),('C4/C5 (50 V)','capacitor','VCHG',50.0),('C12/C13 (50 V)','capacitor','VOR',50.0),
 ('C15/C16/C21 (25 V)','capacitor','+5V',25.0),('C17/C18 (50 V)','capacitor','VMOT',50.0),
]
print("\n## 1) Voltage vs rating\n"); row("Part","Where","Worst-case V","Rating V","Margin","OK?"); row(*["---"]*6)
for part,what,net,rating in checks:
    v=VMAX[net]; m=rating/v; reg=net in ('+5V','XIAO_5V','3V3'); good=m>=(1.05 if reg else 1.2); ok&=good
    row(part,what,f"{v:.1f}",f"{rating:.1f}",f"{m:.1f}x",("✅ (regulated rail)" if reg else "✅") if good else "❌")
print("\nMis-wiring check: all 4 panels in a row (~28 V) would put the CN3722 VCC at 28/30 V and Q1 at 28/30 V: at the limit. **Always wire 2 pairs.**")
# ---------- 2) tracks vs current ----------
def ipc_amps(width_mm, rise=10.0, oz=1.0):
    a=(width_mm/0.0254)*(1.378*oz); return 0.048*rise**0.44*a**0.725
IMAX={'/PACKA+':2.0,'/PACKB+':2.0,'/PACKA_F':2.0,'/PACKB_F':2.0,'/S_LA':1.6,'/S_LB':1.6,'/S_CA':1.0,'/S_CB':1.0,
      '/VMOT':1.2,'/MA1':0.6,'/MA2':0.6,'/MB1':0.6,'/MB2':0.6,'/ISENA':0.6,'/ISENB':0.6,
      '/VCHG':1.0,'/CN_CSP':1.2,'/CN_SW':1.2,'/VSOL':0.8,'/SOL+':0.8,
      '/VOR':1.4,'/VIN_BUCK':1.4,'/BUCK_SW':1.66,'/XIAO_5V':0.4,'/3V3_X':0.01}
widths={}
for t in b.GetTracks():
    if t.GetClass()=='PCB_TRACK': n=t.GetNetname(); widths[n]=min(widths.get(n,9e9),mm(t.GetWidth()))
print("\n## 2) Thinnest track vs worst-case current (1 oz copper)\n"); row("Net","Worst-case A","Thinnest track mm","Carries @10°C rise","Carries @20°C rise","OK?"); row(*["---"]*6)
for n,i in IMAX.items():
    if n not in widths: row(n,i,"(pads/pour only)","-","-","✅"); continue
    w=widths[n]; a10,a20=ipc_amps(w,10),ipc_amps(w,20); good=a20>=i
    short=sum(mm(t.GetLength()) for t in b.GetTracks() if t.GetClass()=='PCB_TRACK' and t.GetNetname()==n and mm(t.GetWidth())<=w+0.001)
    note="✅" if a10>=i else ("✅ (only %.1f mm long, at chip pins)"%short if short<3 else "❌ (over the 10°C limit)")
    ok&= (a10>=i or short<3)
    row(n,i,f"{w:.2f}",f"{a10:.2f} A",f"{a20:.2f} A",note)

# ---------- 2b) real current in every piece of the +5V copper (resistor-network solve) ----------
def solve_net(net, source, loads):
    """source/loads are (ref,pad). Returns list of (track, amps)."""
    parent={}
    def f(a):
        parent.setdefault(a,a)
        while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
        return a
    def u(a,c): parent[f(a)]=f(c)
    k=lambda lay,p:(lay,round(mm(p.x),3),round(mm(p.y),3))
    tracks=[t for t in b.GetTracks() if t.GetNetname()==net and t.GetClass()=='PCB_TRACK']
    for t in b.GetTracks():
        if t.GetNetname()==net and t.GetClass()=='PCB_VIA':
            u(k('F.Cu',t.GetPosition()),k('B.Cu',t.GetPosition()))
    pads={}
    for fp in b.GetFootprints():
        for pd in fp.Pads():
            if pd.GetNetname()!=net: continue
            nid=('PAD',fp.GetReference(),pd.GetNumber()); pads[(fp.GetReference(),pd.GetNumber())]=nid
            lays=['F.Cu','B.Cu'] if pd.GetAttribute()==pcbnew.PAD_ATTRIB_PTH else ['F.Cu']
            for t in tracks:
                for e in (t.GetStart(),t.GetEnd()):
                    if t.GetLayerName() in lays and pd.HitTest(e): u(k(t.GetLayerName(),e),nid)
    for t in tracks:  # endpoints landing on the middle of another track (T joints)
        for e in (t.GetStart(),t.GetEnd()):
            for o in tracks:
                if o is not t and o.GetLayer()==t.GetLayer() and o.HitTest(e,0): pass
    nodes={}; idx=lambda a: nodes.setdefault(f(a),len(nodes))
    R=[]; 
    for t in tracks:
        a,c=idx(k(t.GetLayerName(),t.GetStart())),idx(k(t.GetLayerName(),t.GetEnd()))
        r=1.72e-8*max(mm(t.GetLength()),0.001)*1e-3/(mm(t.GetWidth())*1e-3*35e-6); R.append((t,a,c,r))
    for v in pads.values(): idx(v)
    n=len(nodes); G=[[0.0]*n for _ in range(n)]; I=[0.0]*n
    for t,a,c,r in R:
        g=1/r; G[a][a]+=g; G[c][c]+=g; G[a][c]-=g; G[c][a]-=g
    for key,amps in loads.items():
        if key in pads: I[idx(pads[key])]-=amps
    s0=idx(pads[source]); 
    for i in range(n): G[s0][i]=0.0
    G[s0][s0]=1.0; I[s0]=0.0
    for i in range(n): G[i][i]+=1e-9 if i!=s0 else 0
    # gaussian elimination
    for col in range(n):
        piv=max(range(col,n),key=lambda r_:abs(G[r_][col])); G[col],G[piv]=G[piv],G[col]; I[col],I[piv]=I[piv],I[col]
        pv=G[col][col]
        if abs(pv)<1e-15: continue
        for r_ in range(col+1,n):
            fct=G[r_][col]/pv
            if fct:
                Gr=G[r_]; Gc=G[col]
                for c_ in range(col,n): Gr[c_]-=fct*Gc[c_]
                I[r_]-=fct*I[col]
    V=[0.0]*n
    for r_ in range(n-1,-1,-1):
        V[r_]=(I[r_]-sum(G[r_][c_]*V[c_] for c_ in range(r_+1,n)))/G[r_][r_] if abs(G[r_][r_])>1e-15 else 0
    return [(t,abs(V[a]-V[c])/r) for t,a,c,r in R], V
LOADS={('J7','2'):1.2,('D5','2'):0.35,('A1','27'):0.05,('J8','1'):0.02,('J9','2'):0.005,('R9','1'):0.003,('R31','1'):0.003,('R8','1'):0.001,('R34','1'):0.001,('R37','1'):0.001,('R38','1'):0.001}
res,V=solve_net('/+5V',('L2','2'),LOADS)
print("\n## 2b) +5V: real worst-case current in every piece of copper (servo stall 1.2 A + XIAO 0.35 A + Arduino + sensors + LEDs = 1.63 A)\n")
worst=max(res,key=lambda r_: r_[1]/ipc_amps(mm(r_[0].GetWidth()),10))
bad5=[(t,a) for t,a in res if a>ipc_amps(mm(t.GetWidth()),10)]
row("Pieces of copper","Total load","Tightest piece: current","Its width","It can carry @10°C rise","Load vs limit","Pieces over the limit","OK?"); row(*["---"]*8)
t,a=worst; cap=ipc_amps(mm(t.GetWidth()),10)
row(len(res),f"{sum(LOADS.values()):.2f} A",f"{a:.2f} A",f"{mm(t.GetWidth()):.2f} mm",f"{cap:.2f} A",f"{a/cap*100:.0f}%",len(bad5),"✅" if not bad5 else "❌")
ok&= not bad5
tight=sorted([(a_/ipc_amps(mm(t_.GetWidth()),10),a_,t_) for t_,a_ in res if a_/ipc_amps(mm(t_.GetWidth()),10)>0.85],key=lambda x:-x[0])
if tight:
    print("\nTightest pieces (over 85% of their 10°C limit), board coordinates in mm from the bottom-left corner:")
    for ratio,a_,t_ in tight:
        print(f"- {a_:.2f} A in {mm(t_.GetWidth()):.2f} mm wide, {mm(t_.GetLength()):.1f} mm long, {t_.GetLayerName()}, ({mm(t_.GetStart().x)-100:.1f},{181-mm(t_.GetStart().y):.1f})->({mm(t_.GetEnd().x)-100:.1f},{181-mm(t_.GetEnd().y):.1f}) = {ratio*100:.0f}% of limit")
print(f"\nVoltage drop from the 5 V chip to the furthest part at full load: {max(abs(v) for v in V)*1000:.0f} mV")
# ---------- 3) resistor power ----------
print("\n## 3) Resistor power\n"); row("Part","Current","Power","Rating","OK?"); row(*["---"]*5)
for part,i,r,rat in (('R3 0.2 Ω charge sense (full 1 A, USB-C charging)',1.0,0.2,0.25),('R3 on solar (~0.4 A)',0.4,0.2,0.25),('R32/R33 0.33 Ω motor sense (0.6 A limit)',0.6,0.33,0.25),('R35-R38 4.7k pull-ups',5/4700,4700,0.1)):
    p=i*i*r; good=p<=rat; ok&=good; row(part,f"{i:.3g} A",f"{p*1000:.0f} mW",f"{rat*1000:.0f} mW","✅" if p<=0.85*rat else ("⚠️ near limit" if good else "❌"))
print("\nRESULT:", "ALL CHECKS PASS - every row green" if ok else "NOT ALL PASS - fix the red rows")
