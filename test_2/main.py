import random

from redlock import Redlock

from db.redisdb import RedisDB

RESOURCE_PREFIX = "planes:"
RESOURCE_ID = "1"
RESOURCE_NAME = RESOURCE_PREFIX + RESOURCE_ID

# Create Redis instance
redis = RedisDB()

# Create Redlock instance
dlm = Redlock([{"host": "localhost", "port": 6379, "db": 0}, ])

print("## EXECUTING TEST 2 ##")
print(" One client, Several locks, One resource ")

# Get the resource previously to its modification
prev_resource = redis.get(RESOURCE_NAME)

# Get a lock on the plane number 1 around 10 seconds
plane_1_lock_1 = dlm.lock(RESOURCE_ID, 10000)

# Get another lock on the plane number 1 around 5 seconds
plane_1_lock_2 = dlm.lock(RESOURCE_ID, 5000)

# Check if the lock has been acquired
if plane_1_lock_1 and not plane_1_lock_2:
    print("Lock 1 on resource '" + RESOURCE_NAME + "' acquired successfully, the lock 2 doesn't acquire it")

    # Introduce the lock in the resource
    redis.update(name=RESOURCE_NAME, key="updated_by", value="lock_1")
    redis.update(name=RESOURCE_NAME, key="random", value=random.random())

elif not plane_1_lock_1 and plane_1_lock_2:
    print("Lock 2 on resource'" + RESOURCE_NAME + "' acquired successfully, the lock 1 doesn't acquire it")

    # Introduce the lock in the resource
    redis.update(name=RESOURCE_NAME, key="updated_by", value="lock_2")
    redis.update(name=RESOURCE_NAME, key="random", value=random.random())

else:
    print("Error acquiring the lock on resource '" + RESOURCE_NAME + "'")

# Save data changes on db
redis.bgsave()

# Get the updated resource
updated_resource = redis.get(RESOURCE_NAME)

# Show the resources
print("Previous resource:", prev_resource)
print("Updated resource:", updated_resource)

if prev_resource == updated_resource:
    print("Error updating the resource '" + RESOURCE_NAME + "'")
else:
    print("Resource '" + RESOURCE_NAME + "' updated successfully")

