# 学习笔记

## MySQL 安装
### 企业级 MySQL 部署在 Linux 操作系统上，需要注意的重点：
* 注意操作系统的平台（32位、64位）
* 注意安装 MySQL 的版本（MySQL 企业版、社区版、MariaDB）
* 注意安装后避免 yum 自动更新
* 注意数据库的安全性

### 网络安装
* 安装索引
`yum install mysql-community-release-el7-10.noarch.rpm`

* 安装部件
`yum install my-sql-community-server`

* 防止 yum 自动更新 mysql
`yum remove mysql57-community-release-el7-10.noarch`

### 本地安装
* 下载 RPM
* `yum install *.rpm`

### 启动 MySQL
`systemctl start mysql.service`

### 开机自动启动 MySQL
`systemctl enable mysql`

### 查看 MySQL 服务状态
`systemctl status mysql.servcie`

### 查看安装的 MySQL 版本
`rpm -qa | grep -i ‘mysql’`

### 找出第一次启动后，分配的随机密码
`grep 'password' /var/log/mysqld.log | head -1`

### 登录
`mysql -u root -p`

### 修改 root 的密码
`ALTER USER 'root@localhost' IDENTIFIED BY 'new_password';`

### 查看密码强度策略
`SHOW VARIABLES LIKE 'validate_password%';`

### 设置密码强度策略为低
`set global validate_password_policy=0;`


## 正确使用 MySQL 字符集
### 查看字符集
`show variables like '%character%';`

### 查看校对规则
`show variables like ‘collation_%’;`

**注意： MySQL 中的 utf8 不是 UTF-8 字符集**

### 修改 MySQL 字符集
`vim /etc/my.cnf`

设置以下部分：
```
[client]
default_character_set = utf8mb4

[mysql]
default_character_set = utf8mb4

character_set_server = utf8mb4
init_connect = 'SET NAMES utf8mb4'
character_set_client_handshake = FALSE
collation_server = utf8mb4_unicode_ci
```

重启 MySQL 让设置生效：
`systemctl restart mysqld`


## 多种方式连接 MySQL 数据库
注意： MySQLdb 是 Python2 的包，适用于 MySQL 5.5 和 Python 2.7

### Python 3 连接 MySQL：
* Python 3 安装的 MySQLdb 包叫做 mysqlclient，加载的任然是 MySQLdb
* shell> `pip install mysqlclient`
* python> `import MySQLdb`

### 其他 DB-API：
* shell> `pip install pymysql`  # 流行度最高
* shell> `pip install mysql-connector-python`  # MySQL 官方

### 使用 ORM：
* shell> `pip install sqlalchemy`
