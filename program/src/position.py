'''Import the packages'''
import numpy as np
import pandas as pd
from src.employee import GetEmploeey
from src.functions import get_uuid4

class Getposition:
    '''
    Fourth generated spreadsheet
    In this step the third HR worksheet is processed,
    where it contains information about salary and job.
    Here we will generate the positon sheet.
    '''

    def __init__(self) -> None:
        pass

    #--------------------Reading Dataframe--------------------#
    # Preloads the data
    cargos = pd.read_excel('planilhas\\cargos.xlsx')


    # Creat new column to fill seniority in position_sheet
    cargos['Senioridade'] = np.nan


    # Variable to check if in position have seniority
    pleno = 'PLENO'
    pleno_sig = 'PL'
    junior = 'JUNIOR'
    junior_sig = 'JR'
    senior = 'SENIOR'

    # If the position have seniority, then copy this value in the new column
    for index, row in enumerate(cargos['Nome Cargo']):
        if pleno in row:
            copy_pleno = pleno
            cargos.loc[index, 'Senioridade'] = copy_pleno

        if pleno_sig in row:
            copy_pleno_sig = pleno
            cargos.loc[index, 'Senioridade'] = copy_pleno_sig

        if junior in row:
            copy_junior = junior
            cargos.loc[index, 'Senioridade'] = copy_junior

        if junior_sig in row:
            copy_junior_sig = junior
            cargos.loc[index, 'Senioridade'] = copy_junior_sig

        if senior in row:
            copy_senior = senior
            cargos.loc[index, 'Senioridade'] = copy_senior

    # Fill all missing values whit 'Pleno' seniority
    cargos['Senioridade'].fillna(pleno,inplace=True)

    #--------------------Generating the position Spreadsheet--------------------#
    position_sheet = pd.DataFrame({'Nome Cargo':cargos['Nome Cargo'],
                                'Senioridade': cargos['Senioridade'],
                                'Setor': cargos['Setor'],
                                'Criado_em': GetEmploeey.today,
                                'Upload_em': GetEmploeey.today})

    position_sheet.insert(0,'id','')

    get_uuid4(position_sheet,'Nome Cargo','id')

    position_sheet.to_csv('program\\output_sheets\\todos_cargos.csv', index=False)
    