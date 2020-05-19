# -*- coding:utf-8 -*-

from PBCSTU import PBCSTU

def workFlow(pbcstu):
    program_info = pbcstu.getProgram()
    for index,item in enumerate(program_info['datas']):
        print(f"【{index+1}】:{item['name']}")
    index = int(input('请输入要学习的项目序号： '))
    project_info = pbcstu.getProject(program_info,index)
    for index,item in enumerate(project_info['datas'][0]['tasks']):
        status = ['NoStart','Studying','Completed']
        print(f"【{index+1}】:{status[item['status']]}-->{item['name']}")
    index = int(input('请输入要学习的章节序号： '))
    chapter_info = pbcstu.getChapter(project_info,index)
    for index,item in enumerate(chapter_info['datas']):
        print(f"【{index+1}】:{item['status']}-->{item['title']}")
    index = int(input('请输入要学习的课程序号： '))
    knowledge_info =pbcstu.getKnowledge(chapter_info,index)
    print(f'知识点学习结果：{knowledge_info}')
    return


if __name__ == '__main__':
    pbcstu = PBCSTU()
    # userName = input('请输入用户名（支持短号和身份证号码）： ')
    # password = input('请输入密码： ')
    userName = '342923196111120015'
    password = '11120015'
    user_info = pbcstu.login(userName,password)
    if user_info:
        print(f"您正在以{user_info['departmentName']}【{user_info['fullName']}】的身份登录。")
        while 1:
            workFlow(pbcstu)
    else: 
        print("登录失败,请输入正确的用户名或密码。")