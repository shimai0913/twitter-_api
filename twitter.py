import argparse
from requests_oauthlib import OAuth1Session  # OAuthのライブラリの読み込み
from config import CONFIG
from lib_MyTwitter import MyTwitter

CONSUMER_KEY = CONFIG["CONSUMER_KEY"]
CONSUMER_SECRET = CONFIG["CONSUMER_SECRET"]
ACCESS_TOKEN = CONFIG["ACCESS_TOKEN"]
ACCESS_SECRET = CONFIG["ACCESS_SECRET"]

# ////////////////////////////////////////////////////////////////////////// #
#
#  関数
#
# ////////////////////////////////////////////////////////////////////////// #
def check_args():
    # ---------------------
    # コマンドライン引数の受け取り
    # ---------------------
    parser = argparse.ArgumentParser(add_help=False)

    # 引数の追加
    parser.add_argument("-w", help="search word", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    try:
        result = {}
        result["word"] = args.w
        result["debug"] = args.debug
        result["error_code"] = 1

        return result
    except Exception as e:
        if args.debug:
            print(f"引数指定に誤りがありそうです{e}")
        return 1


# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
    # コマンドライン引数の受け取り
    args = check_args()
    assert args != 1, "Abnormality in argument."

    # 認証処理
    auth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    # インスタンス作成
    twitter = MyTwitter(args, auth)

    # twitter.get_timeline()
    users = twitter.user_search()
    # id_list, username_list, screenname_list = twitter.create_id_list(users)

    for user in users:
        user_id = user["id"]
        user_name = user["name"]
        screen_name = user["screen_name"]
        twitter.follow(user_id, user_name, screen_name)


if __name__ == "__main__":
    main()

# twitter.py -w "プログラミング" --debug
