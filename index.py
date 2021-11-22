import time
import const
import os
import json

index_path = const.convert_result_dir + 'index.json'


def update_index(file_name: str, title: str, file_path: str):
    '''
    param file_name: 文件名
    param title: 标题
    param file_path: 文件路径
    return: None
    '''
    data = {}
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('{}')
    with open(file_path) as f:
        raw = f.read()
        data = json.loads(raw if raw else '{}')
        data[file_name] = title
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


def generate(enabled_subjects: dict):
    '''
    param enabled_subjects: 启用的科目, 如：{'maogai': '毛概'}
    return: None
    '''
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f'\n{time_now}: 开始生成索引\n')

    index_dict = {}

    if os.path.exists(index_path):
        with open(index_path) as f:
            raw = f.read()
            index_dict = json.loads(raw if raw else '{}')

    index_dict['version'] = time_now

    for subject in enabled_subjects.keys():
        subject_path = const.convert_result_dir + subject + '/'
        subject_files = os.listdir(subject_path)
        content = []
        subject_length = 0

        # 加载每个单元的标题map
        unit_title_map = {}
        if 'index.json' in subject_files:
            with open(subject_path + 'index.json', 'r', encoding='utf-8') as f:
                unit_title_map = json.load(f)

        for file in subject_files:
            if file.endswith('.json'):
                if file == 'index.json':
                    continue

                subject_length += 1

                radio = 0
                multiple = 0
                decide = 0
                fill = 0

                unit_path = subject_path + file
                with open(unit_path, 'r', encoding='utf-8') as f:
                    unit_ti = json.load(f)

                    for ti in unit_ti:
                        if ti['type'] == 0:
                            radio += 1
                        elif ti['type'] == 1:
                            multiple += 1
                        elif ti['type'] == 2:
                            fill += 1
                        elif ti['type'] == 3:
                            decide += 1

                    have_title = file in unit_title_map.keys()
                    if not have_title:
                        print(f"{unit_path}：没有索引标题")
                    content.append({
                        'title': unit_title_map[file] if have_title else file.split('.')[0],
                        'radio': radio,
                        'multiple': multiple,
                        'decide': decide,
                        'fill': fill,
                        'data': file,
                        'index': float(file.replace('.json', ''))
                    })
        # 单元排序
        content.sort(key=lambda x: x['index'])
        for c in content:
            c.pop('index')

        subject_dict = {
            'id': subject,
            'chinese': enabled_subjects[subject],
            'length': subject_length,
            'content': content
        }

        subject_index = -1
        for c in index_dict['content']:
            subject_index += 1
            if c['id'] == subject:
                break

        if subject_index == -1:
            index_dict['content'].append(subject_dict)
        else:
            index_dict['content'][subject_index] = subject_dict

        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_dict, f, ensure_ascii=False, indent=4)

    print(f"\n{index_path}: 已生成 {len(index_dict['content'])} 科的索引")
