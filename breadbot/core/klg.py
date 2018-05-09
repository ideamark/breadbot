import random
import re
import string

from breadbot.core import memory
from breadbot.core import common

DO_YOU_MEAN = 'Do you mean:'


def _get_qas(db, coll, is_super=False):
    if coll[-4:] != '_yml':
        return
    if is_super:
        reqs = db[coll].find_one({'$or': [{'tag': 'klg'}, {'tag': 'sec'}]})
    else:
        reqs = db[coll].find_one({'tag': 'klg'})
    if reqs:
        qas = reqs['qas']
        return qas
    else:
        return []


def response(db, user, in_str):
    is_super = common.is_super(user)
    in_str = common.expand_abbrev(in_str)
    in_str = re.sub('[%s]+' % string.punctuation, '', in_str)
    in_str = in_str.lower()
    if len(in_str) < 3:
        return
    regx_str = '(^|.* )' + in_str + '( .*|$)'
    colls = db.collection_names()
    try:
        dias = memory.dialogue(user).get_dia()
        last_dia = dias[-1]
        last_ans = list(last_dia.values())[0]
    except Exception:
        return
    new_ques = []
    if DO_YOU_MEAN in last_ans:
        ques = last_ans.split(r'\n')[1:]
        for que in ques:
            if re.match(regx_str, que):
                new_ques.append(que)
    new_ques = list(set(new_ques))
    if len(new_ques) < 1:
        words = in_str.split(' ')
        for coll in colls:
            qas = _get_qas(db, coll, is_super)
            if not qas:
                continue
            for qa in qas:
                ques = qa['que']
                for que in ques:
                    all_words_in = True
                    que_words = que.split(' ')
                    for word in words:
                        if word not in que_words:
                            all_words_in = False
                            break
                    if all_words_in:
                        new_ques.append('- ' + que)
                        break
        new_ques = list(set(new_ques))
    if len(new_ques) < 1:
        return
    elif len(new_ques) == 1:
        Que = new_ques[0]
        Que = re.sub(r'^- ', '', Que)
        for coll in colls:
            qas = _get_qas(db, coll, is_super)
            if not qas:
                continue
            for qa in qas:
                ques = qa['que']
                if Que in ques:
                    res = qa['ans']
                    break
        if type(res) is list:
            res = random.choice(res)
        if res[-1] == '\n':
            res = res[:-1]
    else:
        new_ques.insert(0, DO_YOU_MEAN)
        res = '\n'.join(new_ques)
    if res:
        memory.dialogue(user).insert_dia(in_str, res)
    return res
