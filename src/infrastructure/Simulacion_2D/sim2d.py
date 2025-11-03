from __future__ import annotations
import time
from collections import deque
from heapq import heappush, heappop
from typing import Dict, List, Optional, Tuple
import pygame
pygame.init()

#colores para entorno
LG = (230,230,230)
BK = (20,20,20)
BL = (60,120,220)
WH = (255,255,255)
YL = (240,200,0)
B0 = (40,40,40)
B1 = (70,70,70)
BT = (235,235,235)
TX = (30,30,30)
TG = (20,120,20)

#colores para robots
RC = [(220,40,40),(34,177,76),(255,127,39),(163,73,164),(255,0,255),
      (0,162,232),(185,122,87),(255,201,14),(0,200,128)]

#parametros del sistema
GW, GH = 28, 18  #tamaño del mapa
MG = 2
FPS = 60
MAX_TPS = 50
MAX_SS = 50
LPW = 210
RPW = 280
GAP = 8


V2 = Tuple[int,int]
St = Tuple[int,int,int]

def manh(a: V2, b: V2) -> int: return abs(a[0]-b[0])+abs(a[1]-b[1])
def clamp(v, lo, hi): return lo if v<lo else hi if v>hi else v

class Grid:
    def __init__(self, w:int, h:int):
        self.w, self.h = w, h
        self.g = [[0 for _ in range(w)] for _ in range(h)]
        for x in range(w): self.g[0][x]=1; self.g[h-1][x]=1
        for y in range(h): self.g[y][0]=1; self.g[y][w-1]=1
        cx, cy = w//2, h//2
        for y in range(cy-2, cy+2):
            for x in range(cx-2, cx+2):
                self.g[y][x]=1
        for y in range(3, h-3, 6):
            for x in range(1, w-1):
                if self.g[y][x]==1 and not (cy-2<=y<cy+2 and cx-2<=x<cx+2):
                    self.g[y][x]=0
    def inb(self,x,y): return 0<=x<self.w and 0<=y<self.h
    def free(self,x,y): return self.g[y][x]==0
    def set_obs(self,x,y,obs:bool):
        if x in (0,self.w-1) or y in (0,self.h-1): return
        self.g[y][x]=1 if obs else 0
    def nei(self,x,y):
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if self.inb(nx,ny) and self.free(nx,ny): yield nx,ny

class Resv:
    def __init__(self):
        self.cell:Dict[St,str]={}
        self.edge:Dict[Tuple[int,V2,V2],str]={}
        self.stat:Dict[Tuple[int,int],str]={}
        self.goal:Dict[Tuple[int,int],str]={}
        self.sta: Dict[Tuple[int,int],str]={}
    def set_goal(self,x,y,r): self.goal[(x,y)]=r
    def set_start(self,x,y,r): self.sta[(x,y)]=r
    def occ(self,x,y,r): self.stat[(x,y)]=r
    def clr_dyn(self): self.cell.clear(); self.edge.clear()
    def clr_all(self):
        self.cell.clear(); self.edge.clear(); self.stat.clear()
        self.goal.clear(); self.sta.clear()
    def cell_ok(self,t,x,y,r):
        if (x,y) in self.goal and self.goal[(x,y)]!=r: return False
        if (x,y) in self.sta  and self.sta[(x,y)] !=r: return False
        if (x,y) in self.stat and self.stat[(x,y)]!=r: return False
        return (t,x,y) not in self.cell
    def edge_ok(self,t,a,b): return (t,b,a) not in self.edge
    def hold(self,r,px:List[St]):
        for i in range(len(px)):
            t,x,y=px[i]
            self.cell[(t,x,y)]=r
            if i>0:
                t0,x0,y0=px[i-1]
                self.edge[(t0,(x0,y0),(x,y))]=r
    def prune(self,tmin:int):
        if tmin<=0: return
        self.cell={k:v for k,v in self.cell.items() if k[0]>=tmin}
        self.edge={k:v for k,v in self.edge.items() if k[0]>=tmin}

def _astar_once(g:Grid, s:V2, d:V2, rs:Resv, rid:str, t0:int, lim:int)->List[St]:
    if not (g.free(*s) and g.free(*d)): return []
    st:St=(t0,s[0],s[1])
    Q:List[Tuple[int,St]]=[]; heappush(Q,(0,st))
    prev:Dict[St,Optional[St]]={st:None}
    gc:Dict[St,int]={st:0}
    def H(x:St)->int: _,xx,yy=x; return manh((xx,yy),d)
    while Q:
        _,cur=heappop(Q); t,x,y=cur
        if (x,y)==d:
            out:deque[St]=deque(); z=cur
            while z is not None: out.appendleft(z); z=prev[z]
            ext=min(3, lim-out[-1][0])
            for k in range(1,ext+1):
                tt,gx,gy=out[-1]; out.append((tt+k,gx,gy))
            return list(out)
        if (t-t0)>=lim: continue
        nt=t+1
        if rs.cell_ok(nt,x,y,rid):
            ns=(nt,x,y); c=gc[cur]+1
            if ns not in gc or c<gc[ns]:
                gc[ns]=c; prev[ns]=cur; heappush(Q,(c+H(ns),ns))
        for nx,ny in g.nei(x,y):
            if not rs.cell_ok(nt,nx,ny,rid): continue
            if not rs.edge_ok(t,(x,y),(nx,ny)): continue
            ns=(nt,nx,ny); c=gc[cur]+1
            if ns not in gc or c<gc[ns]:
                gc[ns]=c; prev[ns]=cur; heappush(Q,(c+H(ns),ns))
    return []

def astar(g:Grid, s:V2, d:V2, rs:Resv, rid:str, t0:int=0)->List[St]:
    base=manh(s,d)+32
    mx=max(256, g.w*g.h*8)
    lim=base
    while lim<=mx:
        p=_astar_once(g,s,d,rs,rid,t0,lim)
        if p: return p
        lim*=2
    return _astar_once(g,s,d,rs,rid,t0,mx)

class Robot:
    def __init__(self, rid:str, col:Tuple[int,int,int], sp:float=6.0):
        self.id=rid; self.c=col; self.sp=sp
        self.s:Optional[V2]=None; self.d:Optional[V2]=None
        self.is0:Optional[V2]=None; self.id0:Optional[V2]=None
        self.p:Optional[V2]=None
        self.path:List[St]=[]; self.pi=0
        self.m="IDLE"; self.wait=0.0
        self.cy=0; self.ud=0
    def plan(self, tgt:V2, g:Grid, rs:Resv, t0:int)->bool:
        assert self.p is not None
        self.path=astar(g,self.p,tgt,rs,self.id,t0); self.pi=0
        if self.path: rs.hold(self.id,self.path); return True
        return False
    def step(self, tick:int):
        if not self.path or self.pi>=len(self.path): return
        tn,x,y=self.path[self.pi]
        if tick>=tn: self.p=(x,y); self.pi+=1
    def at(self, cell:V2)->bool: return self.p is not None and self.p==cell

class Toast:
    def __init__(self): self.msg=""; self.until=0.0
    def show(self,m:str,sec:float=1.5): self.msg=m; self.until=time.perf_counter()+sec
    def draw(self, surf:pygame.Surface, f:pygame.font.Font):
        if time.perf_counter()>self.until or not self.msg: return
        t=f.render(self.msg,True,(255,255,255)); pad=8
        r=pygame.Rect(12,12,t.get_width()+2*pad,t.get_height()+2*pad)
        pygame.draw.rect(surf,TG,r,border_radius=6); surf.blit(t,(r.x+pad,r.y+pad))

class UI:
    def __init__(self, g:Grid, cs:int, m:int=MG):
        self.g=g; self.cs=cs; self.m=m
        inf=pygame.display.Info(); sw,sh=inf.current_w,inf.current_h
        self.surf=pygame.display.set_mode((sw,sh))
        pygame.display.set_caption("Sim 2D")
        b=18 if sw>=1280 else 16 if sw>=1024 else 14
        self.f=pygame.font.SysFont("consolas",b); self.s=pygame.font.SysFont("consolas",max(12,b-2))
        self.lp=pygame.Rect(0,0,LPW,self.surf.get_height())
        self.rp=pygame.Rect(self.surf.get_width()-RPW,0,RPW,self.surf.get_height())
        self.cr=pygame.Rect(self.lp.right+GAP,0,self.surf.get_width()-LPW-RPW-2*GAP,self.surf.get_height())
        self.gw=self.g.w*(self.cs+MG); self.gh=self.g.h*(self.cs+MG)
        self.go=(self.cr.x+(self.cr.w-self.gw)//2, self.cr.y+(self.cr.h-self.gh)//2)
        self.ctrl:Dict[str,pygame.Rect]={}; self._layout()
        self.layer=pygame.Surface((self.gw,self.gh)); self.need=True
        self.cache:Dict[str,Tuple[str,pygame.Surface]]={}; self.toast=Toast()

    def _txt(self,k,s,f,c):
        p=self.cache.get(k)
        if p and p[0]==s: return p[1]
        r=f.render(s,True,c); self.cache[k]=(s,r); return r
    def _mk(self,k,w,h): self.ctrl[k]=pygame.Rect(0,0,w,h)

    def _layout(self):
        def en(k,w,h): 
            if k not in self.ctrl: self._mk(k,w,h)
        for k in ("btn_start","btn_reset","btn_close"): en(k,180,44)
        for k in ("lbl_desc","btn_desc_minus","box_desc","btn_desc_plus",
                  "lbl_carg","btn_carg_minus","box_carg","btn_carg_plus",
                  "lbl_oper","btn_oper_minus","box_oper","btn_oper_plus",
                  "lbl_robots","btn_rob_minus","box_rob","btn_rob_plus",
                  "lbl_move","btn_move_minus","box_move","btn_move_plus",
                  "lbl_speed","btn_spd_minus","box_spd","btn_spd_plus"):
            w = 120 if k in ("lbl_move","lbl_speed") else (90 if k=="lbl_robots" else (64 if "box" in k else 28))
            h = 22 if k.startswith("lbl_") else 28
            en(k,w,h)

        lp=self.lp; sp=12
        th=self.ctrl["btn_start"].h+sp+self.ctrl["btn_reset"].h+sp+self.ctrl["btn_close"].h
        y=lp.y+(lp.h-th)//2
        for k in ("btn_start","btn_reset","btn_close"):
            r=self.ctrl[k]; r.x=lp.x+(lp.w-r.w)//2; r.y=y; y+=r.h+sp

        rp=self.rp; x=rp.x+14; gap=10
        gh=22+4+28+gap; groups=6; ch=groups*gh-gap; y=rp.y+(rp.h-ch)//2
        def line(a,b,c,d):
            nonlocal x,y
            rl=self.ctrl[a]; rl.x=x; rl.y=y; rl.w=160; y+=rl.h+4
            r1=self.ctrl[b]; rb=self.ctrl[c]; r2=self.ctrl[d]
            r1.x=x; r1.y=y; rb.x=r1.right+6; rb.y=y; r2.x=rb.right+6; r2.y=y
            y+=rb.h+gap
        line("lbl_desc","btn_desc_minus","box_desc","btn_desc_plus")
        line("lbl_carg","btn_carg_minus","box_carg","btn_carg_plus")
        line("lbl_oper","btn_oper_minus","box_oper","btn_oper_plus")
        line("lbl_robots","btn_rob_minus","box_rob","btn_rob_plus")
        line("lbl_move","btn_move_minus","box_move","btn_move_plus")
        line("lbl_speed","btn_spd_minus","box_spd","btn_spd_plus")
        self.labels={"lbl_desc":"Tiempo de Descarga (seg)","lbl_carg":"Tiempo de Carga (seg)","lbl_oper":"Tiiempo de Operación (seg)",
                     "lbl_robots":"Cantidad de Robots","lbl_move":"Velocidad Robot (pasos/seg)","lbl_speed":"Velocidad de sistema"}

    def _btn(self,k,txt,hv):
        r=self.ctrl[k]; pygame.draw.rect(self.surf,B1 if hv else B0,r,border_radius=8)
        t=self.f.render(txt,True,BT); self.surf.blit(t,(r.x+(r.w-t.get_width())//2,r.y+(r.h-t.get_height())//2))
    def _sbtn(self,k,txt,hv):
        r=self.ctrl[k]; pygame.draw.rect(self.surf,(60,60,60) if hv else (50,50,50),r,border_radius=6)
        t=self.s.render(txt,True,BT); self.surf.blit(t,(r.x+(r.w-t.get_width())//2,r.y+(r.h-t.get_height())//2))
    def _box(self,k,txt):
        r=self.ctrl[k]; pygame.draw.rect(self.surf,WH,r,border_radius=6)
        pygame.draw.rect(self.surf,(130,130,130),r,width=1,border_radius=6)
        t=self._txt("box_"+k,txt,self.s,(20,20,20))
        self.surf.blit(t,(r.x+(r.w-t.get_width())//2,r.y+(r.h-t.get_height())//2))
    def _lab(self,k):
        r=self.ctrl[k]; t=self._txt("lab_"+k,self.labels[k],self.s,TX); self.surf.blit(t,(r.x,r.y))

    def build_layer(self):
        self.layer.fill(WH)
        for y in range(self.g.h):
            for x in range(self.g.w):
                c=LG if self.g.g[y][x]==0 else BK
                cx=x*(self.cs+MG); cy=y*(self.cs+MG)
                pygame.draw.rect(self.layer,c,(cx,cy,self.cs,self.cs),border_radius=3)
        self.need=False

    def overlay(self, lines:List[str], title="Aviso"):
        o=pygame.Surface(self.surf.get_size(),flags=pygame.SRCALPHA); o.fill((0,0,0,140)); self.surf.blit(o,(0,0))
        b=pygame.Rect(80,80,self.surf.get_width()-160,self.surf.get_height()-160)
        pygame.draw.rect(self.surf,WH,b,border_radius=10); pygame.draw.rect(self.surf,(120,120,120),b,width=2,border_radius=10)
        y=b.y+20; self.surf.blit(self.f.render(title,True,(10,10,10)),(b.x+20,y)); y+=36
        for ln in lines: self.surf.blit(self.s.render(ln,True,(20,20,20)),(b.x+20,y)); y+=22
        self.surf.blit(self.s.render("Pulsa una tecla o clic para continuar",True,(60,60,60)),(b.x+20,b.bottom-40))
        pygame.display.flip()

    def draw(self, rs:Resv, ro:List['Robot'], idx:int, mode:str,
             t_desc:int,t_carg:int,t_oper:int,t_elapsed:float,
             nrob:int, move:int, spd:int):
        self.surf.fill((245,245,248))
        pygame.draw.rect(self.surf,(235,235,240),self.lp)
        pygame.draw.rect(self.surf,(235,235,240),self.rp)
        if self.need: self.build_layer()
        self.surf.blit(self.layer,self.go)

        eff=move*spd
        st=f"Modo: {mode} | Restante: {max(0,t_oper-int(t_elapsed))} s | Avance: {eff} pasos/seg"
        ts=self.s.render(st,True,TX)
        sx=self.cr.x+(self.cr.w-ts.get_width())//2
        sy=max(8,self.go[1]-24)
        self.surf.blit(ts,(sx,sy))

        m=pygame.mouse.get_pos()
        for k,t in (("btn_start","Iniciar simulación"),("btn_reset","Reiniciar"),("btn_close","Cerrar")):
            self._btn(k,t,self.ctrl[k].collidepoint(m))

        for k in ("lbl_desc","lbl_carg","lbl_oper","lbl_robots","lbl_move","lbl_speed"): self._lab(k)
        for k,t in (("btn_desc_minus","−"),("btn_desc_plus","+"),
                    ("btn_carg_minus","−"),("btn_carg_plus","+"),
                    ("btn_oper_minus","−"),("btn_oper_plus","+"),
                    ("btn_rob_minus","−"),("btn_rob_plus","+"),
                    ("btn_move_minus","−"),("btn_move_plus","+"),
                    ("btn_spd_minus","−"),("btn_spd_plus","+")):
            self._sbtn(k,t,self.ctrl[k].collidepoint(m))
        self._box("box_desc",str(t_desc))
        self._box("box_carg",str(t_carg))
        self._box("box_oper",str(t_oper))
        self._box("box_rob", str(nrob))
        self._box("box_move",str(move))
        self._box("box_spd", str(spd))

        def c2p(xc:int,yc:int)->Tuple[int,int]:
            return (self.go[0]+xc*(self.cs+MG), self.go[1]+yc*(self.cs+MG))

        for r in ro:
            if r.s is not None:
                x,y=c2p(*r.s); pygame.draw.rect(self.surf,BL,(x,y,self.cs,self.cs),border_radius=3)
            if r.d is not None:
                x,y=c2p(*r.d); pygame.draw.rect(self.surf,BL,(x,y,self.cs,self.cs),border_radius=3)

        for i,r in enumerate(ro):
            pos=r.p if mode=="RUNNING" and r.p is not None else r.s
            if pos is None: continue
            x,y=c2p(*pos); pygame.draw.rect(self.surf,r.c,(x,y,self.cs,self.cs),border_radius=3)
            if i==idx and mode=="SETUP":
                pygame.draw.rect(self.surf,YL,(x,y,self.cs,self.cs),width=2,border_radius=3)

        for (sx,sy) in list(rs.sta.keys())+list(rs.goal.keys()):
            x,y=c2p(sx,sy)
            pygame.draw.rect(self.surf,(255,120,120),(x,y,self.cs,self.cs),width=2,border_radius=3)

        self.toast.draw(self.surf,self.s)

def mouse_cell(px:Tuple[int,int], go:Tuple[int,int], cs:int, mg:int, gw:int, gh:int)->Optional[V2]:
    mx,my=px; gx,gy=go; w=gw*(cs+mg); h=gh*(cs+mg)
    if not (gx<=mx<gx+w and gy<=my<gy+h): return None
    rx,ry=mx-gx,my-gy
    return int(rx//(cs+mg)), int(ry//(cs+mg))

class Sim:
    def __init__(self, n=3):
        self.n=n; self.td=5; self.tc=5; self.to=60
        self.mv=1; self.ss=1
        self.reset(False)

    def _cell(self)->int:
        inf=pygame.display.Info(); sw,sh=inf.current_w,inf.current_h
        uw=sw-LPW-RPW-2*GAP; uh=sh
        swc=(uw-(self.g.w-1)*MG)//self.g.w
        shc=(uh-(self.g.h-1)*MG)//self.g.h
        return clamp(min(int(swc),int(shc)),10,48)

    def _robots(self,new_n:int):
        new_n=clamp(new_n,1,len(RC))
        if not hasattr(self,"r"): self.r=[]
        cur=len(self.r)
        if new_n>cur:
            for i in range(cur,new_n): self.r.append(Robot(f"R{i+1}",RC[i]))
        else:
            self.r=self.r[:new_n]
        self.n=new_n

    def reset(self, keep:bool):
        if keep and hasattr(self,"g"):
            self.rs=Resv(); self.ck=pygame.time.Clock()
            self.md="SETUP"; self.tk=0; self.el=0.0; self.acc=0.0
            for i,r in enumerate(self.r):
                r.id=f"R{i+1}"; r.s=r.is0; r.d=r.id0
                r.p=None; r.path=[]; r.pi=0; r.m="IDLE"; r.wait=0.0; r.cy=0; r.ud=0
            cs=self._cell(); self.ui=UI(self.g,cs)
            self.sel=0; self.drag=False; self.add=True
            return
        self.g=Grid(GW,GH)
        self.r=[Robot(f"R{i+1}",RC[i%len(RC)]) for i in range(self.n)]
        self.rs=Resv(); cs=self._cell(); self.ui=UI(self.g,cs)
        self.ck=pygame.time.Clock(); self.md="SETUP"; self.tk=0; self.el=0.0; self.acc=0.0
        self.sel=0; self.drag=False; self.add=True

    def _adj_s(self, attr:str, d:int): setattr(self,attr,max(0,getattr(self,attr)+d))
    def _adj_mv(self,d:int): self.mv=clamp(self.mv+d,1,MAX_TPS)
    def _adj_ss(self,d:int): self.ss=clamp(self.ss+d,1,MAX_SS)
    def _adj_n(self,d:int):
        if self.md!="SETUP": return
        self._robots(self.n+d)

    def _panel_clicks(self, ev:pygame.event.Event):
        if ev.type!=pygame.MOUSEBUTTONDOWN: return
        mods=pygame.key.get_mods(); step=5 if (mods & pygame.KMOD_SHIFT) else 1
        p=ev.pos; c=self.ui.ctrl; hit=lambda k: c[k].collidepoint(p)
        if   hit("btn_desc_minus"): self._adj_s("td",-step)
        elif hit("btn_desc_plus"):  self._adj_s("td",+step)
        elif hit("btn_carg_minus"): self._adj_s("tc",-step)
        elif hit("btn_carg_plus"):  self._adj_s("tc",+step)
        elif hit("btn_oper_minus"): self._adj_s("to",-step)
        elif hit("btn_oper_plus"):  self._adj_s("to",+step)
        elif hit("btn_rob_minus"):  self._adj_n(-1)
        elif hit("btn_rob_plus"):   self._adj_n(+1)
        elif hit("btn_move_minus"): self._adj_mv(-step)
        elif hit("btn_move_plus"):  self._adj_mv(+step)
        elif hit("btn_spd_minus"):  self._adj_ss(-step)
        elif hit("btn_spd_plus"):   self._adj_ss(+step)

    def _setup_mouse(self, ev:pygame.event.Event):
        if ev.type==pygame.MOUSEBUTTONDOWN:
            if self.ui.ctrl["btn_start"].collidepoint(ev.pos):
                self.ui.toast.show("Iniciando…"); self._try_start(); return
            if self.ui.ctrl["btn_reset"].collidepoint(ev.pos):
                self.ui.toast.show("Reiniciando…"); self.reset(True); return
            if self.ui.ctrl["btn_close"].collidepoint(ev.pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT)); return
        self._panel_clicks(ev)

        if ev.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION,pygame.MOUSEBUTTONUP):
            cell=mouse_cell(ev.pos,self.ui.go,self.ui.cs,MG,self.g.w,self.g.h)
            if cell is None:
                if ev.type==pygame.MOUSEBUTTONUP: self.drag=False
                return
            gx,gy=cell
            if not self.g.inb(gx,gy):
                if ev.type==pygame.MOUSEBUTTONUP: self.drag=False
                return
            mods=pygame.key.get_mods()
            left=(ev.buttons[0] if ev.type==pygame.MOUSEMOTION else (ev.button==1))
            right=(ev.buttons[2] if ev.type==pygame.MOUSEMOTION else (ev.button==3))
            if ev.type==pygame.MOUSEBUTTONDOWN and right:
                self.drag=True; self.add=not (mods & pygame.KMOD_SHIFT)
            if ev.type==pygame.MOUSEBUTTONUP and ev.button==3: self.drag=False
            if self.drag and ev.type in (pygame.MOUSEMOTION,pygame.MOUSEBUTTONDOWN):
                oc=any((r.s==(gx,gy)) or (r.d==(gx,gy)) for r in self.r)
                if not oc:
                    self.g.set_obs(gx,gy,self.add); self.ui.need=True
                return
            if ev.type==pygame.MOUSEBUTTONDOWN and left:
                r=self.r[getattr(self,"sel",0)]
                if mods & pygame.KMOD_SHIFT:
                    if self.g.free(gx,gy): r.d=(gx,gy)
                else:
                    if self.g.free(gx,gy): r.s=(gx,gy)

    def _wait(self, lines:List[str], title="Aviso"):
        self.ui.overlay(lines,title=title)
        w=True
        while w:
            for ev in pygame.event.get():
                if ev.type in (pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN,pygame.QUIT):
                    w=False; break

    def _try_start(self):
        for r in self.r:
            if r.s is None:
                self._wait([f"{r.id} sin inicio.","Asigna inicio (clic) y destino (Shift+clic)."],"Falta configuración")
                return
            if r.d is None: r.d=r.s
        for r in self.r:
            r.is0=r.s; r.id0=r.d; r.p=r.s; r.m="TO_GOAL"; r.wait=0.0; r.cy=0; r.ud=0

        self.rs.clr_all()
        sc:Dict[Tuple[int,int],str]={}; gc:Dict[Tuple[int,int],str]={}; ds,dd=[],[]
        for r in self.r:
            sx,sy=r.s; self.rs.set_start(sx,sy,r.id)
            gx,gy=r.d; self.rs.set_goal(gx,gy,r.id)
            if (sx,sy) in sc and sc[(sx,sy)]!=r.id: ds.append(r.id)
            else: sc[(sx,sy)]=r.id
            if (gx,gy) in gc and gc[(gx,gy)]!=r.id: dd.append(r.id)
            else: gc[(gx,gy)]=r.id
        if ds or dd:
            ln=[]; 
            if ds: ln.append("Starts duplicados: "+", ".join(sorted(set(ds))))
            if dd: ln.append("Goals duplicados: "+", ".join(sorted(set(dd))))
            self._wait(ln+["No se inició."],"Conflictos"); return

        def dist(rr:Robot)->int: return manh(rr.p,rr.d)
        for r in sorted(self.r,key=dist,reverse=True):
            if not r.plan(r.d,self.g,self.rs,self.tk):
                self._wait([f"{r.id} sin ruta a destino."],"Plan fallido"); return

        self.md="RUNNING"; self.el=0.0; self.acc=0.0; self.ui.toast.show("OK")

    def _run_mouse(self, ev:pygame.event.Event):
        if ev.type==pygame.MOUSEBUTTONDOWN:
            if self.ui.ctrl["btn_reset"].collidepoint(ev.pos):
                self.ui.toast.show("Reiniciando…"); self.reset(True)
            if self.ui.ctrl["btn_close"].collidepoint(ev.pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        self._panel_clicks(ev)

    def _key(self, ev:pygame.event.Event):
        if ev.type!=pygame.KEYDOWN: return
        if self.md=="SETUP":
            if pygame.K_1<=ev.key<=pygame.K_9:
                i=ev.key-pygame.K_1
                if 0<=i<len(self.r): self.sel=i; self.ui.toast.show(f"R{i+1}")
            if ev.key==pygame.K_s: self._try_start()
        if ev.key==pygame.K_ESCAPE: pygame.event.post(pygame.event.Event(pygame.QUIT))

    def run(self):
        run=True; self.sel=0
        while run:
            dt=self.ck.tick(FPS)/1000.0
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT: run=False
                if ev.type in (pygame.KEYDOWN,): self._key(ev)
                if self.md=="SETUP": self._setup_mouse(ev)
                else: self._run_mouse(ev)

            if self.md=="RUNNING":
                tps=float(self.mv)*float(self.ss)
                iv=1.0/max(1.0,tps)
                self.acc+=dt
                mx=200
                k=int(self.acc/iv)
                if k>mx: k=mx
                self.acc-=k*iv
                for _ in range(k):
                    self.tk+=1
                    for r in self.r: r.step(self.tk)
                if self.tk%200==0: self.rs.prune(self.tk-3)

                sc=float(self.ss); tdt=dt*sc; self.el+=tdt
                if self.el>=self.to:
                    ln=["Resultados:"]
                    tot=0
                    for r in self.r: ln.append(f"{r.id}: {r.ud} descargas"); tot+=r.ud
                    ln.append(f"TOTAL: {tot}")
                    self._wait(ln,"Fin"); self.reset(True)

                for r in self.r:
                    if r.m=="TO_GOAL" and r.at(r.d):
                        r.m="UNLOADING"; r.wait=float(self.td); self.rs.occ(r.d[0],r.d[1],r.id)
                    elif r.m=="UNLOADING":
                        r.wait-=tdt
                        if r.wait<=0:
                            r.ud+=1
                            if not r.plan(r.s,self.g,self.rs,self.tk):
                                self._wait([f"{r.id} sin ruta a inicio.","Volviendo a SETUP."],"Aviso")
                                self.reset(True); break
                            r.m="TO_START"
                    elif r.m=="TO_START" and r.at(r.s):
                        r.m="LOADING"; r.wait=float(self.tc); self.rs.occ(r.s[0],r.s[1],r.id)
                    elif r.m=="LOADING":
                        r.wait-=tdt
                        if r.wait<=0:
                            if not r.plan(r.d,self.g,self.rs,self.tk):
                                self._wait([f"{r.id} sin ruta a destino.","Volviendo a SETUP."],"Aviso")
                                self.reset(True); break
                            r.m="TO_GOAL"; r.cy+=1

            self.ui.draw(self.rs,self.r,getattr(self,"sel",0),self.md,self.td,self.tc,self.to,
                         getattr(self,"el",0.0),self.n,self.mv,self.ss)
            pygame.display.flip()
        pygame.quit()

#Parametros de inicio
def make_demo(n=3)->Sim: return Sim(n)
