from hazelcast import HazelcastClient
import time


client = HazelcastClient()
queue = client.get_queue("queue").blocking()
reader2_items = []
while True:
    time.sleep(0.2)
    item = queue.poll()
    if not item:
        break
    reader2_items.append(item)
print("Reader1 items: {}".format(reader2_items))
client.shutdown()

