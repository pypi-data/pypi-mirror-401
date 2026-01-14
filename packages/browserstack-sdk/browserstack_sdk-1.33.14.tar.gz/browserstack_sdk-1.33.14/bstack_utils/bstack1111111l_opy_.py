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
import threading
import logging
import bstack_utils.accessibility as bstack1ll1l11lll_opy_
from bstack_utils.helper import bstack1ll1ll11ll_opy_
logger = logging.getLogger(__name__)
def bstack1111ll1l1_opy_(bstack1llll11l11_opy_):
  return True if bstack1llll11l11_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l11l11ll_opy_(context, *args):
    tags = getattr(args[0], bstack1l11l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ᠚"), [])
    bstack1111l11l_opy_ = bstack1ll1l11lll_opy_.bstack1l1l11llll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1111l11l_opy_
    try:
      bstack111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l1_opy_(bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ᠛")) else context.browser
      if bstack111111ll1_opy_ and bstack111111ll1_opy_.session_id and bstack1111l11l_opy_ and bstack1ll1ll11ll_opy_(
              threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᠜"), None):
          threading.current_thread().isA11yTest = bstack1ll1l11lll_opy_.bstack1lllll1ll_opy_(bstack111111ll1_opy_, bstack1111l11l_opy_)
    except Exception as e:
       logger.debug(bstack1l11l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭᠝").format(str(e)))
def bstack1ll1l111ll_opy_(bstack111111ll1_opy_):
    if bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ᠞"), None) and bstack1ll1ll11ll_opy_(
      threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᠟"), None) and not bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᠠ"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll1l11lll_opy_.bstack11ll11l1l_opy_(bstack111111ll1_opy_, name=bstack1l11l1l_opy_ (u"ࠥࠦᠡ"), path=bstack1l11l1l_opy_ (u"ࠦࠧᠢ"))