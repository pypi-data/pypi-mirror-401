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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1llll1llll1_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1llll1l1l1l_opy_, bstack1lll1llll11_opy_
class bstack1lll11ll1l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l111l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᙩ").format(self.name)
class bstack1ll1lll1111_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l111l1_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᙪ").format(self.name)
class bstack1ll1llllll1_opy_(bstack1llll1l1l1l_opy_):
    bstack1l1lll111l1_opy_: List[str]
    bstack11lll111l11_opy_: Dict[str, str]
    state: bstack1ll1lll1111_opy_
    bstack1llll11111l_opy_: datetime
    bstack1lll1l1lll1_opy_: datetime
    def __init__(
        self,
        context: bstack1lll1llll11_opy_,
        bstack1l1lll111l1_opy_: List[str],
        bstack11lll111l11_opy_: Dict[str, str],
        state=bstack1ll1lll1111_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1lll111l1_opy_ = bstack1l1lll111l1_opy_
        self.bstack11lll111l11_opy_ = bstack11lll111l11_opy_
        self.state = state
        self.bstack1llll11111l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll1l1lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll1111l1_opy_(self, bstack1lll1lll11l_opy_: bstack1ll1lll1111_opy_):
        bstack1llll1ll11l_opy_ = bstack1ll1lll1111_opy_(bstack1lll1lll11l_opy_).name
        if not bstack1llll1ll11l_opy_:
            return False
        if bstack1lll1lll11l_opy_ == self.state:
            return False
        self.state = bstack1lll1lll11l_opy_
        self.bstack1lll1l1lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11111l1l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll11ll111l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l111ll1l_opy_: int = None
    bstack1l1l1ll11ll_opy_: str = None
    bstack11lll_opy_: str = None
    bstack11l11111l_opy_: str = None
    bstack1l1l11l11l1_opy_: str = None
    bstack11lll1l11l1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll111l11l1_opy_ = bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᙫ")
    bstack11lll1l1111_opy_ = bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᙬ")
    bstack1l1llll111l_opy_ = bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦ᙭")
    bstack1l1111l111l_opy_ = bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥ᙮")
    bstack1l111111lll_opy_ = bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᙯ")
    bstack1l11l11l1l1_opy_ = bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᙰ")
    bstack1l1l11lll1l_opy_ = bstack1l111l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᙱ")
    bstack1l1l1l1lll1_opy_ = bstack1l111l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᙲ")
    bstack1l1l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᙳ")
    bstack11lll11l1ll_opy_ = bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᙴ")
    bstack1ll111ll111_opy_ = bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᙵ")
    bstack1l1l1llllll_opy_ = bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᙶ")
    bstack11llllll1l1_opy_ = bstack1l111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᙷ")
    bstack1l11ll1ll11_opy_ = bstack1l111l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᙸ")
    bstack1ll1111ll1l_opy_ = bstack1l111l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᙹ")
    bstack1l11l11llll_opy_ = bstack1l111l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᙺ")
    bstack1l1111111ll_opy_ = bstack1l111l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᙻ")
    bstack11lllll1l11_opy_ = bstack1l111l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᙼ")
    bstack1l111111l1l_opy_ = bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᙽ")
    bstack11ll1lllll1_opy_ = bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᙾ")
    bstack1l111l111l1_opy_ = bstack1l111l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᙿ")
    bstack11llll111ll_opy_ = bstack1l111l1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤ ")
    bstack11lll1111l1_opy_ = bstack1l111l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᚁ")
    bstack1l11111111l_opy_ = bstack1l111l1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᚂ")
    bstack11lllll1lll_opy_ = bstack1l111l1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᚃ")
    bstack11lll1l11ll_opy_ = bstack1l111l1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᚄ")
    bstack11lll1111ll_opy_ = bstack1l111l1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᚅ")
    bstack1l11111ll1l_opy_ = bstack1l111l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᚆ")
    bstack11lll11l11l_opy_ = bstack1l111l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᚇ")
    bstack11lll1lll11_opy_ = bstack1l111l1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᚈ")
    bstack11lllll1111_opy_ = bstack1l111l1_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᚉ")
    bstack1l1l1l111l1_opy_ = bstack1l111l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᚊ")
    bstack1l1l111l111_opy_ = bstack1l111l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᚋ")
    bstack1l11llll1l1_opy_ = bstack1l111l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᚌ")
    bstack1llll11llll_opy_: Dict[str, bstack1ll1llllll1_opy_] = dict()
    bstack11ll1ll1ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1lll111l1_opy_: List[str]
    bstack11lll111l11_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1lll111l1_opy_: List[str],
        bstack11lll111l11_opy_: Dict[str, str],
        bstack1llll1llll1_opy_: bstack1llll1lllll_opy_
    ):
        self.bstack1l1lll111l1_opy_ = bstack1l1lll111l1_opy_
        self.bstack11lll111l11_opy_ = bstack11lll111l11_opy_
        self.bstack1llll1llll1_opy_ = bstack1llll1llll1_opy_
    def track_event(
        self,
        context: bstack1l11111l1l1_opy_,
        test_framework_state: bstack1ll1lll1111_opy_,
        test_hook_state: bstack1lll11ll1l1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l111l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᚍ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11111l1ll_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1111lll1l_opy_ = TestFramework.bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_)
        if not bstack1l1111lll1l_opy_ in TestFramework.bstack11ll1ll1ll1_opy_:
            return
        self.logger.debug(bstack1l111l1_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᚎ").format(len(TestFramework.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_])))
        for callback in TestFramework.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_]:
            try:
                callback(self, instance, bstack1lll1ll1111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᚏ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l1l11lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1l1111111_opy_(self, instance, bstack1lll1ll1111_opy_):
        return
    @abc.abstractmethod
    def bstack1l1l1ll1l1l_opy_(self, instance, bstack1lll1ll1111_opy_):
        return
    @staticmethod
    def bstack1llll11ll1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llll1l1l1l_opy_.create_context(target)
        instance = TestFramework.bstack1llll11llll_opy_.get(ctx.id, None)
        if instance and instance.bstack1llll1l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l11l1lll_opy_(reverse=True) -> List[bstack1ll1llllll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llll11llll_opy_.values(),
            ),
            key=lambda t: t.bstack1llll11111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llll111111_opy_(ctx: bstack1lll1llll11_opy_, reverse=True) -> List[bstack1ll1llllll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llll11llll_opy_.values(),
            ),
            key=lambda t: t.bstack1llll11111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll1ll111l_opy_(instance: bstack1ll1llllll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llll1l111l_opy_(instance: bstack1ll1llllll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll1111l1_opy_(instance: bstack1ll1llllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l111l1_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᚐ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11lll111ll1_opy_(instance: bstack1ll1llllll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l111l1_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᚑ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11ll1ll111l_opy_(instance: bstack1ll1lll1111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l111l1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᚒ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1llll11ll1l_opy_(target, strict)
        return TestFramework.bstack1llll1l111l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1llll11ll1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11llll1l111_opy_(instance: bstack1ll1llllll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11llll1ll1l_opy_(instance: bstack1ll1llllll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_]):
        return bstack1l111l1_opy_ (u"ࠦ࠿ࠨᚓ").join((bstack1ll1lll1111_opy_(bstack1lll1ll1111_opy_[0]).name, bstack1lll11ll1l1_opy_(bstack1lll1ll1111_opy_[1]).name))
    @staticmethod
    def bstack1ll111l11ll_opy_(bstack1lll1ll1111_opy_: Tuple[bstack1ll1lll1111_opy_, bstack1lll11ll1l1_opy_], callback: Callable):
        bstack1l1111lll1l_opy_ = TestFramework.bstack1l1111ll111_opy_(bstack1lll1ll1111_opy_)
        TestFramework.logger.debug(bstack1l111l1_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᚔ").format(bstack1l1111lll1l_opy_))
        if not bstack1l1111lll1l_opy_ in TestFramework.bstack11ll1ll1ll1_opy_:
            TestFramework.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_] = []
        TestFramework.bstack11ll1ll1ll1_opy_[bstack1l1111lll1l_opy_].append(callback)
    @staticmethod
    def bstack1l1l11111l1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᚕ"):
            return klass.__qualname__
        return module + bstack1l111l1_opy_ (u"ࠢ࠯ࠤᚖ") + klass.__qualname__
    @staticmethod
    def bstack1l1l11ll11l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}