import logging
import locale
import time
from SapGuiLibrary import SapGuiLibrary

from hnt_sap_nf.common.tx_result import TxResult
from hnt_sap_nf.j1b1n_transaction import J1b1nTransaction
from .common.session import sessionable
from dotenv import load_dotenv
logger = logging.getLogger(__name__)

class SapGui(SapGuiLibrary):
    def __init__(self) -> None:
        SapGuiLibrary.__init__(self, screenshots_on_error=True)
        locale.setlocale(locale.LC_ALL, ('pt_BR.UTF-8'))
        load_dotenv()
        pass
    def format_float(self, value):
        return locale.format_string("%.2f", value)

    @sessionable
    def run_j1b1n(self, nf):
        logger.info(f"Enter execute run_j1b1n nf:{nf}")
        result = {
            "j1b1n": None,
            "error": None
        }
        try:
            j1b1n = J1b1nTransaction().execute(self, nf)
            result['j1b1n'] = j1b1n.to_dict()
        except Exception as ex:
            logger.error(str(ex))
            result["error"] = str(ex)
        logger.info(f"Leave execute run_j1b1n result:{', '.join([str(result[obj]) for obj in result])}")
        return result

    @sessionable
    def run_j1b1n_mock(self, nf):
        logger.info(f"Enter execute run_j1b1n_mock nf:{nf}")
        epoch_now = int(time.time())
        result = TxResult(str(epoch_now), 'chamada run_j1b1n_mock')
        logger.info(f"Leave run_j1b1n_mock:{result}")
        return result