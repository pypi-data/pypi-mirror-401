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
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import (
    bstack1lll1l1ll11_opy_,
    bstack1llll11l111_opy_,
    bstack1llll11l11l_opy_,
    bstack1llll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll111_opy_ import bstack1ll1l1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1lll1llll11_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1ll1ll_opy_
import weakref
class bstack1l1ll11l1ll_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l1ll111lll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1llll11l1ll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1llll11l1ll_opy_]]
    def __init__(self, bstack1l1ll111lll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1ll111l11_opy_ = dict()
        self.bstack1l1ll111lll_opy_ = bstack1l1ll111lll_opy_
        self.frameworks = frameworks
        bstack1ll1l1111l1_opy_.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.bstack1lll1ll1l1l_opy_, bstack1llll11l111_opy_.POST), self.__1l1ll111ll1_opy_)
        if any(bstack1ll11llll11_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_(
                (bstack1lll1l1ll11_opy_.bstack1llll111l1l_opy_, bstack1llll11l111_opy_.PRE), self.__1l1ll11l1l1_opy_
            )
            bstack1ll11llll11_opy_.bstack1ll111l11ll_opy_(
                (bstack1lll1l1ll11_opy_.QUIT, bstack1llll11l111_opy_.POST), self.__1l1ll11l111_opy_
            )
    def __1l1ll111ll1_opy_(
        self,
        f: bstack1ll1l1111l1_opy_,
        bstack1l1ll111111_opy_: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l111l1_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢዿ"):
                return
            contexts = bstack1l1ll111111_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l111l1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦጀ") in page.url:
                                self.logger.debug(bstack1l111l1_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤጁ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, self.bstack1l1ll111lll_opy_, True)
                                self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨጂ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠤࠥጃ"))
        except Exception as e:
            self.logger.debug(bstack1l111l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢጄ"),e)
    def __1l1ll11l1l1_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llll11l11l_opy_.bstack1llll1l111l_opy_(instance, self.bstack1l1ll111lll_opy_, False):
            return
        if not f.bstack1l1ll1l11ll_opy_(f.hub_url(driver)):
            self.bstack1l1ll111l11_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, self.bstack1l1ll111lll_opy_, True)
            self.logger.debug(bstack1l111l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤጅ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠧࠨጆ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, self.bstack1l1ll111lll_opy_, True)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡩ࡯࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣጇ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠢࠣገ"))
    def __1l1ll11l111_opy_(
        self,
        f: bstack1ll11llll11_opy_,
        driver: object,
        exec: Tuple[bstack1llll11l1ll_opy_, str],
        bstack1lll1ll1111_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1llll11l111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1ll11ll11_opy_(instance)
        self.logger.debug(bstack1l111l1_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡳࡸ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥጉ") + str(instance.ref()) + bstack1l111l1_opy_ (u"ࠤࠥጊ"))
    def bstack1l1ll1111l1_opy_(self, context: bstack1lll1llll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1llll11l1ll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1ll11ll1l_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1ll11llll11_opy_.bstack1l1ll11l11l_opy_(data[1])
                    and data[1].bstack1l1ll11ll1l_opy_(context)
                    and getattr(data[0](), bstack1l111l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢጋ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll11111l_opy_, reverse=reverse)
    def bstack1l1ll1111ll_opy_(self, context: bstack1lll1llll11_opy_, reverse=True) -> List[Tuple[Callable, bstack1llll11l1ll_opy_]]:
        matches = []
        for data in self.bstack1l1ll111l11_opy_.values():
            if (
                data[1].bstack1l1ll11ll1l_opy_(context)
                and getattr(data[0](), bstack1l111l1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣጌ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll11111l_opy_, reverse=reverse)
    def bstack1l1ll111l1l_opy_(self, instance: bstack1llll11l1ll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1ll11ll11_opy_(self, instance: bstack1llll11l1ll_opy_) -> bool:
        if self.bstack1l1ll111l1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llll11l11l_opy_.bstack1llll1111l1_opy_(instance, self.bstack1l1ll111lll_opy_, False)
            return True
        return False