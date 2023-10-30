# **Chatgpt-with-history**

由Python封装的调用Chatgpt并流式返回的方法并具有历史和对话概括功能
并且Pandora项目的地址也可用

## 依赖安装

```shell
pip install openai jieba
```

## 如何获取Pandora项目的api?

Pandora 项目使用假的 api ，类似 fk-xxxxxxxxxxxxxx

请参考这个issue:

<https://githubfast.com/zhile-io/pandora/issues/183>

## 项目结构

1.在fake_api.py中定义一个调用ai的函数

2.在main.py中让用户输入一个字符串，加入一个history列表

3.调用ai进行回答,并且输出后加入history列表

4.再次让用户输入,把用户新输入和history列表中所有内容交给chatgpt

请各位大佬指正,欢迎发起issue

### 这是来自我同学的一个项目

## Star

![star](https://api.star-history.com/svg?repos=hhhhhge/fakegpt&type=Date)
