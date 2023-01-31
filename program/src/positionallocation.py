'''Import the packages'''
import pandas as pd
from src.employee import GetEmploeey
from src.position import Getposition
from src.functions import get_uuid4, xlookup


class GetpositionAllocation:
    '''
    Fifth generated spreadsheet
    In this step the processing of the fourth generated spreadsheet takes place.
    Each job ID generated in the previous step is used here, to assign these jobs to the employees
    '''
    def __init__(self) -> None:
        pass

    #--------------------Reading Dataframe--------------------#
    # Preloads the data
    cargos_hist = pd.read_csv('planilhas\\cargo_temp_historico.csv',sep = ',')
    cargos_merge = GetEmploeey.data.merge(cargos_hist,
                                on='Nome Funcionário',
                                how='left')


    #--------------------Generating the positionAllocation Spreadsheet--------------------#
    # Fill in the start dates with the admission dates
    cargos_merge['Inicial'].fillna(
    cargos_merge['Dt. Admissão'],inplace=True)

    # Uses the xlookup function:
    # (which is very similar to the Excel function) to find the reference values
    cargos_merge['get_leader_id'] = cargos_merge['Gestor'].apply(xlookup, args=(
        GetEmploeey.employee_sheet['Nome'],GetEmploeey.employee_sheet['id']))


    cargos_merge['get_position_id'] = cargos_merge['Cargo'].apply(xlookup, args=(
        Getposition.position_sheet['Nome Cargo'],Getposition.position_sheet['id']))


    cargos_merge['get_position_id_2'] = cargos_merge['Nome Cargo'].apply(xlookup, args=(
        Getposition.position_sheet['Nome Cargo'],Getposition.position_sheet['id']))


    positionallocation_sheet = pd.DataFrame({'Cargo_id': cargos_merge['get_position_id'],
                                        'employee_id': cargos_merge['employee_id'],
                                        'Inicial': cargos_merge['Inicial'],
                                        'Final': cargos_merge['Final'],
                                        'Vinc.Empreg.': cargos_merge['Vinc.Empreg.'],
                                        'ID_Lider': cargos_merge['get_leader_id'],
                                        'Criado_em': GetEmploeey.today,
                                        'Upload_em': GetEmploeey.today})


    positionallocation_sheet.insert(0,'id','') # Creat the new column on dataframe

    get_uuid4(positionallocation_sheet,'employee_id','id')

    # To fill the new column
    positionallocation_sheet['Cargo_id'].fillna(cargos_merge['get_position_id_2'], inplace=True)


    # Save the new spreadsheet
    positionallocation_sheet.to_csv('program\\output_sheets\\cargos_historico.csv',index=False)
