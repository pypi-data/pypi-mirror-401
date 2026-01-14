# coding: UTF-8
import sys
bstack111l11l_opy_ = sys.version_info [0] == 2
bstack11l1_opy_ = 2048
bstack1ll1l1_opy_ = 7
def bstack1l11l1l_opy_ (bstack1111lll_opy_):
    global bstack11l1l_opy_
    bstack1l11111_opy_ = ord (bstack1111lll_opy_ [-1])
    bstack1ll111_opy_ = bstack1111lll_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack1l11111_opy_ % len (bstack1ll111_opy_)
    bstack1_opy_ = bstack1ll111_opy_ [:bstack1lllll1l_opy_] + bstack1ll111_opy_ [bstack1lllll1l_opy_:]
    if bstack111l11l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1_opy_ - (bstack111ll1_opy_ + bstack1l11111_opy_) % bstack1ll1l1_opy_) for bstack111ll1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack11l1_opy_ - (bstack111ll1_opy_ + bstack1l11111_opy_) % bstack1ll1l1_opy_) for bstack111ll1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11llll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lllll1l111_opy_ import bstack1lllll11l11_opy_
class bstack1lll1l1lll1_opy_(abc.ABC):
    bin_session_id: str
    bstack1lllll1l111_opy_: bstack1lllll11l11_opy_
    def __init__(self):
        self.bstack1lll1l11ll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lllll1l111_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll1llll1l1_opy_(self):
        return (self.bstack1lll1l11ll1_opy_ != None and self.bin_session_id != None and self.bstack1lllll1l111_opy_ != None)
    def configure(self, bstack1lll1l11ll1_opy_, config, bin_session_id: str, bstack1lllll1l111_opy_: bstack1lllll11l11_opy_):
        self.bstack1lll1l11ll1_opy_ = bstack1lll1l11ll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lllll1l111_opy_ = bstack1lllll1l111_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣዛ") + str(self.bin_session_id) + bstack1l11l1l_opy_ (u"ࠧࠨዜ"))
    def bstack1ll11l1111l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l11l1l_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣዝ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False