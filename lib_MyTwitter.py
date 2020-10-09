import json
import time
import traceback


class MyTwitter:
    # [Dont Touch] インスタンス変数
    def __init__(self, args, auth):
        self.def_name = "init"
        self.twitter = auth
        self.search_word = args["word"]
        self.debug_flag = args["debug"]
        # self.start_time=time.time()
        # self.debug_flag=args['debug']
        # self._error_code=args['eror_code']

    def get_timeline(self):
        self.def_name = "get_timeline"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f"[ OK ] {description}")
        # メインコード
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        params = {
            "count": 5,
        }
        res = self.twitter.get(url, params=params)
        if res.status_code == 200:
            timelines = json.loads(res.text)
            for line in timelines:
                user_name = line["user"]["name"]
                text = line["text"]
                created_at = line["created_at"]
                # ログ作業後処理
                message = f"get my timeline completed."
                self.write_log("INFO", f"[ OK ] {message}")
        else:
            self.printLog("FATAL", f"!!!!!===== Exception =====!!!!!")
            self.printLog("FATAL", f": {res.status_code}")

    def user_search(self):
        self.def_name = "user_serch"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f"[ OK ] {description}")
        # メインコード
        url = "https://api.twitter.com/1.1/users/search.json"
        params = {
            "q": self.search_word,  # default:Twitter%20API
            "page": 7,  # default:3
            "count": 20,  # default:5, max:20
        }
        res = self.twitter.get(url, params=params)
        if res.status_code == 200:
            users = json.loads(res.text)
            print(len(users))
            # ログ作業後処理
            message = f"user serch completed with serach word「{self.search_word}」."
            self.printLog("INFO", f"[ OK ] {message}")
            return users
        else:
            self.printLog("FATAL", f"!!!!!===== Exception =====!!!!!")
            self.printLog("FATAL", f"{message}: {res.status_code}")

    def create_id_list(self, users):
        self.def_name = "create_id_list"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f"[ OK ] {description}")
        # メインコード
        id_list = []
        username_list = []
        screenname_list = []
        for user in users:
            # print(f'Name: {user["name"]}(@{user["screen_name"]})')
            # print(f'ID: {user["id"]}')
            # print(f'Description: {user["description"]}')
            id_list.append(user["id"])
            username_list.append(user["name"])
            screenname_list.append(user["screen_name"])
        # ログ作業後処理
        message = f"create ID List completed."
        self.printLog("INFO", f"[ OK ] {message}")
        return id_list, username_list, screenname_list

    def follow(self, user_id, user_name, screen_name):
        self.def_name = "follow"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f"[ OK ] {description}")
        # メインコード
        url = "https://api.twitter.com/1.1/friendships/create.json"
        params = {
            "user_id": user_id,
            "follow": True,
            # "screen_name": 2,
        }
        res = self.twitter.post(url, params=params)
        if res.status_code == 200:
            # ログ作業後処理
            message = f"follow succeeded. =>{user_name}(@{screen_name})"
            self.printLog("INFO", f"[ OK ] {message}")
        else:
            self.printLog("FATAL", f"!!!!!===== Exception =====!!!!!")
            message = f"follow failed. =>{user_name}(@{screen_name})"
            self.printLog("FATAL", f"{message}: {res.text}")

    def printLog(self, level, message):
        if self.debug_flag:
            print(f"[{level}] {message}")
