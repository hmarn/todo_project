# Use official Redis image as base
FROM redis:latest

# Optional: Expose the Redis port (default is 6379)
EXPOSE 6379

# Optional: Use a custom redis.conf (uncomment the next two lines if you have one)
# COPY redis.conf /usr/local/etc/redis/redis.conf
# CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]

# Default command to run Redis server
CMD ["redis-server"]
