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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
logger = get_logger(__name__)
bstack1lllll11l1ll_opy_: Dict[str, float] = {}
bstack1lllll11l11l_opy_: List = []
bstack1lllll11l1l1_opy_ = 5
bstack1ll11lll11_opy_ = os.path.join(os.getcwd(), bstack1l111l1_opy_ (u"࠭࡬ࡰࡩࠪ⁃"), bstack1l111l1_opy_ (u"ࠧ࡬ࡧࡼ࠱ࡲ࡫ࡴࡳ࡫ࡦࡷ࠳ࡰࡳࡰࡰࠪ⁄"))
logging.getLogger(bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠪ⁅")).setLevel(logging.WARNING)
lock = FileLock(bstack1ll11lll11_opy_+bstack1l111l1_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ⁆"))
class bstack1lllll111lll_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack1lllll111ll1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1lllll111ll1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l111l1_opy_ (u"ࠥࡱࡪࡧࡳࡶࡴࡨࠦ⁇")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll11ll1ll1_opy_:
    global bstack1lllll11l1ll_opy_
    @staticmethod
    def bstack1ll1111l1l1_opy_(key: str):
        bstack1ll111ll11l_opy_ = bstack1ll11ll1ll1_opy_.bstack11ll1111l1l_opy_(key)
        bstack1ll11ll1ll1_opy_.mark(bstack1ll111ll11l_opy_+bstack1l111l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⁈"))
        return bstack1ll111ll11l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1lllll11l1ll_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ⁉").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll11ll1ll1_opy_.mark(end)
            bstack1ll11ll1ll1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥ⁊").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1lllll11l1ll_opy_ or end not in bstack1lllll11l1ll_opy_:
                logger.debug(bstack1l111l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠥࡵࡲࠡࡧࡱࡨࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠤ⁋").format(start,end))
                return
            duration: float = bstack1lllll11l1ll_opy_[end] - bstack1lllll11l1ll_opy_[start]
            bstack1lllll11ll11_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦ⁌"), bstack1l111l1_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ⁍")).lower() == bstack1l111l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ⁎")
            bstack1lllll11ll1l_opy_: bstack1lllll111lll_opy_ = bstack1lllll111lll_opy_(duration, label, bstack1lllll11l1ll_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l111l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦ⁏"), 0), command, test_name, hook_type, bstack1lllll11ll11_opy_)
            del bstack1lllll11l1ll_opy_[start]
            del bstack1lllll11l1ll_opy_[end]
            bstack1ll11ll1ll1_opy_.bstack1lllll111l1l_opy_(bstack1lllll11ll1l_opy_)
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡪࡧࡳࡶࡴ࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣ⁐").format(e))
    @staticmethod
    def bstack1lllll111l1l_opy_(bstack1lllll11ll1l_opy_):
        os.makedirs(os.path.dirname(bstack1ll11lll11_opy_)) if not os.path.exists(os.path.dirname(bstack1ll11lll11_opy_)) else None
        bstack1ll11ll1ll1_opy_.bstack1lllll11l111_opy_()
        try:
            with lock:
                with open(bstack1ll11lll11_opy_, bstack1l111l1_opy_ (u"ࠨࡲࠬࠤ⁑"), encoding=bstack1l111l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ⁒")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1lllll11ll1l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1lllll111l11_opy_:
            logger.debug(bstack1l111l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢࡾࢁࠧ⁓").format(bstack1lllll111l11_opy_))
            with lock:
                with open(bstack1ll11lll11_opy_, bstack1l111l1_opy_ (u"ࠤࡺࠦ⁔"), encoding=bstack1l111l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ⁕")) as file:
                    data = [bstack1lllll11ll1l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࡦࡶࡰࡦࡰࡧࠤࢀࢃࠢ⁖").format(str(e)))
        finally:
            if os.path.exists(bstack1ll11lll11_opy_+bstack1l111l1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦ⁗")):
                os.remove(bstack1ll11lll11_opy_+bstack1l111l1_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧ⁘"))
    @staticmethod
    def bstack1lllll11l111_opy_():
        attempt = 0
        while (attempt < bstack1lllll11l1l1_opy_):
            attempt += 1
            if os.path.exists(bstack1ll11lll11_opy_+bstack1l111l1_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ⁙")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11ll1111l1l_opy_(label: str) -> str:
        try:
            return bstack1l111l1_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢ⁚").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ⁛").format(e))