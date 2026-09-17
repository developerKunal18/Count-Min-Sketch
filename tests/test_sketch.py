import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
import app as m
@pytest.fixture
def client():
 m.sketch=m.CountMinSketch(128,5); m.app.config['TESTING']=True
 with m.app.test_client() as c: yield c
def test_count(client):
 client.post('/api/events',json={'value':'login'}); client.post('/api/events',json={'value':'login','count':2})
 assert client.get('/api/count/login').get_json()['estimated_count']>=3
def test_unknown(client): assert client.get('/api/count/unknown').get_json()['estimated_count']==0
def test_batch(client):
 r=client.post('/api/events/batch',json={'events':[{'value':'click','count':4},{'value':'view','count':2}]}); assert r.status_code==201
def test_invalid(client): assert client.post('/api/events',json={'value':'','count':1}).status_code==400
def test_stats(client):
 client.post('/api/events',json={'value':'a','count':3}); d=client.get('/api/stats').get_json(); assert d['total_count']==3 and d['counters']==640
def test_validation():
 with pytest.raises(ValueError): m.CountMinSketch(0)
