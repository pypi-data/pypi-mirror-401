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
from browserstack_sdk.bstack11l1ll11ll_opy_ import bstack1lll1l11_opy_
from browserstack_sdk.bstack111l111l1l_opy_ import RobotHandler
def bstack1lll111l_opy_(framework):
    if framework.lower() == bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᮨ"):
        return bstack1lll1l11_opy_.version()
    elif framework.lower() == bstack1l11l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᮩ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩ᮪ࠬ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11l1l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ᮫ࠧ")
def bstack11lll11lll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l11l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᮬ"))
        framework_version.append(importlib.metadata.version(bstack1l11l1l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᮭ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᮮ"))
        framework_version.append(importlib.metadata.version(bstack1l11l1l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᮯ")))
    except:
        pass
    return {
        bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᮰"): bstack1l11l1l_opy_ (u"ࠬࡥࠧ᮱").join(framework_name),
        bstack1l11l1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᮲"): bstack1l11l1l_opy_ (u"ࠧࡠࠩ᮳").join(framework_version)
    }