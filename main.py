import mysql.connector
import time

ip = input('Qual o IP da maquina que deve restaurada a T_Venda\n')
dia = input('Qual o dia que ver voltar a T_venda? EXEMPL0 (2022-01-16)\n')


conexao = mysql.connector.connect(
    host=f"{ip}",
    user='root',
    password='',
    database='PDV',
)
cursor = conexao.cursor()


# VERIFICA A QUANTOS REGISTROS TEM QUE SER CRIADO
def quantidade():

    cont = f"SELECT COUNT(id) FROM CFe WHERE datafiscal = '{dia}'"

    cursor.execute(cont)

    resultado = cursor.fetchall()  # ler o banco de dados

    return resultado

numero = quantidade()[0][0]



# PUXA O CODIGO DE VENDA NA EXISTENTE NA TABELA CFE

def codvenda():

    comando = f"SELECT cod_venda FROM CFe WHERE datafiscal = '{dia}' order by cod_venda"

    cursor.execute(comando)

    resultado = cursor.fetchall()  # ler o banco de dados

    return resultado

def insert():

    contador = 0

    while contador < numero:

        comando = f"INSERT INTO T_Venda (tipo_trans, cod_venda, nPDV, nECF, nEstab, datahora, datahoraECF, vendaEncerrada, nroCupomECF, cod_venda_canc, motivo_canc, cod_Cli, PAN, IDPDV, ID, usuario_canc, consolidadaPDV, TEFConsultado, convAprovado, IdTransacao, chequeCadastrado, IdTransacaoCanc, usuariocanc_original, coo, nrreducao, datafiscal, cupomnestle, VALORBRUTO, VALORCANCELADO, VALORLIQUIDO, VALORBASECALC01, VALORBASECALC02, VALORBASECALC03, VALORBASECALC04, VALORBASECALC05, VALORBASECALC06, VALORBASECALC07, VALORBASEISENTO, VALORBASESUBST, segundaViaEmitida, nrserieecf, pdvrestaurante, controlevenda, datanascimento, datahoravenda, xml, documentodestinatario, chaveCfe, totalimpostofederal, totalimpostoestadual, mensagemsefaz, idclienteclube, VALORBASECALC08, VALORBASECALC09, VALORBASECALC10, VALORBASECALC11, idpedidoecommerce, VALORBASECALC12, participapromocaosorteio, idpedidoplataforma) VALUES ('V', '{contador}', '1', '1', '1', '	2022-05-12 14:24:11	 ', '	2022-05-12 14:24:11	', 'S', NULL, 0, 0, 0, '', 1380, 0, 0, 'N', 'N', 'N', 0, 'N', 0, 0, NULL, 0, '{dia}', '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'N', NULL, 'N', 'N', NULL, '2022-05-09 09:30:01', NULL, NULL, '0', 0, 0, 'Emitido com sucesso + conteudo notas.', 0, NULL, NULL, NULL, NULL, 0, NULL, 'S', NULL)"

        cursor.execute(comando)

        cursor.fetchall()  # ler o banco de dados

        contador += 1

def uptadecodvenda():

    contador = 0

    while contador < numero:

        comando = f"UPDATE T_Venda SET cod_venda = %s where cod_venda = {contador} and datafiscal = '{dia}' and vendaEncerrada = 'S'" % (codvenda()[contador])

        cursor.execute(comando)

        cursor.fetchall()  # ler o banco de dados

        contador += 1

def uptadecampos():

    comando = f"UPDATE T_Venda inner join CFe  on T_Venda.cod_venda = CFe.cod_venda SET T_Venda.chaveCfe =  CFe.chaveCfe, T_Venda.datahora = CFe.datahora, T_Venda.datahoraECF = CFe.datahora, T_Venda.nEstab = CFe.nestab, T_Venda.nPDV = CFe.npdv, T_Venda.nECF = CFe.npdv, T_Venda.datahoravenda = CFe.datahora WHERE T_Venda.datafiscal = '{dia}'"

    cursor.execute(comando)

    cursor.fetchall()  # ler o banco de dados

def updateoperador():

    comando = f"UPDATE T_Venda inner join T_PDV SET T_Venda.IDPDV =  T_PDV.ID WHERE T_Venda.datafiscal = '{dia}' AND T_Venda.datahora BETWEEN T_PDV.dataHoraAbertura AND T_PDV.dataHoraFechamento"

    cursor.execute(comando)

    cursor.fetchall()  # ler o banco de dados
if numero <= 0:
    print("Ja existem registros na T_Venda na data informada")

else:
    insert()
    uptadecodvenda()
    uptadecampos()
    updateoperador()

    print('tabela restaurada com sucesso')
    time.sleep(5)
