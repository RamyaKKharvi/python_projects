
import psycopg2
from salary_slip_generator.setting import POSTGRES_SETTINGS, SALARY_SLIP_TEMPLATE, BASIC_SALARY_PERCENTAGE, HRA, EPF_PERCENTAGE, PROFESSIONAL_TAX, SALARY_SLIP_FOLDER_PATH
from docx import Document

import os

class PdfGeneratorService:
    def __init__(self):
        self.__conn = psycopg2.connect(**POSTGRES_SETTINGS)
        self.__employee_data = []
        self.__employee_dict_data = []


    def get_employee_data(self):
        sql = 'SELECT employee_id, employee_name, department_name, country_name, ph_no, salary, emp.create_date FROM employee AS emp INNER JOIN ' \
              'department AS dep ON emp.department_id = dep.department_id INNER JOIN country AS cont ON emp.country_id ' \
              '= cont.country_id'
        try:
            with self.__conn.cursor() as cur:
                cur.execute(sql)
                self.__employee_data = cur.fetchall()
            self.__create_dict_from_employee_data()

        except Exception as e:
            print('error is: ', e)

    def generate_salary_slip(self):
        self.get_employee_data()
        for emp in self.__employee_dict_data:
            template = Document(SALARY_SLIP_TEMPLATE)
            rows = template.tables[0].rows
            for row in rows:
                for cell in row.cells:
                    salary = int(emp.get('salary'))
                    basic_salary = salary * BASIC_SALARY_PERCENTAGE
                    hra = HRA * salary
                    epf = salary * EPF_PERCENTAGE

                    if '<name>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<name>', emp.get('name'))

                    if '<employee_id>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<employee_id>', emp.get('emp_id'))

                    if '<created_date>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<created_date>', emp.get('created_date'))

                    if '<department_name' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<department_name', emp.get('dep_name'))

                    if '<country_name>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<country_name>', emp.get('country'))

                    if '<ph_no>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<ph_no>', emp.get('ph_no'))

                    if '<basic_salary>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<basic_salary>', basic_salary)

                    if '<hra>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<hra>', hra)

                    if '<special_allowances>' in cell.text:
                        spcl_allow = salary - (hra) - (basic_salary)
                        cell.text = self.__replace_placeholder(cell, '<special_allowances>', spcl_allow)

                    if '<gross_salary>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<gross_salary>', salary)

                    if '<epf>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<epf>', epf)

                    if '<professional_tax>' in cell.text:
                        cell.text = self.__replace_placeholder(cell, '<professional_tax>', PROFESSIONAL_TAX)

                    if '<total_deduction>' in cell.text:
                        total_deduction = epf + PROFESSIONAL_TAX
                        cell.text = self.__replace_placeholder(cell, '<total_deduction>', total_deduction)

                    if '<amount>' in cell.text:
                        amount = salary - epf + PROFESSIONAL_TAX
                        cell.text = self.__replace_placeholder(cell, '<amount>', amount)
            template.save(f'salary_slip_doc/salary_slip_{emp.get("emp_id")}.docx',)

    def __replace_placeholder(self, cell, placeholder, new_value):
        return cell.text.replace(placeholder, str(new_value))

    def __create_dict_from_employee_data(self):
        data_list = []
        for data in self.__employee_data:
            temp_dict = {}
            temp_dict['emp_id'] = data[0]
            temp_dict['name'] = data[1]
            temp_dict['dep_name'] = data[2]
            temp_dict['country'] = data[3]
            temp_dict['ph_no'] = data[4]
            temp_dict['salary'] = data[5]
            temp_dict['created_date'] = data[6].date()
            data_list.append(temp_dict)
        self.__employee_dict_data = data_list

pdf_gen = PdfGeneratorService()
pdf_gen.generate_salary_slip()

