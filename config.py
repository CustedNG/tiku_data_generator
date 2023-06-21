from parser import maogai, junli, jindaishi, not_implement

subject_map = {
    'maogai': {'name': '毛概', 'func': maogai},
    'clang1': {'name': 'C语言上', 'func': not_implement},
    'clang2': {'name': 'C语言下', 'func': not_implement},
    'junli': {'name': '军理', 'func': junli},
    'jinxiandaishi': {'name': '近代史', 'func': jindaishi},
    'sixiu': {'name': '思修', 'func': maogai},
    'makesi': {'name': '马克思', 'func': maogai},
    'feedback': {'name': 'Q&A', 'func': maogai},
}