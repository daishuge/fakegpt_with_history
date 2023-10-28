# fakegpt_with_history
一个使用ai.fakeopen.com的api的包含聊天概括功能的chatgpt聊天机器人

通过大佬zhile-io的项目，实现0消费的chatgpt api调用

## 依赖安装
```shell
pip install openai
pip install jieba
```

## 如何获取fk- 的api?
请参考这个issue: 

https://github.com/zhile-io/pandora/issues/183

## 加入pandora服务检查
由于pandora服务最近不是很稳定,所以加入了检查服务是否正常的功能,如果服务不正常,则会自动切换到openai官方api

灵感来自于我同学hhhhhge: https://github.com/hhhhhge

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

## 运行截图
![image](https://github.com/daishuge/-fakegpt-with-history/assets/122254868/b3204a76-3d1a-4674-a0e7-a3a8aaff7b98)


## 遥遥领先, 稳中向好

[![Star History Chart](https://api.star-history.com/svg?repos=daishuge/-fakegpt-with-history&type=Date)](https://star-history.com/#daishuge/-fakegpt-with-history&Date)