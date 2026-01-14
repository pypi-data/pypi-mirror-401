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
conf = {
    bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᠬ"): False,
    bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᠭ"): True,
    bstack1l11l1l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᠮ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11l1l1ll1l1_opy_ = conf
    @classmethod
    def bstack1llll1111_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11l1l1ll11l_opy_=None):
        return self._11l1l1ll1l1_opy_.get(property_name, bstack11l1l1ll11l_opy_)
    def bstack11ll1l111l_opy_(self, property_name, bstack11l1l1ll1ll_opy_):
        self._11l1l1ll1l1_opy_[property_name] = bstack11l1l1ll1ll_opy_
    def bstack1ll111ll1l_opy_(self, val):
        self._11l1l1ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩᠯ")] = bool(val)
    def bstack111111ll1l_opy_(self):
        return self._11l1l1ll1l1_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᠰ"), False)