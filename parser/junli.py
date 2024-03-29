from typing import List
import xlrd
import os
import const
import json


def parse(dir):
    '''
    param dir: 文件目录
    return: None
    '''
    skip_files: List[str] = []
    ti_count = 0
    for file in os.listdir(dir):
        if not file.endswith('.xls'):
            if not file.endswith('.json'):
                skip_files.append(file)
            continue

        ti_list: dict = []
        data = xlrd.open_workbook(dir + file)
        table = data.sheets()[0]
        if '3' in file:
            for i in range(1, table.nrows):
                if table.row_values(i)[0]:
                    ti_list.append({
                        'question': table.cell(i, 1).value,
                        'options': ['对', '错'],
                        'answer': 0 if table.cell(i, 2).value == '对' else 1,
                        'type': 3
                    })
        elif '1' in file:
            for i in range(1, table.nrows):
                if table.row_values(i)[0]:
                    ti_list.append({
                        'question': table.cell(i, 1).value,
                        'options': [table.cell(i, 2).value, table.cell(i, 3).value, table.cell(i, 4).value, table.cell(i, 5).value],
                        'answer': [const.answer_convert_map[table.cell(i, 6).value.strip()]],
                        'type': 0
                    })
        elif '2' in file:
            for i in range(1, table.nrows):
                if table.row_values(i)[0]:
                    answers = []
                    for item in table.cell(i, 6).value:
                        if item in const.answer_convert_map:
                            answers.append(const.answer_convert_map[item])
                    ti_list.append({
                        'question': table.cell(i, 1).value,
                        'options': [table.cell(i, 2).value, table.cell(i, 3).value, table.cell(i, 4).value, table.cell(i, 5).value],
                        'answer': answers,
                        'type': 1
                    })
        else:
            print('Unknown file type: ' + file)

        ti_count += len(ti_list)
        with open(dir + file.replace('.xls', '.json'), 'w') as f:
            f.write(json.dumps(ti_list, ensure_ascii=False, indent=4))

    print(f'{dir}：解析了{ti_count}道题')

    if len(skip_files) > 0:
        print('skip files:', skip_files)
