from hazelcast import HazelcastClient


client = HazelcastClient()
topic = client.get_topic('topic').blocking()

for value in range(100):
    topic.publish(value)

client.shutdown()

