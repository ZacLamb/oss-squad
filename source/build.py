import sys,shutil,os,re,zipfile
import os as _os
ROOT=_os.path.dirname(_os.path.abspath(__file__))
site=(sys.argv[1] if len(sys.argv)>1 else '').rstrip('/')
site=(site+'/') if site else ''
src=ROOT+'/launch'; dist=ROOT+'/dist'
shutil.rmtree(dist,ignore_errors=True); shutil.copytree(src,dist)
shutil.copy(ROOT+'/game2/index.html',dist+'/index.html')
for p in [os.path.join(r,f) for r,_,fs in os.walk(dist) for f in fs if f.endswith('.html') or f in ('robots.txt','sitemap.xml')]:
    s=open(p).read()
    if site: s=s.replace('__SITE__',site)
    else:
        s=s.replace('content="__SITE__og.jpg"','content="og.jpg"').replace('<meta property="og:url" content="__SITE__">','').replace('Sitemap: __SITE__sitemap.xml\n','')
        s=s.replace('__SITE__','')
    open(p,'w').write(s)
if not site: os.remove(dist+'/sitemap.xml')
z=ROOT+'/oss-squad-site.zip'
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zf:
    for r,_,fs in os.walk(dist):
        for f in fs:
            fp=os.path.join(r,f); zf.write(fp,os.path.relpath(fp,dist))
print('built',z,os.path.getsize(z)//1024,'KB site=',site or '(none)')
