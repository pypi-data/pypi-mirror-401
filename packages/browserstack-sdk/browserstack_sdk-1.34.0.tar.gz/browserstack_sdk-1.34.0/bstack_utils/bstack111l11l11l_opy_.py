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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1ll1llll_opy_, bstack11l1llll1l1_opy_, bstack11l1l1l1l_opy_, error_handler, bstack111lll1111l_opy_, bstack111ll1l1ll1_opy_, bstack111lll111ll_opy_, bstack11llll1111_opy_, bstack1l1l1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llll1l1lll1_opy_ import bstack1llll1l11l11_opy_
import bstack_utils.bstack11llll111l_opy_ as bstack1l11111ll1_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11ll11l11_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack1l111l1l_opy_ import bstack1l111l1l_opy_
from bstack_utils.bstack111l11l1l1_opy_ import bstack111l1111ll_opy_
from bstack_utils.constants import bstack1ll1l1l11_opy_
bstack1lll1ll11l11_opy_ = bstack1l111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ⇃")
logger = logging.getLogger(__name__)
class bstack1llll1lll1_opy_:
    bstack1llll1l1lll1_opy_ = None
    bs_config = None
    bstack1ll1lllll1_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l11ll11ll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def launch(cls, bs_config, bstack1ll1lllll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll1lllll1_opy_ = bstack1ll1lllll1_opy_
        try:
            cls.bstack1lll1ll1llll_opy_()
            bstack11l1llll1ll_opy_ = bstack11l1ll1llll_opy_(bs_config)
            bstack11ll1111ll1_opy_ = bstack11l1llll1l1_opy_(bs_config)
            data = bstack1l11111ll1_opy_.bstack1lll1ll11l1l_opy_(bs_config, bstack1ll1lllll1_opy_)
            config = {
                bstack1l111l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ⇄"): (bstack11l1llll1ll_opy_, bstack11ll1111ll1_opy_),
                bstack1l111l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⇅"): cls.default_headers()
            }
            response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭⇆"), cls.request_url(bstack1l111l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩ⇇")), data, config)
            if response.status_code != 200:
                bstack11llll1l1_opy_ = response.json()
                if bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⇈")] == False:
                    cls.bstack1lll1l1ll1l1_opy_(bstack11llll1l1_opy_)
                    return
                cls.bstack1lll1ll1l111_opy_(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⇉")])
                cls.bstack1lll1l1ll11l_opy_(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⇊")])
                return None
            bstack1lll1l1ll1ll_opy_ = cls.bstack1lll1ll11lll_opy_(response)
            return bstack1lll1l1ll1ll_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦ⇋").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1lll1ll11111_opy_=None):
        if not bstack11ll11l11_opy_.on() and not bstack11111l11l_opy_.on():
            return
        if os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⇌")) == bstack1l111l1_opy_ (u"ࠣࡰࡸࡰࡱࠨ⇍") or os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⇎")) == bstack1l111l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⇏"):
            logger.error(bstack1l111l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ⇐"))
            return {
                bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⇑"): bstack1l111l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⇒"),
                bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⇓"): bstack1l111l1_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭⇔")
            }
        try:
            cls.bstack1llll1l1lll1_opy_.shutdown()
            data = {
                bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⇕"): bstack11llll1111_opy_()
            }
            if not bstack1lll1ll11111_opy_ is None:
                data[bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ⇖")] = [{
                    bstack1l111l1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ⇗"): bstack1l111l1_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ⇘"),
                    bstack1l111l1_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭⇙"): bstack1lll1ll11111_opy_
                }]
            config = {
                bstack1l111l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⇚"): cls.default_headers()
            }
            bstack11l1ll111ll_opy_ = bstack1l111l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩ⇛").format(os.environ[bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⇜")])
            bstack1lll1l1l1ll1_opy_ = cls.request_url(bstack11l1ll111ll_opy_)
            response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠪࡔ࡚࡚ࠧ⇝"), bstack1lll1l1l1ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l111l1_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥ⇞"))
        except Exception as error:
            logger.error(bstack1l111l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤ⇟") + str(error))
            return {
                bstack1l111l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⇠"): bstack1l111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⇡"),
                bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⇢"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll1ll11lll_opy_(cls, response):
        bstack11llll1l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lll1l1ll1ll_opy_ = {}
        if bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠩ࡭ࡻࡹ࠭⇣")) is None:
            os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⇤")] = bstack1l111l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⇥")
        else:
            os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⇦")] = bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"࠭ࡪࡸࡶࠪ⇧"), bstack1l111l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⇨"))
        os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⇩")] = bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⇪"), bstack1l111l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⇫"))
        logger.info(bstack1l111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩ⇬") + os.getenv(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⇭")));
        if bstack11ll11l11_opy_.bstack1lll1l1lllll_opy_(cls.bs_config, cls.bstack1ll1lllll1_opy_.get(bstack1l111l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ⇮"), bstack1l111l1_opy_ (u"ࠧࠨ⇯"))) is True:
            bstack1llll11lll1l_opy_, build_hashed_id, bstack1lll1ll1ll1l_opy_ = cls.bstack1lll1ll111l1_opy_(bstack11llll1l1_opy_)
            if bstack1llll11lll1l_opy_ != None and build_hashed_id != None:
                bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⇰")] = {
                    bstack1l111l1_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬ⇱"): bstack1llll11lll1l_opy_,
                    bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⇲"): build_hashed_id,
                    bstack1l111l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⇳"): bstack1lll1ll1ll1l_opy_
                }
            else:
                bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⇴")] = {}
        else:
            bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⇵")] = {}
        bstack1lll1l1l1lll_opy_, build_hashed_id = cls.bstack1lll1l1ll111_opy_(bstack11llll1l1_opy_)
        if bstack1lll1l1l1lll_opy_ != None and build_hashed_id != None:
            bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⇶")] = {
                bstack1l111l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬ⇷"): bstack1lll1l1l1lll_opy_,
                bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⇸"): build_hashed_id,
            }
        else:
            bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⇹")] = {}
        if bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⇺")].get(bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⇻")) != None or bstack1lll1l1ll1ll_opy_[bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⇼")].get(bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⇽")) != None:
            cls.bstack1lll1ll11ll1_opy_(bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠨ࡬ࡺࡸࠬ⇾")), bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⇿")))
        return bstack1lll1l1ll1ll_opy_
    @classmethod
    def bstack1lll1ll111l1_opy_(cls, bstack11llll1l1_opy_):
        if bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ∀")) == None:
            cls.bstack1lll1ll1l111_opy_()
            return [None, None, None]
        if bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ∁")][bstack1l111l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭∂")] != True:
            cls.bstack1lll1ll1l111_opy_(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭∃")])
            return [None, None, None]
        logger.debug(bstack1l111l1_opy_ (u"ࠧࡼࡿࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩ∄").format(bstack1ll1l1l11_opy_))
        os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ∅")] = bstack1l111l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ∆")
        if bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠪ࡮ࡼࡺࠧ∇")):
            os.environ[bstack1l111l1_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨ∈")] = json.dumps({
                bstack1l111l1_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ∉"): bstack11l1ll1llll_opy_(cls.bs_config),
                bstack1l111l1_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨ∊"): bstack11l1llll1l1_opy_(cls.bs_config)
            })
        if bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ∋")):
            os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ∌")] = bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ∍")]
        if bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ∎")].get(bstack1l111l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ∏"), {}).get(bstack1l111l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ∐")):
            os.environ[bstack1l111l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ∑")] = str(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ−")][bstack1l111l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ∓")][bstack1l111l1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭∔")])
        else:
            os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ∕")] = bstack1l111l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ∖")
        return [bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡰࡷࡵࠩ∗")], bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ∘")], os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ∙")]]
    @classmethod
    def bstack1lll1l1ll111_opy_(cls, bstack11llll1l1_opy_):
        if bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ√")) == None:
            cls.bstack1lll1l1ll11l_opy_()
            return [None, None]
        if bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ∛")][bstack1l111l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ∜")] != True:
            cls.bstack1lll1l1ll11l_opy_(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ∝")])
            return [None, None]
        if bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ∞")].get(bstack1l111l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ∟")):
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ∠"))
            parsed = json.loads(os.getenv(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ∡"), bstack1l111l1_opy_ (u"ࠩࡾࢁࠬ∢")))
            capabilities = bstack1l11111ll1_opy_.bstack1lll1l1llll1_opy_(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ∣")][bstack1l111l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ∤")][bstack1l111l1_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ∥")], bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ∦"), bstack1l111l1_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭∧"))
            bstack1lll1l1l1lll_opy_ = capabilities[bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭∨")]
            os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ∩")] = bstack1lll1l1l1lll_opy_
            if bstack1l111l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ∪") in bstack11llll1l1_opy_ and bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ∫")) is None:
                parsed[bstack1l111l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭∬")] = capabilities[bstack1l111l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ∭")]
            os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ∮")] = json.dumps(parsed)
            scripts = bstack1l11111ll1_opy_.bstack1lll1l1llll1_opy_(bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ∯")][bstack1l111l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ∰")][bstack1l111l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ∱")], bstack1l111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ∲"), bstack1l111l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭∳"))
            bstack1l111l1l_opy_.bstack11l111ll11_opy_(scripts)
            commands = bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭∴")][bstack1l111l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ∵")][bstack1l111l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ∶")].get(bstack1l111l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ∷"))
            bstack1l111l1l_opy_.bstack11l1lll1lll_opy_(commands)
            bstack11l1lllll1l_opy_ = capabilities.get(bstack1l111l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ∸"))
            bstack1l111l1l_opy_.bstack11l1ll11l1l_opy_(bstack11l1lllll1l_opy_)
            bstack1l111l1l_opy_.store()
        return [bstack1lll1l1l1lll_opy_, bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭∹")]]
    @classmethod
    def bstack1lll1ll1l111_opy_(cls, response=None):
        os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ∺")] = bstack1l111l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ∻")
        os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ∼")] = bstack1l111l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭∽")
        os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ∾")] = bstack1l111l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ∿")
        os.environ[bstack1l111l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ≀")] = bstack1l111l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ≁")
        os.environ[bstack1l111l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ≂")] = bstack1l111l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ≃")
        cls.bstack1lll1l1ll1l1_opy_(response, bstack1l111l1_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ≄"))
        return [None, None, None]
    @classmethod
    def bstack1lll1l1ll11l_opy_(cls, response=None):
        os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ≅")] = bstack1l111l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ≆")
        os.environ[bstack1l111l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ≇")] = bstack1l111l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ≈")
        os.environ[bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ≉")] = bstack1l111l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ≊")
        cls.bstack1lll1l1ll1l1_opy_(response, bstack1l111l1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣ≋"))
        return [None, None, None]
    @classmethod
    def bstack1lll1ll11ll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭≌")] = jwt
        os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ≍")] = build_hashed_id
    @classmethod
    def bstack1lll1l1ll1l1_opy_(cls, response=None, product=bstack1l111l1_opy_ (u"ࠦࠧ≎")):
        if response == None or response.get(bstack1l111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ≏")) == None:
            logger.error(product + bstack1l111l1_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ≐"))
            return
        for error in response[bstack1l111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ≑")]:
            bstack111llll1l11_opy_ = error[bstack1l111l1_opy_ (u"ࠨ࡭ࡨࡽࠬ≒")]
            error_message = error[bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ≓")]
            if error_message:
                if bstack111llll1l11_opy_ == bstack1l111l1_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤ≔"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l111l1_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧ≕") + product + bstack1l111l1_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ≖"))
    @classmethod
    def bstack1lll1ll1llll_opy_(cls):
        if cls.bstack1llll1l1lll1_opy_ is not None:
            return
        cls.bstack1llll1l1lll1_opy_ = bstack1llll1l11l11_opy_(cls.bstack1lll1ll1l1ll_opy_)
        cls.bstack1llll1l1lll1_opy_.start()
    @classmethod
    def bstack111l1111l1_opy_(cls):
        if cls.bstack1llll1l1lll1_opy_ is None:
            return
        cls.bstack1llll1l1lll1_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll1ll1l1ll_opy_(cls, bstack1111l1ll1l_opy_, event_url=bstack1l111l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ≗")):
        config = {
            bstack1l111l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ≘"): cls.default_headers()
        }
        logger.debug(bstack1l111l1_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣ≙").format(bstack1l111l1_opy_ (u"ࠩ࠯ࠤࠬ≚").join([event[bstack1l111l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ≛")] for event in bstack1111l1ll1l_opy_])))
        response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠫࡕࡕࡓࡕࠩ≜"), cls.request_url(event_url), bstack1111l1ll1l_opy_, config)
        bstack11l1lll1111_opy_ = response.json()
    @classmethod
    def bstack1ll111llll_opy_(cls, bstack1111l1ll1l_opy_, event_url=bstack1l111l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ≝")):
        logger.debug(bstack1l111l1_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ≞").format(bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ≟")]))
        if not bstack1l11111ll1_opy_.bstack1lll1ll1ll11_opy_(bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ≠")]):
            logger.debug(bstack1l111l1_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ≡").format(bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ≢")]))
            return
        bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1lll1ll1l1l1_opy_(bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ≣")], bstack1111l1ll1l_opy_.get(bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ≤")))
        if bstack1lll1111l1_opy_ != None:
            if bstack1111l1ll1l_opy_.get(bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ≥")) != None:
                bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ≦")][bstack1l111l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭≧")] = bstack1lll1111l1_opy_
            else:
                bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ≨")] = bstack1lll1111l1_opy_
        if event_url == bstack1l111l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ≩"):
            cls.bstack1lll1ll1llll_opy_()
            logger.debug(bstack1l111l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ≪").format(bstack1111l1ll1l_opy_[bstack1l111l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ≫")]))
            cls.bstack1llll1l1lll1_opy_.add(bstack1111l1ll1l_opy_)
        elif event_url == bstack1l111l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ≬"):
            cls.bstack1lll1ll1l1ll_opy_([bstack1111l1ll1l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11l1l111_opy_(cls, logs):
        for log in logs:
            bstack1lll1ll111ll_opy_ = {
                bstack1l111l1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ≭"): bstack1l111l1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪ≮"),
                bstack1l111l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ≯"): log[bstack1l111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ≰")],
                bstack1l111l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ≱"): log[bstack1l111l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ≲")],
                bstack1l111l1_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭≳"): {},
                bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ≴"): log[bstack1l111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ≵")],
            }
            if bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ≶") in log:
                bstack1lll1ll111ll_opy_[bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ≷")] = log[bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ≸")]
            elif bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ≹") in log:
                bstack1lll1ll111ll_opy_[bstack1l111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭≺")] = log[bstack1l111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ≻")]
            cls.bstack1ll111llll_opy_({
                bstack1l111l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ≼"): bstack1l111l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭≽"),
                bstack1l111l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ≾"): [bstack1lll1ll111ll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll1ll1l11l_opy_(cls, steps):
        bstack1lll1l1lll11_opy_ = []
        for step in steps:
            bstack1lll1ll1lll1_opy_ = {
                bstack1l111l1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ≿"): bstack1l111l1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨ⊀"),
                bstack1l111l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⊁"): step[bstack1l111l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⊂")],
                bstack1l111l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⊃"): step[bstack1l111l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⊄")],
                bstack1l111l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⊅"): step[bstack1l111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⊆")],
                bstack1l111l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⊇"): step[bstack1l111l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⊈")]
            }
            if bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⊉") in step:
                bstack1lll1ll1lll1_opy_[bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⊊")] = step[bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⊋")]
            elif bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⊌") in step:
                bstack1lll1ll1lll1_opy_[bstack1l111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⊍")] = step[bstack1l111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⊎")]
            bstack1lll1l1lll11_opy_.append(bstack1lll1ll1lll1_opy_)
        cls.bstack1ll111llll_opy_({
            bstack1l111l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⊏"): bstack1l111l1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⊐"),
            bstack1l111l1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭⊑"): bstack1lll1l1lll11_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1llllll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
    def bstack1l111111l1_opy_(cls, screenshot):
        cls.bstack1ll111llll_opy_({
            bstack1l111l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⊒"): bstack1l111l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⊓"),
            bstack1l111l1_opy_ (u"ࠫࡱࡵࡧࡴࠩ⊔"): [{
                bstack1l111l1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⊕"): bstack1l111l1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ⊖"),
                bstack1l111l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⊗"): datetime.datetime.utcnow().isoformat() + bstack1l111l1_opy_ (u"ࠨ࡜ࠪ⊘"),
                bstack1l111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⊙"): screenshot[bstack1l111l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ⊚")],
                bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⊛"): screenshot[bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⊜")]
            }]
        }, event_url=bstack1l111l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⊝"))
    @classmethod
    @error_handler(class_method=True)
    def bstack111ll1lll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll111llll_opy_({
            bstack1l111l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⊞"): bstack1l111l1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ⊟"),
            bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⊠"): {
                bstack1l111l1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ⊡"): cls.current_test_uuid(),
                bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥ⊢"): cls.bstack111l1ll111_opy_(driver)
            }
        })
    @classmethod
    def bstack111l1l111l_opy_(cls, event: str, bstack1111l1ll1l_opy_: bstack111l1111ll_opy_):
        bstack1111l11l11_opy_ = {
            bstack1l111l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⊣"): event,
            bstack1111l1ll1l_opy_.bstack1111ll1lll_opy_(): bstack1111l1ll1l_opy_.bstack11111ll11l_opy_(event)
        }
        cls.bstack1ll111llll_opy_(bstack1111l11l11_opy_)
        result = getattr(bstack1111l1ll1l_opy_, bstack1l111l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⊤"), None)
        if event == bstack1l111l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⊥"):
            threading.current_thread().bstackTestMeta = {bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⊦"): bstack1l111l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⊧")}
        elif event == bstack1l111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⊨"):
            threading.current_thread().bstackTestMeta = {bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⊩"): getattr(result, bstack1l111l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⊪"), bstack1l111l1_opy_ (u"࠭ࠧ⊫"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⊬"), None) is None or os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⊭")] == bstack1l111l1_opy_ (u"ࠤࡱࡹࡱࡲࠢ⊮")) and (os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⊯"), None) is None or os.environ[bstack1l111l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⊰")] == bstack1l111l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⊱")):
            return False
        return True
    @staticmethod
    def bstack1lll1ll1111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llll1lll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l111l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⊲"): bstack1l111l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⊳"),
            bstack1l111l1_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫ⊴"): bstack1l111l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⊵")
        }
        if os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⊶"), None):
            headers[bstack1l111l1_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⊷")] = bstack1l111l1_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⊸").format(os.environ[bstack1l111l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥ⊹")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l111l1_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭⊺").format(bstack1lll1ll11l11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⊻"), None)
    @staticmethod
    def bstack111l1ll111_opy_(driver):
        return {
            bstack111lll1111l_opy_(): bstack111ll1l1ll1_opy_(driver)
        }
    @staticmethod
    def bstack1lll1l1lll1l_opy_(exception_info, report):
        return [{bstack1l111l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⊼"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lllll111ll_opy_(typename):
        if bstack1l111l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ⊽") in typename:
            return bstack1l111l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ⊾")
        return bstack1l111l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ⊿")