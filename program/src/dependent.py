'''Import the packages'''
import warnings
import pandas as pd
from src.functions import get_uuid4
from src.employee import GetEmploeey
from src.personal_data import GetpersonalData

# Ignore Pandas Future Warning
warnings.simplefilter(action='ignore', category=FutureWarning)

class Getdependent:
    '''
    Sixth generated worksheet
    In this step, the spreadsheet of dependents is generated.
    By default, each dependent is grouped in a single column.
    The idea here is to make each one of these dependents move to more than one column,
    but in the same row, where each row is an employee.
    '''
    def __init__(self) -> None:
        pass

    #--------------------Reading Dataframe--------------------#
    # Preloads the data
    data_raca = GetEmploeey.data.merge(GetpersonalData.raca_cor,
                                            on='Nome Funcionário',
                                            how='left')


    #--------------------Generating the dependents Spreadsheet--------------------#
    # Using pandas melt methods to link each dependent to the single employee
    dependenttype_column = pd.melt(data_raca.reset_index(),
                            id_vars=['employee_id'],
                            value_vars=['Parentesco Dependente 1',
                                        'Parentesco Dependente 2',
                                        'Parentesco Dependente 3'],
                            value_name='Parentesco Dependente').drop('variable',1)

    cpf_dependent = pd.melt(data_raca.reset_index(),
                        id_vars=['employee_id'],
                        value_vars=['CPF Dependente 1',
                                    'CPF Dependente 2',
                                    'CPF Dependente 3'],
                        value_name='CPF Dependente').drop('variable',1)

    name_dependet = pd.melt(data_raca.reset_index(),
                        id_vars=['employee_id'],
                        value_vars=['Nome Dependente 1',
                                    'Nome Dependente 2',
                                    'Nome Dependente 3'],
                        value_name='Nome Dependentes').drop('variable',1)

    birthdate_dependet = pd.melt(data_raca.reset_index(),
                        id_vars = ['employee_id'],
                        value_vars = ['Nascimento Dependente 1',
                                    'Nascimento Dependente 2',
                                    'Nascimento Dependente 3'],
                        value_name='Dt. Nascimento Dependentes').drop('variable',1)

    # Concatenates the two new dependency spreadsheets into a single one
    dependents_sheet = (pd.concat([name_dependet,
                        cpf_dependent['CPF Dependente'],
                        dependenttype_column['Parentesco Dependente'],
                        birthdate_dependet['Dt. Nascimento Dependentes'],],axis=1).fillna(''))


    dependents_sheet.insert(0,'id','')
    dependents_sheet.insert(3,'Possui Dependente?','')

    dependents_sheet['created_at'] = GetEmploeey.today
    dependents_sheet['updated_at'] = GetEmploeey.today

    # Fills in the column informing whether the employee has dependents or not
    # according to the dependentType column

    for indicator, line in dependents_sheet.iterrows():
        if line['Nome Dependentes'] != '':
            dependents_sheet.loc[indicator, 'Possui Dependente?'] = True
        else:
            dependents_sheet.loc[indicator, 'Possui Dependente?'] = False


    get_uuid4(dependents_sheet,'employee_id','id')

    # Save the new spreadsheet
    dependents_sheet.to_csv('program\\output_sheets\\dependentes.csv',index=False,encoding='utf-8')
