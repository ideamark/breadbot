import Levenshtein as Leven
import os
import random
import re
import string
import yaml

from . import common


@common.time_limit(3)
def response(user, in_str):
    in_str = common.que_init(in_str)
    regx_str = '^  - %s.*$' % in_str
    ans = __search_ans(user, regx_str, in_str)
    if not ans:
        regx_str = '^  - .*%s.*$' % in_str.replace(' ', '.*')
        ans = __search_ans(user, regx_str, in_str)
    if not ans:
        ans = common.dont_know()
    return ans

def __search_ans(user, regx_str, in_str):
    is_super = common.is_super(user)
    data_path_list = common.Cfg().get('local', 'data_paths')

    grep_list = []
    for data_path in data_path_list:
        cmd = 'grep -RE "%s" %s' % (regx_str, data_path)
        grep_list.extend(os.popen(cmd).readlines())

    max_jaro = 0
    max_jaro_info_list = []
    for res in grep_list:
        path = res.split(':')[0]
        if os.path.splitext(path)[-1] != '.yml':
            continue
        if 'sec_' in os.path.basename(path) and not is_super:
            continue
        que_str = re.sub('^%s:  - ' % path, '', res)
        que_str = re.sub(r'\n', '', que_str)
        jaro = Leven.jaro_winkler(que_str, in_str)
        if jaro > max_jaro:
            max_jaro = jaro
            max_jaro_info_list = [(path, que_str)]
            if max_jaro == 1:
                break
        elif jaro == max_jaro:
            max_jaro_info_list.append((path, que_str))

    random.shuffle(max_jaro_info_list)
    ans = None
    for path, que_str in max_jaro_info_list:
        fp = open(path, 'r')
        text = fp.read()
        fp.close()
        regx_str = '- que:\n(?:  - .*\n)*  - %s\n(?:  - .*\n)*  ' \
                   'ans:(?: *\|)?\n(?:(?!- que:).*\n)+' % que_str
        qas = re.findall(regx_str, text)
        if not qas:
            continue
        qa = random.choice(qas)
        qa = yaml.load(qa)[0]
        for que in qa['que']:
            if que == que_str:
                ans = qa['ans']
                if type(ans) is list:
                    ans = random.choice(ans)
                break
    return ans
