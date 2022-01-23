# シートCの情報取得試してみる
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_cname(str_doaction):
    tmp_array = str_doaction.split(",")
    tmp = tmp_array[1]

    return tmp[2:-3]


def get_shutuba_data(i, date_site, soup):
    # 指定の日付の会場ごとのページにいく
    ele_div = soup.select("div.link_list")
    # link_listが何個目かで日付を選定すればよい
    ele_a = ele_div[0].select("a")
    cname = get_cname(ele_a[0].attrs["onclick"])
    payload = {"cname": cname}
    r = session.post(url, headers=headers, data=payload)
    r.encoding = r.apparent_encoding
    if "パラメータエラー" in r.text:
        print("error!")
    # print(r.text)
    print("{} OK".format(ele_a[0].text))

    # 情報取得
    ele_table = soup.select_one("#race_list")
    ele_tr = ele_table.select("tr")
    for ele in ele_tr:
        list_race = []
        list_race.append()

    # レース詳細ページにいく

    ele_td = soup.select("td.syutsuba")
    ele_a = ele_td[0].select_one("a")
    cname = get_cname(ele_a.attrs["onclick"])
    payload = {"cname": cname}
    r = session.post(url, headers=headers, data=payload)
    r.encoding = r.apparent_encoding
    if "パラメータエラー" in r.text:
        print("error!")
    # print(r.text)
    print("{} OK".format(payload))

    # 馬ごとの情報を見る
    soup = BeautifulSoup(r.text, 'lxml')
    ele_td = soup.select("td.horse")
    ele_a = ele_td[0].select_one("a")
    cname = get_cname(ele_a.attrs["onclick"])
    payload = {"cname": cname}
    r = session.post(url, headers=headers, data=payload)
    r.encoding = r.apparent_encoding
    if "パラメータエラー" in r.text:
        print("error!")
    print(r.text)
    print("{} OK".format(payload))


if __name__ == '__main__':

    # Excelワークブックの読み込み
    wb = openpyxl.load_workbook("JRAdata.xlsx")
    ws_c = wb["C"]
    # データ読み取り
    df = pd.DataFrame(ws_c.values)
    # print(df.columns)

    # 一旦削除する
    df.drop(range(len(df)), inplace=True)


    url = "https://www.jra.go.jp/JRADB/accessS.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {"cname": "pw01dli00/F3"}

    # 出馬表を選択する
    session = requests.Session()
    r = session.post(url, headers=headers, data=payload)
    # r = requests.get(url, data=payload)
    r.encoding = r.apparent_encoding
    print("{} OK".format(payload))

    # 開催日一覧
    soup = BeautifulSoup(r.text, "lxml")
    ele_h3 = soup.select("h3.sub_header")
    list_date_site = []
    for i, ele in enumerate(ele_h3):
        print(ele.getText())
        tmp = ele.getText()
        pos001 = tmp.find("月")
        tmp_month = int(tmp[:pos001])
        pos002 = tmp.find("日")
        tmp_day = int(tmp[pos001 + 1:pos002])
        datetime_targ = datetime(datetime.now().year, tmp_month, tmp_day)
        list_date_site.append(datetime_targ)


    # ここでサイトの日付とExcelの日付を見比べて足りないものだけをスクレイピングする
    list_date_excel = [datetime(2022, 1, 8), datetime(2022, 1, 15)]
    for i, date_site in enumerate(list_date_site):
        is_exist = False
        for date_excel in list_date_excel:
            if date_site == date_excel:
                is_exist = True
                break
        # ここで指定の日付のデータを取得する処理をする
        if not is_exist:
            df_data = get_shutuba_data(i, date_site)
            df = pd.concat([df, df_data], axis=1)


    print(df)


