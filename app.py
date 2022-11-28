from flask import *
import  mysql.connector

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Connect DB

try:
    # 連接 MySQL/MariaDB 資料庫
    testschema_conn = mysql.connector.connect(
        host='localhost',          # 主機名稱
        database='testschema',  # 資料庫名稱
        user='root',        # 帳號
        password='root')  # 密碼

    if testschema_conn.is_connected():

        # 顯示資料庫版本
        db_Info = testschema_conn.get_server_info()
        print("資料庫版本：", db_Info)

        # 顯示目前使用的資料庫
        cursor = testschema_conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("目前使用的資料庫：", record)

        # 顯示目前使用的資料庫
        cursor = testschema_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM testtable")
        record = cursor.fetchall()


except Exception as e:
    print("資料庫連接失敗：", e)


# TestDB
@app.route("/dbtest")
def dbtest():
    try:
        cursor = testschema_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM testtable")
        record = cursor.fetchall()  
        print(record)
        return record

    except Exception as err:    
        print(err)
        return str(err)

# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True, port=3000)