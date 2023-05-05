from setting import POSTGRES_SETTINGS, URLS
import psycopg2
import requests


class ReqresApi:
    def __init__(self):
        self.__urls = URLS
        self.__response = None
        self.__conn = psycopg2.connect(**POSTGRES_SETTINGS)

    def get_api(self, key):
        req = requests.get(self.__urls['user'])
        self.__response = req.json()[key]

    def display_api(self):
        print(self.__response)

    def syn_reqres_api(self):
        self.get_api('data')
        with self.__conn.cursor() as cur:
            for data in self.__response:
                try:
                    sql = f"INSERT INTO public.ApiReqres(id, email, first_name, last_name, avatar)" \
                          f"VALUES({data['id']},\'{data['email']}\',\'{data['first_name']}\',\'{data['last_name']}\'," \
                          f"\'{data['avatar']}\') ON CONFLICT (id) DO NOTHING"
                    print(sql)
                    cur.execute(sql)
                except Exception as e:
                    print(e)
            self.__conn.commit()
            cur.execute("SELECT * FROM ApiReqres")
            results = cur.fetchmany(5)
            print(results)


req_api_obj = ReqresApi()
req_api_obj.syn_reqres_api()
