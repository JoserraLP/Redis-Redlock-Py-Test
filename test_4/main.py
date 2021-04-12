import random
import threading
import time

from colors import bcolors
from redlock import Redlock

from db.redisdb import RedisDB

RESOURCE_PREFIX = "planes:"
RESOURCE_ID = "1"
RESOURCE_NAME = RESOURCE_PREFIX + RESOURCE_ID


def thread_function():
    # Get another lock on the plane number 1 around 5 seconds
    print(f"{bcolors.OKGREEN}Client 2:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Requesting lock on resource '" + RESOURCE_NAME + f"'...{bcolors.ENDC}")
    plane_1_lock = dlm.lock(RESOURCE_ID, 5000)

    if plane_1_lock:
        print(f"{bcolors.OKGREEN}Client 2:{bcolors.ENDC} "
              f"{bcolors.OKCYAN}Lock on resource '" + RESOURCE_NAME + f"' acquired successfully. {bcolors.ENDC}")

        client_2_lock_1_key = plane_1_lock.key.decode("utf-8")
        print(f"{bcolors.OKGREEN}Client 2:{bcolors.ENDC} "
              f"{bcolors.OKCYAN}Lock key: {bcolors.BOLD}" + client_2_lock_1_key + f"{bcolors.ENDC}")

        client_2_resource_key = redis.get_key(RESOURCE_ID)
        print(f"{bcolors.WARNING}Redis:{bcolors.ENDC} "
              f"{bcolors.WARNING}Resource key: {client_2_resource_key} {bcolors.ENDC}")

        print(f"{bcolors.OKGREEN}Client 2:{bcolors.ENDC} "
              f"{bcolors.OKCYAN}Updating resource '" + RESOURCE_NAME + f"' {bcolors.ENDC}")
        # Update the resource
        redis.update(name=RESOURCE_NAME, key="client", value="client_2")
        redis.update(name=RESOURCE_NAME, key="random", value=random.random())
    else:
        print(f"{bcolors.FAIL}Client 2: Error acquiring the lock on resource '" + RESOURCE_NAME + f"' {bcolors.ENDC}")


# Create Redis instance
redis = RedisDB()

# Create Redlock instance
dlm = Redlock([{"host": "localhost", "port": 6379, "db": 0}, ])

print(f"{bcolors.OKBLUE}## EXECUTING TEST 4 ##{bcolors.ENDC}")
print(f"{bcolors.OKBLUE} Several clients, Several locks, One resource {bcolors.ENDC}")

# Get the resource previously to its modification
print(f"{bcolors.OKCYAN}Retrieving resource in order to compare it after the update...{bcolors.ENDC}")
prev_resource = redis.get(RESOURCE_NAME)

# Get a lock on the plane number 1 around 10 seconds
print(f"{bcolors.OKGREEN}Client 1:{bcolors.ENDC} "
      f"{bcolors.OKCYAN}Requesting lock on resource '" + RESOURCE_NAME + f"'...{bcolors.ENDC}")
plane_1_lock_1 = dlm.lock(RESOURCE_ID, 10000)

# Start the second client process
client_2 = threading.Thread(target=thread_function)

# Start the second client with the thread
print(f"{bcolors.OKGREEN}Client 2: Starting...{bcolors.ENDC} ")
client_2.start()

# Sleep current thread for 2 seconds in order to the second client ask for the lock
print(f"{bcolors.OKGREEN}Client 1: Waiting 2 seconds...{bcolors.ENDC} ")
time.sleep(2)

# Check if the lock has been acquired
if plane_1_lock_1:
    print(f"{bcolors.OKGREEN}Client 1:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Lock on resource '" + RESOURCE_NAME + f"' acquired successfully. {bcolors.ENDC}")

    lock_1_key = plane_1_lock_1.key.decode("utf-8")
    print(f"{bcolors.OKGREEN}Client 1:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Lock key: {bcolors.BOLD}" + lock_1_key + f"{bcolors.ENDC}")

    resource_key = redis.get_key(RESOURCE_ID)
    print(f"{bcolors.WARNING}Redis:{bcolors.ENDC} "
          f"{bcolors.WARNING}Resource key: {resource_key} {bcolors.ENDC}")

    # Introduce the lock in the resource
    print(f"{bcolors.OKGREEN}Client 1:{bcolors.ENDC} "
          f"{bcolors.OKCYAN}Updating resource '" + RESOURCE_NAME + f"' {bcolors.ENDC}")

    # Introduce the lock in the resource
    redis.update(name=RESOURCE_NAME, key="client", value="client_1")
    redis.update(name=RESOURCE_NAME, key="random", value=random.random())

else:
    print(f"{bcolors.FAIL}Client 1: Error acquiring the lock on resource '" + RESOURCE_NAME + f"' {bcolors.ENDC}")

# Save data changes on db
redis.bgsave()

# Get the updated resource
print(f"{bcolors.OKCYAN}Retrieving updated resource{bcolors.ENDC}")
updated_resource = redis.get(RESOURCE_NAME)

# Show the resources
print("Previous resource:", prev_resource)
print("Updated resource:", updated_resource)

if prev_resource == updated_resource:
    print(f"{bcolors.FAIL}Error updating the resource '" + RESOURCE_NAME + f"' {bcolors.ENDC}")
else:
    print(f"{bcolors.OKGREEN}Resource '" + RESOURCE_NAME + f"' updated successfully{bcolors.ENDC}")
