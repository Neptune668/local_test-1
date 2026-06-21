# Git常见命令

## 一.版本号查看文件

### 1.Git版本号-文件操作

#### 鼠标右键打开Git Bash Here，输入命令 git  cat-file  -p  复制版本号

获得提交信息的版本号，再次查询获得的版本号得到文件状态，

再次查询获得文件内容 		，一共查询三次版本号

### 2.Git版本号-分支操作

 HEAD  ---->  main（主分支

​		------>user（分支2

新建分支默认指向最后一次提交，新建提交分支才会发生变化

不同分支指向不同的版本       

##  二.本地仓库

### 1.仓库介绍 

从云端克隆库，本地库分为三个区（存储，暂存，工作（untracked files））

命令查看仓库状态：git status		un

git add 工作到暂存

git commit 暂存区到储存

### 2.仓库创建命令

方式一：桌面创建文件夹，在文件夹里右键打开Git Bash here窗口，

在窗口中输入git init （命令

git config user.name 名称，git config user.email 邮箱，这两天命令加--global全局

上面名称邮箱可以通过config文件直接修改

方式二：git clone 云端仓库路径  （命令方式

​		上面命令后空格，在后面指定仓库名称

方式三：gitHubDesktop直接创建 ,file new,创建库后默认提交一次文件

### 

## 三.文件操作

## 1.  文件删除

git log --oneline  查看日志

git commit -m 删除文件

## 2.文件误删除

git  restore  文件名  （文件恢复（恢复误删文件

git commit  -m  提交了删除操作，这是要用另外的方式恢复

查看日志  git log --oneline

git  reset  --hard    提交的版本号 （，重置某个提交 

git revert   版本号    （恢复到提交版本号之前，和前者不同是：不会

## 四.

## 五.



