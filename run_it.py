
from client import Client
import json

def main():
    client = Client()
    print(client.get_accounts().json())


if __name__ == "__main__":
    main()