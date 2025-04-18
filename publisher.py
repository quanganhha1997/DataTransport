import json
import time
from google.cloud import pubsub_v1

project_id = "dataengr-lab-tranquha"
topic_id = "my-topic"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Load data
with open("vehicle_data.json", "r") as f:
    records = json.load(f)

print(f"Publishing {len(records)} records...")

start_time = time.time()
futures = []

def callback(future):
    try:
        future.result() 
    except Exception as e:
        print(f"Publish failed: {e}")

# Publish all messages
for record in records:
    message_data = json.dumps(record).encode("utf-8")
    future = publisher.publish(topic_path, message_data)
    future.add_done_callback(callback)
    futures.append(future)

for future in futures:
    future.result()

end_time = time.time()
print(f"Published {len(records)}records in {end_time - start_time:.2f} seconds.")

