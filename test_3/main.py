import random

from colors import bcolors
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

print(f"{bcolors.OKBLUE}## EXECUTING TEST 3 ##{bcolors.ENDC}")
print(f"{bcolors.OKBLUE} One client, Several locks, Different resources {bcolors.ENDC}")

# Get the resources previously to its modification
print(f"{bcolors.OKCYAN}Retrieving resource '" + RESOURCE_1_NAME + f"'in order to compare it after the update..."
                                                                   f"{bcolors.ENDC}")
prev_resource_1 = redis.get(RESOURCE_1_NAME)
print(f"{bcolors.OKCYAN}Retrieving resource '" + RESOURCE_2_NAME + f"'in order to compare it after the update..."
                                                                   f"{bcolors.ENDC}")
prev_resource_2 = redis.get(RESOURCE_2_NAME)

# Get a lock on the plane number 0 around 10 seconds
print(f"{bcolors.OKGREEN}Client 1 - Lock 1:{bcolors.ENDC} "
      f"{bcolors.OKCYAN}Requesting lock on resource '" + RESOURCE_1_NAME + f"'...{bcolors.ENDC}")
plane_0_lock_1 = dlm.lock(RESOURCE_1_ID, 10000)

# Get another lock on the plane number 1 around 5 seconds
print(f"{bcolors.OKGREEN}Client 1 - Lock 2:{bcolors.ENDC} "
      f"{bcolors.OKCYAN}Requesting lock on resource '" + RESOURCE_2_NAME + f"'...{bcolors.ENDC}")
plane_1_lock_1 = dlm.lock(RESOURCE_2_ID, 5000)

# Check if the lock has been acquired
if plane_0_lock_1:
    print(f"{bcolors.OKGREEN}Client 1 - Lock 1:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Lock on resource '" + RESOURCE_1_NAME + f"' acquired successfully. {bcolors.ENDC}")

    lock_key = plane_0_lock_1.key.decode("utf-8")
    print(f"{bcolors.OKGREEN}Client 1 - Lock 1:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Lock key for resource {RESOURCE_1_NAME}: {bcolors.BOLD}" + lock_key + f"{bcolors.ENDC}")

    resource_key = redis.get_key(RESOURCE_1_ID)
    print(f"{bcolors.WARNING}Redis:{bcolors.ENDC} "
          f"{bcolors.WARNING}Resource key for resource {RESOURCE_1_NAME}: {resource_key} {bcolors.ENDC}")

    # Introduce the client in the resource
    print(f"{bcolors.OKGREEN}Client 1 - Lock 1:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Updating resource '" + RESOURCE_1_NAME + f"' {bcolors.ENDC}")
    redis.update(name=RESOURCE_1_NAME, key="client", value="client_1")
    redis.update(name=RESOURCE_1_NAME, key="random", value=random.random())
else:
    print(f"{bcolors.FAIL}Client 1: Error acquiring the lock on resource '" + RESOURCE_1_NAME + f"' {bcolors.ENDC}")

if plane_1_lock_1:
    print(f"{bcolors.OKGREEN}Client 1 - Lock 2:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Lock on resource '" + RESOURCE_2_NAME + f"' acquired successfully. {bcolors.ENDC}")

    lock_key = plane_1_lock_1.key.decode("utf-8")
    print(f"{bcolors.OKGREEN}Client 1 - Lock 2:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Lock key for resource {RESOURCE_2_NAME}: {bcolors.BOLD}" + lock_key + f"{bcolors.ENDC}")

    resource_key = redis.get_key(RESOURCE_2_ID)
    print(f"{bcolors.WARNING}Redis:{bcolors.ENDC} "
          f"{bcolors.WARNING}Resource key for resource {RESOURCE_2_NAME}: {resource_key} {bcolors.ENDC}")

    # Introduce the lock in the resource
    print(f"{bcolors.OKGREEN}Client 1 - Lock 2:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Updating resource '" + RESOURCE_2_NAME + f"' {bcolors.ENDC}")

    # Introduce the client in the resources
    redis.update(name=RESOURCE_2_NAME, key="client", value="client_1")
    redis.update(name=RESOURCE_2_NAME, key="random", value=random.random())

else:
    print(f"{bcolors.FAIL}Error acquiring the lock on resource '" + RESOURCE_2_NAME + f"' {bcolors.ENDC}")

# Save data changes on db
redis.bgsave()

# Get the updated resources
print(f"{bcolors.OKCYAN}Retrieving updated resources{bcolors.ENDC}")
updated_resource_1 = redis.get(RESOURCE_1_NAME)
updated_resource_2 = redis.get(RESOURCE_2_NAME)

# Show the resources
print(f"{bcolors.OKCYAN}## RESOURCE '" + RESOURCE_1_NAME + f"' ##{bcolors.ENDC}")
print("Previous resource:", prev_resource_1)
print("Updated resource:", updated_resource_1)

if prev_resource_1 == updated_resource_1:
    print(f"{bcolors.FAIL}Error updating the resource '" + RESOURCE_1_NAME + f"' {bcolors.ENDC}")
else:
    print(f"{bcolors.OKGREEN}Resource '" + RESOURCE_1_NAME + f"' updated successfully{bcolors.ENDC}")

print(f"{bcolors.OKCYAN}## RESOURCE '" + RESOURCE_2_NAME + f"' ##{bcolors.ENDC}")
print("Previous resource:", prev_resource_2)
print("Updated resource:", updated_resource_2)

if prev_resource_2 == updated_resource_2:
    print(f"{bcolors.FAIL}Error updating the resource '" + RESOURCE_2_NAME + f"' {bcolors.ENDC}")
else:
    print(f"{bcolors.OKGREEN}Resource '" + RESOURCE_2_NAME + f"' updated successfully{bcolors.ENDC}")
