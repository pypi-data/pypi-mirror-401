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
class bstack1l1l1l1l1l_opy_:
    def __init__(self, handler):
        self._1llll11l1ll1_opy_ = None
        self.handler = handler
        self._1llll11ll111_opy_ = self.bstack1llll11ll11l_opy_()
        self.patch()
    def patch(self):
        self._1llll11l1ll1_opy_ = self._1llll11ll111_opy_.execute
        self._1llll11ll111_opy_.execute = self.bstack1llll11l1lll_opy_()
    def bstack1llll11l1lll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l111l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨℇ"), driver_command, None, this, args)
            response = self._1llll11l1ll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l111l1_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ℈"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll11ll111_opy_.execute = self._1llll11l1ll1_opy_
    @staticmethod
    def bstack1llll11ll11l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver