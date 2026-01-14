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
from bstack_utils.constants import bstack11l1ll1ll11_opy_
def bstack11lllll11l_opy_(bstack11l1ll1ll1l_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11l11l1l1l_opy_
    host = bstack11l11l1l1l_opy_(cli.config, [bstack1l11l1l_opy_ (u"ࠥࡥࡵ࡯ࡳࠣ᠌"), bstack1l11l1l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ᠍"), bstack1l11l1l_opy_ (u"ࠧࡧࡰࡪࠤ᠎")], bstack11l1ll1ll11_opy_)
    return bstack1l11l1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ᠏").format(host, bstack11l1ll1ll1l_opy_)