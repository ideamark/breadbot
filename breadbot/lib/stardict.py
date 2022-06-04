import os
import sys
import struct
import re

from . import web

dict_path = os.path.dirname(os.path.abspath(__file__))

def translate(word):
    if re.match('[\u4e00-\u9fa5]+', word):
        idx_file = open('%s/dicts/stardict-lazyworm-ce-2.4.2/lazyworm-ce.idx' % dict_path, 'rb')
        dict_file = open('%s/dicts/stardict-lazyworm-ce-2.4.2/lazyworm-ce.dict' % dict_path, 'rb')
    else:
        idx_file = open('%s/dicts/stardict-lazyworm-ec-2.4.2/lazyworm-ec.idx' % dict_path, 'rb')
        dict_file = open('%s/dicts/stardict-lazyworm-ec-2.4.2/lazyworm-ec.dict' % dict_path, 'rb')

    dict_idx = dict()

    while True:
        word_str = b''
        one_byte = idx_file.read(1)

        if one_byte == b'':
            break

        while ord(one_byte) != 0:
            word_str += one_byte
            one_byte = idx_file.read(1)

        buffer = idx_file.read(8)
        word_data_offset, word_data_size = struct.unpack('!ii', buffer)
        dict_idx[word_str.decode()] = [word_data_offset, word_data_size]

    try:
        word_data_offset, word_data_size = dict_idx[word]
        dict_file.seek(word_data_offset)
        word_dict = dict_file.read(word_data_size).decode()
        return word_dict

    except:
        return web.search_baidu(word)

    finally:
        idx_file.close()
        dict_file.close()

if __name__ == '__main__':
    word = sys.argv[1]
    print(translate(word))
