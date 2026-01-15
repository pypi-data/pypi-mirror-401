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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l1l1lll1l_opy_ import bstack11l1l1ll1ll_opy_
from bstack_utils.constants import *
import json
class bstack11l1111l1l_opy_:
    def __init__(self, bstack11l11111l_opy_, bstack11l1ll1111l_opy_):
        self.bstack11l11111l_opy_ = bstack11l11111l_opy_
        self.bstack11l1ll1111l_opy_ = bstack11l1ll1111l_opy_
        self.bstack11l1ll11111_opy_ = None
    def __call__(self):
        bstack11l1l1lllll_opy_ = {}
        while True:
            self.bstack11l1ll11111_opy_ = bstack11l1l1lllll_opy_.get(
                bstack1l111l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᠱ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l1l1lll11_opy_ = self.bstack11l1ll11111_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l1l1lll11_opy_ > 0:
                sleep(bstack11l1l1lll11_opy_ / 1000)
            params = {
                bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᠲ"): self.bstack11l11111l_opy_,
                bstack1l111l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᠳ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l1l1ll1l1_opy_ = bstack1l111l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᠴ") + bstack11l1l1ll11l_opy_ + bstack1l111l1_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᠵ")
            if self.bstack11l1ll1111l_opy_.lower() == bstack1l111l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᠶ"):
                bstack11l1l1lllll_opy_ = bstack11l1l1ll1ll_opy_.results(bstack11l1l1ll1l1_opy_, params)
            else:
                bstack11l1l1lllll_opy_ = bstack11l1l1ll1ll_opy_.bstack11l1l1llll1_opy_(bstack11l1l1ll1l1_opy_, params)
            if str(bstack11l1l1lllll_opy_.get(bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᠷ"), bstack1l111l1_opy_ (u"ࠬ࠸࠰࠱ࠩᠸ"))) != bstack1l111l1_opy_ (u"࠭࠴࠱࠶ࠪᠹ"):
                break
        return bstack11l1l1lllll_opy_.get(bstack1l111l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᠺ"), bstack11l1l1lllll_opy_)