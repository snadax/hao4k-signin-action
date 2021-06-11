import requests
import os
import re

# hao4k 账户信息
username = os.environ["HAO4K_USERNAME"]
password = os.environ["HAO4K_PASSWORD"]
# 添加 server 酱通知
sckey = os.environ["SERVERCHAN_SCKEY"]
send_url = "https://sctapi.ftqq.com/%s.send" % (sckey)
send_content = 'Server ERROR'

# hao4k 签到 url
user_url = "https://www.hao4k.cn/member.php?mod=logging&action=login&phonelogin=no"
base_url = "https://www.hao4k.cn/"
signin_url = "https://www.hao4k.cn/plugin.php?id=k_misign:sign&operation=qiandao&formhash={formhash}&format=empty"
form_data = {
    'formhash': "",
    'referer': "https://www.hao4k.cn/",
    'username': username,
    'password': password,
    'questionid': "0",
    'answer': ""
}
inajax = '&inajax=1'

def run(form_data):
    s = requests.Session()
    s.headers = {
    "authority":"www.hao4k.cn" ,
    "cache-control":"max-age=0" ,
    "sec-ch-ua":"\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"" ,
    "sec-ch-ua-mobile":"?0" ,
    "upgrade-insecure-requests":"1" ,
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" ,
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
    "sec-fetch-site":"none" ,
    "sec-fetch-mode":"navigate" ,
    "sec-fetch-user":"?1" ,
    "sec-fetch-dest":"document" ,
    "accept-language":"zh-CN,zh;q=0.9" 
    }
    user_resp = s.get(user_url)
    login_text = re.findall('action="(.*?)"', user_resp.text)
    for loginhash in login_text:
        if 'loginhash' in loginhash:
            login_url = base_url + loginhash + inajax
            login_url = login_url.replace("amp;", "")
            print(login_url)
    form_text = re.search('formhash=(.*?)\'', user_resp.text)
    print(form_text.group(1))
    form_data['formhash'] = form_text.group(1)
    print(form_data)

    login_resp = s.post(login_url, data=form_data)
    test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html')
    if username in test_resp.text:
      print('login!')
    else:
      return 'login failed!'
    signin_text = re.search('formhash=(.*?)"', test_resp.text)
    signin_resp = s.get(signin_url.format(formhash=signin_text.group(1)))
    test_resp = s.get('https://www.hao4k.cn/k_misign-sign.html')
    if '您的签到排名' in test_resp.text:
      print('signin!')
    else:
      return 'signin failed!'


if __name__ == "__main__":
  signin_log = run(form_data)
  if signin_log is None:
    send_content = "hao4k 每日签到成功！"
    print('Sign in automatically!')
  else:
    send_content = signin_log
    print(signin_log)
  params = {'text': 'hao4k 每日签到结果通知：', 'desp': send_content}
  requests.post(send_url, params=params)
  print('已通知 server 酱')
