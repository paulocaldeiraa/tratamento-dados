'''Import the packages'''
import os
import pandas as pd
from src.functions import replace_str


class CreateSalaryandPositionSheet:
    '''
    A separate process to adapt the HR spreadsheet.
    The spreadsheet in question has too many Excel merges and formulas.
    When loading it, it does not behave the way you want.
    This class allows you to clean the data to obtain only the necessary 
    information for the process.
    '''

    def __init__(self) -> None:
        pass

    #--------------------Reading Dataframe--------------------#
    # The HR spreadsheet is full of merging and special characters.
    # For this reason it is better to convert to csv

    df = pd.read_excel('planilhas\\historico_empregado.xls')

    df.to_csv('planilhas\\temp_salario_cargo.csv',
                        index=False,
                        header=False,
                        sep = ',')

    salario_cargo = pd.read_csv('planilhas\\temp_salario_cargo.csv',header=None)

    #--------------------Setting up the required Dataframes--------------------#
    # Removal of inappropriate characters and correction of the header
    salario_cargo.drop([0,1,2,3,4,5], inplace=True)
    salario_cargo.drop([1,2,3,4,5,6,8,10,11,12,13,14], axis=1,inplace=True)
    salario_cargo.replace('00:00:00',' ',regex=True,inplace=True)

    # Renames the header appropriately
    salario_cargo.rename(columns={0:'Nome', 7:'data', 9:'obs'},inplace=True)

    # Fills in the rest of the column with the employee names,
    # and deletes duplicates for better identification during the process
    salario_cargo['Nome'].fillna(axis=0,method='ffill',inplace=True)
    salario_cargo.dropna(subset=['data','obs'],thresh=1,inplace=True)
    salario_cargo.reset_index(drop=True,inplace=True)

    #--------------------Setting up the required Dataframes - part 2--------------------#
    # Sorting strings to get the relevant information out
    for index, row in enumerate(salario_cargo['obs']):

        troca_salario = 'ALTERAÇÃO SALARIAL'
        troca_cargo = 'TROCA DE CARGO'

        if troca_salario in row:
            copia_valor = salario_cargo.loc[index+1,'obs']
            salario_cargo.loc[index, 'obs'] = salario_cargo.loc[index, 'obs'] + ' ' + copia_valor

        if troca_cargo in row:
            copia_valor_1 = salario_cargo.loc[index+1,'obs']
            copia_valor_2 = salario_cargo.loc[index+2,'obs']
            salario_cargo.loc[index, 'obs'] = salario_cargo.loc[index, 'obs'] + ' ' \
            + copia_valor_1 + ' ' + copia_valor_2

    # Reset index
    salario_cargo.reset_index(drop=True,inplace=True)


    #--------------------Creating the new dataframes--------------------#
    # Creates a list of important information,
    # which will be used to generate the columns of the new dataframes
    salario_nome = []
    salario_data = []
    salario = []

    cargo_nome = []
    cargo_data = []
    cargo = []


    for index, row in enumerate(salario_cargo['obs']):
        if troca_salario in row:
            salario_nome.append(salario_cargo.loc[index, 'Nome'])
            salario_data.append(salario_cargo.loc[index, 'data'])
            salario.append(row)

        if troca_cargo in row:
            cargo_nome.append(salario_cargo.loc[index, 'Nome'])
            cargo_data.append(salario_cargo.loc[index, 'data'])
            cargo.append(row)


    # Generate the two new dataframes
    df_salario = pd.DataFrame({
        'Nome Funcionário': salario_nome,
        'Data': salario_data,
        'Salário': salario
    })

    df_cargo = pd.DataFrame({
        'Nome Funcionário': cargo_nome,
        'Data': cargo_data,
        'Cargo': cargo
    })

    #--------------------Setting up the required Salary_DF--------------------#
    # Splits columns according to a separator
    df_salario[['Salário','obs']] = df_salario['Salário'].str.split('. R',expand=True)

    # Replaces strings to better visualize and/or remove information that is not relevant
    df_salario['obs'].replace('etroativo a ', 'Retroativo a ', regex=True,inplace=True)
    df_salario.replace({'ALTERAÇÃO SALARIAL de:':'','para': ''},inplace=True, regex=True)

    # Reorganizes the entire dataframe to obtain the proper and functional
    # structure for the import process in the database.
    # This restructuring is important so that the new spreadsheets communicate with the others.
    df_salario = df_salario.set_index(['Nome Funcionário',
                                'Data']).stack().str.split(':',
                                expand=True).stack().unstack(-2).reset_index(-1,
                                drop=True).reset_index()

    # Applies the function 'replace_str' to normalize the columns
    df_salario['Salário'] = df_salario['Salário'].apply(replace_str)
    df_salario['Data'] = df_salario['Data'].apply(replace_str)

    #--------------------Get Salary_DF--------------------#
    """
    Since each entry in the HR spreadsheet are in pairs,
    the logic used to organize the entry and exit dates was done this way:

    Every salary change we know the date of the new one,
    but not the old one, so it always needs to start with endDate (odd entries).
    Right below it always comes the new salary, so they refer to the even index.

    Based on that, this piece of code defines the start and end date of a salary and job change.
    """

    df_salario.insert(2,'Final', df_salario.index % 2 == 1)
    df_salario.loc[df_salario['Final'] == False, 'Final'] = df_salario['Data']
    df_salario['Final'].replace(True,'',inplace=True)

    df_salario.insert(2,'Inicial', df_salario.index % 2 == 1)
    df_salario.loc[df_salario['Inicial'] == True, 'Inicial'] = df_salario['Data']
    df_salario['Inicial'].replace(False,'',regex=True,inplace=True)

    df_salario.drop(columns=['Data'], inplace=True)

    df_salario['Duplicados'] = df_salario['Salário'].shift(-1)==df_salario['Salário']

    for index, row in df_salario.iterrows():
        query = row['Duplicados'] == True
        if query is True:
            df_salario.loc[index, 'Final'] = df_salario.loc[index+1, 'Final']
            df_salario.drop(index+1, inplace=True)

    df_salario.drop(columns=['Duplicados'], inplace=True)

    df_salario.to_csv('planilhas\\salario_temp_historico.csv', index=False)

    #--------------------Setting up the required Job_DF--------------------#
    df_cargo.replace('TROCA DE CARGO: ','',inplace=True, regex=True)

    # The logic is the same for creating the salary schedule
    df_cargo = df_cargo.set_index(['Nome Funcionário',
                            'Data']).stack().str.split(' para ',
                            expand=True).stack().unstack(-2).reset_index(-1,
                            drop=True).reset_index()

    df_cargo['Cargo'].replace('[0-9]','',regex=True,inplace=True)
    df_cargo['Cargo'].replace('  - ','',regex=True,inplace=True)
    df_cargo['Cargo'].replace(' - ','',regex=True,inplace=True)

    #--------------------Get Job_DF--------------------#
    # The logic is the same for creating the salary schedule
    df_cargo.insert(2,'Final', df_cargo.index % 2 == 1)
    df_cargo.loc[df_cargo['Final'] == False, 'Final'] = df_cargo['Data']
    df_cargo['Final'].replace(True,'',inplace=True)

    df_cargo.insert(2,'Inicial', df_cargo.index % 2 == 1)
    df_cargo.loc[df_cargo['Inicial'] == True, 'Inicial'] = df_cargo['Data']
    df_cargo['Inicial'].replace(False,'',regex=True,inplace=True)

    df_cargo.drop(columns=['Data'], inplace=True)

    df_cargo['Duplicados'] = df_cargo['Cargo'].shift(-1)==df_cargo['Cargo']

    for index, row in df_cargo.iterrows():
        query = row['Duplicados'] == True
        if query is True:
            df_cargo.loc[index, 'Final'] = df_cargo.loc[index+1, 'Final']
            df_cargo.drop(index+1, inplace=True)

    df_cargo.drop(columns=['Duplicados'], inplace=True)

    df_cargo.to_csv('planilhas\\cargo_temp_historico.csv',index=False)

    #--------------------Delete the CSV--------------------#
    if os.path.exists('planilhas\\temp_salario_cargo.csv'):
        os.remove('planilhas\\temp_salario_cargo.csv')
