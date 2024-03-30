from hazelcast import HazelcastClient
import time


def on_message(message):
    time.sleep(2)
    print(f"Received: {message.message}")


client = HazelcastClient()
topic = client.get_topic("topic").blocking()
topic.add_listener(on_message)
input("subscriber2\n")

client.shutdown()

