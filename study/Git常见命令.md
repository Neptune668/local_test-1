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

git - v 查看git版本

从云端克隆库，本地库分为三个区（存储，暂存，工作（untracked files））

命令查看仓库状态：git status	创建b.txt文件		

git status,	Untracked files未追踪

git add 工作到暂存			$ git rm --cached b.txt让文件回到上一个状态

$ git add *.txt添加以txt结尾的所有文件

git commit -m (-m后面跟提交信息)			暂存区到储存

git log 查看所有提交操作 	 (HEAD -> main)这是最新的提交   q退出查看

### 2.仓库创建命令

方式一：桌面创建文件夹，在文件夹里右键打开Git Bash here窗口，

在窗口中输入git init （命令输完多一个.git文件

git config user.name 名称，git config user.email 邮箱，这两条命令加--global全局配置（下面例子		git config --global  user.name 

上面名称邮箱可以通过config文件直接修改

方式二：git clone 云端仓库路径  （命令方式

​		上面命令后空格，在后面指定克隆仓库名称

方式三：（桌面端操作）gitHubDesktop直接创建 ,file new,创建库后默认提交一个文件（.gitatributes）

file options  git也可以设置用户邮箱

repository settings -->Git config ---> user my global git config 设置全局配置

## 三.文件操作

## 1.  文件删除

git log --oneline  查看日志  一行查看

git commit -m 删除文件

## 2.文件误删除

git  restore  文件名  （文件恢复（恢复误删文件

git commit  -m  提交了删除操作，这是要用另外的方式恢复

查看日志  git log --oneline

git  reset  --hard    提交的版本号 （，	重置某个提交 ，会丢失提交的版本号

git revert   版本号    （恢复到提交版本号之前，和前者不同是：不会丢失提交

## 四.git分支

#### 1.分支创建

创建分支，基于有提交的情况

git branch user(分支名)

git checkout user   	切换分支

git checkout -b order 创建并切换分支

git branch -d user删除分支

#### 2.分支合并

git branch  -v查看分支

git merge user（ 要合并的分支名)

#### 3.标签

git tag

git tag uptfile(标签名) 版本号	给版本号添加标签

git tag -d  uptrfile(标签名)		删除标签

git log  --oneline一行日志

#### 4.更多分支操作

git cherry-pick 指定分支		将指定数量的分支同步到指定分支

git变基

## 五.代码托管

#### 1.远程仓库操作

git remote add origin

git push origin 	将文件推送到远程仓库

git pull origin		将远程仓库拉取到本地

#### 2.远程仓库搭建

