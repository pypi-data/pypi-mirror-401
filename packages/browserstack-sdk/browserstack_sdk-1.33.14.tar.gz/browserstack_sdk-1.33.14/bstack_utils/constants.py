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
import re
from enum import Enum
bstack11l1111l11_opy_ = {
  bstack1l11l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᠱ"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪᠲ"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᠳ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫᠴ"),
  bstack1l11l1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᠵ"): bstack1l11l1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᠶ"),
  bstack1l11l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᠷ"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᠸ"),
  bstack1l11l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᠹ"): bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨᠺ"),
  bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᠻ"): bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨᠼ"),
  bstack1l11l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᠽ"): bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠾ"),
  bstack1l11l1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᠿ"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫᡀ"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬᡁ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨᡂ"),
  bstack1l11l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᡃ"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧᡄ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᡅ"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨᡆ"),
  bstack1l11l1l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬᡇ"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬᡈ"),
  bstack1l11l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᡉ"): bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᡊ"),
  bstack1l11l1l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᡋ"): bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᡌ"),
  bstack1l11l1l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᡍ"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᡎ"),
  bstack1l11l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᡏ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩᡐ"),
  bstack1l11l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᡑ"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᡒ"),
  bstack1l11l1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᡓ"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪᡔ"),
  bstack1l11l1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᡕ"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᡖ"),
  bstack1l11l1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᡗ"): bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨᡘ"),
  bstack1l11l1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬᡙ"): bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬᡚ"),
  bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᡛ"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧᡜ"),
  bstack1l11l1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ᡝ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭ᡞ"),
  bstack1l11l1l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪᡟ"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪᡠ"),
  bstack1l11l1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᡡ"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬᡢ"),
  bstack1l11l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᡣ"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩᡤ"),
  bstack1l11l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᡥ"): bstack1l11l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᡦ"),
  bstack1l11l1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᡧ"): bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩᡨ"),
  bstack1l11l1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᡩ"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᡪ"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᡫ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧᡬ"),
  bstack1l11l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᡭ"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪᡮ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪᡯ"): bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ᡰ"),
  bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᡱ"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᡲ"),
  bstack1l11l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᡳ"): bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨᡴ"),
  bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᡵ"): bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᡶ"),
  bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᡷ"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧᡸ"),
  bstack1l11l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪ᡹"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪ᡺"),
  bstack1l11l1l_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭᡻"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭᡼"),
  bstack1l11l1l_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩ᡽"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩ᡾"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᡿"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᢀ"),
  bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᢁ"): bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᢂ")
}
bstack11l1l1111ll_opy_ = [
  bstack1l11l1l_opy_ (u"ࠪࡳࡸ࠭ᢃ"),
  bstack1l11l1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᢄ"),
  bstack1l11l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᢅ"),
  bstack1l11l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᢆ"),
  bstack1l11l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᢇ"),
  bstack1l11l1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬᢈ"),
  bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᢉ"),
]
bstack11l1llll1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᢊ"): [bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᢋ"), bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧᢌ")],
  bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᢍ"): bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᢎ"),
  bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᢏ"): bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬᢐ"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᢑ"): bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩᢒ"),
  bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢓ"): bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᢔ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᢕ"): bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᢖ"),
  bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᢗ"): bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨᢘ"),
  bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨᢙ"): bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩᢚ"),
  bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࠪᢛ"): [bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ࠭ᢜ"), bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫᢝ")],
  bstack1l11l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᢞ"): bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨᢟ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᢠ"): bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᢡ"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᢢ"): [bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫᢣ"), bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᢤ")],
  bstack1l11l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᢥ"): bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗ࡙ࡗࡈࡏࡔࡅࡄࡐࡊ࠭ᢦ"),
  bstack1l11l1l_opy_ (u"ࠫࡸࡳࡡࡳࡶࡖࡩࡱ࡫ࡣࡵ࡫ࡲࡲࡋ࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࡩࡸࡋࡎࡗࠩᢧ"): bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡔࡘࡃࡉࡇࡖࡘࡗࡇࡔࡊࡑࡑࡣࡘࡓࡁࡓࡖࡢࡗࡊࡒࡅࡄࡖࡌࡓࡓࡥࡆࡆࡃࡗ࡙ࡗࡋ࡟ࡃࡔࡄࡒࡈࡎࡅࡔࠩᢨ")
}
bstack1l1l1ll11_opy_ = {
  bstack1l11l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᢩ"): [bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᢪ"), bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᢫")],
  bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᢬"): [bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴࡡ࡮ࡩࡾ࠭᢭"), bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᢮")],
  bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᢯"): bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᢰ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᢱ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᢲ"),
  bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᢳ"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᢴ"),
  bstack1l11l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᢵ"): [bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡵࡶࡰࠨᢶ"), bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬᢷ")],
  bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᢸ"): bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᢹ"),
  bstack1l11l1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᢺ"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᢻ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࠨᢼ"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࠨᢽ"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᢾ"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᢿ"),
  bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᣀ"): bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᣁ"),
  bstack1l11l1l_opy_ (u"ࠥࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡈࡒࡉࠣᣂ"): bstack1l11l1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࡴ࡯ࡤࡶࡹ࡙ࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࡇࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࡥࡴࠤᣃ"),
}
bstack1llll1l1l1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᣄ"): bstack1l11l1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᣅ"),
  bstack1l11l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᣆ"): [bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᣇ"), bstack1l11l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᣈ")],
  bstack1l11l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᣉ"): bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᣊ"),
  bstack1l11l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᣋ"): bstack1l11l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᣌ"),
  bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᣍ"): [bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᣎ"), bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᣏ")],
  bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᣐ"): bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᣑ"),
  bstack1l11l1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩᣒ"): bstack1l11l1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫᣓ"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᣔ"): [bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᣕ"), bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᣖ")],
  bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᣗ"): [bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬᣘ"), bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬᣙ")]
}
bstack1l1l11l11_opy_ = [
  bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬᣚ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪᣛ"),
  bstack1l11l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧᣜ"),
  bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩᣝ"),
  bstack1l11l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬᣞ"),
  bstack1l11l1l_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩᣟ"),
  bstack1l11l1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨᣠ"),
  bstack1l11l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᣡ"),
  bstack1l11l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬᣢ"),
  bstack1l11l1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᣣ"),
  bstack1l11l1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᣤ"),
  bstack1l11l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᣥ"),
]
bstack11l1ll1lll_opy_ = [
  bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᣦ"),
  bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᣧ"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᣨ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᣩ"),
  bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᣪ"),
  bstack1l11l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᣫ"),
  bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᣬ"),
  bstack1l11l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᣭ"),
  bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᣮ"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᣯ"),
  bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᣰ"),
  bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠨᣱ"),
  bstack1l11l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᣲ"),
  bstack1l11l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡗࡥ࡬࠭ᣳ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᣴ"),
  bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᣵ"),
  bstack1l11l1l_opy_ (u"࠭ࡲࡦࡴࡸࡲ࡙࡫ࡳࡵࡵࠪ᣶"),
  bstack1l11l1l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠶࠭᣷"),
  bstack1l11l1l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠸ࠧ᣸"),
  bstack1l11l1l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠳ࠨ᣹"),
  bstack1l11l1l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠵ࠩ᣺"),
  bstack1l11l1l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠷ࠪ᣻"),
  bstack1l11l1l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠹ࠫ᣼"),
  bstack1l11l1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠻ࠬ᣽"),
  bstack1l11l1l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠽࠭᣾"),
  bstack1l11l1l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠿ࠧ᣿"),
  bstack1l11l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᤀ"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᤁ"),
  bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᤂ"),
  bstack1l11l1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᤃ"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᤄ"),
  bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫᤅ"),
  bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡶࡴࡪࡱࡱࡷࠬᤆ"),
  bstack1l11l1l_opy_ (u"ࠩ࡫ࡹࡧࡘࡥࡨ࡫ࡲࡲࠬᤇ")
]
bstack11l1l111ll1_opy_ = [
  bstack1l11l1l_opy_ (u"ࠪࡹࡵࡲ࡯ࡢࡦࡐࡩࡩ࡯ࡡࠨᤈ"),
  bstack1l11l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᤉ"),
  bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᤊ"),
  bstack1l11l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᤋ"),
  bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡕࡸࡩࡰࡴ࡬ࡸࡾ࠭ᤌ"),
  bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᤍ"),
  bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡕࡣࡪࠫᤎ"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᤏ"),
  bstack1l11l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᤐ"),
  bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᤑ"),
  bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᤒ"),
  bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᤓ"),
  bstack1l11l1l_opy_ (u"ࠨࡱࡶࠫᤔ"),
  bstack1l11l1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᤕ"),
  bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩᤖ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ᤗ"),
  bstack1l11l1l_opy_ (u"ࠬࡸࡥࡨ࡫ࡲࡲࠬᤘ"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨᤙ"),
  bstack1l11l1l_opy_ (u"ࠧ࡮ࡣࡦ࡬࡮ࡴࡥࠨᤚ"),
  bstack1l11l1l_opy_ (u"ࠨࡴࡨࡷࡴࡲࡵࡵ࡫ࡲࡲࠬᤛ"),
  bstack1l11l1l_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧᤜ"),
  bstack1l11l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᤝ"),
  bstack1l11l1l_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪᤞ"),
  bstack1l11l1l_opy_ (u"ࠬࡴ࡯ࡑࡣࡪࡩࡑࡵࡡࡥࡖ࡬ࡱࡪࡵࡵࡵࠩ᤟"),
  bstack1l11l1l_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧᤠ"),
  bstack1l11l1l_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᤡ"),
  bstack1l11l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᤢ"),
  bstack1l11l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡨࡲࡩࡑࡥࡺࡵࠪᤣ"),
  bstack1l11l1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧᤤ"),
  bstack1l11l1l_opy_ (u"ࠫࡳࡵࡐࡪࡲࡨࡰ࡮ࡴࡥࠨᤥ"),
  bstack1l11l1l_opy_ (u"ࠬࡩࡨࡦࡥ࡮࡙ࡗࡒࠧᤦ"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᤧ"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡃࡰࡱ࡮࡭ࡪࡹࠧᤨ"),
  bstack1l11l1l_opy_ (u"ࠨࡥࡤࡴࡹࡻࡲࡦࡅࡵࡥࡸ࡮ࠧᤩ"),
  bstack1l11l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᤪ"),
  bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᤫ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᤬"),
  bstack1l11l1l_opy_ (u"ࠬࡴ࡯ࡃ࡮ࡤࡲࡰࡖ࡯࡭࡮࡬ࡲ࡬࠭᤭"),
  bstack1l11l1l_opy_ (u"࠭࡭ࡢࡵ࡮ࡗࡪࡴࡤࡌࡧࡼࡷࠬ᤮"),
  bstack1l11l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡌࡰࡩࡶࠫ᤯"),
  bstack1l11l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡊࡦࠪᤰ"),
  bstack1l11l1l_opy_ (u"ࠩࡧࡩࡩ࡯ࡣࡢࡶࡨࡨࡉ࡫ࡶࡪࡥࡨࠫᤱ"),
  bstack1l11l1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡓࡥࡷࡧ࡭ࡴࠩᤲ"),
  bstack1l11l1l_opy_ (u"ࠫࡵ࡮࡯࡯ࡧࡑࡹࡲࡨࡥࡳࠩᤳ"),
  bstack1l11l1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪᤴ"),
  bstack1l11l1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡓࡵࡺࡩࡰࡰࡶࠫᤵ"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬᤶ"),
  bstack1l11l1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᤷ"),
  bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ᤸ"),
  bstack1l11l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡅ࡭ࡴࡳࡥࡵࡴ࡬ࡧ᤹ࠬ"),
  bstack1l11l1l_opy_ (u"ࠫࡻ࡯ࡤࡦࡱ࡙࠶ࠬ᤺"),
  bstack1l11l1l_opy_ (u"ࠬࡳࡩࡥࡕࡨࡷࡸ࡯࡯࡯ࡋࡱࡷࡹࡧ࡬࡭ࡃࡳࡴࡸ᤻࠭"),
  bstack1l11l1l_opy_ (u"࠭ࡥࡴࡲࡵࡩࡸࡹ࡯ࡔࡧࡵࡺࡪࡸࠧ᤼"),
  bstack1l11l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭᤽"),
  bstack1l11l1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡆࡨࡵ࠭᤾"),
  bstack1l11l1l_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩ᤿"),
  bstack1l11l1l_opy_ (u"ࠪࡷࡾࡴࡣࡕ࡫ࡰࡩ࡜࡯ࡴࡩࡐࡗࡔࠬ᥀"),
  bstack1l11l1l_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ᥁"),
  bstack1l11l1l_opy_ (u"ࠬ࡭ࡰࡴࡎࡲࡧࡦࡺࡩࡰࡰࠪ᥂"),
  bstack1l11l1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧ᥃"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ᥄"),
  bstack1l11l1l_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࡃࡩࡣࡱ࡫ࡪࡐࡡࡳࠩ᥅"),
  bstack1l11l1l_opy_ (u"ࠩࡻࡱࡸࡐࡡࡳࠩ᥆"),
  bstack1l11l1l_opy_ (u"ࠪࡼࡲࡾࡊࡢࡴࠪ᥇"),
  bstack1l11l1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪ᥈"),
  bstack1l11l1l_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ᥉"),
  bstack1l11l1l_opy_ (u"࠭ࡷࡴࡎࡲࡧࡦࡲࡓࡶࡲࡳࡳࡷࡺࠧ᥊"),
  bstack1l11l1l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪ᥋"),
  bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᥌"),
  bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨ᥍"),
  bstack1l11l1l_opy_ (u"ࠪࡶࡪࡹࡩࡨࡰࡄࡴࡵ࠭᥎"),
  bstack1l11l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࡳࠨ᥏"),
  bstack1l11l1l_opy_ (u"ࠬࡩࡡ࡯ࡣࡵࡽࠬᥐ"),
  bstack1l11l1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᥑ"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᥒ"),
  bstack1l11l1l_opy_ (u"ࠨ࡫ࡨࠫᥓ"),
  bstack1l11l1l_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᥔ"),
  bstack1l11l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᥕ"),
  bstack1l11l1l_opy_ (u"ࠫࡶࡻࡥࡶࡧࠪᥖ"),
  bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡲࡦࡲࠧᥗ"),
  bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࡖࡸࡴࡸࡥࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠧᥘ"),
  bstack1l11l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡃࡢ࡯ࡨࡶࡦࡏ࡭ࡢࡩࡨࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭ᥙ"),
  bstack1l11l1l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡋࡸࡤ࡮ࡸࡨࡪࡎ࡯ࡴࡶࡶࠫᥚ"),
  bstack1l11l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡉ࡯ࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬᥛ"),
  bstack1l11l1l_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᥜ"),
  bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡳࡦࡴࡹࡩࡉ࡫ࡶࡪࡥࡨࠫᥝ"),
  bstack1l11l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᥞ"),
  bstack1l11l1l_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨᥟ"),
  bstack1l11l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡢࡵࡶࡧࡴࡪࡥࠨᥠ"),
  bstack1l11l1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡊࡱࡶࡈࡪࡼࡩࡤࡧࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᥡ"),
  bstack1l11l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡃࡸࡨ࡮ࡵࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩᥢ"),
  bstack1l11l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡴࡵࡲࡥࡑࡣࡼࠫᥣ"),
  bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᥤ"),
  bstack1l11l1l_opy_ (u"ࠬࡽࡤࡪࡱࡖࡩࡷࡼࡩࡤࡧࠪᥥ"),
  bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᥦ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡄࡴࡲࡷࡸ࡙ࡩࡵࡧࡗࡶࡦࡩ࡫ࡪࡰࡪࠫᥧ"),
  bstack1l11l1l_opy_ (u"ࠨࡪ࡬࡫࡭ࡉ࡯࡯ࡶࡵࡥࡸࡺࠧᥨ"),
  bstack1l11l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡒࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࡸ࠭ᥩ"),
  bstack1l11l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ᥪ"),
  bstack1l11l1l_opy_ (u"ࠫࡸ࡯࡭ࡐࡲࡷ࡭ࡴࡴࡳࠨᥫ"),
  bstack1l11l1l_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪᥬ"),
  bstack1l11l1l_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨᥭ"),
  bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᥮"),
  bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᥯"),
  bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᥰ"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᥱ"),
  bstack1l11l1l_opy_ (u"ࠫࡵࡧࡧࡦࡎࡲࡥࡩ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠧᥲ"),
  bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫᥳ"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡳࡺࡺࡳࠨᥴ"),
  bstack1l11l1l_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪ᥵")
]
bstack111llll1l_opy_ = {
  bstack1l11l1l_opy_ (u"ࠨࡸࠪ᥶"): bstack1l11l1l_opy_ (u"ࠩࡹࠫ᥷"),
  bstack1l11l1l_opy_ (u"ࠪࡪࠬ᥸"): bstack1l11l1l_opy_ (u"ࠫ࡫࠭᥹"),
  bstack1l11l1l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫ᥺"): bstack1l11l1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬ᥻"),
  bstack1l11l1l_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᥼"): bstack1l11l1l_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧ᥽"),
  bstack1l11l1l_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭᥾"): bstack1l11l1l_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧ᥿"),
  bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧᦀ"): bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᦁ"),
  bstack1l11l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩᦂ"): bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᦃ"),
  bstack1l11l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᦄ"): bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᦅ"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ᦆ"): bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᦇ"),
  bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ᦈ"): bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᦉ"),
  bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨᦊ"): bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᦋ"),
  bstack1l11l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪᦌ"): bstack1l11l1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᦍ"),
  bstack1l11l1l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᦎ"): bstack1l11l1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᦏ"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᦐ"): bstack1l11l1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩᦑ"),
  bstack1l11l1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪᦒ"): bstack1l11l1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᦓ"),
  bstack1l11l1l_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧᦔ"): bstack1l11l1l_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨᦕ"),
  bstack1l11l1l_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭ᦖ"): bstack1l11l1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᦗ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩᦘ"): bstack1l11l1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᦙ"),
  bstack1l11l1l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᦚ"): bstack1l11l1l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᦛ"),
  bstack1l11l1l_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬᦜ"): bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ᦝ"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᦞ"): bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᦟ"),
  bstack1l11l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠪᦠ"): bstack1l11l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡴࡪࡧࡴࡦࡴࠪᦡ")
}
bstack11l11ll111l_opy_ = bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬࡯ࡴࡩࡷࡥ࠲ࡨࡵ࡭࠰ࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬࠳ࡷ࡫࡬ࡦࡣࡶࡩࡸ࠵࡬ࡢࡶࡨࡷࡹ࠵ࡤࡰࡹࡱࡰࡴࡧࡤࠣᦢ")
bstack11l1l1l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠳࡭࡫ࡡ࡭ࡶ࡫ࡧ࡭࡫ࡣ࡬ࠤᦣ")
bstack11lllllll1_opy_ = bstack1l11l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡥࡥࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡳࡦࡰࡧࡣࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣᦤ")
bstack1lll111lll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧᦥ")
bstack1ll1l1l1l1_opy_ = bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪᦦ")
bstack11llll111_opy_ = bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬᦧ")
bstack1l1ll1l1l1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠩࡧࡩ࡫ࡧࡵ࡭ࡶࠪᦨ"): bstack1l11l1l_opy_ (u"ࠪ࡬ࡺࡨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᦩ"),
  bstack1l11l1l_opy_ (u"ࠫࡺࡹ࠭ࡦࡣࡶࡸࠬᦪ"): bstack1l11l1l_opy_ (u"ࠬ࡮ࡵࡣ࠯ࡸࡷࡪ࠳࡯࡯࡮ࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᦫ"),
  bstack1l11l1l_opy_ (u"࠭ࡵࡴࠩ᦬"): bstack1l11l1l_opy_ (u"ࠧࡩࡷࡥ࠱ࡺࡹ࠭ࡰࡰ࡯ࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ᦭"),
  bstack1l11l1l_opy_ (u"ࠨࡧࡸࠫ᦮"): bstack1l11l1l_opy_ (u"ࠩ࡫ࡹࡧ࠳ࡥࡶ࠯ࡲࡲࡱࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ᦯"),
  bstack1l11l1l_opy_ (u"ࠪ࡭ࡳ࠭ᦰ"): bstack1l11l1l_opy_ (u"ࠫ࡭ࡻࡢ࠮ࡣࡳࡷ࠲ࡵ࡮࡭ࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᦱ"),
  bstack1l11l1l_opy_ (u"ࠬࡧࡵࠨᦲ"): bstack1l11l1l_opy_ (u"࠭ࡨࡶࡤ࠰ࡥࡵࡹࡥ࠮ࡱࡱࡰࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᦳ")
}
bstack11l1l11lll1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᦴ"): 50,
  bstack1l11l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᦵ"): 40,
  bstack1l11l1l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᦶ"): 30,
  bstack1l11l1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᦷ"): 20,
  bstack1l11l1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᦸ"): 10
}
bstack1llll11ll_opy_ = bstack11l1l11lll1_opy_[bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᦹ")]
bstack1l1l1l111_opy_ = bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᦺ")
bstack111111ll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᦻ")
bstack1llllll1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᦼ")
bstack11ll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᦽ")
bstack1lll111111_opy_ = bstack1l11l1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᦾ")
bstack1lll1l1lll_opy_ = {
  bstack1l11l1l_opy_ (u"ࠫࡘࡊࡋ࠮ࡉࡈࡒ࠲࠶࠰࠶ࠩᦿ"): bstack1l11l1l_opy_ (u"ࠬ࠰ࠪࠫࠢ࡞ࡗࡉࡑ࠭ࡈࡇࡑ࠱࠵࠶࠵࡞ࠢࡣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࡥࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡻࡲࡹࡷࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠲࡚ࠥࡨࡪࡵࠣࡱࡦࡿࠠࡤࡣࡸࡷࡪࠦࡣࡰࡰࡩࡰ࡮ࡩࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࠠࡪࡶࠣࡹࡸ࡯࡮ࡨ࠼ࠣࡴ࡮ࡶࠠࡶࡰ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡴࡦࡸࡡ࡭࡮ࡨࡰࠥ࠰ࠪࠫࠩᧀ")
}
bstack11l11ll1l1l_opy_ = [bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᧁ"), bstack1l11l1l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧᧂ")]
bstack11l1l11l1ll_opy_ = [bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᧃ"), bstack1l11l1l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫᧄ")]
bstack1l11l1ll1l_opy_ = re.compile(bstack1l11l1l_opy_ (u"ࠪࡢࡠࡢ࡜ࡸ࠯ࡠ࠯࠿࠴ࠪࠥࠩᧅ"))
bstack1111lllll_opy_ = [
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡏࡣࡰࡩࠬᧆ"),
  bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᧇ"),
  bstack1l11l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᧈ"),
  bstack1l11l1l_opy_ (u"ࠧ࡯ࡧࡺࡇࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࠫᧉ"),
  bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࠬ᧊"),
  bstack1l11l1l_opy_ (u"ࠩࡸࡨ࡮ࡪࠧ᧋"),
  bstack1l11l1l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ᧌"),
  bstack1l11l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࠫ᧍"),
  bstack1l11l1l_opy_ (u"ࠬࡵࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪ᧎"),
  bstack1l11l1l_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࠫ᧏"),
  bstack1l11l1l_opy_ (u"ࠧ࡯ࡱࡕࡩࡸ࡫ࡴࠨ᧐"), bstack1l11l1l_opy_ (u"ࠨࡨࡸࡰࡱࡘࡥࡴࡧࡷࠫ᧑"),
  bstack1l11l1l_opy_ (u"ࠩࡦࡰࡪࡧࡲࡔࡻࡶࡸࡪࡳࡆࡪ࡮ࡨࡷࠬ᧒"),
  bstack1l11l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡖ࡬ࡱ࡮ࡴࡧࡴࠩ᧓"),
  bstack1l11l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡪࡸࡦࡰࡴࡰࡥࡳࡩࡥࡍࡱࡪ࡫࡮ࡴࡧࠨ᧔"),
  bstack1l11l1l_opy_ (u"ࠬࡵࡴࡩࡧࡵࡅࡵࡶࡳࠨ᧕"),
  bstack1l11l1l_opy_ (u"࠭ࡰࡳ࡫ࡱࡸࡕࡧࡧࡦࡕࡲࡹࡷࡩࡥࡐࡰࡉ࡭ࡳࡪࡆࡢ࡫࡯ࡹࡷ࡫ࠧ᧖"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡅࡨࡺࡩࡷ࡫ࡷࡽࠬ᧗"), bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡕࡧࡣ࡬ࡣࡪࡩࠬ᧘"), bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ᧙"), bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡔࡦࡩ࡫ࡢࡩࡨࠫ᧚"), bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࡘࡣ࡬ࡸࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭᧛"),
  bstack1l11l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ᧜"),
  bstack1l11l1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙࡫ࡳࡵࡒࡤࡧࡰࡧࡧࡦࡵࠪ᧝"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࠩ᧞"), bstack1l11l1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡅࡲࡺࡪࡸࡡࡨࡧࡈࡲࡩࡏ࡮ࡵࡧࡱࡸࠬ᧟"),
  bstack1l11l1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧ᧠"),
  bstack1l11l1l_opy_ (u"ࠪࡥࡩࡨࡐࡰࡴࡷࠫ᧡"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡉ࡫ࡶࡪࡥࡨࡗࡴࡩ࡫ࡦࡶࠪ᧢"),
  bstack1l11l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱ࡚ࡩ࡮ࡧࡲࡹࡹ࠭᧣"),
  bstack1l11l1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡶ࡫ࠫ᧤"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡸࡧࠫ᧥"), bstack1l11l1l_opy_ (u"ࠨࡣࡹࡨࡑࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫ᧦"), bstack1l11l1l_opy_ (u"ࠩࡤࡺࡩࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫ᧧"), bstack1l11l1l_opy_ (u"ࠪࡥࡻࡪࡁࡳࡩࡶࠫ᧨"),
  bstack1l11l1l_opy_ (u"ࠫࡺࡹࡥࡌࡧࡼࡷࡹࡵࡲࡦࠩ᧩"), bstack1l11l1l_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡶ࡫ࠫ᧪"), bstack1l11l1l_opy_ (u"࠭࡫ࡦࡻࡶࡸࡴࡸࡥࡑࡣࡶࡷࡼࡵࡲࡥࠩ᧫"),
  bstack1l11l1l_opy_ (u"ࠧ࡬ࡧࡼࡅࡱ࡯ࡡࡴࠩ᧬"), bstack1l11l1l_opy_ (u"ࠨ࡭ࡨࡽࡕࡧࡳࡴࡹࡲࡶࡩ࠭᧭"),
  bstack1l11l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࠫ᧮"), bstack1l11l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡃࡵ࡫ࡸ࠭᧯"), bstack1l11l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪࡊࡩࡳࠩ᧰"), bstack1l11l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡇ࡭ࡸ࡯࡮ࡧࡐࡥࡵࡶࡩ࡯ࡩࡉ࡭ࡱ࡫ࠧ᧱"), bstack1l11l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶ࡚ࡹࡥࡔࡻࡶࡸࡪࡳࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪ᧲"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࠪ᧳"), bstack1l11l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡐࡰࡴࡷࡷࠬ᧴"),
  bstack1l11l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡅ࡫ࡶࡥࡧࡲࡥࡃࡷ࡬ࡰࡩࡉࡨࡦࡥ࡮ࠫ᧵"),
  bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࡕ࡫ࡰࡩࡴࡻࡴࠨ᧶"),
  bstack1l11l1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡅࡨࡺࡩࡰࡰࠪ᧷"), bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡈࡧࡴࡦࡩࡲࡶࡾ࠭᧸"), bstack1l11l1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡲࡹࡌ࡬ࡢࡩࡶࠫ᧹"), bstack1l11l1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡡ࡭ࡋࡱࡸࡪࡴࡴࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᧺"),
  bstack1l11l1l_opy_ (u"ࠨࡦࡲࡲࡹ࡙ࡴࡰࡲࡄࡴࡵࡕ࡮ࡓࡧࡶࡩࡹ࠭᧻"),
  bstack1l11l1l_opy_ (u"ࠩࡸࡲ࡮ࡩ࡯ࡥࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫ᧼"), bstack1l11l1l_opy_ (u"ࠪࡶࡪࡹࡥࡵࡍࡨࡽࡧࡵࡡࡳࡦࠪ᧽"),
  bstack1l11l1l_opy_ (u"ࠫࡳࡵࡓࡪࡩࡱࠫ᧾"),
  bstack1l11l1l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩ࡚ࡴࡩ࡮ࡲࡲࡶࡹࡧ࡮ࡵࡘ࡬ࡩࡼࡹࠧ᧿"),
  bstack1l11l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯ࡦࡵࡳ࡮ࡪࡗࡢࡶࡦ࡬ࡪࡸࡳࠨᨀ"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᨁ"),
  bstack1l11l1l_opy_ (u"ࠨࡴࡨࡧࡷ࡫ࡡࡵࡧࡆ࡬ࡷࡵ࡭ࡦࡆࡵ࡭ࡻ࡫ࡲࡔࡧࡶࡷ࡮ࡵ࡮ࡴࠩᨂ"),
  bstack1l11l1l_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦ࡙ࡨࡦࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᨃ"),
  bstack1l11l1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡐࡢࡶ࡫ࠫᨄ"),
  bstack1l11l1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡘࡶࡥࡦࡦࠪᨅ"),
  bstack1l11l1l_opy_ (u"ࠬ࡭ࡰࡴࡇࡱࡥࡧࡲࡥࡥࠩᨆ"),
  bstack1l11l1l_opy_ (u"࠭ࡩࡴࡊࡨࡥࡩࡲࡥࡴࡵࠪᨇ"),
  bstack1l11l1l_opy_ (u"ࠧࡢࡦࡥࡉࡽ࡫ࡣࡕ࡫ࡰࡩࡴࡻࡴࠨᨈ"),
  bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࡔࡥࡵ࡭ࡵࡺࠧᨉ"),
  bstack1l11l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡄࡦࡸ࡬ࡧࡪࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᨊ"),
  bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡈࡴࡤࡲࡹࡖࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠪᨋ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡓࡧࡴࡶࡴࡤࡰࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᨌ"),
  bstack1l11l1l_opy_ (u"ࠬࡹࡹࡴࡶࡨࡱࡕࡵࡲࡵࠩᨍ"),
  bstack1l11l1l_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡇࡤࡣࡊࡲࡷࡹ࠭ᨎ"),
  bstack1l11l1l_opy_ (u"ࠧࡴ࡭࡬ࡴ࡚ࡴ࡬ࡰࡥ࡮ࠫᨏ"), bstack1l11l1l_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡕࡻࡳࡩࠬᨐ"), bstack1l11l1l_opy_ (u"ࠩࡸࡲࡱࡵࡣ࡬ࡍࡨࡽࠬᨑ"),
  bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡍࡣࡸࡲࡨ࡮ࠧᨒ"),
  bstack1l11l1l_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡨࡧࡴࡄࡣࡳࡸࡺࡸࡥࠨᨓ"),
  bstack1l11l1l_opy_ (u"ࠬࡻ࡮ࡪࡰࡶࡸࡦࡲ࡬ࡐࡶ࡫ࡩࡷࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧᨔ"),
  bstack1l11l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡗࡪࡰࡧࡳࡼࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࠨᨕ"),
  bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚࡯ࡰ࡮ࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᨖ"),
  bstack1l11l1l_opy_ (u"ࠨࡧࡱࡪࡴࡸࡣࡦࡃࡳࡴࡎࡴࡳࡵࡣ࡯ࡰࠬᨗ"),
  bstack1l11l1l_opy_ (u"ࠩࡨࡲࡸࡻࡲࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡵࡋࡥࡻ࡫ࡐࡢࡩࡨࡷᨘࠬ"), bstack1l11l1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡈࡪࡼࡴࡰࡱ࡯ࡷࡕࡵࡲࡵࠩᨙ"), bstack1l11l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨ࡛ࡪࡨࡶࡪࡧࡺࡈࡪࡺࡡࡪ࡮ࡶࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠧᨚ"),
  bstack1l11l1l_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡶࡰࡴࡅࡤࡧ࡭࡫ࡌࡪ࡯࡬ࡸࠬᨛ"),
  bstack1l11l1l_opy_ (u"࠭ࡣࡢ࡮ࡨࡲࡩࡧࡲࡇࡱࡵࡱࡦࡺࠧ᨜"),
  bstack1l11l1l_opy_ (u"ࠧࡣࡷࡱࡨࡱ࡫ࡉࡥࠩ᨝"),
  bstack1l11l1l_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ᨞"),
  bstack1l11l1l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡊࡴࡡࡣ࡮ࡨࡨࠬ᨟"), bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࡘ࡫ࡲࡷ࡫ࡦࡩࡸࡇࡵࡵࡪࡲࡶ࡮ࢀࡥࡥࠩᨠ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰࡃࡦࡧࡪࡶࡴࡂ࡮ࡨࡶࡹࡹࠧᨡ"), bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡇ࡭ࡸࡳࡩࡴࡵࡄࡰࡪࡸࡴࡴࠩᨢ"),
  bstack1l11l1l_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪࡏ࡮ࡴࡶࡵࡹࡲ࡫࡮ࡵࡵࡏ࡭ࡧ࠭ᨣ"),
  bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡗࡥࡵ࠭ᨤ"),
  bstack1l11l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡰ࡬ࡸ࡮ࡧ࡬ࡖࡴ࡯ࠫᨥ"), bstack1l11l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡃ࡯ࡰࡴࡽࡐࡰࡲࡸࡴࡸ࠭ᨦ"), bstack1l11l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡌ࡫ࡳࡵࡲࡦࡈࡵࡥࡺࡪࡗࡢࡴࡱ࡭ࡳ࡭ࠧᨧ"), bstack1l11l1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵ࡫࡮ࡍ࡫ࡱ࡯ࡸࡏ࡮ࡃࡣࡦ࡯࡬ࡸ࡯ࡶࡰࡧࠫᨨ"),
  bstack1l11l1l_opy_ (u"ࠬࡱࡥࡦࡲࡎࡩࡾࡉࡨࡢ࡫ࡱࡷࠬᨩ"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࢀࡡࡣ࡮ࡨࡗࡹࡸࡩ࡯ࡩࡶࡈ࡮ࡸࠧᨪ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡧࡪࡹࡳࡂࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᨫ"),
  bstack1l11l1l_opy_ (u"ࠨ࡫ࡱࡸࡪࡸࡋࡦࡻࡇࡩࡱࡧࡹࠨᨬ"),
  bstack1l11l1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡉࡐࡕࡏࡳ࡬࠭ᨭ"),
  bstack1l11l1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡗࡹࡸࡡࡵࡧࡪࡽࠬᨮ"),
  bstack1l11l1l_opy_ (u"ࠫࡼ࡫ࡢ࡬࡫ࡷࡖࡪࡹࡰࡰࡰࡶࡩ࡙࡯࡭ࡦࡱࡸࡸࠬᨯ"), bstack1l11l1l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵ࡙ࡤ࡭ࡹ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᨰ"),
  bstack1l11l1l_opy_ (u"࠭ࡲࡦ࡯ࡲࡸࡪࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࠩᨱ"),
  bstack1l11l1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡴࡻࡱࡧࡊࡾࡥࡤࡷࡷࡩࡋࡸ࡯࡮ࡊࡷࡸࡵࡹࠧᨲ"),
  bstack1l11l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡅࡤࡴࡹࡻࡲࡦࠩᨳ"),
  bstack1l11l1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩᨴ"),
  bstack1l11l1l_opy_ (u"ࠪࡪࡺࡲ࡬ࡄࡱࡱࡸࡪࡾࡴࡍ࡫ࡶࡸࠬᨵ"),
  bstack1l11l1l_opy_ (u"ࠫࡼࡧࡩࡵࡈࡲࡶࡆࡶࡰࡔࡥࡵ࡭ࡵࡺࠧᨶ"),
  bstack1l11l1l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼࡉ࡯࡯ࡰࡨࡧࡹࡘࡥࡵࡴ࡬ࡩࡸ࠭ᨷ"),
  bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࡑࡥࡲ࡫ࠧᨸ"),
  bstack1l11l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡔࡎࡆࡩࡷࡺࠧᨹ"),
  bstack1l11l1l_opy_ (u"ࠨࡶࡤࡴ࡜࡯ࡴࡩࡕ࡫ࡳࡷࡺࡐࡳࡧࡶࡷࡉࡻࡲࡢࡶ࡬ࡳࡳ࠭ᨺ"),
  bstack1l11l1l_opy_ (u"ࠩࡶࡧࡦࡲࡥࡇࡣࡦࡸࡴࡸࠧᨻ"),
  bstack1l11l1l_opy_ (u"ࠪࡻࡩࡧࡌࡰࡥࡤࡰࡕࡵࡲࡵࠩᨼ"),
  bstack1l11l1l_opy_ (u"ࠫࡸ࡮࡯ࡸ࡚ࡦࡳࡩ࡫ࡌࡰࡩࠪᨽ"),
  bstack1l11l1l_opy_ (u"ࠬ࡯࡯ࡴࡋࡱࡷࡹࡧ࡬࡭ࡒࡤࡹࡸ࡫ࠧᨾ"),
  bstack1l11l1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠨᨿ"),
  bstack1l11l1l_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡷࡸࡽ࡯ࡳࡦࠪᩀ"),
  bstack1l11l1l_opy_ (u"ࠨࡷࡶࡩࡕࡸࡥࡣࡷ࡬ࡰࡹ࡝ࡄࡂࠩᩁ"),
  bstack1l11l1l_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶ࡚ࡈࡆࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠪᩂ"),
  bstack1l11l1l_opy_ (u"ࠪࡻࡪࡨࡄࡳ࡫ࡹࡩࡷࡇࡧࡦࡰࡷ࡙ࡷࡲࠧᩃ"),
  bstack1l11l1l_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡵࡪࠪᩄ"),
  bstack1l11l1l_opy_ (u"ࠬࡻࡳࡦࡐࡨࡻ࡜ࡊࡁࠨᩅ"),
  bstack1l11l1l_opy_ (u"࠭ࡷࡥࡣࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩᩆ"), bstack1l11l1l_opy_ (u"ࠧࡸࡦࡤࡇࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡔࡪ࡯ࡨࡳࡺࡺࠧᩇ"),
  bstack1l11l1l_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡏࡳࡩࡌࡨࠬᩈ"), bstack1l11l1l_opy_ (u"ࠩࡻࡧࡴࡪࡥࡔ࡫ࡪࡲ࡮ࡴࡧࡊࡦࠪᩉ"),
  bstack1l11l1l_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧ࡛ࡉࡇࡂࡶࡰࡧࡰࡪࡏࡤࠨᩊ"),
  bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡳࡦࡶࡒࡲࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡳࡶࡒࡲࡱࡿࠧᩋ"),
  bstack1l11l1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࡚ࡩ࡮ࡧࡲࡹࡹࡹࠧᩌ"),
  bstack1l11l1l_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡩࡦࡵࠪᩍ"), bstack1l11l1l_opy_ (u"ࠧࡸࡦࡤࡗࡹࡧࡲࡵࡷࡳࡖࡪࡺࡲࡺࡋࡱࡸࡪࡸࡶࡢ࡮ࠪᩎ"),
  bstack1l11l1l_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࡊࡤࡶࡩࡽࡡࡳࡧࡎࡩࡾࡨ࡯ࡢࡴࡧࠫᩏ"),
  bstack1l11l1l_opy_ (u"ࠩࡰࡥࡽ࡚ࡹࡱ࡫ࡱ࡫ࡋࡸࡥࡲࡷࡨࡲࡨࡿࠧᩐ"),
  bstack1l11l1l_opy_ (u"ࠪࡷ࡮ࡳࡰ࡭ࡧࡌࡷ࡛࡯ࡳࡪࡤ࡯ࡩࡈ࡮ࡥࡤ࡭ࠪᩑ"),
  bstack1l11l1l_opy_ (u"ࠫࡺࡹࡥࡄࡣࡵࡸ࡭ࡧࡧࡦࡕࡶࡰࠬᩒ"),
  bstack1l11l1l_opy_ (u"ࠬࡹࡨࡰࡷ࡯ࡨ࡚ࡹࡥࡔ࡫ࡱ࡫ࡱ࡫ࡴࡰࡰࡗࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡸࠧᩓ"),
  bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡎ࡝ࡄࡑࠩᩔ"),
  bstack1l11l1l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼ࡚࡯ࡶࡥ࡫ࡍࡩࡋ࡮ࡳࡱ࡯ࡰࠬᩕ"),
  bstack1l11l1l_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡉ࡫ࡧࡨࡪࡴࡁࡱ࡫ࡓࡳࡱ࡯ࡣࡺࡇࡵࡶࡴࡸࠧᩖ"),
  bstack1l11l1l_opy_ (u"ࠩࡰࡳࡨࡱࡌࡰࡥࡤࡸ࡮ࡵ࡮ࡂࡲࡳࠫᩗ"),
  bstack1l11l1l_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉࡳࡷࡳࡡࡵࠩᩘ"), bstack1l11l1l_opy_ (u"ࠫࡱࡵࡧࡤࡣࡷࡊ࡮ࡲࡴࡦࡴࡖࡴࡪࡩࡳࠨᩙ"),
  bstack1l11l1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡈࡪࡲࡡࡺࡃࡧࡦࠬᩚ"),
  bstack1l11l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡉࡥࡎࡲࡧࡦࡺ࡯ࡳࡃࡸࡸࡴࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠩᩛ")
]
bstack1lll1l111l_opy_ = bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡵࡱ࡮ࡲࡥࡩ࠭ᩜ")
bstack11l1ll1l1_opy_ = [bstack1l11l1l_opy_ (u"ࠨ࠰ࡤࡴࡰ࠭ᩝ"), bstack1l11l1l_opy_ (u"ࠩ࠱ࡥࡦࡨࠧᩞ"), bstack1l11l1l_opy_ (u"ࠪ࠲࡮ࡶࡡࠨ᩟")]
bstack1ll11ll1_opy_ = [bstack1l11l1l_opy_ (u"ࠫ࡮ࡪ᩠ࠧ"), bstack1l11l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪᩡ"), bstack1l11l1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩᩢ"), bstack1l11l1l_opy_ (u"ࠧࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩ࠭ᩣ")]
bstack1llllllll1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᩤ"): bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩥ"),
  bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫᩦ"): bstack1l11l1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩧ"),
  bstack1l11l1l_opy_ (u"ࠬ࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩨ"): bstack1l11l1l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩩ"),
  bstack1l11l1l_opy_ (u"ࠧࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩪ"): bstack1l11l1l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩫ"),
  bstack1l11l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩬ"): bstack1l11l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫᩭ")
}
bstack1l1l1ll111_opy_ = [
  bstack1l11l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᩮ"),
  bstack1l11l1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᩯ"),
  bstack1l11l1l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩰ"),
  bstack1l11l1l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᩱ"),
  bstack1l11l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᩲ"),
]
bstack11l111llll_opy_ = bstack11l1ll1lll_opy_ + bstack11l1l111ll1_opy_ + bstack1111lllll_opy_
bstack1ll1l1l1_opy_ = [
  bstack1l11l1l_opy_ (u"ࠩࡡࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࠪࠧᩳ"),
  bstack1l11l1l_opy_ (u"ࠪࡢࡧࡹ࠭࡭ࡱࡦࡥࡱ࠴ࡣࡰ࡯ࠧࠫᩴ"),
  bstack1l11l1l_opy_ (u"ࠫࡣ࠷࠲࠸࠰ࠪ᩵"),
  bstack1l11l1l_opy_ (u"ࠬࡤ࠱࠱࠰ࠪ᩶"),
  bstack1l11l1l_opy_ (u"࠭࡞࠲࠹࠵࠲࠶ࡡ࠶࠮࠻ࡠ࠲ࠬ᩷"),
  bstack1l11l1l_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠸࡛࠱࠯࠼ࡡ࠳࠭᩸"),
  bstack1l11l1l_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠳࡜࠲࠰࠵ࡢ࠴ࠧ᩹"),
  bstack1l11l1l_opy_ (u"ࠩࡡ࠵࠾࠸࠮࠲࠸࠻࠲ࠬ᩺")
]
bstack11l1ll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᩻")
bstack11ll11l111_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠰ࡸ࠴࠳ࡪࡼࡥ࡯ࡶࠪ᩼")
bstack1l1ll1ll_opy_ = [ bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᩽") ]
bstack1l1l11l11l_opy_ = [ bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᩾") ]
bstack1l1l11ll_opy_ = [bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨ᩿ࠫ")]
bstack1lll1111ll_opy_ = [ bstack1l11l1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᪀") ]
bstack1l1l1111l1_opy_ = bstack1l11l1l_opy_ (u"ࠩࡖࡈࡐ࡙ࡥࡵࡷࡳࠫ᪁")
bstack111lll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠪࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩ࠭᪂")
bstack1ll111l1l1_opy_ = bstack1l11l1l_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠨ᪃")
bstack1l11lll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࠫ᪄")
bstack1l11lll1l1_opy_ = [
  bstack1l11l1l_opy_ (u"࠭ࡅࡓࡔࡢࡊࡆࡏࡌࡆࡆࠪ᪅"),
  bstack1l11l1l_opy_ (u"ࠧࡆࡔࡕࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧ᪆"),
  bstack1l11l1l_opy_ (u"ࠨࡇࡕࡖࡤࡈࡌࡐࡅࡎࡉࡉࡥࡂ࡚ࡡࡆࡐࡎࡋࡎࡕࠩ᪇"),
  bstack1l11l1l_opy_ (u"ࠩࡈࡖࡗࡥࡎࡆࡖ࡚ࡓࡗࡑ࡟ࡄࡊࡄࡒࡌࡋࡄࠨ᪈"),
  bstack1l11l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡊ࡚࡟ࡏࡑࡗࡣࡈࡕࡎࡏࡇࡆࡘࡊࡊࠧ᪉"),
  bstack1l11l1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡉࡌࡐࡕࡈࡈࠬ᪊"),
  bstack1l11l1l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡕࡈࡘࠬ᪋"),
  bstack1l11l1l_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡓࡇࡉ࡙ࡘࡋࡄࠨ᪌"),
  bstack1l11l1l_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡃࡅࡓࡗ࡚ࡅࡅࠩ᪍"),
  bstack1l11l1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ᪎"),
  bstack1l11l1l_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡓࡕࡔࡠࡔࡈࡗࡔࡒࡖࡆࡆࠪ᪏"),
  bstack1l11l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࡠࡋࡑ࡚ࡆࡒࡉࡅࠩ᪐"),
  bstack1l11l1l_opy_ (u"ࠫࡊࡘࡒࡠࡃࡇࡈࡗࡋࡓࡔࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧ᪑"),
  bstack1l11l1l_opy_ (u"ࠬࡋࡒࡓࡡࡗ࡙ࡓࡔࡅࡍࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭᪒"),
  bstack1l11l1l_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪ᪓"),
  bstack1l11l1l_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡕࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ᪔"),
  bstack1l11l1l_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡖࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡊࡒࡗ࡙ࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫ᪕"),
  bstack1l11l1l_opy_ (u"ࠩࡈࡖࡗࡥࡐࡓࡑ࡛࡝ࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩ᪖"),
  bstack1l11l1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡏࡃࡐࡉࡤࡔࡏࡕࡡࡕࡉࡘࡕࡌࡗࡇࡇࠫ᪗"),
  bstack1l11l1l_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡒࡆࡕࡒࡐ࡚࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪ᪘"),
  bstack1l11l1l_opy_ (u"ࠬࡋࡒࡓࡡࡐࡅࡓࡊࡁࡕࡑࡕ࡝ࡤࡖࡒࡐ࡚࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫ᪙"),
]
bstack1l111111l_opy_ = bstack1l11l1l_opy_ (u"࠭࠮࠰ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࠲ࠫ᪚")
bstack1l1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠧࡿࠩ᪛")), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᪜"), bstack1l11l1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ᪝"))
bstack11l1llll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡲ࡬ࠫ᪞")
bstack11l11lllll1_opy_ = [ bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᪟"), bstack1l11l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ᪠"), bstack1l11l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ᪡"), bstack1l11l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ᪢")]
bstack1l1l11ll11_opy_ = [ bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᪣"), bstack1l11l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᪤"), bstack1l11l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ᪥"), bstack1l11l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᪦") ]
bstack1l11l11l1l_opy_ = [ bstack1l11l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᪧ") ]
bstack11l11llllll_opy_ = [ bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᪨") ]
bstack11ll1111_opy_ = 360
bstack11l1ll1l1l1_opy_ = bstack1l11l1l_opy_ (u"ࠢࡢࡲࡳ࠱ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢ᪩")
bstack11l11ll1ll1_opy_ = bstack1l11l1l_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲࡭ࡸࡹࡵࡦࡵࠥ᪪")
bstack11l1l1l111l_opy_ = bstack1l11l1l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠧ᪫")
bstack11ll11ll111_opy_ = bstack1l11l1l_opy_ (u"ࠥࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡹ࡫ࡳࡵࡵࠣࡥࡷ࡫ࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡏࡔࠢࡹࡩࡷࡹࡩࡰࡰࠣࠩࡸࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦࠢࡩࡳࡷࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠࡥࡧࡹ࡭ࡨ࡫ࡳ࠯ࠤ᪬")
bstack11l1lllll1l_opy_ = bstack1l11l1l_opy_ (u"ࠦ࠶࠷࠮࠱ࠤ᪭")
bstack1111ll111l_opy_ = {
  bstack1l11l1l_opy_ (u"ࠬࡖࡁࡔࡕࠪ᪮"): bstack1l11l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᪯"),
  bstack1l11l1l_opy_ (u"ࠧࡇࡃࡌࡐࠬ᪰"): bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᪱"),
  bstack1l11l1l_opy_ (u"ࠩࡖࡏࡎࡖࠧ᪲"): bstack1l11l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᪳")
}
bstack1l1ll111ll_opy_ = [
  bstack1l11l1l_opy_ (u"ࠦ࡬࡫ࡴࠣ᪴"),
  bstack1l11l1l_opy_ (u"ࠧ࡭࡯ࡃࡣࡦ࡯᪵ࠧ"),
  bstack1l11l1l_opy_ (u"ࠨࡧࡰࡈࡲࡶࡼࡧࡲࡥࠤ᪶"),
  bstack1l11l1l_opy_ (u"ࠢࡳࡧࡩࡶࡪࡹࡨ᪷ࠣ"),
  bstack1l11l1l_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺ᪸ࠢ"),
  bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᪹"),
  bstack1l11l1l_opy_ (u"ࠥࡷࡺࡨ࡭ࡪࡶࡈࡰࡪࡳࡥ࡯ࡶ᪺ࠥ"),
  bstack1l11l1l_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡆ࡮ࡨࡱࡪࡴࡴࠣ᪻"),
  bstack1l11l1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ᪼"),
  bstack1l11l1l_opy_ (u"ࠨࡣ࡭ࡧࡤࡶࡊࡲࡥ࡮ࡧࡱࡸ᪽ࠧ"),
  bstack1l11l1l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࡳࠣ᪾"),
  bstack1l11l1l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࡕࡦࡶ࡮ࡶࡴᪿࠣ"),
  bstack1l11l1l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࡄࡷࡾࡴࡣࡔࡥࡵ࡭ࡵࡺᫀࠢ"),
  bstack1l11l1l_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤ᫁"),
  bstack1l11l1l_opy_ (u"ࠦࡶࡻࡩࡵࠤ᫂"),
  bstack1l11l1l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲ࡚࡯ࡶࡥ࡫ࡅࡨࡺࡩࡰࡰ᫃ࠥ"),
  bstack1l11l1l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳࡍࡶ࡮ࡷ࡭࡙ࡵࡵࡤࡪ᫄ࠥ"),
  bstack1l11l1l_opy_ (u"ࠢࡴࡪࡤ࡯ࡪࠨ᫅"),
  bstack1l11l1l_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࡁࡱࡲࠥ᫆")
]
bstack11l1l11111l_opy_ = [
  bstack1l11l1l_opy_ (u"ࠤࡦࡰ࡮ࡩ࡫ࠣ᫇"),
  bstack1l11l1l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᫈"),
  bstack1l11l1l_opy_ (u"ࠦࡦࡻࡴࡰࠤ᫉"),
  bstack1l11l1l_opy_ (u"ࠧࡳࡡ࡯ࡷࡤࡰ᫊ࠧ"),
  bstack1l11l1l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ᫋")
]
bstack11l1l1ll_opy_ = {
  bstack1l11l1l_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨᫌ"): [bstack1l11l1l_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢᫍ")],
  bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᫎ"): [bstack1l11l1l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢ᫏")],
  bstack1l11l1l_opy_ (u"ࠦࡦࡻࡴࡰࠤ᫐"): [bstack1l11l1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡇ࡯ࡩࡲ࡫࡮ࡵࠤ᫑"), bstack1l11l1l_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࡕࡱࡄࡧࡹ࡯ࡶࡦࡇ࡯ࡩࡲ࡫࡮ࡵࠤ᫒"), bstack1l11l1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦ᫓"), bstack1l11l1l_opy_ (u"ࠣࡥ࡯࡭ࡨࡱࡅ࡭ࡧࡰࡩࡳࡺࠢ᫔")],
  bstack1l11l1l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤ᫕"): [bstack1l11l1l_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥ᫖")],
  bstack1l11l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᫗"): [bstack1l11l1l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᫘")],
}
bstack11l1l1l11l1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧ᫙"): bstack1l11l1l_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨ᫚"),
  bstack1l11l1l_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧ᫛"): bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᫜"),
  bstack1l11l1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢ᫝"): bstack1l11l1l_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨ᫞"),
  bstack1l11l1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡎࡩࡾࡹࡔࡰࡃࡦࡸ࡮ࡼࡥࡆ࡮ࡨࡱࡪࡴࡴࠣ᫟"): bstack1l11l1l_opy_ (u"ࠨࡳࡦࡰࡧࡏࡪࡿࡳࠣ᫠"),
  bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᫡"): bstack1l11l1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᫢")
}
bstack1111ll11l1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭᫣"): bstack1l11l1l_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡖࡩࡹࡻࡰࠨ᫤"),
  bstack1l11l1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ᫥"): bstack1l11l1l_opy_ (u"࡙ࠬࡵࡪࡶࡨࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭᫦"),
  bstack1l11l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ᫧"): bstack1l11l1l_opy_ (u"ࠧࡕࡧࡶࡸ࡙ࠥࡥࡵࡷࡳࠫ᫨"),
  bstack1l11l1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ᫩"): bstack1l11l1l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡕࡧࡤࡶࡩࡵࡷ࡯ࠩ᫪")
}
bstack11l1l1l11ll_opy_ = 65536
bstack11l1l11l1l1_opy_ = bstack1l11l1l_opy_ (u"ࠪ࠲࠳࠴࡛ࡕࡔࡘࡒࡈࡇࡔࡆࡆࡠࠫ᫫")
bstack11l11ll11l1_opy_ = [
      bstack1l11l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᫬"), bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᫭"), bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᫮"), bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ᫯"), bstack1l11l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪ᫰"),
      bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ᫱"), bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭᫲"), bstack1l11l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬ᫳"), bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭᫴"),
      bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᫵"), bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᫶"), bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ᫷")
    ]
bstack11l1l11l11l_opy_= {
  bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᫸"): bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᫹"),
  bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ᫺"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫻"),
  bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ᫼"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ᫽"),
  bstack1l11l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᫾"): bstack1l11l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᫿"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᬀ"): bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᬁ"),
  bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᬂ"): bstack1l11l1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᬃ"),
  bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᬄ"): bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᬅ"),
  bstack1l11l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᬆ"): bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᬇ"),
  bstack1l11l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᬈ"): bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᬉ"),
  bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫᬊ"): bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬᬋ"),
  bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᬌ"): bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᬍ"),
  bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࡓࡧࡳࡳࡷࡺࡩ࡯ࡩࠪᬎ"): bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫᬏ"),
  bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬐ"): bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᬑ"),
  bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࠧᬒ"): bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࡐࡲࡷ࡭ࡴࡴࡳࠨᬓ"),
  bstack1l11l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫᬔ"): bstack1l11l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬᬕ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᬖ"): bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᬗ"),
  bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᬘ"): bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᬙ"),
  bstack1l11l1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬᬚ"): bstack1l11l1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ᬛ"),
  bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᬜ"): bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᬝ"),
  bstack1l11l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᬞ"): bstack1l11l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬᬟ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᬠ"): bstack1l11l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᬡ"),
  bstack1l11l1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᬢ"): bstack1l11l1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᬣ"),
  bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᬤ"): bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᬥ"),
  bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬦ"): bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᬧ"),
  bstack1l11l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᬨ"): bstack1l11l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᬩ"),
  bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᬪ"): bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᬫ"),
  bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬬ"): bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪᬭ"),
  bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᬮ"): bstack1l11l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᬯ")
}
bstack11l11ll1lll_opy_ = [bstack1l11l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᬰ"), bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᬱ")]
bstack1l11l1l1l1_opy_ = (bstack1l11l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᬲ"),)
bstack11l1l111111_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠱ࡹ࠵࠴ࡻࡰࡥࡣࡷࡩࡤࡩ࡬ࡪࠩᬳ")
bstack1l11ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠯ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠵ࡶ࠲࠱ࡪࡶ࡮ࡪࡳ࠰ࠤ᬴")
bstack111l1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡩࡵ࡭ࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࠨᬵ")
bstack1l1l111l1_opy_ = bstack1l11l1l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠱ࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠤᬶ")
class EVENTS(Enum):
  bstack11l1l1l1l1l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀ࡯࠲࠳ࡼ࠾ࡵࡸࡩ࡯ࡶ࠰ࡦࡺ࡯࡬ࡥ࡮࡬ࡲࡰ࠭ᬷ")
  bstack1l11l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮ࡨࡥࡳࡻࡰࠨᬸ") # final bstack11l1l11ll11_opy_
  bstack11l1l11l111_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡵࡨࡲࡩࡲ࡯ࡨࡵࠪᬹ")
  bstack11l1l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪࡀࡰࡳ࡫ࡱࡸ࠲ࡨࡵࡪ࡮ࡧࡰ࡮ࡴ࡫ࠨᬺ") #shift post bstack11l1l11llll_opy_
  bstack1lllllllll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡶࡲࡪࡰࡷ࠱ࡧࡻࡩ࡭ࡦ࡯࡭ࡳࡱࠧᬻ") #shift post bstack11l1l11llll_opy_
  bstack11l1l1l1111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡹ࡫ࡳࡵࡪࡸࡦࠬᬼ") #shift
  bstack11l11llll1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡶࡥࡳࡥࡼ࠾ࡩࡵࡷ࡯࡮ࡲࡥࡩ࠭ᬽ") #shift
  bstack1lll111l11_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ࠽࡬ࡺࡨ࠭࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࠫᬾ")
  bstack1l1lll1llll_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࠳࠴ࡽ࠿ࡹࡡࡷࡧ࠰ࡶࡪࡹࡵ࡭ࡶࡶࠫᬿ")
  bstack11l11l11l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡣ࠴࠵ࡾࡀࡤࡳ࡫ࡹࡩࡷ࠳ࡰࡦࡴࡩࡳࡷࡳࡳࡤࡣࡱࠫᭀ")
  bstack11ll1ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡱࡵࡣࡢ࡮ࠪᭁ") #shift
  bstack1llll1l111_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠼ࡤࡴࡵ࠳ࡵࡱ࡮ࡲࡥࡩ࠭ᭂ") #shift
  bstack1l1lll11_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡣࡪ࠯ࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠬᭃ")
  bstack1ll111lll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࠭ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠭ࡳࡧࡶࡹࡱࡺࡳ࠮ࡵࡸࡱࡲࡧࡲࡺ᭄ࠩ") #shift
  bstack111llll11l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡡ࠲࠳ࡼ࠾࡬࡫ࡴ࠮ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠮ࡴࡨࡷࡺࡲࡴࡴࠩᭅ") #shift
  bstack11l1l111l11_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡧࡵࡧࡾ࠭ᭆ") #shift
  bstack1l11lllll11_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡨࡶࡨࡿ࠺ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᭇ")
  bstack11l1l11lll_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠾ࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡹࡴࡢࡶࡸࡷࠬᭈ") #shift
  bstack11ll1lll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿࡮ࡵࡣ࠯ࡰࡥࡳࡧࡧࡦ࡯ࡨࡲࡹ࠭ᭉ")
  bstack11l11lll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡵࡸ࡯ࡹࡻ࠰ࡷࡪࡺࡵࡱࠩᭊ") #shift
  bstack1111111ll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡥࡵࡷࡳࠫᭋ")
  bstack11l11llll11_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡹ࡮ࡢࡲࡶ࡬ࡴࡺࠧᭌ") # not bstack11l11ll1l11_opy_ in python
  bstack1llllll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡲࡷ࡬ࡸࠬ᭍") # used in bstack11l11lll111_opy_
  bstack1ll1l111l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡩࡨࡸࠬ᭎") # used in bstack11l11lll111_opy_
  bstack1l1111l111_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼࡫ࡳࡴࡱࠧ᭏")
  bstack1l111l1ll1_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠿ࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠫ᭐")
  bstack11ll111l11_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࡯ࡤࡸࡪࡀࡳࡦࡵࡶ࡭ࡴࡴ࠭ࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠫ᭑") #
  bstack1l1l11111_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡵ࠱࠲ࡻ࠽ࡨࡷ࡯ࡶࡦࡴ࠰ࡸࡦࡱࡥࡔࡥࡵࡩࡪࡴࡓࡩࡱࡷࠫ᭒")
  bstack111ll1ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡰࡦࡴࡦࡽ࠿ࡧࡵࡵࡱ࠰ࡧࡦࡶࡴࡶࡴࡨࠫ᭓")
  bstack1lll1ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡱࡴࡨ࠱ࡹ࡫ࡳࡵࠩ᭔")
  bstack1l1l1lll1l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡲࡲࡷࡹ࠳ࡴࡦࡵࡷࠫ᭕")
  bstack11l1l11l1_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡶࡪ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧ᭖") #shift
  bstack1l11l11111_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩ᭗") #shift
  bstack11l1l1l1lll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡻࡴࡰ࠯ࡦࡥࡵࡺࡵࡳࡧࠪ᭘")
  bstack11l1l111lll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡫࠺ࡪࡦ࡯ࡩ࠲ࡺࡩ࡮ࡧࡲࡹࡹ࠭᭙")
  bstack1ll1llllll1_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡣ࡭࡫࠽ࡷࡹࡧࡲࡵࠩ᭚")
  bstack11l1l11ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩࡵࡷ࡯࡮ࡲࡥࡩ࠭᭛")
  bstack11l11lll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡩࡨࡦࡥ࡮࠱ࡺࡶࡤࡢࡶࡨࠫ᭜")
  bstack1lll11ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡯࡯࠯ࡥࡳࡴࡺࡳࡵࡴࡤࡴࠬ᭝")
  bstack1ll1ll11lll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡰࡰ࠰ࡧࡴࡴ࡮ࡦࡥࡷࠫ᭞")
  bstack1lll11llll1_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡱࡱ࠱ࡸࡺ࡯ࡱࠩ᭟")
  bstack1lll11l11l1_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡹࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠧ᭠")
  bstack1lll11ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡣࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰࠪ᭡")
  bstack11l11ll11ll_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠫ᭢")
  bstack11l1l1111l1_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡨ࡬ࡲࡩࡔࡥࡢࡴࡨࡷࡹࡎࡵࡣࠩ᭣")
  bstack1l11l1111ll_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡊࡰ࡬ࡸࠬ᭤")
  bstack1l11l11llll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡷࡺࠧ᭥")
  bstack1ll11111111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡇࡴࡴࡦࡪࡩࠪ᭦")
  bstack11l11lll11l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡈࡵ࡮ࡧ࡫ࡪࠫ᭧")
  bstack1l1ll1ll111_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀࡡࡪࡕࡨࡰ࡫ࡎࡥࡢ࡮ࡖࡸࡪࡶࠧ᭨")
  bstack1l1ll1lllll_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࠺ࡢ࡫ࡖࡩࡱ࡬ࡈࡦࡣ࡯ࡋࡪࡺࡒࡦࡵࡸࡰࡹ࠭᭩")
  bstack1l1l111ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫࠻ࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡆࡸࡨࡲࡹ࠭᭪")
  bstack1l1ll111lll_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬࠼ࡷࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠬ᭫")
  bstack1l1l111lll1_opy_ = bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࠽ࡧࡱ࡯࠺࡭ࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࡉࡻ࡫࡮ࡵ᭬ࠩ")
  bstack11l1l1ll111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡧࡱࡵࡺ࡫ࡵࡦࡖࡨࡷࡹࡋࡶࡦࡰࡷࠫ᭭")
  bstack1l111llllll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠿ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡵࡰࠨ᭮")
  bstack1ll1l11111l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡀ࡯࡯ࡕࡷࡳࡵ࠭᭯")
class STAGE(Enum):
  bstack11l1l1lll1_opy_ = bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ᭰")
  END = bstack1l11l1l_opy_ (u"ࠫࡪࡴࡤࠨ᭱")
  bstack11l1llllll_opy_ = bstack1l11l1l_opy_ (u"ࠬࡹࡩ࡯ࡩ࡯ࡩࠬ᭲")
bstack11l111111_opy_ = {
  bstack1l11l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭᭳"): bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᭴"),
  bstack1l11l1l_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ᭵"): bstack1l11l1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ᭶")
}
PLAYWRIGHT_HUB_URL = bstack1l11l1l_opy_ (u"ࠥࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠧ᭷")
bstack1ll111lllll_opy_ = 98
bstack1l1lll1l111_opy_ = 100
bstack1llllll1ll1_opy_ = {
  bstack1l11l1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪ᭸"): bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡳࡧࡵࡹࡳࡹࠧ᭹"),
  bstack1l11l1l_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬ᭺"): bstack1l11l1l_opy_ (u"ࠧ࠮࠯ࡵࡩࡷࡻ࡮ࡴ࠯ࡧࡩࡱࡧࡹࠨ᭻"),
  bstack1l11l1l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ࠭᭼"): 0
}
bstack11l1l111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ᭽")
bstack11l1l1l1ll1_opy_ = bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢ᭾")
bstack11l1lll1l_opy_ = bstack1l11l1l_opy_ (u"࡙ࠦࡋࡓࡕࠢࡕࡉࡕࡕࡒࡕࡋࡑࡋࠥࡇࡎࡅࠢࡄࡒࡆࡒ࡙ࡕࡋࡆࡗࠧ᭿")