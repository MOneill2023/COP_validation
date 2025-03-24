import csv
import requests
import random
import json
import time

submission_id = random.randint(0,100)

with open(r"C:\Users\MatthewOneill\Downloads\books.csv", errors="ignore") as f:
    reader = csv.DictReader(f)
    books =[]

    for row in reader:
        if not all(row):
            continue
        books.append({key.strip(): value for key, value in row.items() if key})
    


jsons = json.dumps(books).encode()
before = time.perf_counter()
response = requests.post(f"http://localhost:8000/books/{submission_id}", data=jsons)
after = time.perf_counter()

print(f"time taken = {after - before}, {response.status_code=}, {response._content}")