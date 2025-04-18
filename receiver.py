import time
from threading import Timer
from google.cloud import pubsub_v1

project_id = "dataengr-lab-tranquha"
subscription_id = "my-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

message_count = 0
start_time = time.time()
timeout = 30  # seconds
timer = None

def stop_streaming():
    print("\nNo new messages for {timeout} seconds. Shutting down subscriber...")
    streaming_pull_future.cancel()

def reset_timer():
    global timer
    if timer:
        timer.cancel()
    timer = Timer(timeout, stop_streaming)
    timer.start()

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global message_count
    message.ack()
    message_count += 1

    if message_count % 10000 == 0:
        print(f"Received {message_count} messages.")

    reset_timer()

# Start receiver
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

reset_timer()  

with subscriber:
    try:
        streaming_pull_future.result()
    except Exception as e:
        pass  

end_time = time.time()
if timer:
    timer.cancel()

total_time = end_time - start_time
print(f"\nTotal messages received: {message_count}")
print(f"Total runtime: {total_time:.2f} seconds")

