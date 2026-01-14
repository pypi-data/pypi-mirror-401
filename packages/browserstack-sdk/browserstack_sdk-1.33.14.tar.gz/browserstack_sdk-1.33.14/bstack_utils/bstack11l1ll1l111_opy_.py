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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1l111l1l_opy_
logger = logging.getLogger(__name__)
class bstack11l1ll11lll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llll1l1l11l_opy_ = urljoin(builder, bstack1l11l1l_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪₛ"))
        if params:
            bstack1llll1l1l11l_opy_ += bstack1l11l1l_opy_ (u"ࠦࡄࢁࡽࠣₜ").format(urlencode({bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ₝"): params.get(bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭₞"))}))
        return bstack11l1ll11lll_opy_.bstack1llll1l111ll_opy_(bstack1llll1l1l11l_opy_)
    @staticmethod
    def bstack11l1ll1l1ll_opy_(builder,params=None):
        bstack1llll1l1l11l_opy_ = urljoin(builder, bstack1l11l1l_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨ₟"))
        if params:
            bstack1llll1l1l11l_opy_ += bstack1l11l1l_opy_ (u"ࠣࡁࡾࢁࠧ₠").format(urlencode({bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ₡"): params.get(bstack1l11l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ₢"))}))
        return bstack11l1ll11lll_opy_.bstack1llll1l111ll_opy_(bstack1llll1l1l11l_opy_)
    @staticmethod
    def bstack1llll1l111ll_opy_(bstack1llll1l11ll1_opy_):
        bstack1llll1l1l111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ₣"), os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ₤"), bstack1l11l1l_opy_ (u"࠭ࠧ₥")))
        headers = {bstack1l11l1l_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ₦"): bstack1l11l1l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ₧").format(bstack1llll1l1l111_opy_)}
        response = requests.get(bstack1llll1l11ll1_opy_, headers=headers)
        bstack1llll1l1l1ll_opy_ = {}
        try:
            bstack1llll1l1l1ll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ₨").format(e))
            pass
        if bstack1llll1l1l1ll_opy_ is not None:
            bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ₩")] = response.headers.get(bstack1l11l1l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ₪"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ₫")] = response.status_code
        return bstack1llll1l1l1ll_opy_
    @staticmethod
    def bstack1llll1l11l11_opy_(bstack1llll1l1l1l1_opy_, data):
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࠣ€"))
        return bstack11l1ll11lll_opy_.bstack1llll1l1ll11_opy_(bstack1l11l1l_opy_ (u"ࠧࡑࡑࡖࡘࠬ₭"), bstack1llll1l1l1l1_opy_, data=data)
    @staticmethod
    def bstack1llll1l11lll_opy_(bstack1llll1l1l1l1_opy_, data):
        logger.debug(bstack1l11l1l_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣ࡫ࡪࡺࡔࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡳࠣ₮"))
        res = bstack11l1ll11lll_opy_.bstack1llll1l1ll11_opy_(bstack1l11l1l_opy_ (u"ࠩࡊࡉ࡙࠭₯"), bstack1llll1l1l1l1_opy_, data=data)
        return res
    @staticmethod
    def bstack1llll1l1ll11_opy_(method, bstack1llll1l1l1l1_opy_, data=None, params=None, extra_headers=None):
        bstack1llll1l1l111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ₰"), bstack1l11l1l_opy_ (u"ࠫࠬ₱"))
        headers = {
            bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ₲"): bstack1l11l1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ₳").format(bstack1llll1l1l111_opy_),
            bstack1l11l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭₴"): bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ₵"),
            bstack1l11l1l_opy_ (u"ࠩࡄࡧࡨ࡫ࡰࡵࠩ₶"): bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭₷")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1l111l1l_opy_ + bstack1l11l1l_opy_ (u"ࠦ࠴ࠨ₸") + bstack1llll1l1l1l1_opy_.lstrip(bstack1l11l1l_opy_ (u"ࠬ࠵ࠧ₹"))
        try:
            if method == bstack1l11l1l_opy_ (u"࠭ࡇࡆࡖࠪ₺"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l11l1l_opy_ (u"ࠧࡑࡑࡖࡘࠬ₻"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l11l1l_opy_ (u"ࠨࡒࡘࡘࠬ₼"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l11l1l_opy_ (u"ࠤࡘࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤ₽").format(method))
            logger.debug(bstack1l11l1l_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤࡲࡧࡤࡦࠢࡷࡳ࡛ࠥࡒࡍ࠼ࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣ₾").format(url, method))
            bstack1llll1l1l1ll_opy_ = {}
            try:
                bstack1llll1l1l1ll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l11l1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ₿").format(e, response.text))
            if bstack1llll1l1l1ll_opy_ is not None:
                bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⃀")] = response.headers.get(
                    bstack1l11l1l_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⃁"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⃂")] = response.status_code
            return bstack1llll1l1l1ll_opy_
        except Exception as e:
            logger.error(bstack1l11l1l_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ⃃").format(e, url))
            return None
    @staticmethod
    def bstack11l11l11l11_opy_(bstack1llll1l11ll1_opy_, data):
        bstack1l11l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡑࡗࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⃄")
        bstack1llll1l1l111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⃅"), bstack1l11l1l_opy_ (u"ࠫࠬ⃆"))
        headers = {
            bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⃇"): bstack1l11l1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⃈").format(bstack1llll1l1l111_opy_),
            bstack1l11l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⃉"): bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⃊")
        }
        response = requests.put(bstack1llll1l11ll1_opy_, headers=headers, json=data)
        bstack1llll1l1l1ll_opy_ = {}
        try:
            bstack1llll1l1l1ll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⃋").format(e))
            pass
        logger.debug(bstack1l11l1l_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣࡴࡺࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⃌").format(bstack1llll1l1l1ll_opy_))
        if bstack1llll1l1l1ll_opy_ is not None:
            bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⃍")] = response.headers.get(
                bstack1l11l1l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⃎"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⃏")] = response.status_code
        return bstack1llll1l1l1ll_opy_
    @staticmethod
    def bstack11l111lll1l_opy_(bstack1llll1l11ll1_opy_):
        bstack1l11l1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡧࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⃐")
        bstack1llll1l1l111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃑"), bstack1l11l1l_opy_ (u"⃒ࠩࠪ"))
        headers = {
            bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰ⃓ࠪ"): bstack1l11l1l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⃔").format(bstack1llll1l1l111_opy_),
            bstack1l11l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⃕"): bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⃖")
        }
        response = requests.get(bstack1llll1l11ll1_opy_, headers=headers)
        bstack1llll1l1l1ll_opy_ = {}
        try:
            bstack1llll1l1l1ll_opy_ = response.json()
            logger.debug(bstack1l11l1l_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡨࡧࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⃗").format(bstack1llll1l1l1ll_opy_))
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁ⃘ࠧ").format(e, response.text))
            pass
        if bstack1llll1l1l1ll_opy_ is not None:
            bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧ⃙ࠪ")] = response.headers.get(
                bstack1l11l1l_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨ⃚ࠫ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llll1l1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⃛")] = response.status_code
        return bstack1llll1l1l1ll_opy_
    @staticmethod
    def bstack1111l1lllll_opy_(bstack11l1ll1ll1l_opy_, payload):
        bstack1l11l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡥࡰ࡫ࡳࠡࡣࠣࡔࡔ࡙ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡂࡒࡌࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡵࡩࡶࡻࡥࡴࡶࠣࡴࡦࡿ࡬ࡰࡣࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡄࡔࡎ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⃜")
        try:
            url = bstack1l11l1l_opy_ (u"ࠨࡻࡾ࠱ࡾࢁࠧ⃝").format(bstack11l1l111l1l_opy_, bstack11l1ll1ll1l_opy_)
            bstack1llll1l1l111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⃞"), bstack1l11l1l_opy_ (u"ࠨࠩ⃟"))
            headers = {
                bstack1l11l1l_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⃠"): bstack1l11l1l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⃡").format(bstack1llll1l1l111_opy_),
                bstack1l11l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⃢"): bstack1l11l1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⃣")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1llll1l11l1l_opy_ = [200, 202]
            if response.status_code in bstack1llll1l11l1l_opy_:
                return response.json()
            else:
                logger.error(bstack1l11l1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧ࠮ࠡࡕࡷࡥࡹࡻࡳ࠻ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⃤").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l11l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡵࡷࡣࡨࡵ࡬࡭ࡧࡦࡸࡤࡨࡵࡪ࡮ࡧࡣࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⃥").format(e))
            return None