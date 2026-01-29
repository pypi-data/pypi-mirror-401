import logging
from datetime import datetime
from hnt_sap_nf.common.tx_result import TxResult
logger = logging.getLogger(__name__)
from hnt_sap_nf.common.sap_status_bar import sbar_extracted_text
MSG_SAP_NOTA_FISCAL_CRIADA = "^Nota fiscal ([0-9]+) criada$"
IMPOSTOS = [
                'ICM0',
                'ICON',
                'IPSN',
                'IPI0'
            ] 
class J1b1nTransaction:
    def __init__(self) -> None:
        pass

    def execute(self, sapGuiLib, nf):
        logger.info(f"Enter lançar nf:{nf}")
        sapGuiLib.run_transaction('/nJ1B1N')
    
        sapGuiLib.session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-NFTYPE").Text = nf['categoria_nf'] #Planilha: Cat NF | SAP: Ctg.nota fiscal
        sapGuiLib.session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-BUKRS").Text = nf['empresa'] #Planilha: Empresa | SAP: Empresa
        sapGuiLib.session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-BRANCH").Text = nf['local_negocio'] #Planilha: Unidade | SAP: Local de negócios
        sapGuiLib.session.findById("wnd[0]/usr/cmbJ_1BDYDOC-PARVW").Key = nf['funcao_parceiro'] #SAP: NF função parceiro*
        sapGuiLib.session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-PARID").Text = nf['sap_cod_fornecedor'] #Planilha: Código Fornecedor | SAP: ID parceiro
    
        sapGuiLib.send_vkey(0)
        if nf['categoria_nf'] == 'YS':
            sapGuiLib.session.findById("wnd[0]/usr/subNF_NUMBER:SAPLJ1BB2:2002/txtJ_1BDYDOC-NFENUM").Text = nf['nro_nf'] #Planilha: Nº NF | SAP: Nº da NF-e
            sapGuiLib.session.findById("wnd[0]/usr/txtJ_1BDYDOC-SERIES").Text = nf['serie_nf'] # Série NF Planilha: Nº Série | SAP: Nº da NF-e (campo 2)
            sapGuiLib.session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-DOCDAT").Text = nf['data_emissao'] #Planilha: Data emissão | SAP: Data documento
        elif nf['categoria_nf'] == 'YZ':
            data_atual = datetime.now()
            sapGuiLib.session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-DOCDAT").Text = data_atual.strftime("%d.%m.%Y") #Data corrente, ex. 10.12.2025
    
        #------------------------------------------------------------------------------------------------
        #INCLUSÃO DE MATERIAIS
        for i, item in enumerate(nf['itens']):
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/ctxtJ_1BDYLIN-ITMTYP[1,{i}]").Text = item['tipo'] #Planilha: Tipo item NF | SAP: Tipo de item NF
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/ctxtJ_1BDYLIN-MATNR[3,{i}]").Text = item['cod_material_sap'] #Planilha: Código Material | SAP: Material
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/ctxtJ_1BDYLIN-WERKS[2,{i}]").Text = item['centro'] #Planilha: CD | SAP: Centro
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/txtJ_1BDYLIN-MENGE[4,{i}]").Text = item['quantidade'] #Planilha: Quantidade | SAP: Quantidade
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/ctxtJ_1BDYLIN-MEINS[5,{i}]").Text = item['unidade_medida'] #Planilha: Un Med | SAP: Unidade de medida
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/txtJ_1BDYLIN-NETPR[6,{i}]").Text = sapGuiLib.format_float(float(item['preco'])) #Planilha: Valor UN | SAP: Preço
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/ctxtJ_1BDYLIN-CFOP[9,{i}]").Text = item['cfop'] #Planilha: CFOP Entrada | SAP: CFOP
            sapGuiLib.session.findById(f"wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/tblSAPLJ1BB2ITEM_CONTROL/ctxtJ_1BDYLIN-TAXLW1[10,{i}]").Text = item['dir_fiscal'] #Planilha: Dir Fiscal | SAP: Dir.fisc.: ICMS
            sapGuiLib.send_vkey(0)
            sapGuiLib.send_vkey(0)
        
        sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/btn%#AUTOTEXT004").press() #Botão "Selecionar tudo"
        sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB1/ssubHEADER_TAB:SAPLJ1BB2:2100/btn%#AUTOTEXT001").press() #Botão "DetalhItem"
        sapGuiLib.session.findById("wnd[0]/usr/tabsITEM_TAB/tabpTAX").Select() #Seleciona aba Impsotos
        for i, item in enumerate(nf['itens']):
            for i, imposto in enumerate(IMPOSTOS):
                sapGuiLib.session.findById(f"wnd[0]/usr/tabsITEM_TAB/tabpTAX/ssubITEM_TABS:SAPLJ1BB2:3200/tblSAPLJ1BB2TAX_CONTROL/ctxtJ_1BDYSTX-TAXTYP[0,{i}]").Text = imposto    
                sapGuiLib.session.findById(f"wnd[0]/usr/tabsITEM_TAB/tabpTAX/ssubITEM_TABS:SAPLJ1BB2:3200/tblSAPLJ1BB2TAX_CONTROL/txtJ_1BDYSTX-OTHBAS[7,{i}]").Text = sapGuiLib.format_float(float(item['valor_produto']))
            
            sapGuiLib.session.findById("wnd[0]/usr/tabsITEM_TAB/tabpTAX/ssubITEM_TABS:SAPLJ1BB2:3200/btnPB_NEXT").press()
        
        sapGuiLib.send_vkey(0)
        sapGuiLib.session.findById("wnd[0]/tbar[0]/btn[3]").press()

        if nf['categoria_nf'] == 'YS':
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8").Select() #Seleciona aba DadosNF-e
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subRANDOM_NUMBER:SAPLJ1BB2:2801/ctxtJ_1BNFE_DOCNUM9_DIVIDED-TPEMIS").Text = nf['dados_nfe']['tipo_emissao'] #Planilha: Tipo de emissão | SAP: Tp.emissão
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subRANDOM_NUMBER:SAPLJ1BB2:2801/txtJ_1BNFE_DOCNUM9_DIVIDED-DOCNUM8").Text = nf['dados_nfe']['nro_aleatorio'] #Planilha: Nº aleatorio | SAP: Nº aleatório
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subRANDOM_NUMBER:SAPLJ1BB2:2801/txtJ_1BNFE_ACTIVE-CDV").Text = nf['dados_nfe']['digito_verificador'] #Planilha: Dig verificador | SAP: Díg.verif.
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subTIMESTAMP:SAPLJ1BB2:2803/subAUTHCODE_AREA:SAPLJ1BB2:2805/txtJ_1BDYDOC-AUTHCOD").Text = nf['dados_nfe']['nro_log'] #Planilha: Numero Doc | SAP: Nº do log
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subTIMESTAMP:SAPLJ1BB2:2803/ctxtJ_1BDYDOC-AUTHDATE").Text = nf['dados_nfe']['data_emissao'] #Planilha: Data emissão | SAP: Hora procmto.
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subTIMESTAMP:SAPLJ1BB2:2803/ctxtJ_1BDYDOC-AUTHTIME").Text = nf['dados_nfe']['hora_emissao'] # Planilha: Hora de emissão | SAP: Hora procmto.
        elif nf['categoria_nf'] == 'YZ':
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB4").Select() #Seleciona aba Mensagens
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB4/ssubHEADER_TAB:SAPLJ1BB2:2400/tblSAPLJ1BB2MESSAGE_CONTROL/txtJ_1BDYFTX-MESSAGE[0,2]").Text = f"NOTA DE PRODUTOR {nf['nro_nf']}-{nf['serie_nf']}"
            sapGuiLib.send_vkey(0)
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB5").Select() #Seleciona aba Transporte
            sapGuiLib.session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB5/ssubHEADER_TAB:SAPLJ1BB2:2500/ctxtJ_1BDYDOC-MODFRETE").Text = nf['dados_nfe']['modalid_fret'] #SAP: Modalid.fret

        sapGuiLib.send_vkey(0)
        sapGuiLib.session.findById("wnd[0]/tbar[0]/btn[11]").press()  #Salvar
        sbar = sapGuiLib.session.findById("wnd[0]/sbar").Text
        sap_docnum = sbar_extracted_text(MSG_SAP_NOTA_FISCAL_CRIADA, sbar)
        result = TxResult(sap_docnum, sbar)
        logger.info(f"Leave lançar nf:{result}")
        return result