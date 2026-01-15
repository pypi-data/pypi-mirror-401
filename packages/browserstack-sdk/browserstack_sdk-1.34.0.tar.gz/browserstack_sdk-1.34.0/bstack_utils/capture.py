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
import builtins
import logging
class bstack111l1lll11_opy_:
    def __init__(self, handler):
        self._11l1l1l1ll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l1l1l11l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l111l1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᡄ"), bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᡅ"), bstack1l111l1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᡆ"), bstack1l111l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᡇ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l1l1l1l1l_opy_
        self._11l1l1ll111_opy_()
    def _11l1l1l1l1l_opy_(self, *args, **kwargs):
        self._11l1l1l1ll1_opy_(*args, **kwargs)
        message = bstack1l111l1_opy_ (u"ࠧࠡࠩᡈ").join(map(str, args)) + bstack1l111l1_opy_ (u"ࠨ࡞ࡱࠫᡉ")
        self._11l1l1l1l11_opy_(bstack1l111l1_opy_ (u"ࠩࡌࡒࡋࡕࠧᡊ"), message)
    def _11l1l1l1l11_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᡋ"): level, bstack1l111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᡌ"): msg})
    def _11l1l1ll111_opy_(self):
        for level, bstack11l1l1l11ll_opy_ in self._11l1l1l11l1_opy_.items():
            setattr(logging, level, self._11l1l1l1lll_opy_(level, bstack11l1l1l11ll_opy_))
    def _11l1l1l1lll_opy_(self, level, bstack11l1l1l11ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l1l1l11ll_opy_(msg, *args, **kwargs)
            self._11l1l1l1l11_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l1l1l1ll1_opy_
        for level, bstack11l1l1l11ll_opy_ in self._11l1l1l11l1_opy_.items():
            setattr(logging, level, bstack11l1l1l11ll_opy_)