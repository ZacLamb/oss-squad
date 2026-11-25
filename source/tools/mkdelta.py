import re,sys,json,difflib,gzip,base64
a=open(sys.argv[1]).read(); b=open(sys.argv[2]).read()
sp=lambda t: re.split(r'(?<=[;,{}>\n])',t)
A=sp(a); B=sp(b)
sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
ops=[[i1,i2,''.join(B[j1:j2])] for tag,i1,i2,j1,j2 in sm.get_opcodes() if tag!='equal']
d=base64.b64encode(gzip.compress(json.dumps(ops).encode(),9)).decode()
open(sys.argv[3],'w').write(d); print(len(ops),'ops',len(d),'b64 chars')
