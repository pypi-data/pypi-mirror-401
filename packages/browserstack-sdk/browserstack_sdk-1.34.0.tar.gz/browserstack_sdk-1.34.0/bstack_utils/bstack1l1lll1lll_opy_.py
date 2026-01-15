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
import threading
import logging
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.helper import bstack1l1l1l111_opy_
logger = logging.getLogger(__name__)
def bstack1l1l1l11ll_opy_(bstack1l11ll1111_opy_):
  return True if bstack1l11ll1111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1lllll1l11_opy_(context, *args):
    tags = getattr(args[0], bstack1l111l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᠻ"), [])
    bstack11lll1l11_opy_ = bstack11111l11l_opy_.bstack11l1l11111_opy_(tags)
    threading.current_thread().isA11yTest = bstack11lll1l11_opy_
    try:
      bstack1l1l11lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l11ll_opy_(bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᠼ")) else context.browser
      if bstack1l1l11lll1_opy_ and bstack1l1l11lll1_opy_.session_id and bstack11lll1l11_opy_ and bstack1l1l1l111_opy_(
              threading.current_thread(), bstack1l111l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᠽ"), None):
          threading.current_thread().isA11yTest = bstack11111l11l_opy_.bstack111l1ll1l_opy_(bstack1l1l11lll1_opy_, bstack11lll1l11_opy_)
    except Exception as e:
       logger.debug(bstack1l111l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᠾ").format(str(e)))
def bstack111ll111_opy_(bstack1l1l11lll1_opy_):
    if bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᠿ"), None) and bstack1l1l1l111_opy_(
      threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᡀ"), None) and not bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪᡁ"), False):
      threading.current_thread().a11y_stop = True
      bstack11111l11l_opy_.bstack1lll1l1l_opy_(bstack1l1l11lll1_opy_, name=bstack1l111l1_opy_ (u"ࠣࠤᡂ"), path=bstack1l111l1_opy_ (u"ࠤࠥᡃ"))