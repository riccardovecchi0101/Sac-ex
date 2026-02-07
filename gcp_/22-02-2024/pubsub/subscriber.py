#python -m pubsub.subscriber
from google.cloud import pubsub_v1
from google.cloud.exceptions import NotFound
import json
import sys
import logging

if len(sys.argv) <= 1:
    logging.error("Inserire almeno un cap")
    exit(-1)

caps = sys.argv[1:]


project_id = "umarellcantieriesame"
subscription_id = "sub_cantieri"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def callback(message):
   # print("Messaggio ricevuto RAW:", message.data)
    data = json.loads(message.data.decode("utf-8"))
    cap = data['cap']

    if str(cap) in caps:
        print("Messaggio ricevuto RAW:", message.data)

    message.ack()

subscriber.subscribe(subscription_path, callback=callback)

try:
    print(f"\nIn ascolto sui cap{caps}...\n")
    while True:
        pass
except KeyboardInterrupt:
    print("Chiusura subscriber")
