# python -m pubsub.publisher

from google.cloud import pubsub_v1
import json
import sys
import time
import os

if len(sys.argv) != 2:
    print("email address is required")
    sys.exit(1)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
project_id = "secretsantaesame"

request_topic_id = "secretsanta"
response_subscription_id = "subricevidestinatario"

email = sys.argv[1]
timestamp = time.time_ns()

# --------------------------------------------------
# SUBSCRIBER (PRIMA!)
# --------------------------------------------------
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    project_id, response_subscription_id
)



def callback(msg):
    print("Messaggio ricevuto RAW:", msg.data)

    data = json.loads(msg.data.decode("utf-8"))

    # correlation tramite timestamp
    if data.get("timestamp") == timestamp:
        print("Messaggio decodificato:", data)
        msg.ack()
        done = True
    else:
        # messaggio non mio → ack e ignora
        msg.ack()


subscriber.subscribe(subscription_path, callback=callback)

# --------------------------------------------------
# PUBLISH REQUEST (DOPO)
# --------------------------------------------------
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, request_topic_id)

message = {
    "email": email,
    "timestamp": timestamp
}

future = publisher.publish(
    topic_path,
    json.dumps(message).encode("utf-8")
)

print("Richiesta inviata, message id:", future.result())

# --------------------------------------------------
# WAIT FOR RESPONSE
# --------------------------------------------------
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Interrotto dall'utente")
