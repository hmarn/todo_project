# Note: this script is created to run redish server to work with Web Socket

docker build -t my-redis .

docker run -d --name redis-container -p 6379:6379 my-redis

# Test: 
# docker exec -it redis-container redis-cli
# ping
