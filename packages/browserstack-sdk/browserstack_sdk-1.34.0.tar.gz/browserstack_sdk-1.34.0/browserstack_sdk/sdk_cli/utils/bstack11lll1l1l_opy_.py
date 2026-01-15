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
import json
import shutil
import tempfile
import threading
import urllib.request
import uuid
from pathlib import Path
import logging
import re
from bstack_utils.helper import bstack1l1l1lll1ll_opy_
bstack11ll11ll1ll_opy_ = 100 * 1024 * 1024 # 100 bstack11ll1l11l1l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l11lllll11_opy_ = bstack1l1l1lll1ll_opy_()
bstack1l1l1l1l111_opy_ = bstack1l111l1_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᚦ")
bstack11ll1llll11_opy_ = bstack1l111l1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᚧ")
bstack11lll11111l_opy_ = bstack1l111l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᚨ")
bstack11ll1llll1l_opy_ = bstack1l111l1_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᚩ")
bstack11ll11llll1_opy_ = bstack1l111l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᚪ")
_11ll11lllll_opy_ = threading.local()
def bstack11lllllll11_opy_(test_framework_state, test_hook_state):
    bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡳࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡺࡨࡦࠢࡨࡺࡪࡴࡴࠡࡪࡤࡲࡩࡲࡥࡳࠢࠫࡷࡺࡩࡨࠡࡣࡶࠤࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵࠫࠍࠤࠥࠦࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࡰࡼࠤ࡫࡯࡬ࡦࠢࡸࡴࡱࡵࡡࡥࡵࠣࡳࡨࡩࡵࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᚫ")
    _11ll11lllll_opy_.test_framework_state = test_framework_state
    _11ll11lllll_opy_.test_hook_state = test_hook_state
def bstack11ll1l111ll_opy_():
    bstack1l111l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡔࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡸࡺࡶ࡬ࡦࠢࠫࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧ࠯ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠯ࠠࡰࡴࠣࠬࡓࡵ࡮ࡦ࠮ࠣࡒࡴࡴࡥࠪࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᚬ")
    return (
        getattr(_11ll11lllll_opy_, bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࠩᚭ"), None),
        getattr(_11ll11lllll_opy_, bstack1l111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࠬᚮ"), None)
    )
class bstack11l11l1l1_opy_:
    bstack1l111l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡡ࡭࡫ࡷࡽࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡣࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡷࡺࡶࡰࡰࡴࡷࡷࠥࡨ࡯ࡵࡪࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡌ࡙࡚ࡐ࠰ࡊࡗࡘࡕ࡙ࠠࡖࡔࡏࡷ࠱ࠦࡡ࡯ࡦࠣࡧࡴࡶࡩࡦࡵࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࡵࡱࠣࡥࠥࡪࡥࡴ࡫ࡪࡲࡦࡺࡥࡥࠌࠣࠤࠥࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡺ࡭ࡹ࡮ࡩ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡨࡰ࡯ࡨࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡺࡴࡤࡦࡴࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࡌࡪࠥࡧ࡮ࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࠣࠬ࡮ࡴࠠࡋࡕࡒࡒࠥ࡬࡯ࡳ࡯ࡤࡸ࠮ࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡦࡴࡤࠡࡥࡲࡲࡹࡧࡩ࡯ࡵࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࠠࠡࡨࡲࡶࠥࡺࡨࡦࠢ࡮ࡩࡾࠦࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ࠯ࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡱ࡮ࡤࡧࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡦࡰ࡮ࡧࡩࡷࡁࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧ࠯ࠎࠥࠦࠠࠡ࡫ࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡫ࡶࠤࡦࠦࡶࡰ࡫ࡧࠤࡲ࡫ࡴࡩࡱࡧ⠘࡮ࡺࠠࡩࡣࡱࡨࡱ࡫ࡳࠡࡣ࡯ࡰࠥ࡫ࡲࡳࡱࡵࡷࠥ࡭ࡲࡢࡥࡨࡪࡺࡲ࡬ࡺࠢࡥࡽࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡸ࡭࡫࡭ࠡࡣࡱࡨࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡷ࡬ࡷࡵࡷࡪࡰࡪࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᚯ")
    @staticmethod
    def upload_attachment(bstack11ll11lll1l_opy_: str, *bstack11ll11l1ll1_opy_) -> None:
        if not bstack11ll11lll1l_opy_ or not bstack11ll11lll1l_opy_.strip():
            logger.error(bstack1l111l1_opy_ (u"ࠧࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡑࡴࡲࡺ࡮ࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡯ࡳࠡࡧࡰࡴࡹࡿࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤᚰ"))
            return
        bstack11ll1l111l1_opy_ = bstack11ll11l1ll1_opy_[0] if bstack11ll11l1ll1_opy_ and len(bstack11ll11l1ll1_opy_) > 0 else None
        bstack11ll11l1lll_opy_ = None
        test_framework_state, test_hook_state = bstack11ll1l111ll_opy_()
        try:
            if bstack11ll11lll1l_opy_.startswith(bstack1l111l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᚱ")) or bstack11ll11lll1l_opy_.startswith(bstack1l111l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᚲ")):
                logger.debug(bstack1l111l1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢࡘࡖࡑࡁࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠣᚳ"))
                url = bstack11ll11lll1l_opy_
                bstack11ll11ll11l_opy_ = str(uuid.uuid4())
                bstack11ll1l11111_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11ll1l11111_opy_ or not bstack11ll1l11111_opy_.strip():
                    bstack11ll1l11111_opy_ = bstack11ll11ll11l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l111l1_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡡࠥᚴ") + bstack11ll11ll11l_opy_ + bstack1l111l1_opy_ (u"ࠥࡣࠧᚵ"),
                                                        suffix=bstack1l111l1_opy_ (u"ࠦࡤࠨᚶ") + bstack11ll1l11111_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l111l1_opy_ (u"ࠬࡽࡢࠨᚷ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11ll11l1lll_opy_ = Path(temp_file.name)
                logger.debug(bstack1l111l1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᚸ").format(bstack11ll11l1lll_opy_))
            else:
                bstack11ll11l1lll_opy_ = Path(bstack11ll11lll1l_opy_)
                logger.debug(bstack1l111l1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᚹ").format(bstack11ll11l1lll_opy_))
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡴࡨࡴࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡩࡶࡴࡳࠠࡱࡣࡷ࡬࠴࡛ࡒࡍ࠼ࠣࡿࢂࠨᚺ").format(e))
            return
        if bstack11ll11l1lll_opy_ is None or not bstack11ll11l1lll_opy_.exists():
            logger.error(bstack1l111l1_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᚻ").format(bstack11ll11l1lll_opy_))
            return
        if bstack11ll11l1lll_opy_.stat().st_size > bstack11ll11ll1ll_opy_:
            logger.error(bstack1l111l1_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵ࡬ࡾࡪࠦࡥࡹࡥࡨࡩࡩࡹࠠ࡮ࡣࡻ࡭ࡲࡻ࡭ࠡࡣ࡯ࡰࡴࡽࡥࡥࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡿࢂࠨᚼ").format(bstack11ll11ll1ll_opy_))
            return
        bstack11ll11ll111_opy_ = bstack1l111l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᚽ")
        if bstack11ll1l111l1_opy_:
            try:
                params = json.loads(bstack11ll1l111l1_opy_)
                if bstack1l111l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᚾ") in params and params.get(bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᚿ")) is True:
                    bstack11ll11ll111_opy_ = bstack1l111l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᛀ")
            except Exception as bstack11ll11ll1l1_opy_:
                logger.error(bstack1l111l1_opy_ (u"ࠣࡌࡖࡓࡓࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡖࡡࡳࡣࡰࡷ࠿ࠦࡻࡾࠤᛁ").format(bstack11ll11ll1l1_opy_))
        bstack11ll11lll11_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll11lll1l1_opy_ import bstack1lll11l11ll_opy_
        if test_framework_state in bstack1lll11l11ll_opy_.bstack1l111111ll1_opy_:
            if bstack11ll11ll111_opy_ == bstack11lll11111l_opy_:
                bstack11ll11lll11_opy_ = True
            bstack11ll11ll111_opy_ = bstack11ll1llll1l_opy_
        try:
            platform_index = os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᛂ")]
            target_dir = os.path.join(bstack1l11lllll11_opy_, bstack1l1l1l1l111_opy_ + str(platform_index),
                                      bstack11ll11ll111_opy_)
            if bstack11ll11lll11_opy_:
                target_dir = os.path.join(target_dir, bstack11ll11llll1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l111l1_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧ࠳ࡻ࡫ࡲࡪࡨ࡬ࡩࡩࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᛃ").format(target_dir))
            file_name = os.path.basename(bstack11ll11l1lll_opy_)
            bstack11ll11l1l1l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11ll11l1l1l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11ll1l1111l_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11ll1l1111l_opy_) + extension)):
                    bstack11ll1l1111l_opy_ += 1
                bstack11ll11l1l1l_opy_ = os.path.join(target_dir, base_name + str(bstack11ll1l1111l_opy_) + extension)
            shutil.copy(bstack11ll11l1lll_opy_, bstack11ll11l1l1l_opy_)
            logger.info(bstack1l111l1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡥࡲࡴ࡮࡫ࡤࠡࡶࡲ࠾ࠥࢁࡽࠣᛄ").format(bstack11ll11l1l1l_opy_))
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡲࡵࡶࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᛅ").format(e))
            return
        finally:
            if bstack11ll11lll1l_opy_.startswith(bstack1l111l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᛆ")) or bstack11ll11lll1l_opy_.startswith(bstack1l111l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᛇ")):
                try:
                    if bstack11ll11l1lll_opy_ is not None and bstack11ll11l1lll_opy_.exists():
                        bstack11ll11l1lll_opy_.unlink()
                        logger.debug(bstack1l111l1_opy_ (u"ࠣࡖࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦࠢࡧࡩࡱ࡫ࡴࡦࡦ࠽ࠤࢀࢃࠢᛈ").format(bstack11ll11l1lll_opy_))
                except Exception as ex:
                    logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣᛉ").format(ex))
    @staticmethod
    def bstack1l11ll1ll1_opy_() -> None:
        bstack1l111l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡧ࡯ࡩࡹ࡫ࡳࠡࡣ࡯ࡰࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡷࡩࡱࡶࡩࠥࡴࡡ࡮ࡧࡶࠤࡸࡺࡡࡳࡶࠣࡻ࡮ࡺࡨࠡࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤࠣࡪࡴࡲ࡬ࡰࡹࡨࡨࠥࡨࡹࠡࡣࠣࡲࡺࡳࡢࡦࡴࠣ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᛊ")
        bstack11ll11l1l11_opy_ = bstack1l1l1lll1ll_opy_()
        pattern = re.compile(bstack1l111l1_opy_ (u"ࡶ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࡡࡪࠫࠣᛋ"))
        if os.path.exists(bstack11ll11l1l11_opy_):
            for item in os.listdir(bstack11ll11l1l11_opy_):
                bstack11ll1l11l11_opy_ = os.path.join(bstack11ll11l1l11_opy_, item)
                if os.path.isdir(bstack11ll1l11l11_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11ll1l11l11_opy_)
                    except Exception as e:
                        logger.error(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᛌ").format(e))
        else:
            logger.info(bstack1l111l1_opy_ (u"ࠨࡔࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᛍ").format(bstack11ll11l1l11_opy_))