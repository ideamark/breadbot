import random
import re
import string
import Levenshtein as Leven

from breadbot.core import misc

JARO_WINKLER_PERCENT = 0.98


def response(db, user, inStr):
    inStr = misc.que_init(inStr)
    res = []
    colls = db.collection_names()
    for coll in colls:
        if coll[-4:] != '_yml':
            continue
        reqs = db[coll].find_one()
        tags = reqs['tag']
        if 'dia' not in tags:
            continue
        qas = reqs['QA']
        if not qas:
            continue
        for qa in qas:
            ques = qa['que']
            for que in ques:
                que = str(que)
                que = misc.que_init(que)
                if Leven.jaro_winkler(inStr, que) > JARO_WINKLER_PERCENT:
                    ans = qa['ans']
                    if type(ans) is not list:
                        ans = [ans]
                    res += ans
    if res:
        res = random.choice(res)
    return res
