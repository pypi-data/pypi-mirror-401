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
import threading
from bstack_utils.helper import bstack11lll111_opy_
from bstack_utils.constants import bstack11l1l111ll1_opy_, EVENTS, STAGE
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11l11_opy_:
    bstack1llll1l1lll1_opy_ = None
    @classmethod
    def bstack111lll11ll_opy_(cls):
        if cls.on() and os.getenv(bstack1l111l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⌋")):
            logger.info(
                bstack1l111l1_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ⌌").format(os.getenv(bstack1l111l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⌍"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⌎"), None) is None or os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⌏")] == bstack1l111l1_opy_ (u"ࠤࡱࡹࡱࡲࠢ⌐"):
            return False
        return True
    @classmethod
    def bstack1lll1l1l1l1l_opy_(cls, bs_config, framework=bstack1l111l1_opy_ (u"ࠥࠦ⌑")):
        bstack11l1l1l1111_opy_ = False
        for fw in bstack11l1l111ll1_opy_:
            if fw in framework:
                bstack11l1l1l1111_opy_ = True
        return bstack11lll111_opy_(bs_config.get(bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⌒"), bstack11l1l1l1111_opy_))
    @classmethod
    def bstack1lll1l111lll_opy_(cls, framework):
        return framework in bstack11l1l111ll1_opy_
    @classmethod
    def bstack1lll1l1lllll_opy_(cls, bs_config, framework):
        return cls.bstack1lll1l1l1l1l_opy_(bs_config, framework) is True and cls.bstack1lll1l111lll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⌓"), None)
    @staticmethod
    def bstack111l1l1ll1_opy_():
        if getattr(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⌔"), None):
            return {
                bstack1l111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⌕"): bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭⌖"),
                bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⌗"): getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⌘"), None)
            }
        if getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⌙"), None):
            return {
                bstack1l111l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ⌚"): bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⌛"),
                bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⌜"): getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⌝"), None)
            }
        return None
    @staticmethod
    def bstack1lll1l111ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11ll11l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111ll11l1_opy_(test, hook_name=None):
        bstack1lll1l111l1l_opy_ = test.parent
        if hook_name in [bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⌞"), bstack1l111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⌟"), bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⌠"), bstack1l111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⌡")]:
            bstack1lll1l111l1l_opy_ = test
        scope = []
        while bstack1lll1l111l1l_opy_ is not None:
            scope.append(bstack1lll1l111l1l_opy_.name)
            bstack1lll1l111l1l_opy_ = bstack1lll1l111l1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1l111l11_opy_(hook_type):
        if hook_type == bstack1l111l1_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦ⌢"):
            return bstack1l111l1_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ⌣")
        elif hook_type == bstack1l111l1_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ⌤"):
            return bstack1l111l1_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤ⌥")
    @staticmethod
    def bstack1lll1l1111ll_opy_(bstack111lll111_opy_):
        try:
            if not bstack11ll11l11_opy_.on():
                return bstack111lll111_opy_
            if os.environ.get(bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣ⌦"), None) == bstack1l111l1_opy_ (u"ࠦࡹࡸࡵࡦࠤ⌧"):
                tests = os.environ.get(bstack1l111l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤ⌨"), None)
                if tests is None or tests == bstack1l111l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ〈"):
                    return bstack111lll111_opy_
                bstack111lll111_opy_ = tests.split(bstack1l111l1_opy_ (u"ࠧ࠭ࠩ〉"))
                return bstack111lll111_opy_
        except Exception as exc:
            logger.debug(bstack1l111l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤ⌫") + str(str(exc)) + bstack1l111l1_opy_ (u"ࠤࠥ⌬"))
        return bstack111lll111_opy_