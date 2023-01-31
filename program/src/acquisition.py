'''Import the packages'''
import os
import pandas as pd
from src.employee import GetEmploeey
from src.functions import get_uuid4

class Getacquisition:
    '''
    Seventh generated worksheet
    In this step loads the worksheet that refers to vacations.
    Using it it is possible to make a merge with the main sheet
    and thus load only the necessary information for importation
    '''

    #--------------------Reading Dataframe--------------------#
    # Preloads the data
    df = pd.read_excel('planilhas\\historico_ferias.xls')
    df.to_csv('planilhas\\ferias_temp.csv',index=False, header=False)
    ferias = pd.read_csv('planilhas\\ferias_temp.csv',header=None)

    #--------------------Prepare the Dataframe--------------------#
    # Delete unnecessary lines and columns

    ferias.drop([0,1,2,3,4,5], inplace=True)
    ferias.drop(ferias.tail(3).index,inplace=True) # delete 3 last rows
    ferias.drop([0,1,3,4,5,6,7,8,11,
                    12,15,18,19,20,22,23,
                    21,24,25,26,31,36,34,
                    27,29,35,37],axis=1, inplace=True)

    # Renames the columns to keep the standard of the main spreadsheet
    ferias.rename(columns={2:'Nome Funcionário',
                    9: 'Data Admissão',
                    10: 'Vencimento Férias',
                    13: 'Fer. Venc.',
                    14: 'Fer. Pro.',
                    16: 'Início aquisitivo',
                    17: 'Fim aquisitivo',
                    33: 'Limite p/ gozo',
                    30: 'Dias gozados',
                    28: 'Dias dir.',
                    32: 'Dias restantes'
                    },inplace=True)

    # Fill the empty lines with the name of the employee above
    ferias['Nome Funcionário'].fillna(axis=0,method='ffill',inplace=True)
    ferias['Data Admissão'].fillna(axis=0,method='ffill',inplace=True)

    # Fix the date format
    ferias['Data Admissão'] = ferias['Início aquisitivo'].astype('datetime64')
    ferias['Início aquisitivo'] = ferias['Início aquisitivo'].astype('datetime64')
    ferias['Fim aquisitivo'] = ferias['Fim aquisitivo'].astype('datetime64')
    ferias['Limite p/ gozo'] = ferias['Limite p/ gozo'].astype('datetime64')


    data_ferias = GetEmploeey.data.merge(ferias,
                            on='Nome Funcionário',
                            how='right')

    #--------------------Generating the acquisition Spreadsheet--------------------#
    acquisition_sheet = pd.DataFrame({'employee_id': data_ferias['employee_id'],
                                    'Name': data_ferias['Nome Funcionário'],
                                    'Início do período': data_ferias['Início aquisitivo'],
                                    'Fim do período': data_ferias['Fim aquisitivo'],
                                    'Limite p/ gozo': data_ferias['Limite p/ gozo'],
                                    'Status': True,
                                    'Criado_em': GetEmploeey.today,
                                    'Upload_em': GetEmploeey.today})


    acquisition_sheet.insert(0,'id','') # Creat the new column on dataframe

    get_uuid4(acquisition_sheet,'employee_id','id')

    # Save the new spreadsheet
    acquisition_sheet.to_csv('program\\output_sheets\\ferias.csv', index=False)

    if os.path.exists('planilhas\\ferias_temp.csv'):
        os.remove('planilhas\\ferias_temp.csv')
