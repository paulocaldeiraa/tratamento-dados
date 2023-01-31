'''Import the packages'''
import os
from src.employee import GetEmploeey
from src.personal_data import GetpersonalData
from src.salary import GetSalary
from src.position import Getposition
from src.positionallocation import GetpositionAllocation
from src.dependent import Getdependent
from src.acquisition import Getacquisition


GetEmploeey() # Creates emploeey spreadsheet
GetpersonalData() # Creates personalData spreadsheet
GetSalary() # Creates salary spreadsheet
Getposition() # Creates position spreadsheet
GetpositionAllocation() # Creates positionAllocation spreadsheet
Getdependent() # Creates dependet spreadsheet
Getacquisition() # Creates acquisition spreadsheet



# Remove the temp files
if os.path.exists('planilhas\\salario_temp_historico.csv'):
    os.remove('planilhas\\salario_temp_historico.csv')

if os.path.exists('planilhas\\cargo_temp_historico.csv'):
    os.remove('planilhas\\cargo_temp_historico.csv')
