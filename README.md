# 题库数据生成器
主要将.docx/.xls/.txt文档中的题目，提取并生成json格式的题库数据。


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
- 索引的链接为：{BACKEND_URL}/res/tiku/index.json，如示例：https://v2.custed.lolli.tech/res/tiku/index.json
- 每个单元的题目的链接为：{BACKEND_URL}/res/tiku/{该科目的名称的拼音}/{data}，如示例：https://v2.custed.lolli.tech/res/tiku/maogai/1.json


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
