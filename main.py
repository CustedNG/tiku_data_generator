import os
import time

from parser import maogai, junli, jindaishi, not_implement
import const
import index


subject_map = {
    'maogai': {'name': '毛概', 'func': maogai},
    'clang1': {'name': 'C语言上', 'func': not_implement},
    'clang2': {'name': 'C语言下', 'func': not_implement},
    'junli': {'name': '军理', 'func': junli},
    'jinxiandaishi': {'name': '近代史', 'func': jindaishi},
    'sixiu': {'name': '思修', 'func': not_implement},
    'makesi': {'name': '马克思', 'func': maogai},
    'feedback': {'name': '反馈', 'func': maogai},
}

if __name__ == '__main__':
    start_time = time.time()

    subjects = subject_map.keys()
    enabled_subjects: dict = {}
    for subject in subjects:
        path = const.convert_result_dir + subject + '/'

        if os.path.exists(path):
            info = subject_map[subject]
            # 执行每个科目的解析
            info['func'].parse(path)
            enabled_subjects[subject] = info['name']
        else:
            print(f"{path}: 不存在，跳过")

    # 生成题库索引
    index.generate(enabled_subjects)

    end_time = time.time()
    print(f"\n生成数据耗时：{end_time - start_time} 秒")
