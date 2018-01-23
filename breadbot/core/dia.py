import random
import re
import string
import Levenshtein as Leven

from breadbot.core import misc

JARO_WINKLER_PERCENT = 0.98


def response(db, user, inStr):
    inStr = misc.que_init(inStr)
    ans = ''
    colls = db.collection_names()
    random.shuffle(colls)
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
        random.shuffle(qas)
        for qa in qas:
            ques = qa['que']
            random.shuffle(ques)
            for que in ques:
                que = str(que)
                que = misc.que_init(que)
                if Leven.jaro_winkler(inStr, que) > JARO_WINKLER_PERCENT:
                    ans = qa['ans']
                    if type(ans) is list:
                        ans = random.choice(ans)
                    return ans
    return ans
