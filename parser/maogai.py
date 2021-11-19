from typing import List
import docx2txt
import os
import re
import const
import json


def parse(doc_dir: str):
    answer_locator = '答案'

    docx2txt.convert_dir(doc_dir)
    all_ti_count = 0
    for file in os.listdir(doc_dir):
        if not file.endswith('.txt'):
            continue
        # 题目列表，纯str
        raw_list: List[str] = []
        idx = 0
        f = open(doc_dir + '/' + file, 'r')
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            lines[i] = lines[i].replace(' ', ' ')
            # 根据题号分割题目
            if re.match(r'( )*[1-9]+.*', lines[i]):
                raw_list.append(lines[idx:i])
                idx = i
        raw_list.append(lines[idx:])
        raw_list = raw_list[1:]

        # 标准结构的题目列表
        ti_list = []
        for ti_raw in raw_list:
            # 解析标题
            ti_head = re.match(r'( )*[1-9]+[0-9]*( )*(、|\.|．)*( )*', ti_raw[0])
            title = ti_raw[0].replace(ti_head.group(), '').strip()

            # 解析答案
            answer_raw = ''
            for item in ti_raw:
                if answer_locator in item:
                    answer_raw = item.strip()
            answer = []
            for separator in ['】', '：']:
                if separator in answer_raw:
                    answer_raw = answer_raw.split(separator)[1].strip()
            if answer_raw in const.answer_convert_map:
                answer.append(const.answer_convert_map[answer_raw])
            else:
                for item in answer_raw:
                    if item not in const.answer_convert_map:
                        continue
                    answer.append(const.answer_convert_map[item])

            # 解析选项
            options = []
            answer_idx = -2
            idx_num = 0
            for li in ti_raw:
                if answer_locator in li:
                    answer_idx = idx_num
                idx_num += 1
            for option in ti_raw[1:answer_idx]:
                all_temp_options = re.compile(r'([A|B|C|D|E|F|G][ ]*[、|\.|．]*[ ]*[^\s]+)').findall(option)
                if all_temp_options:
                    for ii in all_temp_options:
                        replace_str = re.match(r'([A|B|C|D|E|F|G][ ]*[、|\.|．]*[ ]*)', ii)
                        if ii:
                            ii = ii.replace(replace_str.group(), '')
                        options.append(ii.strip())

            # 解析类型
            ti_type = 0
            answer_len = len(answer)
            if answer_len > 1:
                ti_type = 1
            if len(options) == 0 and answer_len == 1:
                options = ['对', '错']

            # 添加解析完成的题目到列表
            ti_list.append({
                'title': title,
                'options': options,
                'answer': answer,
                'type': ti_type
            })

        all_ti_count += len(ti_list)

        with open(doc_dir + file.replace('.txt', '.json'), 'w') as f:
            f.write(json.dumps(ti_list, ensure_ascii=False, indent=4))
    
    print(f'{doc_dir}: 共解析了{all_ti_count}道题')