import itchat  
from iexfinance.stocks import Stock, get_historical_data

class GetData(object):     #一个类，用于创建股票对象

    def __init__(self,code=None):  #用于创建对象
        self.aapl = Stock(code)
        # 成交量
        self.data = get_historical_data(code, output_format='pandas').iloc[-1]
        self.aapl2 = Stock(code, output_format='pandas')

    def price(self):     #用来查询价格
        price_data = self.aapl.get_price()
        return price_data

    def volume(self):    #查询销量
        volume_data = self.data.loc["volume"]
        return volume_data

    def markstCap(self):     #查询市值
        #  "市值",
        marketCap_com = self.aapl2.get_quote(displayPercent=True).loc["marketCap"].values
        marketCap_data = marketCap_com[0] if marketCap_com else ''
        return marketCap_data


user_session = []
# 文字消息
@itchat.msg_register(['Text'])      #装饰器，用于扩充函数的功能，是微信提供的功能，可以接受文本消息
def text_reply(msg):
    info_list = ["股价", "市值", "成交量"]    #可查询的内容
    # 单轮查询的
    msg_list = msg['Text'].split("的")    #判断有没有“的”字
    if len(msg_list) == 2 :
        # 创建对象
        try:
            code = GetData(msg_list[0])
        except:
            return "输入错误"
        user_session.append(code)   # 保存存储对象
        if not user_session:
            return "请先输入你想了解的公司"
        message = "该公司的{}是:\n".format(msg_list[-1])     #-1代表最后一次保存的对象，即最后一次输入的内容
        if msg_list[-1] == "股价":
            message += str(user_session[-1].price())
        elif msg_list[-1] == "市值":
            message += str(user_session[-1].markstCap())
        elif msg_list[-1] == "成交量":
            message += str(user_session[-1].volume())
        return message
    else:
        # 多轮查询的
        if msg['Text'] not in info_list:
            # 先创建对象,如果创建成功,给出提示信息
            try:
                code = GetData(msg['Text'])
            except:
                return "输入错误"
            user_session.append(code)
            return "您想知道关于这个公司什么信息1.股价 2.成交量 3.市值"

        else:
            # 判断session
            if not user_session:
                return "请先输入你想了解的公司"
            message = "该公司{}是:\n".format(msg['Text'])
            if msg['Text'] == "股价":
                message += str(user_session[-1].price())
            elif msg['Text'] == "市值":
                message += str(user_session[-1].markstCap())
            elif msg['Text'] == "成交量":
                message += str(user_session[-1].volume())
            return message

# 执行当前文件
if __name__ == '__main__':
    itchat.auto_login()          #用于微信登陆、接受信息
    friends = itchat.get_friends(update=True)[0:]
    Name = {}
    Nic = []
    User = []
    for i in range(len(friends)):
        Nic.append(friends[i]["NickName"])
        User.append(friends[i]["UserName"])
    for i in range(len(friends)):
        Name[Nic[i]] = User[i]
    itchat.run()             #执行之后，弹出二维码
