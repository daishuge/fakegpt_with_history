import os
import sys
import shutil

token_max = 1024

history = []

# 初始化部分
if not os.path.isfile(os.path.join(os.getcwd(), "config.py")):
    shutil.copy(os.path.join(os.getcwd(), "config-template.py"), os.path.join(os.getcwd(), "config.py"))
    print("请修改config.py文件")
    sys.exit()

from chatgpt_api import fake_api
from token_count import token_count
import config

token_max = config.api_key

# main函数
def chat(query):
    if query == "clear":
        history.clear()
        return None
    else:
        history.append("user:" + query)
        query_gpt = ''
        api = fake_api(query)
        for value in api:
            if value:
                query_gpt += value
        history.append("chatgpt:" + query_gpt)
        token()
        return query_gpt


# token计算
def token():
    token = token_count("".join(history))
    if token >= token_max:
        print("概括中...")
        history_str="".join(history)
        result=fake_api(f"请把这段文字概括成{token_max/2}个单词以内,不要有多余内容: \n"+history_str)
        cache = ''
        for value in result:
            if value:
                cache += value
        history.clear()
        history.append("history:"+cache)

if __name__ == '__main__':
    print(chat(input('You:')))
