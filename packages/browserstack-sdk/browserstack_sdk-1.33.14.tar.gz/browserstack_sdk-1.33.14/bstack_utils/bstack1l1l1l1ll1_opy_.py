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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l1ll1l111_opy_ import bstack11l1ll11lll_opy_
from bstack_utils.constants import *
import json
class bstack1l11111ll_opy_:
    def __init__(self, bstack1llll111_opy_, bstack11l1ll11l1l_opy_):
        self.bstack1llll111_opy_ = bstack1llll111_opy_
        self.bstack11l1ll11l1l_opy_ = bstack11l1ll11l1l_opy_
        self.bstack11l1ll11l11_opy_ = None
    def __call__(self):
        bstack11l1ll1l11l_opy_ = {}
        while True:
            self.bstack11l1ll11l11_opy_ = bstack11l1ll1l11l_opy_.get(
                bstack1l11l1l_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ᠐"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l1ll11ll1_opy_ = self.bstack11l1ll11l11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l1ll11ll1_opy_ > 0:
                sleep(bstack11l1ll11ll1_opy_ / 1000)
            params = {
                bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᠑"): self.bstack1llll111_opy_,
                bstack1l11l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᠒"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l1ll111ll_opy_ = bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᠓") + bstack11l1ll1l1l1_opy_ + bstack1l11l1l_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣ᠔")
            if self.bstack11l1ll11l1l_opy_.lower() == bstack1l11l1l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ᠕"):
                bstack11l1ll1l11l_opy_ = bstack11l1ll11lll_opy_.results(bstack11l1ll111ll_opy_, params)
            else:
                bstack11l1ll1l11l_opy_ = bstack11l1ll11lll_opy_.bstack11l1ll1l1ll_opy_(bstack11l1ll111ll_opy_, params)
            if str(bstack11l1ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᠖"), bstack1l11l1l_opy_ (u"ࠧ࠳࠲࠳ࠫ᠗"))) != bstack1l11l1l_opy_ (u"ࠨ࠶࠳࠸ࠬ᠘"):
                break
        return bstack11l1ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧ᠙"), bstack11l1ll1l11l_opy_)