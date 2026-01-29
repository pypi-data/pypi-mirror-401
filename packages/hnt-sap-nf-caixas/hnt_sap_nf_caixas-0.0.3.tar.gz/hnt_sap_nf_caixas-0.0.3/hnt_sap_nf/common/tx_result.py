from datetime import datetime


class TxResult:
    def __init__(self, sap_docnum, sbar=None) -> None:
        self.sap_docnum = sap_docnum
        self.sbar = sbar
        self.created_at = datetime.now().strftime("%Y%m%d%H%M%S")

    def to_dict(self):
        return {
            'sap_docnum': self.sap_docnum,
            'sbar': self.sbar,
            'created_at': self.created_at,
        }

    def __str__(self):
        return f"TxResult instance with sap_docnum: '{self.sap_docnum}', sbar: '{self.sbar}', created_at:'{self.created_at}'"