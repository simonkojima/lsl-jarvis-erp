import pyicom as icom
import json

if __name__ == "__main__":

    ip = "localhost"
    port = 45514

    client = icom.client(ip = ip,
                         port = port)
    client.connect()

    print("connected.")
    
    while True:
        target = input("Press Any Key to Send: ")
        data = dict()
        data['target'] = [str(target)]
        client.send(json.dumps(data).encode('utf-8'))
    