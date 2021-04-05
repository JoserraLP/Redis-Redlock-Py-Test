from db.data_generator import DataGenerator
from db.redisdb import RedisDB

data_generator = DataGenerator()

# Generating data
data_generator.generate_data()

# Retrieving data
data = data_generator.get_data()

# Create Redis instance
redis = RedisDB()

redis.set(data)

print(redis.get("planes:0"))
print(redis.get("planes:1"))


# It is not necessary to indicate the "planes" prefix as all of them are "planes"

# In order to lock a nested resource use ":"
