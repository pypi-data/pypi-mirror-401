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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l111l11l_opy_():
  def __init__(self, args, logger, bstack1lllllll1l1_opy_, bstack1lllllll1ll_opy_, bstack1lllll11l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllllll1l1_opy_ = bstack1lllllll1l1_opy_
    self.bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_
    self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
  def bstack1lllll11_opy_(self, bstack1lllll1l1ll_opy_, bstack11lllll1l1_opy_, bstack1lllll11l11_opy_=False):
    bstack1l1lll111l_opy_ = []
    manager = multiprocessing.Manager()
    bstack111111l111_opy_ = manager.list()
    bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
    if bstack1lllll11l11_opy_:
      for index, platform in enumerate(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄅ")]):
        if index == 0:
          bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᄆ")] = self.args
        bstack1l1lll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lllll1l1ll_opy_,
                                                    args=(bstack11lllll1l1_opy_, bstack111111l111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄇ")]):
        bstack1l1lll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lllll1l1ll_opy_,
                                                    args=(bstack11lllll1l1_opy_, bstack111111l111_opy_)))
    i = 0
    for t in bstack1l1lll111l_opy_:
      try:
        if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᄈ")):
          os.environ[bstack1l111l1_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᄉ")] = json.dumps(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄊ")][i % self.bstack1lllll11l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᄋ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1lll111l_opy_:
      t.join()
    return list(bstack111111l111_opy_)