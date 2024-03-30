from hazelcast import HazelcastClient


client = HazelcastClient()
my_map = client.get_map("map").blocking()
for key in range(1000):
    my_map.put(key, "value {}".format(key))
client.shutdown()

