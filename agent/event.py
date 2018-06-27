
class Event:

    def __init__(self, event_id, machine_name, data, index, category, category_number,
                 entry_type, message, source, replacement_strings, instance_id, time_generated,
                 time_written, user_name, site, container):
        self.event_id = event_id
        self.machine_name = machine_name
        self.data = data
        self.index = index
        self.category = category
        self.category_number = category_number
        self.entry_type = entry_type
        self.message = message
        self.source = source
        self.replacement_strings = replacement_strings
        self.instance_id = instance_id
        self.time_generated = time_generated
        self.time_written = time_written
        self.user_name = user_name
        self.site = site
        self.container = container

    def __str__(self) -> str:
        return "EventID: {0} MachineName: {1} Data: {2} Index: {3} Category: {4} CategoryNumber: {5} EntryType: {6} Message: {7} " \
               "Source: {8} ReplacementStrings: {9} InstanceId: {10} TimeGenerated: {11} TimeWritten: {12} UserName: {13} Site: {14} Container: {15}".\
            format(self.event_id,self.machine_name,self.data,self.index,self.category,self.category_number,self.entry_type,self.message,self.source,
                   self.replacement_strings,self.instance_id,self.time_generated,self.time_written,self.user_name,self.site,self.container)

        # return str

