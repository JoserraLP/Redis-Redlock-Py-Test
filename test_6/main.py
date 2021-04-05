import random
import threading
import time

from redlock import Redlock

from db.redisdb import RedisDB

RESOURCE_PREFIX = "planes:"
RESOURCE_ID = "0"
RESOURCE_NAME = RESOURCE_PREFIX + RESOURCE_ID


def thread_function():
    # Get another lock on the plane number 1 around 5 seconds
    thread_plane_lock = dlm.lock(RESOURCE_ID, 5000)

    if thread_plane_lock:
        print("Client 2: Lock  on resource'" + RESOURCE_NAME + "' acquired successfully, client 1 doesn't acquire it")

        # Update the resource
        redis.update(name=RESOURCE_NAME, key="client", value="client_2")
        redis.update(name=RESOURCE_NAME, key="random", value=random.random())
    else:
        print("Client 2: Error acquiring the lock on resource '" + RESOURCE_NAME + "'")


# Create Redis instance
redis = RedisDB()

# Create Redlock instance
dlm = Redlock([{"host": "localhost", "port": 6379, "db": 0}, ])

print("## EXECUTING TEST 6 ##")
print(" Several clients, Several locks, one resource, client blocked ")

# Get the resource previously to its modification
prev_resource = redis.get(RESOURCE_NAME)

# Get a lock on the plane number 1 around 10 seconds
plane_lock = dlm.lock(RESOURCE_ID, 10000)

# Start the second client process
client_2 = threading.Thread(target=thread_function)

# Start the second client with the thread
client_2.start()

# Sleep current thread for 15 seconds in order to simulate it is blocked and check the behaviour
time.sleep(15)

# Start the second client process, again, to try again
client_2 = threading.Thread(target=thread_function)

# Start the second client with the thread
client_2.start()

# We should check again for the lock
plane_lock = dlm.lock(RESOURCE_ID, 10000)

# Check if the lock has been acquired
if plane_lock:
    print("Client 1: Lock  on resource'" + RESOURCE_NAME + "' acquired successfully, client 2 doesn't acquire it")

    # Introduce the lock in the resource
    redis.update(name=RESOURCE_NAME, key="client", value="client_1")
    redis.update(name=RESOURCE_NAME, key="random", value=random.random())

else:
    print("Client 1: Error acquiring the lock on resource '" + RESOURCE_NAME + "'")

# Save data changes on db
redis.bgsave()

# Get the updated resources
updated_resource = redis.get(RESOURCE_NAME)

# Show the resources
print("## RESOURCE '" + RESOURCE_NAME + "' ##")
print("Previous resource:", prev_resource)
print("Updated resource:", updated_resource)

if prev_resource == updated_resource:
    print("Error updating the resource '" + RESOURCE_NAME + "'")
else:
    print("Resource '" + RESOURCE_NAME + "' updated successfully")
