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
class RobotHandler():
    def __init__(self, args, logger, bstack1lllllll1l1_opy_, bstack1lllllll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll1l1_opy_ = bstack1lllllll1l1_opy_
        self.bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111ll11l1_opy_(bstack1lllll111l1_opy_):
        bstack1lllll11111_opy_ = []
        if bstack1lllll111l1_opy_:
            tokens = str(os.path.basename(bstack1lllll111l1_opy_)).split(bstack1l111l1_opy_ (u"ࠥࡣࠧᄌ"))
            camelcase_name = bstack1l111l1_opy_ (u"ࠦࠥࠨᄍ").join(t.title() for t in tokens)
            suite_name, bstack1lllll1111l_opy_ = os.path.splitext(camelcase_name)
            bstack1lllll11111_opy_.append(suite_name)
        return bstack1lllll11111_opy_
    @staticmethod
    def bstack1lllll111ll_opy_(typename):
        if bstack1l111l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᄎ") in typename:
            return bstack1l111l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᄏ")
        return bstack1l111l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᄐ")