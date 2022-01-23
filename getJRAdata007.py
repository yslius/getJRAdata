# ツールの入力部を試してみる
from datetime import datetime

if __name__ == '__main__':

    sel001 = input("1:過去データ取得　2:出馬表データ取得\n")
    # print(sel001)

    if sel001 == "1":
        print("新規作成")
        sel002 = input("データ取得開始日を入力してください。yyyymmdd\n")
        date_from = datetime.strptime(sel002, "%Y%m%d")
        print(date_from)
        sel003 = input("データ取得終了日を入力してください。yyyymmdd\n")
        date_to = datetime.strptime(sel003, "%Y%m%d")
        print(date_to)
        if date_to <= date_from:
            print("正しく入力してください。")
            exit()
    elif sel001 == "2":
        print("データ更新")
    else:
        print("正しく入力してください。")
        exit()










