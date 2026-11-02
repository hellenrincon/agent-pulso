import numpy as np
from PIL import Image, ImageFilter
B=np.asarray(Image.open('/home/user/pulso-agentes/dashboard/canva/post7-sutil.png').convert('RGB')).astype(np.float32)
H,W,_=B.shape
r,g,b=B[...,0],B[...,1],B[...,2]
yy,xx=np.mgrid[0:H,0:W]
# stream mask
smask=((xx>535)&(xx<680)&(yy>190)&(yy<800)&(r>110)&(r>b+45)&(r>g+15)).astype(np.float32)
smask=np.asarray(Image.fromarray((smask*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)/255
# coffee layer mask in glass
lum0=0.3*r+0.59*g+0.11*b
cmask=(((xx>285)&(xx<815)&(yy>775)&(yy<1190)&(r>g*1.04)&(r-b>12)&(r<235))|((xx>320)&(xx<780)&(yy>790)&(yy<1180)&(lum0<75))).astype(np.float32)
cmask=np.asarray(Image.fromarray((cmask*255).astype('uint8')).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32)/255
# matcha colour from below
m=B[1150:1350,400:700].reshape(-1,3).mean(0)
lum=(0.3*r+0.59*g+0.11*b)[...,None]
matcha=np.clip(m*(0.9+lum/255*0.25),0,255)
A=B*(1-cmask[...,None])+matcha*cmask[...,None]
# remove stream: horizontal interpolation per row
A2=A.copy()
for y in range(190,800):
    row=smask[y]; idx=np.where(row>0.05)[0]
    if len(idx)==0: continue
    x0,x1=idx.min()-3,idx.max()+3
    L=A[y,x0];R=A[y,x1]; t=np.linspace(0,1,x1-x0)[:,None]
    fill=L*(1-t)+R*t
    a=smask[y,x0:x1][:,None]
    A2[y,x0:x1]=A[y,x0:x1]*(1-a)+fill*a
A=A2
fps=30;N=240
rng=np.random.default_rng(1)
noise=np.asarray(Image.fromarray((rng.random((H//8,W//8))*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(np.float32)/255
ytop,ybot=775,1190
for f in range(N):
    t=f/fps
    # stream extent
    front=190+ (min(t,0.6)/0.6)*(800-190)
    tail=190 if t<6.0 else 190+min((t-6.0)/0.5,1)*(800-190)
    sm=smask*((yy<front)&(yy>=tail))
    # flowing texture
    shift=int((t*900)%600)
    Bs=np.roll(B,shift,axis=0)
    strm=B*0.6+Bs*0.4
    strm=np.where((np.roll(smask,shift,axis=0)>0.3)[...,None],strm,B)
    # coffee reveal top-down
    p=np.clip((t-0.5)/5.0,0,1)
    edge=ytop+p*(ybot-ytop+60)+ (noise-0.5)*40
    rev=np.clip((edge-yy)/25,0,1)
    cm=cmask*rev
    frame=A*(1-cm[...,None])+B*cm[...,None]
    frame=frame*(1-sm[...,None])+strm*sm[...,None]
    Image.fromarray(np.clip(frame,0,255).astype('uint8')).save(f'pour/f{f:03d}.png')
print('ok')
