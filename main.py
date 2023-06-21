import os
import time

import index, config, const

if __name__ == '__main__':
    start_time = time.time()

    subjects = config.subject_map.keys()
    enabled_subjects: dict = {}
    for subject in subjects:
        path = const.convert_result_dir + subject + '/'

        if os.path.exists(path):
            info = config.subject_map[subject]
            # 执行每个科目的解析
            info['func'].parse(path)
            enabled_subjects[subject] = info['name']
        else:
            print(f"{path}: 不存在，跳过")

    # 生成题库索引
    index.generate(enabled_subjects)

    end_time = time.time()
    print(f"\n生成数据耗时：{end_time - start_time} 秒")
