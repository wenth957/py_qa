# 基于知识图谱的电影问答系统

最近在学习图数据库, 记录一下学习内容

├─data  原始数据库包括 noe4j数据库csv文件、 训练标签数据 、自定义词典

├─models 主要实现两个类
  - TextClassification.py 问句意图分类
  - QuestionTemplate.py   问句模板匹配、查询neo4j给出答案

├─scripts 处理数据脚本
  
  - csv2neo.py 构建图数据库neo4j
  - load_train.py 构造训练数据 

├─services web聊天界面, 主要使用flask框架调用接口
   - qa_service.py
   ├─static 前端文件
   │  ├─css
   │  ├─images
   │  └─js
   └─templates
      - index.html
         
└─utils 一些公用的处理函数


