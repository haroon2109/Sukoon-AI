import urllib.request
req = urllib.request.Request('http://127.0.0.1:8000/api/verify/text', data=b'{"content":"water is wet"}', headers={'Content-Type': 'application/json'}, method='POST')
try:
    print(urllib.request.urlopen(req).read().decode())
except Exception as e:
    print("Error:", e, e.read().decode() if hasattr(e, 'read') else '')
