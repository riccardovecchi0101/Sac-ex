import json
from google.cloud import pubsub_v1

# METTI QUI IL PROJECT ID VERO
PROJECT_ID = "cantieriumarell"
SUBSCRIPTION_ID = "cantieri-sub"

subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

print("👴 Umarell in ascolto (una pull)...")

response = subscriber.pull(
    request={
        "subscription": sub_path,
        "max_messages": 1
    },
    #timeout=10
)

if not response.received_messages:
    print("Nessun messaggio ricevuto")
else:
    for msg in response.received_messages:
        data = json.loads(msg.message.data.decode("utf-8"))
        print("🚧 Nuovo cantiere ricevuto:")
        print(data)

        subscriber.acknowledge(
            request={
                "subscription": sub_path,
                "ack_ids": [msg.ack_id]
            }
        )
