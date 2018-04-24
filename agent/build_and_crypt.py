def add_attr(attr_name, from_dict, to_dict):
    new_attr_name = attr_name
    if new_attr_name == 'severity_code':
        new_attr_name = 'severity'
    elif new_attr_name == 'facility_code':
        new_attr_name = 'facility'
    elif new_attr_name == 'syslog_version':
        new_attr_name = 'version'
    elif new_attr_name == 'process_id':
        new_attr_name = 'procid'
    elif new_attr_name == 'app_name':
        new_attr_name = 'appname'
    elif new_attr_name == 'message_id':
        new_attr_name = 'msgid'
    elif new_attr_name == 'message':
        new_attr_name = 'msg'

    if attr_name in from_dict:
        if from_dict[attr_name]:
            if from_dict[attr_name] != '-':
                to_dict[new_attr_name] = from_dict[attr_name] if attr_name != 'process_id' else str(from_dict[attr_name])


def build_json_dto(parsed_object):
    attributes = parsed_object.__dict__

    dto = {}

    # Facility
    add_attr('facility_code', attributes, dto)
    # Severity
    add_attr('severity_code', attributes, dto)
    # version
    add_attr('syslog_version', attributes, dto)
    # timestamp
    add_attr('timestamp', attributes, dto)
    # hostname
    add_attr('hostname', attributes, dto)
    # app_name
    add_attr('app_name', attributes, dto)
    # process_id
    add_attr('process_id', attributes, dto)
    # MSG_ID
    add_attr('message_id', attributes, dto)
    # message
    add_attr('message', attributes, dto)
    # full line
    add_attr('line', attributes, dto)
    # FIXME: Not process for now SD_elements
    return dto