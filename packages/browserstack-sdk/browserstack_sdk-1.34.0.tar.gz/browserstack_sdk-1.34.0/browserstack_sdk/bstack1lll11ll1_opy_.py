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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1l1lllll_opy_ = {}
        bstack111ll1111l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ༿"), bstack1l111l1_opy_ (u"ࠬ࠭ཀ"))
        if not bstack111ll1111l_opy_:
            return bstack1l1l1lllll_opy_
        try:
            bstack111ll11111_opy_ = json.loads(bstack111ll1111l_opy_)
            if bstack1l111l1_opy_ (u"ࠨ࡯ࡴࠤཁ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠢࡰࡵࠥག")] = bstack111ll11111_opy_[bstack1l111l1_opy_ (u"ࠣࡱࡶࠦགྷ")]
            if bstack1l111l1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨང") in bstack111ll11111_opy_ or bstack1l111l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨཅ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢཆ")] = bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤཇ"), bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ཈")))
            if bstack1l111l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣཉ") in bstack111ll11111_opy_ or bstack1l111l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨཊ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢཋ")] = bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦཌ"), bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤཌྷ")))
            if bstack1l111l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢཎ") in bstack111ll11111_opy_ or bstack1l111l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢཏ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣཐ")] = bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥད"), bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥདྷ")))
            if bstack1l111l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥན") in bstack111ll11111_opy_ or bstack1l111l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣཔ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤཕ")] = bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨབ"), bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦབྷ")))
            if bstack1l111l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥམ") in bstack111ll11111_opy_ or bstack1l111l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣཙ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤཚ")] = bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨཛ"), bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦཛྷ")))
            if bstack1l111l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤཝ") in bstack111ll11111_opy_ or bstack1l111l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤཞ") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥཟ")] = bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧའ"), bstack111ll11111_opy_.get(bstack1l111l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧཡ")))
            if bstack1l111l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨར") in bstack111ll11111_opy_:
                bstack1l1l1lllll_opy_[bstack1l111l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢལ")] = bstack111ll11111_opy_[bstack1l111l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣཤ")]
        except Exception as error:
            logger.error(bstack1l111l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨཥ") +  str(error))
        return bstack1l1l1lllll_opy_