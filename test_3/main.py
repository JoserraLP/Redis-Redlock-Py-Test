import random

from redlock import Redlock

from db.redisdb import RedisDB

RESOURCE_PREFIX = "planes:"
RESOURCE_1_ID = "0"
RESOURCE_1_NAME = RESOURCE_PREFIX + RESOURCE_1_ID

RESOURCE_2_ID = "1"
RESOURCE_2_NAME = RESOURCE_PREFIX + RESOURCE_2_ID

# Create Redis instance
redis = RedisDB()

# Create Redlock instance
dlm = Redlock([{"host": "localhost", "port": 6379, "db": 0}, ])

print("## EXECUTING TEST 3 ##")
print(" One client, Several locks, Different resources ")

# Get the resource previously to its modification
prev_resource_1 = redis.get(RESOURCE_1_NAME)
prev_resource_2 = redis.get(RESOURCE_2_NAME)

# Get a lock on the plane number 0 around 10 seconds
plane_0_lock_1 = dlm.lock(RESOURCE_1_ID, 10000)

# Get another lock on the plane number 1 around 5 seconds
plane_1_lock_1 = dlm.lock(RESOURCE_2_ID, 5000)

# Check if the lock has been acquired
if plane_0_lock_1:
    print("Lock on resource '" + RESOURCE_1_NAME + "' acquired successfully")

    # Introduce the lock in the resource
    redis.update(name=RESOURCE_1_NAME, key="client", value="client_1")
    redis.update(name=RESOURCE_1_NAME, key="random", value=random.random())
else:
    print("Error acquiring the lock on resource '" + RESOURCE_1_NAME + "'")

if plane_1_lock_1:
    print("Lock on resource'" + RESOURCE_2_NAME + "' acquired successfully")

    # Introduce the lock in the resources
    redis.update(name=RESOURCE_2_NAME, key="client", value="client_2")
    redis.update(name=RESOURCE_2_NAME, key="random", value=random.random())

else:
    print("Error acquiring the lock on resource '" + RESOURCE_2_NAME + "'")

# Save data changes on db
redis.bgsave()

# Get the updated resources
updated_resource_1 = redis.get(RESOURCE_1_NAME)
updated_resource_2 = redis.get(RESOURCE_2_NAME)

# Show the resources
print("## RESOURCE '" + RESOURCE_1_NAME + "' ##")
print("Previous resource:", prev_resource_1)
print("Updated resource:", updated_resource_1)

if prev_resource_1 == updated_resource_1:
    print("Error updating the resource '" + RESOURCE_1_NAME + "'")
else:
    print("Resource '" + RESOURCE_1_NAME + "' updated successfully")

print(" ## RESOURCE '" + RESOURCE_2_NAME + "' ##")
print("Previous resource:", prev_resource_2)
print("Updated resource:", updated_resource_2)

if prev_resource_2 == updated_resource_2:
    print("Error updating the resource '" + RESOURCE_2_NAME + "'")
else:
    print("Resource '" + RESOURCE_2_NAME + "' updated successfully")

