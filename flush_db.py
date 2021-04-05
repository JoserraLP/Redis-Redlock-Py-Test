from db.redisdb import RedisDB

# Create Redis instance
redis = RedisDB()

# Delete all the data on the db
redis.flush_db()
