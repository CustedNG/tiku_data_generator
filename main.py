import re
import os
import docx

answer_convert_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    '是': 0,
    '对': 0,
    '错': 1,
    '否': 1,
}


# [doc_dir]: 'xxx/'
def docx2txt(doc_dir):
    skip_files = []
    for i in os.listdir(doc_dir):
        if not i.endswith('.docx'):
            if not i.endswith('.txt') and not i.endswith('.json') and not i == '.DS_Store':
                skip_files.append(i)
            continue
        # 每个循环中docx文档和txt文档的命名
        gen_txt = doc_dir + i.replace('.docx', '.txt')
        # 新建和打开txt文档
        f = open(gen_txt, 'w')
        # 打开docx的文档并读入名为file的变量中
        file = docx.Document(doc_dir + i)
        # 输入docx中的段落数，以检查是否空文档
        para_len = len(file.paragraphs)
        if para_len < 10:
            print('段落数小于10，跳过')
            continue
        # 将每个段落的内容都写进去txt里面
        for para in file.paragraphs:
            f.write('\n')
            f.write(para.text)
        f.close()
        print('转换完成：' + i)

    if len(skip_files) > 0:
        raise Exception('\n以下文件由于格式问题，没有转换：\n' + str(skip_files))


def parse_maogai():
    doc_dir = 'maogai/'
    docx2txt(doc_dir)
    for file in os.listdir(doc_dir):
        if not file.endswith('.txt'):
            continue
        # 题目列表，纯str
        raw_list = []
        idxes = []
        f = open(doc_dir + '/' + file, 'r')
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            # 根据题号分割题目
            if re.match(r'[0-9]+(、|\.)', lines[i]):
                idx_len = len(idxes)
                if idx_len == 0 or idx_len == 1:
                    idxes.append(i)
                if len(idxes) == 2:
                    idxes[0] = idxes[1]
                    idxes[1] = i
                    raw_list.append(lines[idxes[0]:idxes[1]])

        # 标准结构的题目列表
        ti_list = []
        for ti_raw in raw_list:
            if len(ti_raw) == 0:
                continue
            title = ti_raw[0][2:].strip()
            options = []
            for option in ti_raw[1:-2]:
                options.append(option[2:].strip())
            answer = ti_raw[-2].replace('【正确答案】', '').strip()

            ti_list.append({
                'title': title,
                'options': options,
                'answer': answer,
                'type': 1
            })

        print(f'{file}: {len(ti_list)}题')
        print(f'第一题解析结果：{ti_list[0]}')


def parse_not_implement():
    raise NotImplementedError()


subject_map = {
    'maogai': {'name': '毛概', 'func': parse_maogai},
    'clang1': {'name': 'C语言上', 'func': parse_not_implement},
    'clang2': {'name': 'C语言下', 'func': parse_not_implement},
    'junli1': {'name': '军理上', 'func': parse_not_implement},
    'junli2': {'name': '军理下', 'func': parse_not_implement},
    'jinxiandaishi': {'name': '近代史', 'func': parse_not_implement},
    'sixiu': {'name': '思修', 'func': parse_not_implement},
    'makesi': {'name': '马克思', 'func': parse_not_implement},
}

if __name__ == '__main__':
    subjects = subject_map.keys()
    for subject in subjects:
        if os.path.exists(subject):
            info = subject_map[subject]
            print(f'开始解析{info["name"]}')
            info['func']()
