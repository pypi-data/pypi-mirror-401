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
import builtins
import logging
class bstack111l1l1l11_opy_:
    def __init__(self, handler):
        self._11l1l1lllll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l1l1lll1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᠣ"), bstack1l11l1l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᠤ"), bstack1l11l1l_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᠥ"), bstack1l11l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᠦ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l1l1lll11_opy_
        self._11l1l1llll1_opy_()
    def _11l1l1lll11_opy_(self, *args, **kwargs):
        self._11l1l1lllll_opy_(*args, **kwargs)
        message = bstack1l11l1l_opy_ (u"ࠩࠣࠫᠧ").join(map(str, args)) + bstack1l11l1l_opy_ (u"ࠪࡠࡳ࠭ᠨ")
        self._11l1ll111l1_opy_(bstack1l11l1l_opy_ (u"ࠫࡎࡔࡆࡐࠩᠩ"), message)
    def _11l1ll111l1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l11l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᠪ"): level, bstack1l11l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᠫ"): msg})
    def _11l1l1llll1_opy_(self):
        for level, bstack11l1ll1111l_opy_ in self._11l1l1lll1l_opy_.items():
            setattr(logging, level, self._11l1ll11111_opy_(level, bstack11l1ll1111l_opy_))
    def _11l1ll11111_opy_(self, level, bstack11l1ll1111l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l1ll1111l_opy_(msg, *args, **kwargs)
            self._11l1ll111l1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l1l1lllll_opy_
        for level, bstack11l1ll1111l_opy_ in self._11l1l1lll1l_opy_.items():
            setattr(logging, level, bstack11l1ll1111l_opy_)