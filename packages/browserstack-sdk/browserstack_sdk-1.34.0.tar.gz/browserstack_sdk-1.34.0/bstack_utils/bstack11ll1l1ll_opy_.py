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
from browserstack_sdk.bstack11l11111l1_opy_ import bstack1lllllllll_opy_
from browserstack_sdk.bstack11111lll11_opy_ import RobotHandler
def bstack11l11l1ll_opy_(framework):
    if framework.lower() == bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᯉ"):
        return bstack1lllllllll_opy_.version()
    elif framework.lower() == bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᯊ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᯋ"):
        import behave
        return behave.__version__
    else:
        return bstack1l111l1_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᯌ")
def bstack11ll1l1ll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l111l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᯍ"))
        framework_version.append(importlib.metadata.version(bstack1l111l1_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᯎ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᯏ"))
        framework_version.append(importlib.metadata.version(bstack1l111l1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᯐ")))
    except:
        pass
    return {
        bstack1l111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᯑ"): bstack1l111l1_opy_ (u"ࠪࡣࠬᯒ").join(framework_name),
        bstack1l111l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᯓ"): bstack1l111l1_opy_ (u"ࠬࡥࠧᯔ").join(framework_version)
    }