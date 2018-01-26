import os

from . import data
from . import common


def response(user, inStr):
    splitSig = ';'
    file_name = 'teach.yml'
    if not common.is_super(user):
        return
    if not inStr:
        return
    if splitSig not in inStr:
        return
    data_path = common.cfg().get('data_path')[0]
    file_path = os.path.join(data_path, file_name)
    f = open(file_path, 'a')
    que = inStr.split(splitSig)[0]
    ans = inStr.split(splitSig)[1]
    que = common.init_input(que)
    ans = common.init_input(ans)
    text = '\n- que:\n  - %s\n  ans:\n  - %s\n' % (que, ans)
    f.write(text)
    f.close()
    data.Data([file_path]).import_data()
    return 'OK, I learned.'
