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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11111l11l_opy_
from browserstack_sdk.bstack1lll111lll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll1lll1_opy_, bstack1llllll11ll_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack1llll111l_opy_
from bstack_utils.constants import bstack1lllll1ll1l_opy_
from bstack_utils.bstack11111ll1_opy_ import bstack1l111ll1l_opy_
from bstack_utils.bstack1111111lll_opy_ import bstack1lllll11ll1_opy_
class bstack1lllllllll_opy_:
    def __init__(self, args, logger, bstack1lllllll1l1_opy_, bstack1lllllll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll1l1_opy_ = bstack1lllllll1l1_opy_
        self.bstack1lllllll1ll_opy_ = bstack1lllllll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111lll111_opy_ = []
        self.bstack1lllll1l111_opy_ = []
        self.bstack11l11l1l_opy_ = []
        self.bstack1llllll1111_opy_ = self.bstack11lllll11l_opy_()
        self.bstack1lll111l_opy_ = -1
    def bstack11lllll1l1_opy_(self, bstack1lllllllll1_opy_):
        self.parse_args()
        self.bstack111111111l_opy_()
        self.bstack1lllll11lll_opy_(bstack1lllllllll1_opy_)
        self.bstack1111111l1l_opy_()
    def bstack111l1l1l1_opy_(self):
        bstack11111ll1_opy_ = bstack1l111ll1l_opy_.bstack1llll1ll11_opy_(self.bstack1lllllll1l1_opy_, self.logger)
        if bstack11111ll1_opy_ is None:
            self.logger.warn(bstack1l111l1_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨ჆"))
            return
        bstack11111111ll_opy_ = False
        bstack11111ll1_opy_.bstack1llllll111l_opy_(bstack1l111l1_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧჇ"), bstack11111ll1_opy_.bstack1l1l1111l1_opy_())
        start_time = time.time()
        if bstack11111ll1_opy_.bstack1l1l1111l1_opy_():
            test_files = self.bstack1llllll1l11_opy_()
            bstack11111111ll_opy_ = True
            bstack1llllll11l1_opy_ = bstack11111ll1_opy_.bstack1lllllll111_opy_(test_files)
            if bstack1llllll11l1_opy_:
                self.bstack111lll111_opy_ = [os.path.normpath(item) for item in bstack1llllll11l1_opy_]
                self.__1111111ll1_opy_()
                bstack11111ll1_opy_.bstack111111l11l_opy_(bstack11111111ll_opy_)
                self.logger.info(bstack1l111l1_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ჈").format(self.bstack111lll111_opy_))
            else:
                self.logger.info(bstack1l111l1_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦ჉"))
        bstack11111ll1_opy_.bstack1llllll111l_opy_(bstack1l111l1_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥ჊"), int((time.time() - start_time) * 1000)) # bstack1llllllll11_opy_ to bstack1lllll1llll_opy_
    def __1111111ll1_opy_(self):
        bstack1l111l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡱ࡮ࡤࡧࡪࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡ࡫ࡱࠤࡈࡒࡉࠡࡨ࡯ࡥ࡬ࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡺࡵࡳࡰࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡧ࡫࡯ࡩࠥࡴࡡ࡮ࡧࡶ࠰ࠥࡧ࡮ࡥࠢࡺࡩࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡻࡰࡥࡣࡷࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡇࡑࡏࠠࡢࡴࡪࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡺࡨࡰࡵࡨࠤ࡫࡯࡬ࡦࡵ࠱ࠤ࡚ࡹࡥࡳࠩࡶࠤ࡫࡯࡬ࡵࡧࡵ࡭ࡳ࡭ࠠࡧ࡮ࡤ࡫ࡸࠦࠨ࠮࡯࠯ࠤ࠲ࡱࠩࠡࡴࡨࡱࡦ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡧࡣࡵࠢࡤࡲࡩࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡢࡲࡳࡰ࡮࡫ࡤࠡࡰࡤࡸࡺࡸࡡ࡭࡮ࡼࠤࡩࡻࡲࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ჋")
        try:
            if not self.bstack111lll111_opy_:
                self.logger.debug(bstack1l111l1_opy_ (u"ࠤࡑࡳࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡴࡦࡺࡨࠡࡶࡲࠤࡸ࡫ࡴࠣ჌"))
                return
            bstack1lllll1ll11_opy_ = []
            for flag in self.bstack1lllll1l111_opy_:
                if flag.startswith(bstack1l111l1_opy_ (u"ࠪ࠱ࠬჍ")):
                    bstack1lllll1ll11_opy_.append(flag)
                    continue
                bstack1lllll1l1l1_opy_ = False
                if bstack1l111l1_opy_ (u"ࠫ࠿ࡀࠧ჎") in flag:
                    bstack1llllll1ll1_opy_ = flag.split(bstack1l111l1_opy_ (u"ࠬࡀ࠺ࠨ჏"), 1)[0]
                    if os.path.exists(bstack1llllll1ll1_opy_):
                        bstack1lllll1l1l1_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l111l1_opy_ (u"࠭࠮ࡱࡻࠪა"))):
                        bstack1lllll1l1l1_opy_ = True
                if not bstack1lllll1l1l1_opy_:
                    bstack1lllll1ll11_opy_.append(flag)
            bstack1lllll1ll11_opy_.extend(self.bstack111lll111_opy_)
            self.bstack1lllll1l111_opy_ = bstack1lllll1ll11_opy_
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡶࡩࡱ࡫ࡣࡵࡱࡵࡷ࠿ࠦࡻࡾࠤბ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111111l1_opy_():
        return bstack1lllll11ll1_opy_(bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪგ"))
    def bstack1lllll1lll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll111l_opy_ = -1
        if self.bstack1lllllll1ll_opy_ and bstack1l111l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩდ") in self.bstack1lllllll1l1_opy_:
            self.bstack1lll111l_opy_ = int(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪე")])
        try:
            bstack1llllllllll_opy_ = [bstack1l111l1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ვ"), bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨზ"), bstack1l111l1_opy_ (u"࠭࠭ࡱࠩთ")]
            if self.bstack1lll111l_opy_ >= 0:
                bstack1llllllllll_opy_.extend([bstack1l111l1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨი"), bstack1l111l1_opy_ (u"ࠨ࠯ࡱࠫკ")])
            for arg in bstack1llllllllll_opy_:
                self.bstack1lllll1lll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111111111l_opy_(self):
        bstack1lllll1l111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lllll1l111_opy_ = bstack1lllll1l111_opy_
        return self.bstack1lllll1l111_opy_
    def bstack11l1l1l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack11111111l1_opy_():
                self.logger.warning(bstack1llllll11ll_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1l111l1_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤლ"), bstack1ll1lll1_opy_, str(e))
    def bstack1lllll11lll_opy_(self, bstack1lllllllll1_opy_):
        bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
        if bstack1lllllllll1_opy_:
            self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧმ"))
            self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"࡙ࠫࡸࡵࡦࠩნ"))
        if bstack1l1l1111_opy_.bstack1llllll1lll_opy_():
            self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫო"))
            self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"࠭ࡔࡳࡷࡨࠫპ"))
        self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠧ࠮ࡲࠪჟ"))
        self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭რ"))
        self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫს"))
        self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪტ"))
        if self.bstack1lll111l_opy_ > 1:
            self.bstack1lllll1l111_opy_.append(bstack1l111l1_opy_ (u"ࠫ࠲ࡴࠧუ"))
            self.bstack1lllll1l111_opy_.append(str(self.bstack1lll111l_opy_))
    def bstack1111111l1l_opy_(self):
        if bstack1llll111l_opy_.bstack1ll111l1ll_opy_(self.bstack1lllllll1l1_opy_):
             self.bstack1lllll1l111_opy_ += [
                bstack1lllll1ll1l_opy_.get(bstack1l111l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫფ")), str(bstack1llll111l_opy_.bstack1lll1111_opy_(self.bstack1lllllll1l1_opy_)),
                bstack1lllll1ll1l_opy_.get(bstack1l111l1_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬქ")), str(bstack1lllll1ll1l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬღ")))
            ]
    def bstack1llllllll1l_opy_(self):
        bstack11l11l1l_opy_ = []
        for spec in self.bstack111lll111_opy_:
            bstack11llll11ll_opy_ = [spec]
            bstack11llll11ll_opy_ += self.bstack1lllll1l111_opy_
            bstack11l11l1l_opy_.append(bstack11llll11ll_opy_)
        self.bstack11l11l1l_opy_ = bstack11l11l1l_opy_
        return bstack11l11l1l_opy_
    def bstack11lllll11l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llllll1111_opy_ = True
            return True
        except Exception as e:
            self.bstack1llllll1111_opy_ = False
        return self.bstack1llllll1111_opy_
    def bstack1l111111_opy_(self):
        bstack1l111l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࡳࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤყ")
        try:
            from browserstack_sdk.bstack111111ll1l_opy_ import bstack111111llll_opy_
            bstack1111111l11_opy_ = bstack111111llll_opy_(bstack111111l1l1_opy_=self.bstack1lllll1l111_opy_)
            if not bstack1111111l11_opy_.get(bstack1l111l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪშ"), False):
                self.logger.error(bstack1l111l1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡥࡲࡹࡳࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣჩ").format(bstack1111111l11_opy_.get(bstack1l111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪც"), bstack1l111l1_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬძ"))))
                return 0
            count = bstack1111111l11_opy_.get(bstack1l111l1_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬწ"), 0)
            self.logger.info(bstack1l111l1_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠻ࠢࡾࢁࠧჭ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧხ").format(e))
            return 0
    def bstack1lllll11_opy_(self, bstack1lllll1l1ll_opy_, bstack11lllll1l1_opy_):
        bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩჯ")] = self.bstack1lllllll1l1_opy_
        multiprocessing.set_start_method(bstack1l111l1_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩჰ"))
        bstack1l1lll111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack111111l111_opy_ = manager.list()
        if bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧჱ") in self.bstack1lllllll1l1_opy_:
            for index, platform in enumerate(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨჲ")]):
                bstack1l1lll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lllll1l1ll_opy_,
                                                            args=(self.bstack1lllll1l111_opy_, bstack11lllll1l1_opy_, bstack111111l111_opy_)))
            bstack1llllll1l1l_opy_ = len(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩჳ")])
        else:
            bstack1l1lll111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lllll1l1ll_opy_,
                                                        args=(self.bstack1lllll1l111_opy_, bstack11lllll1l1_opy_, bstack111111l111_opy_)))
            bstack1llllll1l1l_opy_ = 1
        i = 0
        for t in bstack1l1lll111l_opy_:
            os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧჴ")] = str(i)
            if bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫჵ") in self.bstack1lllllll1l1_opy_:
                os.environ[bstack1l111l1_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪჶ")] = json.dumps(self.bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ჷ")][i % bstack1llllll1l1l_opy_])
            i += 1
            t.start()
        for t in bstack1l1lll111l_opy_:
            t.join()
        return list(bstack111111l111_opy_)
    @staticmethod
    def bstack1ll1l111ll_opy_(driver, bstack1lllll1l11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨჸ"), None)
        if item and getattr(item, bstack1l111l1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧჹ"), None) and not getattr(item, bstack1l111l1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨჺ"), False):
            logger.info(
                bstack1l111l1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨ჻"))
            bstack1111111111_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11111l11l_opy_.bstack1lll1l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1llllll1l11_opy_(self):
        bstack1l111l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢჼ")
        try:
            from browserstack_sdk.bstack111111ll1l_opy_ import bstack111111llll_opy_
            bstack1lllllll11l_opy_ = bstack111111llll_opy_(bstack111111l1l1_opy_=self.bstack1lllll1l111_opy_)
            if not bstack1lllllll11l_opy_.get(bstack1l111l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪჽ"), False):
                self.logger.error(bstack1l111l1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢჾ").format(bstack1lllllll11l_opy_.get(bstack1l111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪჿ"), bstack1l111l1_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᄀ"))))
                return []
            test_files = bstack1lllllll11l_opy_.get(bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠪᄁ"), [])
            count = bstack1lllllll11l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡤࡱࡸࡲࡹ࠭ᄂ"), 0)
            self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡾࢁࠥ࡬ࡩ࡭ࡧࡶࠦᄃ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᄄ").format(e))
            return []