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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111ll1l111_opy_
bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
def bstack1lllll11111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllll1111ll_opy_(bstack1lllll1111l1_opy_, bstack1llll1lllll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lllll1111l1_opy_):
        with open(bstack1lllll1111l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllll11111l_opy_(bstack1lllll1111l1_opy_):
        pac = get_pac(url=bstack1lllll1111l1_opy_)
    else:
        raise Exception(bstack1l111l1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ⁜").format(bstack1lllll1111l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l111l1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ⁝"), 80))
        bstack1llll1llllll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll1llllll_opy_ = bstack1l111l1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭⁞")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll1lllll1_opy_, bstack1llll1llllll_opy_)
    return proxy_url
def bstack1l1l1ll1_opy_(config):
    return bstack1l111l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ ") in config or bstack1l111l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⁠") in config
def bstack11ll11l1l_opy_(config):
    if not bstack1l1l1ll1_opy_(config):
        return
    if config.get(bstack1l111l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⁡")):
        return config.get(bstack1l111l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⁢"))
    if config.get(bstack1l111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⁣")):
        return config.get(bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⁤"))
def bstack111lll1l1l_opy_(config, bstack1llll1lllll1_opy_):
    proxy = bstack11ll11l1l_opy_(config)
    proxies = {}
    if config.get(bstack1l111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⁥")) or config.get(bstack1l111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⁦")):
        if proxy.endswith(bstack1l111l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ⁧")):
            proxies = bstack1ll1ll11ll_opy_(proxy, bstack1llll1lllll1_opy_)
        else:
            proxies = {
                bstack1l111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⁨"): proxy
            }
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩ⁩"), proxies)
    return proxies
def bstack1ll1ll11ll_opy_(bstack1lllll1111l1_opy_, bstack1llll1lllll1_opy_):
    proxies = {}
    global bstack1llll1llll1l_opy_
    if bstack1l111l1_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭⁪") in globals():
        return bstack1llll1llll1l_opy_
    try:
        proxy = bstack1lllll1111ll_opy_(bstack1lllll1111l1_opy_, bstack1llll1lllll1_opy_)
        if bstack1l111l1_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦ⁫") in proxy:
            proxies = {}
        elif bstack1l111l1_opy_ (u"ࠧࡎࡔࡕࡒࠥ⁬") in proxy or bstack1l111l1_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧ⁭") in proxy or bstack1l111l1_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨ⁮") in proxy:
            bstack1lllll111111_opy_ = proxy.split(bstack1l111l1_opy_ (u"ࠣࠢࠥ⁯"))
            if bstack1l111l1_opy_ (u"ࠤ࠽࠳࠴ࠨ⁰") in bstack1l111l1_opy_ (u"ࠥࠦⁱ").join(bstack1lllll111111_opy_[1:]):
                proxies = {
                    bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⁲"): bstack1l111l1_opy_ (u"ࠧࠨ⁳").join(bstack1lllll111111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⁴"): str(bstack1lllll111111_opy_[0]).lower() + bstack1l111l1_opy_ (u"ࠢ࠻࠱࠲ࠦ⁵") + bstack1l111l1_opy_ (u"ࠣࠤ⁶").join(bstack1lllll111111_opy_[1:])
                }
        elif bstack1l111l1_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣ⁷") in proxy:
            bstack1lllll111111_opy_ = proxy.split(bstack1l111l1_opy_ (u"ࠥࠤࠧ⁸"))
            if bstack1l111l1_opy_ (u"ࠦ࠿࠵࠯ࠣ⁹") in bstack1l111l1_opy_ (u"ࠧࠨ⁺").join(bstack1lllll111111_opy_[1:]):
                proxies = {
                    bstack1l111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⁻"): bstack1l111l1_opy_ (u"ࠢࠣ⁼").join(bstack1lllll111111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⁽"): bstack1l111l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⁾") + bstack1l111l1_opy_ (u"ࠥࠦⁿ").join(bstack1lllll111111_opy_[1:])
                }
        else:
            proxies = {
                bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ₀"): proxy
            }
    except Exception as e:
        print(bstack1l111l1_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ₁"), bstack1111ll1l111_opy_.format(bstack1lllll1111l1_opy_, str(e)))
    bstack1llll1llll1l_opy_ = proxies
    return proxies