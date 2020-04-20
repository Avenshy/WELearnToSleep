import requests
import json
import os

print('**********  Created By Avenshy  **********')

session=requests.Session()
username=input('Username: ')
password=input('Password: ')
print('Login...',end=' ')
url='https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx'
req=session.get(url)
lt=req.text[req.text.find('name="lt" value="')+17:req.text.find('name="lt" value="')+17+76]
url='https://sso.sflep.com/cas/login?service=http%3a%2f%2fwelearn.sflep.com%2f2019%2fuser%2floginredirect.aspx'
req=session.post(url,data={'username':username,'password':password,'lt':lt,'_eventId':'submit','submit':'LOGIN'})

if('请登录' in req.text):
    print('Fail!!')
    os.system('pause')
    exit(0)

print('Success!!',end='\n\n')
url='https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc'
req=session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/index.aspx'})
back=json.loads(req.text)['clist']
i=1
for x in back:
    print('['+str(i)+']   Finish:'+str(x['per'])+'%   '+x['name'])
    i+=1
i=int(input('\nWhich one you want to finish? Press the number. ').upper())
print('Running...')
cid=str(back[i-1]['cid'])
url='https://welearn.sflep.com/2019/student/course_info.aspx?cid='+cid
req=session.get(url)
uid=req.text[req.text.find('"uid":')+6:req.text.find('"',req.text.find('"uid":')+7)-2]
classid=req.text[req.text.find('classid=')+8:req.text.find('&',req.text.find('classid=')+9)]
i=0
url='https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid='+cid+'&uid='+uid+'&unitidx='+str(i)+'&classid='+classid
req=session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx?cid='+cid})
while '异常' not in req.text and '出错了' not in req.text:
    back=json.loads(req.text)['info']
    for x in back:
        id=x['id'] 
        if('未' in x['iscomplete']):
            print(x['location']+'...',end='')
            url='https://welearn.sflep.com/Ajax/SCO.aspx'
            req=session.post(url,data={'action':'startsco160928','cid':cid,'scoid':id,'uid':uid})
            url='https://welearn.sflep.com/Ajax/SCO.aspx'
            req=session.post(url,data={'action':'savescoinfo160928','cid':cid,'scoid':id,'uid':uid,'progress':'100','crate':'100','status':'unknown','cstatus':'completed','trycount':'100'},headers={'Referer':'https://welearn.sflep.com/Student/StudyCourse.aspx'})
            if('"ret":0' in req.text):
                print('Success!!')
            else:
                print('Fail!!'+req.text)
        else:
            print(x['location']+'   '+x['iscomplete'])
    i+=1
    url='https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid='+cid+'&uid='+uid+'&unitidx='+str(i)+'&classid='+classid
    req=session.get(url,headers={'Referer':'https://welearn.sflep.com/2019/student/course_info.aspx?cid='+cid})
print('\n\nFinish!!')
print('**********  Created By Avenshy  **********')