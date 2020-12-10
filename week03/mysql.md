## 1.在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
- 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
- 将增加远程用户的 SQL 语句作为作业内容提交

### 修改字符集配置项
`vim /etc/my.cnf`

修改以下内容：
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

### 验证字符集
```
mysql> show variables like '%character%';
```

### 创建 test database
```
mysql> create database test;
```

### 增加远程用户 test
```
mysql> create user 'test'@'%' identified by 'test';
```

### 授权给 test 用户访问 test database
```
mysql> grant all on test.* to 'test'@'%';
```
