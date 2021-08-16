# -*- coding:utf-8 -*-

import requests
import re,random,base64,json

from Functions import *

'''
Tips:
课程结构：所有项目(program)->单个项目(project)->单个章节(chapter)->单个知识点(knowledge)[视频(video)/测试(exam)]
学习流程：登录(login)->获取所有项目(getProgram)->获取单个项目(getproject)->获取单个章节(getChapter)->获取单个知识点(getKnowledge)[视频(video)测试(exam)]->学习(study)/测试(exam)
'''

class Study:
    def __init__(self):
        self.s = requests.session()
        self.store = {}
        self.base_url = "some secret url" # https://api.XX.cn/v1

    def login(self,userName,password):
        '''
        login to system.
        params: userName: str, the user'name. could be shortcode,ID,email if binded.
        params：password: str, as you see.
        return: user_info_dict： dict store user's info(success) | False(error)
        '''
        headers = {
            # 'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.12(0x17000c2d) NetType/WIFI Language/zh_CN',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1'
        }

        # 获取登陆页面
        login_url = f'{self.base_url}/users/tokens?random={random.random()}'
        # password&userName为base64加密后的结果
        userName = base64.b64encode(userName.encode('utf-8')).decode('utf-8')
        password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        # Post json
        login_json = {
            "deviceId":"",
            "isCheck":1,
            "nb":1,
            "password":password,
            "userName":userName,
            "domainName":"www.pbcstu.cn"
            }
        login_page= self.s.post(login_url,headers=headers,json=login_json)
        if login_page.status_code == 200:
            user_info_json = login_page.content.decode('utf-8')
             # 将json转成dict(see file login_response.json)
            user_info_dict = json.loads(user_info_json)
            keys = ['token','userId','fullName','departmentName','openId']
            self.store = dictPicker(self.store, user_info_dict,*keys)
        else:
            user_info_dict = False
        return user_info_dict

    def getProgram(self):
        '''
        get the user's registed projects(program).
        return: program_info_dict: dict that store all project_info(success) | False(error)
        '''
        # 获取token并写入headers
        token = self.store['token']
        self.s.headers.update({'token':token})
        # 获取用户注册的项目
        program_url = f'{self.base_url}/mt/myprojects'
        program_data = {
                'limit':'10',
                'offset':'0',
                'orgId':'',
                'type':'0',
                'status':'1',
                'direction':'DESC',
                'random':random.random()
        }
        program_page = self.s.get(program_url,params = program_data)
        if program_page.status_code == 200:
            program_info_json = program_page.content.decode('utf-8')
            # 将json转成dict(see file program_response.json)
            program_info_dict = json.loads(program_info_json)
        else:
            program_info_dict = False
        return program_info_dict

    def getProject(self,program_info_dict,index):
        '''
        get the specify project's info.[program->project]
        params: program_info_dict: dict, dict that contains all projects'info.
        params: index: int, the index of the project in program_info_dict.(from 1)
        return: project_info_dict: dict the store project_info(success) | False(error)
        '''
        the_project = program_info_dict['datas'][index - 1]
        project_id = the_project['id']
        project_url = f'{self.base_url}/mt/projects/{project_id}/myperiods'
        project_data = {
            'isNeedTask':'1',
            'checkMember':'0',
            'isApplyId':'0',
            'random':random.random()
        }
        project_page = self.s.get(project_url,params=project_data)
        if project_page.status_code == 200:
            project_info_json = project_page.content.decode('utf-8')
            # see file project_response.json
            project_info_dict = json.loads(project_info_json)
        else:
            project_info_dict = False
        return project_info_dict
    
    def getChapter(self,project_info_dict,index):
        '''
        get the specify chapter's info.[program->project->chapter]
        params: program_info_dict: dict, dict that contains all chapters'info.
        params: index: int, the index of the chapter in project_info_dict.(from 1)
        return: chapter_info_dict: dict the store chapter_info(success) | False(error)
        '''
        # FIXME 这里的json构造又问题，没必要多一层。反馈。
        the_chapter = project_info_dict['datas'][0]['tasks'][index -1]
        relatedCourse = the_chapter['relatedCourse']
        chapter_summary_url = f'{self.base_url}/knowledges/{relatedCourse}?studyPlanId=&random={random.random()}'
        chapter_summary_page = self.s.get(chapter_summary_url)
        if chapter_summary_page.status_code == 200:
            chapter_summary_json = chapter_summary_page.content.decode('utf-8')
            # see file chapter_summary_respinse.json
            chapter_summary_dict = json.loads(chapter_summary_json)
            sourceId = chapter_summary_dict['sourceId']
            masterID = chapter_summary_dict['masterId']
            self.store['packageId'] = sourceId
            chapter_url = f'{self.base_url}/subknowledges/{sourceId}?masterId={masterID}&random={random.random()}'
            chapter_page = self.s.get(chapter_url)
            if chapter_page.status_code == 200:
                chapter_info_json = chapter_page.content.decode('utf-8')
                # see file chapter_response.json
                chapter_info_dict = json.loads(chapter_info_json)
        else:
            chapter_info_dict = False
        return chapter_info_dict

    # FIXME 是否将处理函数独立出来
    def getKnowledge(self,chapter_info_dict,index):
        '''
        get the specify knowledge's info.[program->project->chapter->knowledge]
        And get it done.[study for the Video,exam for the OteExam]
        params: chapter_info_dict: dict, dict that contains all knowledges'info.
        params: index: int, the index of the knowledge in chapter_info_dict.(from 1)
        return: boolean, True(success) | False(error)
        '''
        the_knowledge = chapter_info_dict['datas'][index - 1]
        knowledge_id = the_knowledge['id']
        # userKnowledgeId = the_knowledge['userKnowledgeId'] exam获取方式修改,拟弃用。
        file_type = the_knowledge['fileType']  # 暂时收集到[Video,OteExam]
        status = the_knowledge['status'] # 暂时收集到[NoStart,Studying，Completed]
        if status != 'Completed':
            if file_type == 'Video':
                video_url = f'{self.base_url}/knowledge/{knowledge_id}?random={random.random()}'
                video_json = {
                        "sourceType": "SingleStudy",
                        "packageId": self.store['packageId'],
                        "planId": ""
                }
                video_page = self.s.post(video_url,json=video_json)
                if video_page.status_code == 200:
                    video_info_json = video_page.content.decode('utf-8')
                    # see file video_response.json
                    video_info_dict = json.loads(video_info_json)
                    orgGroupId = video_info_dict['orgGroupId']
                    userId =self.store['userId']
                    orginalKnowledgeId = video_info_dict['orginalKnowledgeId']
                    packageId = self.store['packageId']
                    studyTime = video_info_dict['standardStudyHours'] *60
                    viewSchedule = random.uniform(30,studyTime)
                    wx_study_json = {
                        "OrgID": orgGroupId,
                        "UserID": userId,
                        "KnowledgeID": orginalKnowledgeId,
                        "MasterID": "",
                        "MasterType": "",
                        "PackageID": packageId,
                        "StudyTime":studyTime,
                        "Type": "1",  
                        "viewSchedule": viewSchedule
                    }
                    study_url = f'{self.base_url}/study?random={random.random()}'
                    study_page = self.s.post(study_url,json=wx_study_json)
                    if study_page.status_code == 200:
                        return True
                    else:
                        return False
                else:
                    return study_page.content.decode('utf-8')
            elif file_type == 'OteExam':
                # FIXME examType=MixedTraining?唯一固定值？
                exam_preview_url = f'{self.base_url}/ote/web/examarrange/{knowledge_id}/preview?packageId={self.store["packageId"]}&userExamMapId=&examType=MixedTraining&masterId=&random={random.random()}'
                exam_preview_page = self.s.get(exam_preview_url)
                if exam_preview_page.status_code == 200:
                    exam_preview_info_json = exam_preview_page.content.decode('utf-8')
                    exam_preview_info_dict = json.loads(exam_preview_info_json)
                    userExamMapId = exam_preview_info_dict['userExamMapId']
                else:
                    return exam_preview_page.content.decode('utf-8')
                exam_url = f'{self.base_url}/ote/web/examarrange/{knowledge_id}/userexammap/{userExamMapId}/start?&random={random.random()}'
                exam_page_option = self.s.options(exam_url)
                exam_page = self.s.get(exam_url)
                print(exam_page.status_code)
                if exam_page.status_code == 200:
                    exam_info_json = exam_page.content.decode('utf-8')
                    # see file exam_response.json
                    exam_info_dict = json.loads(exam_info_json)
                    # 获取相关键值,构建post包
                    userExamId =  exam_info_dict['userExamId']
                    arrangeId =  exam_info_dict['arrangeId']
                    userExamMapId =  exam_info_dict['userExamMapId']
                    uniqueId =  exam_info_dict['uniqueId']
                    # 判断是否限时 
                    isControlTime = exam_info_dict['isControlTime']
                    duration =  exam_info_dict['duration']
                    # 解析答案，构建post包
                    exams =  exam_info_dict['combinedQuestions']
                    answers = []
                    for exam in exams:
                        questionType = exam['QuestionType'] # 暂时收集到[SingleChoice,MultiChoice,Judge]
                        if questionType in ['SingleChoice','MultiChoice']:
                            choices = exam['ChoiceItems']
                        elif questionType == 'Judge':
                            choices = exam['JudgeItems']
                        answer = []
                        for choice in choices:
                            if choice['IsAnswer'] == True:
                                answer.append(choice['ID'])
                        answer_dict = {
                            "questionId":exam['ID'],
                            "questionType": exam['QuestionType'],
                            "index": exam['OrderIndex'],
                            "answer": answer,
                            "attach": []
                        }
                        answers.append(answer_dict)
                    # 判断是否限时? duration:200 (0为不限时，1为限时。200是10题大概的用时。)
                    if isControlTime == 0:
                        duration = 200
                    usedTime = random.randint(duration/2,duration)
                    exams_answer = {
                        'usedTime':usedTime,
                        'answers':answers,
                        "deviceID": None,
                        "submitType": 0,
                        "uniqueId": uniqueId
                        }
                    exam_submit_url = f'{self.base_url}/ote/web/userexam/{userExamId}/submit?arrangeId={arrangeId}&userExamMapId={userExamMapId}&random={random.random()}'
                    exam_submit_page = self.s.post(exam_submit_url,json=exams_answer)
                    # 204 No Content
                    if exam_submit_page.status_code == 204:
                        exam_result_url = f'{self.base_url}/ote/web/userexam/{userExamId}/statistics?arrangeId={arrangeId}&userExamMapId=&random={random.random()}'
                        exam_result_page = self.s.get(exam_result_url)
                        if exam_result_page.status_code == 200:
                            exam_result_info_json = exam_result_page.content.decode('utf-8')
                            # see file exam_result_response.json
                            exam_result_info_dict = json.loads(exam_result_info_json)
                            isPass = exam_result_info_dict['isPass']
                            # maxScore = exam_result_info_dict['maxScore']
                            if isPass == 1:
                                return True
                            else:
                                return False
                    else:
                        return exam_submit_page.content.decode('utf-8')
                else:
                    return exam_page.content.decode('utf-8')
        else:
            return '该知识点已经完成'