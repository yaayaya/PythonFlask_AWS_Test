# 將景點資料存放到資料庫中
# 景點圖片的處理，我們會過濾資料中，不是 JPG 或 PNG 的檔案，
# 景點的每張圖片網址都必須被想辦法儲存在資料庫中。
import json
import mysql.connector

with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)
# 共58筆資料
data = data["result"]["results"]

# print(data[0])                # []
# print(data[0]["file"])        # str    key-value


# file處理
for e in data:
    # 格式問題
    # 先統一大小寫
    e["file"] = e["file"].replace(".JPG", ".jpg")
    # https連結字串異常修正 .jpghttps .jpg https
    e["file"] = e["file"].replace(".jpghttps", ".jpg https")
    # print(e["file"])    # str

    # 篩選資料
    # 只留 JPG 或 PNG檔案
    list_file = e["file"].split()
    # print(list_file)                  # [ ] 含 jpg.mp3.flv陣列

    filterDatas = []
    for x in list_file:
        if ".jpg" in x:
            filterDatas.append(x)

    # 整理網址不能有, 轉換為_
    # str_filterDatas = '__'.join(str(v) for v in filterDatas)
    e["file"] = filterDatas


# 資料庫處理

# print(data[0])
# print(data[0].values())

# dict_values ([5, '新北投站下車，沿中山路直走即可到達公車：216、218、223、230、266、602、小6、小7、小9、、小22、小25、小26至新北投站下
#              車', '新北投溫泉區', '2016/07/07', '121.508447', '10', '2010/02/14', '10', '新北投', '2011051800000061', '1', '養生溫泉', '各業者不
#              同，依據現場公告', 'Y', ['https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000848.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11002891.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D315/E70/F65/1e0951fb-069f-4b13-b5ca-2d09df1d3d90.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D260/E538/F274/e7d482ba-e3c0-40c3-87ef-3f2a1c93edfa.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D919/E767/F581/9ddde70e-55c2-4cf0-bd3d-7a8450582e55.jpg', 'https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D28/E891/F188/77a58890-7711-4ca2-aebe-4aa379726575.jpg'],
#              '飯店、會館大部分集中於中山路、光明路沿線以及北投公園地熱谷附近，總計約有44家，每一家都各有其特色，多樣的溫泉水療以及遊憩設施，提供遊
#              客泡湯養生，而鄰近的景點也是非常值得造訪，例如被列為三級古蹟的三寶吟松閣、星乃湯、瀧乃湯以及北投第一家溫泉旅館「天狗庵」，都有著深遠
#              的歷史背景，而北投公園、北投溫泉博物館、北投文物館、地熱谷等，更是遊客必遊的景點，來到北投除了可以讓溫泉洗滌身心疲憊，也可以順便了解
#              到北投溫泉豐富的人文歷史。', 1, '2016/07/07', '臺北市  北投區中山路、光明路沿線'])

# print(data[0].keys())
# dict_keys (['rate', 'direction', 'name', 'date', 'longitude', 'REF_WP', 'avBegin', 'langinfo', 'MRT', 'SERIAL_NO', 'RowNumber', 'CAT', 'MEMO_TIME', 'POI', 'file', 'idpt', 'latitude', 'description', '_id', 'avEnd', 'address'])
# print(list(data[0].keys()))
# ['rate', 'direction', 'name', 'date', 'longitude', 'REF_WP', 'avBegin', 'langinfo', 'MRT', 'SERIAL_NO', 'RowNumber', 'CAT', 'MEMO_TIME', 'POI', 'file', 'idpt', 'latitude', 'description', '_id', 'avEnd', 'address']

# python要把json資料value值放入mysql欄位內
# 要轉換成str放入

list1 = list(data[0].keys())
list2 = list(data[0].values())

# print(list2)

# print(list1)
str1 = ",".join(list(data[0].keys()))
# print(str1)


# 抓取58筆data中，每一筆欄位資料
# for e in data[0].values():
#     print(e)

# for e in data:
#     # 58筆字典資料
#     # print(e)
#     for i in e:
#         print(e.values())


try:
    # 連結dbtaipei_day_trip資料庫
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="dbtaipei_day_trip"
    )
    # 對資料庫進行操作
    # 使用指標  cursor()
    cursor = db.cursor()

    for e in data:
        # 資料庫執行
        # sql = f"""INSERT INTO data (rate, direction, name, date,
        # longitude, REF_WP, avBegin, langinfo, MRT, SERIAL_NO, RowNumber,
        # CAT, MEMO_TIME, POI, file, idpt, latitude, description, _id, avEnd,
        # address) VALUES ({str_value})"""

        # 資料庫執行
        sql = f"""INSERT INTO data (rate, direction) VALUES (
            {e["rate"]} , '{e["direction"]}')"""

        # sql_2 = "SELECT * FROM data"
        # cursor.execute(sql_2)
        # login_user = cursor.fetchall()
        # print(login_user)

        # print(e.values())
        # print(list_value)
        # str_value = "list_value".join()

        # for i in e.values():
        # print(i)       # str
        # data_value += i
        # print(data_value)
        # val = [data_column, list(e.values())]

        cursor.execute(sql)
        db.commit()
    print("ok")


except Exception as err:
    print("error")
    print(err)
