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
def bstack1llllll1l1l_opy_(package_name):
    bstack1l11l1l_opy_ (u"ࠨࠢࠣࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡥࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࠪࡨ࠲࡬࠴ࠬࠡࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠫ࠮ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡢࡰࡱ࡯࠾࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡰࡢࡥ࡮ࡥ࡬࡫ࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩ࠲ࠠࡇࡣ࡯ࡷࡪࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠌࠣࠤࠥࠦࠢࠣࠤᾛ")
    try:
        import importlib
        import importlib.util
        if hasattr(importlib.util, bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡹࡰࡦࡥࠪᾜ")):
            bstack11111l1l111_opy_ = importlib.util.find_spec(package_name)
            return bstack11111l1l111_opy_ is not None and bstack11111l1l111_opy_.loader is not None
        elif hasattr(importlib, bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭ᾝ")):
            bstack11111l11lll_opy_ = importlib.find_loader(package_name)
            return bstack11111l11lll_opy_ is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        pass
    return False