'''Import the packages'''
import pandas as pd
from src.functions import get_uuid4
from src.employee import GetEmploeey

class GetpersonalData:
    '''
    Second generated worksheet.
    In this step the main emploeey spreadsheet is merged with
    another HR spreadsheet that contains personal information.
    '''
    def __init__(self) -> None:
        pass

    #--------------------Reading Dataframe--------------------#
    # Preloads the data
    # Load a second HR worksheet
    raca_cor = pd.read_excel('planilhas\\raca_cor_dependentes.xlsx')

    # Merges the two HR spreadsheets with pd.merge
    data_raca = GetEmploeey.data.merge(raca_cor,
                    on='Nome Funcionário',
                    how='left')

    #--------------------Generating the personalData Spreadsheet--------------------#
    personaldata_sheet = pd.DataFrame({'employee_id': data_raca['employee_id'],
                                'CPF': data_raca['CPF'],                        
                                'Nome': data_raca['Nome Funcionário'],
                                'Email': data_raca['E-Mail'],
                                'Telefone': data_raca['Celular'],
                                'RG': data_raca['RG'],
                                'Nacionalidade': data_raca['Nacionalidade'],
                                'Dt. Nascimento': data_raca['Dt. Nascimento'],
                                'Sexo': data_raca['Sexo'],
                                'Raça e Cor': data_raca['Raça/Cor'],
                                'Estado Civil': data_raca['Est. Civil'],
                                'Mãe': data_raca['Mãe'],
                                'Pai': data_raca['Pai'],
                                'Endereço Completo': data_raca['Endereço'],
                                'Criado_em': GetEmploeey.today,
                                'Upload_em': GetEmploeey.today})


    personaldata_sheet.insert(0,'id','') #Creat the new column on dataframe

    get_uuid4(personaldata_sheet,'employee_id','id') # Use the function to generate the ID

    # Save the new spreadsheet
    personaldata_sheet.to_csv('program\\output_sheets\\dados_pessoais.csv', index=False)
    