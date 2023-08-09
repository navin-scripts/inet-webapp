import pymongo, requests
from bson.objectid import ObjectId
from sshtunnel import SSHTunnelForwarder


def UniFiMongoClient():
    server = SSHTunnelForwarder(
            '172.31.255.96',
            ssh_username="ubuntu",
            ssh_pkey='~\\Downloads\\keys\\starlink2.pem',
            remote_bind_address=('localhost', 27117)
        )

    server.start()

    client=pymongo.MongoClient("localhost",server.local_bind_port)
    
    return client