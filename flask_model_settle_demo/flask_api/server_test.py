import json
import requests
import pandas as pd

header = {'Content-Type': 'application/json',
          'Accept': 'application/json'}

df = pd.read_csv('../data/test.csv', encoding="utf-8-sig")
df = df.head()
data = df.to_json(orient='records')

resp = requests.post(
    "http://127.0.0.1:5000/predict",
    data = json.dumps(data),
    headers = header
)
print(resp.status_code)
print(resp.json())
