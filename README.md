# afn2afd

------------------------------

Linguagem de implementação:
python3

Dependencias:

Interpretador Python3.4

Instalar dependências:
sudo apt-get install python3

Execução do script:
python3 main.py

------------------------------

O arquivo de entrada deve estar nomeado 'teste1AfndAfd.in' e estar no mesmo diretório de execução do script.
O arquivo de saída se chamará 'teste1AfndAfd.out' e será escrito no mesmo diretório.

O arquivo de texto de entrada pode conter N espaços, sendo divididos por linhas.
As colunas são dividas pelo caractere "|".

A primeira linha deve conter obrigatóriamente o cabeçalho do arquivo.
Que segue o formato:
vazio | simbolo1 | simbolo2 | ... | simboloN | eps
No caso, eps representa epsilon.
eps deve ser minúsculo e não necessariamente precisa ser no final da tabela.

O arquivo pode conter N linhas, da segunda em diante sendo referente aos estados do automato.
Segue o formato:
estadoAtual | estado(s)PorSimbolo1  | estado(s)PorSimbolo1 | ... | estado(s)PorSimboloN | estado(s)PorEps
Se houver mais de um estado resultante, eles devem estar separados por vírgulas:
q1,q2,q3 - podendo conter espaços entre eles -> q1, q2, q3
Se não houver uma transição pelo produto de (estado, símbolo), representar com o caractére '-'.

Os símbolos do alfabeto são definidos pelos símbolos do cabeçalho.
Os estados são definidos pela parte da tabela referentes ao estado atual.
O estado morto é desconsiderado.

Na parte de estado atual:

1. Para indicar que um estado é inicial, utilizar '--' antes do estado. Só deve haver um estado inicial. No caso de mais de um, apenas a última linha com o símbolo '--' será contabilizada.
Ex: '--q1'

2. Para indicar que um estado é final, utilizar '*' após o estado. Podendo haver N estados finais.

3. A parte de estado atual só aceita um estado, se houver mais de um estado.


Exemplos de tabelas de entrada:

1. Com epsilon transição:
       |    a    |   b   |    eps    |<br>
--q1*  |    -    |   q2  |    q3     |
  q2   |  q2,q3  |   q3  |     -     |
  q3   |    q1   |   -   |     -     |

2. Sem epsiolon transição:
       |    a    |   b   |
--q1*  |    -    |   q2  |
  q2   |  q2,q3  |   q3  |
  q3   |    q1   |   -   |