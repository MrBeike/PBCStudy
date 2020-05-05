# PBCStudy

[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/license-GPL3.0-red.svg)](LICENSE)

> 如同[webCourse](https://github.com/MrBeike/WebCourse-QTGUI)，PBCStudy只是又一款学习辅助脚本罢了。


## 如果你觉得OK,可以赞赏作者.
<img src='/tips.jpg'>


## 使用指南
- 使用源码
	- 1.下载源码:git clone https://github.com/MrBeike/PBCStudy.git(或者点击Clone or download按钮—>Download ZIP->解压缩)
	- 2.运行Demo:python launcher.py
    
- 体验可执行文件
	- 1.提供一个测试用文件。条件有限，暂时只提供在windows 7 64bit上打包的Demo。
	- 2.[百度网盘](https://pan.baidu.com/s/1afhx12Ky6Aa4Fqcnou20rQ) 提取码: p9sf

- 其他需要说明的
   - launcher.py是一个简单的Demo,可完成单个知识点的学习。
   - PBCSTU.py 为学习系统相关API接口。
   - 功能丰富和界面开发过段时间吧。
   - 欢迎Fork | pull request | whatever you like，请遵守法律法规及开源协议。


## 主要功能
- 自动学习(已实现)
- 自动测试(已实现)
- 一站到底(正在开发中)
- 还要啥？ contact me at lbbas@126.com

## 实现原理
### 自动学习
    修改studyTime参数值并Post.
### 自动测试
    读取exam page response json,解析并构造正确答案json包并Post.

## 脚本命名提示
    课程结构：所有项目(program)->单个项目(project)->单个章节(chapter)->单个知识点(knowledge)
    
    学习流程：登录(login)->获取所有项目(getProgram)->获取单个项目(getproject)->获取单个章节(getChapter)->获取单个知识点(getKnowledge)

<!-- ## 佛系青年
                春梦随云散
                飞花逐水流
                寄言众儿女
                何必觅闲愁

    Hope you get your own happines,sincerely.
    Cause I know it's hard, but it worths. -->