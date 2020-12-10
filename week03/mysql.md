## 1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。
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

## 2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取: 
- 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
- 将 ORM、插入、查询语句作为作业内容提交

source code: [mysql.py](https://github.com/gzeureka/Python005-01/blob/main/week03/mysql.py)

## 3. 为以下 sql 语句标注执行顺序：
```
SELECT DISTINCT player_id, player_name, count(*) as num          -- 5
FROM player JOIN team ON player.team_id = team.team_id           -- 1
WHERE height > 1.80                                              -- 2
GROUP BY player.team_id                                          -- 3
HAVING num > 2                                                   -- 4
ORDER BY num DESC                                                -- 6
LIMIT 2                                                          -- 7
```

## 4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?
```
Table1

id name

1 table1_table2

2 table1

Table2

id name

1 table1_table2

3 table2
```

INNER JOIN
```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
INNER JOIN Table2
ON Table1.id = Table2.id;
```
查询结果
| table1.id | table1.name | table2.id | table2.name |
|-|-|-|-|
| 1 | table1_table2 | 1 | table1_table2 |

LEFT JOIN
```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
LEFT JOIN Table2
ON Table1.id = Table2.id;
```
查询结果
| table1.id | table1.name | table2.id | table2.name |
|-|-|-|-|
| 1 | table1_table2 | 1 | table1_table2 |
| 2 | table1 | NULL | NULL |

RIGHT JOIN
```
SELECT Table1.id, Table1.name, Table2.id, Table2.name
RIGHT Table1
LEFT JOIN Table2
ON Table1.id = Table2.id;
```
查询结果
| table1.id | table1.name | table2.id | table2.name |
|-|-|-|-|
| 1 | table1_table2 | 1 | table1_table2 |
| NULL | NULL | 3 | table2 |

