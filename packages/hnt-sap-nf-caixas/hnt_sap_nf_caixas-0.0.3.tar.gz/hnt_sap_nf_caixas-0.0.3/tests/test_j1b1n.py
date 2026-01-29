import json
from hnt_sap_nf.hnt_sap_gui import SapGui


def test_create():
    with open("./devdata/json/nf_caixas_GHN-68955.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    nf = payload['payloads'][0]['nf_caixas']
    result = SapGui().run_j1b1n(nf)

    assert result['error'] is None

def test_create_chave_acesso():
    with open("./devdata/json/sap_nf_35251296669288000160550010006831461561796697.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    result = SapGui().run_j1b1n(payload)

    with open("./devdata/json/sap_nf_31251200015861804877559220001443241320827677.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251200988809000335550010001651121840350907.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251205258070000168550010004132661080163793.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251205602272000185550020001438521235812151.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251208066591001698550010000171511340852410.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251208365506000106550010001262411065725349.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251208373288000151550010000136701122387540.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251210971350000159550010005726011000773077.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251211981319000161550010000153121072594075.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251221938705000124550140000199981001391927.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251226240336000115550010002870451299328855.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251235639330000106550010000529851001623777.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251237969285000183550020000029381094569980.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251250983733000161550010006907971246388892.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251254549340000103550010001953431072177460.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251255746019000173550010000136521051806942.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251255825811000113550010000188791883017856.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
    with open("./devdata/json/sap_nf_35251267109710000206550010002775761413632824.json", "r", encoding="utf-8") as payload_json: payload = json.load(payload_json)
