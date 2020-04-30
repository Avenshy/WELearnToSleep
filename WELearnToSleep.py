import requests
import json
print('**********  Created By Avenshy  **********\nVersion:0.2dev\n')
session = requests.Session()
username = input('Username: ')
password = input('Password: ')
print('Login...',end=' ')
url = 'https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx'
req = session.get(url)
lt = req.text[req.text.find('name="lt" value="') + 17:req.text.find('name="lt" value="') + 17 + 76]
url = 'https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx'
req = session.post(url,data={'username':username,'password':password,'lt':lt,'_eventId':'submit','submit':'LOGIN'})
if('请登录' in req.text):
    print('Fail!!')
    exit(0)
print('Success!!',end='\n\n')
url = 'https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc'
req = session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/index.aspx'})
back = json.loads(req.text)['clist']
i = 1
for x in back:
    print('[id:' + str(i) + ']   完成度' + str(x['per']) + '%  ' + x['name'])
    i+=1
i = int(input('\n请输入需要完成的课程id: '))
print('Running...')
cid = str(back[i - 1]['cid'])
url = 'https://welearn.sflep.com/2019/student/course_info.aspx?cid=' + cid
req = session.get(url)
uid = req.text[req.text.find('"uid":') + 6:req.text.find('"',req.text.find('"uid":') + 7) - 2]
classid = req.text[req.text.find('classid=') + 8:req.text.find('&',req.text.find('classid=') + 9)]
i = 0
way1su, way2su, way1fa, way2fa = 0, 0, 0, 0
data = '{"cmi":{"completion_status":"completed","interactions":[],"launch_data":"","progress_measure":"1","score":{"scaled":"100","raw":"100"},"session_time":"0","success_status":"unknown","total_time":"0","mode":"normal"},"adl":{"data":[]},"cci":{"data":[],"service":{"dictionary":{"headword":"","short_cuts":""},"new_words":[],"notes":[],"writing_marking":[],"record":{"files":[]},"play":{"offline_media_id":"9999"}},"retry_count":"0","submit_time":""}}[INTERACTIONINFO]'
url = 'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid=' + cid + '&uid=' + uid + '&unitidx=' + str(i) + '&classid=' + classid
req = session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx?cid=' + cid})
while '异常' not in req.text and '出错了' not in req.text:
    back = json.loads(req.text)['info']
    for x in back:
        id = x['id'] 
        if('未' in x['iscomplete']):
            print(x['location'] + '...',end='')
            url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
            req = session.post(url,data={'action':'startsco160928','cid':cid,'scoid':id,'uid':uid,'nocache':'0.0429450926459094'},headers={'Referer':'https://welearn.sflep.com/Student/StudyCourse.aspx?cid={}&classid={}&sco={}'.format(cid, classid, id)})
            req = session.post(url,data={'action':'setscoinfo','cid':cid,'scoid':id,'uid':uid,'data':data,'isend':'False'},headers={'Referer':'https://welearn.sflep.com/Student/StudyCourse.aspx?cid={}&classid={}&sco={}'.format(cid, classid, id)})
            if('"ret":0' in req.text):
                print('Way1:Success!!!',end='')
                way1su += 1
            else:
                print('Way1:Fail!!!',end='')
                way1fa += 1
            url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
            req = session.post(url,data={'action':'savescoinfo160928','cid':cid,'scoid':id,'uid':uid,'progress':'100','crate':'100','status':'unknown','cstatus':'completed','trycount':'0'},headers={'Referer':'https://welearn.sflep.com/Student/StudyCourse.aspx?cid={}&classid={}&sco={}'.format(cid, classid, id)})
            if('"ret":0' in req.text):
                print('Way2:Success!!!')
                way2su += 1
            else:
                print('Way2:Fail!!!')
                way2fa += 1
        else:
            print(x['location'] + '   ' + x['iscomplete'])
    i+=1
    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid=' + cid + '&uid=' + uid + '&unitidx=' + str(i) + '&classid=' + classid
    req = session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx?cid=' + cid})
print('Finish!!\n')
print('Total counts:\n')
print('way1: {} succeeded, {} failed'.format(way1su, way1fa))
print('way2: {} succeeded, {} failed'.format(way2su, way2fa))
print("\n\n\n**********  Created By Avenshy  **********\n\n\n")
input("Press any key to exit...")
