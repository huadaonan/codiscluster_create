import sys
import paramiko

# 设置服务器IP地址
write_server_ip = "172.22.0.234"
read_server_ip = "10.100.5.89"

ssh_username = "root"
private_key_path = "/root/.ssh/root_fcloud"

def execute_ssh_command(host, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, username=ssh_username, key_filename=private_key_path)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    result = stdout.read().decode('utf-8').strip()
    ssh_client.close()
    return result

def verify_data(write_ip, read_ip, write_address, read_address, command):
    key = command[1]
    value = command[2]

    # SSH to the write server and execute the set command
    write_host, write_port = write_address.split(":")
    write_command = f"redis-cli -h {write_host} -p {write_port} {command[0]} {key} {value}"
    execute_ssh_command(write_ip, write_command)

    # SSH to the read server and execute the get command
    read_host, read_port = read_address.split(":")
    read_command = f"redis-cli -h {read_host} -p {read_port} get {key}"
    read_value = execute_ssh_command(read_ip, read_command)

    if read_value == value:
        return True
    else:
        return False

def main():
    if len(sys.argv) != 5:
        print("Usage: python script_name.py <write_redis_address> <read_redis_address> <forward_command> <reverse_command>")
        sys.exit(1)

    write_address = sys.argv[1]
    read_address = sys.argv[2]
    forward_command = sys.argv[3].split()
    reverse_command = sys.argv[4].split()

    if forward_command[0].lower() != "set" or len(forward_command) != 3:
        print("Only 'set' command with key and value is supported for forward verification.")
        sys.exit(1)

    if reverse_command[0].lower() != "set" or len(reverse_command) != 3:
        print("Only 'set' command with key and value is supported for reverse verification.")
        sys.exit(1)

    # 正向验证
    forward_verification = verify_data(write_server_ip, read_server_ip, write_address, read_address, forward_command)
    # 反向验证
    reverse_verification = verify_data(read_server_ip, write_server_ip, read_address, write_address, reverse_command)

    if forward_verification:
        print(f"Forward Verification: Value '{forward_command[2]}' for key '{forward_command[1]}' successfully written to {write_address} and read from {read_address}.")
    else:
        print(f"Forward Verification: Failed to verify value for key '{forward_command[1]}' between {write_address} and {read_address}.")

    if reverse_verification:
        print(f"Reverse Verification: Value '{reverse_command[2]}' for key '{reverse_command[1]}' successfully written to {read_address} and read from {write_address}.")
    else:
        print(f"Reverse Verification: Failed to verify value for key '{reverse_command[1]}' between {read_address} and {write_address}.")

if __name__ == "__main__":
    main()
