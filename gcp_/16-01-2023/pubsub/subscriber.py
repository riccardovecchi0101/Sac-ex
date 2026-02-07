#python -m pubsub.subscriber


from google.cloud import pubsub_v1
from google.cloud.exceptions import NotFound
import json
from api.gcpdao import Dao


dao = Dao()

project_id = "secretsantaesame"
subscription_id = "subsecretsanta"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

topic_id = "ricevidestinatario"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def callback(message):
    print("Messaggio ricevuto RAW:", message.data)
    data = json.loads(message.data.decode("utf-8"))
    
    try:
       rv = dao.get_destinatario(data['email'])
       message_ = {"messaggio":rv, "timestamp":data['timestamp']}
    except NotFound:
        message_ = {"messaggio":"email non trovata", "timestamp": data['timestamp']}

    publisher.publish(
        topic_path,
        json.dumps(message_).encode("utf-8")
    )

    print("risposta inviata")

    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
print("Subscriber in ascolto...")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Chiusura subscriber")
