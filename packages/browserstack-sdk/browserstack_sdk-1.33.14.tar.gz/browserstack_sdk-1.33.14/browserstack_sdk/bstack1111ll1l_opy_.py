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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11llll1ll_opy_():
  def __init__(self, args, logger, bstack1lllllll1ll_opy_, bstack1111111l11_opy_, bstack1lllll1lll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_
    self.bstack1111111l11_opy_ = bstack1111111l11_opy_
    self.bstack1lllll1lll1_opy_ = bstack1lllll1lll1_opy_
  def bstack1l1lllll1l_opy_(self, bstack11111l11ll_opy_, bstack1l1lllllll_opy_, bstack1lllll1llll_opy_=False):
    bstack1111llll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lllllll111_opy_ = manager.list()
    bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
    if bstack1lllll1llll_opy_:
      for index, platform in enumerate(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨფ")]):
        if index == 0:
          bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩქ")] = self.args
        bstack1111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111l11ll_opy_,
                                                    args=(bstack1l1lllllll_opy_, bstack1lllllll111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪღ")]):
        bstack1111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111l11ll_opy_,
                                                    args=(bstack1l1lllllll_opy_, bstack1lllllll111_opy_)))
    i = 0
    for t in bstack1111llll_opy_:
      try:
        if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩყ")):
          os.environ[bstack1l11l1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪშ")] = json.dumps(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ჩ")][i % self.bstack1lllll1lll1_opy_])
      except Exception as e:
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦც").format(str(e)))
      i += 1
      t.start()
    for t in bstack1111llll_opy_:
      t.join()
    return list(bstack1lllllll111_opy_)