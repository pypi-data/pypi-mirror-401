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
class RobotHandler():
    def __init__(self, args, logger, bstack1lllllll1ll_opy_, bstack1111111l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_
        self.bstack1111111l11_opy_ = bstack1111111l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111lll1l1_opy_(bstack1lllll1ll1l_opy_):
        bstack1lllll1l1l1_opy_ = []
        if bstack1lllll1ll1l_opy_:
            tokens = str(os.path.basename(bstack1lllll1ll1l_opy_)).split(bstack1l11l1l_opy_ (u"ࠧࡥࠢძ"))
            camelcase_name = bstack1l11l1l_opy_ (u"ࠨࠠࠣწ").join(t.title() for t in tokens)
            suite_name, bstack1lllll1l1ll_opy_ = os.path.splitext(camelcase_name)
            bstack1lllll1l1l1_opy_.append(suite_name)
        return bstack1lllll1l1l1_opy_
    @staticmethod
    def bstack1lllll1ll11_opy_(typename):
        if bstack1l11l1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥჭ") in typename:
            return bstack1l11l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤხ")
        return bstack1l11l1l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥჯ")