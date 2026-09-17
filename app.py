from hashlib import sha256
from threading import RLock
from flask import Flask, jsonify, request
app=Flask(__name__)
class CountMinSketch:
 def __init__(self,width=1024,depth=5):
  if width<=0 or depth<=0: raise ValueError('width and depth must be positive')
  self.width,self.depth=width,depth; self.table=[[0]*width for _ in range(depth)]; self.total=0; self.lock=RLock()
 def _indexes(self,value):
  d=sha256(value.encode()).digest(); h1=int.from_bytes(d[:8],'big'); h2=int.from_bytes(d[8:16],'big') or 1
  for r in range(self.depth): yield r,(h1+r*h2)%self.width
 def add(self,value,count=1):
  if not isinstance(value,str) or not value: raise ValueError('value must be a non-empty string')
  if not isinstance(count,int) or isinstance(count,bool) or count<=0: raise ValueError('count must be a positive integer')
  with self.lock:
   for r,i in self._indexes(value): self.table[r][i]+=count
   self.total+=count
 def estimate(self,value):
  if not isinstance(value,str) or not value: raise ValueError('value must be a non-empty string')
  with self.lock: return min(self.table[r][i] for r,i in self._indexes(value))
 def stats(self):
  with self.lock:
   nz=sum(x>0 for row in self.table for x in row)
   return {'width':self.width,'depth':self.depth,'total_count':self.total,'non_zero_counters':nz,'counters':self.width*self.depth}
sketch=CountMinSketch()
@app.get('/health')
def health(): return jsonify({'status':'ok','service':'count-min-sketch'})
@app.post('/api/events')
def add_event():
 b=request.get_json(silent=True); v=b.get('value') if isinstance(b,dict) else None; c=b.get('count',1) if isinstance(b,dict) else 1
 if not isinstance(v,str) or not v or not isinstance(c,int) or isinstance(c,bool) or c<=0: return jsonify({'error':'non-empty string value and positive integer count are required'}),400
 sketch.add(v,c); return jsonify({'value':v,'added':c,'estimated_count':sketch.estimate(v)}),201
@app.post('/api/events/batch')
def batch():
 b=request.get_json(silent=True); events=b.get('events') if isinstance(b,dict) else None
 if not isinstance(events,list) or not events: return jsonify({'error':'non-empty events list is required'}),400
 try:
  for e in events:
   if not isinstance(e,dict): raise ValueError('each event must be an object')
   sketch.add(e.get('value'),e.get('count',1))
 except ValueError as e: return jsonify({'error':str(e)}),400
 return jsonify({'added_events':len(events),'total_count':sketch.total}),201
@app.get('/api/count/<value>')
def count(value): return jsonify({'value':value,'estimated_count':sketch.estimate(value)})
@app.get('/api/stats')
def stats(): return jsonify(sketch.stats())
if __name__=='__main__': app.run(host='0.0.0.0',port=5000,debug=True)
