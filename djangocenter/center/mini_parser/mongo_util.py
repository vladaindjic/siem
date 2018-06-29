import pymongo
import our_constants
import os
import yaml


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


        # ajde da iscitamo passphrase
        from our_constants import JWT_CONFIG_PATH
        with open(JWT_CONFIG_PATH) as stream:
            jwt_config = yaml.load(stream)



        ssl_certfile = os.path.join(our_constants.DJANGOCENTER_CERTS_PREFIX, 'siem-center.crt')
        ssl_keyfile = os.path.join(our_constants.DJANGOCENTER_CERTS_PREFIX, 'siem-center.key')
        # ssl_pem_passphrase = jwt_config['passphrase']  # FIXME: izdvoji ovo negde

        ssl_pem_passphrase = 'siem-center'  # FIXME: izdvoji ovo negde

        ssl_ca_certs = os.path.join(our_constants.DJANGOCENTER_CERTS_PREFIX, 'ca.crt')

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
