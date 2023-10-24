# fakegpt-with-history
一个使用ai.fakeopen.com的api的包含聊天概括功能的chatgpt聊天机器人

通过大佬zhile-io的项目，实现0消费的chatgpt api调用

项目结构:
1.在fake_api.py中定义一个调用ai的函数

2.在token_count.py中定义一个函数来计算token

3.在main.py中让用户输入一个字符串，加入一个history列表

4.调用ai进行回答,并且输出后加入history列表

5.在main.py中调用token_count.py中的函数来计算history列表中的token

6.如果计算出来的token>2500,则调用ai概括,并且覆写进history列表中

请各位大佬指正,本人邮箱: play13661948263@gmail.com

更新:现在zhile-io大佬的api支持了超大token,几乎完全不用担心token,各位在应用的时候可以去掉token计数,但是在调用官方api时建议加上
现在默认不记录token,你可以把main.py中的相关注释去除

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=daishuge/-fakegpt-with-history&type=Date)](https://star-history.com/#daishuge/-fakegpt-with-history&Date)
