# fakegpt_with_history
一个使用反代的api的包含聊天概括功能的chatgpt聊天机器人,免翻墙,不消耗余额

通过大佬[zhile-io](https://github.com/zhile-io)的[pandora](https://github.com/zhile-io/pandora)项目，实现0消费的chatgpt api调用

## 依赖安装
```shell
pip install openai
pip install jieba
```

## 如何获取fk- 的api?
请参考这个[issue](https://github.com/zhile-io/pandora/issues/183):


## 加入pandora服务检查
由于pandora服务最近不是很稳定,所以加入了检查服务是否正常的功能,如果服务不正常,则会自动切换到openai官方api

灵感来自于我同学[hhhhhge](https://github.com/hhhhhge)

此部分代码:

fake_api.py中的fake_api函数:

```python
if if_pandora:
    openai.api_key = "YOUR_PANDORA_FAKE_KEY "    #fake_api
    openai.api_base = "https://ai.fakeopen.com/v1/"
else:
    openai.api_key = "YOUR_OPNEIA_REAL_KEY"  #real_api
```

main.py中的调用:

```python
try:
    fake_api("test", 1000, True, 0.5,config.if_pandora)
except:
    if_pandora=False
    print("pandora 连接错误, 尝试官方api")
```

## 项目结构:
1.在fake_api.py中定义一个调用ai的函数

2.在token_count.py中定义一个函数来计算token

3.在main.py中让用户输入一个字符串，加入一个history列表

4.调用ai进行回答,并且输出后加入history列表

5.在main.py中调用token_count.py中的函数来计算history列表中的token

6.如果计算出来的token>2500,则调用ai概括,并且覆写进history列表中(可选)

7.再次让用户输入,把用户新输入和history列表中所有内容交给chatgpt

请各位大佬指正,欢迎发起issue

更新:现在zhile-io大佬的api支持了超大token,几乎完全不用担心token,各位在应用的时候可以去掉token计数,但是在调用官方api时建议加上

现在默认不记录token,你可以把main.py中的相关注释去除

## 配置文件
在2023.10.28更新中,加入了配置文件

配置文件差不多长这样:

```python
if_pandora = True                           #是否尝试使用pandora反代
long_text = True                            #是否启用概括
max_token = 500                             #到达此token则概括
smaller_text = 50                           #概括成此单词数
openai_api = "YOUR_OPENAI_REAL_KEY"         #real_key
pandora_api = "YOUR_PANDORA_FAKE_KEY"       #fake_key
base_url = "https://ai.fakeopen.com/v1/"    #pandora反代地址
```

你可以在配置文件中进行设置

## 运行截图

![image](https://github.com/daishuge/fakegpt_with_history/assets/122254868/6fc2f993-1430-4cf8-98ba-ce14c7d394f1)


## 遥遥领先, 稳中向好

[![Star History Chart](https://api.star-history.com/svg?repos=daishuge/-fakegpt-with-history&type=Date)](https://star-history.com/#daishuge/-fakegpt-with-history&Date)
