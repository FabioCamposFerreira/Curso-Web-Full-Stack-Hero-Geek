# Estudo de Caso: Cálculo de Salário de Funcionário

Um funcionário enviou o registro de suas horas trabalhadas. Seu objetivo é analisar os registros um a um e excluir os que estiverem incorretos. 

Além disso, você precisa calcular o valor total a ser pago, considerando o salário de R$ 10,00 por hora.

Para automatizar esse processo, será desenvolvido um aplicativo desktop utilizan

<img src="./Estudo%20de%20Caso.png" alt="Estudo de Caso" width="500">

## Dicas

* Será apenas uma tela.
* O botão "Excluir" deve apenas remover o dia da tela.
* O arquivo banco_dados.sql criará a tabela Ponto com as colunas:
   * id (int)
   * data (datetime)
   * horas (float)
* O arquivo banco_dados.py deve conter as funções criar_banco e pegar_todos_pontos.
* O arquivo main.py conterá as funções tela_pontos, excluir_ponto e calcular_total.
* O nome do funcionário é fixo.
