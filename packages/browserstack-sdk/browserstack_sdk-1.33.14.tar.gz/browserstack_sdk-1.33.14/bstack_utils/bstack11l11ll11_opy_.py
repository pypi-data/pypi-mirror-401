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
class bstack111lll1l_opy_:
    def __init__(self, handler):
        self._1llll1l1111l_opy_ = None
        self.handler = handler
        self._1llll1l111l1_opy_ = self.bstack1llll1l11111_opy_()
        self.patch()
    def patch(self):
        self._1llll1l1111l_opy_ = self._1llll1l111l1_opy_.execute
        self._1llll1l111l1_opy_.execute = self.bstack1llll11lllll_opy_()
    def bstack1llll11lllll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11l1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥ⃦ࠣ"), driver_command, None, this, args)
            response = self._1llll1l1111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11l1l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣ⃧"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1l111l1_opy_.execute = self._1llll1l1111l_opy_
    @staticmethod
    def bstack1llll1l11111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver