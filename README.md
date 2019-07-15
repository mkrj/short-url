一个基于Flask，利用mysql、redis实现的短网址服务。

## 原理介绍

进制转换:将long_url存入mysql数据库，为缩短后的token添加索引以加快查询。利用redis实现一全局计数器，将long_url映射为一个类六十二进制的字符串token。

## 依赖
- python框架: Flask
- 数据库: Mysql, Redis
- ORM框架: SQLALchemy

## 安装
```
git clone https://github.com/mkrj/short-url.git
cd short-url
pip install pipenv  # 如果本地已经安装pipenv,跳过此步
pipenv install --dev  # 安装依赖
pipenv shell  # 激活虚拟环境
```

## 创建数据库表
```
flask db init
flask db migrate
flask db upgrade
```
> 需提前建好数据库。

## 运行
- 需先激活虚拟环境
- 需要提前启动redis数据库

### 
```
flask run
```

## 测试
```
pytest test
```

## 使用示例

**POST: /shorten**

接收参数类型:JSON
```
{"url":"http://www.baidu.com?id1234&name=张三&title=多吃水果有益健康"}
```
返回数据类型:JSON
```
"http://yf.me/1"
```
> host可以在.env文件中自主配置。

**POST: /expand**

接收参数类型:JSON
```
{"url":"http://yf.me/1"}
```
返回数据类型:JSON
```
"http://www.baidu.com?id1234&name=张三&title=多吃水果有益健康"
```

### QA
#### 为什么是六十二进制？

因为缩短后的token每位上可选的字符范围在[0-9A-Za-z],总共六十二位。

#### mysql只有在插入记录的时候，ID 才会自增，如何利用自增后的ID进行进制转化？

通过redis的incr方法实现全局计数器功能。

#### 为什么不直接存储生成的短网址，而是存储token?

为了可以自主定义生成短连接的host。

### 为什么项目写的这么复杂，感觉一个脚本就可以实现？

是的，这个项目这样写，完全是杀鸡用牛刀:

比如创建表，可以不用ORM框架，也不用数据库版本管理工具，直接sql命令创建；

比如只有两个API 接口，可以不用上蓝图；

又比如可以整体把初始化的操作、创建表、API都放在一个模块中。

但在大一点的项目中，几乎都要用到ORM框架、数据库版本控制、按功能划分API接口。

这样写复用性更强。

Just for practice。
