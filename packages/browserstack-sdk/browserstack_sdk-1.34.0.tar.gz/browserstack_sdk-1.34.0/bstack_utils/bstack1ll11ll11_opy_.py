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
import re
from bstack_utils.bstack1l1111ll_opy_ import bstack1llll1ll1lll_opy_
from bstack_utils.bstack1111111lll_opy_ import bstack1lllll11ll1_opy_
def bstack1llll1lll1ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l111l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ₂")):
        return bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ₃")
    elif fixture_name.startswith(bstack1l111l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ₄")):
        return bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ₅")
    elif fixture_name.startswith(bstack1l111l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ₆")):
        return bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ₇")
    elif fixture_name.startswith(bstack1l111l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ₈")):
        return bstack1l111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨ₉")
def bstack1llll1lll11l_opy_(fixture_name):
    return bool(re.match(bstack1l111l1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ₊"), fixture_name))
def bstack1llll1ll11l1_opy_(fixture_name):
    return bool(re.match(bstack1l111l1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ₋"), fixture_name))
def bstack1llll1ll111l_opy_(fixture_name):
    return bool(re.match(bstack1l111l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ₌"), fixture_name))
def bstack1llll1ll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l111l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ₍")):
        return bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ₎"), bstack1l111l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ₏")
    elif fixture_name.startswith(bstack1l111l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ₐ")):
        return bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ₑ"), bstack1l111l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬₒ")
    elif fixture_name.startswith(bstack1l111l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧₓ")):
        return bstack1l111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧₔ"), bstack1l111l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨₕ")
    elif fixture_name.startswith(bstack1l111l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨₖ")):
        return bstack1l111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨₗ"), bstack1l111l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪₘ")
    return None, None
def bstack1llll1lll111_opy_(hook_name):
    if hook_name in [bstack1l111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧₙ"), bstack1l111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫₚ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll1ll1ll1_opy_(hook_name):
    if hook_name in [bstack1l111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫₛ"), bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪₜ")]:
        return bstack1l111l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ₝")
    elif hook_name in [bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ₞"), bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ₟")]:
        return bstack1l111l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ₠")
    elif hook_name in [bstack1l111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭₡"), bstack1l111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ₢")]:
        return bstack1l111l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ₣")
    elif hook_name in [bstack1l111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ₤"), bstack1l111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ₥")]:
        return bstack1l111l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ₦")
    return hook_name
def bstack1llll1ll1l1l_opy_(node, scenario):
    if hasattr(node, bstack1l111l1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ₧")):
        parts = node.nodeid.rsplit(bstack1l111l1_opy_ (u"ࠤ࡞ࠦ₨"))
        params = parts[-1]
        return bstack1l111l1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥ₩").format(scenario.name, params)
    return scenario.name
def bstack1llll1lll1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l111l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭₪")):
            examples = list(node.callspec.params[bstack1l111l1_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫ₫")].values())
        return examples
    except:
        return []
def bstack1llll1l1llll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll1ll1l11_opy_(report):
    try:
        status = bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭€")
        if report.passed or (report.failed and hasattr(report, bstack1l111l1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ₭"))):
            status = bstack1l111l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ₮")
        elif report.skipped:
            status = bstack1l111l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ₯")
        bstack1llll1ll1lll_opy_(status)
    except:
        pass
def bstack1lll1llll1_opy_(status):
    try:
        bstack1llll1ll11ll_opy_ = bstack1l111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ₰")
        if status == bstack1l111l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ₱"):
            bstack1llll1ll11ll_opy_ = bstack1l111l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ₲")
        elif status == bstack1l111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ₳"):
            bstack1llll1ll11ll_opy_ = bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ₴")
        bstack1llll1ll1lll_opy_(bstack1llll1ll11ll_opy_)
    except:
        pass
def bstack1llll1llll11_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack11l1l111ll_opy_():
    bstack1l111l1_opy_ (u"ࠣࠤࠥࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡶࡹࡵࡧࡶࡸ࠲ࡶࡡࡳࡣ࡯ࡰࡪࡲࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡡ࡯ࡦࠣࡶࡪࡺࡵࡳࡰࠣࡘࡷࡻࡥࠡ࡫ࡩࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧ࡬ࡴࡧࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠨࠢࠣ₵")
    return bstack1lllll11ll1_opy_(bstack1l111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡥࡷࡧ࡬࡭ࡧ࡯ࠫ₶"))