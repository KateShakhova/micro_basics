from hazelcast import HazelcastClient


client = HazelcastClient()
queue = client.get_queue("queue").blocking()
queue.clear()
for value in range(100):
    queue.put(value)
client.shutdown()

