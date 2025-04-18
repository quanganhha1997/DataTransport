import csv
import requests
import json

vehicle_ids = []

with open("vehicle_ids.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:  # non-empty row
            try:
                vid = int(row[0])
                if vid not in vehicle_ids:
                    vehicle_ids.append(vid)
                if len(vehicle_ids) >= 100:
                    break
            except ValueError:
                continue  # skip rows that don't contain valid ints

all_data = []

for vid in vehicle_ids:
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vid}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        all_data.extend(data)
    else:
        print(f"No data available for VehicleID {vid}")

# Save all data
with open("vehicle_data.json", "w") as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} records to vehicle_data.json")
