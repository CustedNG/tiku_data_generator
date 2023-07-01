# 题库数据生成器
主要将 `.docx/.xls/.txt` 文档中的题目，提取并生成 `json` 格式的题库数据。

## 使用
1. 复制 `.docx` 等类型文件至 `convert/xxx` 内 （xxx 为科目id）
2. （如果是 `.docx`）`python3 docx2txt.py convert/xxx`
3. `python3 main.py`
4. 查看 `.json` 是否存在问题，如果存在问题，对照原 `.docx` 修改生成的 `.txt` （如果有问题，跳转3）
5. （可选，如果只需要生成索引）`python3 index.py`

## 结构
- main.py 解析
- index.py 生成index
- parser/*.py 解析器
- convert/* 数据源+解析后的输出，需要把该文件夹的内容上传到服务器

## 数据源规范
#### 总体
需要换行仅有：`题目结束后，每个选项，难易，答案`

#### 题目
以数字开头，后面接`.、．`三种标点，并跟上题目内容，例如：
```
1.人类历史上以公有制为基础建立的法律是什么（   ）。
1、人类历史上以公有制为基础建立的法律是什么（   ）。
1．人类历史上以公有制为基础建立的法律是什么（   ）。
```
题目中间不能存在换行，例如：
```
1.人类历史上以公有
制为基础建立的法律是什么（   ）。
```

#### 选项
以ABCDEFG开头，例如：
```
A 权利公平
B.机会公平
C．规则公平
D、救济公平  
```

#### 难易与答案
难易可以不存在，但答案必需。以下都可：
```
难易程度：易     
答案：ABCD

【正确答案】C
【难易程度】易

【正确答案是】：A

【答案】：A
```


## JSON结构规范
#### 题库索引
```json
{
    "version": "2021.08.06",
    "content": [
        {
            "id": "maogai",
            "length": 18,
            "chinese": "毛概",
            "content": [
                {
                    "title": "第一章 毛泽东思想及其历史地位",
                    "radio": 30,
                    "multiple": 18,
                    "decide": 12,
                    "fill": 0,
                    "data": "1.json"
                },
            ]
        }
    ]
}
```
字段 | 说明 
---- | ---- 
version | 版本号，更新时间
content | 题库索引内容，每个题库一个索引
---- | ----
content.id | 题库id
content.length | 题目总数
content.chinese | 题库中文名
content.content | 题目列表
---- | ----
content.content.title | 题库标题 
content.content.radio | 单选题数量 
content.content.multiple | 多选题数量 
content.content.decide | 判断题数量 
content.content.fill | 填空题数量 
content.content.data | 题目数据文件名 

**注意事项**：
- 索引的链接为：{BACKEND_URL}/res/tiku/index.json，如示例：https://WEBSITE/res/tiku/index.json
- 每个单元的题目的链接为：{BACKEND_URL}/res/tiku/{该科目的名称的拼音}/{data}，如示例：https://WEBSITE/res/tiku/maogai/1.json


#### 单个题目

```json
{
  "options": [
    "粟裕",
    "aaa",
    "bbb",
  ],
  "question": "下面哪一位是共和国十大将军之一(　　)",
  "answer": [
      0
  ],
  "type": 0
}
```
属性 | 类型 | 说明 
---- | ---- | ---- 
options | string[] 或 int[] | 选项 
question | string | 题目 
answer | int[] | 答案 
type | int | 题目类型 

**注意事项**：
- answer：可能是数组，也可能是单个数字。
- type：0为单选，1为多选，2为填空，3为判断
