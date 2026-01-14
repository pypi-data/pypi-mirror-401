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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111llll11l1_opy_, bstack111llll1l1_opy_, bstack1ll1ll11ll_opy_, bstack1ll1ll1ll_opy_, \
    bstack111llll1l11_opy_
from bstack_utils.measure import measure
def bstack1lllll111_opy_(bstack1llll11lll1l_opy_):
    for driver in bstack1llll11lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1l11lll_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack1l11l11l_opy_(driver, status, reason=bstack1l11l1l_opy_ (u"⃨ࠪࠫ")):
    bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
    if bstack11llllll_opy_.bstack111111ll1l_opy_():
        return
    bstack1lll1ll1l1_opy_ = bstack1lll11l1ll_opy_(bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⃩"), bstack1l11l1l_opy_ (u"⃪ࠬ࠭"), status, reason, bstack1l11l1l_opy_ (u"⃫࠭ࠧ"), bstack1l11l1l_opy_ (u"ࠧࠨ⃬"))
    driver.execute_script(bstack1lll1ll1l1_opy_)
@measure(event_name=EVENTS.bstack11l1l11lll_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack1ll1ll11l_opy_(page, status, reason=bstack1l11l1l_opy_ (u"ࠨ⃭ࠩ")):
    try:
        if page is None:
            return
        bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
        if bstack11llllll_opy_.bstack111111ll1l_opy_():
            return
        bstack1lll1ll1l1_opy_ = bstack1lll11l1ll_opy_(bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ⃮ࠬ"), bstack1l11l1l_opy_ (u"⃯ࠪࠫ"), status, reason, bstack1l11l1l_opy_ (u"ࠫࠬ⃰"), bstack1l11l1l_opy_ (u"ࠬ࠭⃱"))
        page.evaluate(bstack1l11l1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⃲"), bstack1lll1ll1l1_opy_)
    except Exception as e:
        print(bstack1l11l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ⃳"), e)
def bstack1lll11l1ll_opy_(type, name, status, reason, bstack11l111111l_opy_, bstack1l11111ll1_opy_):
    bstack1l11lll11_opy_ = {
        bstack1l11l1l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ⃴"): type,
        bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⃵"): {}
    }
    if type == bstack1l11l1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⃶"):
        bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⃷")][bstack1l11l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⃸")] = bstack11l111111l_opy_
        bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⃹")][bstack1l11l1l_opy_ (u"ࠧࡥࡣࡷࡥࠬ⃺")] = json.dumps(str(bstack1l11111ll1_opy_))
    if type == bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⃻"):
        bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⃼")][bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ⃽")] = name
    if type == bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⃾"):
        bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ⃿")][bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭℀")] = status
        if status == bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ℁") and str(reason) != bstack1l11l1l_opy_ (u"ࠣࠤℂ"):
            bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ℃")][bstack1l11l1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ℄")] = json.dumps(str(reason))
    bstack111l1llll_opy_ = bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ℅").format(json.dumps(bstack1l11lll11_opy_))
    return bstack111l1llll_opy_
def bstack111ll1l1ll_opy_(url, config, logger, bstack111l11l1l_opy_=False):
    hostname = bstack111llll1l1_opy_(url)
    is_private = bstack1ll1ll1ll_opy_(hostname)
    try:
        if is_private or bstack111l11l1l_opy_:
            file_path = bstack111llll11l1_opy_(bstack1l11l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ℆"), bstack1l11l1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬℇ"), logger)
            if os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ℈")) and eval(
                    os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭℉"))):
                return
            if (bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ℊ") in config and not config[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧℋ")]):
                os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩℌ")] = str(True)
                bstack1llll11llll1_opy_ = {bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧℍ"): hostname}
                bstack111llll1l11_opy_(bstack1l11l1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬℎ"), bstack1l11l1l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬℏ"), bstack1llll11llll1_opy_, logger)
    except Exception as e:
        pass
def bstack1l1111ll11_opy_(caps, bstack1llll11lll11_opy_):
    if bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩℐ") in caps:
        caps[bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪℑ")][bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩℒ")] = True
        if bstack1llll11lll11_opy_:
            caps[bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬℓ")][bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ℔")] = bstack1llll11lll11_opy_
    else:
        caps[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫℕ")] = True
        if bstack1llll11lll11_opy_:
            caps[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ№")] = bstack1llll11lll11_opy_
def bstack1lllll111l1l_opy_(bstack1111l11ll1_opy_):
    bstack1llll11ll1ll_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ℗"), bstack1l11l1l_opy_ (u"ࠩࠪ℘"))
    if bstack1llll11ll1ll_opy_ == bstack1l11l1l_opy_ (u"ࠪࠫℙ") or bstack1llll11ll1ll_opy_ == bstack1l11l1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬℚ"):
        threading.current_thread().testStatus = bstack1111l11ll1_opy_
    else:
        if bstack1111l11ll1_opy_ == bstack1l11l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬℛ"):
            threading.current_thread().testStatus = bstack1111l11ll1_opy_