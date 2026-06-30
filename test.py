import urllib.request
req = urllib.request.Request('https://sukoon-backend-25172750096.us-central1.run.app/api/verify', data=b'{"content":"water is wet"}', headers={'Content-Type': 'application/json'}, method='POST')
try:
    print(urllib.request.urlopen(req).read().decode())
except Exception as e:
    print("Error:", e, e.read().decode() if hasattr(e, 'read') else '')
