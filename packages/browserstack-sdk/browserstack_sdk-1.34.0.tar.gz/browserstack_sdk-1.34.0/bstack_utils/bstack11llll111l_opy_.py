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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll11111ll_opy_, bstack11lll11l1_opy_, get_host_info, bstack111l1ll1ll1_opy_, \
 bstack11lll1lll_opy_, bstack1l1l1l111_opy_, error_handler, bstack111lll111ll_opy_, bstack11llll1111_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack1llll111l_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11ll11l11_opy_
from bstack_utils.percy import bstack11ll11111_opy_
from bstack_utils.config import Config
bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll11111_opy_()
@error_handler(class_method=False)
def bstack1lll1ll11l1l_opy_(bs_config, bstack1ll1lllll1_opy_):
  try:
    data = {
        bstack1l111l1_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭⋀"): bstack1l111l1_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ⋁"),
        bstack1l111l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ⋂"): bs_config.get(bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⋃"), bstack1l111l1_opy_ (u"ࠪࠫ⋄")),
        bstack1l111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⋅"): bs_config.get(bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⋆"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⋇"): bs_config.get(bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⋈")),
        bstack1l111l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⋉"): bs_config.get(bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⋊"), bstack1l111l1_opy_ (u"ࠪࠫ⋋")),
        bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⋌"): bstack11llll1111_opy_(),
        bstack1l111l1_opy_ (u"ࠬࡺࡡࡨࡵࠪ⋍"): bstack111l1ll1ll1_opy_(bs_config),
        bstack1l111l1_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ⋎"): get_host_info(),
        bstack1l111l1_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ⋏"): bstack11lll11l1_opy_(),
        bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⋐"): os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⋑")),
        bstack1l111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ⋒"): os.environ.get(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ⋓"), False),
        bstack1l111l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ⋔"): bstack11ll11111ll_opy_(),
        bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⋕"): bstack1lll1l1l1l11_opy_(bs_config),
        bstack1l111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫ⋖"): bstack1lll1l11ll1l_opy_(bstack1ll1lllll1_opy_),
        bstack1l111l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⋗"): bstack1lll1l11l111_opy_(bs_config, bstack1ll1lllll1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⋘"), bstack1l111l1_opy_ (u"ࠪࠫ⋙"))),
        bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⋚"): bstack11lll1lll_opy_(bs_config),
        bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪ⋛"): bstack1lll1l1l11ll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⋜").format(str(error)))
    return None
def bstack1lll1l11ll1l_opy_(framework):
  return {
    bstack1l111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ⋝"): framework.get(bstack1l111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ⋞"), bstack1l111l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⋟")),
    bstack1l111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⋠"): framework.get(bstack1l111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⋡")),
    bstack1l111l1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⋢"): framework.get(bstack1l111l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⋣")),
    bstack1l111l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ⋤"): bstack1l111l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⋥"),
    bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⋦"): framework.get(bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⋧"))
  }
def bstack1lll1l1l11ll_opy_(bs_config):
  bstack1l111l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡳࡵࡣࡵࡸ࠳ࠐࠠࠡࠤࠥࠦ⋨")
  if not bs_config:
    return {}
  bstack1111l111lll_opy_ = bstack1llll111l_opy_(bs_config).bstack1111l1l1111_opy_(bs_config)
  return bstack1111l111lll_opy_
def bstack1ll1ll111_opy_(bs_config, framework):
  bstack1l1l1ll1l_opy_ = False
  bstack11lll11l1l_opy_ = False
  bstack1lll1l1l1111_opy_ = False
  if bstack1l111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⋩") in bs_config:
    bstack1lll1l1l1111_opy_ = True
  elif bstack1l111l1_opy_ (u"࠭ࡡࡱࡲࠪ⋪") in bs_config:
    bstack1l1l1ll1l_opy_ = True
  else:
    bstack11lll11l1l_opy_ = True
  bstack1lll1111l1_opy_ = {
    bstack1l111l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⋫"): bstack11ll11l11_opy_.bstack1lll1l1l1l1l_opy_(bs_config, framework),
    bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⋬"): bstack11111l11l_opy_.bstack11ll1lll1l_opy_(bs_config),
    bstack1l111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⋭"): bs_config.get(bstack1l111l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⋮"), False),
    bstack1l111l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⋯"): bstack11lll11l1l_opy_,
    bstack1l111l1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⋰"): bstack1l1l1ll1l_opy_,
    bstack1l111l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⋱"): bstack1lll1l1l1111_opy_
  }
  return bstack1lll1111l1_opy_
@error_handler(class_method=False)
def bstack1lll1l1l1l11_opy_(bs_config):
  try:
    bstack1lll1l11lll1_opy_ = json.loads(os.getenv(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⋲"), bstack1l111l1_opy_ (u"ࠨࡽࢀࠫ⋳")))
    bstack1lll1l11lll1_opy_ = bstack1lll1l1l11l1_opy_(bs_config, bstack1lll1l11lll1_opy_)
    return {
        bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ⋴"): bstack1lll1l11lll1_opy_
    }
  except Exception as error:
    logger.error(bstack1l111l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⋵").format(str(error)))
    return {}
def bstack1lll1l1l11l1_opy_(bs_config, bstack1lll1l11lll1_opy_):
  if ((bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⋶") in bs_config or not bstack11lll1lll_opy_(bs_config)) and bstack11111l11l_opy_.bstack11ll1lll1l_opy_(bs_config)):
    bstack1lll1l11lll1_opy_[bstack1l111l1_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣ⋷")] = True
  return bstack1lll1l11lll1_opy_
def bstack1lll1l1llll1_opy_(array, bstack1lll1l11l1ll_opy_, bstack1lll1l1l111l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll1l11l1ll_opy_]
    result[key] = o[bstack1lll1l1l111l_opy_]
  return result
def bstack1lll1ll1ll11_opy_(bstack1ll1l1ll11_opy_=bstack1l111l1_opy_ (u"࠭ࠧ⋸")):
  bstack1lll1l11l1l1_opy_ = bstack11111l11l_opy_.on()
  bstack1lll1l11llll_opy_ = bstack11ll11l11_opy_.on()
  bstack1lll1l11ll11_opy_ = percy.bstack1111111l1_opy_()
  if bstack1lll1l11ll11_opy_ and not bstack1lll1l11llll_opy_ and not bstack1lll1l11l1l1_opy_:
    return bstack1ll1l1ll11_opy_ not in [bstack1l111l1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⋹"), bstack1l111l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⋺")]
  elif bstack1lll1l11l1l1_opy_ and not bstack1lll1l11llll_opy_:
    return bstack1ll1l1ll11_opy_ not in [bstack1l111l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⋻"), bstack1l111l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⋼"), bstack1l111l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⋽")]
  return bstack1lll1l11l1l1_opy_ or bstack1lll1l11llll_opy_ or bstack1lll1l11ll11_opy_
@error_handler(class_method=False)
def bstack1lll1ll1l1l1_opy_(bstack1ll1l1ll11_opy_, test=None):
  bstack1lll1l11l11l_opy_ = bstack11111l11l_opy_.on()
  if not bstack1lll1l11l11l_opy_ or bstack1ll1l1ll11_opy_ not in [bstack1l111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⋾")] or test == None:
    return None
  return {
    bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⋿"): bstack1lll1l11l11l_opy_ and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⌀"), None) == True and bstack11111l11l_opy_.bstack11l1l11111_opy_(test[bstack1l111l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⌁")])
  }
def bstack1lll1l11l111_opy_(bs_config, framework):
  bstack1l1l1ll1l_opy_ = False
  bstack11lll11l1l_opy_ = False
  bstack1lll1l1l1111_opy_ = False
  if bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⌂") in bs_config:
    bstack1lll1l1l1111_opy_ = True
  elif bstack1l111l1_opy_ (u"ࠪࡥࡵࡶࠧ⌃") in bs_config:
    bstack1l1l1ll1l_opy_ = True
  else:
    bstack11lll11l1l_opy_ = True
  bstack1lll1111l1_opy_ = {
    bstack1l111l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⌄"): bstack11ll11l11_opy_.bstack1lll1l1l1l1l_opy_(bs_config, framework),
    bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⌅"): bstack11111l11l_opy_.bstack1l1lll11l_opy_(bs_config),
    bstack1l111l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⌆"): bs_config.get(bstack1l111l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⌇"), False),
    bstack1l111l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⌈"): bstack11lll11l1l_opy_,
    bstack1l111l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⌉"): bstack1l1l1ll1l_opy_,
    bstack1l111l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⌊"): bstack1lll1l1l1111_opy_
  }
  return bstack1lll1111l1_opy_