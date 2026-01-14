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
import atexit
import shlex
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack1111ll1l_opy_ import bstack11llll1ll_opy_
from browserstack_sdk.bstack11lll11l1l_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11llll111_opy_
from bstack_utils.messages import bstack111l11lll_opy_, bstack1l1lll11ll_opy_, bstack11l1l11l_opy_, bstack11l11l11_opy_, bstack11l1l1l1_opy_, bstack1l1111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11lllll1_opy_ import get_logger
from bstack_utils.helper import bstack1l1111lll1_opy_
from browserstack_sdk.bstack11l1ll1l1l_opy_ import bstack11l1ll11l_opy_
logger = get_logger(__name__)
def bstack1lll111ll1_opy_():
  global CONFIG
  headers = {
        bstack1l11l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1111lll1_opy_(CONFIG, bstack11llll111_opy_)
  try:
    response = requests.get(bstack11llll111_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111ll1l1l1_opy_ = response.json()[bstack1l11l1l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111l11lll_opy_.format(response.json()))
      return bstack111ll1l1l1_opy_
    else:
      logger.debug(bstack1l1lll11ll_opy_.format(bstack1l11l1l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1lll11ll_opy_.format(e))
def bstack1ll1lllll_opy_(hub_url):
  global CONFIG
  url = bstack1l11l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l11l1l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l11l1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1111lll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1l11l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l11l11_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11ll1lll_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack11lllll1l_opy_():
  try:
    global bstack1l1llll111_opy_
    global CONFIG
    if bstack1l11l1l_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1l11l1l_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack1l1ll1l1l1_opy_
      bstack1ll11l111_opy_ = CONFIG[bstack1l11l1l_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack1ll11l111_opy_ in bstack1l1ll1l1l1_opy_:
        bstack1l1llll111_opy_ = bstack1l1ll1l1l1_opy_[bstack1ll11l111_opy_]
        logger.debug(bstack11l1l1l1_opy_.format(bstack1l1llll111_opy_))
        return
      else:
        logger.debug(bstack1l11l1l_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack1ll11l111_opy_))
    bstack111ll1l1l1_opy_ = bstack1lll111ll1_opy_()
    bstack1l111ll111_opy_ = []
    results = []
    for bstack1lll1llll_opy_ in bstack111ll1l1l1_opy_:
      bstack1l111ll111_opy_.append(bstack11l1ll11l_opy_(target=bstack1ll1lllll_opy_,args=(bstack1lll1llll_opy_,)))
    for t in bstack1l111ll111_opy_:
      t.start()
    for t in bstack1l111ll111_opy_:
      results.append(t.join())
    bstack1l1l11l1l1_opy_ = {}
    for item in results:
      hub_url = item[bstack1l11l1l_opy_ (u"ࠨࡪࡸࡦࡤࡻࡲ࡭ࠩࢂ")]
      latency = item[bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡹ࡫࡮ࡤࡻࠪࢃ")]
      bstack1l1l11l1l1_opy_[hub_url] = latency
    bstack1l111ll1ll_opy_ = min(bstack1l1l11l1l1_opy_, key= lambda x: bstack1l1l11l1l1_opy_[x])
    bstack1l1llll111_opy_ = bstack1l111ll1ll_opy_
    logger.debug(bstack11l1l1l1_opy_.format(bstack1l111ll1ll_opy_))
  except Exception as e:
    logger.debug(bstack1l1111l1l_opy_.format(e))
from browserstack_sdk.bstack11l1ll11ll_opy_ import *
from browserstack_sdk.bstack11l1ll1l1l_opy_ import *
from browserstack_sdk.bstack11l1l111ll_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack11lllll1_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll111l11_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack11lll1ll_opy_():
    global bstack1l1llll111_opy_
    try:
        bstack11ll1l11_opy_ = bstack1llll1l1ll_opy_()
        bstack11llll1l1_opy_(bstack11ll1l11_opy_)
        hub_url = bstack11ll1l11_opy_.get(bstack1l11l1l_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1l11l1l_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1l11l1l_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1l11l1l_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1l1llll111_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1llll1l1ll_opy_():
    global CONFIG
    bstack1ll1ll1111_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1l11l1l_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1l11l1l_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1ll1ll1111_opy_, str):
        raise ValueError(bstack1l11l1l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack11ll1l11_opy_ = bstack1ll1111lll_opy_(bstack1ll1ll1111_opy_)
        return bstack11ll1l11_opy_
    except Exception as e:
        logger.error(bstack1l11l1l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1ll1111lll_opy_(bstack1ll1ll1111_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l11l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1l11l1l_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l11ll1l_opy_ + bstack1ll1ll1111_opy_
        auth = (CONFIG[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack1l1l1l1lll_opy_ = json.loads(response.text)
            return bstack1l1l1l1lll_opy_
    except ValueError as ve:
        logger.error(bstack1l11l1l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l11l1l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11llll1l1_opy_(bstack111ll1l11_opy_):
    global CONFIG
    if bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1l11l1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1l11l1l_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack111ll1l11_opy_:
        bstack11ll1l1l1l_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11ll1l1l1l_opy_)
        bstack1l1ll111l1_opy_ = bstack111ll1l11_opy_.get(bstack1l11l1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1l11111l1_opy_ = bstack1l11l1l_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1l1ll111l1_opy_)
        logger.debug(bstack1l11l1l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1l11111l1_opy_)
        bstack1l111l1111_opy_ = {
            bstack1l11l1l_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1l11l1l_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1l11l1l_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1l11l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1l11l1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1l11111l1_opy_
        }
        bstack11ll1l1l1l_opy_.update(bstack1l111l1111_opy_)
        logger.debug(bstack1l11l1l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11ll1l1l1l_opy_)
        CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11ll1l1l1l_opy_
        logger.debug(bstack1l11l1l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack11l11ll11l_opy_():
    bstack11ll1l11_opy_ = bstack1llll1l1ll_opy_()
    if not bstack11ll1l11_opy_[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1l11l1l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack11ll1l11_opy_[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1l11l1l_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack11l1l1l11_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack11lll11ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l11l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack1l1l111l1_opy_
        logger.debug(bstack1l11l1l_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l11l1l_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1l11l1l_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack111l11ll1_opy_ = json.loads(response.text)
                bstack11111l1l1_opy_ = bstack111l11ll1_opy_.get(bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack11111l1l1_opy_:
                    bstack1l1ll1l1_opy_ = bstack11111l1l1_opy_[0]
                    build_hashed_id = bstack1l1ll1l1_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack1l1lll1l_opy_ = bstack111l1ll11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack1l1lll1l_opy_])
                    logger.info(bstack11ll1l11l_opy_.format(bstack1l1lll1l_opy_))
                    bstack111l1ll1l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack111l1ll1l_opy_ += bstack1l11l1l_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack111l1ll1l_opy_ != bstack1l1ll1l1_opy_.get(bstack1l11l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1lll1l1l1l_opy_.format(bstack1l1ll1l1_opy_.get(bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack111l1ll1l_opy_))
                    return result
                else:
                    logger.debug(bstack1l11l1l_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1l11l1l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1l11l1l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1l11l1l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1llll1l1l_opy_ import bstack1llll1l1l_opy_, bstack1l11ll1l1_opy_, bstack1ll11llll1_opy_, bstack11l1l111_opy_
from bstack_utils.measure import bstack1lll1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll111lll_opy_ import bstack11l1llll11_opy_
from bstack_utils.messages import *
from bstack_utils import bstack11lllll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1ll11l1_opy_, bstack11l111ll11_opy_, bstack11l11l1l1l_opy_, bstack1ll1ll11ll_opy_, \
  bstack111111lll_opy_, \
  Notset, bstack1lllll111l_opy_, \
  bstack11lll1l11_opy_, bstack1lll1l1ll1_opy_, bstack1ll111l111_opy_, bstack11l1111l1_opy_, bstack1111ll11_opy_, bstack111l111l_opy_, \
  bstack11ll1lll1_opy_, \
  bstack11111111_opy_, bstack1ll1ll1l11_opy_, bstack1l11ll1111_opy_, bstack1llll11111_opy_, \
  bstack111llll11_opy_, bstack111llllll1_opy_, bstack11lll1l1l_opy_, bstack11l1l1111_opy_, bstack111llll1ll_opy_
from bstack_utils.bstack111l11ll_opy_ import bstack11lllll11l_opy_
from bstack_utils.bstack1l11l1ll11_opy_ import bstack1lll111l_opy_, bstack11lll11lll_opy_
from bstack_utils.bstack11l11ll11_opy_ import bstack111lll1l_opy_
from bstack_utils.bstack1ll1111l11_opy_ import bstack1l11l11l_opy_, bstack1ll1ll11l_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack1l111lll_opy_
from bstack_utils.bstack1l1l1l1ll1_opy_ import bstack1l11111ll_opy_
from bstack_utils.proxy import bstack111l11l11_opy_, bstack1l1111lll1_opy_, bstack111111l1l_opy_, bstack11l1111ll1_opy_
from bstack_utils.bstack1ll1lll11_opy_ import bstack11ll111ll1_opy_, bstack1ll1l11l1_opy_
import bstack_utils.bstack1l111lll1_opy_ as bstack1l11l1l1_opy_
import bstack_utils.bstack1111111l_opy_ as bstack111ll111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11ll_opy_ import bstack111lll1l11_opy_
from bstack_utils.bstack1lll11lll1_opy_ import bstack111lll111l_opy_
from bstack_utils.bstack1l111ll1l_opy_ import bstack11l1ll1l11_opy_
if os.getenv(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack11l1l11ll1_opy_()
else:
  os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1l11l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack111l11l1_opy_ = bstack1l11l1l_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
bstack1l111l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࣁ")
from ._version import __version__
bstack1l1ll1l1l_opy_ = None
CONFIG = {}
bstack1l1l111l1l_opy_ = {}
bstack11l1l1l1l_opy_ = {}
bstack11l11ll1ll_opy_ = None
bstack11111llll_opy_ = None
bstack1lll1l11l_opy_ = None
bstack11lllllll_opy_ = -1
bstack1l1l1ll1_opy_ = 0
bstack11ll1l1lll_opy_ = bstack1llll11ll_opy_
bstack1l1l1111_opy_ = 1
bstack11ll1ll1l1_opy_ = False
bstack1l1ll11ll1_opy_ = False
bstack1ll1ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪࣂ")
bstack1llllll11_opy_ = bstack1l11l1l_opy_ (u"ࠪࠫࣃ")
bstack1l11l1l111_opy_ = False
bstack11llllll1_opy_ = True
bstack1l11l1lll_opy_ = bstack1l11l1l_opy_ (u"ࠫࠬࣄ")
bstack1ll1l11111_opy_ = []
bstack1ll1l111_opy_ = threading.Lock()
bstack1l11ll1ll_opy_ = threading.Lock()
bstack1l1llll111_opy_ = bstack1l11l1l_opy_ (u"ࠬ࠭ࣅ")
bstack11l111l1ll_opy_ = False
bstack111l1lll_opy_ = None
bstack1l111lllll_opy_ = None
bstack11lll1l11l_opy_ = None
bstack11l11ll1_opy_ = -1
bstack11l11111l_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"࠭ࡾࠨࣆ")), bstack1l11l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1l11l1l_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1l111llll1_opy_ = 0
bstack1ll11l11l_opy_ = 0
bstack1ll1llll11_opy_ = []
bstack1l1ll1lll_opy_ = []
bstack111lll1111_opy_ = []
bstack111l111ll_opy_ = []
bstack1lllll11l_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪࣉ")
bstack1111llll1_opy_ = bstack1l11l1l_opy_ (u"ࠪࠫ࣊")
bstack1l11ll111_opy_ = False
bstack1ll1lll111_opy_ = False
bstack11l1l1ll1l_opy_ = {}
bstack11111l111_opy_ = {}
bstack11lllll111_opy_ = None
bstack111l1111_opy_ = None
bstack11ll11l1ll_opy_ = None
bstack1l11lll111_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack111l1l111_opy_ = None
bstack11ll1ll1ll_opy_ = None
bstack11ll11ll1_opy_ = None
bstack1ll1ll111_opy_ = None
bstack1ll1ll1l1l_opy_ = None
bstack111l111l1_opy_ = None
bstack1l1lllll1_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1llll1l11_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack11l1l1llll_opy_ = None
bstack1l1l1lll_opy_ = None
bstack1lll1111_opy_ = None
bstack11lll1ll11_opy_ = None
bstack11lll11111_opy_ = None
bstack1ll1lllll1_opy_ = None
bstack1l11l11l11_opy_ = None
thread_local = threading.local()
bstack1l111111_opy_ = False
bstack11l11l111_opy_ = bstack1l11l1l_opy_ (u"ࠦࠧ࣋")
logger = bstack11lllll1_opy_.get_logger(__name__, bstack11ll1l1lll_opy_)
bstack11l1l1l11l_opy_ = bstack11lllll1_opy_.bstack1l11llllll_opy_(__name__)
bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
percy = bstack1l1l11lll_opy_()
bstack1lllllll11_opy_ = bstack11l1llll11_opy_()
bstack11lll11l_opy_ = bstack11l1l111ll_opy_()
def bstack1lll1l11ll_opy_():
  global CONFIG
  global bstack1l11ll111_opy_
  global bstack11llllll_opy_
  testContextOptions = bstack1ll11l1l_opy_(CONFIG)
  if bstack111111lll_opy_(CONFIG):
    if (bstack1l11l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1l11l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1l11l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1l11ll111_opy_ = True
    bstack11llllll_opy_.bstack1ll111ll1l_opy_(testContextOptions.get(bstack1l11l1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1l11ll111_opy_ = True
    bstack11llllll_opy_.bstack1ll111ll1l_opy_(True)
def bstack1l1l1111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1l1ll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1ll11lll_opy_():
  global bstack11111l111_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1l11l1l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack1l11l1l_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack11111l111_opy_[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack11l11l1l1_opy_ = re.compile(bstack1l11l1l_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack1ll11l1ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11l11l1l1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l11l1l_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack1l11l1l_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack111ll1l1l_opy_():
  global bstack1l11l11l11_opy_
  if bstack1l11l11l11_opy_ is None:
        bstack1l11l11l11_opy_ = bstack1l1ll11lll_opy_()
  bstack11l1llll_opy_ = bstack1l11l11l11_opy_
  if bstack11l1llll_opy_ and os.path.exists(os.path.abspath(bstack11l1llll_opy_)):
    fileName = bstack11l1llll_opy_
  if bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack11ll_opy_ = os.path.abspath(fileName)
  else:
    bstack11ll_opy_ = bstack1l11l1l_opy_ (u"࠭ࠧࣛ")
  bstack11ll1l1ll_opy_ = os.getcwd()
  bstack11111ll1_opy_ = bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack11ll1l11ll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack11ll_opy_)) and bstack11ll1l1ll_opy_ != bstack1l11l1l_opy_ (u"ࠤࠥࣞ"):
    bstack11ll_opy_ = os.path.join(bstack11ll1l1ll_opy_, bstack11111ll1_opy_)
    if not os.path.exists(bstack11ll_opy_):
      bstack11ll_opy_ = os.path.join(bstack11ll1l1ll_opy_, bstack11ll1l11ll_opy_)
    if bstack11ll1l1ll_opy_ != os.path.dirname(bstack11ll1l1ll_opy_):
      bstack11ll1l1ll_opy_ = os.path.dirname(bstack11ll1l1ll_opy_)
    else:
      bstack11ll1l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠥࠦࣟ")
  bstack1l11l11l11_opy_ = bstack11ll_opy_ if os.path.exists(bstack11ll_opy_) else None
  return bstack1l11l11l11_opy_
def bstack11ll11l11_opy_(config):
    if bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack1lllll1l11_opy_():
  bstack11ll_opy_ = bstack111ll1l1l_opy_()
  if not os.path.exists(bstack11ll_opy_):
    bstack1lllll1lll_opy_(
      bstack1ll1l1llll_opy_.format(os.getcwd()))
  try:
    with open(bstack11ll_opy_, bstack1l11l1l_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack1l11l1l_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack11l11l1l1_opy_)
      yaml.add_constructor(bstack1l11l1l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack1ll11l1ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack11ll11l11_opy_(config)
      return config
  except:
    with open(bstack11ll_opy_, bstack1l11l1l_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack11ll11l11_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1lllll1lll_opy_(bstack1l1lll1l1l_opy_.format(str(exc)))
def bstack1ll1lll1l1_opy_(config):
  bstack111llllll_opy_ = bstack11ll1lllll_opy_(config)
  for option in list(bstack111llllll_opy_):
    if option.lower() in bstack111llll1l_opy_ and option != bstack111llll1l_opy_[option.lower()]:
      bstack111llllll_opy_[bstack111llll1l_opy_[option.lower()]] = bstack111llllll_opy_[option]
      del bstack111llllll_opy_[option]
  return config
def bstack11111ll11_opy_():
  global bstack11l1l1l1l_opy_
  for key, bstack1llll111l_opy_ in bstack11l1llll1_opy_.items():
    if isinstance(bstack1llll111l_opy_, list):
      for var in bstack1llll111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11l1l1l1l_opy_[key] = os.environ[var]
          break
    elif bstack1llll111l_opy_ in os.environ and os.environ[bstack1llll111l_opy_] and str(os.environ[bstack1llll111l_opy_]).strip():
      bstack11l1l1l1l_opy_[key] = os.environ[bstack1llll111l_opy_]
  if bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack11l1l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack11l1l1l1l_opy_[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack111lll111_opy_():
  global bstack1l1l111l1l_opy_
  global bstack1l11l1lll_opy_
  global bstack11111l111_opy_
  bstack11l11ll1l1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack1l1l111l1l_opy_[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack1l1l111l1l_opy_[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack11l11ll1l1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1lll11ll1l_opy_ in bstack1l1l1ll11_opy_.items():
    if isinstance(bstack1lll11ll1l_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1lll11ll1l_opy_:
          if bstack1l11l1l_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack1l1l111l1l_opy_:
            bstack1l1l111l1l_opy_[key] = sys.argv[idx + 1]
            bstack1l11l1lll_opy_ += bstack1l11l1l_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack1l11l1l_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack111llll1ll_opy_(bstack11111l111_opy_, key, sys.argv[idx + 1])
            bstack11l11ll1l1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1lll11ll1l_opy_.lower() == val.lower() and key not in bstack1l1l111l1l_opy_:
          bstack1l1l111l1l_opy_[key] = sys.argv[idx + 1]
          bstack1l11l1lll_opy_ += bstack1l11l1l_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1lll11ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack111llll1ll_opy_(bstack11111l111_opy_, key, sys.argv[idx + 1])
          bstack11l11ll1l1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack11l11ll1l1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack1ll11l11ll_opy_(config):
  bstack11ll1111l_opy_ = config.keys()
  for bstack1ll11111_opy_, bstack1l111l11_opy_ in bstack11l1111l11_opy_.items():
    if bstack1l111l11_opy_ in bstack11ll1111l_opy_:
      config[bstack1ll11111_opy_] = config[bstack1l111l11_opy_]
      del config[bstack1l111l11_opy_]
  for bstack1ll11111_opy_, bstack1l111l11_opy_ in bstack1llll1l1l1_opy_.items():
    if isinstance(bstack1l111l11_opy_, list):
      for bstack11ll11lll1_opy_ in bstack1l111l11_opy_:
        if bstack11ll11lll1_opy_ in bstack11ll1111l_opy_:
          config[bstack1ll11111_opy_] = config[bstack11ll11lll1_opy_]
          del config[bstack11ll11lll1_opy_]
          break
    elif bstack1l111l11_opy_ in bstack11ll1111l_opy_:
      config[bstack1ll11111_opy_] = config[bstack1l111l11_opy_]
      del config[bstack1l111l11_opy_]
  for bstack11ll11lll1_opy_ in list(config):
    for bstack1l1l1l1l1_opy_ in bstack11l111llll_opy_:
      if bstack11ll11lll1_opy_.lower() == bstack1l1l1l1l1_opy_.lower() and bstack11ll11lll1_opy_ != bstack1l1l1l1l1_opy_:
        config[bstack1l1l1l1l1_opy_] = config[bstack11ll11lll1_opy_]
        del config[bstack11ll11lll1_opy_]
  bstack11l11111_opy_ = [{}]
  if not config.get(bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack11l11111_opy_ = config[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack11l11111_opy_:
    for bstack11ll11lll1_opy_ in list(platform):
      for bstack1l1l1l1l1_opy_ in bstack11l111llll_opy_:
        if bstack11ll11lll1_opy_.lower() == bstack1l1l1l1l1_opy_.lower() and bstack11ll11lll1_opy_ != bstack1l1l1l1l1_opy_:
          platform[bstack1l1l1l1l1_opy_] = platform[bstack11ll11lll1_opy_]
          del platform[bstack11ll11lll1_opy_]
  for bstack1ll11111_opy_, bstack1l111l11_opy_ in bstack1llll1l1l1_opy_.items():
    for platform in bstack11l11111_opy_:
      if isinstance(bstack1l111l11_opy_, list):
        for bstack11ll11lll1_opy_ in bstack1l111l11_opy_:
          if bstack11ll11lll1_opy_ in platform:
            platform[bstack1ll11111_opy_] = platform[bstack11ll11lll1_opy_]
            del platform[bstack11ll11lll1_opy_]
            break
      elif bstack1l111l11_opy_ in platform:
        platform[bstack1ll11111_opy_] = platform[bstack1l111l11_opy_]
        del platform[bstack1l111l11_opy_]
  for bstack1111l111_opy_ in bstack1llllllll1_opy_:
    if bstack1111l111_opy_ in config:
      if not bstack1llllllll1_opy_[bstack1111l111_opy_] in config:
        config[bstack1llllllll1_opy_[bstack1111l111_opy_]] = {}
      config[bstack1llllllll1_opy_[bstack1111l111_opy_]].update(config[bstack1111l111_opy_])
      del config[bstack1111l111_opy_]
  for platform in bstack11l11111_opy_:
    for bstack1111l111_opy_ in bstack1llllllll1_opy_:
      if bstack1111l111_opy_ in list(platform):
        if not bstack1llllllll1_opy_[bstack1111l111_opy_] in platform:
          platform[bstack1llllllll1_opy_[bstack1111l111_opy_]] = {}
        platform[bstack1llllllll1_opy_[bstack1111l111_opy_]].update(platform[bstack1111l111_opy_])
        del platform[bstack1111l111_opy_]
  config = bstack1ll1lll1l1_opy_(config)
  return config
def bstack1l1111l1_opy_(config):
  global bstack1llllll11_opy_
  bstack11111ll1l_opy_ = False
  if bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack1l11l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack1l11l1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack11ll1l11_opy_ = bstack1llll1l1ll_opy_()
      if bstack1l11l1l_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack11ll1l11_opy_:
        if not bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack1l11l1l_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack11111ll1l_opy_ = True
        bstack1llllll11_opy_ = config[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack1l11l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack111111lll_opy_(config) and bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack11111ll1l_opy_:
    if not bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack1l11l1l_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      bstack11ll11ll1l_opy_ = datetime.datetime.now()
      bstack11llll111l_opy_ = bstack11ll11ll1l_opy_.strftime(bstack1l11l1l_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack1l1llll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l11l1l_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack11llll111l_opy_, hostname, bstack1l1llll1l1_opy_)
      config[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack1l11l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack1llllll11_opy_ = config[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack11l1ll11l1_opy_():
  bstack1ll111ll11_opy_ =  bstack11l1111l1_opy_()[bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack1ll111ll11_opy_ if bstack1ll111ll11_opy_ else -1
def bstack11l1lll1l1_opy_(bstack1ll111ll11_opy_):
  global CONFIG
  if not bstack1l11l1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack1l11l1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack1ll111ll11_opy_)
  )
def bstack11ll1l1ll1_opy_():
  global CONFIG
  if not bstack1l11l1l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  bstack11ll11ll1l_opy_ = datetime.datetime.now()
  bstack11llll111l_opy_ = bstack11ll11ll1l_opy_.strftime(bstack1l11l1l_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack1l11l1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack11llll111l_opy_
  )
def bstack1ll1ll1ll1_opy_():
  global CONFIG
  if bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack1l11l1l_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack1l11l1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack11ll1l1ll1_opy_()
    os.environ[bstack1l11l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack1l11l1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack1ll111ll11_opy_ = bstack1l11l1l_opy_ (u"ࠪࠫळ")
  bstack1ll11l1lll_opy_ = bstack11l1ll11l1_opy_()
  if bstack1ll11l1lll_opy_ != -1:
    bstack1ll111ll11_opy_ = bstack1l11l1l_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack1ll11l1lll_opy_)
  if bstack1ll111ll11_opy_ == bstack1l11l1l_opy_ (u"ࠬ࠭व"):
    bstack1l1l111l11_opy_ = bstack1llll1111l_opy_(CONFIG[bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack1l1l111l11_opy_ != -1:
      bstack1ll111ll11_opy_ = str(bstack1l1l111l11_opy_)
  if bstack1ll111ll11_opy_:
    bstack11l1lll1l1_opy_(bstack1ll111ll11_opy_)
    os.environ[bstack1l11l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack1l1l1lll11_opy_(bstack11llll11ll_opy_, bstack111lll11l1_opy_, path):
  bstack11lll11l11_opy_ = {
    bstack1l11l1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack111lll11l1_opy_
  }
  if os.path.exists(path):
    bstack1lll1lll_opy_ = json.load(open(path, bstack1l11l1l_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack1lll1lll_opy_ = {}
  bstack1lll1lll_opy_[bstack11llll11ll_opy_] = bstack11lll11l11_opy_
  with open(path, bstack1l11l1l_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack1lll1lll_opy_, outfile)
def bstack1llll1111l_opy_(bstack11llll11ll_opy_):
  bstack11llll11ll_opy_ = str(bstack11llll11ll_opy_)
  bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠬࢄ़ࠧ")), bstack1l11l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack1ll1lll1_opy_):
      os.makedirs(bstack1ll1lll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠧࡿࠩा")), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack1l11l1l_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l11l1l_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack1l11l1l_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l11l1l_opy_ (u"ࠬࡸࠧृ")) as bstack11l1lll11l_opy_:
      bstack11l11lll1l_opy_ = json.load(bstack11l1lll11l_opy_)
    if bstack11llll11ll_opy_ in bstack11l11lll1l_opy_:
      bstack11lll1111_opy_ = bstack11l11lll1l_opy_[bstack11llll11ll_opy_][bstack1l11l1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack1l1111l1ll_opy_ = int(bstack11lll1111_opy_) + 1
      bstack1l1l1lll11_opy_(bstack11llll11ll_opy_, bstack1l1111l1ll_opy_, file_path)
      return bstack1l1111l1ll_opy_
    else:
      bstack1l1l1lll11_opy_(bstack11llll11ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1111l1111_opy_.format(str(e)))
    return -1
def bstack1l1l1l111l_opy_(config):
  if not config[bstack1l11l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1l11111l_opy_(config, index=0):
  global bstack1l11l1l111_opy_
  bstack11ll111ll_opy_ = {}
  caps = bstack11l1ll1lll_opy_ + bstack1l1l11l11_opy_
  if config.get(bstack1l11l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack1l11l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack1l11l1l111_opy_:
    caps += bstack1111lllll_opy_
  for key in config:
    if key in caps + [bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack11ll111ll_opy_[key] = config[key]
  if bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack11lll111l_opy_ in config[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack11lll111l_opy_ in caps:
        continue
      bstack11ll111ll_opy_[bstack11lll111l_opy_] = config[bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack11lll111l_opy_]
  bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack1l11l1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack11ll111ll_opy_:
    del (bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack11ll111ll_opy_
def bstack1l1ll1l11_opy_(config):
  global bstack1l11l1l111_opy_
  bstack1llll1llll_opy_ = {}
  caps = bstack1l1l11l11_opy_
  if bstack1l11l1l111_opy_:
    caps += bstack1111lllll_opy_
  for key in caps:
    if key in config:
      bstack1llll1llll_opy_[key] = config[key]
  return bstack1llll1llll_opy_
def bstack11ll1111l1_opy_(bstack11ll111ll_opy_, bstack1llll1llll_opy_):
  bstack111l1l1l_opy_ = {}
  for key in bstack11ll111ll_opy_.keys():
    if key in bstack11l1111l11_opy_:
      bstack111l1l1l_opy_[bstack11l1111l11_opy_[key]] = bstack11ll111ll_opy_[key]
    else:
      bstack111l1l1l_opy_[key] = bstack11ll111ll_opy_[key]
  for key in bstack1llll1llll_opy_:
    if key in bstack11l1111l11_opy_:
      bstack111l1l1l_opy_[bstack11l1111l11_opy_[key]] = bstack1llll1llll_opy_[key]
    else:
      bstack111l1l1l_opy_[key] = bstack1llll1llll_opy_[key]
  return bstack111l1l1l_opy_
def bstack1l1l11ll1l_opy_(config, index=0):
  global bstack1l11l1l111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11lll1l1ll_opy_ = bstack1ll1ll11l1_opy_(bstack1l11l1ll1l_opy_, config, logger)
  bstack1llll1llll_opy_ = bstack1l1ll1l11_opy_(config)
  bstack1ll11l1ll1_opy_ = bstack1l1l11l11_opy_
  bstack1ll11l1ll1_opy_ += bstack1l1l1ll111_opy_
  bstack1llll1llll_opy_ = update(bstack1llll1llll_opy_, bstack11lll1l1ll_opy_)
  if bstack1l11l1l111_opy_:
    bstack1ll11l1ll1_opy_ += bstack1111lllll_opy_
  if bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack1l11lllll_opy_ = bstack1ll1ll11l1_opy_(bstack1l11l1ll1l_opy_, config[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack1ll11l1ll1_opy_ += list(bstack1l11lllll_opy_.keys())
    for bstack1llllllll_opy_ in bstack1ll11l1ll1_opy_:
      if bstack1llllllll_opy_ in config[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack1llllllll_opy_ == bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack1l11lllll_opy_[bstack1llllllll_opy_] = str(config[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack1llllllll_opy_] * 1.0)
          except:
            bstack1l11lllll_opy_[bstack1llllllll_opy_] = str(config[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack1llllllll_opy_])
        else:
          bstack1l11lllll_opy_[bstack1llllllll_opy_] = config[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1llllllll_opy_]
        del (config[bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1llllllll_opy_])
    bstack1llll1llll_opy_ = update(bstack1llll1llll_opy_, bstack1l11lllll_opy_)
  bstack11ll111ll_opy_ = bstack1l11111l_opy_(config, index)
  for bstack11ll11lll1_opy_ in bstack1l1l11l11_opy_ + list(bstack11lll1l1ll_opy_.keys()):
    if bstack11ll11lll1_opy_ in bstack11ll111ll_opy_:
      bstack1llll1llll_opy_[bstack11ll11lll1_opy_] = bstack11ll111ll_opy_[bstack11ll11lll1_opy_]
      del (bstack11ll111ll_opy_[bstack11ll11lll1_opy_])
  if bstack1lllll111l_opy_(config):
    bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack1llll1llll_opy_)
    caps[bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack11ll111ll_opy_
  else:
    bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack11ll1111l1_opy_(bstack11ll111ll_opy_, bstack1llll1llll_opy_))
    if bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1ll1111l1_opy_():
  global bstack1l1llll111_opy_
  global CONFIG
  if bstack1ll1l1ll11_opy_() <= version.parse(bstack1l11l1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ९")):
    if bstack1l1llll111_opy_ != bstack1l11l1l_opy_ (u"ࠨࠩ॰"):
      return bstack1l11l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1l1llll111_opy_ + bstack1l11l1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢॲ")
    return bstack1ll1l1l1l1_opy_
  if bstack1l1llll111_opy_ != bstack1l11l1l_opy_ (u"ࠫࠬॳ"):
    return bstack1l11l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢॴ") + bstack1l1llll111_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢॵ")
  return bstack1lll111lll_opy_
def bstack1lll11l1l1_opy_(options):
  return hasattr(options, bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨॶ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l111l11l_opy_(options, bstack1llllll11l_opy_):
  for bstack11l11l11l1_opy_ in bstack1llllll11l_opy_:
    if bstack11l11l11l1_opy_ in [bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ"), bstack1l11l1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॸ")]:
      continue
    if bstack11l11l11l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11l11l11l1_opy_] = update(options._experimental_options[bstack11l11l11l1_opy_],
                                                         bstack1llllll11l_opy_[bstack11l11l11l1_opy_])
    else:
      options.add_experimental_option(bstack11l11l11l1_opy_, bstack1llllll11l_opy_[bstack11l11l11l1_opy_])
  if bstack1l11l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1llllll11l_opy_:
    for arg in bstack1llllll11l_opy_[bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
    del (bstack1llllll11l_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")])
  if bstack1l11l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॼ") in bstack1llllll11l_opy_:
    for ext in bstack1llllll11l_opy_[bstack1l11l1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1llllll11l_opy_[bstack1l11l1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬॾ")])
def bstack1l11111l11_opy_(options, bstack11l1ll1ll_opy_):
  if bstack1l11l1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॿ") in bstack11l1ll1ll_opy_:
    for bstack1l11l11lll_opy_ in bstack11l1ll1ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩঀ")]:
      if bstack1l11l11lll_opy_ in options._preferences:
        options._preferences[bstack1l11l11lll_opy_] = update(options._preferences[bstack1l11l11lll_opy_], bstack11l1ll1ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঁ")][bstack1l11l11lll_opy_])
      else:
        options.set_preference(bstack1l11l11lll_opy_, bstack11l1ll1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫং")][bstack1l11l11lll_opy_])
  if bstack1l11l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫঃ") in bstack11l1ll1ll_opy_:
    for arg in bstack11l1ll1ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      options.add_argument(arg)
def bstack1l1ll1l11l_opy_(options, bstack1ll1l111l1_opy_):
  if bstack1l11l1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঅ") in bstack1ll1l111l1_opy_:
    options.use_webview(bool(bstack1ll1l111l1_opy_[bstack1l11l1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪআ")]))
  bstack11l111l11l_opy_(options, bstack1ll1l111l1_opy_)
def bstack1ll1l1111_opy_(options, bstack1llll111ll_opy_):
  for bstack1ll1llllll_opy_ in bstack1llll111ll_opy_:
    if bstack1ll1llllll_opy_ in [bstack1l11l1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧই"), bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ")]:
      continue
    options.set_capability(bstack1ll1llllll_opy_, bstack1llll111ll_opy_[bstack1ll1llllll_opy_])
  if bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack1llll111ll_opy_:
    for arg in bstack1llll111ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
  if bstack1l11l1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫঋ") in bstack1llll111ll_opy_:
    options.bstack1lll11l1_opy_(bool(bstack1llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬঌ")]))
def bstack1111l11l1_opy_(options, bstack1l1lllll11_opy_):
  for bstack1l11ll11l_opy_ in bstack1l1lllll11_opy_:
    if bstack1l11ll11l_opy_ in [bstack1l11l1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍"), bstack1l11l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ঎")]:
      continue
    options._options[bstack1l11ll11l_opy_] = bstack1l1lllll11_opy_[bstack1l11ll11l_opy_]
  if bstack1l11l1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨএ") in bstack1l1lllll11_opy_:
    for bstack1ll1l11ll_opy_ in bstack1l1lllll11_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঐ")]:
      options.bstack1ll1l11l11_opy_(
        bstack1ll1l11ll_opy_, bstack1l1lllll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ঑")][bstack1ll1l11ll_opy_])
  if bstack1l11l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒") in bstack1l1lllll11_opy_:
    for arg in bstack1l1lllll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও")]:
      options.add_argument(arg)
def bstack11l1l11ll_opy_(options, caps):
  if not hasattr(options, bstack1l11l1l_opy_ (u"ࠩࡎࡉ࡞࠭ঔ")):
    return
  if options.KEY == bstack1l11l1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨক"):
    options = bstack1ll1l11lll_opy_.bstack11lll11l1_opy_(bstack1ll1l1lll1_opy_=options, config=CONFIG)
  if options.KEY == bstack1l11l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩখ") and options.KEY in caps:
    bstack11l111l11l_opy_(options, caps[bstack1l11l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪগ")])
  elif options.KEY == bstack1l11l1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঘ") and options.KEY in caps:
    bstack1l11111l11_opy_(options, caps[bstack1l11l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঙ")])
  elif options.KEY == bstack1l11l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩচ") and options.KEY in caps:
    bstack1ll1l1111_opy_(options, caps[bstack1l11l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪছ")])
  elif options.KEY == bstack1l11l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫজ") and options.KEY in caps:
    bstack1l1ll1l11l_opy_(options, caps[bstack1l11l1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬঝ")])
  elif options.KEY == bstack1l11l1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঞ") and options.KEY in caps:
    bstack1111l11l1_opy_(options, caps[bstack1l11l1l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬট")])
def bstack11ll11111_opy_(caps):
  global bstack1l11l1l111_opy_
  if isinstance(os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨঠ")), str):
    bstack1l11l1l111_opy_ = eval(os.getenv(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩড")))
  if bstack1l11l1l111_opy_:
    if bstack1l1l1111ll_opy_() < version.parse(bstack1l11l1l_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঢ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l11l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩত") in caps:
      browser = caps[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪথ")]
    elif bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧদ") in caps:
      browser = caps[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨধ")]
    browser = str(browser).lower()
    if browser == bstack1l11l1l_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨন") or browser == bstack1l11l1l_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ঩"):
      browser = bstack1l11l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪপ")
    if browser == bstack1l11l1l_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬফ"):
      browser = bstack1l11l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬব")
    if browser not in [bstack1l11l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ভ"), bstack1l11l1l_opy_ (u"ࠧࡦࡦࡪࡩࠬম"), bstack1l11l1l_opy_ (u"ࠨ࡫ࡨࠫয"), bstack1l11l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩর"), bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ঱")]:
      return None
    try:
      package = bstack1l11l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ল").format(browser)
      name = bstack1l11l1l_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঳")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll11l1l1_opy_(options):
        return None
      for bstack11ll11lll1_opy_ in caps.keys():
        options.set_capability(bstack11ll11lll1_opy_, caps[bstack11ll11lll1_opy_])
      bstack11l1l11ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1ll1111_opy_(options, bstack1lll11111_opy_):
  if not bstack1lll11l1l1_opy_(options):
    return
  for bstack11ll11lll1_opy_ in bstack1lll11111_opy_.keys():
    if bstack11ll11lll1_opy_ in bstack1l1l1ll111_opy_:
      continue
    if bstack11ll11lll1_opy_ in options._caps and type(options._caps[bstack11ll11lll1_opy_]) in [dict, list]:
      options._caps[bstack11ll11lll1_opy_] = update(options._caps[bstack11ll11lll1_opy_], bstack1lll11111_opy_[bstack11ll11lll1_opy_])
    else:
      options.set_capability(bstack11ll11lll1_opy_, bstack1lll11111_opy_[bstack11ll11lll1_opy_])
  bstack11l1l11ll_opy_(options, bstack1lll11111_opy_)
  if bstack1l11l1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঴") in options._caps:
    if options._caps[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ঵")] and options._caps[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭শ")].lower() != bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪষ"):
      del options._caps[bstack1l11l1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩস")]
def bstack11ll11l11l_opy_(proxy_config):
  if bstack1l11l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨহ") in proxy_config:
    proxy_config[bstack1l11l1l_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ঺")] = proxy_config[bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ঻")]
    del (proxy_config[bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ়ࠫ")])
  if bstack1l11l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫঽ") in proxy_config and proxy_config[bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬা")].lower() != bstack1l11l1l_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪি"):
    proxy_config[bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧী")] = bstack1l11l1l_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬু")
  if bstack1l11l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫূ") in proxy_config:
    proxy_config[bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪৃ")] = bstack1l11l1l_opy_ (u"ࠨࡲࡤࡧࠬৄ")
  return proxy_config
def bstack11l11lllll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ৅") in config:
    return proxy
  config[bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ৆")] = bstack11ll11l11l_opy_(config[bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪে")])
  if proxy == None:
    proxy = Proxy(config[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫৈ")])
  return proxy
def bstack11l111l1l1_opy_(self):
  global CONFIG
  global bstack1l1lllll1_opy_
  try:
    proxy = bstack111111l1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l11l1l_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")):
        proxies = bstack111l11l11_opy_(proxy, bstack1ll1111l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1ll111l_opy_ = proxies.popitem()
          if bstack1l11l1l_opy_ (u"ࠢ࠻࠱࠲ࠦ৊") in bstack1ll1ll111l_opy_:
            return bstack1ll1ll111l_opy_
          else:
            return bstack1l11l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤো") + bstack1ll1ll111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨৌ").format(str(e)))
  return bstack1l1lllll1_opy_(self)
def bstack111ll1lll_opy_():
  global CONFIG
  return bstack11l1111ll1_opy_(CONFIG) and bstack111l111l_opy_() and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11lll1ll_opy_)
def bstack1ll1l1l1l_opy_():
  global CONFIG
  return (bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ্࠭") in CONFIG or bstack1l11l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨৎ") in CONFIG) and bstack11ll1lll1_opy_()
def bstack11ll1lllll_opy_(config):
  bstack111llllll_opy_ = {}
  if bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৏") in config:
    bstack111llllll_opy_ = config[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৐")]
  if bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৑") in config:
    bstack111llllll_opy_ = config[bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৒")]
  proxy = bstack111111l1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l11l1l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৓")) and os.path.isfile(proxy):
      bstack111llllll_opy_[bstack1l11l1l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৔")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l11l1l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ৕")):
        proxies = bstack1l1111lll1_opy_(config, bstack1ll1111l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1ll111l_opy_ = proxies.popitem()
          if bstack1l11l1l_opy_ (u"ࠧࡀ࠯࠰ࠤ৖") in bstack1ll1ll111l_opy_:
            parsed_url = urlparse(bstack1ll1ll111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l11l1l_opy_ (u"ࠨ࠺࠰࠱ࠥৗ") + bstack1ll1ll111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111llllll_opy_[bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৘")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111llllll_opy_[bstack1l11l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ৙")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111llllll_opy_[bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ৚")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111llllll_opy_[bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭৛")] = str(parsed_url.password)
  return bstack111llllll_opy_
def bstack1ll11l1l_opy_(config):
  if bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩড়") in config:
    return config[bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪঢ়")]
  return {}
def bstack1l1111ll11_opy_(caps):
  global bstack1llllll11_opy_
  if bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৞") in caps:
    caps[bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨয়")][bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧৠ")] = True
    if bstack1llllll11_opy_:
      caps[bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪৡ")][bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬৢ")] = bstack1llllll11_opy_
  else:
    caps[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩৣ")] = True
    if bstack1llllll11_opy_:
      caps[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৤")] = bstack1llllll11_opy_
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack111ll1111_opy_():
  global CONFIG
  if not bstack111111lll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৥") in CONFIG and bstack11lll1l1l_opy_(CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ০")]):
    if (
      bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ১") in CONFIG
      and bstack11lll1l1l_opy_(CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭২")].get(bstack1l11l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৩")))
    ):
      logger.debug(bstack1l11l1l_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧ৪"))
      return
    bstack111llllll_opy_ = bstack11ll1lllll_opy_(CONFIG)
    bstack1lll1ll11_opy_(CONFIG[bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৫")], bstack111llllll_opy_)
def bstack1lll1ll11_opy_(key, bstack111llllll_opy_):
  global bstack1l1ll1l1l_opy_
  logger.info(bstack1111ll11l_opy_)
  try:
    bstack1l1ll1l1l_opy_ = Local()
    bstack1lll11l11l_opy_ = {bstack1l11l1l_opy_ (u"࠭࡫ࡦࡻࠪ৬"): key}
    bstack1lll11l11l_opy_.update(bstack111llllll_opy_)
    logger.debug(bstack1lll1lll1_opy_.format(str(bstack1lll11l11l_opy_)).replace(key, bstack1l11l1l_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৭")))
    bstack1l1ll1l1l_opy_.start(**bstack1lll11l11l_opy_)
    if bstack1l1ll1l1l_opy_.isRunning():
      logger.info(bstack11ll111l1l_opy_)
  except Exception as e:
    bstack1lllll1lll_opy_(bstack11l1l1lll_opy_.format(str(e)))
def bstack1l1lll11l_opy_():
  global bstack1l1ll1l1l_opy_
  if bstack1l1ll1l1l_opy_.isRunning():
    logger.info(bstack1l1ll111l_opy_)
    bstack1l1ll1l1l_opy_.stop()
  bstack1l1ll1l1l_opy_ = None
def bstack1l11111lll_opy_(bstack1llll11l1l_opy_=[]):
  global CONFIG
  bstack1111l1lll_opy_ = []
  bstack1l111l1l_opy_ = [bstack1l11l1l_opy_ (u"ࠨࡱࡶࠫ৮"), bstack1l11l1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৯"), bstack1l11l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧৰ"), bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ৱ"), bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৲"), bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৳")]
  try:
    for err in bstack1llll11l1l_opy_:
      bstack1l111l1ll_opy_ = {}
      for k in bstack1l111l1l_opy_:
        val = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৴")][int(err[bstack1l11l1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ৵")])].get(k)
        if val:
          bstack1l111l1ll_opy_[k] = val
      if(err[bstack1l11l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৶")] != bstack1l11l1l_opy_ (u"ࠪࠫ৷")):
        bstack1l111l1ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৸")] = {
          err[bstack1l11l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ৹")]: err[bstack1l11l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৺")]
        }
        bstack1111l1lll_opy_.append(bstack1l111l1ll_opy_)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩ৻") + str(e))
  finally:
    return bstack1111l1lll_opy_
def bstack11llll1l1l_opy_(file_name):
  bstack111lll11_opy_ = []
  try:
    bstack1l1lll1l11_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1lll1l11_opy_):
      with open(bstack1l1lll1l11_opy_) as f:
        bstack1l1111ll1_opy_ = json.load(f)
        bstack111lll11_opy_ = bstack1l1111ll1_opy_
      os.remove(bstack1l1lll1l11_opy_)
    return bstack111lll11_opy_
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪৼ") + str(e))
    return bstack111lll11_opy_
def bstack1llllll1ll_opy_():
  try:
      from bstack_utils.constants import bstack11lllllll1_opy_, EVENTS
      from bstack_utils.helper import bstack11l111ll11_opy_, get_host_info, bstack11llllll_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack11l1ll1l_opy_ = os.path.join(os.getcwd(), bstack1l11l1l_opy_ (u"ࠩ࡯ࡳ࡬࠭৽"), bstack1l11l1l_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭৾"))
      lock = FileLock(bstack11l1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ৿"))
      def bstack11llll1l11_opy_():
          try:
              with lock:
                  with open(bstack11l1ll1l_opy_, bstack1l11l1l_opy_ (u"ࠧࡸࠢ਀"), encoding=bstack1l11l1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਁ")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l11l1l_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣਂ"): {
                              bstack1l11l1l_opy_ (u"ࠣࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠢਃ"): bstack1l11l1l_opy_ (u"ࠤࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠧ਄"),
                          }
                      }
                      bstack1lllll1111_opy_ = datetime.utcnow()
                      bstack11ll11ll1l_opy_ = bstack1lllll1111_opy_.strftime(bstack1l11l1l_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨ࡙࡙ࠣࡉࠢਅ"))
                      bstack11ll11lll_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩਆ")) if os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪਇ")) else bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                      payload = {
                          bstack1l11l1l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠦਉ"): bstack1l11l1l_opy_ (u"ࠣࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧਊ"),
                          bstack1l11l1l_opy_ (u"ࠤࡧࡥࡹࡧࠢ਋"): {
                              bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠤ਌"): bstack11ll11lll_opy_,
                              bstack1l11l1l_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࡤࡪࡡࡺࠤ਍"): bstack11ll11ll1l_opy_,
                              bstack1l11l1l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࠤ਎"): bstack1l11l1l_opy_ (u"ࠨࡓࡅࡍࡉࡩࡦࡺࡵࡳࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࠢਏ"),
                              bstack1l11l1l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡪࡴࡱࡱࠦਐ"): {
                                  bstack1l11l1l_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࡵࠥ਑"): data,
                                  bstack1l11l1l_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ਒"): bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਓ"))
                              },
                              bstack1l11l1l_opy_ (u"ࠦࡺࡹࡥࡳࡡࡧࡥࡹࡧࠢਔ"): bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠧࡻࡳࡦࡴࡑࡥࡲ࡫ࠢਕ")),
                              bstack1l11l1l_opy_ (u"ࠨࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠤਖ"): get_host_info()
                          }
                      }
                      bstack11l11ll111_opy_ = bstack11l11l1l1l_opy_(cli.config, [bstack1l11l1l_opy_ (u"ࠢࡢࡲ࡬ࡷࠧਗ"), bstack1l11l1l_opy_ (u"ࠣࡧࡧࡷࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡢࡶ࡬ࡳࡳࠨਘ"), bstack1l11l1l_opy_ (u"ࠤࡤࡴ࡮ࠨਙ")], bstack11lllllll1_opy_)
                      response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠥࡔࡔ࡙ࡔࠣਚ"), bstack11l11ll111_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l11l1l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦਛ").format(bstack11lllllll1_opy_, payload))
                      else:
                          logger.debug(bstack1l11l1l_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧਜ").format(bstack11lllllll1_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l11l1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਝ").format(e))
      bstack11llll1l11_opy_()
      bstack1lll1l1ll1_opy_(bstack11l1ll1l_opy_, logger)
  except:
    pass
def bstack1lllll111_opy_():
  global bstack11l11l111_opy_
  global bstack1ll1l11111_opy_
  global bstack1ll1llll11_opy_
  global bstack1l1ll1lll_opy_
  global bstack111lll1111_opy_
  global bstack1111llll1_opy_
  global CONFIG
  bstack1l1111lll_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਞ"))
  if bstack1l1111lll_opy_ in [bstack1l11l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧਟ"), bstack1l11l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨਠ")]:
    bstack11ll111l1_opy_()
  percy.shutdown()
  if bstack11l11l111_opy_:
    logger.warning(bstack11l1l111l_opy_.format(str(bstack11l11l111_opy_)))
  else:
    try:
      bstack1lll1lll_opy_ = bstack11lll1l11_opy_(bstack1l11l1l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਡ"), logger)
      if bstack1lll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਢ")) and bstack1lll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਣ")).get(bstack1l11l1l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਤ")):
        logger.warning(bstack11l1l111l_opy_.format(str(bstack1lll1lll_opy_[bstack1l11l1l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਥ")][bstack1l11l1l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਦ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.bstack1111l1l1l_opy_)
  logger.info(bstack111lllllll_opy_)
  global bstack1l1ll1l1l_opy_
  if bstack1l1ll1l1l_opy_:
    bstack1l1lll11l_opy_()
  try:
    with bstack1ll1l111_opy_:
      bstack11lll111l1_opy_ = bstack1ll1l11111_opy_.copy()
    for driver in bstack11lll111l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l1l1111_opy_)
  if bstack1111llll1_opy_ == bstack1l11l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਧ"):
    bstack111lll1111_opy_ = bstack11llll1l1l_opy_(bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਨ"))
  if bstack1111llll1_opy_ == bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ਩") and len(bstack1l1ll1lll_opy_) == 0:
    bstack1l1ll1lll_opy_ = bstack11llll1l1l_opy_(bstack1l11l1l_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਪ"))
    if len(bstack1l1ll1lll_opy_) == 0:
      bstack1l1ll1lll_opy_ = bstack11llll1l1l_opy_(bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਫ"))
  bstack1l111ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨਬ")
  if len(bstack1ll1llll11_opy_) > 0:
    bstack1l111ll1l1_opy_ = bstack1l11111lll_opy_(bstack1ll1llll11_opy_)
  elif len(bstack1l1ll1lll_opy_) > 0:
    bstack1l111ll1l1_opy_ = bstack1l11111lll_opy_(bstack1l1ll1lll_opy_)
  elif len(bstack111lll1111_opy_) > 0:
    bstack1l111ll1l1_opy_ = bstack1l11111lll_opy_(bstack111lll1111_opy_)
  elif len(bstack111l111ll_opy_) > 0:
    bstack1l111ll1l1_opy_ = bstack1l11111lll_opy_(bstack111l111ll_opy_)
  if bool(bstack1l111ll1l1_opy_):
    bstack111lll1lll_opy_(bstack1l111ll1l1_opy_)
  else:
    bstack111lll1lll_opy_()
  bstack1lll1l1ll1_opy_(bstack1l1l1lll1_opy_, logger)
  if bstack1l1111lll_opy_ not in [bstack1l11l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਭ")]:
    bstack1llllll1ll_opy_()
  bstack11lllll1_opy_.bstack1l1111l11_opy_(CONFIG)
  if len(bstack111lll1111_opy_) > 0:
    sys.exit(len(bstack111lll1111_opy_))
def bstack11l1lll11_opy_(bstack1ll11llll_opy_, frame):
  global bstack11llllll_opy_
  logger.error(bstack111l11111_opy_)
  bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਮ"), bstack1ll11llll_opy_)
  if hasattr(signal, bstack1l11l1l_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਯ")):
    bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਰ"), signal.Signals(bstack1ll11llll_opy_).name)
  else:
    bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਱"), bstack1l11l1l_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਲ"))
  if cli.is_running():
    bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.bstack1111l1l1l_opy_)
  bstack1l1111lll_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਲ਼"))
  if bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and not cli.is_enabled(CONFIG):
    bstack111ll1lll1_opy_.stop(bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਵ")))
  bstack1lllll111_opy_()
  sys.exit(1)
def bstack1lllll1lll_opy_(err):
  logger.critical(bstack11l1lll1_opy_.format(str(err)))
  bstack111lll1lll_opy_(bstack11l1lll1_opy_.format(str(err)), True)
  atexit.unregister(bstack1lllll111_opy_)
  bstack11ll111l1_opy_()
  sys.exit(1)
def bstack1lll111l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111lll1lll_opy_(message, True)
  atexit.unregister(bstack1lllll111_opy_)
  bstack11ll111l1_opy_()
  sys.exit(1)
def bstack1l1llll11_opy_():
  global CONFIG
  global bstack1l1l111l1l_opy_
  global bstack11l1l1l1l_opy_
  global bstack11llllll1_opy_
  CONFIG = bstack1lllll1l11_opy_()
  load_dotenv(CONFIG.get(bstack1l11l1l_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਸ਼")))
  bstack11111ll11_opy_()
  bstack111lll111_opy_()
  CONFIG = bstack1ll11l11ll_opy_(CONFIG)
  update(CONFIG, bstack11l1l1l1l_opy_)
  update(CONFIG, bstack1l1l111l1l_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1l1111l1_opy_(CONFIG)
  bstack11llllll1_opy_ = bstack111111lll_opy_(CONFIG)
  os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਷")] = bstack11llllll1_opy_.__str__().lower()
  bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਸ"), bstack11llllll1_opy_)
  if (bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") in CONFIG and bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ਺") in bstack1l1l111l1l_opy_) or (
          bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") in CONFIG and bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ਼ࠬ") not in bstack11l1l1l1l_opy_):
    if os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ਽")):
      CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਾ")] = os.getenv(bstack1l11l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩਿ"))
    else:
      if not CONFIG.get(bstack1l11l1l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤੀ"), bstack1l11l1l_opy_ (u"ࠢࠣੁ")) in bstack1l11l1l1l1_opy_:
        bstack1ll1ll1ll1_opy_()
  elif (bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫੂ") not in CONFIG and bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੃") in CONFIG) or (
          bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੄") in bstack11l1l1l1l_opy_ and bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੅") not in bstack1l1l111l1l_opy_):
    del (CONFIG[bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੆")])
  if bstack1l1l1l111l_opy_(CONFIG):
    bstack1lllll1lll_opy_(bstack1l111l11ll_opy_)
  Config.bstack1llll1111_opy_().bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣੇ"), CONFIG[bstack1l11l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩੈ")])
  bstack1ll11111ll_opy_()
  bstack1lll1ll1ll_opy_()
  if bstack1l11l1l111_opy_ and not CONFIG.get(bstack1l11l1l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੉"), bstack1l11l1l_opy_ (u"ࠤࠥ੊")) in bstack1l11l1l1l1_opy_:
    CONFIG[bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶࠧੋ")] = bstack1lllll11l1_opy_(CONFIG)
    logger.info(bstack1lll1l1111_opy_.format(CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࠨੌ")]))
  if not bstack11llllll1_opy_:
    CONFIG[bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੍")] = [{}]
def bstack11lll1l111_opy_(config, bstack1l1ll1l111_opy_):
  global CONFIG
  global bstack1l11l1l111_opy_
  CONFIG = config
  bstack1l11l1l111_opy_ = bstack1l1ll1l111_opy_
def bstack1lll1ll1ll_opy_():
  global CONFIG
  global bstack1l11l1l111_opy_
  if bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࠪ੎") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1l11l11l1_opy_)
    bstack1l11l1l111_opy_ = True
    bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭੏"), True)
def bstack1lllll11l1_opy_(config):
  bstack1lll1l1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩ੐")
  app = config[bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࠭ੑ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l1ll1l1_opy_:
      if os.path.exists(app):
        bstack1lll1l1l_opy_ = bstack111l1l11l_opy_(config, app)
      elif bstack111l1ll1_opy_(app):
        bstack1lll1l1l_opy_ = app
      else:
        bstack1lllll1lll_opy_(bstack1l1ll11l11_opy_.format(app))
    else:
      if bstack111l1ll1_opy_(app):
        bstack1lll1l1l_opy_ = app
      elif os.path.exists(app):
        bstack1lll1l1l_opy_ = bstack111l1l11l_opy_(app)
      else:
        bstack1lllll1lll_opy_(bstack1l111l111l_opy_)
  else:
    if len(app) > 2:
      bstack1lllll1lll_opy_(bstack111lll11ll_opy_)
    elif len(app) == 2:
      if bstack1l11l1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ੒") in app and bstack1l11l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੓") in app:
        if os.path.exists(app[bstack1l11l1l_opy_ (u"ࠬࡶࡡࡵࡪࠪ੔")]):
          bstack1lll1l1l_opy_ = bstack111l1l11l_opy_(config, app[bstack1l11l1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੕")], app[bstack1l11l1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੖")])
        else:
          bstack1lllll1lll_opy_(bstack1l1ll11l11_opy_.format(app))
      else:
        bstack1lllll1lll_opy_(bstack111lll11ll_opy_)
    else:
      for key in app:
        if key in bstack1ll11ll1_opy_:
          if key == bstack1l11l1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭੗"):
            if os.path.exists(app[key]):
              bstack1lll1l1l_opy_ = bstack111l1l11l_opy_(config, app[key])
            else:
              bstack1lllll1lll_opy_(bstack1l1ll11l11_opy_.format(app))
          else:
            bstack1lll1l1l_opy_ = app[key]
        else:
          bstack1lllll1lll_opy_(bstack11l11l1l11_opy_)
  return bstack1lll1l1l_opy_
def bstack111l1ll1_opy_(bstack1lll1l1l_opy_):
  import re
  bstack1l1l1l1l_opy_ = re.compile(bstack1l11l1l_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੘"))
  bstack111l1l1l1_opy_ = re.compile(bstack1l11l1l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢਖ਼"))
  if bstack1l11l1l_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪਗ਼") in bstack1lll1l1l_opy_ or re.fullmatch(bstack1l1l1l1l_opy_, bstack1lll1l1l_opy_) or re.fullmatch(bstack111l1l1l1_opy_, bstack1lll1l1l_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack111l1l11l_opy_(config, path, bstack1l1l1llll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l11l1l_opy_ (u"ࠬࡸࡢࠨਜ਼")).read()).hexdigest()
  bstack1l11ll1l1l_opy_ = bstack1l111llll_opy_(md5_hash)
  bstack1lll1l1l_opy_ = None
  if bstack1l11ll1l1l_opy_:
    logger.info(bstack1l1l1l1ll_opy_.format(bstack1l11ll1l1l_opy_, md5_hash))
    return bstack1l11ll1l1l_opy_
  bstack11l11llll1_opy_ = datetime.datetime.now()
  bstack1111l1l1_opy_ = MultipartEncoder(
    fields={
      bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࠫੜ"): (os.path.basename(path), open(os.path.abspath(path), bstack1l11l1l_opy_ (u"ࠧࡳࡤࠪ੝")), bstack1l11l1l_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬਫ਼")),
      bstack1l11l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੟"): bstack1l1l1llll1_opy_
    }
  )
  response = requests.post(bstack1lll1l111l_opy_, data=bstack1111l1l1_opy_,
                           headers={bstack1l11l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੠"): bstack1111l1l1_opy_.content_type},
                           auth=(config[bstack1l11l1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੡")], config[bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੢")]))
  try:
    res = json.loads(response.text)
    bstack1lll1l1l_opy_ = res[bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੣")]
    logger.info(bstack11lll111ll_opy_.format(bstack1lll1l1l_opy_))
    bstack1l1l11l111_opy_(md5_hash, bstack1lll1l1l_opy_)
    cli.bstack1lll11lll_opy_(bstack1l11l1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੤"), datetime.datetime.now() - bstack11l11llll1_opy_)
  except ValueError as err:
    bstack1lllll1lll_opy_(bstack1l1ll1ll1l_opy_.format(str(err)))
  return bstack1lll1l1l_opy_
def bstack1ll11111ll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1l1111_opy_
  bstack1l11l1llll_opy_ = 1
  bstack11l11l1lll_opy_ = 1
  if bstack1l11l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੥") in CONFIG:
    bstack11l11l1lll_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੦")]
  else:
    bstack11l11l1lll_opy_ = bstack1l1ll1111l_opy_(framework_name, args) or 1
  if bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧") in CONFIG:
    bstack1l11l1llll_opy_ = len(CONFIG[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੨")])
  bstack1l1l1111_opy_ = int(bstack11l11l1lll_opy_) * int(bstack1l11l1llll_opy_)
def bstack1l1ll1111l_opy_(framework_name, args):
  if framework_name == bstack111111ll_opy_ and args and bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ੩") in args:
      bstack1lll111l1l_opy_ = args.index(bstack1l11l1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੪"))
      return int(args[bstack1lll111l1l_opy_ + 1]) or 1
  return 1
def bstack1l111llll_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ੫"))
    bstack1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠨࢀࠪ੬")), bstack1l11l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੭"), bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੮"))
    if os.path.exists(bstack1ll1l1ll_opy_):
      try:
        bstack1l1ll11l1_opy_ = json.load(open(bstack1ll1l1ll_opy_, bstack1l11l1l_opy_ (u"ࠫࡷࡨࠧ੯")))
        if md5_hash in bstack1l1ll11l1_opy_:
          bstack11111l11_opy_ = bstack1l1ll11l1_opy_[md5_hash]
          bstack11111lll1_opy_ = datetime.datetime.now()
          bstack1l1l11l1l_opy_ = datetime.datetime.strptime(bstack11111l11_opy_[bstack1l11l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨੰ")], bstack1l11l1l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪੱ"))
          if (bstack11111lll1_opy_ - bstack1l1l11l1l_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack11111l11_opy_[bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬੲ")]):
            return None
          return bstack11111l11_opy_[bstack1l11l1l_opy_ (u"ࠨ࡫ࡧࠫੳ")]
      except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭ੴ").format(str(e)))
    return None
  bstack1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠪࢂࠬੵ")), bstack1l11l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੶"), bstack1l11l1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੷"))
  lock_file = bstack1ll1l1ll_opy_ + bstack1l11l1l_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ੸")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1ll1l1ll_opy_):
        with open(bstack1ll1l1ll_opy_, bstack1l11l1l_opy_ (u"ࠧࡳࠩ੹")) as f:
          content = f.read().strip()
          if content:
            bstack1l1ll11l1_opy_ = json.loads(content)
            if md5_hash in bstack1l1ll11l1_opy_:
              bstack11111l11_opy_ = bstack1l1ll11l1_opy_[md5_hash]
              bstack11111lll1_opy_ = datetime.datetime.now()
              bstack1l1l11l1l_opy_ = datetime.datetime.strptime(bstack11111l11_opy_[bstack1l11l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੺")], bstack1l11l1l_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੻"))
              if (bstack11111lll1_opy_ - bstack1l1l11l1l_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack11111l11_opy_[bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੼")]):
                return None
              return bstack11111l11_opy_[bstack1l11l1l_opy_ (u"ࠫ࡮ࡪࠧ੽")]
      return None
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮࠺ࠡࡽࢀࠫ੾").format(str(e)))
    return None
def bstack1l1l11l111_opy_(md5_hash, bstack1lll1l1l_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ੿"))
    bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠧࡿࠩ઀")), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨઁ"))
    if not os.path.exists(bstack1ll1lll1_opy_):
      os.makedirs(bstack1ll1lll1_opy_)
    bstack1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠩࢁࠫં")), bstack1l11l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઃ"), bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઄"))
    bstack1l1lll1ll_opy_ = {
      bstack1l11l1l_opy_ (u"ࠬ࡯ࡤࠨઅ"): bstack1lll1l1l_opy_,
      bstack1l11l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l11l1l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ")),
      bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ"): str(__version__)
    }
    try:
      bstack1l1ll11l1_opy_ = {}
      if os.path.exists(bstack1ll1l1ll_opy_):
        bstack1l1ll11l1_opy_ = json.load(open(bstack1ll1l1ll_opy_, bstack1l11l1l_opy_ (u"ࠩࡵࡦࠬઉ")))
      bstack1l1ll11l1_opy_[md5_hash] = bstack1l1lll1ll_opy_
      with open(bstack1ll1l1ll_opy_, bstack1l11l1l_opy_ (u"ࠥࡻ࠰ࠨઊ")) as outfile:
        json.dump(bstack1l1ll11l1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩઋ").format(str(e)))
    return
  bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠬࢄࠧઌ")), bstack1l11l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"))
  if not os.path.exists(bstack1ll1lll1_opy_):
    os.makedirs(bstack1ll1lll1_opy_)
  bstack1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠧࡿࠩ઎")), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨએ"), bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪઐ"))
  lock_file = bstack1ll1l1ll_opy_ + bstack1l11l1l_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩઑ")
  bstack1l1lll1ll_opy_ = {
    bstack1l11l1l_opy_ (u"ࠫ࡮ࡪࠧ઒"): bstack1lll1l1l_opy_,
    bstack1l11l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨઓ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l11l1l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪઔ")),
    bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬક"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1l1ll11l1_opy_ = {}
      if os.path.exists(bstack1ll1l1ll_opy_):
        with open(bstack1ll1l1ll_opy_, bstack1l11l1l_opy_ (u"ࠨࡴࠪખ")) as f:
          content = f.read().strip()
          if content:
            bstack1l1ll11l1_opy_ = json.loads(content)
      bstack1l1ll11l1_opy_[md5_hash] = bstack1l1lll1ll_opy_
      with open(bstack1ll1l1ll_opy_, bstack1l11l1l_opy_ (u"ࠤࡺࠦગ")) as outfile:
        json.dump(bstack1l1ll11l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥࡻࡰࡥࡣࡷࡩ࠿ࠦࡻࡾࠩઘ").format(str(e)))
def bstack11ll1l1l1_opy_(self):
  return
def bstack1l11l111l1_opy_(self):
  return
def bstack11l1l1l1l1_opy_():
  global bstack11lll1l11l_opy_
  bstack11lll1l11l_opy_ = True
@measure(event_name=EVENTS.bstack1llllll1l1_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1l11l1lll1_opy_(self):
  global bstack1ll1ll1l1_opy_
  global bstack11l11ll1ll_opy_
  global bstack111l1111_opy_
  try:
    if bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫઙ") in bstack1ll1ll1l1_opy_ and self.session_id != None and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩચ"), bstack1l11l1l_opy_ (u"࠭ࠧછ")) != bstack1l11l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨજ"):
      bstack1l11llll11_opy_ = bstack1l11l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨઝ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩઞ")
      if bstack1l11llll11_opy_ == bstack1l11l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪટ"):
        bstack111llll11_opy_(logger)
      if self != None:
        bstack1l11l11l_opy_(self, bstack1l11llll11_opy_, bstack1l11l1l_opy_ (u"ࠫ࠱ࠦࠧઠ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l11l1l_opy_ (u"ࠬ࠭ડ")
    if bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ઢ") in bstack1ll1ll1l1_opy_ and getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ણ"), None):
      bstack1lll1l11_opy_.bstack1ll1l11ll1_opy_(self, bstack11l1l1ll1l_opy_, logger, wait=True)
    if bstack1l11l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨત") in bstack1ll1ll1l1_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l11l11l_opy_(self, bstack1l11l1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤથ"))
      bstack111ll111_opy_.bstack1ll1l111ll_opy_(self)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦદ") + str(e))
  bstack111l1111_opy_(self)
  self.session_id = None
def bstack1ll1llll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l111ll11_opy_
    global bstack1ll1ll1l1_opy_
    command_executor = kwargs.get(bstack1l11l1l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠧધ"), bstack1l11l1l_opy_ (u"ࠬ࠭ન"))
    bstack11ll1llll_opy_ = False
    if type(command_executor) == str and bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ઩") in command_executor:
      bstack11ll1llll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪપ") in str(getattr(command_executor, bstack1l11l1l_opy_ (u"ࠨࡡࡸࡶࡱ࠭ફ"), bstack1l11l1l_opy_ (u"ࠩࠪબ"))):
      bstack11ll1llll_opy_ = True
    else:
      kwargs = bstack1ll1l11lll_opy_.bstack11lll11l1_opy_(bstack1ll1l1lll1_opy_=kwargs, config=CONFIG)
      return bstack11lllll111_opy_(self, *args, **kwargs)
    if bstack11ll1llll_opy_:
      bstack11lll1ll1_opy_ = bstack1l11l1l1_opy_.bstack1ll11lll1l_opy_(CONFIG, bstack1ll1ll1l1_opy_)
      if kwargs.get(bstack1l11l1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫભ")):
        kwargs[bstack1l11l1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬમ")] = bstack1l111ll11_opy_(kwargs[bstack1l11l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ય")], bstack1ll1ll1l1_opy_, CONFIG, bstack11lll1ll1_opy_)
      elif kwargs.get(bstack1l11l1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ર")):
        kwargs[bstack1l11l1l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ઱")] = bstack1l111ll11_opy_(kwargs[bstack1l11l1l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨલ")], bstack1ll1ll1l1_opy_, CONFIG, bstack11lll1ll1_opy_)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤળ").format(str(e)))
  return bstack11lllll111_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l11l11111_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll111ll1_opy_(self, command_executor=bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ઴"), *args, **kwargs):
  global bstack11l11ll1ll_opy_
  global bstack1ll1l11111_opy_
  bstack1llllll111_opy_ = bstack1ll1llll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l1l1lllll_opy_.on():
    return bstack1llllll111_opy_
  try:
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨવ").format(str(command_executor)))
    logger.debug(bstack1l11l1l_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧશ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩષ") in command_executor._url:
      bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨસ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫહ") in command_executor):
    bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ઺"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll11111l_opy_ = getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ઻"), None)
  bstack1lll11ll11_opy_ = {}
  if self.capabilities is not None:
    bstack1lll11ll11_opy_[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧ઼ࠪ")] = self.capabilities.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪઽ"))
    bstack1lll11ll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨા")] = self.capabilities.get(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨિ"))
    bstack1lll11ll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩી")] = self.capabilities.get(bstack1l11l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧુ"))
  if CONFIG.get(bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪૂ"), False) and bstack1ll1l11lll_opy_.bstack1l1l111ll_opy_(bstack1lll11ll11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l11l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫૃ") in bstack1ll1ll1l1_opy_ or bstack1l11l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૄ") in bstack1ll1ll1l1_opy_:
    bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(self)
  if bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ૅ") in bstack1ll1ll1l1_opy_ and bstack1ll11111l_opy_ and bstack1ll11111l_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૆"), bstack1l11l1l_opy_ (u"ࠨࠩે")) == bstack1l11l1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪૈ"):
    bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(self)
  bstack11l11ll1ll_opy_ = self.session_id
  with bstack1ll1l111_opy_:
    bstack1ll1l11111_opy_.append(self)
  return bstack1llllll111_opy_
def bstack1ll11ll1l1_opy_(args):
  return bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠫૉ") in str(args)
def bstack1l1lll1lll_opy_(self, driver_command, *args, **kwargs):
  global bstack11lll1ll11_opy_
  global bstack1l111111_opy_
  bstack1llll11l1_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ૊"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫો"), None)
  bstack11l11llll_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ૌ"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮્ࠩ"), None)
  bstack11l11111l1_opy_ = getattr(self, bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ૎"), None) != None and getattr(self, bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ૏"), None) == True
  if not bstack1l111111_opy_ and bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪૐ") in CONFIG and CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ૑")] == True and bstack1l111lll_opy_.bstack111lll11l_opy_(driver_command) and (bstack11l11111l1_opy_ or bstack1llll11l1_opy_ or bstack11l11llll_opy_) and not bstack1ll11ll1l1_opy_(args):
    try:
      bstack1l111111_opy_ = True
      logger.debug(bstack1l11l1l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ૒").format(driver_command))
      bstack11llll11l_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack11llll11l_opy_)
      try:
        bstack1lll1111l1_opy_ = {
          bstack1l11l1l_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ૓"): {
            bstack1l11l1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ૔"): bstack1l11l1l_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡄࡃࡑࠦ૕"),
            bstack1l11l1l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠨ૖"): [
              {
                bstack1l11l1l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥ૗"): driver_command
              }
            ]
          },
          bstack1l11l1l_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ૘"): {
            bstack1l11l1l_opy_ (u"ࠧࡨ࡯ࡥࡻࠥ૙"): {
              bstack1l11l1l_opy_ (u"ࠨ࡭ࡴࡩࠥ૚"): bstack11llll11l_opy_.get(bstack1l11l1l_opy_ (u"ࠢ࡮ࡵࡪࠦ૛"), bstack1l11l1l_opy_ (u"ࠣࠤ૜")) if isinstance(bstack11llll11l_opy_, dict) else bstack1l11l1l_opy_ (u"ࠤࠥ૝"),
              bstack1l11l1l_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ૞"): bstack11llll11l_opy_.get(bstack1l11l1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧ૟"), True) if isinstance(bstack11llll11l_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1l11l1l_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡩࡧࡴࡢ࠼ࠣࡿࢂ࠭ૠ").format(bstack1lll1111l1_opy_))
        bstack11l1l1l11l_opy_.info(json.dumps(bstack1lll1111l1_opy_, separators=(bstack1l11l1l_opy_ (u"࠭ࠬࠨૡ"), bstack1l11l1l_opy_ (u"ࠧ࠻ࠩૢ"))))
      except Exception as bstack1l111lll1l_opy_:
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠨૣ").format(str(bstack1l111lll1l_opy_)))
    except Exception as err:
      logger.debug(bstack1l11l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ૤").format(str(err)))
    bstack1l111111_opy_ = False
  response = bstack11lll1ll11_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૥") in str(bstack1ll1ll1l1_opy_).lower() or bstack1l11l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ૦") in str(bstack1ll1ll1l1_opy_).lower()) and bstack1l1l1lllll_opy_.on():
    try:
      if driver_command == bstack1l11l1l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ૧"):
        bstack111ll1lll1_opy_.bstack11l1111lll_opy_({
            bstack1l11l1l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ૨"): response[bstack1l11l1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭૩")],
            bstack1l11l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ૪"): bstack111ll1lll1_opy_.current_test_uuid() if bstack111ll1lll1_opy_.current_test_uuid() else bstack1l1l1lllll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11l1l11l1_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll11l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11l11ll1ll_opy_
  global bstack11lllllll_opy_
  global bstack1lll1l11l_opy_
  global bstack11ll1ll1l1_opy_
  global bstack1l1ll11ll1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack11lllll111_opy_
  global bstack1ll1l11111_opy_
  global bstack11l11ll1_opy_
  global bstack11l1l1ll1l_opy_
  if os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ૫")) is not None and bstack1ll1l11lll_opy_.bstack1lll11llll_opy_(CONFIG) is None:
    CONFIG[bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ૬")] = True
  CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭૭")] = str(bstack1ll1ll1l1_opy_) + str(__version__)
  bstack11l11lll_opy_ = os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ૮")]
  bstack11lll1ll1_opy_ = bstack1l11l1l1_opy_.bstack1ll11lll1l_opy_(CONFIG, bstack1ll1ll1l1_opy_)
  CONFIG[bstack1l11l1l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ૯")] = bstack11l11lll_opy_
  CONFIG[bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ૰")] = bstack11lll1ll1_opy_
  if CONFIG.get(bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ૱"),bstack1l11l1l_opy_ (u"ࠩࠪ૲")) and bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૳") in bstack1ll1ll1l1_opy_:
    CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ૴")].pop(bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ૵"), None)
    CONFIG[bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭૶")].pop(bstack1l11l1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ૷"), None)
  command_executor = bstack1ll1111l1_opy_()
  logger.debug(bstack1l1ll1lll1_opy_.format(command_executor))
  proxy = bstack11l11lllll_opy_(CONFIG, proxy)
  bstack1l11l1111_opy_ = 0 if bstack11lllllll_opy_ < 0 else bstack11lllllll_opy_
  try:
    if bstack11ll1ll1l1_opy_ is True:
      bstack1l11l1111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1ll11ll1_opy_ is True:
      bstack1l11l1111_opy_ = int(threading.current_thread().name)
  except:
    bstack1l11l1111_opy_ = 0
  bstack1lll11111_opy_ = bstack1l1l11ll1l_opy_(CONFIG, bstack1l11l1111_opy_)
  logger.debug(bstack1l1111l1l1_opy_.format(str(bstack1lll11111_opy_)))
  if bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ૸") in CONFIG and bstack11lll1l1l_opy_(CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ૹ")]):
    bstack1l1111ll11_opy_(bstack1lll11111_opy_)
  if bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack1l11l1111_opy_) and bstack1ll1l11lll_opy_.bstack1ll11ll111_opy_(bstack1lll11111_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack1ll1l11lll_opy_.set_capabilities(bstack1lll11111_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll1lllll_opy_ = bstack1ll11l11ll_opy_(desired_capabilities)
    bstack1lll1lllll_opy_[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪૺ")] = bstack1lllll111l_opy_(CONFIG)
    bstack1ll11ll1ll_opy_ = bstack1l1l11ll1l_opy_(bstack1lll1lllll_opy_)
    if bstack1ll11ll1ll_opy_:
      bstack1lll11111_opy_ = update(bstack1ll11ll1ll_opy_, bstack1lll11111_opy_)
    desired_capabilities = None
  if options:
    bstack11l1ll1111_opy_(options, bstack1lll11111_opy_)
  if not options:
    options = bstack11ll11111_opy_(bstack1lll11111_opy_)
  bstack11l1l1ll1l_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧૻ"))[bstack1l11l1111_opy_]
  if proxy and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬૼ")):
    options.proxy(proxy)
  if options and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ૽")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll1l1ll11_opy_() < version.parse(bstack1l11l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭૾")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll11111_opy_)
  logger.info(bstack1ll1111l1l_opy_)
  bstack1lll1l111_opy_.end(EVENTS.bstack1111111ll_opy_.value, EVENTS.bstack1111111ll_opy_.value + bstack1l11l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ૿"), EVENTS.bstack1111111ll_opy_.value + bstack1l11l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ଀"), status=True, failure=None, test_name=bstack1lll1l11l_opy_)
  if bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଁ") in kwargs:
    del kwargs[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ࠭ଂ")]
  try:
    if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬଃ")):
      bstack11lllll111_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ଄")):
      bstack11lllll111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧଅ")):
      bstack11lllll111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack11lllll111_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l111lll11_opy_:
    logger.error(bstack1llll111l1_opy_.format(bstack1l11l1l_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧଆ"), str(bstack1l111lll11_opy_)))
    raise bstack1l111lll11_opy_
  if bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack1l11l1111_opy_) and bstack1ll1l11lll_opy_.bstack1ll11ll111_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫଇ")][bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩଈ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack1ll1l11lll_opy_.set_capabilities(bstack1lll11111_opy_, CONFIG)
  try:
    bstack1ll11lll11_opy_ = bstack1l11l1l_opy_ (u"ࠫࠬଉ")
    if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ଊ")):
      if self.caps is not None:
        bstack1ll11lll11_opy_ = self.caps.get(bstack1l11l1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨଋ"))
    else:
      if self.capabilities is not None:
        bstack1ll11lll11_opy_ = self.capabilities.get(bstack1l11l1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢଌ"))
    if bstack1ll11lll11_opy_:
      bstack1l11ll1111_opy_(bstack1ll11lll11_opy_)
      if bstack1ll1l1ll11_opy_() <= version.parse(bstack1l11l1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ଍")):
        self.command_executor._url = bstack1l11l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ଎") + bstack1l1llll111_opy_ + bstack1l11l1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢଏ")
      else:
        self.command_executor._url = bstack1l11l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨଐ") + bstack1ll11lll11_opy_ + bstack1l11l1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ଑")
      logger.debug(bstack1llll11lll_opy_.format(bstack1ll11lll11_opy_))
    else:
      logger.debug(bstack1ll1111l_opy_.format(bstack1l11l1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ଒")))
  except Exception as e:
    logger.debug(bstack1ll1111l_opy_.format(e))
  if bstack1l11l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଓ") in bstack1ll1ll1l1_opy_:
    bstack1l1llll11l_opy_(bstack11lllllll_opy_, bstack11l11ll1_opy_)
  bstack11l11ll1ll_opy_ = self.session_id
  if bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨଔ") in bstack1ll1ll1l1_opy_ or bstack1l11l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩକ") in bstack1ll1ll1l1_opy_ or bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଖ") in bstack1ll1ll1l1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1ll11111l_opy_ = getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬଗ"), None)
  if bstack1l11l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬଘ") in bstack1ll1ll1l1_opy_ or bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬଙ") in bstack1ll1ll1l1_opy_:
    bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(self)
  if bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧଚ") in bstack1ll1ll1l1_opy_ and bstack1ll11111l_opy_ and bstack1ll11111l_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨଛ"), bstack1l11l1l_opy_ (u"ࠩࠪଜ")) == bstack1l11l1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫଝ"):
    bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(self)
  with bstack1ll1l111_opy_:
    bstack1ll1l11111_opy_.append(self)
  if bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ") in CONFIG and bstack1l11l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଟ") in CONFIG[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")][bstack1l11l1111_opy_]:
    bstack1lll1l11l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][bstack1l11l1111_opy_][bstack1l11l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଢ")]
  logger.debug(bstack11lll1l1l1_opy_.format(bstack11l11ll1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11l11ll11l_opy_
    def bstack1l1llll1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l111l1ll_opy_
      if(bstack1l11l1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦଣ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠪࢂࠬତ")), bstack1l11l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଥ"), bstack1l11l1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧଦ")), bstack1l11l1l_opy_ (u"࠭ࡷࠨଧ")) as fp:
          fp.write(bstack1l11l1l_opy_ (u"ࠢࠣନ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l11l1l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ଩")))):
          with open(args[1], bstack1l11l1l_opy_ (u"ࠩࡵࠫପ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l11l1l_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩଫ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111l11l1_opy_)
            if bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨବ") in CONFIG and str(CONFIG[bstack1l11l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩଭ")]).lower() != bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬମ"):
                bstack11111l11l_opy_ = bstack11l11ll11l_opy_()
                bstack1l111l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭ଯ").format(bstack11111l11l_opy_=bstack11111l11l_opy_)
            lines.insert(1, bstack1l111l1l11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l11l1l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥର")), bstack1l11l1l_opy_ (u"ࠩࡺࠫ଱")) as bstack1llll1ll1l_opy_:
              bstack1llll1ll1l_opy_.writelines(lines)
        CONFIG[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬଲ")] = str(bstack1ll1ll1l1_opy_) + str(__version__)
        bstack11l11lll_opy_ = os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩଳ")]
        bstack11lll1ll1_opy_ = bstack1l11l1l1_opy_.bstack1ll11lll1l_opy_(CONFIG, bstack1ll1ll1l1_opy_)
        CONFIG[bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ଴")] = bstack11l11lll_opy_
        CONFIG[bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨଵ")] = bstack11lll1ll1_opy_
        bstack1l11l1111_opy_ = 0 if bstack11lllllll_opy_ < 0 else bstack11lllllll_opy_
        try:
          if bstack11ll1ll1l1_opy_ is True:
            bstack1l11l1111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1ll11ll1_opy_ is True:
            bstack1l11l1111_opy_ = int(threading.current_thread().name)
        except:
          bstack1l11l1111_opy_ = 0
        CONFIG[bstack1l11l1l_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢଶ")] = False
        CONFIG[bstack1l11l1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢଷ")] = True
        bstack1lll11111_opy_ = bstack1l1l11ll1l_opy_(CONFIG, bstack1l11l1111_opy_)
        logger.debug(bstack1l1111l1l1_opy_.format(str(bstack1lll11111_opy_)))
        if CONFIG.get(bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ସ")):
          bstack1l1111ll11_opy_(bstack1lll11111_opy_)
        if bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ହ") in CONFIG and bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ଺") in CONFIG[bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଻")][bstack1l11l1111_opy_]:
          bstack1lll1l11l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ଼ࠩ")][bstack1l11l1111_opy_][bstack1l11l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଽ")]
        args.append(os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠨࢀࠪା")), bstack1l11l1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩି"), bstack1l11l1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬୀ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll11111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l11l1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨୁ"))
      bstack11l111l1ll_opy_ = True
      return bstack1ll1ll1l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll1l1l11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11lllllll_opy_
    global bstack1lll1l11l_opy_
    global bstack11ll1ll1l1_opy_
    global bstack1l1ll11ll1_opy_
    global bstack1ll1ll1l1_opy_
    CONFIG[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧୂ")] = str(bstack1ll1ll1l1_opy_) + str(__version__)
    bstack11l11lll_opy_ = os.environ[bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫୃ")]
    bstack11lll1ll1_opy_ = bstack1l11l1l1_opy_.bstack1ll11lll1l_opy_(CONFIG, bstack1ll1ll1l1_opy_)
    CONFIG[bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪୄ")] = bstack11l11lll_opy_
    CONFIG[bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ୅")] = bstack11lll1ll1_opy_
    bstack1l11l1111_opy_ = 0 if bstack11lllllll_opy_ < 0 else bstack11lllllll_opy_
    try:
      if bstack11ll1ll1l1_opy_ is True:
        bstack1l11l1111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1ll11ll1_opy_ is True:
        bstack1l11l1111_opy_ = int(threading.current_thread().name)
    except:
      bstack1l11l1111_opy_ = 0
    CONFIG[bstack1l11l1l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ୆")] = True
    bstack1lll11111_opy_ = bstack1l1l11ll1l_opy_(CONFIG, bstack1l11l1111_opy_)
    logger.debug(bstack1l1111l1l1_opy_.format(str(bstack1lll11111_opy_)))
    if CONFIG.get(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧେ")):
      bstack1l1111ll11_opy_(bstack1lll11111_opy_)
    if bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧୈ") in CONFIG and bstack1l11l1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୉") in CONFIG[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୊")][bstack1l11l1111_opy_]:
      bstack1lll1l11l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୋ")][bstack1l11l1111_opy_][bstack1l11l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ୌ")]
    import urllib
    import json
    if bstack1l11l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ୍࠭") in CONFIG and str(CONFIG[bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ୎")]).lower() != bstack1l11l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ୏"):
        bstack11llll1ll1_opy_ = bstack11l11ll11l_opy_()
        bstack11111l11l_opy_ = bstack11llll1ll1_opy_ + urllib.parse.quote(json.dumps(bstack1lll11111_opy_))
    else:
        bstack11111l11l_opy_ = bstack1l11l1l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ୐") + urllib.parse.quote(json.dumps(bstack1lll11111_opy_))
    browser = self.connect(bstack11111l11l_opy_)
    return browser
except Exception as e:
    pass
def bstack11l11111ll_opy_():
    global bstack11l111l1ll_opy_
    global bstack1ll1ll1l1_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11ll1ll1_opy_
        global bstack11llllll_opy_
        if not bstack11llllll1_opy_:
          global bstack1ll1lllll1_opy_
          if not bstack1ll1lllll1_opy_:
            from bstack_utils.helper import bstack1l1l111111_opy_, bstack111lllll_opy_, bstack1l1l1111l_opy_
            bstack1ll1lllll1_opy_ = bstack1l1l111111_opy_()
            bstack111lllll_opy_(bstack1ll1ll1l1_opy_)
            bstack11lll1ll1_opy_ = bstack1l11l1l1_opy_.bstack1ll11lll1l_opy_(CONFIG, bstack1ll1ll1l1_opy_)
            bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣ୑"), bstack11lll1ll1_opy_)
          BrowserType.connect = bstack11ll1ll1_opy_
          return
        BrowserType.launch = bstack1lll1l1l11_opy_
        bstack11l111l1ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1llll1ll_opy_
      bstack11l111l1ll_opy_ = True
    except Exception as e:
      pass
def bstack11llllll1l_opy_(context, bstack1ll11lll1_opy_):
  try:
    context.page.evaluate(bstack1l11l1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ୒"), bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ୓")+ json.dumps(bstack1ll11lll1_opy_) + bstack1l11l1l_opy_ (u"ࠤࢀࢁࠧ୔"))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧ୕").format(str(e), traceback.format_exc()))
def bstack11llll11l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l11l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧୖ"), bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪୗ") + json.dumps(message) + bstack1l11l1l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ୘") + json.dumps(level) + bstack1l11l1l_opy_ (u"ࠧࡾࡿࠪ୙"))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣ୚").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1ll1l111l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack111lllll11_opy_(self, url):
  global bstack1llll1l11_opy_
  try:
    bstack111ll1l1ll_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1l1ll1_opy_.format(str(err)))
  try:
    bstack1llll1l11_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1lll1l1_opy_ = str(e)
      if any(err_msg in bstack1l1lll1l1_opy_ for err_msg in bstack1l11lll1l1_opy_):
        bstack111ll1l1ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1l1ll1_opy_.format(str(err)))
    raise e
def bstack1ll11ll11_opy_(self):
  global bstack1l111lllll_opy_
  bstack1l111lllll_opy_ = self
  return
def bstack1l1ll11111_opy_(self):
  global bstack111l1lll_opy_
  bstack111l1lll_opy_ = self
  return
def bstack11l1lll111_opy_(test_name, bstack1l11l1l1l_opy_):
  global CONFIG
  if percy.bstack111ll11ll_opy_() == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ୛"):
    bstack1lll11l111_opy_ = os.path.relpath(bstack1l11l1l1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1lll11l111_opy_)
    bstack1l1l111lll_opy_ = suite_name + bstack1l11l1l_opy_ (u"ࠥ࠱ࠧଡ଼") + test_name
    threading.current_thread().percySessionName = bstack1l1l111lll_opy_
def bstack1lll11111l_opy_(self, test, *args, **kwargs):
  global bstack11ll11l1ll_opy_
  test_name = None
  bstack1l11l1l1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l11l1l1l_opy_ = str(test.source)
  bstack11l1lll111_opy_(test_name, bstack1l11l1l1l_opy_)
  bstack11ll11l1ll_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll111l11_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack11111l1ll_opy_(driver, bstack1l1l111lll_opy_):
  if not bstack1l11ll111_opy_ and bstack1l1l111lll_opy_:
      bstack1l11lll11_opy_ = {
          bstack1l11l1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫଢ଼"): bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୞"),
          bstack1l11l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩୟ"): {
              bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬୠ"): bstack1l1l111lll_opy_
          }
      }
      bstack111l1llll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ୡ").format(json.dumps(bstack1l11lll11_opy_))
      driver.execute_script(bstack111l1llll_opy_)
  if bstack11111llll_opy_:
      bstack1lll1llll1_opy_ = {
          bstack1l11l1l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩୢ"): bstack1l11l1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬୣ"),
          bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ୤"): {
              bstack1l11l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪ୥"): bstack1l1l111lll_opy_ + bstack1l11l1l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ୦"),
              bstack1l11l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭୧"): bstack1l11l1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭୨")
          }
      }
      if bstack11111llll_opy_.status == bstack1l11l1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ୩"):
          bstack11lll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ୪").format(json.dumps(bstack1lll1llll1_opy_))
          driver.execute_script(bstack11lll1l1_opy_)
          bstack1l11l11l_opy_(driver, bstack1l11l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ୫"))
      elif bstack11111llll_opy_.status == bstack1l11l1l_opy_ (u"ࠬࡌࡁࡊࡎࠪ୬"):
          reason = bstack1l11l1l_opy_ (u"ࠨࠢ୭")
          bstack1l1111ll_opy_ = bstack1l1l111lll_opy_ + bstack1l11l1l_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ୮")
          if bstack11111llll_opy_.message:
              reason = str(bstack11111llll_opy_.message)
              bstack1l1111ll_opy_ = bstack1l1111ll_opy_ + bstack1l11l1l_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ୯") + reason
          bstack1lll1llll1_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ୰")] = {
              bstack1l11l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩୱ"): bstack1l11l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ୲"),
              bstack1l11l1l_opy_ (u"ࠬࡪࡡࡵࡣࠪ୳"): bstack1l1111ll_opy_
          }
          bstack11lll1l1_opy_ = bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ୴").format(json.dumps(bstack1lll1llll1_opy_))
          driver.execute_script(bstack11lll1l1_opy_)
          bstack1l11l11l_opy_(driver, bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ୵"), reason)
          bstack111llllll1_opy_(reason, str(bstack11111llll_opy_), str(bstack11lllllll_opy_), logger)
@measure(event_name=EVENTS.bstack1l1l11111_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll111111_opy_(driver, test):
  if percy.bstack111ll11ll_opy_() == bstack1l11l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ୶") and percy.bstack1ll111l1l_opy_() == bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ୷"):
      bstack1ll1111ll1_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭୸"), None)
      bstack11l111lll1_opy_(driver, bstack1ll1111ll1_opy_, test)
  if (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ୹"), None) and
      bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ୺"), None)) or (
      bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭୻"), None) and
      bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ୼"), None)):
      logger.info(bstack1l11l1l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ୽"))
      bstack1ll1l11lll_opy_.bstack11ll11l1l_opy_(driver, name=test.name, path=test.source)
def bstack1l1111ll1l_opy_(test, bstack1l1l111lll_opy_):
    try:
      bstack11l11llll1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l11l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୾")] = bstack1l1l111lll_opy_
      if bstack11111llll_opy_:
        if bstack11111llll_opy_.status == bstack1l11l1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୿"):
          data[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ஀")] = bstack1l11l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ஁")
        elif bstack11111llll_opy_.status == bstack1l11l1l_opy_ (u"࠭ࡆࡂࡋࡏࠫஂ"):
          data[bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧஃ")] = bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஄")
          if bstack11111llll_opy_.message:
            data[bstack1l11l1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩஅ")] = str(bstack11111llll_opy_.message)
      user = CONFIG[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬஆ")]
      key = CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஇ")]
      host = bstack11l11l1l1l_opy_(cli.config, [bstack1l11l1l_opy_ (u"ࠧࡧࡰࡪࡵࠥஈ"), bstack1l11l1l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣஉ"), bstack1l11l1l_opy_ (u"ࠢࡢࡲ࡬ࠦஊ")], bstack1l11l1l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠤ஋"))
      url = bstack1l11l1l_opy_ (u"ࠩࡾࢁ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪ஌").format(host, bstack11l11ll1ll_opy_)
      headers = {
        bstack1l11l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ஍"): bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧஎ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack1lll11lll_opy_(bstack1l11l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡹࡵࡪࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠤஏ"), datetime.datetime.now() - bstack11l11llll1_opy_)
    except Exception as e:
      logger.error(bstack11l1llll1l_opy_.format(str(e)))
def bstack1l1ll111_opy_(test, bstack1l1l111lll_opy_):
  global CONFIG
  global bstack111l1lll_opy_
  global bstack1l111lllll_opy_
  global bstack11l11ll1ll_opy_
  global bstack11111llll_opy_
  global bstack1lll1l11l_opy_
  global bstack1l11lll111_opy_
  global bstack1l1ll11ll_opy_
  global bstack111l1l111_opy_
  global bstack11lll11111_opy_
  global bstack1ll1l11111_opy_
  global bstack11l1l1ll1l_opy_
  global bstack1l11ll1ll_opy_
  try:
    if not bstack11l11ll1ll_opy_:
      with bstack1l11ll1ll_opy_:
        bstack1lll1111l_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"࠭ࡾࠨஐ")), bstack1l11l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ஑"), bstack1l11l1l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪஒ"))
        if os.path.exists(bstack1lll1111l_opy_):
          with open(bstack1lll1111l_opy_, bstack1l11l1l_opy_ (u"ࠩࡵࠫஓ")) as f:
            content = f.read().strip()
            if content:
              bstack1l11l11ll1_opy_ = json.loads(bstack1l11l1l_opy_ (u"ࠥࡿࠧஔ") + content + bstack1l11l1l_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭க") + bstack1l11l1l_opy_ (u"ࠧࢃࠢ஖"))
              bstack11l11ll1ll_opy_ = bstack1l11l11ll1_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࡶࠤ࡫࡯࡬ࡦ࠼ࠣࠫ஗") + str(e))
  if bstack1ll1l11111_opy_:
    with bstack1ll1l111_opy_:
      bstack111l1111l_opy_ = bstack1ll1l11111_opy_.copy()
    for driver in bstack111l1111l_opy_:
      if bstack11l11ll1ll_opy_ == driver.session_id:
        if test:
          bstack1ll111111_opy_(driver, test)
        bstack11111l1ll_opy_(driver, bstack1l1l111lll_opy_)
  elif bstack11l11ll1ll_opy_:
    bstack1l1111ll1l_opy_(test, bstack1l1l111lll_opy_)
  if bstack111l1lll_opy_:
    bstack1l1ll11ll_opy_(bstack111l1lll_opy_)
  if bstack1l111lllll_opy_:
    bstack111l1l111_opy_(bstack1l111lllll_opy_)
  if bstack11lll1l11l_opy_:
    bstack11lll11111_opy_()
def bstack1l11l111l_opy_(self, test, *args, **kwargs):
  bstack1l1l111lll_opy_ = None
  if test:
    bstack1l1l111lll_opy_ = str(test.name)
  bstack1l1ll111_opy_(test, bstack1l1l111lll_opy_)
  bstack1l11lll111_opy_(self, test, *args, **kwargs)
def bstack11l1ll11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1ll1ll_opy_
  global CONFIG
  global bstack1ll1l11111_opy_
  global bstack11l11ll1ll_opy_
  global bstack1l11ll1ll_opy_
  bstack111111ll1_opy_ = None
  try:
    if bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭஘"), None) or bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪங"), None):
      try:
        if not bstack11l11ll1ll_opy_:
          bstack1lll1111l_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠩࢁࠫச")), bstack1l11l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ஛"), bstack1l11l1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ஜ"))
          with bstack1l11ll1ll_opy_:
            if os.path.exists(bstack1lll1111l_opy_):
              with open(bstack1lll1111l_opy_, bstack1l11l1l_opy_ (u"ࠬࡸࠧ஝")) as f:
                content = f.read().strip()
                if content:
                  bstack1l11l11ll1_opy_ = json.loads(bstack1l11l1l_opy_ (u"ࠨࡻࠣஞ") + content + bstack1l11l1l_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩட") + bstack1l11l1l_opy_ (u"ࠣࡿࠥ஠"))
                  bstack11l11ll1ll_opy_ = bstack1l11l11ll1_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡹࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࠨ஡") + str(e))
      if bstack1ll1l11111_opy_:
        with bstack1ll1l111_opy_:
          bstack111l1111l_opy_ = bstack1ll1l11111_opy_.copy()
        for driver in bstack111l1111l_opy_:
          if bstack11l11ll1ll_opy_ == driver.session_id:
            bstack111111ll1_opy_ = driver
    bstack1111l11l_opy_ = bstack1ll1l11lll_opy_.bstack1l1l11llll_opy_(test.tags)
    if bstack111111ll1_opy_:
      threading.current_thread().isA11yTest = bstack1ll1l11lll_opy_.bstack1lllll1ll_opy_(bstack111111ll1_opy_, bstack1111l11l_opy_)
      threading.current_thread().isAppA11yTest = bstack1ll1l11lll_opy_.bstack1lllll1ll_opy_(bstack111111ll1_opy_, bstack1111l11l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1111l11l_opy_
      threading.current_thread().isAppA11yTest = bstack1111l11l_opy_
  except:
    pass
  bstack11ll1ll1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11111llll_opy_
  try:
    bstack11111llll_opy_ = self._test
  except:
    bstack11111llll_opy_ = self.test
def bstack11ll1llll1_opy_():
  global bstack11l11111l_opy_
  try:
    if os.path.exists(bstack11l11111l_opy_):
      os.remove(bstack11l11111l_opy_)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭஢") + str(e))
def bstack11llllllll_opy_():
  global bstack11l11111l_opy_
  bstack1lll1lll_opy_ = {}
  lock_file = bstack11l11111l_opy_ + bstack1l11l1l_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪண")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨத"))
    try:
      if not os.path.isfile(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"࠭ࡷࠨ஥")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠧࡳࠩ஦")) as f:
          content = f.read().strip()
          if content:
            bstack1lll1lll_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ஧") + str(e))
    return bstack1lll1lll_opy_
  try:
    os.makedirs(os.path.dirname(bstack11l11111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠩࡺࠫந")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠪࡶࠬன")) as f:
          content = f.read().strip()
          if content:
            bstack1lll1lll_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ப") + str(e))
  finally:
    return bstack1lll1lll_opy_
def bstack1l1llll11l_opy_(platform_index, item_index):
  global bstack11l11111l_opy_
  lock_file = bstack11l11111l_opy_ + bstack1l11l1l_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫ஫")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ஬"))
    try:
      bstack1lll1lll_opy_ = {}
      if os.path.exists(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠧࡳࠩ஭")) as f:
          content = f.read().strip()
          if content:
            bstack1lll1lll_opy_ = json.loads(content)
      bstack1lll1lll_opy_[item_index] = platform_index
      with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠣࡹࠥம")) as outfile:
        json.dump(bstack1lll1lll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧய") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11l11111l_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack1lll1lll_opy_ = {}
      if os.path.exists(bstack11l11111l_opy_):
        with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠪࡶࠬர")) as f:
          content = f.read().strip()
          if content:
            bstack1lll1lll_opy_ = json.loads(content)
      bstack1lll1lll_opy_[item_index] = platform_index
      with open(bstack11l11111l_opy_, bstack1l11l1l_opy_ (u"ࠦࡼࠨற")) as outfile:
        json.dump(bstack1lll1lll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪல") + str(e))
def bstack11ll111111_opy_(bstack1l11ll11_opy_):
  global CONFIG
  bstack1l1lll1ll1_opy_ = bstack1l11l1l_opy_ (u"࠭ࠧள")
  if not bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪழ") in CONFIG:
    logger.info(bstack1l11l1l_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬவ"))
  try:
    platform = CONFIG[bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬஶ")][bstack1l11ll11_opy_]
    if bstack1l11l1l_opy_ (u"ࠪࡳࡸ࠭ஷ") in platform:
      bstack1l1lll1ll1_opy_ += str(platform[bstack1l11l1l_opy_ (u"ࠫࡴࡹࠧஸ")]) + bstack1l11l1l_opy_ (u"ࠬ࠲ࠠࠨஹ")
    if bstack1l11l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ஺") in platform:
      bstack1l1lll1ll1_opy_ += str(platform[bstack1l11l1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஻")]) + bstack1l11l1l_opy_ (u"ࠨ࠮ࠣࠫ஼")
    if bstack1l11l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭஽") in platform:
      bstack1l1lll1ll1_opy_ += str(platform[bstack1l11l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧா")]) + bstack1l11l1l_opy_ (u"ࠫ࠱ࠦࠧி")
    if bstack1l11l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧீ") in platform:
      bstack1l1lll1ll1_opy_ += str(platform[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨு")]) + bstack1l11l1l_opy_ (u"ࠧ࠭ࠢࠪூ")
    if bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭௃") in platform:
      bstack1l1lll1ll1_opy_ += str(platform[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ௄")]) + bstack1l11l1l_opy_ (u"ࠪ࠰ࠥ࠭௅")
    if bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬெ") in platform:
      bstack1l1lll1ll1_opy_ += str(platform[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ே")]) + bstack1l11l1l_opy_ (u"࠭ࠬࠡࠩை")
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧ௉") + str(e))
  finally:
    if bstack1l1lll1ll1_opy_[len(bstack1l1lll1ll1_opy_) - 2:] == bstack1l11l1l_opy_ (u"ࠨ࠮ࠣࠫொ"):
      bstack1l1lll1ll1_opy_ = bstack1l1lll1ll1_opy_[:-2]
    return bstack1l1lll1ll1_opy_
def bstack1lll111ll_opy_(path, bstack1l1lll1ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11ll1l1111_opy_ = ET.parse(path)
    bstack1llll11ll1_opy_ = bstack11ll1l1111_opy_.getroot()
    bstack1l11ll1l11_opy_ = None
    for suite in bstack1llll11ll1_opy_.iter(bstack1l11l1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨோ")):
      if bstack1l11l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪௌ") in suite.attrib:
        suite.attrib[bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦ்ࠩ")] += bstack1l11l1l_opy_ (u"ࠬࠦࠧ௎") + bstack1l1lll1ll1_opy_
        bstack1l11ll1l11_opy_ = suite
    bstack1l1lll11l1_opy_ = None
    for robot in bstack1llll11ll1_opy_.iter(bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௏")):
      bstack1l1lll11l1_opy_ = robot
    bstack1ll1l1l11l_opy_ = len(bstack1l1lll11l1_opy_.findall(bstack1l11l1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ௐ")))
    if bstack1ll1l1l11l_opy_ == 1:
      bstack1l1lll11l1_opy_.remove(bstack1l1lll11l1_opy_.findall(bstack1l11l1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௑"))[0])
      bstack1l1l11l1_opy_ = ET.Element(bstack1l11l1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௒"), attrib={bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ௓"): bstack1l11l1l_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ௔"), bstack1l11l1l_opy_ (u"ࠬ࡯ࡤࠨ௕"): bstack1l11l1l_opy_ (u"࠭ࡳ࠱ࠩ௖")})
      bstack1l1lll11l1_opy_.insert(1, bstack1l1l11l1_opy_)
      bstack1l1llll1_opy_ = None
      for suite in bstack1l1lll11l1_opy_.iter(bstack1l11l1l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ௗ")):
        bstack1l1llll1_opy_ = suite
      bstack1l1llll1_opy_.append(bstack1l11ll1l11_opy_)
      bstack11ll1l111_opy_ = None
      for status in bstack1l11ll1l11_opy_.iter(bstack1l11l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ௘")):
        bstack11ll1l111_opy_ = status
      bstack1l1llll1_opy_.append(bstack11ll1l111_opy_)
    bstack11ll1l1111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ௙") + str(e))
def bstack1lll1ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l1lll_opy_
  global CONFIG
  if bstack1l11l1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ௚") in options:
    del options[bstack1l11l1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ௛")]
  bstack11lll11l11_opy_ = bstack11llllllll_opy_()
  for item_id in bstack11lll11l11_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1l11l1l_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩ௜"))
    bstack1lll111ll_opy_(path, bstack11ll111111_opy_(bstack11lll11l11_opy_[item_id]))
  bstack11ll1llll1_opy_()
  return bstack1l1l1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l11lll1_opy_(self, ff_profile_dir):
  global bstack11ll11ll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll11ll1_opy_(self, ff_profile_dir)
def bstack111ll11l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1llllll11_opy_
  bstack1l11l1ll1_opy_ = []
  if bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௝") in CONFIG:
    bstack1l11l1ll1_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௞")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l11l1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ௟")],
      pabot_args[bstack1l11l1l_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ௠")],
      argfile,
      pabot_args.get(bstack1l11l1l_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ௡")),
      pabot_args[bstack1l11l1l_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢ௢")],
      platform[0],
      bstack1llllll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l11l1l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ௣")] or [(bstack1l11l1l_opy_ (u"ࠨࠢ௤"), None)]
    for platform in enumerate(bstack1l11l1ll1_opy_)
  ]
def bstack11llllll11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1l11l1l_opy_=bstack1l11l1l_opy_ (u"ࠧࠨ௥")):
  global bstack1ll1ll1l1l_opy_
  self.platform_index = platform_index
  self.bstack1l11l1111l_opy_ = bstack1ll1l11l1l_opy_
  bstack1ll1ll1l1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1llll11l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111l111l1_opy_
  global bstack1l11l1lll_opy_
  bstack1ll1l1lll_opy_ = copy.deepcopy(item)
  if not bstack1l11l1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ௦") in item.options:
    bstack1ll1l1lll_opy_.options[bstack1l11l1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ௧")] = []
  bstack11lll1lll_opy_ = bstack1ll1l1lll_opy_.options[bstack1l11l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௨")].copy()
  for v in bstack1ll1l1lll_opy_.options[bstack1l11l1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௩")]:
    if bstack1l11l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ௪") in v:
      bstack11lll1lll_opy_.remove(v)
    if bstack1l11l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭௫") in v:
      bstack11lll1lll_opy_.remove(v)
    if bstack1l11l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ௬") in v:
      bstack11lll1lll_opy_.remove(v)
  bstack11lll1lll_opy_.insert(0, bstack1l11l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ௭").format(bstack1ll1l1lll_opy_.platform_index))
  bstack11lll1lll_opy_.insert(0, bstack1l11l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩ௮").format(bstack1ll1l1lll_opy_.bstack1l11l1111l_opy_))
  bstack1ll1l1lll_opy_.options[bstack1l11l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௯")] = bstack11lll1lll_opy_
  if bstack1l11l1lll_opy_:
    bstack1ll1l1lll_opy_.options[bstack1l11l1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௰")].insert(0, bstack1l11l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨ௱").format(bstack1l11l1lll_opy_))
  return bstack111l111l1_opy_(caller_id, datasources, is_last, bstack1ll1l1lll_opy_, outs_dir)
def bstack1l1l11ll1_opy_(command, item_index):
  try:
    if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ௲")):
      os.environ[bstack1l11l1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ௳")] = json.dumps(CONFIG[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௴")][item_index % bstack1l1l1ll1_opy_])
    global bstack1l11l1lll_opy_
    if bstack1l11l1lll_opy_:
      command[0] = command[0].replace(bstack1l11l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௵"), bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ௶") + str(item_index % bstack1l1l1ll1_opy_) + bstack1l11l1l_opy_ (u"ࠫࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ௷") + str(
        item_index) + bstack1l11l1l_opy_ (u"ࠬࠦࠧ௸") + bstack1l11l1lll_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௹"),
                                      bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ௺") +  str(item_index % bstack1l1l1ll1_opy_) + bstack1l11l1l_opy_ (u"ࠨࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ௻") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡯ࡲࡨ࡮࡬ࡹࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࡬࡯ࡳࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲ࠿ࠦࡻࡾࠩ௼").format(str(e)))
def bstack1ll11l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll1ll111_opy_
  try:
    bstack1l1l11ll1_opy_(command, item_index)
    return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮࠻ࠢࡾࢁࠬ௽").format(str(e)))
    raise e
def bstack11l1l1l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll1ll111_opy_
  try:
    bstack1l1l11ll1_opy_(command, item_index)
    return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯ࠢ࠵࠲࠶࠹࠺ࠡࡽࢀࠫ௾").format(str(e)))
    try:
      return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦ࠲࠯࠳࠶ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪ௿").format(str(e2)))
      raise e
def bstack1l1l1l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll1ll111_opy_
  try:
    bstack1l1l11ll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠷࠴࠱࠶࠼ࠣࡿࢂ࠭ఀ").format(str(e)))
    try:
      return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l11l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡ࠴࠱࠵࠺ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠬఁ").format(str(e2)))
      raise e
def _1111lll1l_opy_(bstack1ll11l111l_opy_, item_index, process_timeout, sleep_before_start, bstack1l1ll1ll11_opy_):
  bstack1l1l11ll1_opy_(bstack1ll11l111l_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack111ll1ll_opy_(command, bstack111ll1l1_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1ll111_opy_
  global bstack11111l111_opy_
  global bstack1l11l1lll_opy_
  try:
    for env_name, bstack1l11111l1l_opy_ in bstack11111l111_opy_.items():
      os.environ[env_name] = bstack1l11111l1l_opy_
    bstack1l11l1lll_opy_ = bstack1l11l1l_opy_ (u"ࠣࠤం")
    bstack1l1l11ll1_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1ll1ll111_opy_(command, bstack111ll1l1_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡢࡰࡶࠣࡶࡺࡴࠠ࠶࠰࠳࠾ࠥࢁࡽࠨః").format(str(e)))
    try:
      return bstack1ll1ll111_opy_(command, bstack111ll1l1_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l11l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠪఄ").format(str(e2)))
      raise e
def bstack11l11l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll1ll111_opy_
  try:
    process_timeout = _1111lll1l_opy_(command, item_index, process_timeout, sleep_before_start, bstack1l11l1l_opy_ (u"ࠫ࠹࠴࠲ࠨఅ"))
    return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠸࠳࠸࠺ࠡࡽࢀࠫఆ").format(str(e)))
    try:
      return bstack1ll1ll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l11l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ఇ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll11lll_opy_(self, runner, quiet=False, capture=True):
  global bstack11l111ll_opy_
  bstack1l1l111ll1_opy_ = bstack11l111ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l11l1l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧఈ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l11l1l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬఉ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1l111ll1_opy_
def bstack11ll11ll11_opy_(runner, hook_name, context, element, bstack11l1lllll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11lll11l_opy_.bstack1l11llll1l_opy_(hook_name, element)
    bstack11l1lllll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11lll11l_opy_.bstack1lll1l1l1_opy_(element)
      if hook_name not in [bstack1l11l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ఊ"), bstack1l11l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ఋ")] and args and hasattr(args[0], bstack1l11l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫఌ")):
        args[0].error_message = bstack1l11l1l_opy_ (u"ࠬ࠭఍")
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡫ࡥࡳࡪ࡬ࡦࠢ࡫ࡳࡴࡱࡳࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨఎ").format(str(e)))
@measure(event_name=EVENTS.bstack1l1111l111_opy_, stage=STAGE.bstack11l1llllll_opy_, hook_type=bstack1l11l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡁ࡭࡮ࠥఏ"), bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1l1lll111l_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    if runner.hooks.get(bstack1l11l1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧఐ")).__name__ != bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡤࡦࡨࡤࡹࡱࡺ࡟ࡩࡱࡲ࡯ࠧ఑"):
      bstack11ll11ll11_opy_(runner, name, context, runner, bstack11l1lllll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1111ll1l1_opy_(bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩఒ")) else context.browser
      runner.driver_initialised = bstack1l11l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣఓ")
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࠢࡤࡸࡹࡸࡩࡣࡷࡷࡩ࠿ࠦࡻࡾࠩఔ").format(str(e)))
def bstack11lll1llll_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    bstack11ll11ll11_opy_(runner, name, context, context.feature, bstack11l1lllll_opy_, *args)
    try:
      if not bstack1l11ll111_opy_:
        bstack111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l1_opy_(bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬక")) else context.browser
        if is_driver_active(bstack111111ll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l11l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఖ")
          bstack1ll11lll1_opy_ = str(runner.feature.name)
          bstack11llllll1l_opy_(context, bstack1ll11lll1_opy_)
          bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭గ") + json.dumps(bstack1ll11lll1_opy_) + bstack1l11l1l_opy_ (u"ࠩࢀࢁࠬఘ"))
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪఙ").format(str(e)))
def bstack11ll1111ll_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l11l1l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭చ")) else context.feature
    bstack11ll11ll11_opy_(runner, name, context, target, bstack11l1lllll_opy_, *args)
@measure(event_name=EVENTS.bstack1lll1ll11l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1lllllll1_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    bstack11lll11l_opy_.start_test(context)
    bstack11ll11ll11_opy_(runner, name, context, context.scenario, bstack11l1lllll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111ll111_opy_.bstack1l11l11ll_opy_(context, *args)
    try:
      bstack111111ll1_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫఛ"), context.browser)
      if is_driver_active(bstack111111ll1_opy_):
        bstack111ll1lll1_opy_.bstack1ll1lll1l_opy_(bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬజ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l11l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤఝ")
        if (not bstack1l11ll111_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll11lll1_opy_ = str(runner.feature.name)
          bstack1ll11lll1_opy_ = feature_name + bstack1l11l1l_opy_ (u"ࠨࠢ࠰ࠤࠬఞ") + scenario_name
          if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦట"):
            bstack11llllll1l_opy_(context, bstack1ll11lll1_opy_)
            bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨఠ") + json.dumps(bstack1ll11lll1_opy_) + bstack1l11l1l_opy_ (u"ࠫࢂࢃࠧడ"))
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ఢ").format(str(e)))
@measure(event_name=EVENTS.bstack1l1111l111_opy_, stage=STAGE.bstack11l1llllll_opy_, hook_type=bstack1l11l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪ࡙ࡴࡦࡲࠥణ"), bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack11l1l1111l_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    bstack11ll11ll11_opy_(runner, name, context, args[0], bstack11l1lllll_opy_, *args)
    try:
      bstack111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l1_opy_(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭త")) else context.browser
      if is_driver_active(bstack111111ll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l11l1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨథ")
        bstack11lll11l_opy_.bstack1l1lll111_opy_(args[0])
        if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢద"):
          feature_name = bstack1ll11lll1_opy_ = str(runner.feature.name)
          bstack1ll11lll1_opy_ = feature_name + bstack1l11l1l_opy_ (u"ࠪࠤ࠲ࠦࠧధ") + context.scenario.name
          bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩన") + json.dumps(bstack1ll11lll1_opy_) + bstack1l11l1l_opy_ (u"ࠬࢃࡽࠨ఩"))
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪప").format(str(e)))
@measure(event_name=EVENTS.bstack1l1111l111_opy_, stage=STAGE.bstack11l1llllll_opy_, hook_type=bstack1l11l1l_opy_ (u"ࠢࡢࡨࡷࡩࡷ࡙ࡴࡦࡲࠥఫ"), bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1llll1lll_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
  bstack11lll11l_opy_.bstack1l11ll1lll_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧబ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack111111ll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l11l1l_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩభ")
        feature_name = bstack1ll11lll1_opy_ = str(runner.feature.name)
        bstack1ll11lll1_opy_ = feature_name + bstack1l11l1l_opy_ (u"ࠪࠤ࠲ࠦࠧమ") + context.scenario.name
        bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩయ") + json.dumps(bstack1ll11lll1_opy_) + bstack1l11l1l_opy_ (u"ࠬࢃࡽࠨర"))
    if str(step_status).lower() == bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ఱ"):
      bstack1llll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨల")
      bstack1lll1lll1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩళ")
      bstack11111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪఴ")
      try:
        import traceback
        bstack1llll1ll11_opy_ = runner.exception.__class__.__name__
        bstack1l1l11111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll1lll1l_opy_ = bstack1l11l1l_opy_ (u"ࠪࠤࠬవ").join(bstack1l1l11111l_opy_)
        bstack11111l1l_opy_ = bstack1l1l11111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1lllll11ll_opy_.format(str(e)))
      bstack1llll1ll11_opy_ += bstack11111l1l_opy_
      bstack11llll11l1_opy_(context, json.dumps(str(args[0].name) + bstack1l11l1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥశ") + str(bstack1lll1lll1l_opy_)),
                          bstack1l11l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦష"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦస"):
        bstack1ll1ll11l_opy_(getattr(context, bstack1l11l1l_opy_ (u"ࠧࡱࡣࡪࡩࠬహ"), None), bstack1l11l1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ఺"), bstack1llll1ll11_opy_)
        bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ఻") + json.dumps(str(args[0].name) + bstack1l11l1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ఼") + str(bstack1lll1lll1l_opy_)) + bstack1l11l1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫఽ"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥా"):
        bstack1l11l11l_opy_(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ి"), bstack1l11l1l_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦీ") + str(bstack1llll1ll11_opy_))
    else:
      bstack11llll11l1_opy_(context, bstack1l11l1l_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤు"), bstack1l11l1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢూ"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣృ"):
        bstack1ll1ll11l_opy_(getattr(context, bstack1l11l1l_opy_ (u"ࠫࡵࡧࡧࡦࠩౄ"), None), bstack1l11l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ౅"))
      bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫె") + json.dumps(str(args[0].name) + bstack1l11l1l_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦే")) + bstack1l11l1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧై"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ౉"):
        bstack1l11l11l_opy_(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥొ"))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪో").format(str(e)))
  bstack11ll11ll11_opy_(runner, name, context, args[0], bstack11l1lllll_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l1lll1l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack11ll1l1l_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
  bstack11lll11l_opy_.end_test(args[0])
  try:
    bstack1l1ll1l1ll_opy_ = args[0].status.name
    bstack111111ll1_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫౌ"), context.browser)
    bstack111ll111_opy_.bstack1ll1l111ll_opy_(bstack111111ll1_opy_)
    if str(bstack1l1ll1l1ll_opy_).lower() == bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ్࠭"):
      bstack1llll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨ౎")
      bstack1lll1lll1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩ౏")
      bstack11111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪ౐")
      try:
        import traceback
        bstack1llll1ll11_opy_ = runner.exception.__class__.__name__
        bstack1l1l11111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll1lll1l_opy_ = bstack1l11l1l_opy_ (u"ࠪࠤࠬ౑").join(bstack1l1l11111l_opy_)
        bstack11111l1l_opy_ = bstack1l1l11111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1lllll11ll_opy_.format(str(e)))
      bstack1llll1ll11_opy_ += bstack11111l1l_opy_
      bstack11llll11l1_opy_(context, json.dumps(str(args[0].name) + bstack1l11l1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ౒") + str(bstack1lll1lll1l_opy_)),
                          bstack1l11l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ౓"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ౔") or runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶౕࠧ"):
        bstack1ll1ll11l_opy_(getattr(context, bstack1l11l1l_opy_ (u"ࠨࡲࡤ࡫ࡪౖ࠭"), None), bstack1l11l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౗"), bstack1llll1ll11_opy_)
        bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨౘ") + json.dumps(str(args[0].name) + bstack1l11l1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥౙ") + str(bstack1lll1lll1l_opy_)) + bstack1l11l1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬౚ"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ౛") or runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ౜"):
        bstack1l11l11l_opy_(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨౝ"), bstack1l11l1l_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ౞") + str(bstack1llll1ll11_opy_))
    else:
      bstack11llll11l1_opy_(context, bstack1l11l1l_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦ౟"), bstack1l11l1l_opy_ (u"ࠦ࡮ࡴࡦࡰࠤౠ"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢౡ") or runner.driver_initialised == bstack1l11l1l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ౢ"):
        bstack1ll1ll11l_opy_(getattr(context, bstack1l11l1l_opy_ (u"ࠧࡱࡣࡪࡩࠬౣ"), None), bstack1l11l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ౤"))
      bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౥") + json.dumps(str(args[0].name) + bstack1l11l1l_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢ౦")) + bstack1l11l1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ౧"))
      if runner.driver_initialised == bstack1l11l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ౨") or runner.driver_initialised == bstack1l11l1l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭౩"):
        bstack1l11l11l_opy_(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౪"))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ౫").format(str(e)))
  bstack11ll11ll11_opy_(runner, name, context, context.scenario, bstack11l1lllll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l11l1ll_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l11l1l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౬")) else context.feature
    bstack11ll11ll11_opy_(runner, name, context, target, bstack11l1lllll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll1l1111l_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    try:
      bstack111111ll1_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ౭"), context.browser)
      bstack1ll111l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠫࠬ౮")
      if context.failed is True:
        bstack11lll1111l_opy_ = []
        bstack1l1ll1ll1_opy_ = []
        bstack1ll111lll1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11lll1111l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1l11111l_opy_ = traceback.format_tb(exc_tb)
            bstack1l11111111_opy_ = bstack1l11l1l_opy_ (u"ࠬࠦࠧ౯").join(bstack1l1l11111l_opy_)
            bstack1l1ll1ll1_opy_.append(bstack1l11111111_opy_)
            bstack1ll111lll1_opy_.append(bstack1l1l11111l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lllll11ll_opy_.format(str(e)))
        bstack1llll1ll11_opy_ = bstack1l11l1l_opy_ (u"࠭ࠧ౰")
        for i in range(len(bstack11lll1111l_opy_)):
          bstack1llll1ll11_opy_ += bstack11lll1111l_opy_[i] + bstack1ll111lll1_opy_[i] + bstack1l11l1l_opy_ (u"ࠧ࡝ࡰࠪ౱")
        bstack1ll111l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠨࠢࠪ౲").join(bstack1l1ll1ll1_opy_)
        if runner.driver_initialised in [bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ౳"), bstack1l11l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ౴")]:
          bstack11llll11l1_opy_(context, bstack1ll111l1ll_opy_, bstack1l11l1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ౵"))
          bstack1ll1ll11l_opy_(getattr(context, bstack1l11l1l_opy_ (u"ࠬࡶࡡࡨࡧࠪ౶"), None), bstack1l11l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౷"), bstack1llll1ll11_opy_)
          bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౸") + json.dumps(bstack1ll111l1ll_opy_) + bstack1l11l1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ౹"))
          bstack1l11l11l_opy_(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౺"), bstack1l11l1l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ౻") + str(bstack1llll1ll11_opy_))
          bstack1lll1ll1l_opy_ = bstack1llll11111_opy_(bstack1ll111l1ll_opy_, runner.feature.name, logger)
          if (bstack1lll1ll1l_opy_ != None):
            bstack111l111ll_opy_.append(bstack1lll1ll1l_opy_)
      else:
        if runner.driver_initialised in [bstack1l11l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ౼"), bstack1l11l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ౽")]:
          bstack11llll11l1_opy_(context, bstack1l11l1l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ౾") + str(runner.feature.name) + bstack1l11l1l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ౿"), bstack1l11l1l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨಀ"))
          bstack1ll1ll11l_opy_(getattr(context, bstack1l11l1l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧಁ"), None), bstack1l11l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥಂ"))
          bstack111111ll1_opy_.execute_script(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩಃ") + json.dumps(bstack1l11l1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ಄") + str(runner.feature.name) + bstack1l11l1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣಅ")) + bstack1l11l1l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ಆ"))
          bstack1l11l11l_opy_(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨಇ"))
          bstack1lll1ll1l_opy_ = bstack1llll11111_opy_(bstack1ll111l1ll_opy_, runner.feature.name, logger)
          if (bstack1lll1ll1l_opy_ != None):
            bstack111l111ll_opy_.append(bstack1lll1ll1l_opy_)
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫಈ").format(str(e)))
    bstack11ll11ll11_opy_(runner, name, context, context.feature, bstack11l1lllll_opy_, *args)
@measure(event_name=EVENTS.bstack1l1111l111_opy_, stage=STAGE.bstack11l1llllll_opy_, hook_type=bstack1l11l1l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡃ࡯ࡰࠧಉ"), bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1l111ll1_opy_(runner, name, context, bstack11l1lllll_opy_, *args):
    bstack11ll11ll11_opy_(runner, name, context, runner, bstack11l1lllll_opy_, *args)
def bstack1lll1l1ll_opy_(self, name, context, *args):
  try:
    if bstack11llllll1_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1l1l1ll1_opy_
      bstack1ll1111ll_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧಊ")][platform_index]
      os.environ[bstack1l11l1l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ಋ")] = json.dumps(bstack1ll1111ll_opy_)
    global bstack11l1lllll_opy_
    if not hasattr(self, bstack1l11l1l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫಌ")):
      self.driver_initialised = None
    bstack1l111l1lll_opy_ = {
        bstack1l11l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ಍"): bstack1l1lll111l_opy_,
        bstack1l11l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಎ"): bstack11lll1llll_opy_,
        bstack1l11l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭ಏ"): bstack11ll1111ll_opy_,
        bstack1l11l1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಐ"): bstack1lllllll1_opy_,
        bstack1l11l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩ಑"): bstack11l1l1111l_opy_,
        bstack1l11l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩಒ"): bstack1llll1lll_opy_,
        bstack1l11l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧಓ"): bstack11ll1l1l_opy_,
        bstack1l11l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪಔ"): bstack1l11l1ll_opy_,
        bstack1l11l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಕ"): bstack1ll1l1111l_opy_,
        bstack1l11l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬಖ"): bstack1l111ll1_opy_
    }
    handler = bstack1l111l1lll_opy_.get(name, bstack11l1lllll_opy_)
    try:
      handler(self, name, context, bstack11l1lllll_opy_, *args)
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩࠥ࡮࡯ࡰ࡭ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤࢀࢃ࠺ࠡࡽࢀࠫಗ").format(name, str(e)))
    if name in [bstack1l11l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫಘ"), bstack1l11l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ಙ"), bstack1l11l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩಚ")]:
      try:
        bstack111111ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l1_opy_(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ಛ")) else context.browser
        bstack1l11l111_opy_ = (
          (name == bstack1l11l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫಜ") and self.driver_initialised == bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨಝ")) or
          (name == bstack1l11l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪಞ") and self.driver_initialised == bstack1l11l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧಟ")) or
          (name == bstack1l11l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ಠ") and self.driver_initialised in [bstack1l11l1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣಡ"), bstack1l11l1l_opy_ (u"ࠢࡪࡰࡶࡸࡪࡶࠢಢ")]) or
          (name == bstack1l11l1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬಣ") and self.driver_initialised == bstack1l11l1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢತ"))
        )
        if bstack1l11l111_opy_:
          self.driver_initialised = None
          if bstack111111ll1_opy_ and hasattr(bstack111111ll1_opy_, bstack1l11l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧಥ")):
            try:
              bstack111111ll1_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l11l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡵࡺ࡯ࡴࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡪࡲࡳࡰࡀࠠࡼࡿࠪದ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡨࡰࡱ࡮ࠤࡨࡲࡥࡢࡰࡸࡴࠥ࡬࡯ࡳࠢࡾࢁ࠿ࠦࡻࡾࠩಧ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"࠭ࡃࡳ࡫ࡷ࡭ࡨࡧ࡬ࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣࡶࡺࡴࠠࡩࡱࡲ࡯ࠥࢁࡽ࠻ࠢࡾࢁࠬನ").format(name, str(e)))
    try:
      bstack11l1lllll_opy_(self, name, context, *args)
    except Exception as e2:
      logger.debug(bstack1l11l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡴࡸࡩࡨ࡫ࡱࡥࡱࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮ࠤࢀࢃ࠺ࠡࡽࢀࠫ಩").format(name, str(e2)))
def bstack1ll111l11l_opy_(config, startdir):
  return bstack1l11l1l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨಪ").format(bstack1l11l1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣಫ"))
notset = Notset()
def bstack1l11ll111l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll11ll1l_opy_
  if str(name).lower() == bstack1l11l1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪಬ"):
    return bstack1l11l1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥಭ")
  else:
    return bstack1ll11ll1l_opy_(self, name, default, skip)
def bstack1lllll1l1_opy_(item, when):
  global bstack11l1l1llll_opy_
  try:
    bstack11l1l1llll_opy_(item, when)
  except Exception as e:
    pass
def bstack1llll1ll_opy_():
  return
def bstack1lll11l1ll_opy_(type, name, status, reason, bstack11l111111l_opy_, bstack1l11111ll1_opy_):
  bstack1l11lll11_opy_ = {
    bstack1l11l1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬಮ"): type,
    bstack1l11l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಯ"): {}
  }
  if type == bstack1l11l1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩರ"):
    bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಱ")][bstack1l11l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨಲ")] = bstack11l111111l_opy_
    bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಳ")][bstack1l11l1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ಴")] = json.dumps(str(bstack1l11111ll1_opy_))
  if type == bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ವ"):
    bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಶ")][bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಷ")] = name
  if type == bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫಸ"):
    bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಹ")][bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ಺")] = status
    if status == bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ಻"):
      bstack1l11lll11_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ಼")][bstack1l11l1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ಽ")] = json.dumps(str(reason))
  bstack111l1llll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬಾ").format(json.dumps(bstack1l11lll11_opy_))
  return bstack111l1llll_opy_
def bstack111ll1ll1_opy_(driver_command, response):
    if driver_command == bstack1l11l1l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬಿ"):
        bstack111ll1lll1_opy_.bstack11l1111lll_opy_({
            bstack1l11l1l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨೀ"): response[bstack1l11l1l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩು")],
            bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫೂ"): bstack111ll1lll1_opy_.current_test_uuid()
        })
def bstack111ll111l_opy_(item, call, rep):
  global bstack1lll1111_opy_
  global bstack1ll1l11111_opy_
  global bstack1l11ll111_opy_
  name = bstack1l11l1l_opy_ (u"ࠬ࠭ೃ")
  try:
    if rep.when == bstack1l11l1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫೄ"):
      bstack11l11ll1ll_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l11ll111_opy_:
          name = str(rep.nodeid)
          bstack1lll1ll1l1_opy_ = bstack1lll11l1ll_opy_(bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ೅"), name, bstack1l11l1l_opy_ (u"ࠨࠩೆ"), bstack1l11l1l_opy_ (u"ࠩࠪೇ"), bstack1l11l1l_opy_ (u"ࠪࠫೈ"), bstack1l11l1l_opy_ (u"ࠫࠬ೉"))
          threading.current_thread().bstack1ll111111l_opy_ = name
          for driver in bstack1ll1l11111_opy_:
            if bstack11l11ll1ll_opy_ == driver.session_id:
              driver.execute_script(bstack1lll1ll1l1_opy_)
      except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬೊ").format(str(e)))
      try:
        bstack11ll111ll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l11l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧೋ"):
          status = bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧೌ") if rep.outcome.lower() == bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ್") else bstack1l11l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ೎")
          reason = bstack1l11l1l_opy_ (u"ࠪࠫ೏")
          if status == bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ೐"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ೑") if status == bstack1l11l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭೒") else bstack1l11l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭೓")
          data = name + bstack1l11l1l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ೔") if status == bstack1l11l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩೕ") else name + bstack1l11l1l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ೖ") + reason
          bstack11ll1l1l11_opy_ = bstack1lll11l1ll_opy_(bstack1l11l1l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭೗"), bstack1l11l1l_opy_ (u"ࠬ࠭೘"), bstack1l11l1l_opy_ (u"࠭ࠧ೙"), bstack1l11l1l_opy_ (u"ࠧࠨ೚"), level, data)
          for driver in bstack1ll1l11111_opy_:
            if bstack11l11ll1ll_opy_ == driver.session_id:
              driver.execute_script(bstack11ll1l1l11_opy_)
      except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ೛").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭೜").format(str(e)))
  bstack1lll1111_opy_(item, call, rep)
def bstack11l111lll1_opy_(driver, bstack1111l1ll_opy_, test=None):
  global bstack11lllllll_opy_
  if test != None:
    bstack111lll1ll_opy_ = getattr(test, bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨೝ"), None)
    bstack11l11lll11_opy_ = getattr(test, bstack1l11l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩೞ"), None)
    PercySDK.screenshot(driver, bstack1111l1ll_opy_, bstack111lll1ll_opy_=bstack111lll1ll_opy_, bstack11l11lll11_opy_=bstack11l11lll11_opy_, bstack11l1lllll1_opy_=bstack11lllllll_opy_)
  else:
    PercySDK.screenshot(driver, bstack1111l1ll_opy_)
@measure(event_name=EVENTS.bstack111ll1ll1l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll11111l1_opy_(driver):
  if bstack1lllllll11_opy_.bstack1ll111l11_opy_() is True or bstack1lllllll11_opy_.capturing() is True:
    return
  bstack1lllllll11_opy_.bstack11lll11ll1_opy_()
  while not bstack1lllllll11_opy_.bstack1ll111l11_opy_():
    bstack1lll1lll11_opy_ = bstack1lllllll11_opy_.bstack11ll1l11l1_opy_()
    bstack11l111lll1_opy_(driver, bstack1lll1lll11_opy_)
  bstack1lllllll11_opy_.bstack1l111l111_opy_()
def bstack111ll11l1_opy_(sequence, driver_command, response = None, bstack1ll11lllll_opy_ = None, args = None):
    try:
      if sequence != bstack1l11l1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ೟"):
        return
      if percy.bstack111ll11ll_opy_() == bstack1l11l1l_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧೠ"):
        return
      bstack1lll1lll11_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪೡ"), None)
      for command in bstack1l1ll111ll_opy_:
        if command == driver_command:
          with bstack1ll1l111_opy_:
            bstack111l1111l_opy_ = bstack1ll1l11111_opy_.copy()
          for driver in bstack111l1111l_opy_:
            bstack1ll11111l1_opy_(driver)
      bstack1111l111l_opy_ = percy.bstack1ll111l1l_opy_()
      if driver_command in bstack11l1l1ll_opy_[bstack1111l111l_opy_]:
        bstack1lllllll11_opy_.bstack1l1lllll_opy_(bstack1lll1lll11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1ll1111111_opy_(framework_name):
  if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬೢ")):
      return
  bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ೣ"), True)
  global bstack1ll1ll1l1_opy_
  global bstack11l111l1ll_opy_
  global bstack1ll1lll111_opy_
  bstack1ll1ll1l1_opy_ = framework_name
  logger.info(bstack11llll1lll_opy_.format(bstack1ll1ll1l1_opy_.split(bstack1l11l1l_opy_ (u"ࠪ࠱ࠬ೤"))[0]))
  bstack1lll1l11ll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11llllll1_opy_:
      Service.start = bstack11ll1l1l1_opy_
      Service.stop = bstack1l11l111l1_opy_
      webdriver.Remote.get = bstack111lllll11_opy_
      WebDriver.quit = bstack1l11l1lll1_opy_
      webdriver.Remote.__init__ = bstack1ll11l11_opy_
    if not bstack11llllll1_opy_:
        webdriver.Remote.__init__ = bstack1ll111ll1_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1l1lll1lll_opy_
    bstack11l111l1ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11llllll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11l1l1l1l1_opy_
  except Exception as e:
    pass
  bstack11l11111ll_opy_()
  if not bstack11l111l1ll_opy_:
    bstack1lll111l1_opy_(bstack1l11l1l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ೥"), bstack11lllll11_opy_)
  if bstack111ll1lll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭೦")) and callable(getattr(RemoteConnection, bstack1l11l1l_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ೧"))):
        RemoteConnection._get_proxy_url = bstack11l111l1l1_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack11l111l1l1_opy_
    except Exception as e:
      logger.error(bstack1l1111l11l_opy_.format(str(e)))
  if bstack1ll1l1l1l_opy_():
    bstack11111111_opy_(CONFIG, logger)
  if (bstack1l11l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೨") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack111ll11ll_opy_() == bstack1l11l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ೩"):
          bstack111lll1l_opy_(bstack111ll11l1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1l11lll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1ll11111_opy_
      except Exception as e:
        logger.warning(bstack1l1111111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1ll11ll11_opy_
      except Exception as e:
        logger.debug(bstack1ll11l11l1_opy_ + str(e))
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1l1111111l_opy_)
    Output.start_test = bstack1lll11111l_opy_
    Output.end_test = bstack1l11l111l_opy_
    TestStatus.__init__ = bstack11l1ll11_opy_
    QueueItem.__init__ = bstack11llllll11_opy_
    pabot._create_items = bstack111ll11l_opy_
    try:
      from pabot import __version__ as bstack11ll1lll1l_opy_
      if version.parse(bstack11ll1lll1l_opy_) >= version.parse(bstack1l11l1l_opy_ (u"ࠩ࠸࠲࠵࠴࠰ࠨ೪")):
        pabot._run = bstack111ll1ll_opy_
      elif version.parse(bstack11ll1lll1l_opy_) >= version.parse(bstack1l11l1l_opy_ (u"ࠪ࠸࠳࠸࠮࠱ࠩ೫")):
        pabot._run = bstack11l11l1ll1_opy_
      elif version.parse(bstack11ll1lll1l_opy_) >= version.parse(bstack1l11l1l_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫ೬")):
        pabot._run = bstack1l1l1l11l1_opy_
      elif version.parse(bstack11ll1lll1l_opy_) >= version.parse(bstack1l11l1l_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ೭")):
        pabot._run = bstack11l1l1l111_opy_
      else:
        pabot._run = bstack1ll11l1l1_opy_
    except Exception as e:
      pabot._run = bstack1ll11l1l1_opy_
    pabot._create_command_for_execution = bstack1llll11l_opy_
    pabot._report_results = bstack1lll1ll1_opy_
  if bstack1l11l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭೮") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1ll111ll_opy_)
    Runner.run_hook = bstack1lll1l1ll_opy_
    Step.run = bstack1ll11lll_opy_
  if bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ೯") in str(framework_name).lower():
    if not bstack11llllll1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll111l11l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1llll1ll_opy_
      Config.getoption = bstack1l11ll111l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111ll111l_opy_
    except Exception as e:
      pass
def bstack1l111l1l1_opy_():
  global CONFIG
  if bstack1l11l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ೰") in CONFIG and int(CONFIG[bstack1l11l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩೱ")]) > 1:
    logger.warning(bstack11l111l1l_opy_)
def bstack1l11l1l1ll_opy_(arg, bstack1l1lllllll_opy_, bstack111lll11_opy_=None):
  global CONFIG
  global bstack1l1llll111_opy_
  global bstack1l11l1l111_opy_
  global bstack11llllll1_opy_
  global bstack11llllll_opy_
  bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೲ")
  if bstack1l1lllllll_opy_ and isinstance(bstack1l1lllllll_opy_, str):
    bstack1l1lllllll_opy_ = eval(bstack1l1lllllll_opy_)
  CONFIG = bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫೳ")]
  bstack1l1llll111_opy_ = bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭೴")]
  bstack1l11l1l111_opy_ = bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ೵")]
  bstack11llllll1_opy_ = bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ೶")]
  bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ೷"), bstack11llllll1_opy_)
  os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೸")] = bstack1l1111lll_opy_
  os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ೹")] = json.dumps(CONFIG)
  os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ೺")] = bstack1l1llll111_opy_
  os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭೻")] = str(bstack1l11l1l111_opy_)
  os.environ[bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ೼")] = str(True)
  if bstack1ll111l111_opy_(arg, [bstack1l11l1l_opy_ (u"ࠧ࠮ࡰࠪ೽"), bstack1l11l1l_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ೾")]) != -1:
    os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ೿")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11ll11l1l1_opy_)
    return
  bstack1l1llllll_opy_()
  global bstack1l1l1111_opy_
  global bstack11lllllll_opy_
  global bstack1llllll11_opy_
  global bstack1l11l1lll_opy_
  global bstack1l1ll1lll_opy_
  global bstack1ll1lll111_opy_
  global bstack11ll1ll1l1_opy_
  arg.append(bstack1l11l1l_opy_ (u"ࠥ࠱࡜ࠨഀ"))
  arg.append(bstack1l11l1l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢഁ"))
  arg.append(bstack1l11l1l_opy_ (u"ࠧ࠳ࡗࠣം"))
  arg.append(bstack1l11l1l_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧഃ"))
  global bstack11lllll111_opy_
  global bstack111l1111_opy_
  global bstack11lll1ll11_opy_
  global bstack11ll1ll1ll_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll1ll1l1l_opy_
  global bstack111l111l1_opy_
  global bstack1l1ll1111_opy_
  global bstack1llll1l11_opy_
  global bstack1l1lllll1_opy_
  global bstack1ll11ll1l_opy_
  global bstack11l1l1llll_opy_
  global bstack1lll1111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11lllll111_opy_ = webdriver.Remote.__init__
    bstack111l1111_opy_ = WebDriver.quit
    bstack1l1ll1111_opy_ = WebDriver.close
    bstack1llll1l11_opy_ = WebDriver.get
    bstack11lll1ll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack11l1111ll1_opy_(CONFIG) and bstack111l111l_opy_():
    if bstack1ll1l1ll11_opy_() < version.parse(bstack1l11lll1ll_opy_):
      logger.error(bstack11lll1lll1_opy_.format(bstack1ll1l1ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨഄ")) and callable(getattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩഅ"))):
          bstack1l1lllll1_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1lllll1_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack1l1111l11l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll11ll1l_opy_ = Config.getoption
    from _pytest import runner
    bstack11l1l1llll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1l11l1l_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤആ"), bstack1lll111111_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack1lll1111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l11l1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫഇ"))
  bstack1llllll11_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨഈ"), {}).get(bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧഉ"))
  bstack11ll1ll1l1_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1ll1llll1_opy_():
      bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.CONNECT, bstack11l1l111_opy_())
    platform_index = int(os.environ.get(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ഊ"), bstack1l11l1l_opy_ (u"ࠧ࠱ࠩഋ")))
  else:
    bstack1ll1111111_opy_(bstack11ll1ll11_opy_)
  os.environ[bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩഌ")] = CONFIG[bstack1l11l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ഍")]
  os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭എ")] = CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഏ")]
  os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨഐ")] = bstack11llllll1_opy_.__str__()
  from _pytest.config import main as bstack11l11lll1_opy_
  bstack1l11ll11ll_opy_ = []
  try:
    exit_code = bstack11l11lll1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack111llll1_opy_()
    if bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ഑") in multiprocessing.current_process().__dict__.keys():
      for bstack11ll11111l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11ll11ll_opy_.append(bstack11ll11111l_opy_)
    try:
      bstack11l11l1ll_opy_ = (bstack1l11ll11ll_opy_, int(exit_code))
      bstack111lll11_opy_.append(bstack11l11l1ll_opy_)
    except:
      bstack111lll11_opy_.append((bstack1l11ll11ll_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11ll11ll_opy_.append({bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬഒ"): bstack1l11l1l_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪഓ") + os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩഔ")), bstack1l11l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩക"): traceback.format_exc(), bstack1l11l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഖ"): int(os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬഗ")))})
    bstack111lll11_opy_.append((bstack1l11ll11ll_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l11l1l_opy_ (u"ࠨࡲࡦࡶࡵ࡭ࡪࡹࠢഘ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll1l11l_opy_ = e.__class__.__name__
    print(bstack1l11l1l_opy_ (u"ࠢࠦࡵ࠽ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡧ࡫ࡨࡢࡸࡨࠤࡹ࡫ࡳࡵࠢࠨࡷࠧങ") % (bstack1ll1l11l_opy_, e))
    return 1
def bstack1l11llll1_opy_(arg):
  global bstack1ll11l11l_opy_
  bstack1ll1111111_opy_(bstack1llllll1l_opy_)
  os.environ[bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩച")] = str(bstack1l11l1l111_opy_)
  retries = bstack111lll111l_opy_.bstack1l1l1ll1ll_opy_(CONFIG)
  status_code = 0
  if bstack111lll111l_opy_.bstack1l11lll11l_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1l1l1l11_opy_
    status_code = bstack1l1l1l11_opy_(arg)
  if status_code != 0:
    bstack1ll11l11l_opy_ = status_code
def bstack11lll1ll1l_opy_():
  logger.info(bstack1lll11ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l11l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨഛ"), help=bstack1l11l1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫജ"))
  parser.add_argument(bstack1l11l1l_opy_ (u"ࠫ࠲ࡻࠧഝ"), bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩഞ"), help=bstack1l11l1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬട"))
  parser.add_argument(bstack1l11l1l_opy_ (u"ࠧ࠮࡭ࠪഠ"), bstack1l11l1l_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧഡ"), help=bstack1l11l1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪഢ"))
  parser.add_argument(bstack1l11l1l_opy_ (u"ࠪ࠱࡫࠭ണ"), bstack1l11l1l_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩത"), help=bstack1l11l1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഥ"))
  bstack1llll1lll1_opy_ = parser.parse_args()
  try:
    bstack1l1l1l1l1l_opy_ = bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪദ")
    if bstack1llll1lll1_opy_.framework and bstack1llll1lll1_opy_.framework not in (bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧധ"), bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩന")):
      bstack1l1l1l1l1l_opy_ = bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨഩ")
    bstack1l1llllll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1l1l1l_opy_)
    bstack1ll1l1l1ll_opy_ = open(bstack1l1llllll1_opy_, bstack1l11l1l_opy_ (u"ࠪࡶࠬപ"))
    bstack11ll111l_opy_ = bstack1ll1l1l1ll_opy_.read()
    bstack1ll1l1l1ll_opy_.close()
    if bstack1llll1lll1_opy_.username:
      bstack11ll111l_opy_ = bstack11ll111l_opy_.replace(bstack1l11l1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫഫ"), bstack1llll1lll1_opy_.username)
    if bstack1llll1lll1_opy_.key:
      bstack11ll111l_opy_ = bstack11ll111l_opy_.replace(bstack1l11l1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧബ"), bstack1llll1lll1_opy_.key)
    if bstack1llll1lll1_opy_.framework:
      bstack11ll111l_opy_ = bstack11ll111l_opy_.replace(bstack1l11l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧഭ"), bstack1llll1lll1_opy_.framework)
    file_name = bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪമ")
    file_path = os.path.abspath(file_name)
    bstack1111111l1_opy_ = open(file_path, bstack1l11l1l_opy_ (u"ࠨࡹࠪയ"))
    bstack1111111l1_opy_.write(bstack11ll111l_opy_)
    bstack1111111l1_opy_.close()
    logger.info(bstack111l1lll1_opy_)
    try:
      os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫര")] = bstack1llll1lll1_opy_.framework if bstack1llll1lll1_opy_.framework != None else bstack1l11l1l_opy_ (u"ࠥࠦറ")
      config = yaml.safe_load(bstack11ll111l_opy_)
      config[bstack1l11l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫല")] = bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫള")
      bstack11l11l11ll_opy_(bstack1l1l1111l1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111ll11l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l1l111l1_opy_.format(str(e)))
def bstack11l11l11ll_opy_(bstack11l1111l_opy_, config, bstack1l1111111_opy_={}):
  global bstack11llllll1_opy_
  global bstack1111llll1_opy_
  global bstack11llllll_opy_
  if not config:
    return
  bstack11lllll1l1_opy_ = bstack1lll1111ll_opy_ if not bstack11llllll1_opy_ else (
    bstack1l1l11l11l_opy_ if bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࠪഴ") in config else (
        bstack1l1l11ll_opy_ if config.get(bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫവ")) else bstack1l1ll1ll_opy_
    )
)
  bstack11l1ll1ll1_opy_ = False
  bstack11l1111l1l_opy_ = False
  if bstack11llllll1_opy_ is True:
      if bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࠬശ") in config:
          bstack11l1ll1ll1_opy_ = True
      else:
          bstack11l1111l1l_opy_ = True
  bstack11lll1ll1_opy_ = bstack1l11l1l1_opy_.bstack1ll11lll1l_opy_(config, bstack1111llll1_opy_)
  bstack11l1l11111_opy_ = bstack11lll11lll_opy_()
  data = {
    bstack1l11l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഷ"): config[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬസ")],
    bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഹ"): config[bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨഺ")],
    bstack1l11l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ഻ࠪ"): bstack11l1111l_opy_,
    bstack1l11l1l_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮഼ࠫ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪഽ"), bstack1111llll1_opy_),
    bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫാ"): bstack1lllll11l_opy_,
    bstack1l11l1l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬി"): bstack1ll1ll1l11_opy_(),
    bstack1l11l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧീ"): {
      bstack1l11l1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪു"): str(config[bstack1l11l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ൂ")]) if bstack1l11l1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧൃ") in config else bstack1l11l1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤൄ"),
      bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ൅"): sys.version,
      bstack1l11l1l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬെ"): bstack1ll1l1l111_opy_(os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭േ"), bstack1111llll1_opy_)),
      bstack1l11l1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧൈ"): bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൉"),
      bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨൊ"): bstack11lllll1l1_opy_,
      bstack1l11l1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ോ"): bstack11lll1ll1_opy_,
      bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨൌ"): os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ്")],
      bstack1l11l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧൎ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൏"), bstack1111llll1_opy_),
      bstack1l11l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ൐"): bstack1lll111l_opy_(os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ൑"), bstack1111llll1_opy_)),
      bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ൒"): bstack11l1l11111_opy_.get(bstack1l11l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ൓")),
      bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩൔ"): bstack11l1l11111_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬൕ")),
      bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨൖ"): config[bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൗ")] if config[bstack1l11l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ൘")] else bstack1l11l1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ൙"),
      bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൚"): str(config[bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ൛")]) if bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭൜") in config else bstack1l11l1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ൝"),
      bstack1l11l1l_opy_ (u"࠭࡯ࡴࠩ൞"): sys.platform,
      bstack1l11l1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩൟ"): socket.gethostname(),
      bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪൠ"): bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫൡ"))
    }
  }
  if not bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪൢ")) is None:
    data[bstack1l11l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൣ")][bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ൤")] = {
      bstack1l11l1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭൥"): bstack1l11l1l_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ൦"),
      bstack1l11l1l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ൧"): bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ൨")),
      bstack1l11l1l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩ൩"): bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ൪"))
    }
  if bstack11l1111l_opy_ == bstack1ll111l1l1_opy_:
    data[bstack1l11l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ൫")][bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫ൬")] = bstack11l1l1111_opy_(config)
    data[bstack1l11l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൭")][bstack1l11l1l_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭൮")] = percy.bstack1l111l11l_opy_
    data[bstack1l11l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ൯")][bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩ൰")] = percy.percy_build_id
  if not bstack111lll111l_opy_.bstack11ll11ll_opy_(CONFIG):
    data[bstack1l11l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ൱")][bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ൲")] = bstack111lll111l_opy_.bstack11ll11ll_opy_(CONFIG)
  bstack1lll11ll1_opy_ = bstack1111lll1_opy_.bstack1llll1111_opy_(CONFIG, logger)
  bstack1lll11lll1_opy_ = bstack111lll111l_opy_.bstack1llll1111_opy_(config=CONFIG)
  if bstack1lll11ll1_opy_ is not None and bstack1lll11lll1_opy_ is not None and bstack1lll11lll1_opy_.bstack11l1l1ll11_opy_():
    data[bstack1l11l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൳")][bstack1lll11lll1_opy_.bstack11ll11l1_opy_()] = bstack1lll11ll1_opy_.bstack1l1ll11l_opy_()
  update(data[bstack1l11l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൴")], bstack1l1111111_opy_)
  try:
    response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠨࡒࡒࡗ࡙࠭൵"), bstack11lllll11l_opy_(bstack11ll11l111_opy_), data, {
      bstack1l11l1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ൶"): (config[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ൷")], config[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൸")])
    })
    if response:
      logger.debug(bstack1llll1l11l_opy_.format(bstack11l1111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l111lll_opy_.format(str(e)))
def bstack1ll1l1l111_opy_(framework):
  return bstack1l11l1l_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ൹").format(str(framework), __version__) if framework else bstack1l11l1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢൺ").format(
    __version__)
def bstack1l1llllll_opy_():
  global CONFIG
  global bstack11ll1l1lll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1llll11_opy_()
    logger.debug(bstack1lll1l11l1_opy_.format(str(CONFIG)))
    bstack11ll1l1lll_opy_ = bstack11lllll1_opy_.configure_logger(CONFIG, bstack11ll1l1lll_opy_)
    bstack1lll1l11ll_opy_()
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦൻ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111l1l11_opy_
  atexit.register(bstack1lllll111_opy_)
  signal.signal(signal.SIGINT, bstack11l1lll11_opy_)
  signal.signal(signal.SIGTERM, bstack11l1lll11_opy_)
def bstack111l1l11_opy_(exctype, value, traceback):
  global bstack1ll1l11111_opy_
  try:
    for driver in bstack1ll1l11111_opy_:
      bstack1l11l11l_opy_(driver, bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨർ"), bstack1l11l1l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧൽ") + str(value))
  except Exception:
    pass
  logger.info(bstack1111l1ll1_opy_)
  bstack111lll1lll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111lll1lll_opy_(message=bstack1l11l1l_opy_ (u"ࠪࠫൾ"), bstack111111l11_opy_ = False):
  global CONFIG
  bstack1111l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ൿ") if bstack111111l11_opy_ else bstack1l11l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ඀")
  try:
    if message:
      bstack1l1111111_opy_ = {
        bstack1111l1l11_opy_ : str(message)
      }
      bstack11l11l11ll_opy_(bstack1ll111l1l1_opy_, CONFIG, bstack1l1111111_opy_)
    else:
      bstack11l11l11ll_opy_(bstack1ll111l1l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1111lll11_opy_.format(str(e)))
def bstack1ll111llll_opy_(bstack1lllll11_opy_, size):
  bstack11l111l111_opy_ = []
  while len(bstack1lllll11_opy_) > size:
    bstack1l1l1llll_opy_ = bstack1lllll11_opy_[:size]
    bstack11l111l111_opy_.append(bstack1l1l1llll_opy_)
    bstack1lllll11_opy_ = bstack1lllll11_opy_[size:]
  bstack11l111l111_opy_.append(bstack1lllll11_opy_)
  return bstack11l111l111_opy_
def bstack1l11lllll1_opy_(args):
  if bstack1l11l1l_opy_ (u"࠭࠭࡮ࠩඁ") in args and bstack1l11l1l_opy_ (u"ࠧࡱࡦࡥࠫං") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1111111ll_opy_, stage=STAGE.bstack11l1l1lll1_opy_)
def run_on_browserstack(bstack11ll11llll_opy_=None, bstack111lll11_opy_=None, bstack1l11l1l11l_opy_=False):
  global CONFIG
  global bstack1l1llll111_opy_
  global bstack1l11l1l111_opy_
  global bstack1111llll1_opy_
  global bstack11llllll_opy_
  bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩඃ")
  bstack1lll1l1ll1_opy_(bstack1l1l1lll1_opy_, logger)
  if bstack11ll11llll_opy_ and isinstance(bstack11ll11llll_opy_, str):
    bstack11ll11llll_opy_ = eval(bstack11ll11llll_opy_)
  if bstack11ll11llll_opy_:
    CONFIG = bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ඄")]
    bstack1l1llll111_opy_ = bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫඅ")]
    bstack1l11l1l111_opy_ = bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ආ")]
    bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧඇ"), bstack1l11l1l111_opy_)
    bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඈ")
  bstack11llllll_opy_.bstack11ll1l111l_opy_(bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩඉ"), uuid4().__str__())
  logger.info(bstack1l11l1l_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭ඊ") + bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫඋ")));
  logger.debug(bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭ඌ") + bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ඍ")))
  if not bstack1l11l1l11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11ll11l1l1_opy_)
      return
    if sys.argv[1] == bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨඎ") or sys.argv[1] == bstack1l11l1l_opy_ (u"࠭࠭ࡷࠩඏ"):
      logger.info(bstack1l11l1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧඐ").format(__version__))
      return
    if sys.argv[1] == bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧඑ"):
      bstack11lll1ll1l_opy_()
      return
  args = sys.argv
  bstack1l1llllll_opy_()
  global bstack1l1l1111_opy_
  global bstack1l1l1ll1_opy_
  global bstack11ll1ll1l1_opy_
  global bstack1l1ll11ll1_opy_
  global bstack11lllllll_opy_
  global bstack1llllll11_opy_
  global bstack1l11l1lll_opy_
  global bstack1ll1llll11_opy_
  global bstack1l1ll1lll_opy_
  global bstack1ll1lll111_opy_
  global bstack1l111llll1_opy_
  bstack1l1l1ll1_opy_ = len(CONFIG.get(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬඒ"), []))
  if not bstack1l1111lll_opy_:
    if args[1] == bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඓ") or args[1] == bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬඔ"):
      bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬඕ")
      args = args[2:]
    elif args[1] == bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඖ"):
      bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭඗")
      args = args[2:]
    elif args[1] == bstack1l11l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ඘"):
      bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ඙")
      args = args[2:]
    elif args[1] == bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫක"):
      bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬඛ")
      args = args[2:]
    elif args[1] == bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬග"):
      bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඝ")
      args = args[2:]
    elif args[1] == bstack1l11l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඞ"):
      bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨඟ")
      args = args[2:]
    else:
      if not bstack1l11l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬච") in CONFIG or str(CONFIG[bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඡ")]).lower() in [bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫජ"), bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ඣ")]:
        bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඤ")
        args = args[1:]
      elif str(CONFIG[bstack1l11l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඥ")]).lower() == bstack1l11l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧඦ"):
        bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨට")
        args = args[1:]
      elif str(CONFIG[bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඨ")]).lower() == bstack1l11l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪඩ"):
        bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫඪ")
        args = args[1:]
      elif str(CONFIG[bstack1l11l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩණ")]).lower() == bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧඬ"):
        bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨත")
        args = args[1:]
      elif str(CONFIG[bstack1l11l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬථ")]).lower() == bstack1l11l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪද"):
        bstack1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫධ")
        args = args[1:]
      else:
        os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧන")] = bstack1l1111lll_opy_
        bstack1lllll1lll_opy_(bstack1ll1l1ll1l_opy_)
  os.environ[bstack1l11l1l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ඲")] = bstack1l1111lll_opy_
  bstack1111llll1_opy_ = bstack1l1111lll_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l1l111l_opy_ = bstack11l111111_opy_[bstack1l11l1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫඳ")] if bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨප") and bstack1111ll11_opy_() else bstack1l1111lll_opy_
      bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.bstack11l1ll111_opy_, bstack1ll11llll1_opy_(
        sdk_version=__version__,
        path_config=bstack111ll1l1l_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1l111l_opy_,
        frameworks=[bstack1l1l111l_opy_],
        framework_versions={
          bstack1l1l111l_opy_: bstack1lll111l_opy_(bstack1l11l1l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨඵ") if bstack1l1111lll_opy_ in [bstack1l11l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩබ"), bstack1l11l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪභ"), bstack1l11l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ම")] else bstack1l1111lll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣඹ"), None):
        CONFIG[bstack1l11l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤය")] = cli.config.get(bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥර"), None)
    except Exception as e:
      bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.bstack1l1111llll_opy_, e.__traceback__, 1)
    if bstack1l11l1l111_opy_:
      CONFIG[bstack1l11l1l_opy_ (u"ࠤࡤࡴࡵࠨ඼")] = cli.config[bstack1l11l1l_opy_ (u"ࠥࡥࡵࡶࠢල")]
      logger.info(bstack1lll1l1111_opy_.format(CONFIG[bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࠨ඾")]))
  else:
    bstack1llll1l1l_opy_.clear()
  global bstack1ll1ll1l_opy_
  global bstack1ll1lllll1_opy_
  if bstack11ll11llll_opy_:
    try:
      bstack11l11llll1_opy_ = datetime.datetime.now()
      os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ඿")] = bstack1l1111lll_opy_
      bstack11l11l11ll_opy_(bstack111lll1l1_opy_, CONFIG)
      cli.bstack1lll11lll_opy_(bstack1l11l1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤව"), datetime.datetime.now() - bstack11l11llll1_opy_)
    except Exception as e:
      logger.debug(bstack11l111ll1l_opy_.format(str(e)))
  global bstack11lllll111_opy_
  global bstack111l1111_opy_
  global bstack11ll11l1ll_opy_
  global bstack1l11lll111_opy_
  global bstack111l1l111_opy_
  global bstack1l1ll11ll_opy_
  global bstack11ll1ll1ll_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll1ll111_opy_
  global bstack1ll1ll1l1l_opy_
  global bstack111l111l1_opy_
  global bstack1l1ll1111_opy_
  global bstack11l1lllll_opy_
  global bstack11l111ll_opy_
  global bstack1llll1l11_opy_
  global bstack1l1lllll1_opy_
  global bstack1ll11ll1l_opy_
  global bstack11l1l1llll_opy_
  global bstack1l1l1lll_opy_
  global bstack1lll1111_opy_
  global bstack11lll1ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11lllll111_opy_ = webdriver.Remote.__init__
    bstack111l1111_opy_ = WebDriver.quit
    bstack1l1ll1111_opy_ = WebDriver.close
    bstack1llll1l11_opy_ = WebDriver.get
    bstack11lll1ll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1ll1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l1l111111_opy_
    bstack1ll1lllll1_opy_ = bstack1l1l111111_opy_()
  except Exception as e:
    pass
  try:
    global bstack11lll11111_opy_
    from QWeb.keywords import browser
    bstack11lll11111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack11l1111ll1_opy_(CONFIG) and bstack111l111l_opy_():
    if bstack1ll1l1ll11_opy_() < version.parse(bstack1l11lll1ll_opy_):
      logger.error(bstack11lll1lll1_opy_.format(bstack1ll1l1ll11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨශ")) and callable(getattr(RemoteConnection, bstack1l11l1l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩෂ"))):
          RemoteConnection._get_proxy_url = bstack11l111l1l1_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack11l111l1l1_opy_
      except Exception as e:
        logger.error(bstack1l1111l11l_opy_.format(str(e)))
  if not CONFIG.get(bstack1l11l1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫස"), False) and not bstack11ll11llll_opy_:
    logger.info(bstack11l11l111l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧහ") in CONFIG and str(CONFIG[bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨළ")]).lower() != bstack1l11l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫෆ"):
      bstack11lll1ll_opy_()
    elif bstack1l1111lll_opy_ != bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෇") or (bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෈") and not bstack11ll11llll_opy_):
      bstack11lllll1l_opy_()
  if (bstack1l1111lll_opy_ in [bstack1l11l1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ෉"), bstack1l11l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ්"), bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෋")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1l11lll1_opy_
        bstack1l1ll11ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warning(bstack1l1111111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack111l1l111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll11l11l1_opy_ + str(e))
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1l1111111l_opy_)
    if bstack1l1111lll_opy_ != bstack1l11l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෌"):
      bstack11ll1llll1_opy_()
    bstack11ll11l1ll_opy_ = Output.start_test
    bstack1l11lll111_opy_ = Output.end_test
    bstack11ll1ll1ll_opy_ = TestStatus.__init__
    bstack1ll1ll111_opy_ = pabot._run
    bstack1ll1ll1l1l_opy_ = QueueItem.__init__
    bstack111l111l1_opy_ = pabot._create_command_for_execution
    bstack1l1l1lll_opy_ = pabot._report_results
  if bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෍"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1ll111ll_opy_)
    bstack11l1lllll_opy_ = Runner.run_hook
    bstack11l111ll_opy_ = Step.run
  if bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෎"):
    try:
      from _pytest.config import Config
      bstack1ll11ll1l_opy_ = Config.getoption
      from _pytest import runner
      bstack11l1l1llll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1l11l1l_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢා"), bstack1lll111111_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack1lll1111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩැ"))
    if bstack1ll1l11l1_opy_():
      logger.warning(bstack1lll1l1lll_opy_[bstack1l11l1l_opy_ (u"ࠩࡖࡈࡐ࠳ࡇࡆࡐ࠰࠴࠵࠻ࠧෑ")])
  try:
    framework_name = bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩි") if bstack1l1111lll_opy_ in [bstack1l11l1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪී"), bstack1l11l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫු"), bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ෕")] else bstack1l1llll1l_opy_(bstack1l1111lll_opy_)
    bstack1l1l1ll1l_opy_ = {
      bstack1l11l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨූ"): bstack1l11l1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ෗") if bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩෘ") and bstack1111ll11_opy_() else framework_name,
      bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧෙ"): bstack1lll111l_opy_(framework_name),
      bstack1l11l1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩේ"): __version__,
      bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ෛ"): bstack1l1111lll_opy_
    }
    if bstack1l1111lll_opy_ in bstack1l1l11ll11_opy_ + bstack1l11l11l1l_opy_:
      if bstack1ll1l11lll_opy_.bstack1ll1ll1lll_opy_(CONFIG):
        if bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ො") in CONFIG:
          os.environ[bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨෝ")] = os.getenv(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩෞ"), json.dumps(CONFIG[bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩෟ")]))
          CONFIG[bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ෠")].pop(bstack1l11l1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ෡"), None)
          CONFIG[bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ෢")].pop(bstack1l11l1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ෣"), None)
        bstack1l1l1ll1l_opy_[bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ෤")] = {
          bstack1l11l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭෥"): bstack1l11l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ෦"),
          bstack1l11l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ෧"): str(bstack1ll1l1ll11_opy_())
        }
    if bstack1l1111lll_opy_ not in [bstack1l11l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෨")] and not cli.is_running():
      bstack1ll1ll11_opy_, bstack1l11lll1l_opy_ = bstack111ll1lll1_opy_.launch(CONFIG, bstack1l1l1ll1l_opy_)
      if bstack1l11lll1l_opy_.get(bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ෩")) is not None and bstack1ll1l11lll_opy_.bstack1lll11llll_opy_(CONFIG) is None:
        value = bstack1l11lll1l_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෪")].get(bstack1l11l1l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ෫"))
        if value is not None:
            CONFIG[bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ෬")] = value
        else:
          logger.debug(bstack1l11l1l_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡡࡵࡣࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ෭"))
  except Exception as e:
    logger.debug(bstack1llll111l1_opy_.format(bstack1l11l1l_opy_ (u"ࠪࡘࡪࡹࡴࡉࡷࡥࠫ෮"), str(e)))
  if bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ෯"):
    bstack11ll1ll1l1_opy_ = True
    if bstack11ll11llll_opy_ and bstack1l11l1l11l_opy_:
      bstack1llllll11_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ෰"), {}).get(bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෱"))
      bstack1ll1111111_opy_(bstack1l1l1l111_opy_)
    elif bstack11ll11llll_opy_:
      bstack1llllll11_opy_ = CONFIG.get(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫෲ"), {}).get(bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪෳ"))
      global bstack1ll1l11111_opy_
      try:
        if bstack1l11lllll1_opy_(bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෴")]) and multiprocessing.current_process().name == bstack1l11l1l_opy_ (u"ࠪ࠴ࠬ෵"):
          bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෶")].remove(bstack1l11l1l_opy_ (u"ࠬ࠳࡭ࠨ෷"))
          bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෸")].remove(bstack1l11l1l_opy_ (u"ࠧࡱࡦࡥࠫ෹"))
          bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෺")] = bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෻")][0]
          with open(bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෼")], bstack1l11l1l_opy_ (u"ࠫࡷ࠭෽")) as f:
            bstack1l1ll1llll_opy_ = f.read()
          bstack11l1111ll_opy_ = bstack1l11l1l_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨࡪ࡬ࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠫࡷࡪࡲࡦ࠭ࠢࡤࡶ࡬࠲ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡁࠥ࠶ࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࠢࡀࠤࡸࡺࡲࠩ࡫ࡱࡸ࠭ࡧࡲࡨࠫ࠮࠵࠵࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣ෾").format(str(bstack11ll11llll_opy_))
          bstack1l11llll_opy_ = bstack11l1111ll_opy_ + bstack1l1ll1llll_opy_
          bstack11l111l11_opy_ = bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෿")] + bstack1l11l1l_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩ฀")
          with open(bstack11l111l11_opy_, bstack1l11l1l_opy_ (u"ࠨࡹࠪก")):
            pass
          with open(bstack11l111l11_opy_, bstack1l11l1l_opy_ (u"ࠤࡺ࠯ࠧข")) as f:
            f.write(bstack1l11llll_opy_)
          import subprocess
          bstack1111ll111_opy_ = subprocess.run([bstack1l11l1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥฃ"), bstack11l111l11_opy_])
          if os.path.exists(bstack11l111l11_opy_):
            os.unlink(bstack11l111l11_opy_)
          os._exit(bstack1111ll111_opy_.returncode)
        else:
          if bstack1l11lllll1_opy_(bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧค")]):
            bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨฅ")].remove(bstack1l11l1l_opy_ (u"࠭࠭࡮ࠩฆ"))
            bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪง")].remove(bstack1l11l1l_opy_ (u"ࠨࡲࡧࡦࠬจ"))
            bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฉ")] = bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ช")][0]
          bstack1ll1111111_opy_(bstack1l1l1l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧซ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l11l1l_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧฌ")] = bstack1l11l1l_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨญ")
          mod_globals[bstack1l11l1l_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩฎ")] = os.path.abspath(bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฏ")])
          exec(open(bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฐ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l11l1l_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪฑ").format(str(e)))
          for driver in bstack1ll1l11111_opy_:
            bstack111lll11_opy_.append({
              bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩฒ"): bstack11ll11llll_opy_[bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨณ")],
              bstack1l11l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬด"): str(e),
              bstack1l11l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ต"): multiprocessing.current_process().name
            })
            bstack1l11l11l_opy_(driver, bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨถ"), bstack1l11l1l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧท") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1l11111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l11l1l111_opy_, CONFIG, logger)
      bstack111ll1111_opy_()
      bstack1l111l1l1_opy_()
      percy.bstack1ll11l1l1l_opy_()
      bstack1l1lllllll_opy_ = {
        bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ธ"): args[0],
        bstack1l11l1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫน"): CONFIG,
        bstack1l11l1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭บ"): bstack1l1llll111_opy_,
        bstack1l11l1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨป"): bstack1l11l1l111_opy_
      }
      if bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪผ") in CONFIG:
        bstack111lll1l1l_opy_ = bstack11llll1ll_opy_(args, logger, CONFIG, bstack11llllll1_opy_, bstack1l1l1ll1_opy_)
        bstack1ll1llll11_opy_ = bstack111lll1l1l_opy_.bstack1l1lllll1l_opy_(run_on_browserstack, bstack1l1lllllll_opy_, bstack1l11lllll1_opy_(args))
      else:
        if bstack1l11lllll1_opy_(args):
          bstack1l1lllllll_opy_[bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฝ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1lllllll_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll1111111_opy_(bstack1l1l1l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l11l1l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫพ")] = bstack1l11l1l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬฟ")
          mod_globals[bstack1l11l1l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ภ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫม") or bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬย"):
    percy.init(bstack1l11l1l111_opy_, CONFIG, logger)
    percy.bstack1ll11l1l1l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1l1111111l_opy_)
    bstack111ll1111_opy_()
    bstack1ll1111111_opy_(bstack111111ll_opy_)
    if bstack11llllll1_opy_:
      bstack1ll11111ll_opy_(bstack111111ll_opy_, args)
      if bstack1l11l1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬร") in args:
        i = args.index(bstack1l11l1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ฤ"))
        args.pop(i)
        args.pop(i)
      if bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬล") not in CONFIG:
        CONFIG[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฦ")] = [{}]
        bstack1l1l1ll1_opy_ = 1
      if bstack1l1l1111_opy_ == 0:
        bstack1l1l1111_opy_ = 1
      args.insert(0, str(bstack1l1l1111_opy_))
      args.insert(0, str(bstack1l11l1l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩว")))
    if bstack111ll1lll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11l1l11l11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11l111ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l11l1l_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧศ"),
        ).parse_args(bstack11l1l11l11_opy_)
        bstack1lllllll1l_opy_ = args.index(bstack11l1l11l11_opy_[0]) if len(bstack11l1l11l11_opy_) > 0 else len(args)
        args.insert(bstack1lllllll1l_opy_, str(bstack1l11l1l_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪษ")))
        args.insert(bstack1lllllll1l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫส"))))
        if bstack111lll111l_opy_.bstack1l11lll11l_opy_(CONFIG):
          args.insert(bstack1lllllll1l_opy_, str(bstack1l11l1l_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬห")))
          args.insert(bstack1lllllll1l_opy_ + 1, str(bstack1l11l1l_opy_ (u"ࠩࡕࡩࡹࡸࡹࡇࡣ࡬ࡰࡪࡪ࠺ࡼࡿࠪฬ").format(bstack111lll111l_opy_.bstack1l1l1ll1ll_opy_(CONFIG))))
        if bstack11lll1l1l_opy_(os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨอ"))) and str(os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨฮ"), bstack1l11l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪฯ"))) != bstack1l11l1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫะ"):
          for bstack11ll1ll111_opy_ in bstack11l111ll1_opy_:
            args.remove(bstack11ll1ll111_opy_)
          test_files = os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫั")).split(bstack1l11l1l_opy_ (u"ࠨ࠮ࠪา"))
          for bstack1l1l1l1l11_opy_ in test_files:
            args.append(bstack1l1l1l1l11_opy_)
      except Exception as e:
        logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡾࢁ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࡼࡿࠥำ").format(bstack11l1lll1l_opy_, e))
    pabot.main(args)
  elif bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫิ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1l1111111l_opy_)
    for a in args:
      if bstack1l11l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪี") in a:
        bstack11lllllll_opy_ = int(a.split(bstack1l11l1l_opy_ (u"ࠬࡀࠧึ"))[1])
      if bstack1l11l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪื") in a:
        bstack1llllll11_opy_ = str(a.split(bstack1l11l1l_opy_ (u"ࠧ࠻ุࠩ"))[1])
      if bstack1l11l1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨู") in a:
        bstack1l11l1lll_opy_ = str(a.split(bstack1l11l1l_opy_ (u"ࠩ࠽ฺࠫ"))[1])
    bstack1l11lll1_opy_ = None
    bstack1lllll1ll1_opy_ = None
    if bstack1l11l1l_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ฻") in args:
      i = args.index(bstack1l11l1l_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪ฼"))
      args.pop(i)
      bstack1l11lll1_opy_ = args.pop(i)
    if bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ฽") in args:
      i = args.index(bstack1l11l1l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠩ฾"))
      args.pop(i)
      bstack1lllll1ll1_opy_ = args.pop(i)
    if bstack1l11lll1_opy_ is not None:
      global bstack11l11ll1_opy_
      bstack11l11ll1_opy_ = bstack1l11lll1_opy_
    if bstack1lllll1ll1_opy_ is not None and int(bstack11lllllll_opy_) < 0:
      bstack11lllllll_opy_ = int(bstack1lllll1ll1_opy_)
    bstack1ll1111111_opy_(bstack111111ll_opy_)
    run_cli(args)
    if bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ฿") in multiprocessing.current_process().__dict__.keys():
      for bstack11ll11111l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111lll11_opy_.append(bstack11ll11111l_opy_)
  elif bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨเ"):
    bstack1ll11ll11l_opy_ = bstack1lll1l11_opy_(args, logger, CONFIG, bstack11llllll1_opy_)
    bstack1ll11ll11l_opy_.bstack11l1lll1ll_opy_()
    bstack111ll1111_opy_()
    bstack1l1ll11ll1_opy_ = True
    bstack1ll1lll111_opy_ = bstack1ll11ll11l_opy_.bstack1ll11l1l11_opy_()
    bstack1ll11ll11l_opy_.bstack1l1lllllll_opy_(bstack1l11ll111_opy_)
    bstack1ll11ll11l_opy_.bstack1111ll1ll_opy_()
    bstack11l1ll1l11_opy_(bstack1l1111lll_opy_, CONFIG, bstack1ll11ll11l_opy_.bstack111lll1ll1_opy_())
    bstack1l1l1ll11l_opy_ = bstack1ll11ll11l_opy_.bstack1l1lllll1l_opy_(bstack1l11l1l1ll_opy_, {
      bstack1l11l1l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪแ"): bstack1l1llll111_opy_,
      bstack1l11l1l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬโ"): bstack1l11l1l111_opy_,
      bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧใ"): bstack11llllll1_opy_
    })
    try:
      bstack1l11ll11ll_opy_, bstack11lll111_opy_ = map(list, zip(*bstack1l1l1ll11l_opy_))
      bstack1l1ll1lll_opy_ = bstack1l11ll11ll_opy_[0]
      for status_code in bstack11lll111_opy_:
        if status_code != 0:
          bstack1l111llll1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥไ").format(str(e)))
  elif bstack1l1111lll_opy_ == bstack1l11l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ๅ"):
    try:
      from behave.__main__ import main as bstack1l1l1l11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll111l1_opy_(e, bstack1ll111ll_opy_)
    bstack111ll1111_opy_()
    bstack1l1ll11ll1_opy_ = True
    bstack11l111l1_opy_ = 1
    if bstack1l11l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧๆ") in CONFIG:
      bstack11l111l1_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ็")]
    if bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ่ࠬ") in CONFIG:
      bstack1111l11ll_opy_ = int(bstack11l111l1_opy_) * int(len(CONFIG[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ้࠭")]))
    else:
      bstack1111l11ll_opy_ = int(bstack11l111l1_opy_)
    config = Configuration(args)
    bstack11lllll1ll_opy_ = config.paths
    if len(bstack11lllll1ll_opy_) == 0:
      import glob
      pattern = bstack1l11l1l_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧ๊ࠪ")
      bstack11ll1lll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll1lll11_opy_)
      config = Configuration(args)
      bstack11lllll1ll_opy_ = config.paths
    bstack1l11ll1ll1_opy_ = [os.path.normpath(item) for item in bstack11lllll1ll_opy_]
    bstack1lll11l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack11l1l1l1ll_opy_ = [item for item in bstack1lll11l1l_opy_ if item not in bstack1l11ll1ll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l11l1l_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ๋࠭"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11ll1ll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll1llll1l_opy_)))
                    for bstack1ll1llll1l_opy_ in bstack1l11ll1ll1_opy_]
    bstack111lllll1l_opy_ = []
    for spec in bstack1l11ll1ll1_opy_:
      bstack111111l1_opy_ = []
      bstack111111l1_opy_ += bstack11l1l1l1ll_opy_
      bstack111111l1_opy_.append(spec)
      bstack111lllll1l_opy_.append(bstack111111l1_opy_)
    execution_items = []
    for bstack111111l1_opy_ in bstack111lllll1l_opy_:
      if bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ์") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪํ")]):
          item = {}
          item[bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࠬ๎")] = bstack1l11l1l_opy_ (u"ࠩࠣࠫ๏").join(bstack111111l1_opy_)
          item[bstack1l11l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ๐")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l11l1l_opy_ (u"ࠫࡦࡸࡧࠨ๑")] = bstack1l11l1l_opy_ (u"ࠬࠦࠧ๒").join(bstack111111l1_opy_)
        item[bstack1l11l1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ๓")] = 0
        execution_items.append(item)
    bstack111lllll1_opy_ = bstack1ll111llll_opy_(execution_items, bstack1111l11ll_opy_)
    for execution_item in bstack111lllll1_opy_:
      bstack1111llll_opy_ = []
      for item in execution_item:
        bstack1111llll_opy_.append(bstack11l1ll11l_opy_(name=str(item[bstack1l11l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭๔")]),
                                             target=bstack1l11llll1_opy_,
                                             args=(item[bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࠬ๕")],)))
      for t in bstack1111llll_opy_:
        t.start()
      for t in bstack1111llll_opy_:
        t.join()
  else:
    bstack1lllll1lll_opy_(bstack1ll1l1ll1l_opy_)
  if not bstack11ll11llll_opy_:
    bstack11ll111l1_opy_()
    if(bstack1l1111lll_opy_ in [bstack1l11l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ๖"), bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ๗")]):
      bstack1llllll1ll_opy_()
  bstack11lllll1_opy_.bstack1l111l1l1l_opy_()
def browserstack_initialize(bstack1l1lll1111_opy_=None):
  logger.info(bstack1l11l1l_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧ๘") + str(bstack1l1lll1111_opy_))
  run_on_browserstack(bstack1l1lll1111_opy_, None, True)
@measure(event_name=EVENTS.bstack1l11l1l11_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack11ll111l1_opy_():
  global CONFIG
  global bstack1111llll1_opy_
  global bstack1l111llll1_opy_
  global bstack1ll11l11l_opy_
  global bstack11llllll_opy_
  bstack111lll1l11_opy_.bstack11llll1l_opy_()
  if cli.is_running():
    bstack1llll1l1l_opy_.invoke(bstack1l11ll1l1_opy_.bstack1111l1l1l_opy_)
  else:
    bstack1lll11lll1_opy_ = bstack111lll111l_opy_.bstack1llll1111_opy_(config=CONFIG)
    bstack1lll11lll1_opy_.bstack11l11l1111_opy_(CONFIG)
  if bstack1111llll1_opy_ == bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ๙"):
    if not cli.is_enabled(CONFIG):
      bstack111ll1lll1_opy_.stop()
  else:
    bstack111ll1lll1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1l1l1lllll_opy_.bstack11llll1111_opy_()
  if bstack1l11l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ๚") in CONFIG and str(CONFIG[bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ๛")]).lower() != bstack1l11l1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ๜"):
    hashed_id, bstack1l1lll1l_opy_ = bstack11lll11ll_opy_()
  else:
    hashed_id, bstack1l1lll1l_opy_ = get_build_link()
  bstack11ll1ll1l_opy_(hashed_id)
  logger.info(bstack1l11l1l_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ࠪ๝") + bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ๞"), bstack1l11l1l_opy_ (u"ࠫࠬ๟")) + bstack1l11l1l_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾ࠥ࠭๠") + os.getenv(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ๡"), bstack1l11l1l_opy_ (u"ࠧࠨ๢")))
  if hashed_id is not None and bstack11l1ll11l1_opy_() != -1:
    sessions = bstack1l111l11l1_opy_(hashed_id)
    bstack11l11l1l_opy_(sessions, bstack1l1lll1l_opy_)
  if bstack1111llll1_opy_ == bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ๣") and bstack1l111llll1_opy_ != 0:
    sys.exit(bstack1l111llll1_opy_)
  if bstack1111llll1_opy_ == bstack1l11l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ๤") and bstack1ll11l11l_opy_ != 0:
    sys.exit(bstack1ll11l11l_opy_)
def bstack11ll1ll1l_opy_(new_id):
    global bstack1lllll11l_opy_
    bstack1lllll11l_opy_ = new_id
def bstack1l1llll1l_opy_(bstack1l1l11l1ll_opy_):
  if bstack1l1l11l1ll_opy_:
    return bstack1l1l11l1ll_opy_.capitalize()
  else:
    return bstack1l11l1l_opy_ (u"ࠪࠫ๥")
@measure(event_name=EVENTS.bstack1l111l1ll1_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack11l1ll111l_opy_(bstack111111111_opy_):
  if bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ๦") in bstack111111111_opy_ and bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๧")] != bstack1l11l1l_opy_ (u"࠭ࠧ๨"):
    return bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๩")]
  else:
    bstack1l1l111lll_opy_ = bstack1l11l1l_opy_ (u"ࠣࠤ๪")
    if bstack1l11l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ๫") in bstack111111111_opy_ and bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๬")] != None:
      bstack1l1l111lll_opy_ += bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๭")] + bstack1l11l1l_opy_ (u"ࠧ࠲ࠠࠣ๮")
      if bstack111111111_opy_[bstack1l11l1l_opy_ (u"࠭࡯ࡴࠩ๯")] == bstack1l11l1l_opy_ (u"ࠢࡪࡱࡶࠦ๰"):
        bstack1l1l111lll_opy_ += bstack1l11l1l_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ๱")
      bstack1l1l111lll_opy_ += (bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๲")] or bstack1l11l1l_opy_ (u"ࠪࠫ๳"))
      return bstack1l1l111lll_opy_
    else:
      bstack1l1l111lll_opy_ += bstack1l1llll1l_opy_(bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ๴")]) + bstack1l11l1l_opy_ (u"ࠧࠦࠢ๵") + (
              bstack111111111_opy_[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๶")] or bstack1l11l1l_opy_ (u"ࠧࠨ๷")) + bstack1l11l1l_opy_ (u"ࠣ࠮ࠣࠦ๸")
      if bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠩࡲࡷࠬ๹")] == bstack1l11l1l_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ๺"):
        bstack1l1l111lll_opy_ += bstack1l11l1l_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ๻")
      bstack1l1l111lll_opy_ += bstack111111111_opy_[bstack1l11l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๼")] or bstack1l11l1l_opy_ (u"࠭ࠧ๽")
      return bstack1l1l111lll_opy_
@measure(event_name=EVENTS.bstack11l1l11lll_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack1ll1l1ll1_opy_(bstack1l11ll11l1_opy_):
  if bstack1l11ll11l1_opy_ == bstack1l11l1l_opy_ (u"ࠢࡥࡱࡱࡩࠧ๾"):
    return bstack1l11l1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๿")
  elif bstack1l11ll11l1_opy_ == bstack1l11l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ຀"):
    return bstack1l11l1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ກ")
  elif bstack1l11ll11l1_opy_ == bstack1l11l1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦຂ"):
    return bstack1l11l1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ຃")
  elif bstack1l11ll11l1_opy_ == bstack1l11l1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧຄ"):
    return bstack1l11l1l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ຅")
  elif bstack1l11ll11l1_opy_ == bstack1l11l1l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤຆ"):
    return bstack1l11l1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧງ")
  elif bstack1l11ll11l1_opy_ == bstack1l11l1l_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦຈ"):
    return bstack1l11l1l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬຉ")
  else:
    return bstack1l11l1l_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩຊ") + bstack1l1llll1l_opy_(
      bstack1l11ll11l1_opy_) + bstack1l11l1l_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ຋")
def bstack1l111111ll_opy_(session):
  return bstack1l11l1l_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧຌ").format(
    session[bstack1l11l1l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬຍ")], bstack11l1ll111l_opy_(session), bstack1ll1l1ll1_opy_(session[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨຎ")]),
    bstack1ll1l1ll1_opy_(session[bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຏ")]),
    bstack1l1llll1l_opy_(session[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬຐ")] or session[bstack1l11l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬຑ")] or bstack1l11l1l_opy_ (u"࠭ࠧຒ")) + bstack1l11l1l_opy_ (u"ࠢࠡࠤຓ") + (session[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪດ")] or bstack1l11l1l_opy_ (u"ࠩࠪຕ")),
    session[bstack1l11l1l_opy_ (u"ࠪࡳࡸ࠭ຖ")] + bstack1l11l1l_opy_ (u"ࠦࠥࠨທ") + session[bstack1l11l1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩຘ")], session[bstack1l11l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨນ")] or bstack1l11l1l_opy_ (u"ࠧࠨບ"),
    session[bstack1l11l1l_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬປ")] if session[bstack1l11l1l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ຜ")] else bstack1l11l1l_opy_ (u"ࠪࠫຝ"))
@measure(event_name=EVENTS.bstack1l1lll11_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def bstack11l11l1l_opy_(sessions, bstack1l1lll1l_opy_):
  try:
    bstack111ll1ll11_opy_ = bstack1l11l1l_opy_ (u"ࠦࠧພ")
    if not os.path.exists(bstack1l111111l_opy_):
      os.mkdir(bstack1l111111l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l1l_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪຟ")), bstack1l11l1l_opy_ (u"࠭ࡲࠨຠ")) as f:
      bstack111ll1ll11_opy_ = f.read()
    bstack111ll1ll11_opy_ = bstack111ll1ll11_opy_.replace(bstack1l11l1l_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫມ"), str(len(sessions)))
    bstack111ll1ll11_opy_ = bstack111ll1ll11_opy_.replace(bstack1l11l1l_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨຢ"), bstack1l1lll1l_opy_)
    bstack111ll1ll11_opy_ = bstack111ll1ll11_opy_.replace(bstack1l11l1l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪຣ"),
                                              sessions[0].get(bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧ຤")) if sessions[0] else bstack1l11l1l_opy_ (u"ࠫࠬລ"))
    with open(os.path.join(bstack1l111111l_opy_, bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ຦")), bstack1l11l1l_opy_ (u"࠭ࡷࠨວ")) as stream:
      stream.write(bstack111ll1ll11_opy_.split(bstack1l11l1l_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫຨ"))[0])
      for session in sessions:
        stream.write(bstack1l111111ll_opy_(session))
      stream.write(bstack111ll1ll11_opy_.split(bstack1l11l1l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬຩ"))[1])
    logger.info(bstack1l11l1l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬສ").format(bstack1l111111l_opy_));
  except Exception as e:
    logger.debug(bstack1llll1l1_opy_.format(str(e)))
def bstack1l111l11l1_opy_(hashed_id):
  global CONFIG
  try:
    bstack11l11llll1_opy_ = datetime.datetime.now()
    host = bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪຫ") if bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࠨຬ") in CONFIG else bstack1l11l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ອ")
    user = CONFIG[bstack1l11l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨຮ")]
    key = CONFIG[bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪຯ")]
    bstack1l1l1ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧະ") if bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵ࠭ັ") in CONFIG else (bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧາ") if CONFIG.get(bstack1l11l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨຳ")) else bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧິ"))
    host = bstack11l11l1l1l_opy_(cli.config, [bstack1l11l1l_opy_ (u"ࠨࡡࡱ࡫ࡶࠦີ"), bstack1l11l1l_opy_ (u"ࠢࡢࡲࡳࡅࡺࡺ࡯࡮ࡣࡷࡩࠧຶ"), bstack1l11l1l_opy_ (u"ࠣࡣࡳ࡭ࠧື")], host) if bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵຸ࠭") in CONFIG else bstack11l11l1l1l_opy_(cli.config, [bstack1l11l1l_opy_ (u"ࠥࡥࡵ࡯ࡳູࠣ"), bstack1l11l1l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ຺"), bstack1l11l1l_opy_ (u"ࠧࡧࡰࡪࠤົ")], host)
    url = bstack1l11l1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨຼ").format(host, bstack1l1l1ll1l1_opy_, hashed_id)
    headers = {
      bstack1l11l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ຽ"): bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ຾"),
    }
    proxies = bstack1l1111lll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack1lll11lll_opy_(bstack1l11l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦ຿"), datetime.datetime.now() - bstack11l11llll1_opy_)
      return list(map(lambda session: session[bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨເ")], response.json()))
  except Exception as e:
    logger.debug(bstack11111111l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1lllllllll_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def get_build_link():
  global CONFIG
  global bstack1lllll11l_opy_
  try:
    if bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧແ") in CONFIG:
      bstack11l11llll1_opy_ = datetime.datetime.now()
      host = bstack1l11l1l_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨໂ") if bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࠪໃ") in CONFIG else bstack1l11l1l_opy_ (u"ࠧࡢࡲ࡬ࠫໄ")
      user = CONFIG[bstack1l11l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ໅")]
      key = CONFIG[bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬໆ")]
      bstack1l1l1ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ໇") if bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࠨ່") in CONFIG else bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫້ࠧ")
      url = bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ໊࠭").format(user, key, host, bstack1l1l1ll1l1_opy_)
      if cli.is_enabled(CONFIG):
        bstack1l1lll1l_opy_, hashed_id = cli.bstack11l1l11l1l_opy_()
        logger.info(bstack11ll1l11l_opy_.format(bstack1l1lll1l_opy_))
        return [hashed_id, bstack1l1lll1l_opy_]
      else:
        headers = {
          bstack1l11l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ໋࠭"): bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ໌"),
        }
        if bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫໍ") in CONFIG:
          params = {bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ໎"): CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ໏")], bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ໐"): CONFIG[bstack1l11l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ໑")]}
        else:
          params = {bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ໒"): CONFIG[bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ໓")]}
        proxies = bstack1l1111lll1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l11l111ll_opy_ = response.json()[0][bstack1l11l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ໔")]
          if bstack1l11l111ll_opy_:
            bstack1l1lll1l_opy_ = bstack1l11l111ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ໕")].split(bstack1l11l1l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ໖"))[0] + bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭໗") + bstack1l11l111ll_opy_[
              bstack1l11l1l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ໘")]
            logger.info(bstack11ll1l11l_opy_.format(bstack1l1lll1l_opy_))
            bstack1lllll11l_opy_ = bstack1l11l111ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ໙")]
            bstack111l1ll1l_opy_ = CONFIG[bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ໚")]
            if bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ໛") in CONFIG:
              bstack111l1ll1l_opy_ += bstack1l11l1l_opy_ (u"ࠪࠤࠬໜ") + CONFIG[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ໝ")]
            if bstack111l1ll1l_opy_ != bstack1l11l111ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪໞ")]:
              logger.debug(bstack1lll1l1l1l_opy_.format(bstack1l11l111ll_opy_[bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫໟ")], bstack111l1ll1l_opy_))
            cli.bstack1lll11lll_opy_(bstack1l11l1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨ໠"), datetime.datetime.now() - bstack11l11llll1_opy_)
            return [bstack1l11l111ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ໡")], bstack1l1lll1l_opy_]
    else:
      logger.warning(bstack1lll11l11_opy_)
  except Exception as e:
    logger.debug(bstack11l1111111_opy_.format(str(e)))
  return [None, None]
def bstack111ll1l1ll_opy_(url, bstack111l11l1l_opy_=False):
  global CONFIG
  global bstack11l11l111_opy_
  if not bstack11l11l111_opy_:
    hostname = bstack111llll1l1_opy_(url)
    is_private = bstack1ll1ll1ll_opy_(hostname)
    if (bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭໢") in CONFIG and not bstack11lll1l1l_opy_(CONFIG[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ໣")])) and (is_private or bstack111l11l1l_opy_):
      bstack11l11l111_opy_ = hostname
def bstack111llll1l1_opy_(url):
  return urlparse(url).hostname
def bstack1ll1ll1ll_opy_(hostname):
  for bstack111l1l1ll_opy_ in bstack1ll1l1l1_opy_:
    regex = re.compile(bstack111l1l1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1111ll1l1_opy_(bstack1llll11l11_opy_):
  return True if bstack1llll11l11_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack111llll11l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11lllllll_opy_
  bstack1l111111l1_opy_ = not (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ໤"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ໥"), None))
  bstack1ll1lll1ll_opy_ = getattr(driver, bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭໦"), None) != True
  bstack11l11llll_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ໧"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ໨"), None)
  if bstack11l11llll_opy_:
    if not bstack111llll111_opy_():
      logger.warning(bstack1l11l1l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ໩"))
      return {}
    logger.debug(bstack1l11l1l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ໪"))
    logger.debug(perform_scan(driver, driver_command=bstack1l11l1l_opy_ (u"ࠫࡪࡾࡥࡤࡷࡷࡩࡘࡩࡲࡪࡲࡷࠫ໫")))
    results = bstack1l1l1l11l_opy_(bstack1l11l1l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ໬"))
    if results is not None and results.get(bstack1l11l1l_opy_ (u"ࠨࡩࡴࡵࡸࡩࡸࠨ໭")) is not None:
        return results[bstack1l11l1l_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ໮")]
    logger.error(bstack1l11l1l_opy_ (u"ࠣࡐࡲࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡗ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥ໯"))
    return []
  if not bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack11lllllll_opy_) or (bstack1ll1lll1ll_opy_ and bstack1l111111l1_opy_):
    logger.warning(bstack1l11l1l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ໰"))
    return {}
  try:
    logger.debug(bstack1l11l1l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ໱"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l111lll_opy_.bstack1llll1ll1_opy_)
    return results
  except Exception:
    logger.error(bstack1l11l1l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨ໲"))
    return {}
@measure(event_name=EVENTS.bstack1ll111lll_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11lllllll_opy_
  bstack1l111111l1_opy_ = not (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ໳"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ໴"), None))
  bstack1ll1lll1ll_opy_ = getattr(driver, bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ໵"), None) != True
  bstack11l11llll_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ໶"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ໷"), None)
  if bstack11l11llll_opy_:
    if not bstack111llll111_opy_():
      logger.warning(bstack1l11l1l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ໸"))
      return {}
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩ໹"))
    logger.debug(perform_scan(driver, driver_command=bstack1l11l1l_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ໺")))
    results = bstack1l1l1l11l_opy_(bstack1l11l1l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨ໻"))
    if results is not None and results.get(bstack1l11l1l_opy_ (u"ࠢࡴࡷࡰࡱࡦࡸࡹࠣ໼")) is not None:
        return results[bstack1l11l1l_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤ໽")]
    logger.error(bstack1l11l1l_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡓࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ໾"))
    return {}
  if not bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack11lllllll_opy_) or (bstack1ll1lll1ll_opy_ and bstack1l111111l1_opy_):
    logger.warning(bstack1l11l1l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠴ࠢ໿"))
    return {}
  try:
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺࠩༀ"))
    logger.debug(perform_scan(driver))
    bstack1lllll1l1l_opy_ = driver.execute_async_script(bstack1l111lll_opy_.bstack1ll1l1l11_opy_)
    return bstack1lllll1l1l_opy_
  except Exception:
    logger.error(bstack1l11l1l_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡸࡱࡲࡧࡲࡺࠢࡺࡥࡸࠦࡦࡰࡷࡱࡨ࠳ࠨ༁"))
    return {}
def bstack111llll111_opy_():
  global CONFIG
  global bstack11lllllll_opy_
  bstack1lll1ll111_opy_ = bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༂"), None) and bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༃"), None)
  if not bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack11lllllll_opy_) or not bstack1lll1ll111_opy_:
        logger.warning(bstack1l11l1l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ༄"))
        return False
  return True
def bstack1l1l1l11l_opy_(result_type):
    bstack1llll111_opy_ = bstack111ll1lll1_opy_.current_test_uuid() if bstack111ll1lll1_opy_.current_test_uuid() else bstack1l1l1lllll_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack1l11111ll_opy_(bstack1llll111_opy_, result_type))
        try:
            return future.result(timeout=bstack11ll1111_opy_)
        except TimeoutError:
            logger.error(bstack1l11l1l_opy_ (u"ࠤࡗ࡭ࡲ࡫࡯ࡶࡶࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࡸࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡓࡧࡶࡹࡱࡺࡳࠣ༅").format(bstack11ll1111_opy_))
        except Exception as ex:
            logger.debug(bstack1l11l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡵࡩࡹࡸࡩࡦࡸ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣ༆").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11l11l11l_opy_, stage=STAGE.bstack11l1llllll_opy_, bstack1l1l111lll_opy_=bstack1lll1l11l_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11lllllll_opy_
  bstack1l111111l1_opy_ = not (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ༇"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ༈"), None))
  bstack11111lll_opy_ = not (bstack1ll1ll11ll_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༉"), None) and bstack1ll1ll11ll_opy_(
          threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༊"), None))
  bstack1ll1lll1ll_opy_ = getattr(driver, bstack1l11l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ་"), None) != True
  if not bstack1ll1l11lll_opy_.bstack1ll111l1_opy_(CONFIG, bstack11lllllll_opy_) or (bstack1ll1lll1ll_opy_ and bstack1l111111l1_opy_ and bstack11111lll_opy_):
    logger.warning(bstack1l11l1l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡸࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠦ༌"))
    return {}
  try:
    bstack11l11ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠪࡥࡵࡶࠧ།") in CONFIG and CONFIG.get(bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࠨ༎"), bstack1l11l1l_opy_ (u"ࠬ࠭༏"))
    session_id = getattr(driver, bstack1l11l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ༐"), None)
    if not session_id:
      logger.warning(bstack1l11l1l_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡨࡷ࡯ࡶࡦࡴࠥ༑"))
      return {bstack1l11l1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ༒"): bstack1l11l1l_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡩࡳࡺࡴࡤࠣ༓")}
    if bstack11l11ll1l_opy_:
      try:
        bstack1ll11l1111_opy_ = {
              bstack1l11l1l_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧ༔"): os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ༕"), os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ༖"), bstack1l11l1l_opy_ (u"࠭ࠧ༗"))),
              bstack1l11l1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪ༘ࠧ"): bstack111ll1lll1_opy_.current_test_uuid() if bstack111ll1lll1_opy_.current_test_uuid() else bstack1l1l1lllll_opy_.current_hook_uuid(),
              bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶ༙ࠬ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ༚")),
              bstack1l11l1l_opy_ (u"ࠪࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ༛"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l11l1l_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ༜"): os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ༝"), bstack1l11l1l_opy_ (u"࠭ࠧ༞")),
              bstack1l11l1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ༟"): kwargs.get(bstack1l11l1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩ༠"), None) or bstack1l11l1l_opy_ (u"ࠩࠪ༡")
          }
        if not hasattr(thread_local, bstack1l11l1l_opy_ (u"ࠪࡦࡦࡹࡥࡠࡣࡳࡴࡤࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࠪ༢")):
            scripts = {bstack1l11l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ༣"): bstack1l111lll_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack111ll1llll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack111ll1llll_opy_[bstack1l11l1l_opy_ (u"ࠬࡹࡣࡢࡰࠪ༤")] = bstack111ll1llll_opy_[bstack1l11l1l_opy_ (u"࠭ࡳࡤࡣࡱࠫ༥")] % json.dumps(bstack1ll11l1111_opy_)
        bstack1l111lll_opy_.bstack11llll11_opy_(bstack111ll1llll_opy_)
        bstack1l111lll_opy_.store()
        bstack1l1ll11l1l_opy_ = driver.execute_script(bstack1l111lll_opy_.perform_scan)
      except Exception as bstack1ll1lll11l_opy_:
        logger.info(bstack1l11l1l_opy_ (u"ࠢࡂࡲࡳ࡭ࡺࡳࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠢ༦") + str(bstack1ll1lll11l_opy_))
        bstack1l1ll11l1l_opy_ = {bstack1l11l1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ༧"): str(bstack1ll1lll11l_opy_)}
    else:
      bstack1l1ll11l1l_opy_ = driver.execute_async_script(bstack1l111lll_opy_.perform_scan, {bstack1l11l1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ༨"): kwargs.get(bstack1l11l1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡧࡴࡳ࡭ࡢࡰࡧࠫ༩"), None) or bstack1l11l1l_opy_ (u"ࠫࠬ༪")})
    return bstack1l1ll11l1l_opy_
  except Exception as err:
    logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰ࠱ࠤࢀࢃࠢ༫").format(str(err)))
    return {}