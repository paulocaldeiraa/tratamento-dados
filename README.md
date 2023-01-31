<h1 align="center"> Tratamento de Dados </h1>

![VsCode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

# :scroll: Índice

* [Índice](#scroll-índice)
* [Problematização](#interrobang-problematização)
* [Pandas](#panda_face-pandas)
    * [pd.apply](#pdapply)
    * [pd.drop](#pddrop)
    * [pd.fillna](#pdfillna)
    * [pd.insert](#pdinsert)
    * [pd.melt](#pdmelt)
    * [pd.merge](#pdmerge)
    * [pd.replace](#pdreplace)
    * [pd.shift](#pdshift)
    * [pd.stack e pd.unstack](#pdstack-e-pdunstack)
    * [pd.tail](#pdtail)
    * [pd.to_datetime](#pdto_datetime)
* [UUID](#key-uuid)
* [Faker](#clown_face-faker)



# :interrobang: Problematização

Imagina que você trabalha para uma empresa que está desenvolvendo um sistema para um dos setores. Nesse setor, existem muitas planilhas e os funcionários estão tendo dificuldade em organizar e manter as informações.

A equipe de TI entra em ação e arquiteta um programa para automatizar essa demanda. Seu trabalho é preparar todas as planilhas bagunçadas, gerar novas em formato CSV contendo apenas as informações mais relevantes, seguindo o modelo de dados desenhado. Isso irá garantir uma importação segura e organizada dos dados para o sistema novo.

Tendo em mente a situação simulada acima a ideia do projeto é explorar a biblioteca Pandas do Python, testando as múltiplas opções e observando os resultados. Também vou utilizar UUID que gera ID's aleatórios e o FAKER que cria dados falsos. Assim o projeto tem como objetivo servir de guia, principalmente para alguns dos recursos do Pandas, podendo ser consultado sempre que achar necessidade.


# :panda_face: Pandas

O Pandas é uma ferramenta rápida, poderosa, flexível e fácil de usar, de análise e manipulação de dados. Essa biblioteca é de código aberto e foi construída em cima da linguagem de programação Python. Você pode conferir toda a documentação [clicando aqui](https://pandas.pydata.org/docs/reference/frame.html).


## pd.apply

> **__SINTAXE:__** DataFrame.apply(func, axis=0, raw=False, result_type=None, args=(), **kwargs)

O método apply aplica uma função ao longo dataframe. Essa aplicabilidade pode ser definida pelo index (axis=0), ou pela coluna (axis=1). O retorno do apply vai ser o que for especificado pela função que ele vai aplicar no dataframe. 

Um exemplo bem simples de como usar apply:

```
def alt_caractere(caractere):
    caractere = caractere.replace('a','b')
    return caractere

df = pd.DataFrame(
    {'col_1': [1],
    'col_2': ['a']}
)

df.apply(alt_caractere)

# Resultado:
    col_1 col_2
0    1    b
```

Na documentação em inglês você encontra mais detalhes e exemplos. Só [clicar aqui](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html). 

## pd.drop

> **__SINTAXE:__** DataFrame.drop(labels=None, *, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')

O drop é utilizado para excluir linhas ou colunas do dataframe. Precisamos passar o nome correspondente ou indicar o index que deve ser removido. 
Existem outros métodos para excluir linhas ou colunas e estes são específicos como: 
- drop_duplicates: remove os duplicados
- dropna: remove valores missing (faltantes)

Ao longo do projeto vou detalhar e exemplificar melhor cada uma. A documentação do drop é [essa aqui](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html).
Você também pode ver um simples exemplo de como utiliza-lo. 

```
df = pd.DataFrame(
    {'col_1': [1],
    'col_2': ['a']}
)
# Caso queira apagar a coluna 2, podemos usar o 'columns' que recebe o nome da coluna 
df.drop(columns='col_2')

# Resultado 
    col_1
0    1

# Podemos também passar o index da coluna e obter o mesmo resultado
df.drop('col_2', axis=1)

# Resultado 
    col_1
0    1
```

## pd.fillna

> **__SINTAXE:__** DataFrame.fillna(value=None, *, method=None, axis=None, inplace=False, limit=None, downcast=None)

O fillna preenche um valor missing no dataframe. Esse método pode parecer simples mas ele é muito útil quando estamos lidando com uma grande quantidade de dados. Um dos parâmetros que fillna recebe é 'method' que por padrão vem como None, mas podemos passar por exemplo 'ffill' que faz com que, pegue o último valor válido e preencha a próxima célula missing com ele. Vou detalhar esse método quando estiver trabalhando com ele no projeto. Por agora você pode conferir a [documentação oficial](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html?highlight=fillna#pandas.DataFrame.fillna). 


## pd.insert

> **__SINTAXE:__** DataFrame.insert(loc, column, value, allow_duplicates=_NoDefault.no_default)

Com o insert você insere uma coluna nova no dataframe no local especificado. Basicamente você diz ao pandas, em qual posição quer a coluna, o nome da coluna e os valores.
Você também encontra a documentação [aqui](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.insert.html). 

```
df = pd.DataFrame(
    {'col_1': [1],
    'col_2': ['a']}
)

df.insert(1, 'col_3', 'abc')

# Resultado
    col_1 col_3 col_2
0   1     abc   a

# Se eu quisesse a col_3 no final, bastava mudar o parâmetro loc
df.insert(2, 'col_3', 'abc')

# Resultado
    col_1 col_2 col_3
0   1     a     abc
```

## pd.melt

> **__SINTAXE:__** pandas.melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value', col_level=None, ignore_index=True)

O melt reformula o dataframe, ele muda a orientação saindo de um formato amplo para um longo. Usamos melt quando queremos plotar cada item e analisar como estão distribuídos os valores. Ele retorna um dataFrame transformado que contém uma ou mais colunas identificadoras e apenas duas colunas não-identificadoras nomeadas variável e valor. Vou utilizar um exemplo que encontrei no site [DelftStack](https://www.delftstack.com/pt/api/python-pandas/pandas-dataframe-dataframe.melt-function/).

```
# Criamos um df com 3 colunas 

dataframe=pd.DataFrame({'Attendance': {0: 60, 1: 100, 2: 80,3: 78,4: 95},
                    'Name': {0: 'Olivia', 1: 'John', 2: 'Laura',3: 'Ben',4: 'Kevin'},
                    'Obtained Marks': {0: '90%', 1: '75%', 2: '82%',3: '64%',4: '45%'}})

# Usando o método e identificando apenas a coluna 'Name'
# Como resultado vamos ter o agrupamento dos nomes e as duas colunas não-identificadoras

dataframe1 = pd.melt(dataframe, 
                     id_vars=['Name'])

# Resultado
     Name        variable value
0  Olivia      Attendance    60
1    John      Attendance   100
2   Laura      Attendance    80
3     Ben      Attendance    78
4   Kevin      Attendance    95
5  Olivia  Obtained Marks   90%
6    John  Obtained Marks   75%
7   Laura  Obtained Marks   82%
8     Ben  Obtained Marks   64%
9   Kevin  Obtained Marks   45%
```
Confira a [documentação oficial](https://pandas.pydata.org/docs/reference/api/pandas.melt.html) do método.


## pd.merge

> **__SINTAXE:__** DataFrame.merge(right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)

Com o merge é possível unir dois dataframes por coluna ou por index. Caso queira unir por coluna, o index de ambos os dataframes serão ignorados. O merge é bastante utilizado nesse projeto porque permite, de forma muito similar, fazer a função 'xlookup' do Excel. Como vamos trabalhar com varias planilhas as vezes em uma, consta algumas informações que não tem em outra, o merge conseguir unir e resolver esse problema. Vou deixar a [documentação oficial](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html?highlight=merge#pandas.DataFrame.merge) e exemplificar melhor ao longo do trabalho. 

## pd.replace

> **__SINTAXE:__** DataFrame.replace(to_replace=None, value=_NoDefault.no_default, *, inplace=False, limit=None, regex=False, method=_NoDefault.no_default)

Replace é um método muito útil para lidar com string (textos), é usado para substituir palavras ou trechos. Vou utilizar em diversas partes do projeto para remover ou alterar strings das tabelas. Um exemplo para limpar o dataframe é utilizar o replace para remover caracteres indesejados. 

```
df = pd.DataFrame(
    {'col_1': [1,2,3,4],
    'col_2': ['a','b','c','d']}
)

df.replace('a',1)

# Resultado
    col_1	col_2
0	    1	1
1	    2	b
2	    3	c
3	    4	d

# Ou podemos passas mais de um valor em um dicionário
df.replace({'a':1, 'b':2})

# Resultado
    col_1	col_2
0	    1	1
1	    2	2
2	    3	c
3	    4	d
```

Vamos ver mais exemplos do replace durante o projeto. Você pode consultar a [documentação oficial aqui](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html?highlight=replace#pandas.DataFrame.replace).

## pd.shift

> **__SINTAXE:__**  DataFrame.shift(periods=1, freq=None, axis=0, fill_value=_NoDefault.no_default)

O shift é usado para deslocar o index do dataframe. Ele recebe o parâmetro 'periods' que determina a quantidade de linhas que vão se deslocar, de cima para baixo. Enquanto desloca a novas linhas recebem NaN (valor missing) por padrão.

```
df = pd.DataFrame(
    {'col_1': [1,2,3,4],
    'col_2': ['a','b','c','d']}
)

df.shift(periods=1)

# Resultado
	col_1	col_2
0	NaN	    NaN
1	1.0	    a
2	2.0	    b
3	3.0	    c


```
Se caso eu quisesse inverter a ordem e deslocar de baixo para cima bastava alterar o parâmetro 'periods' para -1 (df.shift(periods=-1)). Também é possível deslocar colunas inteiras usando o parâmetro 'axis' como no exemplo, vamos usar o mesmo dataframe.

```
df.shift(periods=1, axis=1)

# Resultado
    col_1	col_2
0	NaN	    1
1	NaN	    2
2	NaN	    3
3	NaN	    4   

```

Perceba que agora o eixo se desloca da esquerda para a direita, se quiser alterar essa ordem, é so mudar novamente o parâmetro 'periods' para -1. Confira a [documentação oficial](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html?highlight=shift#pandas.DataFrame.shift) do pandas.


## pd.stack e pd.unstack

> **__SINTAXE:__** DataFrame.stack(level=- 1, dropna=True)

> **__SINTAXE:__** DataFrame.unstack(level=- 1, fill_value=None)

O stack e o unstack do Pandas fazem a rotação das colunas para as linhas e vice-versa. Tanto o stack quanto o unstack são usados para remodelar os dataframes, são adequados quando estamos lidando com tabelas de muilti-index. No stack obtemos como resultado a transformação da coluna de interesse em um index. Já no unstack faz exatamente o oposto, retomando o dataframe. Tabelas muilti-index são mais complexas do que as convencionais, no projeto vou abordar com mais detalhes e exemplificando esses dois métodos do pandas. Aqui você pode encontrar a [documentação oficial do stack](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.stack.html) e aqui a [documentação oficial do unstack](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.unstack.html)


## pd.to_datetime

> **__SINTAXE:__**  pandas.to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)

Esse método converte uma série em um objeto do tipo pandas datetime. É ideal para trabalhar com datas nas tabelas e evitar erros na hora de fazer importação, definindo o formato correto do banco de dados. Também é bastante útil quando as datas estão guardadas como string ou não são reconhecidas como data. Vou deixar para exemplificar o to_datetime ao longo do projeto, agora você pode conferir a [documentação](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html?highlight=to_datetime) e alguns exemplos no site do pandas.


# :key: UUID

O UUID gera ID's únicos e imutáveis e essa biblioteca será muito valiosa no processo. Para o projeto temos muitas planilhas e cada linha de cada planilha e pode ser referente a um único dado. Atribuindo esse ID único gerado, garante que na hora da importação todas as informações serão direcionadas para cada ID. O UUDI é uma biblioteca que não vem inclusa no pacote do Anaconda, por exemplo. Talvez haja a necessidade de instalar e para isso pasta digitar o comando no terminal: 

> **__NOTA:__** pip install uuid

A geração dos ID's podem ocorrem de algumas formas, como queremos que cada um seja único a [documentação oficial](https://docs.python.org/3/library/uuid.html) recomenda que usamos o uuid4(). Assim, vou criar uma função no python que vai gerar o ID sempre que for preciso.

Os ID's gerados pelo UUID são como no exemplo:

```
import uuid 

uuid.uuid4()

# Resultado
UUID('ceb0da33-dbca-472d-bee1-4e0680356af6')

```

# :clown_face: Faker

O faker gera dados falsos aleatórios para popular o dataframe. Vou utilizar pra preencher todas as planilhas, criando nomes, documentos, email e tudo mais que for necessário. Faker é uma biblioteca bastante fácil e intuitiva de usar. Assim como UUID é necessário fazer a instalação desse pacote. 

> **__NOTA:__** pip install faker

Vou deixar um exemplo aqui da utilização do faker e indicar a [documentação oficial](https://faker.readthedocs.io/en/master/) para mais detalhes.

```
from faker import Faker 
fake = Faker()

fake.name()

#Resultado 
'Brenda Duran'

fake.address()

#Resultado
'740 Ana Club Suite 945\nWest Edgarfort, WV 26740'

```
