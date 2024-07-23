import sys
import json
from steam import game_servers as gs

class ServerInfoExtractor:
    def __init__(self, server_info):
        self.server_info = server_info

    def get_value(self, keys, default='Unknown'):
        """
        Try multiple keys to get a value from server_info.
        Returns the first found value or the default.
        """
        for key in keys:
            if isinstance(key, str):
                value = self.server_info.get(key, None)
            elif isinstance(key, (list, tuple)):
                value = self._nested_get(key)
            else:
                continue

            if value is not None:
                return value
        return default

    def _nested_get(self, keys):
        """Helper method to get nested dictionary values."""
        temp = self.server_info
        for key in keys:
            if isinstance(temp, dict):
                temp = temp.get(key)
            else:
                return None
        return temp

def get_server_info(ip, port):
    try:
        server = gs.a2s_info((ip, port))
        players = gs.a2s_players((ip, port))
        return server, players
    except gs.NoResponseError:
        raise ConnectionError("The server did not respond. It may be offline or the IP/port might be incorrect.")
    except gs.BrokenMessageError:
        raise ValueError("Received an invalid response from the server. The server might be running an incompatible version.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

def print_server_info(server_info, players):
    extractor = ServerInfoExtractor(server_info)

    print("Server info:")
    print(f"- Name: {extractor.get_value(['name', 'server_name', 'hostname'])}")
    print(f"- Map: {extractor.get_value(['map', 'map_name'])}")
    print(f"- Game: {extractor.get_value(['game', 'gamedir'])}")
    
    print("\nServer Statistics:")
    print(f"- Game Mode: {extractor.get_value(['game_mode', 'gamemode'], 'Unknown')}")
    
    player_count = extractor.get_value(['players', 'player_count', 'num_players', ['rules', 'players']])
    max_players = extractor.get_value(['max_players', 'maxplayers', ['rules', 'max_players']])
    
    print(f"- Maximum Players: {max_players}")
    
    if player_count != 'Unknown' and max_players != 'Unknown':
        try:
            available_slots = int(max_players) - int(player_count)
            print(f"- Available Slots: {available_slots}")
        except ValueError:
            print("- Available Slots: Unable to calculate")
    else:
        print("- Available Slots: Unknown")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_server.py <ip:port>")
        sys.exit(1)

    ip_port = sys.argv[1].split(':')
    if len(ip_port) != 2:
        print("Invalid game server IP format. Use format: <ip:port>")
        sys.exit(1)
    
    ip = ip_port[0]
    try:
        port = int(ip_port[1])
    except ValueError:
        print("Invalid port number. Port must be an integer.")
        sys.exit(1)

    try:
        server_info, players = get_server_info(ip, port)
        if server_info:
            print_server_info(server_info, players)
        else:
            print("Failed to retrieve server info.")
    except ConnectionError as e:
        print(f"Connection Error: {e}")
    except ValueError as e:
        print(f"Value Error: {e}")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")