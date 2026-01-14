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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1ll1l11lll_opy_
from browserstack_sdk.bstack11l1ll1l1l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll111111_opy_, bstack111111l1l1_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111lll111l_opy_
from bstack_utils.constants import bstack1llllll1ll1_opy_
from bstack_utils.bstack1lll11ll1_opy_ import bstack1111lll1_opy_
from bstack_utils.bstack11111l1111_opy_ import bstack1llllll1l1l_opy_
class bstack1lll1l11_opy_:
    def __init__(self, args, logger, bstack1lllllll1ll_opy_, bstack1111111l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_
        self.bstack1111111l11_opy_ = bstack1111111l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l11ll1ll1_opy_ = []
        self.bstack1lllllllll1_opy_ = []
        self.bstack111lllll1l_opy_ = []
        self.bstack1llllll1111_opy_ = self.bstack1ll11l1l11_opy_()
        self.bstack11l111l1_opy_ = -1
    def bstack1l1lllllll_opy_(self, bstack1111111lll_opy_):
        self.parse_args()
        self.bstack1lllllll1l1_opy_()
        self.bstack111111ll11_opy_(bstack1111111lll_opy_)
        self.bstack11111l111l_opy_()
    def bstack1111ll1ll_opy_(self):
        bstack1lll11ll1_opy_ = bstack1111lll1_opy_.bstack1llll1111_opy_(self.bstack1lllllll1ll_opy_, self.logger)
        if bstack1lll11ll1_opy_ is None:
            self.logger.warn(bstack1l11l1l_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲࡙ࠥ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣႥ"))
            return
        bstack111111111l_opy_ = False
        bstack1lll11ll1_opy_.bstack11111111l1_opy_(bstack1l11l1l_opy_ (u"ࠨࡥ࡯ࡣࡥࡰࡪࡪࠢႦ"), bstack1lll11ll1_opy_.bstack11l1l1ll11_opy_())
        start_time = time.time()
        if bstack1lll11ll1_opy_.bstack11l1l1ll11_opy_():
            test_files = self.bstack1111111l1l_opy_()
            bstack111111111l_opy_ = True
            bstack1llllllllll_opy_ = bstack1lll11ll1_opy_.bstack111111l11l_opy_(test_files)
            if bstack1llllllllll_opy_:
                self.bstack1l11ll1ll1_opy_ = [os.path.normpath(item) for item in bstack1llllllllll_opy_]
                self.__1llllllll1l_opy_()
                bstack1lll11ll1_opy_.bstack11111111ll_opy_(bstack111111111l_opy_)
                self.logger.info(bstack1l11l1l_opy_ (u"ࠢࡕࡧࡶࡸࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡸࡷ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧႧ").format(self.bstack1l11ll1ll1_opy_))
            else:
                self.logger.info(bstack1l11l1l_opy_ (u"ࠣࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹࡨࡶࡪࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡥࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨႨ"))
        bstack1lll11ll1_opy_.bstack11111111l1_opy_(bstack1l11l1l_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡔࡢ࡭ࡨࡲ࡙ࡵࡁࡱࡲ࡯ࡽࠧႩ"), int((time.time() - start_time) * 1000)) # bstack1llllll11ll_opy_ to bstack111111l1ll_opy_
    def __1llllllll1l_opy_(self):
        bstack1l11l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡳࡰࡦࡩࡥࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣ࡭ࡳࠦࡃࡍࡋࠣࡪࡱࡧࡧࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡵࡷࡵࡲࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡩ࡭ࡱ࡫ࠠ࡯ࡣࡰࡩࡸ࠲ࠠࡢࡰࡧࠤࡼ࡫ࠠࡴ࡫ࡰࡴࡱࡿࠠࡶࡲࡧࡥࡹ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡉࡌࡊࠢࡤࡶ࡬ࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡵࡪࡲࡷࡪࠦࡦࡪ࡮ࡨࡷ࠳ࠦࡕࡴࡧࡵࠫࡸࠦࡦࡪ࡮ࡷࡩࡷ࡯࡮ࡨࠢࡩࡰࡦ࡭ࡳࠡࠪ࠰ࡱ࠱ࠦ࠭࡬ࠫࠣࡶࡪࡳࡡࡪࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴࡢࡥࡷࠤࡦࡴࡤࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡤࡴࡵࡲࡩࡦࡦࠣࡲࡦࡺࡵࡳࡣ࡯ࡰࡾࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣႪ")
        try:
            if not self.bstack1l11ll1ll1_opy_:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡓࡵࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡶࡡࡵࡪࠣࡸࡴࠦࡳࡦࡶࠥႫ"))
                return
            bstack1lllllll11l_opy_ = []
            for flag in self.bstack1lllllllll1_opy_:
                if flag.startswith(bstack1l11l1l_opy_ (u"ࠬ࠳ࠧႬ")):
                    bstack1lllllll11l_opy_.append(flag)
                    continue
                bstack111111l111_opy_ = False
                if bstack1l11l1l_opy_ (u"࠭࠺࠻ࠩႭ") in flag:
                    bstack1llllll1l11_opy_ = flag.split(bstack1l11l1l_opy_ (u"ࠧ࠻࠼ࠪႮ"), 1)[0]
                    if os.path.exists(bstack1llllll1l11_opy_):
                        bstack111111l111_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l11l1l_opy_ (u"ࠨ࠰ࡳࡽࠬႯ"))):
                        bstack111111l111_opy_ = True
                if not bstack111111l111_opy_:
                    bstack1lllllll11l_opy_.append(flag)
            bstack1lllllll11l_opy_.extend(self.bstack1l11ll1ll1_opy_)
            self.bstack1lllllllll1_opy_ = bstack1lllllll11l_opy_
        except Exception as e:
            self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤࡸ࡫࡬ࡦࡥࡷࡳࡷࡹ࠺ࠡࡽࢀࠦႰ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1llllll11l1_opy_():
        return bstack1llllll1l1l_opy_(bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬႱ"))
    def bstack1111111111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l111l1_opy_ = -1
        if self.bstack1111111l11_opy_ and bstack1l11l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫႲ") in self.bstack1lllllll1ll_opy_:
            self.bstack11l111l1_opy_ = int(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬႳ")])
        try:
            bstack111111lll1_opy_ = [bstack1l11l1l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨႴ"), bstack1l11l1l_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪႵ"), bstack1l11l1l_opy_ (u"ࠨ࠯ࡳࠫႶ")]
            if self.bstack11l111l1_opy_ >= 0:
                bstack111111lll1_opy_.extend([bstack1l11l1l_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪႷ"), bstack1l11l1l_opy_ (u"ࠪ࠱ࡳ࠭Ⴘ")])
            for arg in bstack111111lll1_opy_:
                self.bstack1111111111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lllllll1l1_opy_(self):
        bstack1lllllllll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lllllllll1_opy_ = bstack1lllllllll1_opy_
        return self.bstack1lllllllll1_opy_
    def bstack11l1lll1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1llllll11l1_opy_():
                self.logger.warning(bstack111111l1l1_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1l11l1l_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦႹ"), bstack1lll111111_opy_, str(e))
    def bstack111111ll11_opy_(self, bstack1111111lll_opy_):
        bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
        if bstack1111111lll_opy_:
            self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩႺ"))
            self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"࠭ࡔࡳࡷࡨࠫႻ"))
        if bstack11llllll_opy_.bstack111111ll1l_opy_():
            self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ⴜ"))
            self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠨࡖࡵࡹࡪ࠭Ⴝ"))
        self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠩ࠰ࡴࠬႾ"))
        self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨႿ"))
        self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭Ⴠ"))
        self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬჁ"))
        if self.bstack11l111l1_opy_ > 1:
            self.bstack1lllllllll1_opy_.append(bstack1l11l1l_opy_ (u"࠭࠭࡯ࠩჂ"))
            self.bstack1lllllllll1_opy_.append(str(self.bstack11l111l1_opy_))
    def bstack11111l111l_opy_(self):
        if bstack111lll111l_opy_.bstack1l11lll11l_opy_(self.bstack1lllllll1ll_opy_):
             self.bstack1lllllllll1_opy_ += [
                bstack1llllll1ll1_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠭Ⴣ")), str(bstack111lll111l_opy_.bstack1l1l1ll1ll_opy_(self.bstack1lllllll1ll_opy_)),
                bstack1llllll1ll1_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧჄ")), str(bstack1llllll1ll1_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧჅ")))
            ]
    def bstack1llllll1lll_opy_(self):
        bstack111lllll1l_opy_ = []
        for spec in self.bstack1l11ll1ll1_opy_:
            bstack111111l1_opy_ = [spec]
            bstack111111l1_opy_ += self.bstack1lllllllll1_opy_
            bstack111lllll1l_opy_.append(bstack111111l1_opy_)
        self.bstack111lllll1l_opy_ = bstack111lllll1l_opy_
        return bstack111lllll1l_opy_
    def bstack1ll11l1l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llllll1111_opy_ = True
            return True
        except Exception as e:
            self.bstack1llllll1111_opy_ = False
        return self.bstack1llllll1111_opy_
    def bstack111lll1ll1_opy_(self):
        bstack1l11l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥ࡮ࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ჆")
        try:
            from browserstack_sdk.bstack11111ll1ll_opy_ import bstack11111lll11_opy_
            bstack11111l11l1_opy_ = bstack11111lll11_opy_(bstack11111ll1l1_opy_=self.bstack1lllllllll1_opy_)
            if not bstack11111l11l1_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬჇ"), False):
                self.logger.error(bstack1l11l1l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡧࡴࡻ࡮ࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥ჈").format(bstack11111l11l1_opy_.get(bstack1l11l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ჉"), bstack1l11l1l_opy_ (u"ࠧࡖࡰ࡮ࡲࡴࡽ࡮ࠡࡧࡵࡶࡴࡸࠧ჊"))))
                return 0
            count = bstack11111l11l1_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡥࡲࡹࡳࡺࠧ჋"), 0)
            self.logger.info(bstack1l11l1l_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠽ࠤࢀࢃࠢ჌").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l11l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢჍ").format(e))
            return 0
    def bstack1l1lllll1l_opy_(self, bstack11111l11ll_opy_, bstack1l1lllllll_opy_):
        bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ჎")] = self.bstack1lllllll1ll_opy_
        multiprocessing.set_start_method(bstack1l11l1l_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫ჏"))
        bstack1111llll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lllllll111_opy_ = manager.list()
        if bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩა") in self.bstack1lllllll1ll_opy_:
            for index, platform in enumerate(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪბ")]):
                bstack1111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11111l11ll_opy_,
                                                            args=(self.bstack1lllllllll1_opy_, bstack1l1lllllll_opy_, bstack1lllllll111_opy_)))
            bstack1111111ll1_opy_ = len(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫგ")])
        else:
            bstack1111llll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11111l11ll_opy_,
                                                        args=(self.bstack1lllllllll1_opy_, bstack1l1lllllll_opy_, bstack1lllllll111_opy_)))
            bstack1111111ll1_opy_ = 1
        i = 0
        for t in bstack1111llll_opy_:
            os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩდ")] = str(i)
            if bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ე") in self.bstack1lllllll1ll_opy_:
                os.environ[bstack1l11l1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬვ")] = json.dumps(self.bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨზ")][i % bstack1111111ll1_opy_])
            i += 1
            t.start()
        for t in bstack1111llll_opy_:
            t.join()
        return list(bstack1lllllll111_opy_)
    @staticmethod
    def bstack1ll1l11ll1_opy_(driver, bstack1llllllll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪთ"), None)
        if item and getattr(item, bstack1l11l1l_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩი"), None) and not getattr(item, bstack1l11l1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪკ"), False):
            logger.info(
                bstack1l11l1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣლ"))
            bstack1llllll111l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll1l11lll_opy_.bstack11ll11l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1111111l1l_opy_(self):
        bstack1l11l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡢࡦࠢࡨࡼࡪࡩࡵࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤმ")
        try:
            from browserstack_sdk.bstack11111ll1ll_opy_ import bstack11111lll11_opy_
            bstack111111llll_opy_ = bstack11111lll11_opy_(bstack11111ll1l1_opy_=self.bstack1lllllllll1_opy_)
            if not bstack111111llll_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬნ"), False):
                self.logger.error(bstack1l11l1l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤო").format(bstack111111llll_opy_.get(bstack1l11l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬპ"), bstack1l11l1l_opy_ (u"ࠧࡖࡰ࡮ࡲࡴࡽ࡮ࠡࡧࡵࡶࡴࡸࠧჟ"))))
                return []
            test_files = bstack111111llll_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠬრ"), [])
            count = bstack111111llll_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡦࡳࡺࡴࡴࠨს"), 0)
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷࡩࡩࠦࡻࡾࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࢀࢃࠠࡧ࡫࡯ࡩࡸࠨტ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧუ").format(e))
            return []