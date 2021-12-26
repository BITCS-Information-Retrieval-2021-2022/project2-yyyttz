# team12-Author retrieval engine



## 项目说明

### Project2:  学者检索引擎

通过姓名、领域、机构、论文来对学者进行检索，并展示学者之间的作者关系图，节点之间的距离反映学者之间的亲近度。

#### 推荐爬取的站点

- AMiner: https://www.aminer.cn/
- Semantic Scholar：https://www.semanticscholar.org/

#### 要求

- **AMiner必选**，爬取作者信息，作者之间共同著作、所属机构等信息，以[Bengio](https://www.aminer.cn/profile/yoshua-bengio/53f4ba75dabfaed83977b7db)为例
- **Semantic Scholar必选**
- 爬到的数据必须存储到**MongoDB**中，字段必须定义清晰
- 当爬取到重名作者时，需要做到重名区分和同人合并
  - 可以利用机构、共同著作等信息

### 检索模块

#### 要求

- 从MongoDB中读取数据实现**综合检索**，要求无论是输入作者姓名、作者机构、领域、论文名称，都能得到相应的检索结果，如下例所示：

[![image-20211021105934462](https://github.com/BITCS-Information-Retrieval-2021-2022/Assignment-Description/raw/main/imgs/1.png)](https://github.com/BITCS-Information-Retrieval-2021-2022/Assignment-Description/blob/main/imgs/1.png) [![image-20211021110021291](https://github.com/BITCS-Information-Retrieval-2021-2022/Assignment-Description/raw/main/imgs/2.png)](https://github.com/BITCS-Information-Retrieval-2021-2022/Assignment-Description/blob/main/imgs/2.png)

- 可以自己实现搜索算法，也可以使用已有的搜索引擎工具，比如**Elasticsearch**（[https://www.elastic.co](https://www.elastic.co/)）
- 要求展示模块提供**作者网络信息**，可以根据数据库中爬取到的信息，也可以自行分析论文、引文等
- 利用已有数据对学者进行额外分析是**可选加分项**，例如师门关系、搜索过程中的学者对齐

### 展示模块

#### 要求

- 设计并实现一个学者搜索引擎网站，包括三个页面：

  - 首页/搜索页

  - 检索结果列表页

  - 作者**Profile页面**，可参考AMiner：

    - 必须包括：

      - 作者个人信息：姓名、照片、职称、所属机构
      - 作者发表论文
      - 作者关系网络，要求以**可视化**形式展现

      [![image-20211021192957783](https://github.com/BITCS-Information-Retrieval-2021-2022/Assignment-Description/raw/main/imgs/3.png)](https://github.com/BITCS-Information-Retrieval-2021-2022/Assignment-Description/blob/main/imgs/3.png)

      

- 推荐使用Python Django（[https://www.djangoproject.com](https://www.djangoproject.com/)）库来实现

### 提交内容

- 一个MongoDB数据库
- 在仓库README中给出爬取数据的**统计信息**，例如每个数据源爬取的学者数、字段覆盖率等
- 验收时，展示学者检索引擎的检索结果



## 项目配置

### 服务器信息

* 系统：Ubuntu Server 20.04 LTS 64位
* ip：121.5.169.182


* ssh port：22

### 账户信息

### 1. root

账号：cty

密码：tg0XAKx2stAzeOWH

### 2. front

账号：front

密码：xxjsfront

### 1. back

账号：back

密码：xxjsback

### 文件结构

#### 1. 用户个人空间

每个账户创建后，均会在`/home`路径下创建个人存储空间，路径为`/home/username`

ps：请将个人数据存放在该路径下

#### 2. 服务器存储结构

| 目录           | 大小 | 文件系统  | 硬盘 |
| -------------- | ---- | --------- | ---- |
| /dev           | 1.9G | udev      | SSD  |
| /              | 50G  | /dev/vda2 | HDD  |
| /run           | 394M | temfs     | SSD  |
| /dev/shm       | 2.0G | temfs     | SSD  |
| /run/lock      | 5.0M | temfs     | SSD  |
| /sys/fs/cgroup | 2.0G | temfs     | SSD  |
| /run/user/126  | 394M | temfs     | SSD  |
| /run/user/1001 | 394M | temfs     | SSD  |

ps：请将大型数据存储在`/home`路径下



## 项目环境

### ES

* version: v7.15.1
* ip: 121.5.169.182
* port: 9200
* 配置文件位置: `/home/cty/resources/elasticsearch-7.15.1/config/elasticsearch.yml`

### MongoDB

* version: v3.6.8
* ip: 121.5.169.182
* port: 28887
* 数据文件位置: `/var/lib/mongodb`
* 日志文件位置:`/var/log/mongodb/mongodb.log`
* 配置文件位置:`/etc/mongodb.conf`

### Python环境

- version: v3.8.10



## 常用命令

### 1. MongoDB

```shell
# 登入root用户
su
# 进入mongodb的tmux环境
tmux a -t mongodb
# 启动MongoDB服务
service mongodb start
或者
/usr/bin/mongod -f /etc/mongodb.conf &
# 停止MongoDB服务
service mongodb stop
# 重启MongoDB服务
service mongodb restart
# 进入MongoDB
mongo
# 查看所有database
show dbs
# 查看所有collections
show collections
# 创建database
use db_name
# 创建集合
db.createCollection("collection_name")
# 删除集合
db.collection_name.drop()
```

### 2. ES

```shell
# 登入cty用户
su cty
# 进入ES的tmux环境
tmux a -t es
# 启动
/home/cty/resources/elasticsearch-7.15.1/bin/elasticsearch -d
```

### 3. 后端

```shell
# 进入IR的tmux环境
tmux a -t ir
# 启动服务
python /home/cty/IR/back/main.py
```

### 4. 前端

```shell
# 进入IR的tmux环境
tmux a -t ir
# 启动服务
python /home/cty/IR/front/app.py
```

## 代码说明

### 0. 数据处理

数据处理：`/home/cty/IR/data_process/process.py`

> 从a_researcher和a_paper表中读取并解析MongoDB中原始数据，获得领域和其对应作者的关系，存入MongoDB的tag_author中，同理获得作者id和其发表过的论文id存为re_paper，获得作者之间共同发表论文数存为author_relation，获得同名作者的id列表存为author_name。

重名消歧：`/home/cty/IR/data_process/dname_split.py`

> 根据author_name和author_relation，以共同发表论文最高为标准，判断论文中作者对应的id

相似度改进：`/home/cty/IR/data_process/similarity.py`

### 1. 创建ES索引

创建索引：`/home/cty/IR/back/make_index.py`

删除索引：`/home/cty/IR/back/delete_index.py`

### 2. 后端部分

检索：`/home/cty/IR/back/search.py`

接口：`/home/cty/IR/back/main.py`

ps. 接口基于flask框架

### 3. 前端部分

代码：`/home/cty/IR/front`

环境：

- Flask 2.0.2
- Python 3.8.10

### 4. 数据统计

代码：`/home/cty/IR/statistics/dataCount.py`

## 接口说明

**query**

- **说明**
  - 主查询，根据query在author中检索并返回相应的文档
- **参数**
  - `query`：查询内容
  - `from`：返回分页结果的第几页
  - `size`：每一页的文档数

**find**

  - **说明**
    - 引用网络查询，根据query作者的id检索个人信息和其论文信息
- **参数**
  - `id`：query作者的id
  - `from`：返回分页结果的第几页
  - `size`：每一页的文档数

**relation**

- **说明**
  - 作者网络关系图，根据query作者的id在re_paper中检索并处理成网络坐标图的形式
- **参数**
  - `id`：query作者的id
  - `from`：返回分页结果的第几页
  - `size`：每一页的文档数量

## 提交说明

请在`project3-team8`中创建个人分支，将所有修改提交到个人分支中，确定无误后再合并至主分支，以避免污染主分支，并且方便出现问题后进行回滚操作。

## 界面展示

- 首页搜索页面

![HomePage](https://github.com/BITCS-Information-Retrieval-2021-2022/project2-yyyttz/blob/main/IR/images/HomePage.png)

- 搜索结果页面

![normalResult](https://github.com/BITCS-Information-Retrieval-2021-2022/project2-yyyttz/blob/main/IR/images/normalResult.png)

- 作者详情页

![authorDetail](https://github.com/BITCS-Information-Retrieval-2021-2022/project2-yyyttz/blob/main/IR/images/authorDetail.png)
