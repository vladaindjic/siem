import os

# DJANGOCENTER_PREFIX = '/home/vi3/Faks/Bezbednost/djangocenter'
DJANGOCENTER_PREFIX = os.path.dirname(__file__)
CENTER_PREFIX = os.path.join(DJANGOCENTER_PREFIX, 'center')
MINI_PARSER_PREFIX = os.path.join(CENTER_PREFIX, 'mini_parser')
MINI_PARSER_CERTS_PREFIX = os.path.join(MINI_PARSER_PREFIX, 'certs')

JWT_CONFIG_PATH = os.path.join(DJANGOCENTER_PREFIX, 'jwt-config.yaml')
# sertifikati
DJANGOCENTER_CERTS_PREFIX = os.path.join(DJANGOCENTER_PREFIX, 'certs')
