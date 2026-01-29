import json
from hnt_sap_nf.hnt_sap_gui import SapGui

class TestJ1b1nTransaction:
    def setup_method(self, method):
        with open(f"./devdata/json/{method.__name__}.json", "r", encoding="utf-8") as arquivo_json: nf = json.load(arquivo_json)
        self.nf = nf
        self.saved_record = None
        self.error_record = None

    def test_sap_nf_31251200015861804877559220001443241320827677(self):
        if self.nf is not None:
            result = SapGui().run_j1b1n(self.nf)
            self.saved_record = result.get('j1b1n')
            self.error_record = result.get('error')
        assert self.saved_record is not None
    def test_sap_nf_35251200988809000335550010001651121840350907(self):
        if self.nf is not None:
            result = SapGui().run_j1b1n(self.nf)
            self.saved_record = result.get('j1b1n')
            self.error_record = result.get('error')
        assert self.saved_record is not None
    def test_j1b1n_mock(self):
        if self.nf is not None:
            result = SapGui().run_j1b1n_mock(self.nf)
            assert result.sbar == 'chamada run_j1b1n_mock'
    def teardown_method(self, method):
        if self.saved_record is not None:
            with open(f"./output/json/saved_{method.__name__}.json", "w", encoding="utf-8") as json_file:
                json.dump( self.saved_record, json_file, ensure_ascii=False, indent=4)
        if self.error_record is not None:
            with open(f"./output/json/error_{method.__name__}.json", "w", encoding="utf-8") as json_file:
                json.dump( self.error_record, json_file, ensure_ascii=False, indent=4)

