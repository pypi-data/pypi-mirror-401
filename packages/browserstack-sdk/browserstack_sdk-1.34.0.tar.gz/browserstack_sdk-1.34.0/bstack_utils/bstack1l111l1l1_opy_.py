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
import tempfile
import math
from bstack_utils import bstack1ll1lll11_opy_
from bstack_utils.constants import bstack1111l1l1l_opy_, bstack11l11l1ll11_opy_
from bstack_utils.helper import bstack111ll1111l1_opy_, get_host_info
from bstack_utils.bstack11l1l1lll1l_opy_ import bstack11l1l1ll1ll_opy_
import json
import re
import sys
bstack11111ll1l11_opy_ = bstack1l111l1_opy_ (u"ࠦࡷ࡫ࡴࡳࡻࡗࡩࡸࡺࡳࡐࡰࡉࡥ࡮ࡲࡵࡳࡧࠥἾ")
bstack11111lll11l_opy_ = bstack1l111l1_opy_ (u"ࠧࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠦἿ")
bstack1111l1l1ll1_opy_ = bstack1l111l1_opy_ (u"ࠨࡲࡶࡰࡓࡶࡪࡼࡩࡰࡷࡶࡰࡾࡌࡡࡪ࡮ࡨࡨࡋ࡯ࡲࡴࡶࠥὀ")
bstack11111ll1l1l_opy_ = bstack1l111l1_opy_ (u"ࠢࡳࡧࡵࡹࡳࡖࡲࡦࡸ࡬ࡳࡺࡹ࡬ࡺࡈࡤ࡭ࡱ࡫ࡤࠣὁ")
bstack1111l111l1l_opy_ = bstack1l111l1_opy_ (u"ࠣࡵ࡮࡭ࡵࡌ࡬ࡢ࡭ࡼࡥࡳࡪࡆࡢ࡫࡯ࡩࡩࠨὂ")
bstack11111llll1l_opy_ = bstack1l111l1_opy_ (u"ࠤࡵࡹࡳ࡙࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࠨὃ")
bstack11111llllll_opy_ = {
    bstack11111ll1l11_opy_,
    bstack11111lll11l_opy_,
    bstack1111l1l1ll1_opy_,
    bstack11111ll1l1l_opy_,
    bstack1111l111l1l_opy_,
    bstack11111llll1l_opy_
}
bstack11111l11l1l_opy_ = {bstack1l111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪὄ")}
logger = bstack1ll1lll11_opy_.get_logger(__name__, bstack1111l1l1l_opy_)
class bstack1111l1l111l_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack1111l11l111_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1llll111l_opy_:
    _1ll11l1llll_opy_ = None
    def __init__(self, config):
        self.bstack1111l11ll1l_opy_ = False
        self.bstack1111l11l1l1_opy_ = False
        self.bstack1111l11lll1_opy_ = False
        self.bstack11111l1l1ll_opy_ = False
        self.bstack1111l1l1l1l_opy_ = None
        self.bstack1111l11llll_opy_ = bstack1111l1l111l_opy_()
        self.bstack1111l1111l1_opy_ = None
        opts = config.get(bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨὅ"), {})
        self.bstack11111l11lll_opy_ = config.get(bstack1l111l1_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡅࡏࡘࠪ὆"), bstack1l111l1_opy_ (u"ࠨࠢ὇"))
        self.bstack11111l1lll1_opy_ = config.get(bstack1l111l1_opy_ (u"ࠧࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࡅࡏࡍࠬὈ"), bstack1l111l1_opy_ (u"ࠣࠤὉ"))
        bstack11111l11111_opy_ = opts.get(bstack11111llll1l_opy_, {})
        bstack11111l1l111_opy_ = None
        if bstack1l111l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩὊ") in bstack11111l11111_opy_:
            bstack1111l1l11ll_opy_ = bstack11111l11111_opy_[bstack1l111l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪὋ")]
            if bstack1111l1l11ll_opy_ is None or (isinstance(bstack1111l1l11ll_opy_, str) and bstack1111l1l11ll_opy_.strip() == bstack1l111l1_opy_ (u"ࠫࠬὌ")) or (isinstance(bstack1111l1l11ll_opy_, list) and len(bstack1111l1l11ll_opy_) == 0):
                bstack11111l1l111_opy_ = []
            elif isinstance(bstack1111l1l11ll_opy_, list):
                bstack11111l1l111_opy_ = bstack1111l1l11ll_opy_
            elif isinstance(bstack1111l1l11ll_opy_, str) and bstack1111l1l11ll_opy_.strip():
                bstack11111l1l111_opy_ = bstack1111l1l11ll_opy_
            else:
                logger.warning(bstack1l111l1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡶࡢ࡮ࡸࡩࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡩ࡯ࡩࠣࡸࡴࠦࡥ࡮ࡲࡷࡽࠥࡲࡩࡴࡶ࠱ࠦὍ").format(bstack1111l1l11ll_opy_))
                bstack11111l1l111_opy_ = []
        self.__1111l11111l_opy_(
            bstack11111l11111_opy_.get(bstack1l111l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧ὎"), False),
            bstack11111l11111_opy_.get(bstack1l111l1_opy_ (u"ࠧ࡮ࡱࡧࡩࠬ὏"), bstack1l111l1_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨὐ")),
            bstack11111l1l111_opy_
        )
        self.__11111l1l11l_opy_(opts.get(bstack1111l1l1ll1_opy_, False))
        self.__11111l111l1_opy_(opts.get(bstack11111ll1l1l_opy_, False))
        self.__11111l1llll_opy_(opts.get(bstack1111l111l1l_opy_, False))
    @classmethod
    def bstack1llll1ll11_opy_(cls, config=None):
        if cls._1ll11l1llll_opy_ is None and config is not None:
            cls._1ll11l1llll_opy_ = bstack1llll111l_opy_(config)
        return cls._1ll11l1llll_opy_
    @staticmethod
    def bstack1ll111l1ll_opy_(config: dict) -> bool:
        bstack1111l111l11_opy_ = config.get(bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭ὑ"), {}).get(bstack11111ll1l11_opy_, {})
        return bstack1111l111l11_opy_.get(bstack1l111l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫὒ"), False)
    @staticmethod
    def bstack1lll1111_opy_(config: dict) -> int:
        bstack1111l111l11_opy_ = config.get(bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨὓ"), {}).get(bstack11111ll1l11_opy_, {})
        retries = 0
        if bstack1llll111l_opy_.bstack1ll111l1ll_opy_(config):
            retries = bstack1111l111l11_opy_.get(bstack1l111l1_opy_ (u"ࠬࡳࡡࡹࡔࡨࡸࡷ࡯ࡥࡴࠩὔ"), 1)
        return retries
    @staticmethod
    def bstack1l11l11l1_opy_(config: dict) -> dict:
        bstack1111l111lll_opy_ = config.get(bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪὕ"), {})
        return {
            key: value for key, value in bstack1111l111lll_opy_.items() if key in bstack11111llllll_opy_
        }
    @staticmethod
    def bstack11111llll11_opy_():
        bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦὖ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤὗ").format(os.getenv(bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ὘")))))
    @staticmethod
    def bstack11111lll111_opy_(test_name: str):
        bstack1l111l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡪࡨࡧࡰࠦࡩࡧࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢὙ")
        bstack11111l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥ὚").format(os.getenv(bstack1l111l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥὛ"))))
        with open(bstack11111l111ll_opy_, bstack1l111l1_opy_ (u"࠭ࡡࠨ὜")) as file:
            file.write(bstack1l111l1_opy_ (u"ࠢࡼࡿ࡟ࡲࠧὝ").format(test_name))
    @staticmethod
    def bstack1111l1l1lll_opy_(framework: str) -> bool:
       return framework.lower() in bstack11111l11l1l_opy_
    @staticmethod
    def bstack11l111ll111_opy_(config: dict) -> bool:
        bstack11111l1ll1l_opy_ = config.get(bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬ὞"), {}).get(bstack11111lll11l_opy_, {})
        return bstack11111l1ll1l_opy_.get(bstack1l111l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪὟ"), False)
    @staticmethod
    def bstack11l11l11l1l_opy_(config: dict, bstack11l111l1ll1_opy_: int = 0) -> int:
        bstack1l111l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡩࡡ࡯ࠢࡥࡩࠥࡧ࡮ࠡࡣࡥࡷࡴࡲࡵࡵࡧࠣࡲࡺࡳࡢࡦࡴࠣࡳࡷࠦࡡࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࡵࡣ࡯ࡣࡹ࡫ࡳࡵࡵࠣࠬ࡮ࡴࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࠪࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡲࡨࡶࡨ࡫࡮ࡵࡣࡪࡩ࠲ࡨࡡࡴࡧࡧࠤࡹ࡮ࡲࡦࡵ࡫ࡳࡱࡪࡳࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣὠ")
        bstack11111l1ll1l_opy_ = config.get(bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨὡ"), {}).get(bstack1l111l1_opy_ (u"ࠬࡧࡢࡰࡴࡷࡆࡺ࡯࡬ࡥࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫὢ"), {})
        bstack11111ll111l_opy_ = 0
        bstack1111l11l1ll_opy_ = 0
        if bstack1llll111l_opy_.bstack11l111ll111_opy_(config):
            bstack1111l11l1ll_opy_ = bstack11111l1ll1l_opy_.get(bstack1l111l1_opy_ (u"࠭࡭ࡢࡺࡉࡥ࡮ࡲࡵࡳࡧࡶࠫὣ"), 5)
            if isinstance(bstack1111l11l1ll_opy_, str) and bstack1111l11l1ll_opy_.endswith(bstack1l111l1_opy_ (u"ࠧࠦࠩὤ")):
                try:
                    percentage = int(bstack1111l11l1ll_opy_.strip(bstack1l111l1_opy_ (u"ࠨࠧࠪὥ")))
                    if bstack11l111l1ll1_opy_ > 0:
                        bstack11111ll111l_opy_ = math.ceil((percentage * bstack11l111l1ll1_opy_) / 100)
                    else:
                        raise ValueError(bstack1l111l1_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡱࡧࡵࡧࡪࡴࡴࡢࡩࡨ࠱ࡧࡧࡳࡦࡦࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࡹ࠮ࠣὦ"))
                except ValueError as e:
                    raise ValueError(bstack1l111l1_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡧࡱࡸࡦ࡭ࡥࠡࡸࡤࡰࡺ࡫ࠠࡧࡱࡵࠤࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴ࠼ࠣࡿࢂࠨὧ").format(bstack1111l11l1ll_opy_)) from e
            else:
                bstack11111ll111l_opy_ = int(bstack1111l11l1ll_opy_)
        logger.info(bstack1l111l1_opy_ (u"ࠦࡒࡧࡸࠡࡨࡤ࡭ࡱࡻࡲࡦࡵࠣࡸ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡳࡦࡶࠣࡸࡴࡀࠠࡼࡿࠣࠬ࡫ࡸ࡯࡮ࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂ࠯ࠢὨ").format(bstack11111ll111l_opy_, bstack1111l11l1ll_opy_))
        return bstack11111ll111l_opy_
    def bstack1111l1l11l1_opy_(self):
        return self.bstack11111l1l1ll_opy_
    def bstack11111ll1111_opy_(self):
        return self.bstack1111l1l1l1l_opy_
    def bstack11111ll1lll_opy_(self):
        return self.bstack1111l1111l1_opy_
    def __1111l11111l_opy_(self, enabled, mode, source=None):
        try:
            self.bstack11111l1l1ll_opy_ = bool(enabled)
            if mode not in [bstack1l111l1_opy_ (u"ࠬࡸࡥ࡭ࡧࡹࡥࡳࡺࡆࡪࡴࡶࡸࠬὩ"), bstack1l111l1_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡐࡰ࡯ࡽࠬὪ")]:
                logger.warning(bstack1l111l1_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡱࡴࡪࡥࠡࠩࡾࢁࠬࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡇࡩ࡫ࡧࡵ࡭ࡶ࡬ࡲ࡬ࠦࡴࡰࠢࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪ࠲ࠧὫ").format(mode))
                mode = bstack1l111l1_opy_ (u"ࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨὬ")
            self.bstack1111l1l1l1l_opy_ = mode
            self.bstack1111l1111l1_opy_ = []
            if source is None:
                self.bstack1111l1111l1_opy_ = None
            elif isinstance(source, list):
                self.bstack1111l1111l1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1l111l1_opy_ (u"ࠩ࠱࡮ࡸࡵ࡮ࠨὭ")):
                self.bstack1111l1111l1_opy_ = self._11111l1l1l1_opy_(source)
            self.__1111l111ll1_opy_()
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡲࡧࡲࡵࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࠳ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠻ࠢࡾࢁ࠱ࠦ࡭ࡰࡦࡨ࠾ࠥࢁࡽ࠭ࠢࡶࡳࡺࡸࡣࡦ࠼ࠣࡿࢂ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥὮ").format(enabled, mode, source, e))
    def bstack111111lllll_opy_(self):
        return self.bstack1111l11ll1l_opy_
    def __11111l1l11l_opy_(self, value):
        self.bstack1111l11ll1l_opy_ = bool(value)
        self.__1111l111ll1_opy_()
    def bstack11111lllll1_opy_(self):
        return self.bstack1111l11l1l1_opy_
    def __11111l111l1_opy_(self, value):
        self.bstack1111l11l1l1_opy_ = bool(value)
        self.__1111l111ll1_opy_()
    def bstack1111l1111ll_opy_(self):
        return self.bstack1111l11lll1_opy_
    def __11111l1llll_opy_(self, value):
        self.bstack1111l11lll1_opy_ = bool(value)
        self.__1111l111ll1_opy_()
    def __1111l111ll1_opy_(self):
        if self.bstack11111l1l1ll_opy_:
            self.bstack1111l11ll1l_opy_ = False
            self.bstack1111l11l1l1_opy_ = False
            self.bstack1111l11lll1_opy_ = False
            self.bstack1111l11llll_opy_.enable(bstack11111llll1l_opy_)
        elif self.bstack1111l11ll1l_opy_:
            self.bstack1111l11l1l1_opy_ = False
            self.bstack1111l11lll1_opy_ = False
            self.bstack11111l1l1ll_opy_ = False
            self.bstack1111l11llll_opy_.enable(bstack1111l1l1ll1_opy_)
        elif self.bstack1111l11l1l1_opy_:
            self.bstack1111l11ll1l_opy_ = False
            self.bstack1111l11lll1_opy_ = False
            self.bstack11111l1l1ll_opy_ = False
            self.bstack1111l11llll_opy_.enable(bstack11111ll1l1l_opy_)
        elif self.bstack1111l11lll1_opy_:
            self.bstack1111l11ll1l_opy_ = False
            self.bstack1111l11l1l1_opy_ = False
            self.bstack11111l1l1ll_opy_ = False
            self.bstack1111l11llll_opy_.enable(bstack1111l111l1l_opy_)
        else:
            self.bstack1111l11llll_opy_.disable()
    def bstack1l1l1111l1_opy_(self):
        return self.bstack1111l11llll_opy_.bstack1111l11l111_opy_()
    def bstack1lll11l11_opy_(self):
        if self.bstack1111l11llll_opy_.bstack1111l11l111_opy_():
            return self.bstack1111l11llll_opy_.get_name()
        return None
    def _11111l1l1l1_opy_(self, bstack1111l1l1l11_opy_):
        bstack1l111l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡹ࡯ࡶࡴࡦࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠣࡥࡳࡪࠠࡧࡱࡵࡱࡦࡺࠠࡪࡶࠣࡪࡴࡸࠠࡴ࡯ࡤࡶࡹࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࡹࡷࡩࡥࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠤ࠭ࡹࡴࡳࠫ࠽ࠤࡕࡧࡴࡩࠢࡷࡳࠥࡺࡨࡦࠢࡍࡗࡔࡔࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡵࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦὯ")
        if not os.path.isfile(bstack1111l1l1l11_opy_):
            logger.error(bstack1l111l1_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࠫࢀࢃࠧࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥὰ").format(bstack1111l1l1l11_opy_))
            return []
        data = None
        try:
            with open(bstack1111l1l1l11_opy_, bstack1l111l1_opy_ (u"ࠨࡲࠣά")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1l111l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡋࡕࡒࡒࠥ࡬ࡲࡰ࡯ࠣࡷࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥὲ").format(bstack1111l1l1l11_opy_, e))
            return []
        _1111l111111_opy_ = None
        _11111l1ll11_opy_ = None
        def _11111l11l11_opy_():
            bstack11111ll1ll1_opy_ = {}
            bstack11111l1111l_opy_ = {}
            try:
                if self.bstack11111l11lll_opy_.startswith(bstack1l111l1_opy_ (u"ࠨࡽࠪέ")) and self.bstack11111l11lll_opy_.endswith(bstack1l111l1_opy_ (u"ࠩࢀࠫὴ")):
                    bstack11111ll1ll1_opy_ = json.loads(self.bstack11111l11lll_opy_)
                else:
                    bstack11111ll1ll1_opy_ = dict(item.split(bstack1l111l1_opy_ (u"ࠪ࠾ࠬή")) for item in self.bstack11111l11lll_opy_.split(bstack1l111l1_opy_ (u"ࠫ࠱࠭ὶ")) if bstack1l111l1_opy_ (u"ࠬࡀࠧί") in item) if self.bstack11111l11lll_opy_ else {}
                if self.bstack11111l1lll1_opy_.startswith(bstack1l111l1_opy_ (u"࠭ࡻࠨὸ")) and self.bstack11111l1lll1_opy_.endswith(bstack1l111l1_opy_ (u"ࠧࡾࠩό")):
                    bstack11111l1111l_opy_ = json.loads(self.bstack11111l1lll1_opy_)
                else:
                    bstack11111l1111l_opy_ = dict(item.split(bstack1l111l1_opy_ (u"ࠨ࠼ࠪὺ")) for item in self.bstack11111l1lll1_opy_.split(bstack1l111l1_opy_ (u"ࠩ࠯ࠫύ")) if bstack1l111l1_opy_ (u"ࠪ࠾ࠬὼ") in item) if self.bstack11111l1lll1_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1l111l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤ࡫࡫ࡡࡵࡷࡵࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹ࠺ࠡࡽࢀࠦώ").format(e))
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࠽ࠤࢀࢃࠬࠡࡅࡏࡍ࠿ࠦࡻࡾࠤ὾").format(bstack11111ll1ll1_opy_, bstack11111l1111l_opy_))
            return bstack11111ll1ll1_opy_, bstack11111l1111l_opy_
        if _1111l111111_opy_ is None or _11111l1ll11_opy_ is None:
            _1111l111111_opy_, _11111l1ll11_opy_ = _11111l11l11_opy_()
        def bstack1111l11ll11_opy_(name, bstack11111ll11l1_opy_):
            if name in _11111l1ll11_opy_:
                return _11111l1ll11_opy_[name]
            if name in _1111l111111_opy_:
                return _1111l111111_opy_[name]
            if bstack11111ll11l1_opy_.get(bstack1l111l1_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭὿")):
                return bstack11111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧᾀ")]
            return None
        if isinstance(data, dict):
            bstack11111lll1l1_opy_ = []
            bstack11111ll11ll_opy_ = re.compile(bstack1l111l1_opy_ (u"ࡳࠩࡡ࡟ࡆ࠳࡚࠱࠯࠼ࡣࡢ࠱ࠤࠨᾁ"))
            for name, bstack11111ll11l1_opy_ in data.items():
                if not isinstance(bstack11111ll11l1_opy_, dict):
                    continue
                url = bstack11111ll11l1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡸࡶࡱ࠭ᾂ"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1l111l1_opy_ (u"ࠪࠫᾃ")):
                    logger.warning(bstack1l111l1_opy_ (u"ࠦࡗ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡࡗࡕࡐࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡳࡰࡷࡵࡧࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣᾄ").format(name, bstack11111ll11l1_opy_))
                    continue
                if not bstack11111ll11ll_opy_.match(name):
                    logger.warning(bstack1l111l1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࡪࡴࡸ࡭ࡢࡶࠣࡪࡴࡸࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤᾅ").format(name, bstack11111ll11l1_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l111l1_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠣࠫࢀࢃࠧࠡ࡯ࡸࡷࡹࠦࡨࡢࡸࡨࠤࡦࠦ࡬ࡦࡰࡪࡸ࡭ࠦࡢࡦࡶࡺࡩࡪࡴࠠ࠲ࠢࡤࡲࡩࠦ࠳࠱ࠢࡦ࡬ࡦࡸࡡࡤࡶࡨࡶࡸ࠴ࠢᾆ").format(name))
                    continue
                bstack11111ll11l1_opy_ = bstack11111ll11l1_opy_.copy()
                bstack11111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᾇ")] = name
                bstack11111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨᾈ")] = bstack1111l11ll11_opy_(name, bstack11111ll11l1_opy_)
                if not bstack11111ll11l1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࡅࡶࡦࡴࡣࡩࠩᾉ")) or bstack11111ll11l1_opy_.get(bstack1l111l1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࠪᾊ")) == bstack1l111l1_opy_ (u"ࠫࠬᾋ"):
                    logger.warning(bstack1l111l1_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࠦࡢࡳࡣࡱࡧ࡭ࠦ࡮ࡰࡶࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡩࡩࠦࡦࡰࡴࠣࡷࡴࡻࡲࡤࡧࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧᾌ").format(name, bstack11111ll11l1_opy_))
                    continue
                if bstack11111ll11l1_opy_.get(bstack1l111l1_opy_ (u"࠭ࡢࡢࡵࡨࡆࡷࡧ࡮ࡤࡪࠪᾍ")) and bstack11111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠧࡣࡣࡶࡩࡇࡸࡡ࡯ࡥ࡫ࠫᾎ")] == bstack11111ll11l1_opy_[bstack1l111l1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨᾏ")]:
                    logger.warning(bstack1l111l1_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡥࡳࡪࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡶ࡫ࡩࠥࡹࡡ࡮ࡧࠣࡪࡴࡸࠠࡴࡱࡸࡶࡨ࡫ࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤᾐ").format(name, bstack11111ll11l1_opy_))
                    continue
                bstack11111lll1l1_opy_.append(bstack11111ll11l1_opy_)
            return bstack11111lll1l1_opy_
        return data
    def bstack1111ll111ll_opy_(self):
        data = {
            bstack1l111l1_opy_ (u"ࠪࡶࡺࡴ࡟ࡴ࡯ࡤࡶࡹࡥࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠩᾑ"): {
                bstack1l111l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬᾒ"): self.bstack1111l1l11l1_opy_(),
                bstack1l111l1_opy_ (u"ࠬࡳ࡯ࡥࡧࠪᾓ"): self.bstack11111ll1111_opy_(),
                bstack1l111l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᾔ"): self.bstack11111ll1lll_opy_()
            }
        }
        return data
    def bstack1111l1l1111_opy_(self, config):
        bstack11111lll1ll_opy_ = {}
        bstack11111lll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭ᾕ")] = {
            bstack1l111l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᾖ"): self.bstack1111l1l11l1_opy_(),
            bstack1l111l1_opy_ (u"ࠩࡰࡳࡩ࡫ࠧᾗ"): self.bstack11111ll1111_opy_()
        }
        bstack11111lll1ll_opy_[bstack1l111l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩ࠭ᾘ")] = {
            bstack1l111l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬᾙ"): self.bstack11111lllll1_opy_()
        }
        bstack11111lll1ll_opy_[bstack1l111l1_opy_ (u"ࠬࡸࡵ࡯ࡡࡳࡶࡪࡼࡩࡰࡷࡶࡰࡾࡥࡦࡢ࡫࡯ࡩࡩࡥࡦࡪࡴࡶࡸࠬᾚ")] = {
            bstack1l111l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᾛ"): self.bstack111111lllll_opy_()
        }
        bstack11111lll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡤ࡬ࡡࡪ࡮࡬ࡲ࡬ࡥࡡ࡯ࡦࡢࡪࡱࡧ࡫ࡺࠩᾜ")] = {
            bstack1l111l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᾝ"): self.bstack1111l1111ll_opy_()
        }
        if self.bstack1ll111l1ll_opy_(config):
            bstack11111lll1ll_opy_[bstack1l111l1_opy_ (u"ࠩࡵࡩࡹࡸࡹࡠࡶࡨࡷࡹࡹ࡟ࡰࡰࡢࡪࡦ࡯࡬ࡶࡴࡨࠫᾞ")] = {
                bstack1l111l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫᾟ"): True,
                bstack1l111l1_opy_ (u"ࠫࡲࡧࡸࡠࡴࡨࡸࡷ࡯ࡥࡴࠩᾠ"): self.bstack1lll1111_opy_(config)
            }
        if self.bstack11l111ll111_opy_(config):
            bstack11111lll1ll_opy_[bstack1l111l1_opy_ (u"ࠬࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡳࡳࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠧᾡ")] = {
                bstack1l111l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᾢ"): True,
                bstack1l111l1_opy_ (u"ࠧ࡮ࡣࡻࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡸ࠭ᾣ"): self.bstack11l11l11l1l_opy_(config)
            }
        return bstack11111lll1ll_opy_
    def bstack1lll1lllll_opy_(self, config):
        bstack1l111l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࡹࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤࠤࡧࡿࠠ࡮ࡣ࡮࡭ࡳ࡭ࠠࡢࠢࡦࡥࡱࡲࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡨࡵࡪ࡮ࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᾤ")
        if not (config.get(bstack1l111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᾥ"), None) in bstack11l11l1ll11_opy_ and self.bstack1111l1l11l1_opy_()):
            return None
        bstack1111l11l11l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᾦ"), None)
        logger.debug(bstack1l111l1_opy_ (u"ࠦࡠࡩ࡯࡭࡮ࡨࡧࡹࡈࡵࡪ࡮ࡧࡈࡦࡺࡡ࡞ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡕࡖࡋࡇ࠾ࠥࢁࡽࠣᾧ").format(bstack1111l11l11l_opy_))
        try:
            bstack11l1ll111ll_opy_ = bstack1l111l1_opy_ (u"ࠧࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠥᾨ").format(bstack1111l11l11l_opy_)
            payload = {
                bstack1l111l1_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦᾩ"): config.get(bstack1l111l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᾪ"), bstack1l111l1_opy_ (u"ࠨࠩᾫ")),
                bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧᾬ"): config.get(bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᾭ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤᾮ"): os.environ.get(bstack1l111l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦᾯ"), bstack1l111l1_opy_ (u"ࠨࠢᾰ")),
                bstack1l111l1_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥᾱ"): int(os.environ.get(bstack1l111l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦᾲ")) or bstack1l111l1_opy_ (u"ࠤ࠳ࠦᾳ")),
                bstack1l111l1_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢᾴ"): int(os.environ.get(bstack1l111l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨ᾵")) or bstack1l111l1_opy_ (u"ࠧ࠷ࠢᾶ")),
                bstack1l111l1_opy_ (u"ࠨࡨࡰࡵࡷࡍࡳ࡬࡯ࠣᾷ"): get_host_info(),
            }
            logger.debug(bstack1l111l1_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡ࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡴࡦࡿ࡬ࡰࡣࡧ࠾ࠥࢁࡽࠣᾸ").format(payload))
            response = bstack11l1l1ll1ll_opy_.bstack11111l11ll1_opy_(bstack11l1ll111ll_opy_, payload)
            if response:
                logger.debug(bstack1l111l1_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡂࡶ࡫࡯ࡨࠥࡪࡡࡵࡣࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨᾹ").format(response))
                return response
            else:
                logger.error(bstack1l111l1_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨᾺ").format(bstack1111l11l11l_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠥ࡟ࡨࡵ࡬࡭ࡧࡦࡸࡇࡻࡩ࡭ࡦࡇࡥࡹࡧ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅࠢࡾࢁ࠿ࠦࡻࡾࠤΆ").format(bstack1111l11l11l_opy_, e))
            return None