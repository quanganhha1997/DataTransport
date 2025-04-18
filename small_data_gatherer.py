import requests
import json

vehicle_ids = [2901, 2904]
all_data = []

for vid in vehicle_ids:
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vid}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        all_data.extend(data)
    else:
        print(f"Data not available for VehicleID {vid}")

with open("bcsample.json", "w") as f:
    json.dump(all_data, f, indent=2)
