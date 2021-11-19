import os
import time

from parser import maogai, not_implement
import const


subject_map = {
    'maogai': {'name': '毛概', 'func': maogai.parse},
    'clang1': {'name': 'C语言上', 'func': not_implement},
    'clang2': {'name': 'C语言下', 'func': not_implement},
    'junli1': {'name': '军理上', 'func': not_implement},
    'junli2': {'name': '军理下', 'func': not_implement},
    'jinxiandaishi': {'name': '近代史', 'func': not_implement},
    'sixiu': {'name': '思修', 'func': not_implement},
    'makesi': {'name': '马克思', 'func': not_implement},
}

if __name__ == '__main__':
    index_dict = {
        'version': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        'content': []
    }
    subjects = subject_map.keys()
    for subject in subjects:
        path = const.convert_result_dir + subject + '/'
        if os.path.exists(path):
            info = subject_map[subject]
            info['func'](path)
            print('\n')
