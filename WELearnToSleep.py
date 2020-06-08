import requests
import re
import sys
from time import sleep

print("**********  Created By Avenshy & SSmJaE  **********")
print("                 Version:0.3dev")
print("***************************************************\n")

# 获取账户密码
try:  # 直接从命令行中获取
    username, password = sys.argv[1], sys.argv[2]
except:
    username = input('Username: ')
    password = input('Password: ')
print("Login...")

# 登录模块
session = requests.Session()
loginUrl = "https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx"
response = session.get(loginUrl)
lt = re.search('name="lt" value="(.*?)"', response.text).group(1)
response = session.post(loginUrl, data={"username": username,
                                        "password": password,
                                        "lt": lt,
                                        "_eventId": "submit",
                                        "submit": "LOGIN"})
if "请登录" in response.text:
    print("Login Failed!!")
    exit(0)
else:
    print("Login Success!!", end="\n\n")

while True:
    # 查询课程信息
    url = "https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc"
    response = session.get(
        url, headers={"Referer": "https://welearn.sflep.com/2019/student/index.aspx"})
    back = response.json()["clist"]
    for i, course in enumerate(back, start=1):
        print(f'[NO.{i:>2}] 完成度{course["per"]:>3}% {course["name"]}')

    # 选择课程
    order = int(input("\n请输入需要完成的课程序号（上方[]内的数字）: "))
    cid = back[order - 1]["cid"]
    print("Running...")

    # 刷课模块
    url = f"https://welearn.sflep.com/2019/student/course_info.aspx?cid={cid}"
    response = session.get(url)

    uid = re.search('"uid":(.*?),', response.text).group(1)
    classid = re.search('"classid":"(.*?)"', response.text).group(1)

    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx'
    response = session.get(url,params={'action':'courseunits','cid':cid,'uid':uid},headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx'})
    back = response.json()['info']

    # 选择单元 直接复制了WELearnToSleeep的代码
    print('\n\n[NO. 0]  按顺序完成全部单元课程')
    i = 0
    unitsnum = len(back)
    for x in back:
        i+=1
        print('[NO.{:>2d}]  {}  {}'.format(i,x['unitname'],x['name']))
    unitidx = int(input('\n\n请选择需要完成的单元序号（上方[]内的数字，输入0为按顺序刷全部单元）： '))



    # 伪造请求
    way1Succeed, way2Succeed, way1Failed, way2Failed = 0, 0, 0, 0
    data = '{"cmi":{"completion_status":"completed","interactions":[],"launch_data":"","progress_measure":"1","score":{"scaled":"100","raw":"100"},"session_time":"0","success_status":"unknown","total_time":"0","mode":"normal"},"adl":{"data":[]},"cci":{"data":[],"service":{"dictionary":{"headword":"","short_cuts":""},"new_words":[],"notes":[],"writing_marking":[],"record":{"files":[]},"play":{"offline_media_id":"9999"}},"retry_count":"0","submit_time":""}}[INTERACTIONINFO]'

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
            if "未" in course["iscomplete"]:  # 章节未完成
                print(f'[未完成]    {course["location"]}')
                id = course["id"]
                session.post(ajaxUrl, data={"action": "startsco160928",
                                            "cid": cid,
                                            "scoid": id,
                                            "uid": uid,
                                            "nocache": "0.0429450926459094",
                                            },
                             headers={"Referer": f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"})
                response = session.post(ajaxUrl, data={"action": "setscoinfo",
                                                       "cid": cid,
                                                       "scoid": id,
                                                       "uid": uid,
                                                       "data": data,
                                                       "isend": "False", },
                                        headers={"Referer": f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"})
                if '"ret":0' in response.text:
                    print("[已模拟]    Way1:Success!!!", end="  ")
                    way1Succeed += 1
                else:
                    print("[已模拟]    Way1:Failed !!!", end="  ")
                    way1Failed += 1

                response = session.post(ajaxUrl, data={"action": "savescoinfo160928",
                                                       "cid": cid,
                                                       "scoid": id,
                                                       "uid": uid,
                                                       "progress": "100",
                                                       "crate": "100",
                                                       "status": "unknown",
                                                       "cstatus": "completed",
                                                       "trycount": "0",
                                                       },
                                        headers={"Referer": f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"})
                sleep(1) # 延迟1秒防止服务器压力过大
                if '"ret":0' in response.text:
                    print("Way2:Success!!!")
                    way2Succeed += 1
                else:
                    print("Way2:Fail   !!!")
                    way2Failed += 1
            else:  # 章节已完成
                print(f'[已完成]    {course["location"]}')

        if unitidx != 0:
            break
        else:
            i += 1
    if unitidx == 0:
        break
    else:
        print('本单元运行完毕！回到选课处！！\n\n\n\n')


print(f"""
***************************************************
Finish!!
Total counts:
way1: {way1Succeed} succeeded, {way1Failed} failed
way2: {way2Succeed} succeeded, {way2Failed} failed
**********  Created By Avenshy & SSmJaE  **********""")
input("Press any key to exit...")