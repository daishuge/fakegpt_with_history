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
                print(value,end='')
                query_gpt += value
        print()
        history.append("chatgpt:" + query_gpt)

if __name__ == '__main__':
    while True:
        chat(input('You:'))
