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
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l1l1lll1l_opy_ import bstack11l1l1ll1ll_opy_
from bstack_utils.constants import bstack11l11lll111_opy_, bstack1111l1l1l_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack1llll111l_opy_
from bstack_utils import bstack1ll1lll11_opy_
bstack11l111lll11_opy_ = 10
class bstack1l11l11l1l_opy_:
    def __init__(self, bstack11l111111l_opy_, config, bstack11l111l1ll1_opy_=0):
        self.bstack11l111l1l11_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l111l111l_opy_ = bstack1l111l1_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤᮡ").format(bstack11l11lll111_opy_)
        self.bstack11l111l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧᮢ").format(os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᮣ"))))
        self.bstack11l111lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧᮤ").format(os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᮥ"))))
        self.bstack11l11l11ll1_opy_ = 2
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        self.config = config
        self.logger = bstack1ll1lll11_opy_.get_logger(__name__, bstack1111l1l1l_opy_)
        self.bstack11l111l1ll1_opy_ = bstack11l111l1ll1_opy_
        self.bstack11l111ll1l1_opy_ = False
        self.bstack11l11l111ll_opy_ = not (
                            os.environ.get(bstack1l111l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢᮦ")) and
                            os.environ.get(bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧᮧ")) and
                            os.environ.get(bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧᮨ"))
                        )
        if bstack1llll111l_opy_.bstack11l111ll111_opy_(config):
            self.bstack11l11l11ll1_opy_ = bstack1llll111l_opy_.bstack11l11l11l1l_opy_(config, self.bstack11l111l1ll1_opy_)
            self.bstack11l111l1lll_opy_()
    def bstack11l11l1111l_opy_(self):
        return bstack1l111l1_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥᮩ").format(self.config.get(bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᮪")), os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ᮫ࠬ")))
    def bstack11l111l11l1_opy_(self):
        try:
            if self.bstack11l11l111ll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l111lllll_opy_, bstack1l111l1_opy_ (u"ࠢࡳࠤᮬ")) as f:
                        bstack11l11l11111_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l11l11111_opy_ = set()
                bstack11l111ll1ll_opy_ = bstack11l11l11111_opy_ - self.bstack11l111l1l11_opy_
                if not bstack11l111ll1ll_opy_:
                    return
                self.bstack11l111l1l11_opy_.update(bstack11l111ll1ll_opy_)
                data = {bstack1l111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨᮭ"): list(self.bstack11l111l1l11_opy_), bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧᮮ"): self.config.get(bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᮯ")), bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ᮰"): os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ᮱")), bstack1l111l1_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ᮲"): self.config.get(bstack1l111l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᮳"))}
            response = bstack11l1l1ll1ll_opy_.bstack11l11l11l11_opy_(self.bstack11l111l111l_opy_, data)
            if response.get(bstack1l111l1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᮴")) == 200:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ᮵").format(data))
            else:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ᮶").format(response))
        except Exception as e:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ᮷").format(e))
    def bstack11l111llll1_opy_(self):
        if self.bstack11l11l111ll_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l111lllll_opy_, bstack1l111l1_opy_ (u"ࠧࡸࠢ᮸")) as f:
                        bstack11l111l1l1l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l111l1l1l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤ᮹").format(failed_count))
                if failed_count >= self.bstack11l11l11ll1_opy_:
                    self.logger.info(bstack1l111l1_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣᮺ").format(failed_count, self.bstack11l11l11ll1_opy_))
                    self.bstack11l11l111l1_opy_(failed_count)
                    self.bstack11l111ll1l1_opy_ = True
            return
        try:
            response = bstack11l1l1ll1ll_opy_.bstack11l111llll1_opy_(bstack1l111l1_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧᮻ").format(self.bstack11l111l111l_opy_, self.config.get(bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᮼ")), os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᮽ")), self.config.get(bstack1l111l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᮾ"))))
            if response.get(bstack1l111l1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᮿ")) == 200:
                failed_count = response.get(bstack1l111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤᯀ"), 0)
                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤᯁ").format(failed_count))
                if failed_count >= self.bstack11l11l11ll1_opy_:
                    self.logger.info(bstack1l111l1_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣᯂ").format(failed_count, self.bstack11l11l11ll1_opy_))
                    self.bstack11l11l111l1_opy_(failed_count)
                    self.bstack11l111ll1l1_opy_ = True
            else:
                self.logger.error(bstack1l111l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᯃ").format(response))
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦᯄ").format(e))
    def bstack11l11l111l1_opy_(self, failed_count):
        with open(self.bstack11l111l11ll_opy_, bstack1l111l1_opy_ (u"ࠦࡼࠨᯅ")) as f:
            f.write(bstack1l111l1_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥᯆ").format(datetime.now()))
            f.write(bstack1l111l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥᯇ").format(failed_count))
        self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣᯈ").format(self.bstack11l111l11ll_opy_))
    def bstack11l111l1lll_opy_(self):
        def bstack11l111lll1l_opy_():
            while not self.bstack11l111ll1l1_opy_:
                time.sleep(bstack11l111lll11_opy_)
                self.bstack11l111l11l1_opy_()
                self.bstack11l111llll1_opy_()
        bstack11l111ll11l_opy_ = threading.Thread(target=bstack11l111lll1l_opy_, daemon=True)
        bstack11l111ll11l_opy_.start()