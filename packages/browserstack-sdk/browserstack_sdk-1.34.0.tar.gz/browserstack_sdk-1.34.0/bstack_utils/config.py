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
conf = {
    bstack1l111l1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᡍ"): False,
    bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᡎ"): True,
    bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭ᡏ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11l1l1l111l_opy_ = conf
    @classmethod
    def bstack1llll1ll11_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11l1l1l1111_opy_=None):
        return self._11l1l1l111l_opy_.get(property_name, bstack11l1l1l1111_opy_)
    def bstack11ll11l11l_opy_(self, property_name, bstack11l1l11llll_opy_):
        self._11l1l1l111l_opy_[property_name] = bstack11l1l11llll_opy_
    def bstack1l1ll111_opy_(self, val):
        self._11l1l1l111l_opy_[bstack1l111l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧᡐ")] = bool(val)
    def bstack1llllll1lll_opy_(self):
        return self._11l1l1l111l_opy_.get(bstack1l111l1_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᡑ"), False)