import os
import re

from breadbot.core import common


LOG = common.ConsoleLog()


def get_path_list():
    path_list = common.Cfg().get('local', 'data_paths')
    path_list = common.expand_path(path_list)
    path_list = common.get_md_path_list(path_list)
    return path_list


def empty_db(db):
    for key in db.keys():
        db.delete(key)
    LOG.info('Empty Database Done')


def simpleQA(db, lines):
    qus = ''
    ans = ''
    for i, line in enumerate(lines):
        if not line:
            continue
        elif not qus and re.match('^## .*', line):
            qus = re.sub('^## +', '', line)
            qus = re.sub(r'[^\w\s]', '', qus)
            qus = re.sub(' *\n$', '', qus)
            qus = qus.lower()
        elif qus and line:
            ans += line
            if i >= len(lines) - 1:
                ans = re.sub('\n+$', '', ans)
                ans = ans.split('\n')
                db.sadd(qus, *set(ans))
                qus = ''
                ans = ''
            for line2 in lines[i + 1:]:
                if not line2:
                    continue
                elif re.match('^## .*', line2):
                    ans = re.sub('\n+$', '', ans)
                    ans = ans.split('\n')
                    db.sadd(qus, *set(ans))
                    qus = ''
                    ans = ''
                else:
                    break


def knowledgeQA(db, lines):
    qus = ''
    ans = ''
    for i, line in enumerate(lines):
        if not line:
            continue
        elif not qus and re.match('^## .*', line):
            qus = re.sub('^## +', '', line)
            qus = re.sub(r'[^\w\s]', '', qus)
            qus = re.sub(' *\n$', '', qus)
            qus = qus.lower()
        elif qus and line:
            ans += line
            if i >= len(lines) - 1:
                ans = re.sub('\n+$', '', ans)
                db.set(qus, ans)
                qus = ''
                ans = ''
            for line2 in lines[i + 1:]:
                if not line2:
                    continue
                elif re.match('^## .*', line2):
                    ans = re.sub('\n+$', '', ans)
                    db.set(qus, ans)
                    qus = ''
                    ans = ''
                else:
                    break


def parser(db, lines):
    engine = ''
    start = False
    content = []
    for line in lines:
        if re.match(r'^> *\[.*\].*$', line):
            line = re.sub(r'^> *\[', '', line)
            line = re.sub(r'\].*$', '', line)
            engine = line.split(' ')[0]
            status = line.split(' ')[1]
            if 'start' in status:
                start = True
            elif 'end' in status:
                start = False
                eval('%s(db, content)' % engine)
                del content[:]
        if start:
            content.append(line)


def import_data(db):
    try:
        empty_db(db)
        path_list = get_path_list()

        for path in path_list:
            LOG.info('Import %s' % path)
            with open(path, 'r') as fp:
                lines = fp.readlines()
                parser(db, lines)

        LOG.info('All Data is Imported')
        return None

    except Exception as e:
        LOG.error(e)


if __name__ == '__main__':
    user = 'localuser'
    db = common.get_db()
    import_data(db)
