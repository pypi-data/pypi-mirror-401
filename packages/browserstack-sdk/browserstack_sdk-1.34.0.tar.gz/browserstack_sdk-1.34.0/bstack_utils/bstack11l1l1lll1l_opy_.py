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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l11lll111_opy_
logger = logging.getLogger(__name__)
class bstack11l1l1ll1ll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llll1l11111_opy_ = urljoin(builder, bstack1l111l1_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨ₼"))
        if params:
            bstack1llll1l11111_opy_ += bstack1l111l1_opy_ (u"ࠤࡂࡿࢂࠨ₽").format(urlencode({bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ₾"): params.get(bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₿"))}))
        return bstack11l1l1ll1ll_opy_.bstack1llll1l1111l_opy_(bstack1llll1l11111_opy_)
    @staticmethod
    def bstack11l1l1llll1_opy_(builder,params=None):
        bstack1llll1l11111_opy_ = urljoin(builder, bstack1l111l1_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭⃀"))
        if params:
            bstack1llll1l11111_opy_ += bstack1l111l1_opy_ (u"ࠨ࠿ࡼࡿࠥ⃁").format(urlencode({bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃂"): params.get(bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃃"))}))
        return bstack11l1l1ll1ll_opy_.bstack1llll1l1111l_opy_(bstack1llll1l11111_opy_)
    @staticmethod
    def bstack1llll1l1111l_opy_(bstack1llll11lll11_opy_):
        bstack1llll11lll1l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⃄"), os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⃅"), bstack1l111l1_opy_ (u"ࠫࠬ⃆")))
        headers = {bstack1l111l1_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⃇"): bstack1l111l1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⃈").format(bstack1llll11lll1l_opy_)}
        response = requests.get(bstack1llll11lll11_opy_, headers=headers)
        bstack1llll11llll1_opy_ = {}
        try:
            bstack1llll11llll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⃉").format(e))
            pass
        if bstack1llll11llll1_opy_ is not None:
            bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⃊")] = response.headers.get(bstack1l111l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⃋"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⃌")] = response.status_code
        return bstack1llll11llll1_opy_
    @staticmethod
    def bstack1llll11lllll_opy_(bstack1llll11ll1l1_opy_, data):
        logger.debug(bstack1l111l1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࠨ⃍"))
        return bstack11l1l1ll1ll_opy_.bstack1llll1l111l1_opy_(bstack1l111l1_opy_ (u"ࠬࡖࡏࡔࡖࠪ⃎"), bstack1llll11ll1l1_opy_, data=data)
    @staticmethod
    def bstack1llll11ll1ll_opy_(bstack1llll11ll1l1_opy_, data):
        logger.debug(bstack1l111l1_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡩࡨࡸ࡙࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡸࠨ⃏"))
        res = bstack11l1l1ll1ll_opy_.bstack1llll1l111l1_opy_(bstack1l111l1_opy_ (u"ࠧࡈࡇࡗࠫ⃐"), bstack1llll11ll1l1_opy_, data=data)
        return res
    @staticmethod
    def bstack1llll1l111l1_opy_(method, bstack1llll11ll1l1_opy_, data=None, params=None, extra_headers=None):
        bstack1llll11lll1l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃑"), bstack1l111l1_opy_ (u"⃒ࠩࠪ"))
        headers = {
            bstack1l111l1_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰ⃓ࠪ"): bstack1l111l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⃔").format(bstack1llll11lll1l_opy_),
            bstack1l111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⃕"): bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⃖"),
            bstack1l111l1_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧ⃗"): bstack1l111l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱ⃘ࠫ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l11lll111_opy_ + bstack1l111l1_opy_ (u"ࠤ࠲⃙ࠦ") + bstack1llll11ll1l1_opy_.lstrip(bstack1l111l1_opy_ (u"ࠪ࠳⃚ࠬ"))
        try:
            if method == bstack1l111l1_opy_ (u"ࠫࡌࡋࡔࠨ⃛"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l111l1_opy_ (u"ࠬࡖࡏࡔࡖࠪ⃜"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l111l1_opy_ (u"࠭ࡐࡖࡖࠪ⃝"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l111l1_opy_ (u"ࠢࡖࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ⃞").format(method))
            logger.debug(bstack1l111l1_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡰࡥࡩ࡫ࠠࡵࡱ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ⃟").format(url, method))
            bstack1llll11llll1_opy_ = {}
            try:
                bstack1llll11llll1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l111l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⃠").format(e, response.text))
            if bstack1llll11llll1_opy_ is not None:
                bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⃡")] = response.headers.get(
                    bstack1l111l1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⃢"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⃣")] = response.status_code
            return bstack1llll11llll1_opy_
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⃤").format(e, url))
            return None
    @staticmethod
    def bstack11l11l11l11_opy_(bstack1llll11lll11_opy_, data):
        bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡖࡕࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤ⃥ࠥࠦࠠࠡࠢࠥࠦࠧ")
        bstack1llll11lll1l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘ⃦ࠬ"), bstack1l111l1_opy_ (u"ࠩࠪ⃧"))
        headers = {
            bstack1l111l1_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰ⃨ࠪ"): bstack1l111l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⃩").format(bstack1llll11lll1l_opy_),
            bstack1l111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨ⃪ࠫ"): bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯⃫ࠩ")
        }
        response = requests.put(bstack1llll11lll11_opy_, headers=headers, json=data)
        bstack1llll11llll1_opy_ = {}
        try:
            bstack1llll11llll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⃬").format(e))
            pass
        logger.debug(bstack1l111l1_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡲࡸࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿ⃭ࠥ").format(bstack1llll11llll1_opy_))
        if bstack1llll11llll1_opy_ is not None:
            bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧ⃮ࠪ")] = response.headers.get(
                bstack1l111l1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨ⃯ࠫ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⃰")] = response.status_code
        return bstack1llll11llll1_opy_
    @staticmethod
    def bstack11l111llll1_opy_(bstack1llll11lll11_opy_):
        bstack1l111l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡬࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⃱")
        bstack1llll11lll1l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⃲"), bstack1l111l1_opy_ (u"ࠧࠨ⃳"))
        headers = {
            bstack1l111l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⃴"): bstack1l111l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⃵").format(bstack1llll11lll1l_opy_),
            bstack1l111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⃶"): bstack1l111l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⃷")
        }
        response = requests.get(bstack1llll11lll11_opy_, headers=headers)
        bstack1llll11llll1_opy_ = {}
        try:
            bstack1llll11llll1_opy_ = response.json()
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥ࡭ࡥࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⃸").format(bstack1llll11llll1_opy_))
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⃹").format(e, response.text))
            pass
        if bstack1llll11llll1_opy_ is not None:
            bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⃺")] = response.headers.get(
                bstack1l111l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⃻"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llll11llll1_opy_[bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⃼")] = response.status_code
        return bstack1llll11llll1_opy_
    @staticmethod
    def bstack11111l11ll1_opy_(bstack11l1ll111ll_opy_, payload):
        bstack1l111l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡣ࡮ࡩࡸࠦࡡࠡࡒࡒࡗ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩࠥࡇࡐࡊࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡽࡱࡵࡡࡥࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡲࡤࡽࡱࡵࡡࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡂࡒࡌ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⃽")
        try:
            url = bstack1l111l1_opy_ (u"ࠦࢀࢃ࠯ࡼࡿࠥ⃾").format(bstack11l11lll111_opy_, bstack11l1ll111ll_opy_)
            bstack1llll11lll1l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⃿"), bstack1l111l1_opy_ (u"࠭ࠧ℀"))
            headers = {
                bstack1l111l1_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ℁"): bstack1l111l1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫℂ").format(bstack1llll11lll1l_opy_),
                bstack1l111l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ℃"): bstack1l111l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭℄")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1llll1l111ll_opy_ = [200, 202]
            if response.status_code in bstack1llll1l111ll_opy_:
                return response.json()
            else:
                logger.error(bstack1l111l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥ࠳ࠦࡓࡵࡣࡷࡹࡸࡀࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ℅").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡳࡵࡡࡦࡳࡱࡲࡥࡤࡶࡢࡦࡺ࡯࡬ࡥࡡࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ℆").format(e))
            return None