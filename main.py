from fake_api import fake_api
from token_count import token_count

history = []

def main():

    while True:
        query = input("\n\nYou: ")
        history.append("user:" + query)
        history_string="".join(history)
        full_result = fake_api(history_string, 2500,True)

        history.append("chatgpt: " + full_result)

        history_string="".join(history)

        tokens=token_count(history_string)

    #fakeopen项目似乎没有token限制,正在测试,后续可能取消注释
        #如果token数超过2500，就清空历史记录
    # if tokens>2500:
    #         gaikuo=fake_api("请概括成500个英文单词以内,不要有多余内容: "+history_string,600,False)

    #         print("概括中...")

    #         history.clear()

    #         history.append("history:"+gaikuo)

if __name__ == '__main__':
    main()
