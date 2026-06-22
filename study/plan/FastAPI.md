# FastAPI

### 一、新建项目

#### 1.装依赖

pip install uvicron和 fastapi

pip list 查看所有装过的

#### 2.导包，创建对象

from fastapi import FastAPI

app = FastAPI()

@app.get("/user/{info}")	下面写一个函数：返回值为json,页面会显示 info接收地址中输入的内容

local终端开启服务器：fa_a:app模块名

uvicorn fa_1:app --reload

#### 3.快速启动

导包uvicorn

main()方法中写：uvicorn.run(

app = "fa_2:app",host = "0.0.0.0",port =8000,reload = True)

reload 修改p

## 二、项目

### 1.测试

/docs	内置测试框架

### 2.路由分发：API

整合py文件

from fastapi import APIRouter

user_router =  APIRouter(prefix="/user",tags=["用户模块"])	创建路由对象

@user_router.get("/goods/info")

再将这两个路由对象导入到main.py

创建fastapi对象

app = FastAPI("")

app.include_router(xxx)

### 3.ORM概念

对象关系映射

表对应类，列对应类的属性

## 三、SQLAlchemy

### 1.安装依赖

sqlalchemy   pymysql









