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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1111llll_opy_, bstack1ll1l1l1l1_opy_, bstack1l1l1l111_opy_, bstack1ll111l1_opy_, \
    bstack11l1111ll1l_opy_
from bstack_utils.measure import measure
def bstack111lllllll_opy_(bstack1llll11l11l1_opy_):
    for driver in bstack1llll11l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack11llll1ll_opy_(driver, status, reason=bstack1l111l1_opy_ (u"ࠨࠩ℉")):
    bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
    if bstack1l1l1111_opy_.bstack1llllll1lll_opy_():
        return
    bstack111ll1l11_opy_ = bstack11l111llll_opy_(bstack1l111l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬℊ"), bstack1l111l1_opy_ (u"ࠪࠫℋ"), status, reason, bstack1l111l1_opy_ (u"ࠫࠬℌ"), bstack1l111l1_opy_ (u"ࠬ࠭ℍ"))
    driver.execute_script(bstack111ll1l11_opy_)
@measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack11ll1lll11_opy_(page, status, reason=bstack1l111l1_opy_ (u"࠭ࠧℎ")):
    try:
        if page is None:
            return
        bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
        if bstack1l1l1111_opy_.bstack1llllll1lll_opy_():
            return
        bstack111ll1l11_opy_ = bstack11l111llll_opy_(bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪℏ"), bstack1l111l1_opy_ (u"ࠨࠩℐ"), status, reason, bstack1l111l1_opy_ (u"ࠩࠪℑ"), bstack1l111l1_opy_ (u"ࠪࠫℒ"))
        page.evaluate(bstack1l111l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧℓ"), bstack111ll1l11_opy_)
    except Exception as e:
        print(bstack1l111l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥ℔"), e)
def bstack11l111llll_opy_(type, name, status, reason, bstack1lll11l111_opy_, bstack1l11ll1l1l_opy_):
    bstack11l1ll1ll_opy_ = {
        bstack1l111l1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ℕ"): type,
        bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ№"): {}
    }
    if type == bstack1l111l1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ℗"):
        bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ℘")][bstack1l111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩℙ")] = bstack1lll11l111_opy_
        bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧℚ")][bstack1l111l1_opy_ (u"ࠬࡪࡡࡵࡣࠪℛ")] = json.dumps(str(bstack1l11ll1l1l_opy_))
    if type == bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧℜ"):
        bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪℝ")][bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭℞")] = name
    if type == bstack1l111l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ℟"):
        bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭℠")][bstack1l111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ℡")] = status
        if status == bstack1l111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ™") and str(reason) != bstack1l111l1_opy_ (u"ࠨࠢ℣"):
            bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪℤ")][bstack1l111l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ℥")] = json.dumps(str(reason))
    bstack1l1lllllll_opy_ = bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧΩ").format(json.dumps(bstack11l1ll1ll_opy_))
    return bstack1l1lllllll_opy_
def bstack111llllll1_opy_(url, config, logger, bstack111111111_opy_=False):
    hostname = bstack1ll1l1l1l1_opy_(url)
    is_private = bstack1ll111l1_opy_(hostname)
    try:
        if is_private or bstack111111111_opy_:
            file_path = bstack11l1111llll_opy_(bstack1l111l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ℧"), bstack1l111l1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪℨ"), logger)
            if os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ℩")) and eval(
                    os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫK"))):
                return
            if (bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫÅ") in config and not config[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬℬ")]):
                os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧℭ")] = str(True)
                bstack1llll11l1l1l_opy_ = {bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ℮"): hostname}
                bstack11l1111ll1l_opy_(bstack1l111l1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪℯ"), bstack1l111l1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪℰ"), bstack1llll11l1l1l_opy_, logger)
    except Exception as e:
        pass
def bstack11l111l1ll_opy_(caps, bstack1llll11l11ll_opy_):
    if bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧℱ") in caps:
        caps[bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨℲ")][bstack1l111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧℳ")] = True
        if bstack1llll11l11ll_opy_:
            caps[bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪℴ")][bstack1l111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬℵ")] = bstack1llll11l11ll_opy_
    else:
        caps[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩℶ")] = True
        if bstack1llll11l11ll_opy_:
            caps[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ℷ")] = bstack1llll11l11ll_opy_
def bstack1llll1ll1lll_opy_(bstack11111ll111_opy_):
    bstack1llll11l1l11_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪℸ"), bstack1l111l1_opy_ (u"ࠧࠨℹ"))
    if bstack1llll11l1l11_opy_ == bstack1l111l1_opy_ (u"ࠨࠩ℺") or bstack1llll11l1l11_opy_ == bstack1l111l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ℻"):
        threading.current_thread().testStatus = bstack11111ll111_opy_
    else:
        if bstack11111ll111_opy_ == bstack1l111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪℼ"):
            threading.current_thread().testStatus = bstack11111ll111_opy_