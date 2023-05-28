import pymysql
import os

def mysql_connect():
    host=os.getenv("DB_HOST")
    user=os.getenv("DB_USER")
    password=os.getenv("DB_PASSWORD")
    database=os.getenv("DB_DATABASE")
    ssl_ca=os.getenv("SSL_CA")
    return pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8mb4',
                           ssl_ca=ssl_ca, cursorclass=pymysql.cursors.DictCursor)

def init_database():
    if os.getenv("DB_HOST") in ["localhost", "127.0.0.1"]:
        with mysql_connect() as connect:
            with connect.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS users (user_id char(4) PRIMARY KEY, nickname varchar(10) default '名無しのギャンブラー' , having_money int default 3000);")
                cur.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id char(4) PRIMARY KEY, user_id char(4) NOT NULL, dealer_id char(4) NOT NULL, amount int NOT NULL, type enum('bet', 'payout', 'payment', 'gift', 'other') NOT NULL, detail varchar(32), hide_detail varchar(32), timestamp datetime default (now()))")
                cur.execute("CREATE TABLE IF NOT EXISTS dealers (dealer_id char(4) PRIMARY KEY, name varchar(10) NOT NULL, description varchar(32) NOT NULL, creator varchar(10) NOT NULL)")
            connect.commit()

def destroy_db():
    with mysql_connect() as con:
        with con.cursor() as cur:
            cur.execute("DELETE FROM users")
            cur.execute("DELETE FROM transactions")
            cur.execute("DELETE FROM dealers")
            con.commit()