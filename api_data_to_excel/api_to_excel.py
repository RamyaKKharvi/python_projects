
from setting import URLS, WORKBOOK_PATH
import requests
import xlsxwriter


class ApiToExcel:
    def __init__(self):
        self.__url = URLS
        self.__data = None

    def get_api_data(self):
        api_response = requests.get(self.__url)
        self.__data = api_response.json()['data']
        self.create_excel()

    def create_excel(self):
        if len(self.__data) > 0:
            list_headers = list(self.__data[0].keys())
            list_rows = []

            for val in self.__data:
                list_data_val = list(val.values())
                list_rows.append(list_data_val)

            with xlsxwriter.Workbook(WORKBOOK_PATH) as my_api_workbook:
                worksheet = my_api_workbook.add_worksheet()
                row = 0
                column = 0

                for header in list_headers:
                    worksheet.write(row, column, header)
                    column = column + 1

                for id, email, first_name, last_name, avatar in list_rows:
                    row = row + 1
                    worksheet.write(row, 0, id)
                    worksheet.write(row, 1, email)
                    worksheet.write(row, 2, first_name)
                    worksheet.write(row, 3, last_name)
                    worksheet.write(row, 4, avatar)


api_to_excel = ApiToExcel()
api_to_excel.get_api_data()