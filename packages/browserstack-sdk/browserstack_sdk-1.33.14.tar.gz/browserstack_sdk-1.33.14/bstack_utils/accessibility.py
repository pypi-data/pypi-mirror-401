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
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l1lll1l1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1llll1ll_opy_ as bstack11ll11l11l1_opy_, EVENTS
from bstack_utils.bstack1l111lll_opy_ import bstack1l111lll_opy_
from bstack_utils.helper import bstack11ll11ll1l_opy_, bstack1111l11111_opy_, bstack111111lll_opy_, bstack11l1lll1ll1_opy_, \
  bstack11l1lllll11_opy_, bstack11l1111l1_opy_, get_host_info, bstack11ll1111lll_opy_, bstack11l111ll11_opy_, error_handler, bstack11ll111111l_opy_, bstack11ll1111l1l_opy_, bstack1ll1ll11ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11lllll1_opy_ import get_logger
from bstack_utils.bstack1lll1l111_opy_ import bstack1ll1llll11l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import bstack11lllll1_opy_
logger = get_logger(__name__)
bstack11l1l1l11l_opy_ = bstack11lllll1_opy_.bstack1l11llllll_opy_(__name__)
bstack1lll1l111_opy_ = bstack1ll1llll11l_opy_()
@error_handler(class_method=False)
def _11ll11lll11_opy_(driver, bstack1llllllll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l11l1l_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᚭ"): caps.get(bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᚮ"), None),
        bstack1l11l1l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᚯ"): bstack1llllllll11_opy_.get(bstack1l11l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚰ"), None),
        bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᚱ"): caps.get(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᚲ"), None),
        bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᚳ"): caps.get(bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᚴ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᚵ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᚶ"), None) is None or os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᚷ")] == bstack1l11l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᚸ"):
        return False
    return True
def bstack1ll1ll1lll_opy_(config):
  return config.get(bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚹ"), False) or any([p.get(bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚺ"), False) == True for p in config.get(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᚻ"), [])])
def bstack1ll111l1_opy_(config, bstack1l11l1111_opy_):
  try:
    bstack11l1llllll1_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚼ"), False)
    if int(bstack1l11l1111_opy_) < len(config.get(bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᚽ"), [])) and config[bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᚾ")][bstack1l11l1111_opy_]:
      bstack11ll1111l11_opy_ = config[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᚿ")][bstack1l11l1111_opy_].get(bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛀ"), None)
    else:
      bstack11ll1111l11_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛁ"), None)
    if bstack11ll1111l11_opy_ != None:
      bstack11l1llllll1_opy_ = bstack11ll1111l11_opy_
    bstack11ll11ll11l_opy_ = os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᛂ")) is not None and len(os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᛃ"))) > 0 and os.getenv(bstack1l11l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᛄ")) != bstack1l11l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᛅ")
    return bstack11l1llllll1_opy_ and bstack11ll11ll11l_opy_
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᛆ") + str(error))
  return False
def bstack1l1l11llll_opy_(test_tags):
  bstack1ll11111lll_opy_ = os.getenv(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᛇ"))
  if bstack1ll11111lll_opy_ is None:
    return True
  bstack1ll11111lll_opy_ = json.loads(bstack1ll11111lll_opy_)
  try:
    include_tags = bstack1ll11111lll_opy_[bstack1l11l1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᛈ")] if bstack1l11l1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᛉ") in bstack1ll11111lll_opy_ and isinstance(bstack1ll11111lll_opy_[bstack1l11l1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᛊ")], list) else []
    exclude_tags = bstack1ll11111lll_opy_[bstack1l11l1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᛋ")] if bstack1l11l1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᛌ") in bstack1ll11111lll_opy_ and isinstance(bstack1ll11111lll_opy_[bstack1l11l1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᛍ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᛎ") + str(error))
  return False
def bstack11ll11l111l_opy_(config, bstack11l1llll11l_opy_, bstack11ll11ll1l1_opy_, bstack11l1lll1l11_opy_):
  bstack11l1lll1lll_opy_ = bstack11l1lll1ll1_opy_(config)
  bstack11ll11ll1ll_opy_ = bstack11l1lllll11_opy_(config)
  if bstack11l1lll1lll_opy_ is None or bstack11ll11ll1ll_opy_ is None:
    logger.error(bstack1l11l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᛏ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᛐ"), bstack1l11l1l_opy_ (u"ࠪࡿࢂ࠭ᛑ")))
    data = {
        bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᛒ"): config[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᛓ")],
        bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᛔ"): config.get(bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᛕ"), os.path.basename(os.getcwd())),
        bstack1l11l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫᛖ"): bstack11ll11ll1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᛗ"): config.get(bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᛘ"), bstack1l11l1l_opy_ (u"ࠫࠬᛙ")),
        bstack1l11l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᛚ"): {
            bstack1l11l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᛛ"): bstack11l1llll11l_opy_,
            bstack1l11l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᛜ"): bstack11ll11ll1l1_opy_,
            bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᛝ"): __version__,
            bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᛞ"): bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᛟ"),
            bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᛠ"): bstack1l11l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᛡ"),
            bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᛢ"): bstack11l1lll1l11_opy_
        },
        bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᛣ"): settings,
        bstack1l11l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩᛤ"): bstack11ll1111lll_opy_(),
        bstack1l11l1l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩᛥ"): bstack11l1111l1_opy_(),
        bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬᛦ"): get_host_info(),
        bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᛧ"): bstack111111lll_opy_(config)
    }
    headers = {
        bstack1l11l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᛨ"): bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᛩ"),
    }
    config = {
        bstack1l11l1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᛪ"): (bstack11l1lll1lll_opy_, bstack11ll11ll1ll_opy_),
        bstack1l11l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᛫"): headers
    }
    response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ᛬"), bstack11ll11l11l1_opy_ + bstack1l11l1l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪ᛭"), data, config)
    bstack11ll11111ll_opy_ = response.json()
    if bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᛮ")]:
      parsed = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᛯ"), bstack1l11l1l_opy_ (u"࠭ࡻࡾࠩᛰ")))
      parsed[bstack1l11l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛱ")] = bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᛲ")][bstack1l11l1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᛳ")]
      os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᛴ")] = json.dumps(parsed)
      bstack1l111lll_opy_.bstack11llll11_opy_(bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᛵ")][bstack1l11l1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᛶ")])
      bstack1l111lll_opy_.bstack11ll111llll_opy_(bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᛷ")][bstack1l11l1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᛸ")])
      bstack1l111lll_opy_.store()
      return bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭᛹")][bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ᛺")], bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡨࡦࡺࡡࠨ᛻")][bstack1l11l1l_opy_ (u"ࠫ࡮ࡪࠧ᛼")]
    else:
      logger.error(bstack1l11l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭᛽") + bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᛾")])
      if bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᛿")] == bstack1l11l1l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪᜀ"):
        for bstack11ll11111l1_opy_ in bstack11ll11111ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᜁ")]:
          logger.error(bstack11ll11111l1_opy_[bstack1l11l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᜂ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧᜃ") +  str(error))
    return None, None
def bstack11l1lllllll_opy_():
  if os.getenv(bstack1l11l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᜄ")) is None:
    return {
        bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᜅ"): bstack1l11l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᜆ"),
        bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᜇ"): bstack1l11l1l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨᜈ")
    }
  data = {bstack1l11l1l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫᜉ"): bstack11ll11ll1l_opy_()}
  headers = {
      bstack1l11l1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᜊ"): bstack1l11l1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ᜋ") + os.getenv(bstack1l11l1l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦᜌ")),
      bstack1l11l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᜍ"): bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᜎ")
  }
  response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠩࡓ࡙࡙࠭ᜏ"), bstack11ll11l11l1_opy_ + bstack1l11l1l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬᜐ"), data, { bstack1l11l1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᜑ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l11l1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨᜒ") + bstack1111l11111_opy_().isoformat() + bstack1l11l1l_opy_ (u"࡚࠭ࠨᜓ"))
      return {bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹ᜔ࠧ"): bstack1l11l1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴ᜕ࠩ"), bstack1l11l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᜖"): bstack1l11l1l_opy_ (u"ࠪࠫ᜗")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ᜘") + str(error))
    return {
        bstack1l11l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ᜙"): bstack1l11l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᜚"),
        bstack1l11l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᜛"): str(error)
    }
def bstack11ll111l1ll_opy_(bstack11ll111ll11_opy_):
    return re.match(bstack1l11l1l_opy_ (u"ࡳࠩࡡࡠࡩ࠱ࠨ࡝࠰࡟ࡨ࠰࠯࠿ࠥࠩ᜜"), bstack11ll111ll11_opy_.strip()) is not None
def bstack1ll11ll111_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll11lll1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll11lll1l_opy_ = desired_capabilities
        else:
          bstack11ll11lll1l_opy_ = {}
        bstack1ll111lll11_opy_ = (bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᜝"), bstack1l11l1l_opy_ (u"ࠪࠫ᜞")).lower() or caps.get(bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᜟ"), bstack1l11l1l_opy_ (u"ࠬ࠭ᜠ")).lower())
        if bstack1ll111lll11_opy_ == bstack1l11l1l_opy_ (u"࠭ࡩࡰࡵࠪᜡ"):
            return True
        if bstack1ll111lll11_opy_ == bstack1l11l1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᜢ"):
            bstack1l1lll111ll_opy_ = str(float(caps.get(bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᜣ")) or bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᜤ"), {}).get(bstack1l11l1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜥ"),bstack1l11l1l_opy_ (u"ࠫࠬᜦ"))))
            if bstack1ll111lll11_opy_ == bstack1l11l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᜧ") and int(bstack1l1lll111ll_opy_.split(bstack1l11l1l_opy_ (u"࠭࠮ࠨᜨ"))[0]) < float(bstack11l1lllll1l_opy_):
                logger.warning(str(bstack11ll11ll111_opy_))
                return False
            return True
        bstack1l1llll1lll_opy_ = caps.get(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᜩ"), {}).get(bstack1l11l1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᜪ"), caps.get(bstack1l11l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᜫ"), bstack1l11l1l_opy_ (u"ࠪࠫᜬ")))
        if bstack1l1llll1lll_opy_:
            logger.warning(bstack1l11l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᜭ"))
            return False
        browser = caps.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᜮ"), bstack1l11l1l_opy_ (u"࠭ࠧᜯ")).lower() or bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᜰ"), bstack1l11l1l_opy_ (u"ࠨࠩᜱ")).lower()
        if browser != bstack1l11l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᜲ"):
            logger.warning(bstack1l11l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᜳ"))
            return False
        browser_version = caps.get(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ᜴ࠬ")) or caps.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᜵")) or bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᜶")) or bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᜷"), {}).get(bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᜸")) or bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᜹"), {}).get(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᜺"))
        bstack1l1lll1ll11_opy_ = bstack11l1lll1l1l_opy_.bstack1ll111lllll_opy_
        bstack11ll11l1l1l_opy_ = False
        if config is not None:
          bstack11ll11l1l1l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᜻") in config and str(config[bstack1l11l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᜼")]).lower() != bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᜽")
        if os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᜾"), bstack1l11l1l_opy_ (u"ࠨࠩ᜿")).lower() == bstack1l11l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᝀ") or bstack11ll11l1l1l_opy_:
          bstack1l1lll1ll11_opy_ = bstack11l1lll1l1l_opy_.bstack1l1lll1l111_opy_
        if browser_version and browser_version != bstack1l11l1l_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᝁ") and int(browser_version.split(bstack1l11l1l_opy_ (u"ࠫ࠳࠭ᝂ"))[0]) <= bstack1l1lll1ll11_opy_:
          logger.warning(bstack1ll1lll1l1l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻ࡮࡫ࡱࡣࡦ࠷࠱ࡺࡡࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࡤࡩࡨࡳࡱࡰࡩࡤࡼࡥࡳࡵ࡬ࡳࡳࢃ࠮ࠨᝃ"))
          return False
        if not options:
          bstack1ll111l1l11_opy_ = caps.get(bstack1l11l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᝄ")) or bstack11ll11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᝅ"), {})
          if bstack1l11l1l_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᝆ") in bstack1ll111l1l11_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᝇ"), []):
              logger.warning(bstack1l11l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᝈ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨᝉ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll111ll11_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᝊ"), {})
    bstack1lll111ll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᝋ")] = os.getenv(bstack1l11l1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᝌ"))
    bstack11ll1111111_opy_ = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᝍ"), bstack1l11l1l_opy_ (u"ࠩࡾࢁࠬᝎ"))).get(bstack1l11l1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᝏ"))
    if not config[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᝐ")].get(bstack1l11l1l_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᝑ")):
      if bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᝒ") in caps:
        caps[bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᝓ")][bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᝔")] = bstack1lll111ll11_opy_
        caps[bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᝕")][bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᝖")][bstack1l11l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᝗")] = bstack11ll1111111_opy_
      else:
        caps[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᝘")] = bstack1lll111ll11_opy_
        caps[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᝙")][bstack1l11l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᝚")] = bstack11ll1111111_opy_
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ᝛") +  str(error))
def bstack1lllll1ll_opy_(driver, bstack11ll111l11l_opy_):
  try:
    setattr(driver, bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ᝜"), True)
    session = driver.session_id
    if session:
      bstack11ll11l1111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll11l1111_opy_ = False
      bstack11ll11l1111_opy_ = url.scheme in [bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣ᝝"), bstack1l11l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ᝞")]
      if bstack11ll11l1111_opy_:
        if bstack11ll111l11l_opy_:
          logger.info(bstack1l11l1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧ᝟"))
      return bstack11ll111l11l_opy_
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᝠ") + str(e))
    return False
def bstack11ll11l1l_opy_(driver, name, path):
  try:
    bstack1l1lll1l11l_opy_ = {
        bstack1l11l1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᝡ"): threading.current_thread().current_test_uuid,
        bstack1l11l1l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᝢ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᝣ"), bstack1l11l1l_opy_ (u"ࠪࠫᝤ")),
        bstack1l11l1l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᝥ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᝦ"), bstack1l11l1l_opy_ (u"࠭ࠧᝧ"))
    }
    bstack1l1lll11lll_opy_ = bstack1lll1l111_opy_.bstack1ll11l1l11l_opy_(EVENTS.bstack11l11l11l_opy_.value)
    logger.debug(bstack1l11l1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᝨ"))
    try:
      if (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᝩ"), None) and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᝪ"), None)):
        scripts = {bstack1l11l1l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᝫ"): bstack1l111lll_opy_.perform_scan}
        bstack11ll11l11ll_opy_ = json.loads(scripts[bstack1l11l1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᝬ")].replace(bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣ᝭"), bstack1l11l1l_opy_ (u"ࠨࠢᝮ")))
        bstack11ll11l11ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᝯ")][bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᝰ")] = None
        scripts[bstack1l11l1l_opy_ (u"ࠤࡶࡧࡦࡴࠢ᝱")] = bstack1l11l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᝲ") + json.dumps(bstack11ll11l11ll_opy_)
        bstack1l111lll_opy_.bstack11llll11_opy_(scripts)
        bstack1l111lll_opy_.store()
        logger.debug(driver.execute_script(bstack1l111lll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111lll_opy_.perform_scan, {bstack1l11l1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᝳ"): name}))
      bstack1lll1l111_opy_.end(EVENTS.bstack11l11l11l_opy_.value, bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᝴"), bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᝵"), True, None)
    except Exception as error:
      bstack1lll1l111_opy_.end(EVENTS.bstack11l11l11l_opy_.value, bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᝶"), bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᝷"), False, str(error))
    bstack1l1lll11lll_opy_ = bstack1lll1l111_opy_.bstack11ll11l1l11_opy_(EVENTS.bstack1l1lll1llll_opy_.value)
    bstack1lll1l111_opy_.mark(bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᝸"))
    try:
      if (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ᝹"), None) and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᝺"), None)):
        scripts = {bstack1l11l1l_opy_ (u"ࠬࡹࡣࡢࡰࠪ᝻"): bstack1l111lll_opy_.perform_scan}
        bstack11ll11l11ll_opy_ = json.loads(scripts[bstack1l11l1l_opy_ (u"ࠨࡳࡤࡣࡱࠦ᝼")].replace(bstack1l11l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ᝽"), bstack1l11l1l_opy_ (u"ࠣࠤ᝾")))
        bstack11ll11l11ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᝿")][bstack1l11l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪក")] = None
        scripts[bstack1l11l1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤខ")] = bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣគ") + json.dumps(bstack11ll11l11ll_opy_)
        bstack1l111lll_opy_.bstack11llll11_opy_(scripts)
        bstack1l111lll_opy_.store()
        logger.debug(driver.execute_script(bstack1l111lll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111lll_opy_.bstack11l1llll111_opy_, bstack1l1lll1l11l_opy_))
      bstack1lll1l111_opy_.end(bstack1l1lll11lll_opy_, bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨឃ"), bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧង"),True, None)
    except Exception as error:
      bstack1lll1l111_opy_.end(bstack1l1lll11lll_opy_, bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣច"), bstack1l1lll11lll_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢឆ"),False, str(error))
    logger.info(bstack1l11l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨជ"))
    try:
      bstack1ll111l11ll_opy_ = {
        bstack1l11l1l_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧឈ"): {
          bstack1l11l1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨញ"): bstack1l11l1l_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥដ"),
        },
        bstack1l11l1l_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤឋ"): {
          bstack1l11l1l_opy_ (u"ࠣࡤࡲࡨࡾࠨឌ"): {
            bstack1l11l1l_opy_ (u"ࠤࡰࡷ࡬ࠨឍ"): bstack1l11l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨណ"),
            bstack1l11l1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧត"): True
          }
        }
      }
      bstack11l1l1l11l_opy_.info(json.dumps(bstack1ll111l11ll_opy_, separators=(bstack1l11l1l_opy_ (u"ࠬ࠲ࠧថ"), bstack1l11l1l_opy_ (u"࠭࠺ࠨទ"))))
    except Exception as bstack1l111lll1l_opy_:
      logger.debug(bstack1l11l1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨធ") + str(bstack1l111lll1l_opy_) + bstack1l11l1l_opy_ (u"ࠣࠤន"))
  except Exception as bstack1ll111ll11l_opy_:
    logger.error(bstack1l11l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦប") + str(path) + bstack1l11l1l_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧផ") + str(bstack1ll111ll11l_opy_))
def bstack11ll111lll1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l11l1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥព")) and str(caps.get(bstack1l11l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦភ"))).lower() == bstack1l11l1l_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢម"):
        bstack1l1lll111ll_opy_ = caps.get(bstack1l11l1l_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤយ")) or caps.get(bstack1l11l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥរ"))
        if bstack1l1lll111ll_opy_ and int(str(bstack1l1lll111ll_opy_)) < bstack11l1lllll1l_opy_:
            return False
    return True
def bstack1lll11llll_opy_(config):
  if bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩល") in config:
        return config[bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪវ")]
  for platform in config.get(bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧឝ"), []):
      if bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬឞ") in platform:
          return platform[bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ស")]
  return None
def bstack1l1l111ll_opy_(bstack1lll11ll11_opy_):
  try:
    browser_name = bstack1lll11ll11_opy_[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ហ")]
    browser_version = bstack1lll11ll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪឡ")]
    chrome_options = bstack1lll11ll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪអ")]
    try:
        bstack11ll1111ll1_opy_ = int(browser_version.split(bstack1l11l1l_opy_ (u"ࠪ࠲ࠬឣ"))[0])
    except ValueError as e:
        logger.error(bstack1l11l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡳࡼࡥࡳࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠣឤ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l11l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬឥ")):
        logger.warning(bstack1l11l1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤឦ"))
        return False
    if bstack11ll1111ll1_opy_ < bstack11l1lll1l1l_opy_.bstack1l1lll1l111_opy_:
        logger.warning(bstack1ll1lll1l1l_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡃࡩࡴࡲࡱࡪࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡼࡅࡒࡒࡘ࡚ࡁࡏࡖࡖ࠲ࡒࡏࡎࡊࡏࡘࡑࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡖࡒࡓࡓࡗ࡚ࡅࡅࡡࡆࡌࡗࡕࡍࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࢀࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠨឧ"))
        return False
    if chrome_options and any(bstack1l11l1l_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬឨ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l11l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦឩ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡪࡴࡸࠠ࡭ࡱࡦࡥࡱࠦࡃࡩࡴࡲࡱࡪࡀࠠࠣឪ") + str(e))
    return False
def bstack11lll11l1_opy_(bstack1ll1l1lll1_opy_, config):
    try:
      bstack1ll111ll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫឫ") in config and config[bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬឬ")] == True
      bstack11ll11l1l1l_opy_ = bstack1l11l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪឭ") in config and str(config[bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫឮ")]).lower() != bstack1l11l1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧឯ")
      if not (bstack1ll111ll1ll_opy_ and (not bstack111111lll_opy_(config) or bstack11ll11l1l1l_opy_)):
        return bstack1ll1l1lll1_opy_
      bstack11ll111ll1l_opy_ = bstack1l111lll_opy_.bstack11ll11l1ll1_opy_
      if bstack11ll111ll1l_opy_ is None:
        logger.debug(bstack1l11l1l_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡫ࠠࡏࡱࡱࡩࠧឰ"))
        return bstack1ll1l1lll1_opy_
      bstack11l1lll11ll_opy_ = int(str(bstack11ll1111l1l_opy_()).split(bstack1l11l1l_opy_ (u"ࠪ࠲ࠬឱ"))[0])
      logger.debug(bstack1l11l1l_opy_ (u"ࠦࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࠦឲ") + str(bstack11l1lll11ll_opy_) + bstack1l11l1l_opy_ (u"ࠧࠨឳ"))
      if bstack11l1lll11ll_opy_ == 3 and isinstance(bstack1ll1l1lll1_opy_, dict) and bstack1l11l1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭឴") in bstack1ll1l1lll1_opy_ and bstack11ll111ll1l_opy_ is not None:
        if bstack1l11l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ឵") not in bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨា")]:
          bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩិ")][bstack1l11l1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨី")] = {}
        if bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩឹ") in bstack11ll111ll1l_opy_:
          if bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪឺ") not in bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ុ")][bstack1l11l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬូ")]:
            bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨួ")][bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧើ")][bstack1l11l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨឿ")] = []
          for arg in bstack11ll111ll1l_opy_[bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩៀ")]:
            if arg not in bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬេ")][bstack1l11l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫែ")][bstack1l11l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬៃ")]:
              bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨោ")][bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧៅ")][bstack1l11l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨំ")].append(arg)
        if bstack1l11l1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨះ") in bstack11ll111ll1l_opy_:
          if bstack1l11l1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩៈ") not in bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭៉")][bstack1l11l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៊")]:
            bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ់")][bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៌")][bstack1l11l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ៍")] = []
          for ext in bstack11ll111ll1l_opy_[bstack1l11l1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ៎")]:
            if ext not in bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ៏")][bstack1l11l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ័")][bstack1l11l1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ៑")]:
              bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ្")][bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៓")][bstack1l11l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ។")].append(ext)
        if bstack1l11l1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ៕") in bstack11ll111ll1l_opy_:
          if bstack1l11l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ៖") not in bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ៗ")][bstack1l11l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ៘")]:
            bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ៙")][bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៚")][bstack1l11l1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ៛")] = {}
          bstack11ll111111l_opy_(bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫៜ")][bstack1l11l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៝")][bstack1l11l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ៞")],
                    bstack11ll111ll1l_opy_[bstack1l11l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭៟")])
        os.environ[bstack1l11l1l_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭០")] = bstack1l11l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ១")
        return bstack1ll1l1lll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1l1lll1_opy_, ChromeOptions):
          chrome_options = bstack1ll1l1lll1_opy_
        elif isinstance(bstack1ll1l1lll1_opy_, dict):
          for value in bstack1ll1l1lll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1l1lll1_opy_, dict):
            bstack1ll1l1lll1_opy_[bstack1l11l1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ២")] = chrome_options
          else:
            bstack1ll1l1lll1_opy_ = chrome_options
        if bstack11ll111ll1l_opy_ is not None:
          if bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ៣") in bstack11ll111ll1l_opy_:
                bstack11l1llll1l1_opy_ = chrome_options.arguments or []
                new_args = bstack11ll111ll1l_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ៤")]
                for arg in new_args:
                    if arg not in bstack11l1llll1l1_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l11l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ៥") in bstack11ll111ll1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l11l1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ៦"), [])
                bstack11ll111l1l1_opy_ = bstack11ll111ll1l_opy_[bstack1l11l1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ៧")]
                for extension in bstack11ll111l1l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l11l1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ៨") in bstack11ll111ll1l_opy_:
                bstack11ll111l111_opy_ = chrome_options.experimental_options.get(bstack1l11l1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ៩"), {})
                bstack11ll11l1lll_opy_ = bstack11ll111ll1l_opy_[bstack1l11l1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ៪")]
                bstack11ll111111l_opy_(bstack11ll111l111_opy_, bstack11ll11l1lll_opy_)
                chrome_options.add_experimental_option(bstack1l11l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ៫"), bstack11ll111l111_opy_)
        os.environ[bstack1l11l1l_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫ៬")] = bstack1l11l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ៭")
        return bstack1ll1l1lll1_opy_
    except Exception as e:
      logger.error(bstack1l11l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡥࡦ࡬ࡲ࡬ࠦ࡮ࡰࡰ࠰ࡆࡘࠦࡩ࡯ࡨࡵࡥࠥࡧ࠱࠲ࡻࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠨ៮") + str(e))
      return bstack1ll1l1lll1_opy_