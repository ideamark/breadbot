import random
import re
import string

from breadbot.core import memory
from breadbot.core import common

DO_YOU_MEAN = 'Do you mean:'


def _get_qas(db, coll, isSuper=False):
    if coll[-4:] != '_yml':
        return
    reqs = db[coll].find_one()
    tags = reqs['tag']
    if 'klg' not in tags:
        return
    elif 'sec' in tags and not isSuper:
        return
    qas = reqs['qas']
    return qas


def response(db, user, inStr):
    isSuper = common.is_super(user)
    inStr = common.expand_abbrev(inStr)
    inStr = re.sub('[%s]+' % string.punctuation, '', inStr)
    inStr = inStr.lower()
    if len(inStr) < 3:
        return
    regexStr = '(^|.* )' + inStr + '( .*|$)'
    colls = db.collection_names()
    try:
        dias = memory.dialogue(user).get_dia()
        lastDia = dias[-1]
        lastAns = list(lastDia.values())[0]
    except Exception:
        return
    newQues = []
    if DO_YOU_MEAN in lastAns:
        ques = lastAns.split(r'\n')[1:]
        for que in ques:
            if re.match(regexStr, que):
                newQues.append(que)
    newQues = list(set(newQues))
    if len(newQues) < 1:
        words = inStr.split(' ')
        for coll in colls:
            qas = _get_qas(db, coll, isSuper)
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
                        newQues.append('- ' + que)
                        break
        newQues = list(set(newQues))
    if len(newQues) < 1:
        return
    elif len(newQues) == 1:
        Que = newQues[0]
        Que = re.sub(r'^- ', '', Que)
        for coll in colls:
            qas = _get_qas(db, coll, isSuper)
            if not qas:
                continue
            for qa in qas:
                ques = qa['que']
                if Que in ques:
                    res = qa['ans']
                    break
        if type(res) == list:
            res = random.choice(res)
        if res[-1] == '\n':
            res = res[:-1]
    else:
        newQues.insert(0, DO_YOU_MEAN)
        res = '\n'.join(newQues)
    if res:
        memory.dialogue(user).insert_dia(inStr, res)
    return res
