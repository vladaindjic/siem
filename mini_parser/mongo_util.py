import pymongo


class MongoUtil(object):
    instance = None

    @staticmethod
    def get_instance():
        if MongoUtil.instance is None:
            MongoUtil.instance = MongoUtil()
        return MongoUtil.instance

    def __init__(self):
        username = "siem"
        password = "siem_center123"
        host = "localhost"
        port = str(27017)
        database = "log-mongo"
        enabled = "true"
        ssl_certfile = "/home/zarko/Fax/Bezbednost/Siem/siem/mini_parser/certs/sysqo.crt"
        ssl_keyfile = "/home/zarko/Fax/Bezbednost/Siem/siem/mini_parser/certs/sysqo.key"
        ssl_pem_passphrase = "sysqo"
        ssl_ca_certs = "/home/zarko/Fax/Bezbednost/Siem/siem/mini_parser/certs//ca.crt"

        self.client = pymongo.MongoClient("mongodb://" + username + ":" + password +
                                          "@" + host + ":" + port + "/?authSource=" + database
                                          + "&ssl_certfile=" + ssl_certfile
                                          + "&ssl_keyfile=" + ssl_keyfile
                                          + "&ssl_pem_passphrase=" + ssl_pem_passphrase
                                          + "&ssl_ca_certs=" + ssl_ca_certs
                                          + "&ssl=" + enabled)

        self.log_mongo = self.client['log-mongo']

    @staticmethod
    def get_collection(collection_str):
        return MongoUtil.get_instance().log_mongo[collection_str]

    @staticmethod
    def get_log_collection():
        return MongoUtil.get_collection('log')

    @staticmethod
    def get_alarm_collection():
        return MongoUtil.get_collection('alarm')

    @staticmethod
    def get_alarm_fire_collection():
        return MongoUtil.get_collection('alarm-fire')
