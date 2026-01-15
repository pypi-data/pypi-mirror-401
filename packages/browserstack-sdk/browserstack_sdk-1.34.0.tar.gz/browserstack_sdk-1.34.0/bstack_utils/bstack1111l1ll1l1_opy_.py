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
import os
import time
from bstack_utils.bstack11l1l1lll1l_opy_ import bstack11l1l1ll1ll_opy_
from bstack_utils.constants import bstack11l11lll111_opy_
from bstack_utils.helper import get_host_info, bstack111ll1111l1_opy_
class bstack1111ll11ll1_opy_:
    bstack1l111l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡢࡰࡧࡰࡪࡹࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡶࡻ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤⅾ")
    def __init__(self, config, logger):
        bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡪࡩࡤࡶ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡦࡳࡳ࡬ࡩࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡢࡷࡹࡸࡡࡵࡧࡪࡽ࠿ࠦࡳࡵࡴ࠯ࠤࡹ࡫ࡳࡵࠢࡲࡶࡩ࡫ࡲࡪࡰࡪࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࠦ࡮ࡢ࡯ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣⅿ")
        self.config = config
        self.logger = logger
        self.bstack1lll1lll1l1l_opy_ = bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡰ࡭࡫ࡷ࠱ࡹ࡫ࡳࡵࡵࠥↀ")
        self.bstack1lll1lllllll_opy_ = None
        self.bstack1lll1lll11l1_opy_ = 60
        self.bstack1lll1lll11ll_opy_ = 5
        self.bstack1lll1lllll11_opy_ = 0
    def bstack1111l1ll11l_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1l111l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡸࡴࡸࡥࡴࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡴࡴࡲ࡬ࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤↁ")
        self.logger.debug(bstack1l111l1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡌࡲ࡮ࡺࡩࡢࡶ࡬ࡲ࡬ࠦࡳࡱ࡮࡬ࡸࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣↂ").format(orchestration_strategy))
        try:
            bstack1lll1lll1ll1_opy_ = []
            bstack1l111l1_opy_ (u"ࠦࠧࠨࡗࡦࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤ࡫࡫ࡴࡤࡪࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢ࡬ࡷࠥࡹ࡯ࡶࡴࡦࡩࠥ࡯ࡳࠡࡶࡼࡴࡪࠦ࡯ࡧࠢࡤࡶࡷࡧࡹࠡࡣࡱࡨࠥ࡯ࡴࠨࡵࠣࡩࡱ࡫࡭ࡦࡰࡷࡷࠥࡧࡲࡦࠢࡲࡪࠥࡺࡹࡱࡧࠣࡨ࡮ࡩࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡰࠣࡸ࡭ࡧࡴࠡࡥࡤࡷࡪ࠲ࠠࡶࡵࡨࡶࠥ࡮ࡡࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡲࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡵࡲࡹࡷࡩࡥࠡࡹ࡬ࡸ࡭ࠦࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭ࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣࠤࠥↃ")
            source = orchestration_metadata[bstack1l111l1_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫↄ")].get(bstack1l111l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ↅ"), [])
            bstack1lll1lll1111_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1l111l1_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭ↆ")].get(bstack1l111l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩↇ"), False) and not bstack1lll1lll1111_opy_:
                bstack1lll1lll1ll1_opy_ = bstack111ll1111l1_opy_(source) # bstack1lll1llll1ll_opy_-repo is handled bstack1lll1llll111_opy_
            payload = {
                bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣↈ"): [{bstack1l111l1_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ↉"): f} for f in test_files],
                bstack1l111l1_opy_ (u"ࠦࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡹࡸࡡࡵࡧࡪࡽࠧ↊"): orchestration_strategy,
                bstack1l111l1_opy_ (u"ࠧࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡒ࡫ࡴࡢࡦࡤࡸࡦࠨ↋"): orchestration_metadata,
                bstack1l111l1_opy_ (u"ࠨ࡮ࡰࡦࡨࡍࡳࡪࡥࡹࠤ↌"): int(os.environ.get(bstack1l111l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥ↍")) or bstack1l111l1_opy_ (u"ࠣ࠲ࠥ↎")),
                bstack1l111l1_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࡏࡱࡧࡩࡸࠨ↏"): int(os.environ.get(bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ←")) or bstack1l111l1_opy_ (u"ࠦ࠶ࠨ↑")),
                bstack1l111l1_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ→"): self.config.get(bstack1l111l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ↓"), bstack1l111l1_opy_ (u"ࠧࠨ↔")),
                bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ↕"): self.config.get(bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ↖"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ↗"): os.environ.get(bstack1l111l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ↘"), bstack1l111l1_opy_ (u"ࠧࠨ↙")),
                bstack1l111l1_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣ↚"): get_host_info(),
                bstack1l111l1_opy_ (u"ࠢࡱࡴࡇࡩࡹࡧࡩ࡭ࡵࠥ↛"): bstack1lll1lll1ll1_opy_
            }
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣ࡝ࡶࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࡣࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤ↜").format(payload))
            response = bstack11l1l1ll1ll_opy_.bstack1llll11lllll_opy_(self.bstack1lll1lll1l1l_opy_, payload)
            if response:
                self.bstack1lll1lllllll_opy_ = self._1lll1lll1l11_opy_(response)
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤ࡞ࡷࡵࡲࡩࡵࡖࡨࡷࡹࡹ࡝ࠡࡕࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ↝").format(self.bstack1lll1lllllll_opy_))
            else:
                self.logger.error(bstack1l111l1_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠰ࠥ↞"))
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺࠻ࠢࡾࢁࠧ↟").format(e))
    def _1lll1lll1l11_opy_(self, response):
        bstack1l111l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡶࡴࡱ࡯ࡴࠡࡶࡨࡷࡹࡹࠠࡂࡒࡌࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡡ࡯ࡦࠣࡩࡽࡺࡲࡢࡥࡷࡷࠥࡸࡥ࡭ࡧࡹࡥࡳࡺࠠࡧ࡫ࡨࡰࡩࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ↠")
        bstack11llll1l1_opy_ = {}
        bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ↡")] = response.get(bstack1l111l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ↢"), self.bstack1lll1lll11l1_opy_)
        bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡋࡱࡸࡪࡸࡶࡢ࡮ࠥ↣")] = response.get(bstack1l111l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦ↤"), self.bstack1lll1lll11ll_opy_)
        bstack1llll1111111_opy_ = response.get(bstack1l111l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ↥"))
        bstack1lll1llll1l1_opy_ = response.get(bstack1l111l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣ↦"))
        if bstack1llll1111111_opy_:
            bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ↧")] = bstack1llll1111111_opy_.split(bstack11l11lll111_opy_ + bstack1l111l1_opy_ (u"ࠨ࠯ࠣ↨"))[1] if bstack11l11lll111_opy_ + bstack1l111l1_opy_ (u"ࠢ࠰ࠤ↩") in bstack1llll1111111_opy_ else bstack1llll1111111_opy_
        else:
            bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ↪")] = None
        if bstack1lll1llll1l1_opy_:
            bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨ↫")] = bstack1lll1llll1l1_opy_.split(bstack11l11lll111_opy_ + bstack1l111l1_opy_ (u"ࠥ࠳ࠧ↬"))[1] if bstack11l11lll111_opy_ + bstack1l111l1_opy_ (u"ࠦ࠴ࠨ↭") in bstack1lll1llll1l1_opy_ else bstack1lll1llll1l1_opy_
        else:
            bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹ࡛ࡲ࡭ࠤ↮")] = None
        if (
            response.get(bstack1l111l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ↯")) is None or
            response.get(bstack1l111l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤ↰")) is None or
            response.get(bstack1l111l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࡗࡵࡰࠧ↱")) is None or
            response.get(bstack1l111l1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡗࡵࡰࠧ↲")) is None
        ):
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥ࡟ࡵࡸ࡯ࡤࡧࡶࡷࡤࡹࡰ࡭࡫ࡷࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡹࡰࡰࡰࡶࡩࡢࠦࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡰࡸࡰࡱࠦࡶࡢ࡮ࡸࡩ࠭ࡹࠩࠡࡨࡲࡶࠥࡹ࡯࡮ࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡹࠠࡪࡰࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ↳"))
        return bstack11llll1l1_opy_
    def bstack1111l1ll1ll_opy_(self):
        if not self.bstack1lll1lllllll_opy_:
            self.logger.error(bstack1l111l1_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡔ࡯ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠱ࠦ↴"))
            return None
        bstack1lll1lll111l_opy_ = None
        test_files = []
        bstack1lll1llll11l_opy_ = int(time.time() * 1000) # bstack1lll1llllll1_opy_ sec
        bstack1lll1lll1lll_opy_ = int(self.bstack1lll1lllllll_opy_.get(bstack1l111l1_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࡏ࡮ࡵࡧࡵࡺࡦࡲࠢ↵"), self.bstack1lll1lll11ll_opy_))
        bstack1lll1lllll1l_opy_ = int(self.bstack1lll1lllllll_opy_.get(bstack1l111l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢ↶"), self.bstack1lll1lll11l1_opy_)) * 1000
        bstack1lll1llll1l1_opy_ = self.bstack1lll1lllllll_opy_.get(bstack1l111l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦ↷"), None)
        bstack1llll1111111_opy_ = self.bstack1lll1lllllll_opy_.get(bstack1l111l1_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡖࡴ࡯ࠦ↸"), None)
        if bstack1llll1111111_opy_ is None and bstack1lll1llll1l1_opy_ is None:
            return None
        try:
            while bstack1llll1111111_opy_ and (time.time() * 1000 - bstack1lll1llll11l_opy_) < bstack1lll1lllll1l_opy_:
                response = bstack11l1l1ll1ll_opy_.bstack1llll11ll1ll_opy_(bstack1llll1111111_opy_, {})
                if response and response.get(bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ↹")):
                    bstack1lll1lll111l_opy_ = response.get(bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡴࠤ↺"))
                self.bstack1lll1lllll11_opy_ += 1
                if bstack1lll1lll111l_opy_:
                    break
                time.sleep(bstack1lll1lll1lll_opy_)
                self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡌࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡧࡴࡲࡱࠥࡸࡥࡴࡷ࡯ࡸ࡛ࠥࡒࡍࠢࡤࡪࡹ࡫ࡲࠡࡹࡤ࡭ࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡻࡾࠢࡶࡩࡨࡵ࡮ࡥࡵ࠱ࠦ↻").format(bstack1lll1lll1lll_opy_))
            if bstack1lll1llll1l1_opy_ and not bstack1lll1lll111l_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡆࡦࡶࡦ࡬࡮ࡴࡧࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡨࡵࡳࡲࠦࡴࡪ࡯ࡨࡳࡺࡺࠠࡖࡔࡏࠦ↼"))
                response = bstack11l1l1ll1ll_opy_.bstack1llll11ll1ll_opy_(bstack1lll1llll1l1_opy_, {})
                if response and response.get(bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡷࠧ↽")):
                    bstack1lll1lll111l_opy_ = response.get(bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡸࠨ↾"))
            if bstack1lll1lll111l_opy_ and len(bstack1lll1lll111l_opy_) > 0:
                for bstack111l11l1l1_opy_ in bstack1lll1lll111l_opy_:
                    file_path = bstack111l11l1l1_opy_.get(bstack1l111l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ↿"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1lll1lll111l_opy_:
                return None
            self.logger.debug(bstack1l111l1_opy_ (u"ࠤ࡞࡫ࡪࡺࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡊ࡮ࡲࡥࡴ࡟ࠣࡓࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡴࡨࡧࡪ࡯ࡶࡦࡦ࠽ࠤࢀࢃࠢ⇀").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠥ࡟࡬࡫ࡴࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡵࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵ࠽ࠤࢀࢃࠢ⇁").format(e))
            return None
    def bstack1111ll11l1l_opy_(self):
        bstack1l111l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡁࡑࡋࠣࡧࡦࡲ࡬ࡴࠢࡰࡥࡩ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⇂")
        return self.bstack1lll1lllll11_opy_