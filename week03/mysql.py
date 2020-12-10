# 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:
# 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间

from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pymysql

Base = declarative_base()


class User_table(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    age = Column(Integer)
    birthday = Column(String(10))
    gender = Column(String(10))
    create_time = Column(DateTime(), default=datetime.now)
    update_time = Column(DateTime(), default=datetime.now,
                         onupdate=datetime.now)


def create_users_table():
    '''使用 sqlalchemy ORM 方式创建表'''
    # 打开数据库连接
    engine = create_engine(
        'mysql+pymysql://test:test@localhost:3306/test', echo=True, encoding='utf-8')

    Base.metadata.create_all(engine)


def add_data_to_users_table():
    db = pymysql.connect('localhost', 'test', 'test', 'test')

    try:
        with db.cursor() as cursor:
            now = datetime.now()
            sql = '''INSERT INTO users (name, age, birthday, gender, create_time, update_time) VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (
                ('张三', 20, '2000-01-01', 'male', now, now),
                ('李四', 30, '1990-02-01', 'female', now, now),
                ('王五', 40, '1980-03-01', 'male', now, now),
            )
            cursor.executemany(sql, values)
        db.commit()
    except Exception as e:
        print(f'insert error {e}')
    finally:
        db.close()
        print(f'insert {cursor.rowcount} rows')


def query_data_on_users_table():
    db = pymysql.connect('localhost', 'test', 'test', 'test')

    try:
        with db.cursor() as cursor:
            sql = '''SELECT * FROM users'''
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                print(i)
        db.commit()
    except Exception as e:
        print(f'select error {e}')
    finally:
        db.close()
        print(f'select {cursor.rowcount} rows')


if __name__ == '__main__':
    create_users_table()
    add_data_to_users_table()
    query_data_on_users_table()
