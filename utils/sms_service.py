from melipayamak import Api
def SMS(Text_sms,number):
    username = '09301699559'
    password = 'P@3LB'
    api = Api(username,password)
    sms = api.sms()
    to = f'0{number}'
    _from = '50004001699559'
    text = Text_sms
    response = sms.send(to,_from,text)
    print(response)