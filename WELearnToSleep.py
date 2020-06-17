import requests
import re
from sys import argv
from time import sleep
from random import randint
session = requests.Session()
print("**********  Created By Avenshy & SSmJaE  **********")
print("                 Version:0.4dev\n")
print("     https://github.com/Avenshy/WELearnToSleep")
print("   本软件遵守GPLv3协议，且免费、开源，禁止售卖!")
print("   本软件遵守GPLv3协议，且免费、开源，禁止售卖!")
print("   本软件遵守GPLv3协议，且免费、开源，禁止售卖!")
print("***************************************************\n")

def printline():
    print('-'*51)

# 获取账户密码
try:  # 直接从命令行中获取
    username, password = sys.argv[1], sys.argv[2]
except:
    loginmode=input('请选择登录方式: \n  1.账号密码登录\n  2.Cookie登录\n\n请输入数字1或2: ')
    printline()
    if loginmode=='1':
        username = input('请输入账号: ')
        password = input('请输入密码: ')
        # 登录模块
        print('登录中...')
        loginUrl = "https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx"
        response = session.get(loginUrl)
        lt = re.search('name="lt" value="(.*?)"', response.text).group(1)
        response = session.post(loginUrl, data={"username": username,
                                                "password": password,
                                                "lt": lt,
                                                "_eventId": "submit",
                                                "submit": "LOGIN"})
        if "请登录" in response.text:
            input("登录失败!!")
            exit(0)
        else:
            print("登录成功!!")
    elif loginmode=='2':
        try:
            cookie = dict(map(lambda x:x.split('=',1),input('请粘贴Cookie: ').split(";")))
        except:
            input('Cookie输入错误!!!')
            exit(0)
        for k,v in cookie.items():
              session.cookies[k]=v
    else:
        input('输入错误!!')
        exit(0) 
printline()
while True:
    # 查询课程信息
    url = "https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc"
    response = session.get(
        url, headers={"Referer": "https://welearn.sflep.com/2019/student/index.aspx"})
    if '\"clist\":[]}' in response.text:
        input('发生错误!!!可能是登录错误或没有课程!!!')
        exit(0)
    else:
        print('查询课程成功!!!')
        printline()
        print('我的课程: \n')
    back = response.json()["clist"]
    for i, course in enumerate(back, start=1):
        print(f'[NO.{i:>2}] 完成度{course["per"]:>3}% {course["name"]}')

    # 选择课程
    order = int(input("\n请输入需要完成的课程序号（上方[]内的数字）: "))
    cid = back[order - 1]["cid"]
    printline()
    print("获取单元中...")
    printline()
    # 刷课模块
    url = f"https://welearn.sflep.com/2019/student/course_info.aspx?cid={cid}"
    response = session.get(url)

    uid = re.search('"uid":(.*?),', response.text).group(1)
    classid = re.search('"classid":"(.*?)"', response.text).group(1)

    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx'
    response = session.get(url,params={'action':'courseunits','cid':cid,'uid':uid},headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx'})
    back = response.json()['info']

    # 选择单元 使用了WELearnToSleeep的代码
    print('[NO. 0]  按顺序完成全部单元课程')
    unitsnum = len(back)
    for i,x in enumerate(back,start=1):
        if x['visible']=='true':
            print(f'[NO.{i:>2d}]  [已开放]  {x["unitname"]}  {x["name"]}')
        else:
            print(f'[NO.{i:>2d}] ![未开放]! {x["unitname"]}  {x["name"]}')
    unitidx = int(input('\n\n请选择需要完成的单元序号（上方[]内的数字，输入0为按顺序刷全部单元）： '))
    printline()
    inputcrate = input('模式1:每个练习指定正确率，请直接输入指定的正确率\n如:希望每个练习正确率均为100，则输入 100\n\n模式2:每个练习随机正确率，请输入正确率上下限并用英文逗号隔开\n如:希望每个练习正确率为70～100，则输入 70,100\n\n请严格按照以上格式输入每个练习的正确率: ')
    if ',' in inputcrate:
        mycrate=eval(inputcrate)
        randommode=True
    else:
        mycrate=inputcrate
        randommode=False
    printline()
    # 伪造请求
    way1Succeed, way2Succeed, way1Failed, way2Failed = 0, 0, 0, 0

    ajaxUrl = "https://welearn.sflep.com/Ajax/SCO.aspx"
    infoHeaders = {
        "Referer": f"https://welearn.sflep.com/2019/student/course_info.aspx?cid={cid}",
    }

    if(unitidx == 0):
        i = 0
    else:
        i = unitidx - 1
        unitsnum = unitidx

    while True:
        response = session.get(
            f'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid={cid}&uid={uid}&unitidx={i}&classid={classid}', headers=infoHeaders)

        if "异常" in response.text or "出错了" in response.text:
            break

        for course in response.json()["info"]:
            if course['isvisible']=='false':  # 跳过未开放课程
                print(f'[!!跳过!!]    {course["location"]}')
            elif "未" in course["iscomplete"]:  # 章节未完成
                print(f'[即将完成]    {course["location"]}')
                if randommode is True:
                    crate=str(randint(mycrate[0],mycrate[1]))
                else:
                    crate=mycrate
                data = '{"cmi":{"completion_status":"completed","interactions":[],"launch_data":"","progress_measure":"1","score":{"scaled":"'+crate+'","raw":"100"},"session_time":"0","success_status":"unknown","total_time":"0","mode":"normal"},"adl":{"data":[]},"cci":{"data":[],"service":{"dictionary":{"headword":"","short_cuts":""},"new_words":[],"notes":[],"writing_marking":[],"record":{"files":[]},"play":{"offline_media_id":"9999"}},"retry_count":"0","submit_time":""}}[INTERACTIONINFO]'

                id = course["id"]
                session.post(ajaxUrl, data={"action": "startsco160928",
                                            "cid": cid,
                                            "scoid": id,
                                            "uid": uid
                                            },
                             headers={"Referer": f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"})
                response = session.post(ajaxUrl, data={"action": "setscoinfo",
                                                       "cid": cid,
                                                       "scoid": id,
                                                       "uid": uid,
                                                       "data": data,
                                                       "isend": "False" },
                                        headers={"Referer": f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"})
                print(f'>>>>>>>>>>>>>>正确率:{crate:>3}%',end='  ')
                if '"ret":0' in response.text:
                    print("方式1:成功!!!", end="  ")
                    way1Succeed += 1
                else:
                    print("方式1:失败!!!", end="  ")
                    way1Failed += 1

                response = session.post(ajaxUrl, data={"action": "savescoinfo160928",
                                                       "cid": cid,
                                                       "scoid": id,
                                                       "uid": uid,
                                                       "progress": "100",
                                                       "crate": crate,
                                                       "status": "unknown",
                                                       "cstatus": "completed",
                                                       "trycount": "0",
                                                       },
                                        headers={"Referer": f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"})
#                sleep(1) # 延迟1秒防止服务器压力过大
                if '"ret":0' in response.text:
                    print("方式2:成功!!!")
                    way2Succeed += 1
                else:
                    print("方式2:失败!!!")
                    way2Failed += 1
            else:  # 章节已完成
                print(f'[ 已完成 ]    {course["location"]}')

        if unitidx != 0:
            break
        else:
            i += 1
    if unitidx == 0:
        break
    else:
        print('本单元运行完毕！回到选课处！！\n\n\n\n')
        printline()

printline()
print(f"""
***************************************************
全部完成!!

总计:
方式1: {way1Succeed} 成功, {way1Failed} 失败
方式2: {way2Succeed} 成功, {way2Failed} 失败

https://github.com/Avenshy/WELearnToSleep
本软件遵守GPLv3协议，且免费、开源，禁止售卖!
本软件遵守GPLv3协议，且免费、开源，禁止售卖!
本软件遵守GPLv3协议，且免费、开源，禁止售卖!
**********  Created By Avenshy & SSmJaE  **********""")
input("Press any key to exit...")