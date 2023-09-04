import redis
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <write_redis_address> <read_redis_address> <command>")
        sys.exit(1)

    write_address = sys.argv[1]
    read_address = sys.argv[2]
    command = sys.argv[3].split()

    if command[0].lower() != "set" or len(command) != 3:
        print("Only 'set' command with key and value is supported.")
        sys.exit(1)

    key = command[1]
    value = command[2]

    # Connect to the write Redis instance and set the value
    write_host, write_port = write_address.split(":")
    write_redis = redis.StrictRedis(host=write_host, port=int(write_port))
    write_redis.set(key, value)

    # Connect to the read Redis instance and get the value
    read_host, read_port = read_address.split(":")
    read_redis = redis.StrictRedis(host=read_host, port=int(read_port))
    read_value = read_redis.get(key)

    if read_value.decode('utf-8') == value:
        print(f"Value '{value}' for key '{key}' successfully written to {write_address} and read from {read_address}.")
    else:
        print(f"Failed to verify value for key '{key}' between {write_address} and {read_address}.")

if __name__ == "__main__":
    main()
