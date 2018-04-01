# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
#
#
# ##
# # Python function for reading linux lastlog file
# # http://www.likexian.com/
# #
# # Copyright 2014, Kexian Li
# # Released under the Apache License, Version 2.0
# #
# ##
#
#
# import struct
#
#
# # #define UT_LINESIZE      32
# # #define UT_HOSTSIZE     256
# #
# # struct lastlog {
# #     time_t  ll_time;
# #     char    ll_line[UT_LINESIZE];
# #     char    ll_host[UT_HOSTSIZE];
# # };
# LASTLOG_STRUCT = 'l32s256s'
# LASTLOG_STRUCT_SIZE = struct.calcsize(LASTLOG_STRUCT)
#
#
# def read_lastlog(fname):
#     result = []
#
#     fp = open(fname, 'rb')
#     while True:
#         bytes = fp.read(LASTLOG_STRUCT_SIZE)
#         if not bytes:
#             break
#
#         data = struct.unpack(LASTLOG_STRUCT, bytes)
#         data = [(lambda s: str(s).split("\0", 1)[0])(i) for i in data]
#         if data[0] != '0':
#             result.append(data)
#
#     fp.close()
#     result.reverse()
#
#     return result
#
#
# print('reading data from lastlog')
# data = read_lastlog('/var/log/lastlog')
# for i in data:
#     print(i)
#
#
#
#
#
#
#
#
#
#

import utmp


with open('/var/log/lastlog', 'rb') as fd:
    buf = fd.read()
    print(buf)
    it = utmp.read(buf)
    while it:
        try:
            entry = next(it)
            print(entry.time, entry.type, entry)
        except:
            print("Sve puca")
            continue
