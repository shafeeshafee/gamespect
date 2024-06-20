import sys
from steam import game_servers as gs

def get_server_info(ip, port):
    server = gs.a2s_info((ip, port))
    return server

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("How to Use: inspect_server <ip:port>")
        sys.exit(1)

    ip_port = sys.argv[1].split(':')
    if len(ip_port) != 2:
        print("Invalid game server IP format. Use format: <ip:port>")
        sys.exit(1)
    
    ip = ip_port[0]
    port = int(ip_port[1])

    try:
        server_info = get_server_info(ip, port)
        if server_info:
            print("Server info:")
            for key, value in server_info.items():
                print(f"- {key.title()} : {value}")
        else:
            print("Failed to retrieve server info.")
    except Exception as e:
        print(f"An error occured: {e}")


