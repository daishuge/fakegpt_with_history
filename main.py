from fake_api import fake_api
from token_count import token_count

history = []    #历史记录储存

def main():

    while True:
        query = input("\n\nYou: ")
        if query == "clear":
            history.clear()
            continue

        history.append("user:" + query)
        history_string="".join(history)
        full_result = fake_api(history_string, 2500,True,1)

        history.append("chatgpt: " + full_result)

        history_string="".join(history)

        tokens=token_count(history_string)
'''
        如果你使用openai官方api,请去掉注释
        if tokens>10000:
                print("概括中...")

                history_string="".join(history)

                gaikuo=fake_api("请把这段文字概括成1000个英文单词以内,不要有多余内容: "+history_string,600,False,0.3)

                print("\n\n概括结果:"+gaikuo+"\n\n")
                
                history.clear()

                history.append("history:"+gaikuo)
'''

if __name__ == '__main__':
    #调用main函数
    main()