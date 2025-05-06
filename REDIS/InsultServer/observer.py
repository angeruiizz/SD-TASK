import redis

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name = "INSULTS_broadcast"

def receive_insults():
    pubsub = client.pubsub()
    pubsub.subscribe(channel_name)
    print(f"Observer subscribed to: {channel_name}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            insult = message['data']
            print(f"Observer received: {insult}")

receive_insults()
