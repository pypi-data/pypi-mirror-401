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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11l1llll_opy_ = {}
        bstack111ll1l111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ༬"), bstack1l11l1l_opy_ (u"ࠧࠨ༭"))
        if not bstack111ll1l111_opy_:
            return bstack1l11l1llll_opy_
        try:
            bstack111ll1l11l_opy_ = json.loads(bstack111ll1l111_opy_)
            if bstack1l11l1l_opy_ (u"ࠣࡱࡶࠦ༮") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠤࡲࡷࠧ༯")] = bstack111ll1l11l_opy_[bstack1l11l1l_opy_ (u"ࠥࡳࡸࠨ༰")]
            if bstack1l11l1l_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ༱") in bstack111ll1l11l_opy_ or bstack1l11l1l_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ༲") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ༳")] = bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦ༴"), bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱ༵ࠦ")))
            if bstack1l11l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ༶") in bstack111ll1l11l_opy_ or bstack1l11l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥ༷ࠣ") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ༸")] = bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨ༹"), bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ༺")))
            if bstack1l11l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ༻") in bstack111ll1l11l_opy_ or bstack1l11l1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ༼") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ༽")] = bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ༾"), bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧ༿")))
            if bstack1l11l1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧཀ") in bstack111ll1l11l_opy_ or bstack1l11l1l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥཁ") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦག")] = bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣགྷ"), bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨང")))
            if bstack1l11l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧཅ") in bstack111ll1l11l_opy_ or bstack1l11l1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥཆ") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦཇ")] = bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ཈"), bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨཉ")))
            if bstack1l11l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦཊ") in bstack111ll1l11l_opy_ or bstack1l11l1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦཋ") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧཌ")] = bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢཌྷ"), bstack111ll1l11l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢཎ")))
            if bstack1l11l1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣཏ") in bstack111ll1l11l_opy_:
                bstack1l11l1llll_opy_[bstack1l11l1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤཐ")] = bstack111ll1l11l_opy_[bstack1l11l1l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥད")]
        except Exception as error:
            logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣདྷ") +  str(error))
        return bstack1l11l1llll_opy_