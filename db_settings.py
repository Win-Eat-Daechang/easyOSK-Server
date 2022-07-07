import pymysql


db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='aa06030137',
    db='piuda',
    charset='utf8'
)

cursor = db.cursor()
sql = """
        CREATE TABLE store(
            idx INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY_KEY,
            name VARCHAR(256) NOT NULL,
        );"""
cursor.exequte(sql)
cursor.execute("show tables")
db.commit()
db.close()
