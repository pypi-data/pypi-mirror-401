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
import re
from bstack_utils.bstack1ll1111l11_opy_ import bstack1lllll111l1l_opy_
from bstack_utils.bstack11111l1111_opy_ import bstack1llllll1l1l_opy_
def bstack1lllll1111ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁡")):
        return bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⁢")
    elif fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁣")):
        return bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⁤")
    elif fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁥")):
        return bstack1l11l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⁦")
    elif fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⁧")):
        return bstack1l11l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⁨")
def bstack1llll1llllll_opy_(fixture_name):
    return bool(re.match(bstack1l11l1l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ⁩"), fixture_name))
def bstack1lllll111l11_opy_(fixture_name):
    return bool(re.match(bstack1l11l1l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ⁪"), fixture_name))
def bstack1llll1lllll1_opy_(fixture_name):
    return bool(re.match(bstack1l11l1l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ⁫"), fixture_name))
def bstack1llll1llll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ⁬")):
        return bstack1l11l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⁭"), bstack1l11l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⁮")
    elif fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⁯")):
        return bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ⁰"), bstack1l11l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧⁱ")
    elif fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⁲")):
        return bstack1l11l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⁳"), bstack1l11l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⁴")
    elif fixture_name.startswith(bstack1l11l1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁵")):
        return bstack1l11l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⁶"), bstack1l11l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ⁷")
    return None, None
def bstack1lllll111111_opy_(hook_name):
    if hook_name in [bstack1l11l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⁸"), bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⁹")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll1llll1l_opy_(hook_name):
    if hook_name in [bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⁺"), bstack1l11l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⁻")]:
        return bstack1l11l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⁼")
    elif hook_name in [bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⁽"), bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⁾")]:
        return bstack1l11l1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧⁿ")
    elif hook_name in [bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ₀"), bstack1l11l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ₁")]:
        return bstack1l11l1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ₂")
    elif hook_name in [bstack1l11l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ₃"), bstack1l11l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ₄")]:
        return bstack1l11l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ₅")
    return hook_name
def bstack1lllll11111l_opy_(node, scenario):
    if hasattr(node, bstack1l11l1l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ₆")):
        parts = node.nodeid.rsplit(bstack1l11l1l_opy_ (u"ࠦࡠࠨ₇"))
        params = parts[-1]
        return bstack1l11l1l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ₈").format(scenario.name, params)
    return scenario.name
def bstack1llll1lll11l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l11l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ₉")):
            examples = list(node.callspec.params[bstack1l11l1l_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭₊")].values())
        return examples
    except:
        return []
def bstack1llll1lll1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lllll1111l1_opy_(report):
    try:
        status = bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ₋")
        if report.passed or (report.failed and hasattr(report, bstack1l11l1l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ₌"))):
            status = bstack1l11l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ₍")
        elif report.skipped:
            status = bstack1l11l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ₎")
        bstack1lllll111l1l_opy_(status)
    except:
        pass
def bstack11ll111ll1_opy_(status):
    try:
        bstack1llll1lll111_opy_ = bstack1l11l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ₏")
        if status == bstack1l11l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ₐ"):
            bstack1llll1lll111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧₑ")
        elif status == bstack1l11l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩₒ"):
            bstack1llll1lll111_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪₓ")
        bstack1lllll111l1l_opy_(bstack1llll1lll111_opy_)
    except:
        pass
def bstack1llll1lll1l1_opy_(item=None, report=None, summary=None, extra=None):
    return
def bstack1ll1l11l1_opy_():
    bstack1l11l1l_opy_ (u"ࠥࠦࠧࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺ࠭ࡱࡣࡵࡥࡱࡲࡥ࡭ࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲ࡚ࠥࡲࡶࡧࠣ࡭࡫ࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡮ࡶࡩࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥࠣࠤࠥₔ")
    return bstack1llllll1l1l_opy_(bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡧࡲࡢ࡮࡯ࡩࡱ࠭ₕ"))