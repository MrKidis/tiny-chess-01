import os,json,urllib.request,urllib.error
from array import array
V={"P":1,"N":2,"B":3,"R":4,"Q":5,"K":6}
KN=(33,31,18,14,-14,-18,-31,-33);KI=(1,-1,16,-16,15,17,-15,-17,2,-2);BS=(15,17,-15,-17);RS=(1,-1,16,-16)
B=10**6
D=int(os.environ.get("ENGINE_DEPTH","4"))

def P(f):
 b=array('b',[0]*128)
 for r,row in enumerate(f.split()[0].split('/')):
  x=0
  for c in row:
   if c.isdigit(): x+=int(c)
   else: b[16*(7-r)+x]=V[c.upper()]*(1 if c.isupper() else -1); x+=1
 return b

def n(i): return chr(97+i%16)+str(i//16+1)

def g(i,d):
 j=i+d
 return j if 0<=j<128 and 0<=j//16<8 and 0<=j%16<8 else None

def G(b,sd):
 out=[]
 for i,p in enumerate(b):
  if p==0 or (p>0)!=(sd>0): continue
  t=p if p>0 else -p
  if t==1:
   d=16 if p>0 else -16
   j=g(i,d)
   if j and b[j]==0:
    out.append((i,j,'q' if j//16==(7 if p>0 else 0) else ''))
    j2=g(j,d)
    if j2 and b[j2]==0 and i//16==(1 if p>0 else 6): out.append((i,j2,''))
   for e in (g(i,d+1),g(i,d-1)):
    if e and b[e] and (b[e]>0)!=(p>0) and abs(b[e])!=6: out.append((i,e,'q' if e//16==(7 if p>0 else 0) else ''))
  elif t in (2,6):
   for d in (KN if t==2 else KI[:8]):
    j=g(i,d)
    if j and (b[j]==0 or ((b[j]>0)!=(p>0) and abs(b[j])!=6)): out.append((i,j,''))
   if t==6:
    for e in (2,-2):
     j=g(i,e)
     if j and b[i+e//2]==0 and b[j]==0: out.append((i,j,''))
  else:
   for d in (BS if t==3 else RS if t==4 else BS+RS):
    j=g(i,d)
    while j is not None:
     q=b[j]
     if q:
      if (q>0)!=(p>0) and abs(q)!=6: out.append((i,j,''))
      break
     out.append((i,j,'')); j=g(j,d)
 return out

def ic(b,sd):
 try: k=b.index(6 if sd>0 else -6)
 except ValueError: return False
 op=-sd
 for e in (k+15,k+17,k-15,k-17):
  if 0<=e<128 and b[e]==op: return True
 for d in KI[:8]:
  j=g(k,d)
  if j and b[j] and (b[j]>0)!=(sd>0) and abs(b[j]) in (6,2): return True
 for d in BS+RS:
  j=g(k,d)
  while j is not None:
   p=b[j]
   if p:
    if p and (p>0)!=(sd>0) and abs(p) in (3,4,5): return True
    break
   j=g(j,d)
 return False

def ev(b):
 s=0
 for i,p in enumerate(b):
  if p:
   s+=abs(p) if p>0 else -abs(p)
   if abs(p)==1: s+=i//16-1 if p>0 else 6-i//16
 return s

def ab(b,sd,d,a,Bb):
 if d==0: return ev(b)
 best=-B
 for mv in G(b,sd):
  i,j=mv[0],mv[1]
  x=b[i]; c=b[j]
  b[i]=0; b[j]=x
  if ic(b,sd): b[i]=x; b[j]=c; continue
  v=-ab(b,-sd,d-1,-Bb,-a)
  b[i]=x; b[j]=c
  if v>best: best=v; a=v
  if best>=Bb: break
 return best

def bm(b,sd,d):
 bst,bv=None,-B
 for mv in G(b,sd):
  i,j=mv[0],mv[1]
  x=b[i]; b[i]=0; b[j]=x
  if ic(b,sd): b[i]=x; b[j]=0; continue
  v=-ab(b,-sd,d-1,-B,B)
  b[i]=x; b[j]=0
  if v>bv: bv=v; bst=mv
 return bst

def s(u):
 return 16*(int(u[1])-1)+(ord(u[0])-97)

def choose(fen, legal):
 if not legal: return ''
 b = P(fen); sd = 1 if fen.split()[1] == 'w' else -1
 st, bv = legal[0], -B
 for u in legal:
  i, j = s(u[:2]), s(u[2:4])
  x = b[i]; c = b[j]
  b[i] = 0
  b[j] = x
  v = -ab(b, -sd, D - 1, -B, B)
  if len(u) > 4 and x < 0: b[j] = -6
  elif len(u) > 4: b[j] = 6
  b[i] = x
  b[j] = c
  if v > bv:
   bv = v
   st = u
 return st

def post(p,body):
 r=urllib.request.Request(os.environ['MAKEFUN_ENV_URL']+p,data=json.dumps(body).encode(),headers={'content-type':'application/json'})
 with urllib.request.urlopen(r) as x: return json.load(x)

def run():
 g=post('/game',{})
 while True:
  g=post('/game',{})
  if g['status']=='done': break
  while g['status']=='your_move':
   try: g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
   except urllib.error.HTTPError: g=post('/game',{})
 print('done:',g.get('wins'),'won,',g.get('draws'),'drawn,',g.get('losses'),'lost')

if __name__=='__main__': run()
