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
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll11l111l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1111lll_opy_ as bstack11l1llll111_opy_, EVENTS
from bstack_utils.bstack1l111l1l_opy_ import bstack1l111l1l_opy_
from bstack_utils.helper import bstack11llll1111_opy_, bstack1111l1l1ll_opy_, bstack11lll1lll_opy_, bstack11l1ll1llll_opy_, \
  bstack11l1llll1l1_opy_, bstack11lll11l1_opy_, get_host_info, bstack11ll11111ll_opy_, bstack11l1l1l1l_opy_, error_handler, bstack11l1lll11l1_opy_, bstack11ll111l111_opy_, bstack1l1l1l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1ll11ll1ll1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import bstack1ll1lll11_opy_
logger = get_logger(__name__)
bstack1l1111ll1_opy_ = bstack1ll1lll11_opy_.bstack1l11llll1l_opy_(__name__)
bstack11lll1l1ll_opy_ = bstack1ll11ll1ll1_opy_()
@error_handler(class_method=False)
def _11ll111llll_opy_(driver, bstack1lllll1l11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l111l1_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᛎ"): caps.get(bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᛏ"), None),
        bstack1l111l1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᛐ"): bstack1lllll1l11l_opy_.get(bstack1l111l1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᛑ"), None),
        bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᛒ"): caps.get(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᛓ"), None),
        bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᛔ"): caps.get(bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛕ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᛖ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᛗ"), None) is None or os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᛘ")] == bstack1l111l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛙ"):
        return False
    return True
def bstack11ll1lll1l_opy_(config):
  return config.get(bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᛚ"), False) or any([p.get(bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᛛ"), False) == True for p in config.get(bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᛜ"), [])])
def bstack1l1llllll1_opy_(config, bstack1l1l11111l_opy_):
  try:
    bstack11ll11l1111_opy_ = config.get(bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛝ"), False)
    if int(bstack1l1l11111l_opy_) < len(config.get(bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᛞ"), [])) and config[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᛟ")][bstack1l1l11111l_opy_]:
      bstack11l1ll1ll1l_opy_ = config[bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᛠ")][bstack1l1l11111l_opy_].get(bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᛡ"), None)
    else:
      bstack11l1ll1ll1l_opy_ = config.get(bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᛢ"), None)
    if bstack11l1ll1ll1l_opy_ != None:
      bstack11ll11l1111_opy_ = bstack11l1ll1ll1l_opy_
    bstack11ll1111l11_opy_ = os.getenv(bstack1l111l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᛣ")) is not None and len(os.getenv(bstack1l111l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᛤ"))) > 0 and os.getenv(bstack1l111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᛥ")) != bstack1l111l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛦ")
    return bstack11ll11l1111_opy_ and bstack11ll1111l11_opy_
  except Exception as error:
    logger.debug(bstack1l111l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᛧ") + str(error))
  return False
def bstack11l1l11111_opy_(test_tags):
  bstack1l1ll1lllll_opy_ = os.getenv(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᛨ"))
  if bstack1l1ll1lllll_opy_ is None:
    return True
  bstack1l1ll1lllll_opy_ = json.loads(bstack1l1ll1lllll_opy_)
  try:
    include_tags = bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᛩ")] if bstack1l111l1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᛪ") in bstack1l1ll1lllll_opy_ and isinstance(bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᛫")], list) else []
    exclude_tags = bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᛬")] if bstack1l111l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᛭") in bstack1l1ll1lllll_opy_ and isinstance(bstack1l1ll1lllll_opy_[bstack1l111l1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᛮ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᛯ") + str(error))
  return False
def bstack11l1lll11ll_opy_(config, bstack11ll111ll1l_opy_, bstack11l1ll1l11l_opy_, bstack11l1llll11l_opy_):
  bstack11l1llll1ll_opy_ = bstack11l1ll1llll_opy_(config)
  bstack11ll1111ll1_opy_ = bstack11l1llll1l1_opy_(config)
  if bstack11l1llll1ll_opy_ is None or bstack11ll1111ll1_opy_ is None:
    logger.error(bstack1l111l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᛰ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᛱ"), bstack1l111l1_opy_ (u"ࠨࡽࢀࠫᛲ")))
    data = {
        bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᛳ"): config[bstack1l111l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᛴ")],
        bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᛵ"): config.get(bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᛶ"), os.path.basename(os.getcwd())),
        bstack1l111l1_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᛷ"): bstack11llll1111_opy_(),
        bstack1l111l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᛸ"): config.get(bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᛹"), bstack1l111l1_opy_ (u"ࠩࠪ᛺")),
        bstack1l111l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ᛻"): {
            bstack1l111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ᛼"): bstack11ll111ll1l_opy_,
            bstack1l111l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᛽"): bstack11l1ll1l11l_opy_,
            bstack1l111l1_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ᛾"): __version__,
            bstack1l111l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ᛿"): bstack1l111l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᜀ"),
            bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᜁ"): bstack1l111l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᜂ"),
            bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᜃ"): bstack11l1llll11l_opy_
        },
        bstack1l111l1_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᜄ"): settings,
        bstack1l111l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᜅ"): bstack11ll11111ll_opy_(),
        bstack1l111l1_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᜆ"): bstack11lll11l1_opy_(),
        bstack1l111l1_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᜇ"): get_host_info(),
        bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᜈ"): bstack11lll1lll_opy_(config)
    }
    headers = {
        bstack1l111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᜉ"): bstack1l111l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᜊ"),
    }
    config = {
        bstack1l111l1_opy_ (u"ࠬࡧࡵࡵࡪࠪᜋ"): (bstack11l1llll1ll_opy_, bstack11ll1111ll1_opy_),
        bstack1l111l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᜌ"): headers
    }
    response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠧࡑࡑࡖࡘࠬᜍ"), bstack11l1llll111_opy_ + bstack1l111l1_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᜎ"), data, config)
    bstack11l1lll1111_opy_ = response.json()
    if bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᜏ")]:
      parsed = json.loads(os.getenv(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᜐ"), bstack1l111l1_opy_ (u"ࠫࢀࢃࠧᜑ")))
      parsed[bstack1l111l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜒ")] = bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᜓ")][bstack1l111l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᜔")]
      os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍ᜕ࠩ")] = json.dumps(parsed)
      bstack1l111l1l_opy_.bstack11l111ll11_opy_(bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠩࡧࡥࡹࡧࠧ᜖")][bstack1l111l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᜗")])
      bstack1l111l1l_opy_.bstack11l1lll1lll_opy_(bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠫࡩࡧࡴࡢࠩ᜘")][bstack1l111l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ᜙")])
      bstack1l111l1l_opy_.store()
      return bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡢࡶࡤࠫ᜚")][bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ᜛")], bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠨࡦࡤࡸࡦ࠭᜜")][bstack1l111l1_opy_ (u"ࠩ࡬ࡨࠬ᜝")]
    else:
      logger.error(bstack1l111l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫ᜞") + bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᜟ")])
      if bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᜠ")] == bstack1l111l1_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᜡ"):
        for bstack11ll111ll11_opy_ in bstack11l1lll1111_opy_[bstack1l111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᜢ")]:
          logger.error(bstack11ll111ll11_opy_[bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᜣ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᜤ") +  str(error))
    return None, None
def bstack11ll11l11ll_opy_():
  if os.getenv(bstack1l111l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᜥ")) is None:
    return {
        bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᜦ"): bstack1l111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᜧ"),
        bstack1l111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜨ"): bstack1l111l1_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᜩ")
    }
  data = {bstack1l111l1_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᜪ"): bstack11llll1111_opy_()}
  headers = {
      bstack1l111l1_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᜫ"): bstack1l111l1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᜬ") + os.getenv(bstack1l111l1_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᜭ")),
      bstack1l111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᜮ"): bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᜯ")
  }
  response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠧࡑࡗࡗࠫᜰ"), bstack11l1llll111_opy_ + bstack1l111l1_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᜱ"), data, { bstack1l111l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᜲ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l111l1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᜳ") + bstack1111l1l1ll_opy_().isoformat() + bstack1l111l1_opy_ (u"ࠫ࡟᜴࠭"))
      return {bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ᜵"): bstack1l111l1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ᜶"), bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᜷"): bstack1l111l1_opy_ (u"ࠨࠩ᜸")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧ᜹") + str(error))
    return {
        bstack1l111l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᜺"): bstack1l111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᜻"),
        bstack1l111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᜼"): str(error)
    }
def bstack11ll1111111_opy_(bstack11l1lll1l11_opy_):
    return re.match(bstack1l111l1_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧ᜽"), bstack11l1lll1l11_opy_.strip()) is not None
def bstack11l11llll_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l1lll1l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l1lll1l1l_opy_ = desired_capabilities
        else:
          bstack11l1lll1l1l_opy_ = {}
        bstack1ll1111l1ll_opy_ = (bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᜾"), bstack1l111l1_opy_ (u"ࠨࠩ᜿")).lower() or caps.get(bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᝀ"), bstack1l111l1_opy_ (u"ࠪࠫᝁ")).lower())
        if bstack1ll1111l1ll_opy_ == bstack1l111l1_opy_ (u"ࠫ࡮ࡵࡳࠨᝂ"):
            return True
        if bstack1ll1111l1ll_opy_ == bstack1l111l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᝃ"):
            bstack1ll111l1111_opy_ = str(float(caps.get(bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᝄ")) or bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᝅ"), {}).get(bstack1l111l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᝆ"),bstack1l111l1_opy_ (u"ࠩࠪᝇ"))))
            if bstack1ll1111l1ll_opy_ == bstack1l111l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᝈ") and int(bstack1ll111l1111_opy_.split(bstack1l111l1_opy_ (u"ࠫ࠳࠭ᝉ"))[0]) < float(bstack11ll111l1ll_opy_):
                logger.warning(str(bstack11l1ll1l1ll_opy_))
                return False
            return True
        bstack1l1lll1ll1l_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᝊ"), {}).get(bstack1l111l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᝋ"), caps.get(bstack1l111l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᝌ"), bstack1l111l1_opy_ (u"ࠨࠩᝍ")))
        if bstack1l1lll1ll1l_opy_:
            logger.warning(bstack1l111l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᝎ"))
            return False
        browser = caps.get(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᝏ"), bstack1l111l1_opy_ (u"ࠫࠬᝐ")).lower() or bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᝑ"), bstack1l111l1_opy_ (u"࠭ࠧᝒ")).lower()
        if browser != bstack1l111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᝓ"):
            logger.warning(bstack1l111l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ᝔"))
            return False
        browser_version = caps.get(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᝕")) or caps.get(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᝖")) or bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᝗")) or bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᝘"), {}).get(bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᝙")) or bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᝚"), {}).get(bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᝛"))
        bstack1l1lll11111_opy_ = bstack11ll11l111l_opy_.bstack1ll111lllll_opy_
        bstack11ll111l1l1_opy_ = False
        if config is not None:
          bstack11ll111l1l1_opy_ = bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᝜") in config and str(config[bstack1l111l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᝝")]).lower() != bstack1l111l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ᝞")
        if os.environ.get(bstack1l111l1_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᝟"), bstack1l111l1_opy_ (u"࠭ࠧᝠ")).lower() == bstack1l111l1_opy_ (u"ࠧࡵࡴࡸࡩࠬᝡ") or bstack11ll111l1l1_opy_:
          bstack1l1lll11111_opy_ = bstack11ll11l111l_opy_.bstack1ll1111lll1_opy_
        if browser_version and browser_version != bstack1l111l1_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᝢ") and int(browser_version.split(bstack1l111l1_opy_ (u"ࠩ࠱ࠫᝣ"))[0]) <= bstack1l1lll11111_opy_:
          logger.warning(bstack1ll1ll1111l_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭ᝤ"))
          return False
        if not options:
          bstack1l1llllll11_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᝥ")) or bstack11l1lll1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᝦ"), {})
          if bstack1l111l1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᝧ") in bstack1l1llllll11_opy_.get(bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬᝨ"), []):
              logger.warning(bstack1l111l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᝩ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᝪ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1lll11ll_opy_ = config.get(bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᝫ"), {})
    bstack1ll1lll11ll_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᝬ")] = os.getenv(bstack1l111l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᝭"))
    bstack11l1lllll11_opy_ = json.loads(os.getenv(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᝮ"), bstack1l111l1_opy_ (u"ࠧࡼࡿࠪᝯ"))).get(bstack1l111l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᝰ"))
    if not config[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᝱")].get(bstack1l111l1_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᝲ")):
      if bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᝳ") in caps:
        caps[bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᝴")][bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᝵")] = bstack1ll1lll11ll_opy_
        caps[bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᝶")][bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᝷")][bstack1l111l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᝸")] = bstack11l1lllll11_opy_
      else:
        caps[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᝹")] = bstack1ll1lll11ll_opy_
        caps[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᝺")][bstack1l111l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᝻")] = bstack11l1lllll11_opy_
  except Exception as error:
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢ᝼") +  str(error))
def bstack111l1ll1l_opy_(driver, bstack11l1lllllll_opy_):
  try:
    setattr(driver, bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ᝽"), True)
    session = driver.session_id
    if session:
      bstack11ll111lll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll111lll1_opy_ = False
      bstack11ll111lll1_opy_ = url.scheme in [bstack1l111l1_opy_ (u"ࠣࡪࡷࡸࡵࠨ᝾"), bstack1l111l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᝿")]
      if bstack11ll111lll1_opy_:
        if bstack11l1lllllll_opy_:
          logger.info(bstack1l111l1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥក"))
      return bstack11l1lllllll_opy_
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢខ") + str(e))
    return False
def bstack1lll1l1l_opy_(driver, name, path):
  try:
    bstack1l1lll1l1l1_opy_ = {
        bstack1l111l1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬគ"): threading.current_thread().current_test_uuid,
        bstack1l111l1_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫឃ"): os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬង"), bstack1l111l1_opy_ (u"ࠨࠩច")),
        bstack1l111l1_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ឆ"): os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧជ"), bstack1l111l1_opy_ (u"ࠫࠬឈ"))
    }
    bstack1ll111ll11l_opy_ = bstack11lll1l1ll_opy_.bstack1ll1111l1l1_opy_(EVENTS.bstack11ll111111_opy_.value)
    logger.debug(bstack1l111l1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨញ"))
    try:
      if (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ដ"), None) and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩឋ"), None)):
        scripts = {bstack1l111l1_opy_ (u"ࠨࡵࡦࡥࡳ࠭ឌ"): bstack1l111l1l_opy_.perform_scan}
        bstack11l1lll1ll1_opy_ = json.loads(scripts[bstack1l111l1_opy_ (u"ࠤࡶࡧࡦࡴࠢឍ")].replace(bstack1l111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨណ"), bstack1l111l1_opy_ (u"ࠦࠧត")))
        bstack11l1lll1ll1_opy_[bstack1l111l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨថ")][bstack1l111l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ទ")] = None
        scripts[bstack1l111l1_opy_ (u"ࠢࡴࡥࡤࡲࠧធ")] = bstack1l111l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦន") + json.dumps(bstack11l1lll1ll1_opy_)
        bstack1l111l1l_opy_.bstack11l111ll11_opy_(scripts)
        bstack1l111l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1l111l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111l1l_opy_.perform_scan, {bstack1l111l1_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤប"): name}))
      bstack11lll1l1ll_opy_.end(EVENTS.bstack11ll111111_opy_.value, bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥផ"), bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤព"), True, None)
    except Exception as error:
      bstack11lll1l1ll_opy_.end(EVENTS.bstack11ll111111_opy_.value, bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧភ"), bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦម"), False, str(error))
    bstack1ll111ll11l_opy_ = bstack11lll1l1ll_opy_.bstack11ll1111l1l_opy_(EVENTS.bstack1l1lllll1ll_opy_.value)
    bstack11lll1l1ll_opy_.mark(bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢយ"))
    try:
      if (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨរ"), None) and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫល"), None)):
        scripts = {bstack1l111l1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨវ"): bstack1l111l1l_opy_.perform_scan}
        bstack11l1lll1ll1_opy_ = json.loads(scripts[bstack1l111l1_opy_ (u"ࠦࡸࡩࡡ࡯ࠤឝ")].replace(bstack1l111l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣឞ"), bstack1l111l1_opy_ (u"ࠨࠢស")))
        bstack11l1lll1ll1_opy_[bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪហ")][bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨឡ")] = None
        scripts[bstack1l111l1_opy_ (u"ࠤࡶࡧࡦࡴࠢអ")] = bstack1l111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨឣ") + json.dumps(bstack11l1lll1ll1_opy_)
        bstack1l111l1l_opy_.bstack11l111ll11_opy_(scripts)
        bstack1l111l1l_opy_.store()
        logger.debug(driver.execute_script(bstack1l111l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111l1l_opy_.bstack11ll11l11l1_opy_, bstack1l1lll1l1l1_opy_))
      bstack11lll1l1ll_opy_.end(bstack1ll111ll11l_opy_, bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦឤ"), bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥឥ"),True, None)
    except Exception as error:
      bstack11lll1l1ll_opy_.end(bstack1ll111ll11l_opy_, bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨឦ"), bstack1ll111ll11l_opy_ + bstack1l111l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧឧ"),False, str(error))
    logger.info(bstack1l111l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦឨ"))
    try:
      bstack1ll111ll1l1_opy_ = {
        bstack1l111l1_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥឩ"): {
          bstack1l111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦឪ"): bstack1l111l1_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣឫ"),
        },
        bstack1l111l1_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢឬ"): {
          bstack1l111l1_opy_ (u"ࠨࡢࡰࡦࡼࠦឭ"): {
            bstack1l111l1_opy_ (u"ࠢ࡮ࡵࡪࠦឮ"): bstack1l111l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦឯ"),
            bstack1l111l1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥឰ"): True
          }
        }
      }
      bstack1l1111ll1_opy_.info(json.dumps(bstack1ll111ll1l1_opy_, separators=(bstack1l111l1_opy_ (u"ࠪ࠰ࠬឱ"), bstack1l111l1_opy_ (u"ࠫ࠿࠭ឲ"))))
    except Exception as bstack1lll11111l_opy_:
      logger.debug(bstack1l111l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦឳ") + str(bstack1lll11111l_opy_) + bstack1l111l1_opy_ (u"ࠨࠢ឴"))
  except Exception as bstack1l1ll1lll11_opy_:
    logger.error(bstack1l111l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤ឵") + str(path) + bstack1l111l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥា") + str(bstack1l1ll1lll11_opy_))
def bstack11ll111111l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l111l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣិ")) and str(caps.get(bstack1l111l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤី"))).lower() == bstack1l111l1_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧឹ"):
        bstack1ll111l1111_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢឺ")) or caps.get(bstack1l111l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣុ"))
        if bstack1ll111l1111_opy_ and int(str(bstack1ll111l1111_opy_)) < bstack11ll111l1ll_opy_:
            return False
    return True
def bstack1l1lll11l_opy_(config):
  if bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧូ") in config:
        return config[bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨួ")]
  for platform in config.get(bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬើ"), []):
      if bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪឿ") in platform:
          return platform[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫៀ")]
  return None
def bstack1l111llll_opy_(bstack111ll1ll11_opy_):
  try:
    browser_name = bstack111ll1ll11_opy_[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫេ")]
    browser_version = bstack111ll1ll11_opy_[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨែ")]
    chrome_options = bstack111ll1ll11_opy_[bstack1l111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨៃ")]
    try:
        bstack11l1ll1lll1_opy_ = int(browser_version.split(bstack1l111l1_opy_ (u"ࠨ࠰ࠪោ"))[0])
    except ValueError as e:
        logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨៅ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l111l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪំ")):
        logger.warning(bstack1l111l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢះ"))
        return False
    if bstack11l1ll1lll1_opy_ < bstack11ll11l111l_opy_.bstack1ll1111lll1_opy_:
        logger.warning(bstack1ll1ll1111l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡃࡐࡐࡖࡘࡆࡔࡔࡔ࠰ࡐࡍࡓࡏࡍࡖࡏࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘ࡛ࡐࡑࡑࡕࡘࡊࡊ࡟ࡄࡊࡕࡓࡒࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࡾࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳࠭ៈ"))
        return False
    if chrome_options and any(bstack1l111l1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪ៉") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l111l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ៊"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨ់") + str(e))
    return False
def bstack1ll1ll1l_opy_(bstack1ll1llll1l_opy_, config):
    try:
      bstack1l1lllllll1_opy_ = bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ៌") in config and config[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ៍")] == True
      bstack11ll111l1l1_opy_ = bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ៎") in config and str(config[bstack1l111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ៏")]).lower() != bstack1l111l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ័")
      if not (bstack1l1lllllll1_opy_ and (not bstack11lll1lll_opy_(config) or bstack11ll111l1l1_opy_)):
        return bstack1ll1llll1l_opy_
      bstack11ll11111l1_opy_ = bstack1l111l1l_opy_.bstack11l1lllll1l_opy_
      if bstack11ll11111l1_opy_ is None:
        logger.debug(bstack1l111l1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥ៑"))
        return bstack1ll1llll1l_opy_
      bstack11l1ll1l1l1_opy_ = int(str(bstack11ll111l111_opy_()).split(bstack1l111l1_opy_ (u"ࠨ࠰្ࠪ"))[0])
      logger.debug(bstack1l111l1_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤ៓") + str(bstack11l1ll1l1l1_opy_) + bstack1l111l1_opy_ (u"ࠥࠦ។"))
      if bstack11l1ll1l1l1_opy_ == 3 and isinstance(bstack1ll1llll1l_opy_, dict) and bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ៕") in bstack1ll1llll1l_opy_ and bstack11ll11111l1_opy_ is not None:
        if bstack1l111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៖") not in bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ៗ")]:
          bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៘")][bstack1l111l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭៙")] = {}
        if bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ៚") in bstack11ll11111l1_opy_:
          if bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ៛") not in bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫៜ")][bstack1l111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៝")]:
            bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭៞")][bstack1l111l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៟")][bstack1l111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭០")] = []
          for arg in bstack11ll11111l1_opy_[bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ១")]:
            if arg not in bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ២")][bstack1l111l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៣")][bstack1l111l1_opy_ (u"ࠬࡧࡲࡨࡵࠪ៤")]:
              bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭៥")][bstack1l111l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៦")][bstack1l111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭៧")].append(arg)
        if bstack1l111l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭៨") in bstack11ll11111l1_opy_:
          if bstack1l111l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ៩") not in bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ៪")][bstack1l111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៫")]:
            bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭៬")][bstack1l111l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៭")][bstack1l111l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ៮")] = []
          for ext in bstack11ll11111l1_opy_[bstack1l111l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭៯")]:
            if ext not in bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ៰")][bstack1l111l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៱")][bstack1l111l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ៲")]:
              bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭៳")][bstack1l111l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៴")][bstack1l111l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ៵")].append(ext)
        if bstack1l111l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ៶") in bstack11ll11111l1_opy_:
          if bstack1l111l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ៷") not in bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ៸")][bstack1l111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៹")]:
            bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭៺")][bstack1l111l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៻")][bstack1l111l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ៼")] = {}
          bstack11l1lll11l1_opy_(bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ៽")][bstack1l111l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ៾")][bstack1l111l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ៿")],
                    bstack11ll11111l1_opy_[bstack1l111l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᠀")])
        os.environ[bstack1l111l1_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫ᠁")] = bstack1l111l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ᠂")
        return bstack1ll1llll1l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1llll1l_opy_, ChromeOptions):
          chrome_options = bstack1ll1llll1l_opy_
        elif isinstance(bstack1ll1llll1l_opy_, dict):
          for value in bstack1ll1llll1l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1llll1l_opy_, dict):
            bstack1ll1llll1l_opy_[bstack1l111l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᠃")] = chrome_options
          else:
            bstack1ll1llll1l_opy_ = chrome_options
        if bstack11ll11111l1_opy_ is not None:
          if bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᠄") in bstack11ll11111l1_opy_:
                bstack11l1ll1ll11_opy_ = chrome_options.arguments or []
                new_args = bstack11ll11111l1_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᠅")]
                for arg in new_args:
                    if arg not in bstack11l1ll1ll11_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l111l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᠆") in bstack11ll11111l1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l111l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᠇"), [])
                bstack11ll111l11l_opy_ = bstack11ll11111l1_opy_[bstack1l111l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᠈")]
                for extension in bstack11ll111l11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l111l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᠉") in bstack11ll11111l1_opy_:
                bstack11l1lll111l_opy_ = chrome_options.experimental_options.get(bstack1l111l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᠊"), {})
                bstack11l1llllll1_opy_ = bstack11ll11111l1_opy_[bstack1l111l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᠋")]
                bstack11l1lll11l1_opy_(bstack11l1lll111l_opy_, bstack11l1llllll1_opy_)
                chrome_options.add_experimental_option(bstack1l111l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᠌"), bstack11l1lll111l_opy_)
        os.environ[bstack1l111l1_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᠍")] = bstack1l111l1_opy_ (u"ࠬࡺࡲࡶࡧࠪ᠎")
        return bstack1ll1llll1l_opy_
    except Exception as e:
      logger.error(bstack1l111l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦ᠏") + str(e))
      return bstack1ll1llll1l_opy_