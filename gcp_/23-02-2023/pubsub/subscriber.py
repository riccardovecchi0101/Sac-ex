from google.cloud import pubsub_v1
import sys 

project_id = "chirpsexam"

if len(sys.argv) != 2:
    exit(-1
         )
topic_name = sys.argv[1]

sub_name = f"sub-{topic_name}"
subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(project_id, sub_name)

# crea la subscription solo se non esiste
try:
    subscriber.get_subscription(request={"subscription": sub_path})
except:
    subscriber.create_subscription(
        request={
            "name": sub_path,
            "topic": topic_name,
        }
    )

def callback(msg):
    print(msg.data.decode())
    msg.ack()

subscriber.subscribe(sub_path, callback)

print(f"Listening on topic #{topic_name}")
while True:
    pass
