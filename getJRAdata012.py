# シートA、シートBの情報取得試してみる
# import requests
# from bs4 import BeautifulSoup
from datetime import datetime
# import openpyxl
# from openpyxl.utils.dataframe import dataframe_to_rows
# import pandas as pd
# import glob
from classScrapeJRA import ScrapeJRA
from classExcelData import ExcelData


def get_data_newexcel(date_from, date_to):
    # インスタンスを作る
    exceldata = ExcelData()
    scrapejra = ScrapeJRA()

    # レース結果を選択する
    scrapejra.next_page({"cname": "pw01sli00/AF"})

    # 過去レース結果検索を選択する
    scrapejra.next_page({"cname": "pw01skl00999999/B3"})

    # 例えば2020年6月を選択する
    scrapejra.next_page_date(date_from.year, date_from.month)

    # 指定の日付の会場ごとのページにいく
    scrapejra.next_page_place()

    # レース詳細ページにいく
    scrapejra.next_page_place_race()

    # 馬ごとの情報を見る
    scrapejra.next_page_umadata()

    # Excel保存する
    exceldata.create_new_excel(date_from, date_to)


def get_data_updateexcel():
    # インスタンスを作る
    exceldata = ExcelData()
    scrapejra = ScrapeJRA()

    # Excelを読み込む
    if not exceldata.read_excel() :
        return

    # 出馬表を開く
    scrapejra.next_page_shutuba()

    # 日付を取得する
    list_date =scrapejra.next_page_shutuba_list()
    if len(list_date) == 0:
        return

    # 当日の日付データを取得する
    # list_date_place = []
    # for i, date_targ in enumerate(list_date):
    #     if date_targ.day != datetime.now().day:
    #         continue
    #     list_place_cname = scrapejra.next_page_shutuba_date(i)

    # すべての会場のcnameを取得する
    list_date_place = scrapejra.next_page_shutuba_place(list_date)
    if len(list_date_place) == 0:
        return

    # 日付、場所ごとにデータを取得する
    for i, list_place in enumerate(list_date_place):
        excel_date = list_date[i]
        for place_cname in list_place:
            # 対象の場所のレースcname一覧を取得する
            list_race_cname = scrapejra.next_page_shutuba_racelist(place_cname)
            if len(list_race_cname) == 0:
                continue
            for race_cname in list_race_cname:
                # 出馬表に移動する
                if not scrapejra.next_page_shutuba_race(race_cname):
                    continue
                # 出馬表のデータを取得する
                list_data = scrapejra.get_shutuba_data(excel_date)
                for data in list_data:
                    exceldata.append_list(data)


if __name__ == '__main__':

    get_data_updateexcel()

    exceldata = ExcelData()
    scrapejra = ScrapeJRA()

    exceldata.read_excel()

    sel001 = input("1:過去データ取得　2:出馬表データ取得\n")
    # print(sel001)

    if sel001 == "1":
        print("新規作成")
        sel002 = input("データ取得開始日を入力してください。yyyymmdd\n")
        date_from = datetime.strptime(sel002, "%Y%m%d")
        # print(date_from)
        sel003 = input("データ取得終了日を入力してください。yyyymmdd\n")
        date_to = datetime.strptime(sel003, "%Y%m%d")
        # print(date_to)
        if date_to <= date_from:
            print("正しく入力してください。")
            exit()
        get_data_newexcel(date_from, date_to)
    elif sel001 == "2":
        # print("データ更新")
        get_data_updateexcel()
    else:
        print("正しく入力してください。")
        exit()

