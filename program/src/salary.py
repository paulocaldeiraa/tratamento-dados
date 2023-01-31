'''Import the packages'''
import pandas as pd
from src.employee import GetEmploeey
from src.create_salary_position_sheet import CreateSalaryandPositionSheet
from src.functions import get_uuid4

class GetSalary:
    '''
    Third generated worksheet
    In this step the third HR worksheet is processed,
    containing information about salary and position.
    Here we will generate the salary sheet.
    '''

    def __init__(self) -> None:
        pass

    # Prepare the HR spreadsheet with the class below
    CreateSalaryandPositionSheet()

    #--------------------Reading Dataframe--------------------#
    # Preloads the data
    salario = pd.read_csv('planilhas\\salario_temp_historico.csv',sep = ',')

    data_salario = GetEmploeey.data.merge(salario,
                            on='Nome Funcionário',
                            how='left')

    #--------------------Generating the salary Spreadsheet--------------------#
    # Fill in the start dates with the admission dates
    data_salario['Inicial'].fillna(data_salario['Dt. Admissão'],inplace=True)

    salary_sheet = pd.DataFrame({'employee_id': data_salario['employee_id'],
                            'Salários': data_salario['Salário_y'],
                            'Data Inicial': data_salario['Inicial'],
                            'Data FInal': data_salario['Final'],
                            'Bonus': data_salario['Adcional'],
                            'Criado_em': GetEmploeey.today,
                            'Upload_em': GetEmploeey.today})

    salary_sheet.insert(0,'id','') #Creat the new column on dataframe

    get_uuid4(salary_sheet,'employee_id','id')

    # Save the new spreadsheet
    salary_sheet.to_csv('program\\output_sheets\\salario.csv', index=False)
