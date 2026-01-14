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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1111lll_opy_, bstack11l1111l1_opy_, get_host_info, bstack111lllll111_opy_, \
 bstack111111lll_opy_, bstack1ll1ll11ll_opy_, error_handler, bstack11l111ll11l_opy_, bstack11ll11ll1l_opy_
import bstack_utils.accessibility as bstack1ll1l11lll_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111lll111l_opy_
from bstack_utils.bstack111l1l1111_opy_ import bstack1l1l1lllll_opy_
from bstack_utils.percy import bstack1l1l11lll_opy_
from bstack_utils.config import Config
bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1l11lll_opy_()
@error_handler(class_method=False)
def bstack1lll1ll1l11l_opy_(bs_config, bstack1l1l1ll1l_opy_):
  try:
    data = {
        bstack1l11l1l_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ⊟"): bstack1l11l1l_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ⊠"),
        bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ⊡"): bs_config.get(bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⊢"), bstack1l11l1l_opy_ (u"ࠬ࠭⊣")),
        bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⊤"): bs_config.get(bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⊥"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⊦"): bs_config.get(bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⊧")),
        bstack1l11l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⊨"): bs_config.get(bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ⊩"), bstack1l11l1l_opy_ (u"ࠬ࠭⊪")),
        bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊫"): bstack11ll11ll1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬ⊬"): bstack111lllll111_opy_(bs_config),
        bstack1l11l1l_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ⊭"): get_host_info(),
        bstack1l11l1l_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ⊮"): bstack11l1111l1_opy_(),
        bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⊯"): os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ⊰")),
        bstack1l11l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ⊱"): os.environ.get(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ⊲"), False),
        bstack1l11l1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ⊳"): bstack11ll1111lll_opy_(),
        bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⊴"): bstack1lll1l1l111l_opy_(bs_config),
        bstack1l11l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭⊵"): bstack1lll1l1llll1_opy_(bstack1l1l1ll1l_opy_),
        bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⊶"): bstack1lll1l1l1l1l_opy_(bs_config, bstack1l1l1ll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ⊷"), bstack1l11l1l_opy_ (u"ࠬ࠭⊸"))),
        bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⊹"): bstack111111lll_opy_(bs_config),
        bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ⊺"): bstack1lll1l1l11l1_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⊻").format(str(error)))
    return None
def bstack1lll1l1llll1_opy_(framework):
  return {
    bstack1l11l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ⊼"): framework.get(bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ⊽"), bstack1l11l1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⊾")),
    bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⊿"): framework.get(bstack1l11l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⋀")),
    bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ⋁"): framework.get(bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⋂")),
    bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ⋃"): bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⋄"),
    bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⋅"): framework.get(bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⋆"))
  }
def bstack1lll1l1l11l1_opy_(bs_config):
  bstack1l11l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠮ࠋࠢࠣࠦࠧࠨ⋇")
  if not bs_config:
    return {}
  bstack11111llllll_opy_ = bstack111lll111l_opy_(bs_config).bstack11111l1ll11_opy_(bs_config)
  return bstack11111llllll_opy_
def bstack1ll11lll1l_opy_(bs_config, framework):
  bstack11l1ll1ll1_opy_ = False
  bstack11l1111l1l_opy_ = False
  bstack1lll1l1l11ll_opy_ = False
  if bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⋈") in bs_config:
    bstack1lll1l1l11ll_opy_ = True
  elif bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࠬ⋉") in bs_config:
    bstack11l1ll1ll1_opy_ = True
  else:
    bstack11l1111l1l_opy_ = True
  bstack11lll1ll1_opy_ = {
    bstack1l11l1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⋊"): bstack1l1l1lllll_opy_.bstack1lll1l1l1l11_opy_(bs_config, framework),
    bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⋋"): bstack1ll1l11lll_opy_.bstack1ll1ll1lll_opy_(bs_config),
    bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⋌"): bs_config.get(bstack1l11l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⋍"), False),
    bstack1l11l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⋎"): bstack11l1111l1l_opy_,
    bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⋏"): bstack11l1ll1ll1_opy_,
    bstack1l11l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⋐"): bstack1lll1l1l11ll_opy_
  }
  return bstack11lll1ll1_opy_
@error_handler(class_method=False)
def bstack1lll1l1l111l_opy_(bs_config):
  try:
    bstack1lll1l1ll1l1_opy_ = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⋑"), bstack1l11l1l_opy_ (u"ࠪࡿࢂ࠭⋒")))
    bstack1lll1l1ll1l1_opy_ = bstack1lll1l1ll1ll_opy_(bs_config, bstack1lll1l1ll1l1_opy_)
    return {
        bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭⋓"): bstack1lll1l1ll1l1_opy_
    }
  except Exception as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ⋔").format(str(error)))
    return {}
def bstack1lll1l1ll1ll_opy_(bs_config, bstack1lll1l1ll1l1_opy_):
  if ((bstack1l11l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⋕") in bs_config or not bstack111111lll_opy_(bs_config)) and bstack1ll1l11lll_opy_.bstack1ll1ll1lll_opy_(bs_config)):
    bstack1lll1l1ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠢࡪࡰࡦࡰࡺࡪࡥࡆࡰࡦࡳࡩ࡫ࡤࡆࡺࡷࡩࡳࡹࡩࡰࡰࠥ⋖")] = True
  return bstack1lll1l1ll1l1_opy_
def bstack1lll1lll1l11_opy_(array, bstack1lll1l1l1lll_opy_, bstack1lll1l1ll11l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll1l1l1lll_opy_]
    result[key] = o[bstack1lll1l1ll11l_opy_]
  return result
def bstack1lll1lll11l1_opy_(bstack11l1111l_opy_=bstack1l11l1l_opy_ (u"ࠨࠩ⋗")):
  bstack1lll1l1ll111_opy_ = bstack1ll1l11lll_opy_.on()
  bstack1lll1l1lll11_opy_ = bstack1l1l1lllll_opy_.on()
  bstack1lll1l1l1ll1_opy_ = percy.bstack111ll11ll_opy_()
  if bstack1lll1l1l1ll1_opy_ and not bstack1lll1l1lll11_opy_ and not bstack1lll1l1ll111_opy_:
    return bstack11l1111l_opy_ not in [bstack1l11l1l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⋘"), bstack1l11l1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⋙")]
  elif bstack1lll1l1ll111_opy_ and not bstack1lll1l1lll11_opy_:
    return bstack11l1111l_opy_ not in [bstack1l11l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⋚"), bstack1l11l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⋛"), bstack1l11l1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⋜")]
  return bstack1lll1l1ll111_opy_ or bstack1lll1l1lll11_opy_ or bstack1lll1l1l1ll1_opy_
@error_handler(class_method=False)
def bstack1lll1lll11ll_opy_(bstack11l1111l_opy_, test=None):
  bstack1lll1l1lll1l_opy_ = bstack1ll1l11lll_opy_.on()
  if not bstack1lll1l1lll1l_opy_ or bstack11l1111l_opy_ not in [bstack1l11l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⋝")] or test == None:
    return None
  return {
    bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⋞"): bstack1lll1l1lll1l_opy_ and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⋟"), None) == True and bstack1ll1l11lll_opy_.bstack1l1l11llll_opy_(test[bstack1l11l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⋠")])
  }
def bstack1lll1l1l1l1l_opy_(bs_config, framework):
  bstack11l1ll1ll1_opy_ = False
  bstack11l1111l1l_opy_ = False
  bstack1lll1l1l11ll_opy_ = False
  if bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⋡") in bs_config:
    bstack1lll1l1l11ll_opy_ = True
  elif bstack1l11l1l_opy_ (u"ࠬࡧࡰࡱࠩ⋢") in bs_config:
    bstack11l1ll1ll1_opy_ = True
  else:
    bstack11l1111l1l_opy_ = True
  bstack11lll1ll1_opy_ = {
    bstack1l11l1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⋣"): bstack1l1l1lllll_opy_.bstack1lll1l1l1l11_opy_(bs_config, framework),
    bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⋤"): bstack1ll1l11lll_opy_.bstack1lll11llll_opy_(bs_config),
    bstack1l11l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⋥"): bs_config.get(bstack1l11l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⋦"), False),
    bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⋧"): bstack11l1111l1l_opy_,
    bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⋨"): bstack11l1ll1ll1_opy_,
    bstack1l11l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⋩"): bstack1lll1l1l11ll_opy_
  }
  return bstack11lll1ll1_opy_