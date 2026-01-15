# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstack1ll_opy_ = 7
def bstack1l111l1_opy_ (bstack11l_opy_):
    global bstack11ll1ll_opy_
    bstack111l_opy_ = ord (bstack11l_opy_ [-1])
    bstack1l1ll_opy_ = bstack11l_opy_ [:-1]
    bstack11l1ll1_opy_ = bstack111l_opy_ % len (bstack1l1ll_opy_)
    bstack11l1ll_opy_ = bstack1l1ll_opy_ [:bstack11l1ll1_opy_] + bstack1l1ll_opy_ [bstack11l1ll1_opy_:]
    if bstack1lll_opy_:
        bstack11ll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack1l11l11_opy_ + bstack111l_opy_) % bstack1ll_opy_) for bstack1l11l11_opy_, char in enumerate (bstack11l1ll_opy_)])
    else:
        bstack11ll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack1l11l11_opy_ + bstack111l_opy_) % bstack1ll_opy_) for bstack1l11l11_opy_, char in enumerate (bstack11l1ll_opy_)])
    return eval (bstack11ll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1llll1llll1_opy_ import bstack1llll1lllll_opy_
class bstack1ll1l1ll1ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1llll1llll1_opy_: bstack1llll1lllll_opy_
    def __init__(self):
        self.bstack1lll11l1l1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1llll1llll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll11lll1ll_opy_(self):
        return (self.bstack1lll11l1l1l_opy_ != None and self.bin_session_id != None and self.bstack1llll1llll1_opy_ != None)
    def configure(self, bstack1lll11l1l1l_opy_, config, bin_session_id: str, bstack1llll1llll1_opy_: bstack1llll1lllll_opy_):
        self.bstack1lll11l1l1l_opy_ = bstack1lll11l1l1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1llll1llll1_opy_ = bstack1llll1llll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨዼ") + str(self.bin_session_id) + bstack1l111l1_opy_ (u"ࠥࠦዽ"))
    def bstack1l1lll1l111_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l111l1_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨዾ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False