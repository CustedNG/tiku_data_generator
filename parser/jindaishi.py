from typing import List
import xlrd
import os
import const
import json

def parse(dir):
    skip_files: List[str] = []
    all_ti_dict: dict[str, dict] = {}
    ti_count = 0
    for file in os.listdir(dir):
        if not file.endswith('.xls'):
            if not file.endswith('.json'):
                skip_files.append(file)
            continue
        
        ti_list: List[dict] = []
        is_single = file.endswith('single.xls')
        data = xlrd.open_workbook(dir + file)
        table = data.sheets()[0]
        for i in range(2, table.nrows):
            if table.row_values(i)[0]:
                answers = []
                for item in table.cell(i, 6).value.strip():
                    if item in const.answer_convert_map:
                        answers.append(const.answer_convert_map[item])
                ti_list.append({
                    'question': table.cell(i, 1).value,
                    'options': [table.cell(i, 2).value, table.cell(i, 3).value, table.cell(i, 4).value, table.cell(i, 5).value],
                    'answer': answers,
                    'type': 0 if is_single else 1
                })
        if file.split('-')[0] in all_ti_dict.keys():
            all_ti_dict[file.split('-')[0]].append(ti_list)
        else:
            all_ti_dict[file.split('-')[0]] = ti_list
        ti_count += len(ti_list)
    
    for unit_idx in all_ti_dict:
        with open(dir + unit_idx + '.json', 'w') as f:
            f.write(json.dumps(all_ti_dict[unit_idx], ensure_ascii=False, indent=4))
    print(f'{dir}：共解析了{ti_count}道题')
        
        
    if len(skip_files) > 0:
        raise Exception('skip files:', skip_files)