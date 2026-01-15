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
import inspect
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack111ll1ll_opy_ import bstack1l111l11l_opy_
from browserstack_sdk.bstack1lll11ll1_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE, bstack11lll11ll1_opy_
from bstack_utils.messages import bstack11ll1lll1_opy_, bstack1ll11l1l11_opy_, bstack1l1111111_opy_, bstack11l11l11ll_opy_, bstack1llll1l1l1_opy_, bstack1ll1llll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
from bstack_utils.helper import bstack111lll1l1l_opy_
from browserstack_sdk.bstack1lll111lll_opy_ import bstack11l11ll1l_opy_
logger = get_logger(__name__)
def bstack11l11ll111_opy_():
  global CONFIG
  headers = {
        bstack1l111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l111l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack111lll1l1l_opy_(CONFIG, bstack11lll11ll1_opy_)
  try:
    response = requests.get(bstack11lll11ll1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11ll1l11ll_opy_ = response.json()[bstack1l111l1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack11ll1lll1_opy_.format(response.json()))
      return bstack11ll1l11ll_opy_
    else:
      logger.debug(bstack1ll11l1l11_opy_.format(bstack1l111l1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1ll11l1l11_opy_.format(e))
def bstack11ll111l11_opy_(hub_url):
  global CONFIG
  url = bstack1l111l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l111l1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l111l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l111l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack111lll1l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1111111_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l11l11ll_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack1l111111l_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack1l1111lll1_opy_():
  try:
    global bstack1l1l1l11l1_opy_
    global CONFIG
    if bstack1l111l1_opy_ (u"ࠫ࡭ࡻࡢࡓࡧࡪ࡭ࡴࡴࠧࡾ") in CONFIG and CONFIG[bstack1l111l1_opy_ (u"ࠬ࡮ࡵࡣࡔࡨ࡫࡮ࡵ࡮ࠨࡿ")]:
      from bstack_utils.constants import bstack111l1lll1_opy_
      bstack111ll1111_opy_ = CONFIG[bstack1l111l1_opy_ (u"࠭ࡨࡶࡤࡕࡩ࡬࡯࡯࡯ࠩࢀ")]
      if bstack111ll1111_opy_ in bstack111l1lll1_opy_:
        bstack1l1l1l11l1_opy_ = bstack111l1lll1_opy_[bstack111ll1111_opy_]
        logger.debug(bstack1llll1l1l1_opy_.format(bstack1l1l1l11l1_opy_))
        return
      else:
        logger.debug(bstack1l111l1_opy_ (u"ࠢࡉࡷࡥࠤࡰ࡫ࡹࠡࠩࡾࢁࠬࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡎࡕࡃࡡࡘࡖࡑࡥࡍࡂࡒ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥࠤࡩ࡫ࡴࡦࡥࡷ࡭ࡴࡴࠢࢁ").format(bstack111ll1111_opy_))
    bstack11ll1l11ll_opy_ = bstack11l11ll111_opy_()
    bstack1l11l1l1_opy_ = []
    results = []
    for bstack1lll1ll11l_opy_ in bstack11ll1l11ll_opy_:
      bstack1l11l1l1_opy_.append(bstack11l11ll1l_opy_(target=bstack11ll111l11_opy_,args=(bstack1lll1ll11l_opy_,)))
    for t in bstack1l11l1l1_opy_:
      t.start()
    for t in bstack1l11l1l1_opy_:
      results.append(t.join())
    bstack1ll1l1ll_opy_ = {}
    for item in results:
      hub_url = item[bstack1l111l1_opy_ (u"ࠨࡪࡸࡦࡤࡻࡲ࡭ࠩࢂ")]
      latency = item[bstack1l111l1_opy_ (u"ࠩ࡯ࡥࡹ࡫࡮ࡤࡻࠪࢃ")]
      bstack1ll1l1ll_opy_[hub_url] = latency
    bstack1l111l11ll_opy_ = min(bstack1ll1l1ll_opy_, key= lambda x: bstack1ll1l1ll_opy_[x])
    bstack1l1l1l11l1_opy_ = bstack1l111l11ll_opy_
    logger.debug(bstack1llll1l1l1_opy_.format(bstack1l111l11ll_opy_))
  except Exception as e:
    logger.debug(bstack1ll1llll_opy_.format(e))
from browserstack_sdk.bstack11l11111l1_opy_ import *
from browserstack_sdk.bstack1lll111lll_opy_ import *
from browserstack_sdk.bstack11l11l11l_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1ll1lll11_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack1lll11111_opy_():
    global bstack1l1l1l11l1_opy_
    try:
        bstack11ll11111l_opy_ = bstack1l1ll11111_opy_()
        bstack1l111l11l1_opy_(bstack11ll11111l_opy_)
        hub_url = bstack11ll11111l_opy_.get(bstack1l111l1_opy_ (u"ࠥࡹࡷࡲࠢࢄ"), bstack1l111l1_opy_ (u"ࠦࠧࢅ"))
        if hub_url.endswith(bstack1l111l1_opy_ (u"ࠬ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ࢆ")):
            hub_url = hub_url.rsplit(bstack1l111l1_opy_ (u"࠭࠯ࡸࡦ࠲࡬ࡺࡨࠧࢇ"), 1)[0]
        if hub_url.startswith(bstack1l111l1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࠨ࢈")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࠪࢉ")):
            hub_url = hub_url[8:]
        bstack1l1l1l11l1_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1ll11111_opy_():
    global CONFIG
    bstack1lll1l1ll_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢊ"), {}).get(bstack1l111l1_opy_ (u"ࠪ࡫ࡷ࡯ࡤࡏࡣࡰࡩࠬࢋ"), bstack1l111l1_opy_ (u"ࠫࡓࡕ࡟ࡈࡔࡌࡈࡤࡔࡁࡎࡇࡢࡔࡆ࡙ࡓࡆࡆࠪࢌ"))
    if not isinstance(bstack1lll1l1ll_opy_, str):
        raise ValueError(bstack1l111l1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡌࡸࡩࡥࠢࡱࡥࡲ࡫ࠠ࡮ࡷࡶࡸࠥࡨࡥࠡࡣࠣࡺࡦࡲࡩࡥࠢࡶࡸࡷ࡯࡮ࡨࠤࢍ"))
    try:
        bstack11ll11111l_opy_ = bstack1llll1111_opy_(bstack1lll1l1ll_opy_)
        return bstack11ll11111l_opy_
    except Exception as e:
        logger.error(bstack1l111l1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧࢎ").format(str(e)))
        return {}
def bstack1llll1111_opy_(bstack1lll1l1ll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l111l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ࢏")] or not CONFIG[bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ࢐")]:
            raise ValueError(bstack1l111l1_opy_ (u"ࠤࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠦ࢑"))
        url = bstack1l111l1ll_opy_ + bstack1lll1l1ll_opy_
        auth = (CONFIG[bstack1l111l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ࢒")], CONFIG[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࢓")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11l1ll1l_opy_ = json.loads(response.text)
            return bstack11l1ll1l_opy_
    except ValueError as ve:
        logger.error(bstack1l111l1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡵ࡭ࡩࠦࡤࡦࡶࡤ࡭ࡱࡹࠠ࠻ࠢࡾࢁࠧ࢔").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l111l1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡶ࡮ࡪࠠࡥࡧࡷࡥ࡮ࡲࡳࠡ࠼ࠣࡿࢂࠨ࢕").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1l111l11l1_opy_(bstack111l11ll1_opy_):
    global CONFIG
    if bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ࢖") not in CONFIG or str(CONFIG[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢗ")]).lower() == bstack1l111l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࢘"):
        CONFIG[bstack1l111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭࢙ࠩ")] = False
    elif bstack1l111l1_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥ࢚ࠩ") in bstack111l11ll1_opy_:
        bstack11llllll_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ࢛ࠩ"), {})
        logger.debug(bstack1l111l1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠧࡶࠦ࢜"), bstack11llllll_opy_)
        bstack1llll1l11_opy_ = bstack111l11ll1_opy_.get(bstack1l111l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡒࡦࡲࡨࡥࡹ࡫ࡲࡴࠤ࢝"), [])
        bstack1lll11l11l_opy_ = bstack1l111l1_opy_ (u"ࠣ࠮ࠥ࢞").join(bstack1llll1l11_opy_)
        logger.debug(bstack1l111l1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡅࡸࡷࡹࡵ࡭ࠡࡴࡨࡴࡪࡧࡴࡦࡴࠣࡷࡹࡸࡩ࡯ࡩ࠽ࠤࠪࡹࠢ࢟"), bstack1lll11l11l_opy_)
        bstack1l1l1lll1_opy_ = {
            bstack1l111l1_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧࢠ"): bstack1l111l1_opy_ (u"ࠦࡦࡺࡳ࠮ࡴࡨࡴࡪࡧࡴࡦࡴࠥࢡ"),
            bstack1l111l1_opy_ (u"ࠧ࡬࡯ࡳࡥࡨࡐࡴࡩࡡ࡭ࠤࢢ"): bstack1l111l1_opy_ (u"ࠨࡴࡳࡷࡨࠦࢣ"),
            bstack1l111l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࠭ࡳࡧࡳࡩࡦࡺࡥࡳࠤࢤ"): bstack1lll11l11l_opy_
        }
        bstack11llllll_opy_.update(bstack1l1l1lll1_opy_)
        logger.debug(bstack1l111l1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡖࡲࡧࡥࡹ࡫ࡤࠡ࡮ࡲࡧࡦࡲࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠨࡷࠧࢥ"), bstack11llllll_opy_)
        CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")] = bstack11llllll_opy_
        logger.debug(bstack1l111l1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡉ࡭ࡳࡧ࡬ࠡࡅࡒࡒࡋࡏࡇ࠻ࠢࠨࡷࠧࢧ"), CONFIG)
def bstack1111ll1l_opy_():
    bstack11ll11111l_opy_ = bstack1l1ll11111_opy_()
    if not bstack11ll11111l_opy_[bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫࢨ")]:
      raise ValueError(bstack1l111l1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡗࡵࡰࠥ࡯ࡳࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡴࡳࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠢࢩ"))
    return bstack11ll11111l_opy_[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡘࡶࡱ࠭ࢪ")] + bstack1l111l1_opy_ (u"ࠧࡀࡥࡤࡴࡸࡃࠧࢫ")
@measure(event_name=EVENTS.bstack1l111ll11_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack1ll11lll1l_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l111l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ")], CONFIG[bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ")])
        url = bstack11ll1ll11_opy_
        logger.debug(bstack1l111l1_opy_ (u"ࠥࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡶࡴࡳࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠣࡅࡕࡏࠢࢮ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l111l1_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥࢯ"): bstack1l111l1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣࢰ")})
            if response.status_code == 200:
                bstack11l11111_opy_ = json.loads(response.text)
                bstack111l1llll_opy_ = bstack11l11111_opy_.get(bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠭ࢱ"), [])
                if bstack111l1llll_opy_:
                    bstack1111l111_opy_ = bstack111l1llll_opy_[0]
                    build_hashed_id = bstack1111l111_opy_.get(bstack1l111l1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪࢲ"))
                    bstack11ll1l1l1_opy_ = bstack1l11ll1l1_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11ll1l1l1_opy_])
                    logger.info(bstack1lll1lll1_opy_.format(bstack11ll1l1l1_opy_))
                    bstack1l1111ll11_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࢳ")]
                    if bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࢴ") in CONFIG:
                      bstack1l1111ll11_opy_ += bstack1l111l1_opy_ (u"ࠪࠤࠬࢵ") + CONFIG[bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢶ")]
                    if bstack1l1111ll11_opy_ != bstack1111l111_opy_.get(bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢷ")):
                      logger.debug(bstack1l1l11l11l_opy_.format(bstack1111l111_opy_.get(bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࢸ")), bstack1l1111ll11_opy_))
                    return result
                else:
                    logger.debug(bstack1l111l1_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡎࡰࠢࡥࡹ࡮ࡲࡤࡴࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠱ࠦࢹ"))
            else:
                logger.debug(bstack1l111l1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢺ"))
        except Exception as e:
            logger.error(bstack1l111l1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡶࠤ࠿ࠦࡻࡾࠤࢻ").format(str(e)))
    else:
        logger.debug(bstack1l111l1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡆࡓࡓࡌࡉࡈࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡥࡹ࡮ࡲࡤࡴ࠰ࠥࢼ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll111ll_opy_ import bstack11ll111ll_opy_, bstack1lll1ll1_opy_, bstack11l111111_opy_, bstack1ll1lll11l_opy_
from bstack_utils.measure import bstack11lll1l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11l11l11_opy_ import bstack111llll1ll_opy_
from bstack_utils.messages import *
from bstack_utils import bstack1ll1lll11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11l111l_opy_, bstack11l1l1l1l_opy_, bstack1llll1l1ll_opy_, bstack1l1l1l111_opy_, \
  bstack11lll1lll_opy_, \
  Notset, bstack1llllllll_opy_, \
  bstack1l1l11l1l_opy_, bstack111lll1l11_opy_, bstack1lll11l1l1_opy_, bstack11lll11l1_opy_, bstack1lllllll1_opy_, bstack11l111l11l_opy_, \
  bstack1l11l1l1ll_opy_, \
  bstack111llll1_opy_, bstack1lll1l1ll1_opy_, bstack111lll1111_opy_, bstack1l1111ll1l_opy_, \
  bstack111l11l11_opy_, bstack1llll11lll_opy_, bstack11lll111_opy_, bstack1l11lll11_opy_, bstack11ll1l1lll_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack11ll11ll1_opy_
from bstack_utils.bstack11ll1l1ll_opy_ import bstack11l11l1ll_opy_, bstack11ll1l1ll1_opy_
from bstack_utils.bstack1ll11ll1l_opy_ import bstack1l1l1l1l1l_opy_
from bstack_utils.bstack1l1111ll_opy_ import bstack11llll1ll_opy_, bstack11ll1lll11_opy_
from bstack_utils.bstack1l111l1l_opy_ import bstack1l111l1l_opy_
from bstack_utils.bstack1l11l1lll1_opy_ import bstack11l1111l1l_opy_
from bstack_utils.proxy import bstack1ll1ll11ll_opy_, bstack111lll1l1l_opy_, bstack11ll11l1l_opy_, bstack1l1l1ll1_opy_
from bstack_utils.bstack1ll11ll11_opy_ import bstack1lll1llll1_opy_, bstack11l1l111ll_opy_
import bstack_utils.bstack11llll111l_opy_ as bstack1l11111ll1_opy_
import bstack_utils.bstack1l1lll1lll_opy_ as bstack1l1lllll1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack11lll1l1l_opy_ import bstack11l11l1l1_opy_
from bstack_utils.bstack1l111l1l1_opy_ import bstack1llll111l_opy_
from bstack_utils.bstack11ll11lll1_opy_ import bstack1l11l11l1l_opy_
if os.getenv(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ࢽ")):
  cli.bstack11l1llll1l_opy_()
else:
  os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡊࡒࡓࡐ࡙ࠧࢾ")] = bstack1l111l1_opy_ (u"࠭ࡴࡳࡷࡨࠫࢿ")
bstack1l11l111l1_opy_ = bstack1l111l1_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧࣀ")
bstack1l1l111111_opy_ = bstack1l111l1_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧࣁ")
from ._version import __version__
bstack1l11l1111l_opy_ = None
CONFIG = {}
bstack1llll11ll_opy_ = {}
bstack1111111ll_opy_ = {}
bstack1llll1ll1l_opy_ = None
bstack1l111lll_opy_ = None
bstack1l1l1l1ll1_opy_ = None
bstack111llll11_opy_ = -1
bstack1lll11l1_opy_ = 0
bstack111l111l1_opy_ = bstack1111l1l1l_opy_
bstack1lll1ll1l1_opy_ = 1
bstack1l1111l1l_opy_ = False
bstack1l11111l11_opy_ = False
bstack1lll11ll1l_opy_ = bstack1l111l1_opy_ (u"ࠩࠪࣂ")
bstack1lll111l1_opy_ = bstack1l111l1_opy_ (u"ࠪࠫࣃ")
bstack11ll11l1_opy_ = False
bstack11l1ll1l1_opy_ = True
bstack11111l1l_opy_ = bstack1l111l1_opy_ (u"ࠫࠬࣄ")
bstack1l11ll11_opy_ = []
bstack1ll11l11_opy_ = threading.Lock()
bstack1l11l1ll1_opy_ = threading.Lock()
bstack1ll1111l_opy_ = None
bstack1l1l1l11l1_opy_ = bstack1l111l1_opy_ (u"ࠬ࠭ࣅ")
bstack11l1111111_opy_ = False
bstack11llllllll_opy_ = None
bstack11l1l1ll11_opy_ = None
bstack1l11lllll_opy_ = None
bstack11l1ll11l_opy_ = -1
bstack11lll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"࠭ࡾࠨࣆ")), bstack1l111l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧࣇ"), bstack1l111l1_opy_ (u"ࠨ࠰ࡵࡳࡧࡵࡴ࠮ࡴࡨࡴࡴࡸࡴ࠮ࡪࡨࡰࡵ࡫ࡲ࠯࡬ࡶࡳࡳ࠭ࣈ"))
bstack1llllll11_opy_ = 0
bstack1lll111ll_opy_ = 0
bstack1l1llll1l1_opy_ = []
bstack1ll1111ll1_opy_ = []
bstack11lllll1ll_opy_ = []
bstack1l1ll11l1_opy_ = []
bstack1l1lll1111_opy_ = bstack1l111l1_opy_ (u"ࠩࠪࣉ")
bstack11ll1l111_opy_ = bstack1l111l1_opy_ (u"ࠪࠫ࣊")
bstack1ll1l1ll1_opy_ = False
bstack1l11l1l1l1_opy_ = False
bstack11lll11l11_opy_ = {}
bstack1l1111l1ll_opy_ = {}
bstack111lll1l1_opy_ = None
bstack1l11111l1l_opy_ = None
bstack11lllll1_opy_ = None
bstack1l1ll111ll_opy_ = None
bstack1l1l11ll1l_opy_ = None
bstack1l1l11l1ll_opy_ = None
bstack1lll11ll11_opy_ = None
bstack1lll11lll_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack1111l11l1_opy_ = None
bstack1l1l111lll_opy_ = None
bstack1l1l11l11_opy_ = None
bstack1ll1l1lll_opy_ = None
bstack1l111l111_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1l1l11l111_opy_ = None
bstack1lll1lll11_opy_ = None
bstack111ll11ll_opy_ = None
bstack1lll1l11_opy_ = None
bstack11l11l111_opy_ = None
bstack11ll11lll_opy_ = None
bstack1l11lllll1_opy_ = None
thread_local = threading.local()
bstack1l1l1llll1_opy_ = False
bstack1l11llll1_opy_ = bstack1l111l1_opy_ (u"ࠦࠧ࣋")
logger = bstack1ll1lll11_opy_.get_logger(__name__, bstack111l111l1_opy_)
bstack1l1111ll1_opy_ = bstack1ll1lll11_opy_.bstack1l11llll1l_opy_(__name__)
bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
percy = bstack11ll11111_opy_()
bstack1l111lll1_opy_ = bstack111llll1ll_opy_()
bstack11l1l11ll_opy_ = bstack11l11l11l_opy_()
def bstack111l1l1ll_opy_():
  global CONFIG
  global bstack1ll1l1ll1_opy_
  global bstack1l1l1111_opy_
  testContextOptions = bstack1ll11llll1_opy_(CONFIG)
  if bstack11lll1lll_opy_(CONFIG):
    if (bstack1l111l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࣌") in testContextOptions and str(testContextOptions[bstack1l111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࣍")]).lower() == bstack1l111l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎")):
      bstack1ll1l1ll1_opy_ = True
    bstack1l1l1111_opy_.bstack1l1ll111_opy_(testContextOptions.get(bstack1l111l1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷ࣏ࠬ"), False))
  else:
    bstack1ll1l1ll1_opy_ = True
    bstack1l1l1111_opy_.bstack1l1ll111_opy_(True)
def bstack111ll11l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111l1111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1ll11ll_opy_():
  global bstack1l1111l1ll_opy_
  args = sys.argv
  for i in range(len(args)):
    if bstack1l111l1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨ࣐") == args[i].lower() or bstack1l111l1_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪ࣑ࠦ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      bstack1l1111l1ll_opy_[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒")] = path
      return path
  return None
bstack1lllll1ll1_opy_ = re.compile(bstack1l111l1_opy_ (u"ࡷࠨ࠮ࠫࡁ࡟ࠨࢀ࠮࠮ࠫࡁࠬࢁ࠳࠰࠿࣓ࠣ"))
def bstack1ll11l1111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lllll1ll1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l111l1_opy_ (u"ࠨࠤࡼࠤࣔ") + group + bstack1l111l1_opy_ (u"ࠢࡾࠤࣕ"), os.environ.get(group))
  return value
def bstack1l11lll1l1_opy_():
  global bstack1l11lllll1_opy_
  if bstack1l11lllll1_opy_ is None:
        bstack1l11lllll1_opy_ = bstack11l1ll11ll_opy_()
  bstack1l1ll1l111_opy_ = bstack1l11lllll1_opy_
  if bstack1l1ll1l111_opy_ and os.path.exists(os.path.abspath(bstack1l1ll1l111_opy_)):
    fileName = bstack1l1ll1l111_opy_
  if bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࣖ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ࣗ")])) and not bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬࣘ") in locals():
    fileName = os.environ[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨࣙ")]
  if bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧࣚ") in locals():
    bstack11lll_opy_ = os.path.abspath(fileName)
  else:
    bstack11lll_opy_ = bstack1l111l1_opy_ (u"࠭ࠧࣛ")
  bstack1l11l1111_opy_ = os.getcwd()
  bstack1l111lllll_opy_ = bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪࣜ")
  bstack1llll1l11l_opy_ = bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬࣝ")
  while (not os.path.exists(bstack11lll_opy_)) and bstack1l11l1111_opy_ != bstack1l111l1_opy_ (u"ࠤࠥࣞ"):
    bstack11lll_opy_ = os.path.join(bstack1l11l1111_opy_, bstack1l111lllll_opy_)
    if not os.path.exists(bstack11lll_opy_):
      bstack11lll_opy_ = os.path.join(bstack1l11l1111_opy_, bstack1llll1l11l_opy_)
    if bstack1l11l1111_opy_ != os.path.dirname(bstack1l11l1111_opy_):
      bstack1l11l1111_opy_ = os.path.dirname(bstack1l11l1111_opy_)
    else:
      bstack1l11l1111_opy_ = bstack1l111l1_opy_ (u"ࠥࠦࣟ")
  bstack1l11lllll1_opy_ = bstack11lll_opy_ if os.path.exists(bstack11lll_opy_) else None
  return bstack1l11lllll1_opy_
def bstack1l1l11111_opy_(config):
    if bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡔࡨࡴࡴࡸࡴࡪࡰࡪࠫ࣠") in config:
      config[bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ࣡")] = config[bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷࡖࡪࡶ࡯ࡳࡶ࡬ࡲ࡬࠭࣢")]
    if bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡗ࡫ࡰࡰࡴࡷ࡭ࡳ࡭ࡏࡱࡶ࡬ࡳࡳࡹࣣࠧ") in config:
      config[bstack1l111l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬࣤ")] = config[bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺࡒࡦࡲࡲࡶࡹ࡯࡮ࡨࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣥ")]
def bstack1l11ll11l1_opy_():
  bstack11lll_opy_ = bstack1l11lll1l1_opy_()
  if not os.path.exists(bstack11lll_opy_):
    bstack1l11lll1_opy_(
      bstack1llll111l1_opy_.format(os.getcwd()))
  try:
    with open(bstack11lll_opy_, bstack1l111l1_opy_ (u"ࠪࡶࣦࠬ")) as stream:
      yaml.add_implicit_resolver(bstack1l111l1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࣧ"), bstack1lllll1ll1_opy_)
      yaml.add_constructor(bstack1l111l1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࣨ"), bstack1ll11l1111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      bstack1l1l11111_opy_(config)
      return config
  except:
    with open(bstack11lll_opy_, bstack1l111l1_opy_ (u"࠭ࡲࠨࣩ")) as stream:
      try:
        config = yaml.safe_load(stream)
        bstack1l1l11111_opy_(config)
        return config
      except yaml.YAMLError as exc:
        bstack1l11lll1_opy_(bstack11l11l1ll1_opy_.format(str(exc)))
def bstack1l1l11l1l1_opy_(config):
  bstack1111ll11l_opy_ = bstack1ll1l11lll_opy_(config)
  for option in list(bstack1111ll11l_opy_):
    if option.lower() in bstack1llll1ll1_opy_ and option != bstack1llll1ll1_opy_[option.lower()]:
      bstack1111ll11l_opy_[bstack1llll1ll1_opy_[option.lower()]] = bstack1111ll11l_opy_[option]
      del bstack1111ll11l_opy_[option]
  return config
def bstack1lll1ll111_opy_():
  global bstack1111111ll_opy_
  for key, bstack11lll1llll_opy_ in bstack1l1l11llll_opy_.items():
    if isinstance(bstack11lll1llll_opy_, list):
      for var in bstack11lll1llll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1111111ll_opy_[key] = os.environ[var]
          break
    elif bstack11lll1llll_opy_ in os.environ and os.environ[bstack11lll1llll_opy_] and str(os.environ[bstack11lll1llll_opy_]).strip():
      bstack1111111ll_opy_[key] = os.environ[bstack11lll1llll_opy_]
  if bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ࣪") in os.environ:
    bstack1111111ll_opy_[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ࣫")] = {}
    bstack1111111ll_opy_[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭࣬")][bstack1l111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣭ࠬ")] = os.environ[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࣮࠭")]
def bstack11l1llll1_opy_():
  global bstack1llll11ll_opy_
  global bstack11111l1l_opy_
  global bstack1l1111l1ll_opy_
  bstack1llllll1l1_opy_ = []
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) - 1 and bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣯").lower() == val.lower():
      bstack1llll11ll_opy_[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࣰࠪ")] = {}
      bstack1llll11ll_opy_[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࣱࠫ")][bstack1l111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = sys.argv[idx + 1]
      bstack1llllll1l1_opy_.extend([idx, idx + 1])
      break
  for key, bstack1lll11llll_opy_ in bstack1l11l1ll_opy_.items():
    if isinstance(bstack1lll11llll_opy_, list):
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        for var in bstack1lll11llll_opy_:
          if bstack1l111l1_opy_ (u"ࠩ࠰࠱ࠬࣳ") + var.lower() == val.lower() and key not in bstack1llll11ll_opy_:
            bstack1llll11ll_opy_[key] = sys.argv[idx + 1]
            bstack11111l1l_opy_ += bstack1l111l1_opy_ (u"ࠪࠤ࠲࠳ࠧࣴ") + var + bstack1l111l1_opy_ (u"ࠫࠥ࠭ࣵ") + shlex.quote(sys.argv[idx + 1])
            bstack11ll1l1lll_opy_(bstack1l1111l1ll_opy_, key, sys.argv[idx + 1])
            bstack1llllll1l1_opy_.extend([idx, idx + 1])
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx >= len(sys.argv) - 1:
          continue
        if bstack1l111l1_opy_ (u"ࠬ࠳࠭ࠨࣶ") + bstack1lll11llll_opy_.lower() == val.lower() and key not in bstack1llll11ll_opy_:
          bstack1llll11ll_opy_[key] = sys.argv[idx + 1]
          bstack11111l1l_opy_ += bstack1l111l1_opy_ (u"࠭ࠠ࠮࠯ࠪࣷ") + bstack1lll11llll_opy_ + bstack1l111l1_opy_ (u"ࠧࠡࠩࣸ") + shlex.quote(sys.argv[idx + 1])
          bstack11ll1l1lll_opy_(bstack1l1111l1ll_opy_, key, sys.argv[idx + 1])
          bstack1llllll1l1_opy_.extend([idx, idx + 1])
  for idx in sorted(set(bstack1llllll1l1_opy_), reverse=True):
    if idx < len(sys.argv):
      del sys.argv[idx]
def bstack11l1lll11_opy_(config):
  bstack1ll111l11_opy_ = config.keys()
  for bstack11lll1ll1l_opy_, bstack1111llll1_opy_ in bstack111111l11_opy_.items():
    if bstack1111llll1_opy_ in bstack1ll111l11_opy_:
      config[bstack11lll1ll1l_opy_] = config[bstack1111llll1_opy_]
      del config[bstack1111llll1_opy_]
  for bstack11lll1ll1l_opy_, bstack1111llll1_opy_ in bstack111lll111l_opy_.items():
    if isinstance(bstack1111llll1_opy_, list):
      for bstack11llllll1l_opy_ in bstack1111llll1_opy_:
        if bstack11llllll1l_opy_ in bstack1ll111l11_opy_:
          config[bstack11lll1ll1l_opy_] = config[bstack11llllll1l_opy_]
          del config[bstack11llllll1l_opy_]
          break
    elif bstack1111llll1_opy_ in bstack1ll111l11_opy_:
      config[bstack11lll1ll1l_opy_] = config[bstack1111llll1_opy_]
      del config[bstack1111llll1_opy_]
  for bstack11llllll1l_opy_ in list(config):
    for bstack1ll111lll1_opy_ in bstack11llll11_opy_:
      if bstack11llllll1l_opy_.lower() == bstack1ll111lll1_opy_.lower() and bstack11llllll1l_opy_ != bstack1ll111lll1_opy_:
        config[bstack1ll111lll1_opy_] = config[bstack11llllll1l_opy_]
        del config[bstack11llllll1l_opy_]
  bstack11l1l11ll1_opy_ = [{}]
  if not config.get(bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ")):
    config[bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")] = [{}]
  bstack11l1l11ll1_opy_ = config[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")]
  for platform in bstack11l1l11ll1_opy_:
    for bstack11llllll1l_opy_ in list(platform):
      for bstack1ll111lll1_opy_ in bstack11llll11_opy_:
        if bstack11llllll1l_opy_.lower() == bstack1ll111lll1_opy_.lower() and bstack11llllll1l_opy_ != bstack1ll111lll1_opy_:
          platform[bstack1ll111lll1_opy_] = platform[bstack11llllll1l_opy_]
          del platform[bstack11llllll1l_opy_]
  for bstack11lll1ll1l_opy_, bstack1111llll1_opy_ in bstack111lll111l_opy_.items():
    for platform in bstack11l1l11ll1_opy_:
      if isinstance(bstack1111llll1_opy_, list):
        for bstack11llllll1l_opy_ in bstack1111llll1_opy_:
          if bstack11llllll1l_opy_ in platform:
            platform[bstack11lll1ll1l_opy_] = platform[bstack11llllll1l_opy_]
            del platform[bstack11llllll1l_opy_]
            break
      elif bstack1111llll1_opy_ in platform:
        platform[bstack11lll1ll1l_opy_] = platform[bstack1111llll1_opy_]
        del platform[bstack1111llll1_opy_]
  for bstack1l1l1llll_opy_ in bstack1111l1ll1_opy_:
    if bstack1l1l1llll_opy_ in config:
      if not bstack1111l1ll1_opy_[bstack1l1l1llll_opy_] in config:
        config[bstack1111l1ll1_opy_[bstack1l1l1llll_opy_]] = {}
      config[bstack1111l1ll1_opy_[bstack1l1l1llll_opy_]].update(config[bstack1l1l1llll_opy_])
      del config[bstack1l1l1llll_opy_]
  for platform in bstack11l1l11ll1_opy_:
    for bstack1l1l1llll_opy_ in bstack1111l1ll1_opy_:
      if bstack1l1l1llll_opy_ in list(platform):
        if not bstack1111l1ll1_opy_[bstack1l1l1llll_opy_] in platform:
          platform[bstack1111l1ll1_opy_[bstack1l1l1llll_opy_]] = {}
        platform[bstack1111l1ll1_opy_[bstack1l1l1llll_opy_]].update(platform[bstack1l1l1llll_opy_])
        del platform[bstack1l1l1llll_opy_]
  config = bstack1l1l11l1l1_opy_(config)
  return config
def bstack11l111lll_opy_(config):
  global bstack1lll111l1_opy_
  bstack1l111llll1_opy_ = False
  if bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨࣼ") in config and str(config[bstack1l111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩࣽ")]).lower() != bstack1l111l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣾ"):
    if bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࣿ") not in config or str(config[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬऀ")]).lower() == bstack1l111l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨँ"):
      config[bstack1l111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩं")] = False
    else:
      bstack11ll11111l_opy_ = bstack1l1ll11111_opy_()
      if bstack1l111l1_opy_ (u"ࠫ࡮ࡹࡔࡳ࡫ࡤࡰࡌࡸࡩࡥࠩः") in bstack11ll11111l_opy_:
        if not bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
          config[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
        config[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")][bstack1l111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪइ")] = bstack1l111l1_opy_ (u"ࠩࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠨई")
        bstack1l111llll1_opy_ = True
        bstack1lll111l1_opy_ = config[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")].get(bstack1l111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऊ"))
  if bstack11lll1lll_opy_(config) and bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩऋ") in config and str(config[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪऌ")]).lower() != bstack1l111l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ऍ") and not bstack1l111llll1_opy_:
    if not bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬऎ") in config:
      config[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")] = {}
    if not config[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऐ")].get(bstack1l111l1_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨऑ")) and not bstack1l111l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ") in config[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪओ")]:
      bstack11llll1111_opy_ = datetime.datetime.now()
      bstack1l1l1l1lll_opy_ = bstack11llll1111_opy_.strftime(bstack1l111l1_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫऔ"))
      hostname = socket.gethostname()
      bstack111lll11_opy_ = bstack1l111l1_opy_ (u"ࠨࠩक").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l111l1_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫख").format(bstack1l1l1l1lll_opy_, hostname, bstack111lll11_opy_)
      config[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧग")][bstack1l111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")] = identifier
    bstack1lll111l1_opy_ = config[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩङ")].get(bstack1l111l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच"))
  return config
def bstack11l1lll11l_opy_():
  bstack1llll1l1l_opy_ =  bstack11lll11l1_opy_()[bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭छ")]
  return bstack1llll1l1l_opy_ if bstack1llll1l1l_opy_ else -1
def bstack11lll1l1_opy_(bstack1llll1l1l_opy_):
  global CONFIG
  if not bstack1l111l1_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪज") in CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ")]:
    return
  CONFIG[bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")] = CONFIG[bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")].replace(
    bstack1l111l1_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧठ"),
    str(bstack1llll1l1l_opy_)
  )
def bstack1l111ll1_opy_():
  global CONFIG
  if not bstack1l111l1_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬड") in CONFIG[bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩढ")]:
    return
  bstack11llll1111_opy_ = datetime.datetime.now()
  bstack1l1l1l1lll_opy_ = bstack11llll1111_opy_.strftime(bstack1l111l1_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ण"))
  CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")] = CONFIG[bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬथ")].replace(
    bstack1l111l1_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪद"),
    bstack1l1l1l1lll_opy_
  )
def bstack111ll11l1l_opy_():
  global CONFIG
  if bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧध") in CONFIG and not bool(CONFIG[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]):
    del CONFIG[bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऩ")]
    return
  if not bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪप") in CONFIG:
    CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫफ")] = bstack1l111l1_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ब")
  if bstack1l111l1_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪभ") in CONFIG[bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]:
    bstack1l111ll1_opy_()
    os.environ[bstack1l111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪय")] = CONFIG[bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩर")]
  if not bstack1l111l1_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪऱ") in CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫल")]:
    return
  bstack1llll1l1l_opy_ = bstack1l111l1_opy_ (u"ࠪࠫळ")
  bstack11l11l1lll_opy_ = bstack11l1lll11l_opy_()
  if bstack11l11l1lll_opy_ != -1:
    bstack1llll1l1l_opy_ = bstack1l111l1_opy_ (u"ࠫࡈࡏࠠࠨऴ") + str(bstack11l11l1lll_opy_)
  if bstack1llll1l1l_opy_ == bstack1l111l1_opy_ (u"ࠬ࠭व"):
    bstack1l1l1ll11_opy_ = bstack1lllll11l1_opy_(CONFIG[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩश")])
    if bstack1l1l1ll11_opy_ != -1:
      bstack1llll1l1l_opy_ = str(bstack1l1l1ll11_opy_)
  if bstack1llll1l1l_opy_:
    bstack11lll1l1_opy_(bstack1llll1l1l_opy_)
    os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫष")] = CONFIG[bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪस")]
def bstack1ll11111l1_opy_(bstack11l1l11l1_opy_, bstack1l11l1lll_opy_, path):
  bstack11ll11ll11_opy_ = {
    bstack1l111l1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ह"): bstack1l11l1lll_opy_
  }
  if os.path.exists(path):
    bstack11lll1ll1_opy_ = json.load(open(path, bstack1l111l1_opy_ (u"ࠪࡶࡧ࠭ऺ")))
  else:
    bstack11lll1ll1_opy_ = {}
  bstack11lll1ll1_opy_[bstack11l1l11l1_opy_] = bstack11ll11ll11_opy_
  with open(path, bstack1l111l1_opy_ (u"ࠦࡼ࠱ࠢऻ")) as outfile:
    json.dump(bstack11lll1ll1_opy_, outfile)
def bstack1lllll11l1_opy_(bstack11l1l11l1_opy_):
  bstack11l1l11l1_opy_ = str(bstack11l1l11l1_opy_)
  bstack1lll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠬࢄ़ࠧ")), bstack1l111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ऽ"))
  try:
    if not os.path.exists(bstack1lll1l1l1_opy_):
      os.makedirs(bstack1lll1l1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠧࡿࠩा")), bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨि"), bstack1l111l1_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫी"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l111l1_opy_ (u"ࠪࡻࠬु")):
        pass
      with open(file_path, bstack1l111l1_opy_ (u"ࠦࡼ࠱ࠢू")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l111l1_opy_ (u"ࠬࡸࠧृ")) as bstack1l1111l1_opy_:
      bstack11l1ll1ll1_opy_ = json.load(bstack1l1111l1_opy_)
    if bstack11l1l11l1_opy_ in bstack11l1ll1ll1_opy_:
      bstack1l11lll1l_opy_ = bstack11l1ll1ll1_opy_[bstack11l1l11l1_opy_][bstack1l111l1_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪॄ")]
      bstack1ll11l1l_opy_ = int(bstack1l11lll1l_opy_) + 1
      bstack1ll11111l1_opy_(bstack11l1l11l1_opy_, bstack1ll11l1l_opy_, file_path)
      return bstack1ll11l1l_opy_
    else:
      bstack1ll11111l1_opy_(bstack11l1l11l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warning(bstack1l1l111l_opy_.format(str(e)))
    return -1
def bstack11lll11111_opy_(config):
  if not config[bstack1l111l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩॅ")] or not config[bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫॆ")]:
    return True
  else:
    return False
def bstack1111111l_opy_(config, index=0):
  global bstack11ll11l1_opy_
  bstack1l1llll11l_opy_ = {}
  caps = bstack1l11l1ll1l_opy_ + bstack1l1l11ll11_opy_
  if config.get(bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭े"), False):
    bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧै")] = True
    bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॉ")] = config.get(bstack1l111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॊ"), {})
  if bstack11ll11l1_opy_:
    caps += bstack1l1l1lll1l_opy_
  for key in config:
    if key in caps + [bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩो")]:
      continue
    bstack1l1llll11l_opy_[key] = config[key]
  if bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ") in config:
    for bstack1lll111l1l_opy_ in config[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ्ࠫ")][index]:
      if bstack1lll111l1l_opy_ in caps:
        continue
      bstack1l1llll11l_opy_[bstack1lll111l1l_opy_] = config[bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॎ")][index][bstack1lll111l1l_opy_]
  bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬॏ")] = socket.gethostname()
  if bstack1l111l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬॐ") in bstack1l1llll11l_opy_:
    del (bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭॑")])
  return bstack1l1llll11l_opy_
def bstack1llll11l1_opy_(config):
  global bstack11ll11l1_opy_
  bstack111ll111ll_opy_ = {}
  caps = bstack1l1l11ll11_opy_
  if bstack11ll11l1_opy_:
    caps += bstack1l1l1lll1l_opy_
  for key in caps:
    if key in config:
      bstack111ll111ll_opy_[key] = config[key]
  return bstack111ll111ll_opy_
def bstack11ll11llll_opy_(bstack1l1llll11l_opy_, bstack111ll111ll_opy_):
  bstack1ll1l1111_opy_ = {}
  for key in bstack1l1llll11l_opy_.keys():
    if key in bstack111111l11_opy_:
      bstack1ll1l1111_opy_[bstack111111l11_opy_[key]] = bstack1l1llll11l_opy_[key]
    else:
      bstack1ll1l1111_opy_[key] = bstack1l1llll11l_opy_[key]
  for key in bstack111ll111ll_opy_:
    if key in bstack111111l11_opy_:
      bstack1ll1l1111_opy_[bstack111111l11_opy_[key]] = bstack111ll111ll_opy_[key]
    else:
      bstack1ll1l1111_opy_[key] = bstack111ll111ll_opy_[key]
  return bstack1ll1l1111_opy_
def bstack1l1ll111l_opy_(config, index=0):
  global bstack11ll11l1_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l1l1lll1_opy_ = bstack1ll11l111l_opy_(bstack11lll111ll_opy_, config, logger)
  bstack111ll111ll_opy_ = bstack1llll11l1_opy_(config)
  bstack1l1111l11l_opy_ = bstack1l1l11ll11_opy_
  bstack1l1111l11l_opy_ += bstack1l1l111ll_opy_
  bstack111ll111ll_opy_ = update(bstack111ll111ll_opy_, bstack11l1l1lll1_opy_)
  if bstack11ll11l1_opy_:
    bstack1l1111l11l_opy_ += bstack1l1l1lll1l_opy_
  if bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ॒ࠩ") in config:
    if bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ॓") in config[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
      caps[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॕ")] = config[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॗ")]
    if bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭क़") in config[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index]:
      caps[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨग़")] = str(config[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़")][index][bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪड़")])
    bstack1l1111l1l1_opy_ = bstack1ll11l111l_opy_(bstack11lll111ll_opy_, config[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][index], logger)
    bstack1l1111l11l_opy_ += list(bstack1l1111l1l1_opy_.keys())
    for bstack1l1l1l1l1_opy_ in bstack1l1111l11l_opy_:
      if bstack1l1l1l1l1_opy_ in config[bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧफ़")][index]:
        if bstack1l1l1l1l1_opy_ == bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧय़"):
          try:
            bstack1l1111l1l1_opy_[bstack1l1l1l1l1_opy_] = str(config[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॠ")][index][bstack1l1l1l1l1_opy_] * 1.0)
          except:
            bstack1l1111l1l1_opy_[bstack1l1l1l1l1_opy_] = str(config[bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪॡ")][index][bstack1l1l1l1l1_opy_])
        else:
          bstack1l1111l1l1_opy_[bstack1l1l1l1l1_opy_] = config[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫॢ")][index][bstack1l1l1l1l1_opy_]
        del (config[bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬॣ")][index][bstack1l1l1l1l1_opy_])
    bstack111ll111ll_opy_ = update(bstack111ll111ll_opy_, bstack1l1111l1l1_opy_)
  bstack1l1llll11l_opy_ = bstack1111111l_opy_(config, index)
  for bstack11llllll1l_opy_ in bstack1l1l11ll11_opy_ + list(bstack11l1l1lll1_opy_.keys()):
    if bstack11llllll1l_opy_ in bstack1l1llll11l_opy_:
      bstack111ll111ll_opy_[bstack11llllll1l_opy_] = bstack1l1llll11l_opy_[bstack11llllll1l_opy_]
      del (bstack1l1llll11l_opy_[bstack11llllll1l_opy_])
  if bstack1llllllll_opy_(config):
    bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ।")] = True
    caps.update(bstack111ll111ll_opy_)
    caps[bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ॥")] = bstack1l1llll11l_opy_
  else:
    bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ०")] = False
    caps.update(bstack11ll11llll_opy_(bstack1l1llll11l_opy_, bstack111ll111ll_opy_))
    if bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ१") in caps:
      caps[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ२")] = caps[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭३")]
      del (caps[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ४")])
    if bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ५") in caps:
      caps[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭६")] = caps[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭७")]
      del (caps[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ८")])
  return caps
def bstack1lllllll11_opy_():
  global bstack1l1l1l11l1_opy_
  global CONFIG
  if bstack111l1111l_opy_() <= version.parse(bstack1l111l1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ९")):
    if bstack1l1l1l11l1_opy_ != bstack1l111l1_opy_ (u"ࠨࠩ॰"):
      return bstack1l111l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1l1l1l11l1_opy_ + bstack1l111l1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢॲ")
    return bstack11lllllll1_opy_
  if bstack1l1l1l11l1_opy_ != bstack1l111l1_opy_ (u"ࠫࠬॳ"):
    return bstack1l111l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢॴ") + bstack1l1l1l11l1_opy_ + bstack1l111l1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢॵ")
  return bstack1l11lll111_opy_
def bstack11l1l1llll_opy_(options):
  return hasattr(options, bstack1l111l1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨॶ"))
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
def bstack1lllll1lll_opy_(options, bstack11l1l1ll_opy_):
  for bstack11l1111l1_opy_ in bstack11l1l1ll_opy_:
    if bstack11l1111l1_opy_ in [bstack1l111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॷ"), bstack1l111l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ॸ")]:
      continue
    if bstack11l1111l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11l1111l1_opy_] = update(options._experimental_options[bstack11l1111l1_opy_],
                                                         bstack11l1l1ll_opy_[bstack11l1111l1_opy_])
    else:
      options.add_experimental_option(bstack11l1111l1_opy_, bstack11l1l1ll_opy_[bstack11l1111l1_opy_])
  if bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack11l1l1ll_opy_:
    for arg in bstack11l1l1ll_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
    del (bstack11l1l1ll_opy_[bstack1l111l1_opy_ (u"ࠬࡧࡲࡨࡵࠪॻ")])
  if bstack1l111l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪॼ") in bstack11l1l1ll_opy_:
    for ext in bstack11l1l1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫॽ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack11l1l1ll_opy_[bstack1l111l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬॾ")])
def bstack1ll1l11111_opy_(options, bstack11l11l1l11_opy_):
  if bstack1l111l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॿ") in bstack11l11l1l11_opy_:
    for bstack1l1l1l1111_opy_ in bstack11l11l1l11_opy_[bstack1l111l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩঀ")]:
      if bstack1l1l1l1111_opy_ in options._preferences:
        options._preferences[bstack1l1l1l1111_opy_] = update(options._preferences[bstack1l1l1l1111_opy_], bstack11l11l1l11_opy_[bstack1l111l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪঁ")][bstack1l1l1l1111_opy_])
      else:
        options.set_preference(bstack1l1l1l1111_opy_, bstack11l11l1l11_opy_[bstack1l111l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫং")][bstack1l1l1l1111_opy_])
  if bstack1l111l1_opy_ (u"࠭ࡡࡳࡩࡶࠫঃ") in bstack11l11l1l11_opy_:
    for arg in bstack11l11l1l11_opy_[bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      options.add_argument(arg)
def bstack1ll1l111l_opy_(options, bstack1l11ll11l_opy_):
  if bstack1l111l1_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩঅ") in bstack1l11ll11l_opy_:
    options.use_webview(bool(bstack1l11ll11l_opy_[bstack1l111l1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪআ")]))
  bstack1lllll1lll_opy_(options, bstack1l11ll11l_opy_)
def bstack1l11l1l11l_opy_(options, bstack1lll111ll1_opy_):
  for bstack1l1ll11ll1_opy_ in bstack1lll111ll1_opy_:
    if bstack1l1ll11ll1_opy_ in [bstack1l111l1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧই"), bstack1l111l1_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ")]:
      continue
    options.set_capability(bstack1l1ll11ll1_opy_, bstack1lll111ll1_opy_[bstack1l1ll11ll1_opy_])
  if bstack1l111l1_opy_ (u"ࠬࡧࡲࡨࡵࠪউ") in bstack1lll111ll1_opy_:
    for arg in bstack1lll111ll1_opy_[bstack1l111l1_opy_ (u"࠭ࡡࡳࡩࡶࠫঊ")]:
      options.add_argument(arg)
  if bstack1l111l1_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫঋ") in bstack1lll111ll1_opy_:
    options.bstack1llll1111l_opy_(bool(bstack1lll111ll1_opy_[bstack1l111l1_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬঌ")]))
def bstack1llllll1l_opy_(options, bstack11ll1l111l_opy_):
  for bstack111l1l111_opy_ in bstack11ll1l111l_opy_:
    if bstack111l1l111_opy_ in [bstack1l111l1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍"), bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ঎")]:
      continue
    options._options[bstack111l1l111_opy_] = bstack11ll1l111l_opy_[bstack111l1l111_opy_]
  if bstack1l111l1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨএ") in bstack11ll1l111l_opy_:
    for bstack111111ll1_opy_ in bstack11ll1l111l_opy_[bstack1l111l1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঐ")]:
      options.bstack11l1l11l_opy_(
        bstack111111ll1_opy_, bstack11ll1l111l_opy_[bstack1l111l1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ঑")][bstack111111ll1_opy_])
  if bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ঒") in bstack11ll1l111l_opy_:
    for arg in bstack11ll1l111l_opy_[bstack1l111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ও")]:
      options.add_argument(arg)
def bstack1lll1lll_opy_(options, caps):
  if not hasattr(options, bstack1l111l1_opy_ (u"ࠩࡎࡉ࡞࠭ঔ")):
    return
  if options.KEY == bstack1l111l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨক"):
    options = bstack11111l11l_opy_.bstack1ll1ll1l_opy_(bstack1ll1llll1l_opy_=options, config=CONFIG)
  if options.KEY == bstack1l111l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩখ") and options.KEY in caps:
    bstack1lllll1lll_opy_(options, caps[bstack1l111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪগ")])
  elif options.KEY == bstack1l111l1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫঘ") and options.KEY in caps:
    bstack1ll1l11111_opy_(options, caps[bstack1l111l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬঙ")])
  elif options.KEY == bstack1l111l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩচ") and options.KEY in caps:
    bstack1l11l1l11l_opy_(options, caps[bstack1l111l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪছ")])
  elif options.KEY == bstack1l111l1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫজ") and options.KEY in caps:
    bstack1ll1l111l_opy_(options, caps[bstack1l111l1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬঝ")])
  elif options.KEY == bstack1l111l1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫঞ") and options.KEY in caps:
    bstack1llllll1l_opy_(options, caps[bstack1l111l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬট")])
def bstack111ll1l1_opy_(caps):
  global bstack11ll11l1_opy_
  if isinstance(os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨঠ")), str):
    bstack11ll11l1_opy_ = eval(os.getenv(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩড")))
  if bstack11ll11l1_opy_:
    if bstack111ll11l_opy_() < version.parse(bstack1l111l1_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨঢ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l111l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪণ")
    if bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩত") in caps:
      browser = caps[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪথ")]
    elif bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧদ") in caps:
      browser = caps[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨধ")]
    browser = str(browser).lower()
    if browser == bstack1l111l1_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨন") or browser == bstack1l111l1_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ঩"):
      browser = bstack1l111l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪপ")
    if browser == bstack1l111l1_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬফ"):
      browser = bstack1l111l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬব")
    if browser not in [bstack1l111l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ভ"), bstack1l111l1_opy_ (u"ࠧࡦࡦࡪࡩࠬম"), bstack1l111l1_opy_ (u"ࠨ࡫ࡨࠫয"), bstack1l111l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩর"), bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ঱")]:
      return None
    try:
      package = bstack1l111l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ল").format(browser)
      name = bstack1l111l1_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭঳")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1l1llll_opy_(options):
        return None
      for bstack11llllll1l_opy_ in caps.keys():
        options.set_capability(bstack11llllll1l_opy_, caps[bstack11llllll1l_opy_])
      bstack1lll1lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l1ll1l1l_opy_(options, bstack1l11ll1l_opy_):
  if not bstack11l1l1llll_opy_(options):
    return
  for bstack11llllll1l_opy_ in bstack1l11ll1l_opy_.keys():
    if bstack11llllll1l_opy_ in bstack1l1l111ll_opy_:
      continue
    if bstack11llllll1l_opy_ in options._caps and type(options._caps[bstack11llllll1l_opy_]) in [dict, list]:
      options._caps[bstack11llllll1l_opy_] = update(options._caps[bstack11llllll1l_opy_], bstack1l11ll1l_opy_[bstack11llllll1l_opy_])
    else:
      options.set_capability(bstack11llllll1l_opy_, bstack1l11ll1l_opy_[bstack11llllll1l_opy_])
  bstack1lll1lll_opy_(options, bstack1l11ll1l_opy_)
  if bstack1l111l1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ঴") in options._caps:
    if options._caps[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ঵")] and options._caps[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭শ")].lower() != bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪষ"):
      del options._caps[bstack1l111l1_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩস")]
def bstack1l1l1l11_opy_(proxy_config):
  if bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨহ") in proxy_config:
    proxy_config[bstack1l111l1_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ঺")] = proxy_config[bstack1l111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ঻")]
    del (proxy_config[bstack1l111l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼ়ࠫ")])
  if bstack1l111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫঽ") in proxy_config and proxy_config[bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬা")].lower() != bstack1l111l1_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪি"):
    proxy_config[bstack1l111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧী")] = bstack1l111l1_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬু")
  if bstack1l111l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫূ") in proxy_config:
    proxy_config[bstack1l111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪৃ")] = bstack1l111l1_opy_ (u"ࠨࡲࡤࡧࠬৄ")
  return proxy_config
def bstack11lll111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ৅") in config:
    return proxy
  config[bstack1l111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ৆")] = bstack1l1l1l11_opy_(config[bstack1l111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪে")])
  if proxy == None:
    proxy = Proxy(config[bstack1l111l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫৈ")])
  return proxy
def bstack1l1ll1llll_opy_(self):
  global CONFIG
  global bstack1l1l111lll_opy_
  try:
    proxy = bstack11ll11l1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l111l1_opy_ (u"࠭࠮ࡱࡣࡦࠫ৉")):
        proxies = bstack1ll1ll11ll_opy_(proxy, bstack1lllllll11_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1l11l_opy_ = proxies.popitem()
          if bstack1l111l1_opy_ (u"ࠢ࠻࠱࠲ࠦ৊") in bstack111l1l11l_opy_:
            return bstack111l1l11l_opy_
          else:
            return bstack1l111l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤো") + bstack111l1l11l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨৌ").format(str(e)))
  return bstack1l1l111lll_opy_(self)
def bstack111llllll_opy_():
  global CONFIG
  return bstack1l1l1ll1_opy_(CONFIG) and bstack11l111l11l_opy_() and bstack111l1111l_opy_() >= version.parse(bstack1ll11111ll_opy_)
def bstack11l1ll111_opy_():
  global CONFIG
  return (bstack1l111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ্࠭") in CONFIG or bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨৎ") in CONFIG) and bstack1l11l1l1ll_opy_()
def bstack1ll1l11lll_opy_(config):
  bstack1111ll11l_opy_ = {}
  if bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৏") in config:
    bstack1111ll11l_opy_ = config[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ৐")]
  if bstack1l111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৑") in config:
    bstack1111ll11l_opy_ = config[bstack1l111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৒")]
  proxy = bstack11ll11l1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l111l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ৓")) and os.path.isfile(proxy):
      bstack1111ll11l_opy_[bstack1l111l1_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭৔")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l111l1_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ৕")):
        proxies = bstack111lll1l1l_opy_(config, bstack1lllllll11_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1l11l_opy_ = proxies.popitem()
          if bstack1l111l1_opy_ (u"ࠧࡀ࠯࠰ࠤ৖") in bstack111l1l11l_opy_:
            parsed_url = urlparse(bstack111l1l11l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l111l1_opy_ (u"ࠨ࠺࠰࠱ࠥৗ") + bstack111l1l11l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1111ll11l_opy_[bstack1l111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ৘")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1111ll11l_opy_[bstack1l111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ৙")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1111ll11l_opy_[bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ৚")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1111ll11l_opy_[bstack1l111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭৛")] = str(parsed_url.password)
  return bstack1111ll11l_opy_
def bstack1ll11llll1_opy_(config):
  if bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩড়") in config:
    return config[bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪঢ়")]
  return {}
def bstack11l111l1ll_opy_(caps):
  global bstack1lll111l1_opy_
  if bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ৞") in caps:
    caps[bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨয়")][bstack1l111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧৠ")] = True
    if bstack1lll111l1_opy_:
      caps[bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪৡ")][bstack1l111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬৢ")] = bstack1lll111l1_opy_
  else:
    caps[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩৣ")] = True
    if bstack1lll111l1_opy_:
      caps[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭৤")] = bstack1lll111l1_opy_
@measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack11ll1l11_opy_():
  global CONFIG
  if not bstack11lll1lll_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৥") in CONFIG and bstack11lll111_opy_(CONFIG[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ০")]):
    if (
      bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ১") in CONFIG
      and bstack11lll111_opy_(CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭২")].get(bstack1l111l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧ৩")))
    ):
      logger.debug(bstack1l111l1_opy_ (u"ࠦࡑࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡣࡶࠤࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡪࡴࡡࡣ࡮ࡨࡨࠧ৪"))
      return
    bstack1111ll11l_opy_ = bstack1ll1l11lll_opy_(CONFIG)
    bstack1l1l1l111l_opy_(CONFIG[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৫")], bstack1111ll11l_opy_)
def bstack1l1l1l111l_opy_(key, bstack1111ll11l_opy_):
  global bstack1l11l1111l_opy_
  logger.info(bstack111llll1l_opy_)
  try:
    bstack1l11l1111l_opy_ = Local()
    bstack1l1lll11_opy_ = {bstack1l111l1_opy_ (u"࠭࡫ࡦࡻࠪ৬"): key}
    bstack1l1lll11_opy_.update(bstack1111ll11l_opy_)
    logger.debug(bstack1l1ll1111l_opy_.format(str(bstack1l1lll11_opy_)).replace(key, bstack1l111l1_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ৭")))
    bstack1l11l1111l_opy_.start(**bstack1l1lll11_opy_)
    if bstack1l11l1111l_opy_.isRunning():
      logger.info(bstack1ll11ll1_opy_)
  except Exception as e:
    bstack1l11lll1_opy_(bstack11111lll1_opy_.format(str(e)))
def bstack1l11llll_opy_():
  global bstack1l11l1111l_opy_
  if bstack1l11l1111l_opy_.isRunning():
    logger.info(bstack1l1ll1111_opy_)
    bstack1l11l1111l_opy_.stop()
  bstack1l11l1111l_opy_ = None
def bstack1lll1l11ll_opy_(bstack1l1l1111l_opy_=[]):
  global CONFIG
  bstack1l1ll1l1l1_opy_ = []
  bstack1ll1l1111l_opy_ = [bstack1l111l1_opy_ (u"ࠨࡱࡶࠫ৮"), bstack1l111l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৯"), bstack1l111l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧৰ"), bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ৱ"), bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৲"), bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ৳")]
  try:
    for err in bstack1l1l1111l_opy_:
      bstack1l1ll11lll_opy_ = {}
      for k in bstack1ll1l1111l_opy_:
        val = CONFIG[bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৴")][int(err[bstack1l111l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ৵")])].get(k)
        if val:
          bstack1l1ll11lll_opy_[k] = val
      if(err[bstack1l111l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৶")] != bstack1l111l1_opy_ (u"ࠪࠫ৷")):
        bstack1l1ll11lll_opy_[bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪ৸")] = {
          err[bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ৹")]: err[bstack1l111l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ৺")]
        }
        bstack1l1ll1l1l1_opy_.append(bstack1l1ll11lll_opy_)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩ৻") + str(e))
  finally:
    return bstack1l1ll1l1l1_opy_
def bstack1ll1ll1ll1_opy_(file_name):
  bstack1lll111111_opy_ = []
  try:
    bstack111l1111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111l1111_opy_):
      with open(bstack111l1111_opy_) as f:
        bstack11llll1l11_opy_ = json.load(f)
        bstack1lll111111_opy_ = bstack11llll1l11_opy_
      os.remove(bstack111l1111_opy_)
    return bstack1lll111111_opy_
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪৼ") + str(e))
    return bstack1lll111111_opy_
def bstack1l111ll1l1_opy_():
  try:
      from bstack_utils.constants import bstack111l11l1_opy_, EVENTS
      from bstack_utils.helper import bstack11l1l1l1l_opy_, get_host_info, bstack1l1l1111_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1ll11lll11_opy_ = os.path.join(os.getcwd(), bstack1l111l1_opy_ (u"ࠩ࡯ࡳ࡬࠭৽"), bstack1l111l1_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭৾"))
      lock = FileLock(bstack1ll11lll11_opy_+bstack1l111l1_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ৿"))
      def bstack1ll111llll_opy_():
          try:
              with lock:
                  with open(bstack1ll11lll11_opy_, bstack1l111l1_opy_ (u"ࠧࡸࠢ਀"), encoding=bstack1l111l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧਁ")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l111l1_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣਂ"): {
                              bstack1l111l1_opy_ (u"ࠣࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠢਃ"): bstack1l111l1_opy_ (u"ࠤࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠧ਄"),
                          }
                      }
                      bstack11111l11_opy_ = datetime.utcnow()
                      bstack11llll1111_opy_ = bstack11111l11_opy_.strftime(bstack1l111l1_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨ࡙࡙ࠣࡉࠢਅ"))
                      bstack1lll11ll_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩਆ")) if os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪਇ")) else bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                      payload = {
                          bstack1l111l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠦਉ"): bstack1l111l1_opy_ (u"ࠣࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧਊ"),
                          bstack1l111l1_opy_ (u"ࠤࡧࡥࡹࡧࠢ਋"): {
                              bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠤ਌"): bstack1lll11ll_opy_,
                              bstack1l111l1_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࡤࡪࡡࡺࠤ਍"): bstack11llll1111_opy_,
                              bstack1l111l1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࠤ਎"): bstack1l111l1_opy_ (u"ࠨࡓࡅࡍࡉࡩࡦࡺࡵࡳࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࠢਏ"),
                              bstack1l111l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡪࡴࡱࡱࠦਐ"): {
                                  bstack1l111l1_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࡵࠥ਑"): data,
                                  bstack1l111l1_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ਒"): bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧਓ"))
                              },
                              bstack1l111l1_opy_ (u"ࠦࡺࡹࡥࡳࡡࡧࡥࡹࡧࠢਔ"): bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠧࡻࡳࡦࡴࡑࡥࡲ࡫ࠢਕ")),
                              bstack1l111l1_opy_ (u"ࠨࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠤਖ"): get_host_info()
                          }
                      }
                      bstack1ll1l11l11_opy_ = bstack1llll1l1ll_opy_(cli.config, [bstack1l111l1_opy_ (u"ࠢࡢࡲ࡬ࡷࠧਗ"), bstack1l111l1_opy_ (u"ࠣࡧࡧࡷࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡢࡶ࡬ࡳࡳࠨਘ"), bstack1l111l1_opy_ (u"ࠤࡤࡴ࡮ࠨਙ")], bstack111l11l1_opy_)
                      response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠥࡔࡔ࡙ࡔࠣਚ"), bstack1ll1l11l11_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l111l1_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦਛ").format(bstack111l11l1_opy_, payload))
                      else:
                          logger.debug(bstack1l111l1_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧਜ").format(bstack111l11l1_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l111l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਝ").format(e))
      bstack1ll111llll_opy_()
      bstack111lll1l11_opy_(bstack1ll11lll11_opy_, logger)
  except:
    pass
def bstack111lllllll_opy_():
  global bstack1l11llll1_opy_
  global bstack1l11ll11_opy_
  global bstack1l1llll1l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack11lllll1ll_opy_
  global bstack11ll1l111_opy_
  global CONFIG
  bstack11l111111l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਞ"))
  if bstack11l111111l_opy_ in [bstack1l111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧਟ"), bstack1l111l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨਠ")]:
    bstack1l1l1lll_opy_()
  percy.shutdown()
  if bstack1l11llll1_opy_:
    logger.warning(bstack1l111l1l11_opy_.format(str(bstack1l11llll1_opy_)))
  else:
    try:
      bstack11lll1ll1_opy_ = bstack1l1l11l1l_opy_(bstack1l111l1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਡ"), logger)
      if bstack11lll1ll1_opy_.get(bstack1l111l1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਢ")) and bstack11lll1ll1_opy_.get(bstack1l111l1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਣ")).get(bstack1l111l1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਤ")):
        logger.warning(bstack1l111l1l11_opy_.format(str(bstack11lll1ll1_opy_[bstack1l111l1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਥ")][bstack1l111l1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਦ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.bstack1lll11l1l_opy_)
  logger.info(bstack11l111l1l1_opy_)
  global bstack1l11l1111l_opy_
  if bstack1l11l1111l_opy_:
    bstack1l11llll_opy_()
  try:
    with bstack1ll11l11_opy_:
      bstack1ll1ll111l_opy_ = bstack1l11ll11_opy_.copy()
    for driver in bstack1ll1ll111l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1111lll_opy_)
  if bstack11ll1l111_opy_ == bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਧ"):
    bstack11lllll1ll_opy_ = bstack1ll1ll1ll1_opy_(bstack1l111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਨ"))
  if bstack11ll1l111_opy_ == bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ਩") and len(bstack1ll1111ll1_opy_) == 0:
    bstack1ll1111ll1_opy_ = bstack1ll1ll1ll1_opy_(bstack1l111l1_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਪ"))
    if len(bstack1ll1111ll1_opy_) == 0:
      bstack1ll1111ll1_opy_ = bstack1ll1ll1ll1_opy_(bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਫ"))
  bstack11l111l11_opy_ = bstack1l111l1_opy_ (u"ࠧࠨਬ")
  if len(bstack1l1llll1l1_opy_) > 0:
    bstack11l111l11_opy_ = bstack1lll1l11ll_opy_(bstack1l1llll1l1_opy_)
  elif len(bstack1ll1111ll1_opy_) > 0:
    bstack11l111l11_opy_ = bstack1lll1l11ll_opy_(bstack1ll1111ll1_opy_)
  elif len(bstack11lllll1ll_opy_) > 0:
    bstack11l111l11_opy_ = bstack1lll1l11ll_opy_(bstack11lllll1ll_opy_)
  elif len(bstack1l1ll11l1_opy_) > 0:
    bstack11l111l11_opy_ = bstack1lll1l11ll_opy_(bstack1l1ll11l1_opy_)
  if bool(bstack11l111l11_opy_):
    bstack1ll11ll11l_opy_(bstack11l111l11_opy_)
  else:
    bstack1ll11ll11l_opy_()
  bstack111lll1l11_opy_(bstack111111lll_opy_, logger)
  if bstack11l111111l_opy_ not in [bstack1l111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਭ")]:
    bstack1l111ll1l1_opy_()
  bstack1ll1lll11_opy_.bstack11l1l111_opy_(CONFIG)
  if len(bstack11lllll1ll_opy_) > 0:
    sys.exit(len(bstack11lllll1ll_opy_))
def bstack1ll11l1ll1_opy_(bstack1l11111lll_opy_, frame):
  global bstack1l1l1111_opy_
  logger.error(bstack1l1ll111l1_opy_)
  bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਮ"), bstack1l11111lll_opy_)
  if hasattr(signal, bstack1l111l1_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਯ")):
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਰ"), signal.Signals(bstack1l11111lll_opy_).name)
  else:
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ਱"), bstack1l111l1_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਲ"))
  if cli.is_running():
    bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.bstack1lll11l1l_opy_)
  bstack11l111111l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਲ਼"))
  if bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ਴") and not cli.is_enabled(CONFIG):
    bstack1llll1lll1_opy_.stop(bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਵ")))
  bstack111lllllll_opy_()
  sys.exit(1)
def bstack1l11lll1_opy_(err):
  logger.critical(bstack11ll1lllll_opy_.format(str(err)))
  bstack1ll11ll11l_opy_(bstack11ll1lllll_opy_.format(str(err)), True)
  atexit.unregister(bstack111lllllll_opy_)
  bstack1l1l1lll_opy_()
  sys.exit(1)
def bstack11l1l1ll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll11ll11l_opy_(message, True)
  atexit.unregister(bstack111lllllll_opy_)
  bstack1l1l1lll_opy_()
  sys.exit(1)
def bstack1ll1l1l111_opy_():
  global CONFIG
  global bstack1llll11ll_opy_
  global bstack1111111ll_opy_
  global bstack11l1ll1l1_opy_
  CONFIG = bstack1l11ll11l1_opy_()
  load_dotenv(CONFIG.get(bstack1l111l1_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਸ਼")))
  bstack1lll1ll111_opy_()
  bstack11l1llll1_opy_()
  CONFIG = bstack11l1lll11_opy_(CONFIG)
  update(CONFIG, bstack1111111ll_opy_)
  update(CONFIG, bstack1llll11ll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack11l111lll_opy_(CONFIG)
  bstack11l1ll1l1_opy_ = bstack11lll1lll_opy_(CONFIG)
  os.environ[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਷")] = bstack11l1ll1l1_opy_.__str__().lower()
  bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਸ"), bstack11l1ll1l1_opy_)
  if (bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਹ") in CONFIG and bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ਺") in bstack1llll11ll_opy_) or (
          bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਻") in CONFIG and bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ਼ࠬ") not in bstack1111111ll_opy_):
    if os.getenv(bstack1l111l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ਽")):
      CONFIG[bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਾ")] = os.getenv(bstack1l111l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩਿ"))
    else:
      if not CONFIG.get(bstack1l111l1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤੀ"), bstack1l111l1_opy_ (u"ࠢࠣੁ")) in bstack1ll111111l_opy_:
        bstack111ll11l1l_opy_()
  elif (bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫੂ") not in CONFIG and bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੃") in CONFIG) or (
          bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭੄") in bstack1111111ll_opy_ and bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੅") not in bstack1llll11ll_opy_):
    del (CONFIG[bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੆")])
  if bstack11lll11111_opy_(CONFIG):
    bstack1l11lll1_opy_(bstack11l1l111l_opy_)
  Config.bstack1llll1ll11_opy_().bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣੇ"), CONFIG[bstack1l111l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩੈ")])
  bstack1l1l1l1ll_opy_()
  bstack11l111ll1_opy_()
  if bstack11ll11l1_opy_ and not CONFIG.get(bstack1l111l1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ੉"), bstack1l111l1_opy_ (u"ࠤࠥ੊")) in bstack1ll111111l_opy_:
    CONFIG[bstack1l111l1_opy_ (u"ࠪࡥࡵࡶࠧੋ")] = bstack11l111ll_opy_(CONFIG)
    logger.info(bstack1l1ll11l1l_opy_.format(CONFIG[bstack1l111l1_opy_ (u"ࠫࡦࡶࡰࠨੌ")]))
  if not bstack11l1ll1l1_opy_:
    CONFIG[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੍")] = [{}]
def bstack1ll11l1l1_opy_(config, bstack11ll1ll1l_opy_):
  global CONFIG
  global bstack11ll11l1_opy_
  CONFIG = config
  bstack11ll11l1_opy_ = bstack11ll1ll1l_opy_
def bstack11l111ll1_opy_():
  global CONFIG
  global bstack11ll11l1_opy_
  if bstack1l111l1_opy_ (u"࠭ࡡࡱࡲࠪ੎") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1ll11l11l_opy_)
    bstack11ll11l1_opy_ = True
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭੏"), True)
def bstack11l111ll_opy_(config):
  bstack1ll1l11ll1_opy_ = bstack1l111l1_opy_ (u"ࠨࠩ੐")
  app = config[bstack1l111l1_opy_ (u"ࠩࡤࡴࡵ࠭ੑ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l11111l_opy_:
      if os.path.exists(app):
        bstack1ll1l11ll1_opy_ = bstack1l11l1l111_opy_(config, app)
      elif bstack1l1llllll_opy_(app):
        bstack1ll1l11ll1_opy_ = app
      else:
        bstack1l11lll1_opy_(bstack1l11111111_opy_.format(app))
    else:
      if bstack1l1llllll_opy_(app):
        bstack1ll1l11ll1_opy_ = app
      elif os.path.exists(app):
        bstack1ll1l11ll1_opy_ = bstack1l11l1l111_opy_(app)
      else:
        bstack1l11lll1_opy_(bstack1l111ll1ll_opy_)
  else:
    if len(app) > 2:
      bstack1l11lll1_opy_(bstack1111l1l1_opy_)
    elif len(app) == 2:
      if bstack1l111l1_opy_ (u"ࠪࡴࡦࡺࡨࠨ੒") in app and bstack1l111l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੓") in app:
        if os.path.exists(app[bstack1l111l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ੔")]):
          bstack1ll1l11ll1_opy_ = bstack1l11l1l111_opy_(config, app[bstack1l111l1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ੕")], app[bstack1l111l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ੖")])
        else:
          bstack1l11lll1_opy_(bstack1l11111111_opy_.format(app))
      else:
        bstack1l11lll1_opy_(bstack1111l1l1_opy_)
    else:
      for key in app:
        if key in bstack11llllll11_opy_:
          if key == bstack1l111l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭੗"):
            if os.path.exists(app[key]):
              bstack1ll1l11ll1_opy_ = bstack1l11l1l111_opy_(config, app[key])
            else:
              bstack1l11lll1_opy_(bstack1l11111111_opy_.format(app))
          else:
            bstack1ll1l11ll1_opy_ = app[key]
        else:
          bstack1l11lll1_opy_(bstack11l1l1l11l_opy_)
  return bstack1ll1l11ll1_opy_
def bstack1l1llllll_opy_(bstack1ll1l11ll1_opy_):
  import re
  bstack1ll1ll1ll_opy_ = re.compile(bstack1l111l1_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੘"))
  bstack11llll1lll_opy_ = re.compile(bstack1l111l1_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢਖ਼"))
  if bstack1l111l1_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪਗ਼") in bstack1ll1l11ll1_opy_ or re.fullmatch(bstack1ll1ll1ll_opy_, bstack1ll1l11ll1_opy_) or re.fullmatch(bstack11llll1lll_opy_, bstack1ll1l11ll1_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l1lll1ll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1l11l1l111_opy_(config, path, bstack11l11l111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l111l1_opy_ (u"ࠬࡸࡢࠨਜ਼")).read()).hexdigest()
  bstack11ll1l1111_opy_ = bstack1lll1l1l1l_opy_(md5_hash)
  bstack1ll1l11ll1_opy_ = None
  if bstack11ll1l1111_opy_:
    logger.info(bstack11l1ll1lll_opy_.format(bstack11ll1l1111_opy_, md5_hash))
    return bstack11ll1l1111_opy_
  bstack1ll11llll_opy_ = datetime.datetime.now()
  bstack1ll1llllll_opy_ = MultipartEncoder(
    fields={
      bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࠫੜ"): (os.path.basename(path), open(os.path.abspath(path), bstack1l111l1_opy_ (u"ࠧࡳࡤࠪ੝")), bstack1l111l1_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬਫ਼")),
      bstack1l111l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ੟"): bstack11l11l111l_opy_
    }
  )
  response = requests.post(bstack11llll11l_opy_, data=bstack1ll1llllll_opy_,
                           headers={bstack1l111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੠"): bstack1ll1llllll_opy_.content_type},
                           auth=(config[bstack1l111l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੡")], config[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੢")]))
  try:
    res = json.loads(response.text)
    bstack1ll1l11ll1_opy_ = res[bstack1l111l1_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੣")]
    logger.info(bstack1l11ll11ll_opy_.format(bstack1ll1l11ll1_opy_))
    bstack1ll11l11l1_opy_(md5_hash, bstack1ll1l11ll1_opy_)
    cli.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੤"), datetime.datetime.now() - bstack1ll11llll_opy_)
  except ValueError as err:
    bstack1l11lll1_opy_(bstack1111l1ll_opy_.format(str(err)))
  return bstack1ll1l11ll1_opy_
def bstack1l1l1l1ll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1lll1ll1l1_opy_
  bstack1l1l1lllll_opy_ = 1
  bstack11ll1111_opy_ = 1
  if bstack1l111l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੥") in CONFIG:
    bstack11ll1111_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੦")]
  else:
    bstack11ll1111_opy_ = bstack1l111l1111_opy_(framework_name, args) or 1
  if bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧") in CONFIG:
    bstack1l1l1lllll_opy_ = len(CONFIG[bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੨")])
  bstack1lll1ll1l1_opy_ = int(bstack11ll1111_opy_) * int(bstack1l1l1lllll_opy_)
def bstack1l111l1111_opy_(framework_name, args):
  if framework_name == bstack1l1lll1l1_opy_ and args and bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ੩") in args:
      bstack11l1l1111_opy_ = args.index(bstack1l111l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ੪"))
      return int(args[bstack11l1l1111_opy_ + 1]) or 1
  return 1
def bstack1lll1l1l1l_opy_(md5_hash):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ੫"))
    bstack11l1111ll_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠨࢀࠪ੬")), bstack1l111l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੭"), bstack1l111l1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ੮"))
    if os.path.exists(bstack11l1111ll_opy_):
      try:
        bstack1ll1ll1lll_opy_ = json.load(open(bstack11l1111ll_opy_, bstack1l111l1_opy_ (u"ࠫࡷࡨࠧ੯")))
        if md5_hash in bstack1ll1ll1lll_opy_:
          bstack1lllll1ll_opy_ = bstack1ll1ll1lll_opy_[md5_hash]
          bstack11l11ll11l_opy_ = datetime.datetime.now()
          bstack11l1l11lll_opy_ = datetime.datetime.strptime(bstack1lllll1ll_opy_[bstack1l111l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨੰ")], bstack1l111l1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪੱ"))
          if (bstack11l11ll11l_opy_ - bstack11l1l11lll_opy_).days > 30:
            return None
          elif version.parse(str(__version__)) > version.parse(bstack1lllll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬੲ")]):
            return None
          return bstack1lllll1ll_opy_[bstack1l111l1_opy_ (u"ࠨ࡫ࡧࠫੳ")]
      except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡐࡈ࠺ࠦࡨࡢࡵ࡫ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭ੴ").format(str(e)))
    return None
  bstack11l1111ll_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠪࢂࠬੵ")), bstack1l111l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੶"), bstack1l111l1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੷"))
  lock_file = bstack11l1111ll_opy_ + bstack1l111l1_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ੸")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l1111ll_opy_):
        with open(bstack11l1111ll_opy_, bstack1l111l1_opy_ (u"ࠧࡳࠩ੹")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1ll1lll_opy_ = json.loads(content)
            if md5_hash in bstack1ll1ll1lll_opy_:
              bstack1lllll1ll_opy_ = bstack1ll1ll1lll_opy_[md5_hash]
              bstack11l11ll11l_opy_ = datetime.datetime.now()
              bstack11l1l11lll_opy_ = datetime.datetime.strptime(bstack1lllll1ll_opy_[bstack1l111l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ੺")], bstack1l111l1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭੻"))
              if (bstack11l11ll11l_opy_ - bstack11l1l11lll_opy_).days > 30:
                return None
              elif version.parse(str(__version__)) > version.parse(bstack1lllll1ll_opy_[bstack1l111l1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ੼")]):
                return None
              return bstack1lllll1ll_opy_[bstack1l111l1_opy_ (u"ࠫ࡮ࡪࠧ੽")]
      return None
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮࠺ࠡࡽࢀࠫ੾").format(str(e)))
    return None
def bstack1ll11l11l1_opy_(md5_hash, bstack1ll1l11ll1_opy_):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ੿"))
    bstack1lll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠧࡿࠩ઀")), bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨઁ"))
    if not os.path.exists(bstack1lll1l1l1_opy_):
      os.makedirs(bstack1lll1l1l1_opy_)
    bstack11l1111ll_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠩࢁࠫં")), bstack1l111l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪઃ"), bstack1l111l1_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ઄"))
    bstack1lll1l111l_opy_ = {
      bstack1l111l1_opy_ (u"ࠬ࡯ࡤࠨઅ"): bstack1ll1l11ll1_opy_,
      bstack1l111l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩઆ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l111l1_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫઇ")),
      bstack1l111l1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ઈ"): str(__version__)
    }
    try:
      bstack1ll1ll1lll_opy_ = {}
      if os.path.exists(bstack11l1111ll_opy_):
        bstack1ll1ll1lll_opy_ = json.load(open(bstack11l1111ll_opy_, bstack1l111l1_opy_ (u"ࠩࡵࡦࠬઉ")))
      bstack1ll1ll1lll_opy_[md5_hash] = bstack1lll1l111l_opy_
      with open(bstack11l1111ll_opy_, bstack1l111l1_opy_ (u"ࠥࡻ࠰ࠨઊ")) as outfile:
        json.dump(bstack1ll1ll1lll_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡓࡄ࠶ࠢ࡫ࡥࡸ࡮ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩઋ").format(str(e)))
    return
  bstack1lll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠬࢄࠧઌ")), bstack1l111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"))
  if not os.path.exists(bstack1lll1l1l1_opy_):
    os.makedirs(bstack1lll1l1l1_opy_)
  bstack11l1111ll_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠧࡿࠩ઎")), bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨએ"), bstack1l111l1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪઐ"))
  lock_file = bstack11l1111ll_opy_ + bstack1l111l1_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩઑ")
  bstack1lll1l111l_opy_ = {
    bstack1l111l1_opy_ (u"ࠫ࡮ࡪࠧ઒"): bstack1ll1l11ll1_opy_,
    bstack1l111l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨઓ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l111l1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪઔ")),
    bstack1l111l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬક"): str(__version__)
  }
  try:
    with FileLock(lock_file, timeout=10):
      bstack1ll1ll1lll_opy_ = {}
      if os.path.exists(bstack11l1111ll_opy_):
        with open(bstack11l1111ll_opy_, bstack1l111l1_opy_ (u"ࠨࡴࠪખ")) as f:
          content = f.read().strip()
          if content:
            bstack1ll1ll1lll_opy_ = json.loads(content)
      bstack1ll1ll1lll_opy_[md5_hash] = bstack1lll1l111l_opy_
      with open(bstack11l1111ll_opy_, bstack1l111l1_opy_ (u"ࠤࡺࠦગ")) as outfile:
        json.dump(bstack1ll1ll1lll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡑࡉ࠻ࠠࡩࡣࡶ࡬ࠥࡻࡰࡥࡣࡷࡩ࠿ࠦࡻࡾࠩઘ").format(str(e)))
def bstack111ll1llll_opy_(self):
  return
def bstack11lll11lll_opy_(self):
  return
def bstack1l1111l11_opy_():
  global bstack1l11lllll_opy_
  bstack1l11lllll_opy_ = True
@measure(event_name=EVENTS.bstack1ll1l1l11l_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll11lll_opy_(self):
  global bstack1lll11ll1l_opy_
  global bstack1llll1ll1l_opy_
  global bstack1l11111l1l_opy_
  try:
    if bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫઙ") in bstack1lll11ll1l_opy_ and self.session_id != None and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩચ"), bstack1l111l1_opy_ (u"࠭ࠧછ")) != bstack1l111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨજ"):
      bstack1l1ll11l11_opy_ = bstack1l111l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨઝ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩઞ")
      if bstack1l1ll11l11_opy_ == bstack1l111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪટ"):
        bstack111l11l11_opy_(logger)
      if self != None:
        bstack11llll1ll_opy_(self, bstack1l1ll11l11_opy_, bstack1l111l1_opy_ (u"ࠫ࠱ࠦࠧઠ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l111l1_opy_ (u"ࠬ࠭ડ")
    if bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ઢ") in bstack1lll11ll1l_opy_ and getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ણ"), None):
      bstack1lllllllll_opy_.bstack1ll1l111ll_opy_(self, bstack11lll11l11_opy_, logger, wait=True)
    if bstack1l111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨત") in bstack1lll11ll1l_opy_:
      bstack1l1lllll1l_opy_.bstack111ll111_opy_(self)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥથ") + str(e))
  bstack1l11111l1l_opy_(self)
  self.session_id = None
def bstack11l111ll1l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1ll11l1ll_opy_
    global bstack1lll11ll1l_opy_
    command_executor = kwargs.get(bstack1l111l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭દ"), bstack1l111l1_opy_ (u"ࠫࠬધ"))
    bstack1l11l11ll_opy_ = False
    if type(command_executor) == str and bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨન") in command_executor:
      bstack1l11l11ll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ઩") in str(getattr(command_executor, bstack1l111l1_opy_ (u"ࠧࡠࡷࡵࡰࠬપ"), bstack1l111l1_opy_ (u"ࠨࠩફ"))):
      bstack1l11l11ll_opy_ = True
    else:
      kwargs = bstack11111l11l_opy_.bstack1ll1ll1l_opy_(bstack1ll1llll1l_opy_=kwargs, config=CONFIG)
      return bstack111lll1l1_opy_(self, *args, **kwargs)
    if bstack1l11l11ll_opy_:
      bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1ll1ll111_opy_(CONFIG, bstack1lll11ll1l_opy_)
      if kwargs.get(bstack1l111l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪબ")):
        kwargs[bstack1l111l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫભ")] = bstack1ll11l1ll_opy_(kwargs[bstack1l111l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬમ")], bstack1lll11ll1l_opy_, CONFIG, bstack1lll1111l1_opy_)
      elif kwargs.get(bstack1l111l1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬય")):
        kwargs[bstack1l111l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ર")] = bstack1ll11l1ll_opy_(kwargs[bstack1l111l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ઱")], bstack1lll11ll1l_opy_, CONFIG, bstack1lll1111l1_opy_)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣલ").format(str(e)))
  return bstack111lll1l1_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11111ll11_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack11l11lll_opy_(self, command_executor=bstack1l111l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱࠴࠶࠼࠴࠰࠯࠲࠱࠵࠿࠺࠴࠵࠶ࠥળ"), *args, **kwargs):
  global bstack1llll1ll1l_opy_
  global bstack1l11ll11_opy_
  bstack1l1l1ll1l1_opy_ = bstack11l111ll1l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11ll11l11_opy_.on():
    return bstack1l1l1ll1l1_opy_
  try:
    logger.debug(bstack1l111l1_opy_ (u"ࠪࡇࡴࡳ࡭ࡢࡰࡧࠤࡊࡾࡥࡤࡷࡷࡳࡷࠦࡷࡩࡧࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡪࡦࡲࡳࡦࠢ࠰ࠤࢀࢃࠧ઴").format(str(command_executor)))
    logger.debug(bstack1l111l1_opy_ (u"ࠫࡍࡻࡢࠡࡗࡕࡐࠥ࡯ࡳࠡ࠯ࠣࡿࢂ࠭વ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨશ") in command_executor._url:
      bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧષ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪસ") in command_executor):
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩહ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11ll1l1l1l_opy_ = getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ઺"), None)
  bstack111ll1ll11_opy_ = {}
  if self.capabilities is not None:
    bstack111ll1ll11_opy_[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ઻")] = self.capabilities.get(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦ઼ࠩ"))
    bstack111ll1ll11_opy_[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧઽ")] = self.capabilities.get(bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧા"))
    bstack111ll1ll11_opy_[bstack1l111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨિ")] = self.capabilities.get(bstack1l111l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ી"))
  if CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩુ"), False) and bstack11111l11l_opy_.bstack1l111llll_opy_(bstack111ll1ll11_opy_):
    threading.current_thread().a11yPlatform = True
  if bstack1l111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪૂ") in bstack1lll11ll1l_opy_ or bstack1l111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૃ") in bstack1lll11ll1l_opy_:
    bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(self)
  if bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬૄ") in bstack1lll11ll1l_opy_ and bstack11ll1l1l1l_opy_ and bstack11ll1l1l1l_opy_.get(bstack1l111l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ૅ"), bstack1l111l1_opy_ (u"ࠧࠨ૆")) == bstack1l111l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩે"):
    bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(self)
  bstack1llll1ll1l_opy_ = self.session_id
  with bstack1ll11l11_opy_:
    bstack1l11ll11_opy_.append(self)
  return bstack1l1l1ll1l1_opy_
def bstack1llll11ll1_opy_(args):
  return bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠪૈ") in str(args)
def bstack1ll11l11ll_opy_(self, driver_command, *args, **kwargs):
  global bstack1lll1l11_opy_
  global bstack1l1l1llll1_opy_
  bstack1ll1llll1_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧૉ"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ૊"), None)
  bstack1111l11l_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬો"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨૌ"), None)
  bstack1l111l1lll_opy_ = getattr(self, bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴ્ࠧ"), None) != None and getattr(self, bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ૎"), None) == True
  if not bstack1l1l1llll1_opy_ and bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ૏") in CONFIG and CONFIG[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪૐ")] == True and bstack1l111l1l_opy_.bstack111l11lll_opy_(driver_command) and (bstack1l111l1lll_opy_ or bstack1ll1llll1_opy_ or bstack1111l11l_opy_) and not bstack1llll11ll1_opy_(args):
    try:
      bstack1l1l1llll1_opy_ = True
      logger.debug(bstack1l111l1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭૑").format(driver_command))
      bstack1l11l1llll_opy_ = perform_scan(self, driver_command=driver_command)
      logger.debug(bstack1l11l1llll_opy_)
      try:
        bstack111l1l1l_opy_ = {
          bstack1l111l1_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨ૒"): {
            bstack1l111l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢ૓"): bstack1l111l1_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡃࡂࡐࠥ૔"),
            bstack1l111l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡥࡵࡧࡵࡷࠧ૕"): [
              {
                bstack1l111l1_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ૖"): driver_command
              }
            ]
          },
          bstack1l111l1_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧ૗"): {
            bstack1l111l1_opy_ (u"ࠦࡧࡵࡤࡺࠤ૘"): {
              bstack1l111l1_opy_ (u"ࠧࡳࡳࡨࠤ૙"): bstack1l11l1llll_opy_.get(bstack1l111l1_opy_ (u"ࠨ࡭ࡴࡩࠥ૚"), bstack1l111l1_opy_ (u"ࠢࠣ૛")) if isinstance(bstack1l11l1llll_opy_, dict) else bstack1l111l1_opy_ (u"ࠣࠤ૜"),
              bstack1l111l1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥ૝"): bstack1l11l1llll_opy_.get(bstack1l111l1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ૞"), True) if isinstance(bstack1l11l1llll_opy_, dict) else True
            }
          }
        }
        logger.debug(bstack1l111l1_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯ࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࡬ࡰࡩࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠬ૟").format(bstack111l1l1l_opy_))
        bstack1l1111ll1_opy_.info(json.dumps(bstack111l1l1l_opy_, separators=(bstack1l111l1_opy_ (u"ࠬ࠲ࠧૠ"), bstack1l111l1_opy_ (u"࠭࠺ࠨૡ"))))
      except Exception as bstack1lll11111l_opy_:
        logger.debug(bstack1l111l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠧૢ").format(str(bstack1lll11111l_opy_)))
    except Exception as err:
      logger.debug(bstack1l111l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ૣ").format(str(err)))
    bstack1l1l1llll1_opy_ = False
  response = bstack1lll1l11_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૤") in str(bstack1lll11ll1l_opy_).lower() or bstack1l111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ૥") in str(bstack1lll11ll1l_opy_).lower()) and bstack11ll11l11_opy_.on():
    try:
      if driver_command == bstack1l111l1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ૦"):
        bstack1llll1lll1_opy_.bstack1l111111l1_opy_({
            bstack1l111l1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ૧"): response[bstack1l111l1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ૨")],
            bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ૩"): bstack1llll1lll1_opy_.current_test_uuid() if bstack1llll1lll1_opy_.current_test_uuid() else bstack11ll11l11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll11lll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1llll1ll1l_opy_
  global bstack111llll11_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1l1111l1l_opy_
  global bstack1l11111l11_opy_
  global bstack1lll11ll1l_opy_
  global bstack111lll1l1_opy_
  global bstack1l11ll11_opy_
  global bstack11l1ll11l_opy_
  global bstack11lll11l11_opy_
  if os.getenv(bstack1l111l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭૪")) is not None and bstack11111l11l_opy_.bstack1l1lll11l_opy_(CONFIG) is None:
    CONFIG[bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ૫")] = True
  CONFIG[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ૬")] = str(bstack1lll11ll1l_opy_) + str(__version__)
  bstack1l1llll11_opy_ = os.environ[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ૭")]
  bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1ll1ll111_opy_(CONFIG, bstack1lll11ll1l_opy_)
  CONFIG[bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ૮")] = bstack1l1llll11_opy_
  CONFIG[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ૯")] = bstack1lll1111l1_opy_
  if CONFIG.get(bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ૰"),bstack1l111l1_opy_ (u"ࠨࠩ૱")) and bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૲") in bstack1lll11ll1l_opy_:
    CONFIG[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ૳")].pop(bstack1l111l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ૴"), None)
    CONFIG[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ૵")].pop(bstack1l111l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ૶"), None)
  command_executor = bstack1lllllll11_opy_()
  logger.debug(bstack111ll111l1_opy_.format(command_executor))
  proxy = bstack11lll111l_opy_(CONFIG, proxy)
  bstack1l1l11111l_opy_ = 0 if bstack111llll11_opy_ < 0 else bstack111llll11_opy_
  try:
    if bstack1l1111l1l_opy_ is True:
      bstack1l1l11111l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l11111l11_opy_ is True:
      bstack1l1l11111l_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1l11111l_opy_ = 0
  bstack1l11ll1l_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1l1l11111l_opy_)
  logger.debug(bstack1111ll11_opy_.format(str(bstack1l11ll1l_opy_)))
  if bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ૷") in CONFIG and bstack11lll111_opy_(CONFIG[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ૸")]):
    bstack11l111l1ll_opy_(bstack1l11ll1l_opy_)
  if bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack1l1l11111l_opy_) and bstack11111l11l_opy_.bstack11l11llll_opy_(bstack1l11ll1l_opy_, options, desired_capabilities, CONFIG):
    threading.current_thread().a11yPlatform = True
    if (cli.accessibility is None or not cli.accessibility.is_enabled()):
      bstack11111l11l_opy_.set_capabilities(bstack1l11ll1l_opy_, CONFIG)
  if desired_capabilities:
    bstack1l1ll1ll_opy_ = bstack11l1lll11_opy_(desired_capabilities)
    bstack1l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩૹ")] = bstack1llllllll_opy_(CONFIG)
    bstack111ll1lll_opy_ = bstack1l1ll111l_opy_(bstack1l1ll1ll_opy_)
    if bstack111ll1lll_opy_:
      bstack1l11ll1l_opy_ = update(bstack111ll1lll_opy_, bstack1l11ll1l_opy_)
    desired_capabilities = None
  if options:
    bstack11l1ll1l1l_opy_(options, bstack1l11ll1l_opy_)
  if not options:
    options = bstack111ll1l1_opy_(bstack1l11ll1l_opy_)
  bstack11lll11l11_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૺ"))[bstack1l1l11111l_opy_]
  if proxy and bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫૻ")):
    options.proxy(proxy)
  if options and bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫૼ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111l1111l_opy_() < version.parse(bstack1l111l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ૽")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11ll1l_opy_)
  logger.info(bstack1ll1l11l_opy_)
  bstack11lll1l1ll_opy_.end(EVENTS.bstack1l1l11ll1_opy_.value, EVENTS.bstack1l1l11ll1_opy_.value + bstack1l111l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ૾"), EVENTS.bstack1l1l11ll1_opy_.value + bstack1l111l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ૿"), status=True, failure=None, test_name=bstack1l1l1l1ll1_opy_)
  if bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡴࡷࡵࡦࡪ࡮ࡨࠫ଀") in kwargs:
    del kwargs[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡵࡸ࡯ࡧ࡫࡯ࡩࠬଁ")]
  try:
    if bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫଂ")):
      bstack111lll1l1_opy_(self, command_executor=command_executor,
                options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
    elif bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫଃ")):
      bstack111lll1l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities, options=options,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭଄")):
      bstack111lll1l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive, file_detector=file_detector)
    else:
      bstack111lll1l1_opy_(self, command_executor=command_executor,
                desired_capabilities=desired_capabilities,
                browser_profile=browser_profile, proxy=proxy,
                keep_alive=keep_alive)
  except Exception as bstack1l1ll1ll11_opy_:
    logger.error(bstack11l11lll11_opy_.format(bstack1l111l1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰ࠭ଅ"), str(bstack1l1ll1ll11_opy_)))
    raise bstack1l1ll1ll11_opy_
  if bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack1l1l11111l_opy_) and bstack11111l11l_opy_.bstack11l11llll_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪଆ")][bstack1l111l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨଇ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11111l11l_opy_.set_capabilities(bstack1l11ll1l_opy_, CONFIG)
  try:
    bstack11lll1l111_opy_ = bstack1l111l1_opy_ (u"ࠪࠫଈ")
    if bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬଉ")):
      if self.caps is not None:
        bstack11lll1l111_opy_ = self.caps.get(bstack1l111l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧଊ"))
    else:
      if self.capabilities is not None:
        bstack11lll1l111_opy_ = self.capabilities.get(bstack1l111l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨଋ"))
    if bstack11lll1l111_opy_:
      bstack111lll1111_opy_(bstack11lll1l111_opy_)
      if bstack111l1111l_opy_() <= version.parse(bstack1l111l1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧଌ")):
        self.command_executor._url = bstack1l111l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ଍") + bstack1l1l1l11l1_opy_ + bstack1l111l1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ଎")
      else:
        self.command_executor._url = bstack1l111l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧଏ") + bstack11lll1l111_opy_ + bstack1l111l1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧଐ")
      logger.debug(bstack1l111l1ll1_opy_.format(bstack11lll1l111_opy_))
    else:
      logger.debug(bstack1ll11l1l1l_opy_.format(bstack1l111l1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ଑")))
  except Exception as e:
    logger.debug(bstack1ll11l1l1l_opy_.format(e))
  if bstack1l111l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ଒") in bstack1lll11ll1l_opy_:
    bstack1ll1ll1111_opy_(bstack111llll11_opy_, bstack11l1ll11l_opy_)
  bstack1llll1ll1l_opy_ = self.session_id
  if bstack1l111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧଓ") in bstack1lll11ll1l_opy_ or bstack1l111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨଔ") in bstack1lll11ll1l_opy_ or bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨକ") in bstack1lll11ll1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11ll1l1l1l_opy_ = getattr(threading.current_thread(), bstack1l111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫଖ"), None)
  if bstack1l111l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫଗ") in bstack1lll11ll1l_opy_ or bstack1l111l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫଘ") in bstack1lll11ll1l_opy_:
    bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(self)
  if bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ଙ") in bstack1lll11ll1l_opy_ and bstack11ll1l1l1l_opy_ and bstack11ll1l1l1l_opy_.get(bstack1l111l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧଚ"), bstack1l111l1_opy_ (u"ࠨࠩଛ")) == bstack1l111l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪଜ"):
    bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(self)
  with bstack1ll11l11_opy_:
    bstack1l11ll11_opy_.append(self)
  if bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଝ") in CONFIG and bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଞ") in CONFIG[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଟ")][bstack1l1l11111l_opy_]:
    bstack1l1l1l1ll1_opy_ = CONFIG[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")][bstack1l1l11111l_opy_][bstack1l111l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଡ")]
  logger.debug(bstack1l11l11l_opy_.format(bstack1llll1ll1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1111ll1l_opy_
    def bstack11l1llll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l1111111_opy_
      if(bstack1l111l1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥଢ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠩࢁࠫଣ")), bstack1l111l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪତ"), bstack1l111l1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ଥ")), bstack1l111l1_opy_ (u"ࠬࡽࠧଦ")) as fp:
          fp.write(bstack1l111l1_opy_ (u"ࠨࠢଧ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l111l1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤନ")))):
          with open(args[1], bstack1l111l1_opy_ (u"ࠨࡴࠪ଩")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l111l1_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨପ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11l111l1_opy_)
            if bstack1l111l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧଫ") in CONFIG and str(CONFIG[bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨବ")]).lower() != bstack1l111l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫଭ"):
                bstack1l11l111ll_opy_ = bstack1111ll1l_opy_()
                bstack1l1l111111_opy_ = bstack1l111l1_opy_ (u"࠭ࠧࠨࠌ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࠽ࠍࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࠽ࠍࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࠎ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࢀࠐࠠࠡ࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࠎࠥࠦࡴࡳࡻࠣࡿࢀࠐࠠࠡࠢࠣࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡁࠊࠡࠢࢀࢁࠥࡩࡡࡵࡥ࡫ࠤ࠭࡫ࡸࠪࠢࡾࡿࠏࠦࠠࠡࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࡩࡷࡸ࡯ࡳࠪࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠧ࠲ࠠࡦࡺࠬ࠿ࠏࠦࠠࡾࡿࠍࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁࡻࠋࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࠫࢀࡩࡤࡱࡗࡵࡰࢂ࠭ࠠࠬࠢࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩ࠭ࠌࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠌࠣࠤࢂࢃࠩ࠼ࠌࢀࢁࡀࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࠪࠫࠬମ").format(bstack1l11l111ll_opy_=bstack1l11l111ll_opy_)
            lines.insert(1, bstack1l1l111111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l111l1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤଯ")), bstack1l111l1_opy_ (u"ࠨࡹࠪର")) as bstack1111lll11_opy_:
              bstack1111lll11_opy_.writelines(lines)
        CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ଱")] = str(bstack1lll11ll1l_opy_) + str(__version__)
        bstack1l1llll11_opy_ = os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨଲ")]
        bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1ll1ll111_opy_(CONFIG, bstack1lll11ll1l_opy_)
        CONFIG[bstack1l111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧଳ")] = bstack1l1llll11_opy_
        CONFIG[bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ଴")] = bstack1lll1111l1_opy_
        bstack1l1l11111l_opy_ = 0 if bstack111llll11_opy_ < 0 else bstack111llll11_opy_
        try:
          if bstack1l1111l1l_opy_ is True:
            bstack1l1l11111l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l11111l11_opy_ is True:
            bstack1l1l11111l_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1l11111l_opy_ = 0
        CONFIG[bstack1l111l1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨଵ")] = False
        CONFIG[bstack1l111l1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨଶ")] = True
        bstack1l11ll1l_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1l1l11111l_opy_)
        logger.debug(bstack1111ll11_opy_.format(str(bstack1l11ll1l_opy_)))
        if CONFIG.get(bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬଷ")):
          bstack11l111l1ll_opy_(bstack1l11ll1l_opy_)
        if bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬସ") in CONFIG and bstack1l111l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨହ") in CONFIG[bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ଺")][bstack1l1l11111l_opy_]:
          bstack1l1l1l1ll1_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ଻")][bstack1l1l11111l_opy_][bstack1l111l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨ଼ࠫ")]
        args.append(os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠧࡿࠩଽ")), bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨା"), bstack1l111l1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫି")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11ll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l111l1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧୀ"))
      bstack11l1111111_opy_ = True
      return bstack1l111l111_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack111ll1l1l1_opy_(self,
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
    global bstack111llll11_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1l1111l1l_opy_
    global bstack1l11111l11_opy_
    global bstack1lll11ll1l_opy_
    CONFIG[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ୁ")] = str(bstack1lll11ll1l_opy_) + str(__version__)
    bstack1l1llll11_opy_ = os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪୂ")]
    bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1ll1ll111_opy_(CONFIG, bstack1lll11ll1l_opy_)
    CONFIG[bstack1l111l1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩୃ")] = bstack1l1llll11_opy_
    CONFIG[bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩୄ")] = bstack1lll1111l1_opy_
    bstack1l1l11111l_opy_ = 0 if bstack111llll11_opy_ < 0 else bstack111llll11_opy_
    try:
      if bstack1l1111l1l_opy_ is True:
        bstack1l1l11111l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l11111l11_opy_ is True:
        bstack1l1l11111l_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1l11111l_opy_ = 0
    CONFIG[bstack1l111l1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ୅")] = True
    bstack1l11ll1l_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack1l1l11111l_opy_)
    logger.debug(bstack1111ll11_opy_.format(str(bstack1l11ll1l_opy_)))
    if CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭୆")):
      bstack11l111l1ll_opy_(bstack1l11ll1l_opy_)
    if bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭େ") in CONFIG and bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩୈ") in CONFIG[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୉")][bstack1l1l11111l_opy_]:
      bstack1l1l1l1ll1_opy_ = CONFIG[bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୊")][bstack1l1l11111l_opy_][bstack1l111l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬୋ")]
    import urllib
    import json
    if bstack1l111l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬୌ") in CONFIG and str(CONFIG[bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ୍࠭")]).lower() != bstack1l111l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ୎"):
        bstack1l111l111l_opy_ = bstack1111ll1l_opy_()
        bstack1l11l111ll_opy_ = bstack1l111l111l_opy_ + urllib.parse.quote(json.dumps(bstack1l11ll1l_opy_))
    else:
        bstack1l11l111ll_opy_ = bstack1l111l1_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭୏") + urllib.parse.quote(json.dumps(bstack1l11ll1l_opy_))
    browser = self.connect(bstack1l11l111ll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1ll1lll_opy_():
    global bstack11l1111111_opy_
    global bstack1lll11ll1l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1111l1lll_opy_
        global bstack1l1l1111_opy_
        if not bstack11l1ll1l1_opy_:
          global bstack11ll11lll_opy_
          if not bstack11ll11lll_opy_:
            from bstack_utils.helper import bstack1111l1l11_opy_, bstack111ll1l111_opy_, bstack1ll1lllll_opy_
            bstack11ll11lll_opy_ = bstack1111l1l11_opy_()
            bstack111ll1l111_opy_(bstack1lll11ll1l_opy_)
            bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1ll1ll111_opy_(CONFIG, bstack1lll11ll1l_opy_)
            bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ୐"), bstack1lll1111l1_opy_)
          BrowserType.connect = bstack1111l1lll_opy_
          return
        BrowserType.launch = bstack111ll1l1l1_opy_
        bstack11l1111111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l1llll_opy_
      bstack11l1111111_opy_ = True
    except Exception as e:
      pass
def bstack1lll1l111_opy_(context, bstack1lllllll1l_opy_):
  try:
    if getattr(context, bstack1l111l1_opy_ (u"࠭ࡰࡢࡩࡨࠫ୑"), None):
      context.page.evaluate(bstack1l111l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ୒"), bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ୓")+ json.dumps(bstack1lllllll1l_opy_) + bstack1l111l1_opy_ (u"ࠤࢀࢁࠧ୔"))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧ୕").format(str(e), traceback.format_exc()))
def bstack1l1l1l1l11_opy_(context, message, level):
  try:
    if getattr(context, bstack1l111l1_opy_ (u"ࠫࡵࡧࡧࡦࠩୖ"), None):
      context.page.evaluate(bstack1l111l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨୗ"), bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ୘") + json.dumps(message) + bstack1l111l1_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ୙") + json.dumps(level) + bstack1l111l1_opy_ (u"ࠨࡿࢀࠫ୚"))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁ࠿ࠦࡻࡾࠤ୛").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack1l1ll11l_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1l11ll1ll_opy_(self, url):
  global bstack1ll1l1lll_opy_
  try:
    bstack111llllll1_opy_(url)
  except Exception as err:
    logger.debug(bstack111ll11ll1_opy_.format(str(err)))
  try:
    bstack1ll1l1lll_opy_(self, url)
  except Exception as e:
    try:
      bstack1llllll11l_opy_ = str(e)
      if any(err_msg in bstack1llllll11l_opy_ for err_msg in bstack1l11lll11l_opy_):
        bstack111llllll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111ll11ll1_opy_.format(str(err)))
    raise e
def bstack1l1ll11ll_opy_(self):
  global bstack11l1l1ll11_opy_
  bstack11l1l1ll11_opy_ = self
  return
def bstack11l11lllll_opy_(self):
  global bstack11llllllll_opy_
  bstack11llllllll_opy_ = self
  return
def bstack1l11l1l1l_opy_(test_name, bstack1lll11lll1_opy_):
  global CONFIG
  if percy.bstack1111111l1_opy_() == bstack1l111l1_opy_ (u"ࠥࡸࡷࡻࡥࠣଡ଼"):
    bstack11l11llll1_opy_ = os.path.relpath(bstack1lll11lll1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l11llll1_opy_)
    bstack111l1l11_opy_ = suite_name + bstack1l111l1_opy_ (u"ࠦ࠲ࠨଢ଼") + test_name
    threading.current_thread().percySessionName = bstack111l1l11_opy_
def bstack1l1ll1l1ll_opy_(self, test, *args, **kwargs):
  global bstack11lllll1_opy_
  test_name = None
  bstack1lll11lll1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1lll11lll1_opy_ = str(test.source)
  bstack1l11l1l1l_opy_(test_name, bstack1lll11lll1_opy_)
  bstack11lllll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1lll1l1111_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll1l111l1_opy_(driver, bstack111l1l11_opy_):
  if not bstack1ll1l1ll1_opy_ and bstack111l1l11_opy_:
      bstack11l1ll1ll_opy_ = {
          bstack1l111l1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ୞"): bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧୟ"),
          bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪୠ"): {
              bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ୡ"): bstack111l1l11_opy_
          }
      }
      bstack1l1lllllll_opy_ = bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧୢ").format(json.dumps(bstack11l1ll1ll_opy_))
      driver.execute_script(bstack1l1lllllll_opy_)
  if bstack1l111lll_opy_:
      bstack1l11l11lll_opy_ = {
          bstack1l111l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪୣ"): bstack1l111l1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭୤"),
          bstack1l111l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ୥"): {
              bstack1l111l1_opy_ (u"࠭ࡤࡢࡶࡤࠫ୦"): bstack111l1l11_opy_ + bstack1l111l1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ୧"),
              bstack1l111l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ୨"): bstack1l111l1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ୩")
          }
      }
      if bstack1l111lll_opy_.status == bstack1l111l1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨ୪"):
          bstack1l1l11lll_opy_ = bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ୫").format(json.dumps(bstack1l11l11lll_opy_))
          driver.execute_script(bstack1l1l11lll_opy_)
          bstack11llll1ll_opy_(driver, bstack1l111l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୬"))
      elif bstack1l111lll_opy_.status == bstack1l111l1_opy_ (u"࠭ࡆࡂࡋࡏࠫ୭"):
          reason = bstack1l111l1_opy_ (u"ࠢࠣ୮")
          bstack1llll11l11_opy_ = bstack111l1l11_opy_ + bstack1l111l1_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠩ୯")
          if bstack1l111lll_opy_.message:
              reason = str(bstack1l111lll_opy_.message)
              bstack1llll11l11_opy_ = bstack1llll11l11_opy_ + bstack1l111l1_opy_ (u"ࠩࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࠩ୰") + reason
          bstack1l11l11lll_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ୱ")] = {
              bstack1l111l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ୲"): bstack1l111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ୳"),
              bstack1l111l1_opy_ (u"࠭ࡤࡢࡶࡤࠫ୴"): bstack1llll11l11_opy_
          }
          bstack1l1l11lll_opy_ = bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ୵").format(json.dumps(bstack1l11l11lll_opy_))
          driver.execute_script(bstack1l1l11lll_opy_)
          bstack11llll1ll_opy_(driver, bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ୶"), reason)
          bstack1llll11lll_opy_(reason, str(bstack1l111lll_opy_), str(bstack111llll11_opy_), logger)
@measure(event_name=EVENTS.bstack11l1llllll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack111lllll_opy_(driver, test):
  if percy.bstack1111111l1_opy_() == bstack1l111l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ୷") and percy.bstack1l1ll1ll1l_opy_() == bstack1l111l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ୸"):
      bstack111llll11l_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ୹"), None)
      bstack11l1111lll_opy_(driver, bstack111llll11l_opy_, test)
  if (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ୺"), None) and
      bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ୻"), None)) or (
      bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ୼"), None) and
      bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ୽"), None)):
      logger.info(bstack1l111l1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤ୾"))
      bstack11111l11l_opy_.bstack1lll1l1l_opy_(driver, name=test.name, path=test.source)
def bstack1l1l111l1l_opy_(test, bstack111l1l11_opy_):
    try:
      bstack1ll11llll_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ୿")] = bstack111l1l11_opy_
      if bstack1l111lll_opy_:
        if bstack1l111lll_opy_.status == bstack1l111l1_opy_ (u"ࠫࡕࡇࡓࡔࠩ஀"):
          data[bstack1l111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ஁")] = bstack1l111l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ஂ")
        elif bstack1l111lll_opy_.status == bstack1l111l1_opy_ (u"ࠧࡇࡃࡌࡐࠬஃ"):
          data[bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ஄")] = bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஅ")
          if bstack1l111lll_opy_.message:
            data[bstack1l111l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪஆ")] = str(bstack1l111lll_opy_.message)
      user = CONFIG[bstack1l111l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭இ")]
      key = CONFIG[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஈ")]
      host = bstack1llll1l1ll_opy_(cli.config, [bstack1l111l1_opy_ (u"ࠨࡡࡱ࡫ࡶࠦஉ"), bstack1l111l1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤஊ"), bstack1l111l1_opy_ (u"ࠣࡣࡳ࡭ࠧ஋")], bstack1l111l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥ஌"))
      url = bstack1l111l1_opy_ (u"ࠪࡿࢂ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ஍").format(host, bstack1llll1ll1l_opy_)
      headers = {
        bstack1l111l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪஎ"): bstack1l111l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨஏ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers, auth=(user, key))
        cli.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡺࡶࡤࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠥஐ"), datetime.datetime.now() - bstack1ll11llll_opy_)
    except Exception as e:
      logger.error(bstack1ll111ll11_opy_.format(str(e)))
def bstack1ll1lll1l1_opy_(test, bstack111l1l11_opy_):
  global CONFIG
  global bstack11llllllll_opy_
  global bstack11l1l1ll11_opy_
  global bstack1llll1ll1l_opy_
  global bstack1l111lll_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1l1ll111ll_opy_
  global bstack1l1l11ll1l_opy_
  global bstack1l1l11l1ll_opy_
  global bstack11l11l111_opy_
  global bstack1l11ll11_opy_
  global bstack11lll11l11_opy_
  global bstack1l11l1ll1_opy_
  try:
    if not bstack1llll1ll1l_opy_:
      with bstack1l11l1ll1_opy_:
        bstack1l1l11l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠧࡿࠩ஑")), bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨஒ"), bstack1l111l1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫஓ"))
        if os.path.exists(bstack1l1l11l1_opy_):
          with open(bstack1l1l11l1_opy_, bstack1l111l1_opy_ (u"ࠪࡶࠬஔ")) as f:
            content = f.read().strip()
            if content:
              bstack11l11lll1l_opy_ = json.loads(bstack1l111l1_opy_ (u"ࠦࢀࠨக") + content + bstack1l111l1_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ஖") + bstack1l111l1_opy_ (u"ࠨࡽࠣ஗"))
              bstack1llll1ll1l_opy_ = bstack11l11lll1l_opy_.get(str(threading.get_ident()))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡋࡇࡷࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ஘") + str(e))
  if bstack1l11ll11_opy_:
    with bstack1ll11l11_opy_:
      bstack11ll11l1ll_opy_ = bstack1l11ll11_opy_.copy()
    for driver in bstack11ll11l1ll_opy_:
      if bstack1llll1ll1l_opy_ == driver.session_id:
        if test:
          bstack111lllll_opy_(driver, test)
        bstack1ll1l111l1_opy_(driver, bstack111l1l11_opy_)
  elif bstack1llll1ll1l_opy_:
    bstack1l1l111l1l_opy_(test, bstack111l1l11_opy_)
  if bstack11llllllll_opy_:
    bstack1l1l11ll1l_opy_(bstack11llllllll_opy_)
  if bstack11l1l1ll11_opy_:
    bstack1l1l11l1ll_opy_(bstack11l1l1ll11_opy_)
  if bstack1l11lllll_opy_:
    bstack11l11l111_opy_()
def bstack11ll1ll111_opy_(self, test, *args, **kwargs):
  bstack111l1l11_opy_ = None
  if test:
    bstack111l1l11_opy_ = str(test.name)
  bstack1ll1lll1l1_opy_(test, bstack111l1l11_opy_)
  bstack1l1ll111ll_opy_(self, test, *args, **kwargs)
def bstack1ll1lll1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll11ll11_opy_
  global CONFIG
  global bstack1l11ll11_opy_
  global bstack1llll1ll1l_opy_
  global bstack1l11l1ll1_opy_
  bstack1l1l11lll1_opy_ = None
  try:
    if bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧங"), None) or bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫச"), None):
      try:
        if not bstack1llll1ll1l_opy_:
          bstack1l1l11l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠪࢂࠬ஛")), bstack1l111l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫஜ"), bstack1l111l1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ஝"))
          with bstack1l11l1ll1_opy_:
            if os.path.exists(bstack1l1l11l1_opy_):
              with open(bstack1l1l11l1_opy_, bstack1l111l1_opy_ (u"࠭ࡲࠨஞ")) as f:
                content = f.read().strip()
                if content:
                  bstack11l11lll1l_opy_ = json.loads(bstack1l111l1_opy_ (u"ࠢࡼࠤட") + content + bstack1l111l1_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ஠") + bstack1l111l1_opy_ (u"ࠤࢀࠦ஡"))
                  bstack1llll1ll1l_opy_ = bstack11l11lll1l_opy_.get(str(threading.get_ident()))
      except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࡳࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠩ஢") + str(e))
      if bstack1l11ll11_opy_:
        with bstack1ll11l11_opy_:
          bstack11ll11l1ll_opy_ = bstack1l11ll11_opy_.copy()
        for driver in bstack11ll11l1ll_opy_:
          if bstack1llll1ll1l_opy_ == driver.session_id:
            bstack1l1l11lll1_opy_ = driver
    bstack11lll1l11_opy_ = bstack11111l11l_opy_.bstack11l1l11111_opy_(test.tags)
    if bstack1l1l11lll1_opy_:
      threading.current_thread().isA11yTest = bstack11111l11l_opy_.bstack111l1ll1l_opy_(bstack1l1l11lll1_opy_, bstack11lll1l11_opy_)
      threading.current_thread().isAppA11yTest = bstack11111l11l_opy_.bstack111l1ll1l_opy_(bstack1l1l11lll1_opy_, bstack11lll1l11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11lll1l11_opy_
      threading.current_thread().isAppA11yTest = bstack11lll1l11_opy_
  except:
    pass
  bstack1lll11ll11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l111lll_opy_
  try:
    bstack1l111lll_opy_ = self._test
  except:
    bstack1l111lll_opy_ = self.test
def bstack1llllll111_opy_():
  global bstack11lll1lll1_opy_
  try:
    if os.path.exists(bstack11lll1lll1_opy_):
      os.remove(bstack11lll1lll1_opy_)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧண") + str(e))
def bstack1l1l11ll_opy_():
  global bstack11lll1lll1_opy_
  bstack11lll1ll1_opy_ = {}
  lock_file = bstack11lll1lll1_opy_ + bstack1l111l1_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫத")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩ஥"))
    try:
      if not os.path.isfile(bstack11lll1lll1_opy_):
        with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠧࡸࠩ஦")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11lll1lll1_opy_):
        with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠨࡴࠪ஧")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1ll1_opy_ = json.loads(content)
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫந") + str(e))
    return bstack11lll1ll1_opy_
  try:
    os.makedirs(os.path.dirname(bstack11lll1lll1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      if not os.path.isfile(bstack11lll1lll1_opy_):
        with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠪࡻࠬன")) as f:
          json.dump({}, f)
      if os.path.exists(bstack11lll1lll1_opy_):
        with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠫࡷ࠭ப")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1ll1_opy_ = json.loads(content)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ஫") + str(e))
  finally:
    return bstack11lll1ll1_opy_
def bstack1ll1ll1111_opy_(platform_index, item_index):
  global bstack11lll1lll1_opy_
  lock_file = bstack11lll1lll1_opy_ + bstack1l111l1_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ஬")
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ஭"))
    try:
      bstack11lll1ll1_opy_ = {}
      if os.path.exists(bstack11lll1lll1_opy_):
        with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠨࡴࠪம")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1ll1_opy_ = json.loads(content)
      bstack11lll1ll1_opy_[item_index] = platform_index
      with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠤࡺࠦய")) as outfile:
        json.dump(bstack11lll1ll1_opy_, outfile)
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨர") + str(e))
    return
  try:
    os.makedirs(os.path.dirname(bstack11lll1lll1_opy_), exist_ok=True)
    with FileLock(lock_file, timeout=10):
      bstack11lll1ll1_opy_ = {}
      if os.path.exists(bstack11lll1lll1_opy_):
        with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠫࡷ࠭ற")) as f:
          content = f.read().strip()
          if content:
            bstack11lll1ll1_opy_ = json.loads(content)
      bstack11lll1ll1_opy_[item_index] = platform_index
      with open(bstack11lll1lll1_opy_, bstack1l111l1_opy_ (u"ࠧࡽࠢல")) as outfile:
        json.dump(bstack11lll1ll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫள") + str(e))
def bstack11lll1111_opy_(bstack111l11111_opy_):
  global CONFIG
  bstack1ll1ll1l1_opy_ = bstack1l111l1_opy_ (u"ࠧࠨழ")
  if not bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫவ") in CONFIG:
    logger.info(bstack1l111l1_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ஶ"))
  try:
    platform = CONFIG[bstack1l111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஷ")][bstack111l11111_opy_]
    if bstack1l111l1_opy_ (u"ࠫࡴࡹࠧஸ") in platform:
      bstack1ll1ll1l1_opy_ += str(platform[bstack1l111l1_opy_ (u"ࠬࡵࡳࠨஹ")]) + bstack1l111l1_opy_ (u"࠭ࠬࠡࠩ஺")
    if bstack1l111l1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஻") in platform:
      bstack1ll1ll1l1_opy_ += str(platform[bstack1l111l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ஼")]) + bstack1l111l1_opy_ (u"ࠩ࠯ࠤࠬ஽")
    if bstack1l111l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧா") in platform:
      bstack1ll1ll1l1_opy_ += str(platform[bstack1l111l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨி")]) + bstack1l111l1_opy_ (u"ࠬ࠲ࠠࠨீ")
    if bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨு") in platform:
      bstack1ll1ll1l1_opy_ += str(platform[bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩூ")]) + bstack1l111l1_opy_ (u"ࠨ࠮ࠣࠫ௃")
    if bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ௄") in platform:
      bstack1ll1ll1l1_opy_ += str(platform[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ௅")]) + bstack1l111l1_opy_ (u"ࠫ࠱ࠦࠧெ")
    if bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ே") in platform:
      bstack1ll1ll1l1_opy_ += str(platform[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧை")]) + bstack1l111l1_opy_ (u"ࠧ࠭ࠢࠪ௉")
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨொ") + str(e))
  finally:
    if bstack1ll1ll1l1_opy_[len(bstack1ll1ll1l1_opy_) - 2:] == bstack1l111l1_opy_ (u"ࠩ࠯ࠤࠬோ"):
      bstack1ll1ll1l1_opy_ = bstack1ll1ll1l1_opy_[:-2]
    return bstack1ll1ll1l1_opy_
def bstack1lll1ll11_opy_(path, bstack1ll1ll1l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l111l111_opy_ = ET.parse(path)
    bstack1llllllll1_opy_ = bstack11l111l111_opy_.getroot()
    bstack1l1llll1ll_opy_ = None
    for suite in bstack1llllllll1_opy_.iter(bstack1l111l1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩௌ")):
      if bstack1l111l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨ்ࠫ") in suite.attrib:
        suite.attrib[bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௎")] += bstack1l111l1_opy_ (u"࠭ࠠࠨ௏") + bstack1ll1ll1l1_opy_
        bstack1l1llll1ll_opy_ = suite
    bstack11l1lll1_opy_ = None
    for robot in bstack1llllllll1_opy_.iter(bstack1l111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ௐ")):
      bstack11l1lll1_opy_ = robot
    bstack1l1l1lll11_opy_ = len(bstack11l1lll1_opy_.findall(bstack1l111l1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௑")))
    if bstack1l1l1lll11_opy_ == 1:
      bstack11l1lll1_opy_.remove(bstack11l1lll1_opy_.findall(bstack1l111l1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௒"))[0])
      bstack1l11llll11_opy_ = ET.Element(bstack1l111l1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௓"), attrib={bstack1l111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௔"): bstack1l111l1_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬ௕"), bstack1l111l1_opy_ (u"࠭ࡩࡥࠩ௖"): bstack1l111l1_opy_ (u"ࠧࡴ࠲ࠪௗ")})
      bstack11l1lll1_opy_.insert(1, bstack1l11llll11_opy_)
      bstack11l1111ll1_opy_ = None
      for suite in bstack11l1lll1_opy_.iter(bstack1l111l1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௘")):
        bstack11l1111ll1_opy_ = suite
      bstack11l1111ll1_opy_.append(bstack1l1llll1ll_opy_)
      bstack11l11ll1_opy_ = None
      for status in bstack1l1llll1ll_opy_.iter(bstack1l111l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ௙")):
        bstack11l11ll1_opy_ = status
      bstack11l1111ll1_opy_.append(bstack11l11ll1_opy_)
    bstack11l111l111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ௚") + str(e))
def bstack1l1lll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1lll1lll11_opy_
  global CONFIG
  if bstack1l111l1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ௛") in options:
    del options[bstack1l111l1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ௜")]
  bstack11ll11ll11_opy_ = bstack1l1l11ll_opy_()
  for item_id in bstack11ll11ll11_opy_.keys():
    path = os.path.join(outs_dir, str(item_id), bstack1l111l1_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪ௝"))
    bstack1lll1ll11_opy_(path, bstack11lll1111_opy_(bstack11ll11ll11_opy_[item_id]))
  bstack1llllll111_opy_()
  return bstack1lll1lll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll111l111_opy_(self, ff_profile_dir):
  global bstack1lll11lll_opy_
  if not ff_profile_dir:
    return None
  return bstack1lll11lll_opy_(self, ff_profile_dir)
def bstack11l11l1111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll111l1_opy_
  bstack1llll1ll_opy_ = []
  if bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௞") in CONFIG:
    bstack1llll1ll_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௟")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l111l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥ௠")],
      pabot_args[bstack1l111l1_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ௡")],
      argfile,
      pabot_args.get(bstack1l111l1_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ௢")),
      pabot_args[bstack1l111l1_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ௣")],
      platform[0],
      bstack1lll111l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l111l1_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ௤")] or [(bstack1l111l1_opy_ (u"ࠢࠣ௥"), None)]
    for platform in enumerate(bstack1llll1ll_opy_)
  ]
def bstack1ll1l1lll1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1l1lllll_opy_=bstack1l111l1_opy_ (u"ࠨࠩ௦")):
  global bstack1l11lll1ll_opy_
  self.platform_index = platform_index
  self.bstack1l1lll1l_opy_ = bstack1l1lllll_opy_
  bstack1l11lll1ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll1l11l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1111l11l1_opy_
  global bstack11111l1l_opy_
  bstack1ll11ll111_opy_ = copy.deepcopy(item)
  if not bstack1l111l1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ௧") in item.options:
    bstack1ll11ll111_opy_.options[bstack1l111l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௨")] = []
  bstack111lllll1l_opy_ = bstack1ll11ll111_opy_.options[bstack1l111l1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௩")].copy()
  for v in bstack1ll11ll111_opy_.options[bstack1l111l1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௪")]:
    if bstack1l111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ௫") in v:
      bstack111lllll1l_opy_.remove(v)
    if bstack1l111l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ௬") in v:
      bstack111lllll1l_opy_.remove(v)
    if bstack1l111l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ௭") in v:
      bstack111lllll1l_opy_.remove(v)
  bstack111lllll1l_opy_.insert(0, bstack1l111l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ௮").format(bstack1ll11ll111_opy_.platform_index))
  bstack111lllll1l_opy_.insert(0, bstack1l111l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ௯").format(bstack1ll11ll111_opy_.bstack1l1lll1l_opy_))
  bstack1ll11ll111_opy_.options[bstack1l111l1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௰")] = bstack111lllll1l_opy_
  if bstack11111l1l_opy_:
    bstack1ll11ll111_opy_.options[bstack1l111l1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௱")].insert(0, bstack1l111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ௲").format(bstack11111l1l_opy_))
  return bstack1111l11l1_opy_(caller_id, datasources, is_last, bstack1ll11ll111_opy_, outs_dir)
def bstack1l11l11111_opy_(command, item_index):
  try:
    if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ௳")):
      os.environ[bstack1l111l1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ௴")] = json.dumps(CONFIG[bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௵")][item_index % bstack1lll11l1_opy_])
    global bstack11111l1l_opy_
    if bstack11111l1l_opy_:
      command[0] = command[0].replace(bstack1l111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௶"), bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ௷") + str(item_index % bstack1lll11l1_opy_) + bstack1l111l1_opy_ (u"ࠬࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭௸") + str(
        item_index) + bstack1l111l1_opy_ (u"࠭ࠠࠨ௹") + bstack11111l1l_opy_, 1)
    else:
      command[0] = command[0].replace(bstack1l111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௺"),
                                      bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ௻") +  str(item_index % bstack1lll11l1_opy_) + bstack1l111l1_opy_ (u"ࠩࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ௼") + str(item_index), 1)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡰࡳࡩ࡯ࡦࡺ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦࡦࡰࡴࠣࡴࡦࡨ࡯ࡵࠢࡵࡹࡳࡀࠠࡼࡿࠪ௽").format(str(e)))
def bstack11l1ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11l1l11_opy_
  try:
    bstack1l11l11111_opy_(command, item_index)
    return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥࡸࡵ࡯࠼ࠣࡿࢂ࠭௾").format(str(e)))
    raise e
def bstack1lllll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l11l1l11_opy_
  try:
    bstack1l11l11111_opy_(command, item_index)
    return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡥࡳࡹࠦࡲࡶࡰࠣ࠶࠳࠷࠳࠻ࠢࡾࢁࠬ௿").format(str(e)))
    try:
      return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
    except Exception as e2:
      logger.error(bstack1l111l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠ࠳࠰࠴࠷ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫఀ").format(str(e2)))
      raise e
def bstack11l111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l11l1l11_opy_
  try:
    bstack1l11l11111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡴࡸࡲࠥ࠸࠮࠲࠷࠽ࠤࢀࢃࠧఁ").format(str(e)))
    try:
      return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
    except Exception as e2:
      logger.error(bstack1l111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡨ࡯ࡵࠢ࠵࠲࠶࠻ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂ࠭ం").format(str(e2)))
      raise e
def _11llll1ll1_opy_(bstack111lll1ll_opy_, item_index, process_timeout, sleep_before_start, bstack11l1l1111l_opy_):
  bstack1l11l11111_opy_(bstack111lll1ll_opy_, item_index)
  if process_timeout is None:
    process_timeout = 3600
  if sleep_before_start and sleep_before_start > 0:
    time.sleep(min(sleep_before_start, 5))
  return process_timeout
def bstack1ll1l11l1l_opy_(command, bstack1ll1ll1l1l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11l1l11_opy_
  global bstack1l1111l1ll_opy_
  global bstack11111l1l_opy_
  try:
    for env_name, bstack11llll11l1_opy_ in bstack1l1111l1ll_opy_.items():
      os.environ[env_name] = bstack11llll11l1_opy_
    bstack11111l1l_opy_ = bstack1l111l1_opy_ (u"ࠤࠥః")
    bstack1l11l11111_opy_(command, item_index)
    if process_timeout is None:
      process_timeout = 3600
    if sleep_before_start and sleep_before_start > 0:
      time.sleep(min(sleep_before_start, 5))
    return bstack1l11l1l11_opy_(command, bstack1ll1ll1l1l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡣࡱࡷࠤࡷࡻ࡮ࠡ࠷࠱࠴࠿ࠦࡻࡾࠩఄ").format(str(e)))
    try:
      return bstack1l11l1l11_opy_(command, bstack1ll1ll1l1l_opy_, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l111l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡤࡲࡸࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠫఅ").format(str(e2)))
      raise e
def bstack1l11111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1l11l1l11_opy_
  try:
    process_timeout = _11llll1ll1_opy_(command, item_index, process_timeout, sleep_before_start, bstack1l111l1_opy_ (u"ࠬ࠺࠮࠳ࠩఆ"))
    return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡦࡴࡺࠠࡳࡷࡱࠤ࠹࠴࠲࠻ࠢࡾࢁࠬఇ").format(str(e)))
    try:
      return bstack1l11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
    except Exception as e2:
      logger.error(bstack1l111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡧࡵࡴࠡࡨࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠧఈ").format(str(e2)))
      raise e
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l11l111l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111111ll_opy_
  bstack1l1ll1l11_opy_ = bstack1l111111ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l111l1_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨఉ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l111l1_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭ఊ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1ll1l11_opy_
def bstack11l1l111l1_opy_(runner, hook_name, context, element, bstack1lll1ll1ll_opy_, *args):
  global bstack1ll1111l_opy_
  try:
    if runner.hooks.get(hook_name):
      bstack11l1l11ll_opy_.bstack111lllll11_opy_(hook_name, element)
    if bstack1ll1111l_opy_ is None or bstack1ll1111l_opy_:
      bstack1lll1ll1ll_opy_(runner, hook_name, context, *args)
    else:
      bstack1l1lllll1_opy_ = (context,) + args
      bstack1lll1ll1ll_opy_(runner, hook_name, *bstack1l1lllll1_opy_)
    if runner.hooks.get(hook_name):
      bstack11l1l11ll_opy_.bstack1llll1lll_opy_(element)
      if hook_name not in [bstack1l111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧఋ"), bstack1l111l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧఌ")] and args and hasattr(args[0], bstack1l111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬ఍")):
        args[0].error_message = bstack1l111l1_opy_ (u"࠭ࠧఎ")
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩఏ").format(str(e)))
@measure(event_name=EVENTS.bstack11l11ll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_, hook_type=bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡂ࡮࡯ࠦఐ"), bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack11l11lll1_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    if runner.hooks.get(bstack1l111l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ఑")).__name__ != bstack1l111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨఒ"):
      bstack11l1l111l1_opy_(runner, name, context, runner, bstack1lll1ll1ll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l1l1l11ll_opy_(bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪఓ")) else context.browser
      runner.driver_initialised = bstack1l111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤఔ")
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪక").format(str(e)))
def bstack111111ll_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    bstack11l1l111l1_opy_(runner, name, context, context.feature, bstack1lll1ll1ll_opy_, *args)
    try:
      if not bstack1ll1l1ll1_opy_:
        bstack1l1l11lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l11ll_opy_(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ఖ")) else context.browser
        if is_driver_active(bstack1l1l11lll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤగ")
          bstack1lllllll1l_opy_ = str(runner.feature.name)
          bstack1lll1l111_opy_(context, bstack1lllllll1l_opy_)
          bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧఘ") + json.dumps(bstack1lllllll1l_opy_) + bstack1l111l1_opy_ (u"ࠪࢁࢂ࠭ఙ"))
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫచ").format(str(e)))
def bstack1l111l11_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l111l1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧఛ")) else context.feature
    bstack11l1l111l1_opy_(runner, name, context, target, bstack1lll1ll1ll_opy_, *args)
@measure(event_name=EVENTS.bstack11llll1l_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack111l1lll_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    bstack11l1l11ll_opy_.start_test(context)
    bstack11l1l111l1_opy_(runner, name, context, context.scenario, bstack1lll1ll1ll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1lllll1l_opy_.bstack1lllll1l11_opy_(context, *args)
    try:
      bstack1l1l11lll1_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬజ"), context.browser)
      if is_driver_active(bstack1l1l11lll1_opy_):
        bstack1llll1lll1_opy_.bstack111ll1lll1_opy_(bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ఝ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥఞ")
        if (not bstack1ll1l1ll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1lllllll1l_opy_ = str(runner.feature.name)
          bstack1lllllll1l_opy_ = feature_name + bstack1l111l1_opy_ (u"ࠩࠣ࠱ࠥ࠭ట") + scenario_name
          if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఠ"):
            bstack1lll1l111_opy_(context, bstack1lllllll1l_opy_)
            bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩడ") + json.dumps(bstack1lllllll1l_opy_) + bstack1l111l1_opy_ (u"ࠬࢃࡽࠨఢ"))
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧణ").format(str(e)))
@measure(event_name=EVENTS.bstack11l11ll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_, hook_type=bstack1l111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࡓࡵࡧࡳࠦత"), bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll111111_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    bstack11l1l111l1_opy_(runner, name, context, args[0], bstack1lll1ll1ll_opy_, *args)
    try:
      bstack1l1l11lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l11ll_opy_(bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧథ")) else context.browser
      if is_driver_active(bstack1l1l11lll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l111l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢద")
        bstack11l1l11ll_opy_.bstack1l1ll1l1l_opy_(args[0])
        if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣధ"):
          feature_name = bstack1lllllll1l_opy_ = str(runner.feature.name)
          bstack1lllllll1l_opy_ = feature_name + bstack1l111l1_opy_ (u"ࠫࠥ࠳ࠠࠨన") + context.scenario.name
          bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ఩") + json.dumps(bstack1lllllll1l_opy_) + bstack1l111l1_opy_ (u"࠭ࡽࡾࠩప"))
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫఫ").format(str(e)))
@measure(event_name=EVENTS.bstack11l11ll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_, hook_type=bstack1l111l1_opy_ (u"ࠣࡣࡩࡸࡪࡸࡓࡵࡧࡳࠦబ"), bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack11ll1lll_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
  bstack11l1l11ll_opy_.bstack1ll1llll11_opy_(args[0])
  try:
    step_status = args[0].status.name
    bstack1l1l11lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨభ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1l11lll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l111l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪమ")
        feature_name = bstack1lllllll1l_opy_ = str(runner.feature.name)
        bstack1lllllll1l_opy_ = feature_name + bstack1l111l1_opy_ (u"ࠫࠥ࠳ࠠࠨయ") + context.scenario.name
        bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪర") + json.dumps(bstack1lllllll1l_opy_) + bstack1l111l1_opy_ (u"࠭ࡽࡾࠩఱ"))
    if str(step_status).lower() in [bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧల"), bstack1l111l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧళ")]:
      bstack11l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠩࠪఴ")
      bstack1ll1l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠪࠫవ")
      bstack1ll111ll1l_opy_ = bstack1l111l1_opy_ (u"ࠫࠬశ")
      try:
        import traceback
        bstack11l1llll11_opy_ = runner.exception.__class__.__name__
        bstack11l1ll111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠬࠦࠧష").join(bstack11l1ll111l_opy_)
        bstack1ll111ll1l_opy_ = bstack11l1ll111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11l11l11_opy_.format(str(e)))
      bstack11l1llll11_opy_ += bstack1ll111ll1l_opy_
      bstack1l1l1l1l11_opy_(context, json.dumps(str(args[0].name) + bstack1l111l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧస") + str(bstack1ll1l1l1l_opy_)),
                          bstack1l111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨహ"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ఺"):
        bstack11ll1lll11_opy_(getattr(context, bstack1l111l1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ఻"), None), bstack1l111l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦ఼ࠥ"), bstack11l1llll11_opy_)
        bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩఽ") + json.dumps(str(args[0].name) + bstack1l111l1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦా") + str(bstack1ll1l1l1l_opy_)) + bstack1l111l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ి"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧీ"):
        bstack11llll1ll_opy_(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨు"), bstack1l111l1_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨూ") + str(bstack11l1llll11_opy_))
    else:
      bstack1l1l1l1l11_opy_(context, bstack1l111l1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦృ"), bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤౄ"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ౅"):
        bstack11ll1lll11_opy_(getattr(context, bstack1l111l1_opy_ (u"࠭ࡰࡢࡩࡨࠫె"), None), bstack1l111l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢే"))
      bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ై") + json.dumps(str(args[0].name) + bstack1l111l1_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ౉")) + bstack1l111l1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩొ"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤో"):
        bstack11llll1ll_opy_(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧౌ"))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁ్ࠬ").format(str(e)))
  bstack11l1l111l1_opy_(runner, name, context, args[0], bstack1lll1ll1ll_opy_, *args)
@measure(event_name=EVENTS.bstack1l11ll111_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll1111ll_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
  bstack11l1l11ll_opy_.end_test(args[0])
  try:
    bstack1l1111lll_opy_ = args[0].status.name
    bstack1l1l11lll1_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭౎"), context.browser)
    bstack1l1lllll1l_opy_.bstack111ll111_opy_(bstack1l1l11lll1_opy_)
    if str(bstack1l1111lll_opy_).lower() in [bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ౏"), bstack1l111l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౐")]:
      bstack11l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠪࠫ౑")
      bstack1ll1l1l1l_opy_ = bstack1l111l1_opy_ (u"ࠫࠬ౒")
      bstack1ll111ll1l_opy_ = bstack1l111l1_opy_ (u"ࠬ࠭౓")
      try:
        import traceback
        bstack11l1llll11_opy_ = runner.exception.__class__.__name__
        bstack11l1ll111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1ll1l1l1l_opy_ = bstack1l111l1_opy_ (u"࠭ࠠࠨ౔").join(bstack11l1ll111l_opy_)
        bstack1ll111ll1l_opy_ = bstack11l1ll111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11l11l11_opy_.format(str(e)))
      bstack11l1llll11_opy_ += bstack1ll111ll1l_opy_
      bstack1l1l1l1l11_opy_(context, json.dumps(str(args[0].name) + bstack1l111l1_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨౕ") + str(bstack1ll1l1l1l_opy_)),
                          bstack1l111l1_opy_ (u"ࠣࡧࡵࡶࡴࡸౖࠢ"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౗") or runner.driver_initialised == bstack1l111l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪౘ"):
        bstack11ll1lll11_opy_(getattr(context, bstack1l111l1_opy_ (u"ࠫࡵࡧࡧࡦࠩౙ"), None), bstack1l111l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧౚ"), bstack11l1llll11_opy_)
        bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ౛") + json.dumps(str(args[0].name) + bstack1l111l1_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ౜") + str(bstack1ll1l1l1l_opy_)) + bstack1l111l1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨౝ"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ౞") or runner.driver_initialised == bstack1l111l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ౟"):
        bstack11llll1ll_opy_(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫౠ"), bstack1l111l1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤౡ") + str(bstack11l1llll11_opy_))
    else:
      bstack1l1l1l1l11_opy_(context, bstack1l111l1_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢౢ"), bstack1l111l1_opy_ (u"ࠢࡪࡰࡩࡳࠧౣ"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ౤") or runner.driver_initialised == bstack1l111l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ౥"):
        bstack11ll1lll11_opy_(getattr(context, bstack1l111l1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨ౦"), None), bstack1l111l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ౧"))
      bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ౨") + json.dumps(str(args[0].name) + bstack1l111l1_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥ౩")) + bstack1l111l1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭౪"))
      if runner.driver_initialised == bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ౫") or runner.driver_initialised == bstack1l111l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ౬"):
        bstack11llll1ll_opy_(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౭"))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭౮").format(str(e)))
  bstack11l1l111l1_opy_(runner, name, context, context.scenario, bstack1lll1ll1ll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11l1lllll1_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l111l1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ౯")) else context.feature
    bstack11l1l111l1_opy_(runner, name, context, target, bstack1lll1ll1ll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11lll1l1l1_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    try:
      bstack1l1l11lll1_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ౰"), context.browser)
      bstack111ll1l1ll_opy_ = bstack1l111l1_opy_ (u"ࠧࠨ౱")
      if context.failed is True:
        bstack1l1llll1_opy_ = []
        bstack1l1111l111_opy_ = []
        bstack1111lll1_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1llll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11l1ll111l_opy_ = traceback.format_tb(exc_tb)
            bstack11lll1ll_opy_ = bstack1l111l1_opy_ (u"ࠨࠢࠪ౲").join(bstack11l1ll111l_opy_)
            bstack1l1111l111_opy_.append(bstack11lll1ll_opy_)
            bstack1111lll1_opy_.append(bstack11l1ll111l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11l11l11_opy_.format(str(e)))
        bstack11l1llll11_opy_ = bstack1l111l1_opy_ (u"ࠩࠪ౳")
        for i in range(len(bstack1l1llll1_opy_)):
          bstack11l1llll11_opy_ += bstack1l1llll1_opy_[i] + bstack1111lll1_opy_[i] + bstack1l111l1_opy_ (u"ࠪࡠࡳ࠭౴")
        bstack111ll1l1ll_opy_ = bstack1l111l1_opy_ (u"ࠫࠥ࠭౵").join(bstack1l1111l111_opy_)
        if runner.driver_initialised in [bstack1l111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ౶"), bstack1l111l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ౷")]:
          bstack1l1l1l1l11_opy_(context, bstack111ll1l1ll_opy_, bstack1l111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ౸"))
          bstack11ll1lll11_opy_(getattr(context, bstack1l111l1_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭౹"), None), bstack1l111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౺"), bstack11l1llll11_opy_)
          bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ౻") + json.dumps(bstack111ll1l1ll_opy_) + bstack1l111l1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫ౼"))
          bstack11llll1ll_opy_(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ౽"), bstack1l111l1_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦ౾") + str(bstack11l1llll11_opy_))
          bstack11ll1ll1_opy_ = bstack1l1111ll1l_opy_(bstack111ll1l1ll_opy_, runner.feature.name, logger)
          if (bstack11ll1ll1_opy_ != None):
            bstack1l1ll11l1_opy_.append(bstack11ll1ll1_opy_)
      else:
        if runner.driver_initialised in [bstack1l111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ౿"), bstack1l111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧಀ")]:
          bstack1l1l1l1l11_opy_(context, bstack1l111l1_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧಁ") + str(runner.feature.name) + bstack1l111l1_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧಂ"), bstack1l111l1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤಃ"))
          bstack11ll1lll11_opy_(getattr(context, bstack1l111l1_opy_ (u"ࠬࡶࡡࡨࡧࠪ಄"), None), bstack1l111l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨಅ"))
          bstack1l1l11lll1_opy_.execute_script(bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬಆ") + json.dumps(bstack1l111l1_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦಇ") + str(runner.feature.name) + bstack1l111l1_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦಈ")) + bstack1l111l1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩಉ"))
          bstack11llll1ll_opy_(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಊ"))
          bstack11ll1ll1_opy_ = bstack1l1111ll1l_opy_(bstack111ll1l1ll_opy_, runner.feature.name, logger)
          if (bstack11ll1ll1_opy_ != None):
            bstack1l1ll11l1_opy_.append(bstack11ll1ll1_opy_)
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧಋ").format(str(e)))
    bstack11l1l111l1_opy_(runner, name, context, context.feature, bstack1lll1ll1ll_opy_, *args)
@measure(event_name=EVENTS.bstack11l11ll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_, hook_type=bstack1l111l1_opy_ (u"ࠨࡡࡧࡶࡨࡶࡆࡲ࡬ࠣಌ"), bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1lll1111ll_opy_(runner, name, context, bstack1lll1ll1ll_opy_, *args):
    bstack11l1l111l1_opy_(runner, name, context, runner, bstack1lll1ll1ll_opy_, *args)
def bstack1l1l1ll1ll_opy_(self, filename=None):
  bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࡒ࡯ࡢࡦࠣ࡬ࡴࡵ࡫ࡴࠢࡤࡲࡩࠦࡥ࡯ࡵࡸࡶࡪࠦࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠰ࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠢࡤࡶࡪࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡦࡦ࠱ࠎࠥࠦࡂࡦࡪࡤࡺࡪࠦࡶ࠲࠰࠶࠯ࠥࡪ࡯ࡦࡵࡱࠫࡹࠦࡣࡢ࡮࡯ࠤࡷࡻ࡮ࠡࡪࡲࡳࡰࡹࠠࡵࡪࡤࡸࠥࡧࡲࡦࡰࠪࡸࠥࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡴࡱࠣࡻࡪࠦ࡭ࡶࡵࡷࠎࠥࠦࡤࡰࠢࡷ࡬࡮ࡹࠠࡦࡺࡳࡰ࡮ࡩࡩࡵ࡮ࡼࠤࡹࡵࠠ࡮ࡣ࡮ࡩࠥࡹࡵࡳࡧࠣࡻࡪ࠭ࡲࡦࠢࡦࡥࡱࡲࡥࡥࠢ࡬ࡲࠥࡧ࡮ࡺࠢࡦࡥࡸ࡫࠮ࠋࠢࠣࠦࠧࠨ಍")
  global bstack1ll111l1l_opy_
  bstack1ll111l1l_opy_(self, filename)
  bstack1111ll1ll_opy_ = []
  bstack11ll1l11l1_opy_ = [bstack1l111l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩಎ"), bstack1l111l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭ಏ"), bstack1l111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಐ"), bstack1l111l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ಑"), bstack1l111l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨಒ"), bstack1l111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ಓ")]
  bstack11lllll1l_opy_ = lambda *_: None
  for hook_name in bstack11ll1l11l1_opy_:
    if hook_name not in self.hooks:
      self.hooks[hook_name] = bstack11lllll1l_opy_
      bstack1111ll1ll_opy_.append(hook_name)
  if bstack1111ll1ll_opy_:
    os.environ[bstack1l111l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡎࡏࡐࡍࡖࠫಔ")] = bstack1l111l1_opy_ (u"ࠨ࠮ࠪಕ").join(bstack1111ll1ll_opy_)
def bstack11111llll_opy_(self, name, *args):
  global bstack1lll1ll1ll_opy_
  global bstack1ll1111l_opy_
  try:
    if bstack11l1ll1l1_opy_:
      platform_index = int(threading.current_thread()._name) % bstack1lll11l1_opy_
      bstack1l111l1l1l_opy_ = CONFIG[bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಖ")][platform_index]
      os.environ[bstack1l111l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫಗ")] = json.dumps(bstack1l111l1l1l_opy_)
    if not hasattr(self, bstack1l111l1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩಘ")):
      self.driver_initialised = None
    bstack11lll1111l_opy_ = {
        bstack1l111l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩಙ"): bstack11l11lll1_opy_,
        bstack1l111l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧಚ"): bstack111111ll_opy_,
        bstack1l111l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫಛ"): bstack1l111l11_opy_,
        bstack1l111l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪಜ"): bstack111l1lll_opy_,
        bstack1l111l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧಝ"): bstack1ll111111_opy_,
        bstack1l111l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧಞ"): bstack11ll1lll_opy_,
        bstack1l111l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬಟ"): bstack1ll1111ll_opy_,
        bstack1l111l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨಠ"): bstack11l1lllll1_opy_,
        bstack1l111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ಡ"): bstack11lll1l1l1_opy_,
        bstack1l111l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪಢ"): bstack1lll1111ll_opy_
    }
    handler = bstack11lll1111l_opy_.get(name, bstack1lll1ll1ll_opy_)
    try:
      if args:
        context = args[0]
        remaining_args = args[1:]
        if bstack1ll1111l_opy_ is None or not bstack1ll1111l_opy_:
          context = self.context
          remaining_args = args
      else:
        context = self.context
        remaining_args = ()
      handler(self, name, context, bstack1lll1ll1ll_opy_, *remaining_args)
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧࠣ࡬ࡴࡵ࡫ࠡࡪࡤࡲࡩࡲࡥࡳࠢࡾࢁ࠿ࠦࡻࡾࠩಣ").format(name, str(e)))
    if name in [bstack1l111l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩತ"), bstack1l111l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಥ"), bstack1l111l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧದ")]:
      try:
        bstack1l1l11lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l11ll_opy_(bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫಧ")) else context.browser
        bstack1l111lll1l_opy_ = (
          (name == bstack1l111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩನ") and self.driver_initialised == bstack1l111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ಩")) or
          (name == bstack1l111l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಪ") and self.driver_initialised == bstack1l111l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥಫ")) or
          (name == bstack1l111l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಬ") and self.driver_initialised in [bstack1l111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨಭ"), bstack1l111l1_opy_ (u"ࠧ࡯࡮ࡴࡶࡨࡴࠧಮ")]) or
          (name == bstack1l111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪಯ") and self.driver_initialised == bstack1l111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧರ"))
        )
        if bstack1l111lll1l_opy_:
          self.driver_initialised = None
          if bstack1l1l11lll1_opy_ and hasattr(bstack1l1l11lll1_opy_, bstack1l111l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬಱ")):
            try:
              bstack1l1l11lll1_opy_.quit()
            except Exception as e:
              logger.debug(bstack1l111l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡳࡸ࡭ࡹࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࠦࡨࡰࡱ࡮࠾ࠥࢁࡽࠨಲ").format(str(e)))
      except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡭ࡵ࡯࡬ࠢࡦࡰࡪࡧ࡮ࡶࡲࠣࡪࡴࡸࠠࡼࡿ࠽ࠤࢀࢃࠧಳ").format(name, str(e)))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠫࡈࡸࡩࡵ࡫ࡦࡥࡱࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥࠡࡴࡸࡲࠥ࡮࡯ࡰ࡭ࠣࡿࢂࡀࠠࡼࡿࠪ಴").format(name, str(e)))
    try:
      if bstack1ll1111l_opy_ is None or bstack1ll1111l_opy_:
        try:
          bstack1lll1ll1ll_opy_(self, name, self.context, *args)
        except TypeError:
          bstack1lll1ll1ll_opy_(self, name, *args)
      else:
        bstack1lll1ll1ll_opy_(self, name, *args)
    except Exception as e2:
      logger.debug(bstack1l111l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤ࡭ࡵ࡯࡬ࠢࡾࢁ࠿ࠦࡻࡾࠩವ").format(name, str(e2)))
def bstack11l1l1l1ll_opy_(config, startdir):
  return bstack1l111l1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦಶ").format(bstack1l111l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨಷ"))
notset = Notset()
def bstack1l11ll111l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1ll1lll1_opy_
  if str(name).lower() == bstack1l111l1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨಸ"):
    return bstack1l111l1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣಹ")
  else:
    return bstack1l1ll1lll1_opy_(self, name, default, skip)
def bstack11llll1l1l_opy_(item, when):
  global bstack1l1l11l111_opy_
  try:
    bstack1l1l11l111_opy_(item, when)
  except Exception as e:
    pass
def bstack111ll11l11_opy_():
  return
def bstack11l111llll_opy_(type, name, status, reason, bstack1lll11l111_opy_, bstack1l11ll1l1l_opy_):
  bstack11l1ll1ll_opy_ = {
    bstack1l111l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ಺"): type,
    bstack1l111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ಻"): {}
  }
  if type == bstack1l111l1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫಼ࠧ"):
    bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಽ")][bstack1l111l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ಾ")] = bstack1lll11l111_opy_
    bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಿ")][bstack1l111l1_opy_ (u"ࠩࡧࡥࡹࡧࠧೀ")] = json.dumps(str(bstack1l11ll1l1l_opy_))
  if type == bstack1l111l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫು"):
    bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧೂ")][bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪೃ")] = name
  if type == bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩೄ"):
    bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ೅")][bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨೆ")] = status
    if status == bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩೇ"):
      bstack11l1ll1ll_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ೈ")][bstack1l111l1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ೉")] = json.dumps(str(reason))
  bstack1l1lllllll_opy_ = bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪೊ").format(json.dumps(bstack11l1ll1ll_opy_))
  return bstack1l1lllllll_opy_
def bstack11llll111_opy_(driver_command, response):
    if driver_command == bstack1l111l1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪೋ"):
        bstack1llll1lll1_opy_.bstack1l111111l1_opy_({
            bstack1l111l1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ೌ"): response[bstack1l111l1_opy_ (u"ࠨࡸࡤࡰࡺ࡫್ࠧ")],
            bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ೎"): bstack1llll1lll1_opy_.current_test_uuid()
        })
def bstack1llll111ll_opy_(item, call, rep):
  global bstack111ll11ll_opy_
  global bstack1l11ll11_opy_
  global bstack1ll1l1ll1_opy_
  name = bstack1l111l1_opy_ (u"ࠪࠫ೏")
  try:
    if rep.when == bstack1l111l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ೐"):
      bstack1llll1ll1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1l1ll1_opy_:
          name = str(rep.nodeid)
          bstack111ll1l11_opy_ = bstack11l111llll_opy_(bstack1l111l1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭೑"), name, bstack1l111l1_opy_ (u"࠭ࠧ೒"), bstack1l111l1_opy_ (u"ࠧࠨ೓"), bstack1l111l1_opy_ (u"ࠨࠩ೔"), bstack1l111l1_opy_ (u"ࠩࠪೕ"))
          threading.current_thread().bstack1ll111l11l_opy_ = name
          for driver in bstack1l11ll11_opy_:
            if bstack1llll1ll1l_opy_ == driver.session_id:
              driver.execute_script(bstack111ll1l11_opy_)
      except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪೖ").format(str(e)))
      try:
        bstack1lll1llll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l111l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ೗"):
          status = bstack1l111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ೘") if rep.outcome.lower() == bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭೙") else bstack1l111l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ೚")
          reason = bstack1l111l1_opy_ (u"ࠨࠩ೛")
          if status == bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ೜"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l111l1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨೝ") if status == bstack1l111l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫೞ") else bstack1l111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ೟")
          data = name + bstack1l111l1_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨೠ") if status == bstack1l111l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧೡ") else name + bstack1l111l1_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫೢ") + reason
          bstack1lllll111l_opy_ = bstack11l111llll_opy_(bstack1l111l1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫೣ"), bstack1l111l1_opy_ (u"ࠪࠫ೤"), bstack1l111l1_opy_ (u"ࠫࠬ೥"), bstack1l111l1_opy_ (u"ࠬ࠭೦"), level, data)
          for driver in bstack1l11ll11_opy_:
            if bstack1llll1ll1l_opy_ == driver.session_id:
              driver.execute_script(bstack1lllll111l_opy_)
      except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ೧").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ೨").format(str(e)))
  bstack111ll11ll_opy_(item, call, rep)
def bstack11l1111lll_opy_(driver, bstack111ll1ll1_opy_, test=None):
  global bstack111llll11_opy_
  if test != None:
    bstack1111l11ll_opy_ = getattr(test, bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭೩"), None)
    bstack1lll1lll1l_opy_ = getattr(test, bstack1l111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ೪"), None)
    PercySDK.screenshot(driver, bstack111ll1ll1_opy_, bstack1111l11ll_opy_=bstack1111l11ll_opy_, bstack1lll1lll1l_opy_=bstack1lll1lll1l_opy_, bstack11lllllll_opy_=bstack111llll11_opy_)
  else:
    PercySDK.screenshot(driver, bstack111ll1ll1_opy_)
@measure(event_name=EVENTS.bstack1ll1lll1l_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1lllll1l1_opy_(driver):
  if bstack1l111lll1_opy_.bstack1ll1111l1l_opy_() is True or bstack1l111lll1_opy_.capturing() is True:
    return
  bstack1l111lll1_opy_.bstack11l1l1l11_opy_()
  while not bstack1l111lll1_opy_.bstack1ll1111l1l_opy_():
    bstack1l1ll1ll1_opy_ = bstack1l111lll1_opy_.bstack1ll1111l11_opy_()
    bstack11l1111lll_opy_(driver, bstack1l1ll1ll1_opy_)
  bstack1l111lll1_opy_.bstack1ll1111l1_opy_()
def bstack111llll111_opy_(sequence, driver_command, response = None, bstack11ll1111l1_opy_ = None, args = None):
    try:
      if sequence != bstack1l111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ೫"):
        return
      if percy.bstack1111111l1_opy_() == bstack1l111l1_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ೬"):
        return
      bstack1l1ll1ll1_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ೭"), None)
      for command in bstack11ll11ll1l_opy_:
        if command == driver_command:
          with bstack1ll11l11_opy_:
            bstack11ll11l1ll_opy_ = bstack1l11ll11_opy_.copy()
          for driver in bstack11ll11l1ll_opy_:
            bstack1lllll1l1_opy_(driver)
      bstack1ll1111111_opy_ = percy.bstack1l1ll1ll1l_opy_()
      if driver_command in bstack11lll111l1_opy_[bstack1ll1111111_opy_]:
        bstack1l111lll1_opy_.bstack11lll1ll11_opy_(bstack1l1ll1ll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1111l1111_opy_(framework_name):
  if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ೮")):
      return
  bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ೯"), True)
  global bstack1lll11ll1l_opy_
  global bstack11l1111111_opy_
  global bstack1l11l1l1l1_opy_
  bstack1lll11ll1l_opy_ = framework_name
  logger.info(bstack11l1111l_opy_.format(bstack1lll11ll1l_opy_.split(bstack1l111l1_opy_ (u"ࠨ࠯ࠪ೰"))[0]))
  bstack111l1l1ll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11l1ll1l1_opy_:
      Service.start = bstack111ll1llll_opy_
      Service.stop = bstack11lll11lll_opy_
      webdriver.Remote.get = bstack1l11ll1ll_opy_
      WebDriver.quit = bstack1ll11lll_opy_
      webdriver.Remote.__init__ = bstack1ll11lll1_opy_
    if not bstack11l1ll1l1_opy_:
        webdriver.Remote.__init__ = bstack11l11lll_opy_
    WebDriver.getAccessibilityResults = getAccessibilityResults
    WebDriver.get_accessibility_results = getAccessibilityResults
    WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
    WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
    WebDriver.performScan = perform_scan
    WebDriver.perform_scan = perform_scan
    WebDriver.execute = bstack1ll11l11ll_opy_
    bstack11l1111111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11l1ll1l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1111l11_opy_
  except Exception as e:
    pass
  bstack1l1ll1lll_opy_()
  if not bstack11l1111111_opy_:
    bstack11l1l1ll1l_opy_(bstack1l111l1_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦೱ"), bstack111ll11lll_opy_)
  if bstack111llllll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      if hasattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫೲ")) and callable(getattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬೳ"))):
        RemoteConnection._get_proxy_url = bstack1l1ll1llll_opy_
      else:
        from selenium.webdriver.remote.client_config import ClientConfig
        ClientConfig.get_proxy_url = bstack1l1ll1llll_opy_
    except Exception as e:
      logger.error(bstack11l1lll111_opy_.format(str(e)))
  if bstack11l1ll111_opy_():
    bstack111llll1_opy_(CONFIG, logger)
  if (bstack1l111l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೴") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1111111l1_opy_() == bstack1l111l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ೵"):
          bstack1l1l1l1l1l_opy_(bstack111llll111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll111l111_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l11lllll_opy_
      except Exception as e:
        logger.warning(bstack1lllll1111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1ll11ll_opy_
      except Exception as e:
        logger.debug(bstack11ll1ll11l_opy_ + str(e))
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1lllll1111_opy_)
    Output.start_test = bstack1l1ll1l1ll_opy_
    Output.end_test = bstack11ll1ll111_opy_
    TestStatus.__init__ = bstack1ll1lll1ll_opy_
    QueueItem.__init__ = bstack1ll1l1lll1_opy_
    pabot._create_items = bstack11l11l1111_opy_
    try:
      from pabot import __version__ as bstack1111ll111_opy_
      if version.parse(bstack1111ll111_opy_) >= version.parse(bstack1l111l1_opy_ (u"ࠧ࠶࠰࠳࠲࠵࠭೶")):
        pabot._run = bstack1ll1l11l1l_opy_
      elif version.parse(bstack1111ll111_opy_) >= version.parse(bstack1l111l1_opy_ (u"ࠨ࠶࠱࠶࠳࠶ࠧ೷")):
        pabot._run = bstack1l11111ll_opy_
      elif version.parse(bstack1111ll111_opy_) >= version.parse(bstack1l111l1_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ೸")):
        pabot._run = bstack11l111l1_opy_
      elif version.parse(bstack1111ll111_opy_) >= version.parse(bstack1l111l1_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪ೹")):
        pabot._run = bstack1lllll111_opy_
      else:
        pabot._run = bstack11l1ll1111_opy_
    except Exception as e:
      pabot._run = bstack11l1ll1111_opy_
    pabot._create_command_for_execution = bstack1lll1l11l_opy_
    pabot._report_results = bstack1l1lll11l1_opy_
  if bstack1l111l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ೺") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1l1ll1l11l_opy_)
    Runner.run_hook = bstack11111llll_opy_
    try:
      from behave import __version__ as bstack111lll11l1_opy_
      if version.parse(bstack111lll11l1_opy_) >= version.parse(bstack1l111l1_opy_ (u"ࠬ࠷࠮࠴࠰࠳ࠫ೻")):
        Runner.load_hooks = bstack1l1l1ll1ll_opy_
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡨࡥࡩࡣࡹࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ೼").format(str(e)))
    Step.run = bstack1l11l111l_opy_
  if bstack1l111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ೽") in str(framework_name).lower():
    if not bstack11l1ll1l1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1l1l1ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111ll11l11_opy_
      Config.getoption = bstack1l11ll111l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llll111ll_opy_
    except Exception as e:
      pass
def bstack1ll1l11ll_opy_():
  global CONFIG
  if bstack1l111l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ೾") in CONFIG and int(CONFIG[bstack1l111l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ೿")]) > 1:
    logger.warning(bstack1l1111111l_opy_)
def bstack111llll1l1_opy_(arg, bstack11lllll1l1_opy_, bstack1lll111111_opy_=None):
  global CONFIG
  global bstack1l1l1l11l1_opy_
  global bstack11ll11l1_opy_
  global bstack11l1ll1l1_opy_
  global bstack1l1l1111_opy_
  bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪഀ")
  if bstack11lllll1l1_opy_ and isinstance(bstack11lllll1l1_opy_, str):
    bstack11lllll1l1_opy_ = eval(bstack11lllll1l1_opy_)
  CONFIG = bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫഁ")]
  bstack1l1l1l11l1_opy_ = bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ം")]
  bstack11ll11l1_opy_ = bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨഃ")]
  bstack11l1ll1l1_opy_ = bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪഄ")]
  bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩഅ"), bstack11l1ll1l1_opy_)
  os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫആ")] = bstack11l111111l_opy_
  os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩഇ")] = json.dumps(CONFIG)
  os.environ[bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫഈ")] = bstack1l1l1l11l1_opy_
  os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഉ")] = str(bstack11ll11l1_opy_)
  os.environ[bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬഊ")] = str(True)
  if bstack1lll11l1l1_opy_(arg, [bstack1l111l1_opy_ (u"ࠧ࠮ࡰࠪഋ"), bstack1l111l1_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩഌ")]) != -1:
    os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ഍")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111l1ll1_opy_)
    return
  bstack11ll1111ll_opy_()
  global bstack1lll1ll1l1_opy_
  global bstack111llll11_opy_
  global bstack1lll111l1_opy_
  global bstack11111l1l_opy_
  global bstack1ll1111ll1_opy_
  global bstack1l11l1l1l1_opy_
  global bstack1l1111l1l_opy_
  arg.append(bstack1l111l1_opy_ (u"ࠥ࠱࡜ࠨഎ"))
  arg.append(bstack1l111l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢഏ"))
  arg.append(bstack1l111l1_opy_ (u"ࠧ࠳ࡗࠣഐ"))
  arg.append(bstack1l111l1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧ഑"))
  global bstack111lll1l1_opy_
  global bstack1l11111l1l_opy_
  global bstack1lll1l11_opy_
  global bstack1lll11ll11_opy_
  global bstack1lll11lll_opy_
  global bstack1l11lll1ll_opy_
  global bstack1111l11l1_opy_
  global bstack1l1l11l11_opy_
  global bstack1ll1l1lll_opy_
  global bstack1l1l111lll_opy_
  global bstack1l1ll1lll1_opy_
  global bstack1l1l11l111_opy_
  global bstack111ll11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111lll1l1_opy_ = webdriver.Remote.__init__
    bstack1l11111l1l_opy_ = WebDriver.quit
    bstack1l1l11l11_opy_ = WebDriver.close
    bstack1ll1l1lll_opy_ = WebDriver.get
    bstack1lll1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1l1ll1_opy_(CONFIG) and bstack11l111l11l_opy_():
    if bstack111l1111l_opy_() < version.parse(bstack1ll11111ll_opy_):
      logger.error(bstack11l1l11l1l_opy_.format(bstack111l1111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨഒ")) and callable(getattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩഓ"))):
          bstack1l1l111lll_opy_ = RemoteConnection._get_proxy_url
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          bstack1l1l111lll_opy_ = ClientConfig.get_proxy_url
      except Exception as e:
        logger.error(bstack11l1lll111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1ll1lll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l11l111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warning(bstack1l111l1_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤഔ"), bstack1ll1lll1_opy_, str(e))
  try:
    from pytest_bdd import reporting
    bstack111ll11ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l111l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫക"))
  bstack1lll111l1_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨഖ"), {}).get(bstack1l111l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧഗ"))
  bstack1l1111l1l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1llll11111_opy_():
      bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.CONNECT, bstack1ll1lll11l_opy_())
    platform_index = int(os.environ.get(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ഘ"), bstack1l111l1_opy_ (u"ࠧ࠱ࠩങ")))
  else:
    bstack1111l1111_opy_(bstack1ll111l1l1_opy_)
  os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩച")] = CONFIG[bstack1l111l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഛ")]
  os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ജ")] = CONFIG[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഝ")]
  os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨഞ")] = bstack11l1ll1l1_opy_.__str__()
  from _pytest.config import main as bstack11111l1l1_opy_
  bstack11111l111_opy_ = []
  try:
    exit_code = bstack11111l1l1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l1l1l11l_opy_()
    if bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪട") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l11l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11111l111_opy_.append(bstack11l1l11l11_opy_)
    try:
      bstack111l1ll11_opy_ = (bstack11111l111_opy_, int(exit_code))
      bstack1lll111111_opy_.append(bstack111l1ll11_opy_)
    except:
      bstack1lll111111_opy_.append((bstack11111l111_opy_, exit_code))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11111l111_opy_.append({bstack1l111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬഠ"): bstack1l111l1_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪഡ") + os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩഢ")), bstack1l111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩണ"): traceback.format_exc(), bstack1l111l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪത"): int(os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬഥ")))})
    bstack1lll111111_opy_.append((bstack11111l111_opy_, 1))
def mod_behave_main(args, retries):
  try:
    from behave.configuration import Configuration
    from behave.__main__ import run_behave
    from browserstack_sdk.bstack_behave_runner import BehaveRunner
    config = Configuration(args)
    config.update_userdata({bstack1l111l1_opy_ (u"ࠨࡲࡦࡶࡵ࡭ࡪࡹࠢദ"): str(retries)})
    return run_behave(config, runner_class=BehaveRunner)
  except Exception as e:
    bstack1ll1lll111_opy_ = e.__class__.__name__
    print(bstack1l111l1_opy_ (u"ࠢࠦࡵ࠽ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡧ࡫ࡨࡢࡸࡨࠤࡹ࡫ࡳࡵࠢࠨࡷࠧധ") % (bstack1ll1lll111_opy_, e))
    return 1
def bstack11ll1llll1_opy_(arg):
  global bstack1lll111ll_opy_
  bstack1111l1111_opy_(bstack11ll11l111_opy_)
  os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩന")] = str(bstack11ll11l1_opy_)
  retries = bstack1llll111l_opy_.bstack1lll1111_opy_(CONFIG)
  status_code = 0
  if bstack1llll111l_opy_.bstack1ll111l1ll_opy_(CONFIG):
    status_code = mod_behave_main(arg, retries)
  else:
    from behave.__main__ import main as bstack1ll1l1ll1l_opy_
    status_code = bstack1ll1l1ll1l_opy_(arg)
  if status_code != 0:
    bstack1lll111ll_opy_ = status_code
def bstack1ll111lll_opy_():
  logger.info(bstack1l1lll111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨഩ"), help=bstack1l111l1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫപ"))
  parser.add_argument(bstack1l111l1_opy_ (u"ࠫ࠲ࡻࠧഫ"), bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩബ"), help=bstack1l111l1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬഭ"))
  parser.add_argument(bstack1l111l1_opy_ (u"ࠧ࠮࡭ࠪമ"), bstack1l111l1_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧയ"), help=bstack1l111l1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪര"))
  parser.add_argument(bstack1l111l1_opy_ (u"ࠪ࠱࡫࠭റ"), bstack1l111l1_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩല"), help=bstack1l111l1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫള"))
  bstack1lll11l1ll_opy_ = parser.parse_args()
  try:
    bstack1l1l1ll11l_opy_ = bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪഴ")
    if bstack1lll11l1ll_opy_.framework and bstack1lll11l1ll_opy_.framework not in (bstack1l111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧവ"), bstack1l111l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩശ")):
      bstack1l1l1ll11l_opy_ = bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨഷ")
    bstack1l11l11ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1ll11l_opy_)
    bstack111lll1lll_opy_ = open(bstack1l11l11ll1_opy_, bstack1l111l1_opy_ (u"ࠪࡶࠬസ"))
    bstack11lll1l11l_opy_ = bstack111lll1lll_opy_.read()
    bstack111lll1lll_opy_.close()
    if bstack1lll11l1ll_opy_.username:
      bstack11lll1l11l_opy_ = bstack11lll1l11l_opy_.replace(bstack1l111l1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫഹ"), bstack1lll11l1ll_opy_.username)
    if bstack1lll11l1ll_opy_.key:
      bstack11lll1l11l_opy_ = bstack11lll1l11l_opy_.replace(bstack1l111l1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧഺ"), bstack1lll11l1ll_opy_.key)
    if bstack1lll11l1ll_opy_.framework:
      bstack11lll1l11l_opy_ = bstack11lll1l11l_opy_.replace(bstack1l111l1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ഻ࠧ"), bstack1lll11l1ll_opy_.framework)
    file_name = bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮഼ࠪ")
    file_path = os.path.abspath(file_name)
    bstack111111l1l_opy_ = open(file_path, bstack1l111l1_opy_ (u"ࠨࡹࠪഽ"))
    bstack111111l1l_opy_.write(bstack11lll1l11l_opy_)
    bstack111111l1l_opy_.close()
    logger.info(bstack11l1l1ll1_opy_)
    try:
      os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫാ")] = bstack1lll11l1ll_opy_.framework if bstack1lll11l1ll_opy_.framework != None else bstack1l111l1_opy_ (u"ࠥࠦി")
      config = yaml.safe_load(bstack11lll1l11l_opy_)
      config[bstack1l111l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫീ")] = bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫു")
      bstack1l1111llll_opy_(bstack1111llll_opy_, config)
    except Exception as e:
      logger.debug(bstack111l111ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11ll1ll1l1_opy_.format(str(e)))
def bstack1l1111llll_opy_(bstack1ll1l1ll11_opy_, config, bstack11ll111l_opy_={}):
  global bstack11l1ll1l1_opy_
  global bstack11ll1l111_opy_
  global bstack1l1l1111_opy_
  if not config:
    return
  bstack1llllll1ll_opy_ = bstack1ll11lllll_opy_ if not bstack11l1ll1l1_opy_ else (
    bstack1lll1ll1l_opy_ if bstack1l111l1_opy_ (u"࠭ࡡࡱࡲࠪൂ") in config else (
        bstack1l1ll1l1_opy_ if config.get(bstack1l111l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫൃ")) else bstack1lll1l1lll_opy_
    )
)
  bstack1l1l1ll1l_opy_ = False
  bstack11lll11l1l_opy_ = False
  if bstack11l1ll1l1_opy_ is True:
      if bstack1l111l1_opy_ (u"ࠨࡣࡳࡴࠬൄ") in config:
          bstack1l1l1ll1l_opy_ = True
      else:
          bstack11lll11l1l_opy_ = True
  bstack1lll1111l1_opy_ = bstack1l11111ll1_opy_.bstack1ll1ll111_opy_(config, bstack11ll1l111_opy_)
  bstack1lll1l1l11_opy_ = bstack11ll1l1ll1_opy_()
  data = {
    bstack1l111l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൅"): config[bstack1l111l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬെ")],
    bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧേ"): config[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨൈ")],
    bstack1l111l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ൉"): bstack1ll1l1ll11_opy_,
    bstack1l111l1_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫൊ"): os.environ.get(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪോ"), bstack11ll1l111_opy_),
    bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫൌ"): bstack1l1lll1111_opy_,
    bstack1l111l1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ്ࠬ"): bstack1lll1l1ll1_opy_(),
    bstack1l111l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൎ"): {
      bstack1l111l1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ൏"): str(config[bstack1l111l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭൐")]) if bstack1l111l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൑") in config else bstack1l111l1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ൒"),
      bstack1l111l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ൓"): sys.version,
      bstack1l111l1_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬൔ"): bstack1l1lll1l11_opy_(os.environ.get(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ൕ"), bstack11ll1l111_opy_)),
      bstack1l111l1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧൖ"): bstack1l111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ൗ"),
      bstack1l111l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ൘"): bstack1llllll1ll_opy_,
      bstack1l111l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭൙"): bstack1lll1111l1_opy_,
      bstack1l111l1_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨ൚"): os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ൛")],
      bstack1l111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ൜"): os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൝"), bstack11ll1l111_opy_),
      bstack1l111l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ൞"): bstack11l11l1ll_opy_(os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൟ"), bstack11ll1l111_opy_)),
      bstack1l111l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧൠ"): bstack1lll1l1l11_opy_.get(bstack1l111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧൡ")),
      bstack1l111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩൢ"): bstack1lll1l1l11_opy_.get(bstack1l111l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬൣ")),
      bstack1l111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ൤"): config[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ൥")] if config[bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ൦")] else bstack1l111l1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ൧"),
      bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൨"): str(config[bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ൩")]) if bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭൪") in config else bstack1l111l1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ൫"),
      bstack1l111l1_opy_ (u"࠭࡯ࡴࠩ൬"): sys.platform,
      bstack1l111l1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ൭"): socket.gethostname(),
      bstack1l111l1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ൮"): bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ൯"))
    }
  }
  if not bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ൰")) is None:
    data[bstack1l111l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ൱")][bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࡍࡦࡶࡤࡨࡦࡺࡡࠨ൲")] = {
      bstack1l111l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭൳"): bstack1l111l1_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ൴"),
      bstack1l111l1_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ൵"): bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ൶")),
      bstack1l111l1_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࡑࡹࡲࡨࡥࡳࠩ൷"): bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧ൸"))
    }
  if bstack1ll1l1ll11_opy_ == bstack11l1l1lll_opy_:
    data[bstack1l111l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ൹")][bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࠫൺ")] = bstack1l11lll11_opy_(config)
    data[bstack1l111l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪൻ")][bstack1l111l1_opy_ (u"ࠨ࡫ࡶࡔࡪࡸࡣࡺࡃࡸࡸࡴࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ർ")] = percy.bstack111lll1ll1_opy_
    data[bstack1l111l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬൽ")][bstack1l111l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡄࡸ࡭ࡱࡪࡉࡥࠩൾ")] = percy.percy_build_id
  if not bstack1llll111l_opy_.bstack1l11l11l1_opy_(CONFIG):
    data[bstack1l111l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧൿ")][bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ඀")] = bstack1llll111l_opy_.bstack1l11l11l1_opy_(CONFIG)
  bstack11111ll1_opy_ = bstack1l111ll1l_opy_.bstack1llll1ll11_opy_(CONFIG, logger)
  bstack1l111l1l1_opy_ = bstack1llll111l_opy_.bstack1llll1ll11_opy_(config=CONFIG)
  if bstack11111ll1_opy_ is not None and bstack1l111l1l1_opy_ is not None and bstack1l111l1l1_opy_.bstack1l1l1111l1_opy_():
    data[bstack1l111l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩඁ")][bstack1l111l1l1_opy_.bstack1lll11l11_opy_()] = bstack11111ll1_opy_.bstack1l11l111_opy_()
  update(data[bstack1l111l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪං")], bstack11ll111l_opy_)
  try:
    response = bstack11l1l1l1l_opy_(bstack1l111l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ඃ"), bstack11ll11ll1_opy_(bstack1l1l1111ll_opy_), data, {
      bstack1l111l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ඄"): (config[bstack1l111l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬඅ")], config[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧආ")])
    })
    if response:
      logger.debug(bstack11l1l1l1l1_opy_.format(bstack1ll1l1ll11_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111ll1l1l_opy_.format(str(e)))
def bstack1l1lll1l11_opy_(framework):
  return bstack1l111l1_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤඇ").format(str(framework), __version__) if framework else bstack1l111l1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢඈ").format(
    __version__)
def bstack11ll1111ll_opy_():
  global CONFIG
  global bstack111l111l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1l1l111_opy_()
    logger.debug(bstack11l1ll11_opy_.format(str(CONFIG)))
    bstack111l111l1_opy_ = bstack1ll1lll11_opy_.configure_logger(CONFIG, bstack111l111l1_opy_)
    bstack111l1l1ll_opy_()
  except Exception as e:
    logger.error(bstack1l111l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦඉ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111ll111l_opy_
  atexit.register(bstack111lllllll_opy_)
  signal.signal(signal.SIGINT, bstack1ll11l1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack1ll11l1ll1_opy_)
def bstack111ll111l_opy_(exctype, value, traceback):
  global bstack1l11ll11_opy_
  try:
    for driver in bstack1l11ll11_opy_:
      bstack11llll1ll_opy_(driver, bstack1l111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨඊ"), bstack1l111l1_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧඋ") + str(value))
  except Exception:
    pass
  logger.info(bstack11ll111l1l_opy_)
  bstack1ll11ll11l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll11ll11l_opy_(message=bstack1l111l1_opy_ (u"ࠪࠫඌ"), bstack1ll1l1l1_opy_ = False):
  global CONFIG
  bstack1ll111ll_opy_ = bstack1l111l1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ඍ") if bstack1ll1l1l1_opy_ else bstack1l111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫඎ")
  try:
    if message:
      bstack11ll111l_opy_ = {
        bstack1ll111ll_opy_ : str(message)
      }
      bstack1l1111llll_opy_(bstack11l1l1lll_opy_, CONFIG, bstack11ll111l_opy_)
    else:
      bstack1l1111llll_opy_(bstack11l1l1lll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1ll11l1_opy_.format(str(e)))
def bstack11ll1llll_opy_(bstack1llll11l_opy_, size):
  bstack1ll1l111_opy_ = []
  while len(bstack1llll11l_opy_) > size:
    bstack1lllll11l_opy_ = bstack1llll11l_opy_[:size]
    bstack1ll1l111_opy_.append(bstack1lllll11l_opy_)
    bstack1llll11l_opy_ = bstack1llll11l_opy_[size:]
  bstack1ll1l111_opy_.append(bstack1llll11l_opy_)
  return bstack1ll1l111_opy_
def bstack111111l1_opy_(args):
  if bstack1l111l1_opy_ (u"࠭࠭࡮ࠩඏ") in args and bstack1l111l1_opy_ (u"ࠧࡱࡦࡥࠫඐ") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1l1l11ll1_opy_, stage=STAGE.bstack1ll1l1llll_opy_)
def run_on_browserstack(bstack111l11l1l_opy_=None, bstack1lll111111_opy_=None, bstack1llll1l1_opy_=False):
  global CONFIG
  global bstack1l1l1l11l1_opy_
  global bstack11ll11l1_opy_
  global bstack11ll1l111_opy_
  global bstack1l1l1111_opy_
  bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠨࠩඑ")
  bstack111lll1l11_opy_(bstack111111lll_opy_, logger)
  if bstack111l11l1l_opy_ and isinstance(bstack111l11l1l_opy_, str):
    bstack111l11l1l_opy_ = eval(bstack111l11l1l_opy_)
  if bstack111l11l1l_opy_:
    CONFIG = bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩඒ")]
    bstack1l1l1l11l1_opy_ = bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫඓ")]
    bstack11ll11l1_opy_ = bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ඔ")]
    bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧඕ"), bstack11ll11l1_opy_)
    bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඖ")
  bstack1l1l1111_opy_.bstack11ll11l11l_opy_(bstack1l111l1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ඗"), uuid4().__str__())
  logger.info(bstack1l111l1_opy_ (u"ࠨࡕࡇࡏࠥࡸࡵ࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭඘") + bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ඙")));
  logger.debug(bstack1l111l1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭ක") + bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ඛ")))
  if not bstack1llll1l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111l1ll1_opy_)
      return
    if sys.argv[1] == bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨග") or sys.argv[1] == bstack1l111l1_opy_ (u"࠭࠭ࡷࠩඝ"):
      logger.info(bstack1l111l1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧඞ").format(__version__))
      return
    if sys.argv[1] == bstack1l111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧඟ"):
      bstack1ll111lll_opy_()
      return
  args = sys.argv
  bstack11ll1111ll_opy_()
  global bstack1lll1ll1l1_opy_
  global bstack1lll11l1_opy_
  global bstack1l1111l1l_opy_
  global bstack1l11111l11_opy_
  global bstack111llll11_opy_
  global bstack1lll111l1_opy_
  global bstack11111l1l_opy_
  global bstack1l1llll1l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack1l11l1l1l1_opy_
  global bstack1llllll11_opy_
  bstack1lll11l1_opy_ = len(CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬච"), []))
  if not bstack11l111111l_opy_:
    if args[1] == bstack1l111l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඡ") or args[1] == bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬජ"):
      bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬඣ")
      args = args[2:]
    elif args[1] == bstack1l111l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඤ"):
      bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ඥ")
      args = args[2:]
    elif args[1] == bstack1l111l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧඦ"):
      bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨට")
      args = args[2:]
    elif args[1] == bstack1l111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඨ"):
      bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬඩ")
      args = args[2:]
    elif args[1] == bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඪ"):
      bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ණ")
      args = args[2:]
    elif args[1] == bstack1l111l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧඬ"):
      bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨත")
      args = args[2:]
    else:
      if not bstack1l111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬථ") in CONFIG or str(CONFIG[bstack1l111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ද")]).lower() in [bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫධ"), bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭න")]:
        bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭඲")
        args = args[1:]
      elif str(CONFIG[bstack1l111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඳ")]).lower() == bstack1l111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧප"):
        bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨඵ")
        args = args[1:]
      elif str(CONFIG[bstack1l111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭බ")]).lower() == bstack1l111l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪභ"):
        bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫම")
        args = args[1:]
      elif str(CONFIG[bstack1l111l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩඹ")]).lower() == bstack1l111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧය"):
        bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨර")
        args = args[1:]
      elif str(CONFIG[bstack1l111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ඼")]).lower() == bstack1l111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪල"):
        bstack11l111111l_opy_ = bstack1l111l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ඾")
        args = args[1:]
      else:
        os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ඿")] = bstack11l111111l_opy_
        bstack1l11lll1_opy_(bstack11l1ll11l1_opy_)
  os.environ[bstack1l111l1_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧව")] = bstack11l111111l_opy_
  bstack11ll1l111_opy_ = bstack11l111111l_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1l1l111ll1_opy_ = bstack1l11l1ll11_opy_[bstack1l111l1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫශ")] if bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෂ") and bstack1lllllll1_opy_() else bstack11l111111l_opy_
      bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.bstack11111111l_opy_, bstack11l111111_opy_(
        sdk_version=__version__,
        path_config=bstack1l11lll1l1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1l1l111ll1_opy_,
        frameworks=[bstack1l1l111ll1_opy_],
        framework_versions={
          bstack1l1l111ll1_opy_: bstack11l11l1ll_opy_(bstack1l111l1_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨස") if bstack11l111111l_opy_ in [bstack1l111l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩහ"), bstack1l111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪළ"), bstack1l111l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ෆ")] else bstack11l111111l_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ෇"), None):
        CONFIG[bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ෈")] = cli.config.get(bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ෉"), None)
    except Exception as e:
      bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.bstack1l1lll1ll1_opy_, e.__traceback__, 1)
    if bstack11ll11l1_opy_:
      CONFIG[bstack1l111l1_opy_ (u"ࠤࡤࡴࡵࠨ්")] = cli.config[bstack1l111l1_opy_ (u"ࠥࡥࡵࡶࠢ෋")]
      logger.info(bstack1l1ll11l1l_opy_.format(CONFIG[bstack1l111l1_opy_ (u"ࠫࡦࡶࡰࠨ෌")]))
  else:
    bstack11ll111ll_opy_.clear()
  global bstack1l111l111_opy_
  global bstack11ll11lll_opy_
  if bstack111l11l1l_opy_:
    try:
      bstack1ll11llll_opy_ = datetime.datetime.now()
      os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෍")] = bstack11l111111l_opy_
      bstack1l1111llll_opy_(bstack1l111ll111_opy_, CONFIG)
      cli.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾ࡸࡪ࡫ࡠࡶࡨࡷࡹࡥࡡࡵࡶࡨࡱࡵࡺࡥࡥࠤ෎"), datetime.datetime.now() - bstack1ll11llll_opy_)
    except Exception as e:
      logger.debug(bstack1ll1l11l1_opy_.format(str(e)))
  global bstack111lll1l1_opy_
  global bstack1l11111l1l_opy_
  global bstack11lllll1_opy_
  global bstack1l1ll111ll_opy_
  global bstack1l1l11l1ll_opy_
  global bstack1l1l11ll1l_opy_
  global bstack1lll11ll11_opy_
  global bstack1lll11lll_opy_
  global bstack1l11l1l11_opy_
  global bstack1l11lll1ll_opy_
  global bstack1111l11l1_opy_
  global bstack1l1l11l11_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1ll111l1l_opy_
  global bstack1l111111ll_opy_
  global bstack1ll1l1lll_opy_
  global bstack1l1l111lll_opy_
  global bstack1l1ll1lll1_opy_
  global bstack1l1l11l111_opy_
  global bstack1lll1lll11_opy_
  global bstack111ll11ll_opy_
  global bstack1lll1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111lll1l1_opy_ = webdriver.Remote.__init__
    bstack1l11111l1l_opy_ = WebDriver.quit
    bstack1l1l11l11_opy_ = WebDriver.close
    bstack1ll1l1lll_opy_ = WebDriver.get
    bstack1lll1l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l111l111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1111l1l11_opy_
    bstack11ll11lll_opy_ = bstack1111l1l11_opy_()
  except Exception as e:
    pass
  try:
    global bstack11l11l111_opy_
    from QWeb.keywords import browser
    bstack11l11l111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1l1ll1_opy_(CONFIG) and bstack11l111l11l_opy_():
    if bstack111l1111l_opy_() < version.parse(bstack1ll11111ll_opy_):
      logger.error(bstack11l1l11l1l_opy_.format(bstack111l1111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        if hasattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨා")) and callable(getattr(RemoteConnection, bstack1l111l1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩැ"))):
          RemoteConnection._get_proxy_url = bstack1l1ll1llll_opy_
        else:
          from selenium.webdriver.remote.client_config import ClientConfig
          ClientConfig.get_proxy_url = bstack1l1ll1llll_opy_
      except Exception as e:
        logger.error(bstack11l1lll111_opy_.format(str(e)))
  if not CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫෑ"), False) and not bstack111l11l1l_opy_:
    logger.info(bstack11111111_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l111l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧි") in CONFIG and str(CONFIG[bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨී")]).lower() != bstack1l111l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫු"):
      bstack1lll11111_opy_()
    elif bstack11l111111l_opy_ != bstack1l111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෕") or (bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧූ") and not bstack111l11l1l_opy_):
      bstack1l1111lll1_opy_()
  if (bstack11l111111l_opy_ in [bstack1l111l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ෗"), bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨෘ"), bstack1l111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫෙ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll111l111_opy_
        bstack1l1l11ll1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warning(bstack1lllll1111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1l11l1ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11ll1ll11l_opy_ + str(e))
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1lllll1111_opy_)
    if bstack11l111111l_opy_ != bstack1l111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬේ"):
      bstack1llllll111_opy_()
    bstack11lllll1_opy_ = Output.start_test
    bstack1l1ll111ll_opy_ = Output.end_test
    bstack1lll11ll11_opy_ = TestStatus.__init__
    bstack1l11l1l11_opy_ = pabot._run
    bstack1l11lll1ll_opy_ = QueueItem.__init__
    bstack1111l11l1_opy_ = pabot._create_command_for_execution
    bstack1lll1lll11_opy_ = pabot._report_results
  if bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬෛ"):
    global bstack1ll1111l_opy_
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1l1ll1l11l_opy_)
    bstack1lll1ll1ll_opy_ = Runner.run_hook
    bstack1ll111l1l_opy_ = Runner.load_hooks
    bstack1l111111ll_opy_ = Step.run
    try:
      sig = inspect.signature(bstack1lll1ll1ll_opy_)
      params = list(sig.parameters.keys())
      bstack1ll1111l_opy_ = bstack1l111l1_opy_ (u"࠭ࡣࡰࡰࡷࡩࡽࡺࠧො") in params
      logger.info(bstack1l111l1_opy_ (u"ࠧࡅࡧࡷࡩࡨࡺࡥࡥࠢࡥࡩ࡭ࡧࡶࡦࠢࡵࡹࡳࡥࡨࡰࡱ࡮ࠤࡸ࡯ࡧ࡯ࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫෝ").format(bstack1l111l1_opy_ (u"ࠨ࠳࠱࠶࠳࠼ࠠࠩࡹ࡬ࡸ࡭ࠦࡣࡰࡰࡷࡩࡽࡺࠩࠨෞ") if bstack1ll1111l_opy_ else bstack1l111l1_opy_ (u"ࠩ࠴࠲࠸࠱ࠠࠩࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡦࡳࡳࡺࡥࡹࡶࠬࠫෟ")))
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡢࡦࡪࡤࡺࡪࠦࡲࡶࡰࡢ࡬ࡴࡵ࡫ࠡࡵ࡬࡫ࡳࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ෠").format(str(e)))
      bstack1ll1111l_opy_ = None
  if bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෡"):
    try:
      from _pytest.config import Config
      bstack1l1ll1lll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l11l111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warning(bstack1l111l1_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧ෢"), bstack1ll1lll1_opy_, str(e))
    try:
      from pytest_bdd import reporting
      bstack111ll11ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ෣"))
    if bstack11l1l111ll_opy_():
      logger.warning(bstack11ll1l1l11_opy_[bstack1l111l1_opy_ (u"ࠧࡔࡆࡎ࠱ࡌࡋࡎ࠮࠲࠳࠹ࠬ෤")])
  try:
    framework_name = bstack1l111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ෥") if bstack11l111111l_opy_ in [bstack1l111l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ෦"), bstack1l111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෧"), bstack1l111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෨")] else bstack11lll11l_opy_(bstack11l111111l_opy_)
    bstack1ll1lllll1_opy_ = {
      bstack1l111l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭෩"): bstack1l111l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ෪") if bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෫") and bstack1lllllll1_opy_() else framework_name,
      bstack1l111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ෬"): bstack11l11l1ll_opy_(framework_name),
      bstack1l111l1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ෭"): __version__,
      bstack1l111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ෮"): bstack11l111111l_opy_
    }
    if bstack11l111111l_opy_ in bstack11ll1ll1ll_opy_ + bstack1l11ll1l11_opy_:
      if bstack11111l11l_opy_.bstack11ll1lll1l_opy_(CONFIG):
        if bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ෯") in CONFIG:
          os.environ[bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭෰")] = os.getenv(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ෱"), json.dumps(CONFIG[bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧෲ")]))
          CONFIG[bstack1l111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨෳ")].pop(bstack1l111l1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ෴"), None)
          CONFIG[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ෵")].pop(bstack1l111l1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ෶"), None)
        bstack1ll1lllll1_opy_[bstack1l111l1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ෷")] = {
          bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෸"): bstack1l111l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ෹"),
          bstack1l111l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ෺"): str(bstack111l1111l_opy_())
        }
    if bstack11l111111l_opy_ not in [bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ෻")] and not cli.is_running():
      bstack11l11l1l1l_opy_, bstack11llll1l1_opy_ = bstack1llll1lll1_opy_.launch(CONFIG, bstack1ll1lllll1_opy_)
      if bstack11llll1l1_opy_.get(bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ෼")) is not None and bstack11111l11l_opy_.bstack1l1lll11l_opy_(CONFIG) is None:
        value = bstack11llll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ෽")].get(bstack1l111l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭෾"))
        if value is not None:
            CONFIG[bstack1l111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෿")] = value
        else:
          logger.debug(bstack1l111l1_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ฀"))
  except Exception as e:
    logger.debug(bstack11l11lll11_opy_.format(bstack1l111l1_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩก"), str(e)))
  if bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩข"):
    bstack1l1111l1l_opy_ = True
    if bstack111l11l1l_opy_ and bstack1llll1l1_opy_:
      bstack1lll111l1_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧฃ"), {}).get(bstack1l111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ค"))
      bstack1111l1111_opy_(bstack1ll11ll1l1_opy_)
    elif bstack111l11l1l_opy_:
      bstack1lll111l1_opy_ = CONFIG.get(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩฅ"), {}).get(bstack1l111l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨฆ"))
      global bstack1l11ll11_opy_
      try:
        if bstack111111l1_opy_(bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪง")]) and multiprocessing.current_process().name == bstack1l111l1_opy_ (u"ࠨ࠲ࠪจ"):
          bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฉ")].remove(bstack1l111l1_opy_ (u"ࠪ࠱ࡲ࠭ช"))
          bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧซ")].remove(bstack1l111l1_opy_ (u"ࠬࡶࡤࡣࠩฌ"))
          bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩญ")] = bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪฎ")][0]
          with open(bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฏ")], bstack1l111l1_opy_ (u"ࠩࡵࠫฐ")) as f:
            bstack11l1lllll_opy_ = f.read()
          bstack1ll11111_opy_ = bstack1l111l1_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨฑ").format(str(bstack111l11l1l_opy_))
          bstack11lllll111_opy_ = bstack1ll11111_opy_ + bstack11l1lllll_opy_
          bstack111ll1l11l_opy_ = bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧฒ")] + bstack1l111l1_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧณ")
          with open(bstack111ll1l11l_opy_, bstack1l111l1_opy_ (u"࠭ࡷࠨด")):
            pass
          with open(bstack111ll1l11l_opy_, bstack1l111l1_opy_ (u"ࠢࡸ࠭ࠥต")) as f:
            f.write(bstack11lllll111_opy_)
          import subprocess
          bstack11l11111ll_opy_ = subprocess.run([bstack1l111l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣถ"), bstack111ll1l11l_opy_])
          if os.path.exists(bstack111ll1l11l_opy_):
            os.unlink(bstack111ll1l11l_opy_)
          os._exit(bstack11l11111ll_opy_.returncode)
        else:
          if bstack111111l1_opy_(bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬท")]):
            bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ธ")].remove(bstack1l111l1_opy_ (u"ࠫ࠲ࡳࠧน"))
            bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨบ")].remove(bstack1l111l1_opy_ (u"࠭ࡰࡥࡤࠪป"))
            bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪผ")] = bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฝ")][0]
          bstack1111l1111_opy_(bstack1ll11ll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬพ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l111l1_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬฟ")] = bstack1l111l1_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ภ")
          mod_globals[bstack1l111l1_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧม")] = os.path.abspath(bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩย")])
          exec(open(bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪร")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l111l1_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨฤ").format(str(e)))
          for driver in bstack1l11ll11_opy_:
            bstack1lll111111_opy_.append({
              bstack1l111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧล"): bstack111l11l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฦ")],
              bstack1l111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪว"): str(e),
              bstack1l111l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫศ"): multiprocessing.current_process().name
            })
            bstack11llll1ll_opy_(driver, bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ษ"), bstack1l111l1_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥส") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11ll11_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11ll11l1_opy_, CONFIG, logger)
      bstack11ll1l11_opy_()
      bstack1ll1l11ll_opy_()
      percy.bstack1ll11111l_opy_()
      bstack11lllll1l1_opy_ = {
        bstack1l111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫห"): args[0],
        bstack1l111l1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩฬ"): CONFIG,
        bstack1l111l1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫอ"): bstack1l1l1l11l1_opy_,
        bstack1l111l1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ฮ"): bstack11ll11l1_opy_
      }
      if bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨฯ") in CONFIG:
        bstack11llllll1_opy_ = bstack1l111l11l_opy_(args, logger, CONFIG, bstack11l1ll1l1_opy_, bstack1lll11l1_opy_)
        bstack1l1llll1l1_opy_ = bstack11llllll1_opy_.bstack1lllll11_opy_(run_on_browserstack, bstack11lllll1l1_opy_, bstack111111l1_opy_(args))
      else:
        if bstack111111l1_opy_(args):
          bstack11lllll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩะ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11lllll1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1111l1111_opy_(bstack1ll11ll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l111l1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩั")] = bstack1l111l1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪา")
          mod_globals[bstack1l111l1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫำ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩิ") or bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪี"):
    percy.init(bstack11ll11l1_opy_, CONFIG, logger)
    percy.bstack1ll11111l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1lllll1111_opy_)
    bstack11ll1l11_opy_()
    bstack1111l1111_opy_(bstack1l1lll1l1_opy_)
    if bstack11l1ll1l1_opy_:
      bstack1l1l1l1ll_opy_(bstack1l1lll1l1_opy_, args)
      if bstack1l111l1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪึ") in args:
        i = args.index(bstack1l111l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫื"))
        args.pop(i)
        args.pop(i)
      if bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵุࠪ") not in CONFIG:
        CONFIG[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶูࠫ")] = [{}]
        bstack1lll11l1_opy_ = 1
      if bstack1lll1ll1l1_opy_ == 0:
        bstack1lll1ll1l1_opy_ = 1
      args.insert(0, str(bstack1lll1ll1l1_opy_))
      args.insert(0, str(bstack1l111l1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹฺࠧ")))
    if bstack1llll1lll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1llll1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1111lll1l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l111l1_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ฻"),
        ).parse_args(bstack1l1llll1l_opy_)
        bstack111l111l_opy_ = args.index(bstack1l1llll1l_opy_[0]) if len(bstack1l1llll1l_opy_) > 0 else len(args)
        args.insert(bstack111l111l_opy_, str(bstack1l111l1_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ฼")))
        args.insert(bstack111l111l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ฽"))))
        if bstack1llll111l_opy_.bstack1ll111l1ll_opy_(CONFIG):
          args.insert(bstack111l111l_opy_, str(bstack1l111l1_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ฾")))
          args.insert(bstack111l111l_opy_ + 1, str(bstack1l111l1_opy_ (u"ࠧࡓࡧࡷࡶࡾࡌࡡࡪ࡮ࡨࡨ࠿ࢁࡽࠨ฿").format(bstack1llll111l_opy_.bstack1lll1111_opy_(CONFIG))))
        if bstack11lll111_opy_(os.environ.get(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭เ"))) and str(os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭แ"), bstack1l111l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨโ"))) != bstack1l111l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩใ"):
          for bstack1lll1111l_opy_ in bstack1111lll1l_opy_:
            args.remove(bstack1lll1111l_opy_)
          test_files = os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩไ")).split(bstack1l111l1_opy_ (u"࠭ࠬࠨๅ"))
          for bstack11111l1ll_opy_ in test_files:
            args.append(bstack11111l1ll_opy_)
      except Exception as e:
        logger.error(bstack1l111l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠣๆ").format(bstack1ll1l1l11_opy_, e))
    pabot.main(args)
  elif bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ็"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1lllll1111_opy_)
    for a in args:
      if bstack1l111l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ่") in a:
        bstack111llll11_opy_ = int(a.split(bstack1l111l1_opy_ (u"ࠪ࠾้ࠬ"))[1])
      if bstack1l111l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ๊") in a:
        bstack1lll111l1_opy_ = str(a.split(bstack1l111l1_opy_ (u"ࠬࡀ๋ࠧ"))[1])
      if bstack1l111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭์") in a:
        bstack11111l1l_opy_ = str(a.split(bstack1l111l1_opy_ (u"ࠧ࠻ࠩํ"))[1])
    bstack111lll1l_opy_ = None
    bstack11l1lll1ll_opy_ = None
    if bstack1l111l1_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ๎") in args:
      i = args.index(bstack1l111l1_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ๏"))
      args.pop(i)
      bstack111lll1l_opy_ = args.pop(i)
    if bstack1l111l1_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽ࠭๐") in args:
      i = args.index(bstack1l111l1_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠧ๑"))
      args.pop(i)
      bstack11l1lll1ll_opy_ = args.pop(i)
    if bstack111lll1l_opy_ is not None:
      global bstack11l1ll11l_opy_
      bstack11l1ll11l_opy_ = bstack111lll1l_opy_
    if bstack11l1lll1ll_opy_ is not None and int(bstack111llll11_opy_) < 0:
      bstack111llll11_opy_ = int(bstack11l1lll1ll_opy_)
    bstack1111l1111_opy_(bstack1l1lll1l1_opy_)
    run_cli(args)
    if bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ๒") in multiprocessing.current_process().__dict__.keys():
      for bstack11l1l11l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll111111_opy_.append(bstack11l1l11l11_opy_)
  elif bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭๓"):
    bstack1l1llll111_opy_ = bstack1lllllllll_opy_(args, logger, CONFIG, bstack11l1ll1l1_opy_)
    bstack1l1llll111_opy_.bstack11l1l1l1_opy_()
    bstack11ll1l11_opy_()
    bstack1l11111l11_opy_ = True
    bstack1l11l1l1l1_opy_ = bstack1l1llll111_opy_.bstack11lllll11l_opy_()
    bstack1l1llll111_opy_.bstack11lllll1l1_opy_(bstack1ll1l1ll1_opy_)
    bstack1l1llll111_opy_.bstack111l1l1l1_opy_()
    bstack1l11l11l1l_opy_(bstack11l111111l_opy_, CONFIG, bstack1l1llll111_opy_.bstack1l111111_opy_())
    bstack1llll1llll_opy_ = bstack1l1llll111_opy_.bstack1lllll11_opy_(bstack111llll1l1_opy_, {
      bstack1l111l1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ๔"): bstack1l1l1l11l1_opy_,
      bstack1l111l1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ๕"): bstack11ll11l1_opy_,
      bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ๖"): bstack11l1ll1l1_opy_
    })
    try:
      bstack11111l111_opy_, bstack11ll1l11l_opy_ = map(list, zip(*bstack1llll1llll_opy_))
      bstack1ll1111ll1_opy_ = bstack11111l111_opy_[0]
      for status_code in bstack11ll1l11l_opy_:
        if status_code != 0:
          bstack1llllll11_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣ๗").format(str(e)))
  elif bstack11l111111l_opy_ == bstack1l111l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ๘"):
    try:
      from behave.__main__ import main as bstack1ll1l1ll1l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1l1ll1l_opy_(e, bstack1l1ll1l11l_opy_)
    bstack11ll1l11_opy_()
    bstack1l11111l11_opy_ = True
    bstack1lll111l_opy_ = 1
    if bstack1l111l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ๙") in CONFIG:
      bstack1lll111l_opy_ = CONFIG[bstack1l111l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭๚")]
    if bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๛") in CONFIG:
      bstack11l1lll1l_opy_ = int(bstack1lll111l_opy_) * int(len(CONFIG[bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๜")]))
    else:
      bstack11l1lll1l_opy_ = int(bstack1lll111l_opy_)
    config = Configuration(args)
    bstack1llll11l1l_opy_ = config.paths
    if len(bstack1llll11l1l_opy_) == 0:
      import glob
      pattern = bstack1l111l1_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨ๝")
      bstack1llll111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1llll111_opy_)
      config = Configuration(args)
      bstack1llll11l1l_opy_ = config.paths
    bstack111lll111_opy_ = [os.path.normpath(item) for item in bstack1llll11l1l_opy_]
    bstack1l111ll11l_opy_ = [os.path.normpath(item) for item in args]
    bstack11l11ll11_opy_ = [item for item in bstack1l111ll11l_opy_ if item not in bstack111lll111_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l111l1_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫ๞"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111lll111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll1ll1l11_opy_)))
                    for bstack1ll1ll1l11_opy_ in bstack111lll111_opy_]
    bstack11l11l1l_opy_ = []
    for spec in bstack111lll111_opy_:
      bstack11llll11ll_opy_ = []
      bstack11llll11ll_opy_ += bstack11l11ll11_opy_
      bstack11llll11ll_opy_.append(spec)
      bstack11l11l1l_opy_.append(bstack11llll11ll_opy_)
    execution_items = []
    for bstack11llll11ll_opy_ in bstack11l11l1l_opy_:
      if bstack1l111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๟") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๠")]):
          item = {}
          item[bstack1l111l1_opy_ (u"࠭ࡡࡳࡩࠪ๡")] = bstack1l111l1_opy_ (u"ࠧࠡࠩ๢").join(bstack11llll11ll_opy_)
          item[bstack1l111l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ๣")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l111l1_opy_ (u"ࠩࡤࡶ࡬࠭๤")] = bstack1l111l1_opy_ (u"ࠪࠤࠬ๥").join(bstack11llll11ll_opy_)
        item[bstack1l111l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ๦")] = 0
        execution_items.append(item)
    bstack1ll11l1lll_opy_ = bstack11ll1llll_opy_(execution_items, bstack11l1lll1l_opy_)
    for execution_item in bstack1ll11l1lll_opy_:
      bstack1l1lll111l_opy_ = []
      for item in execution_item:
        bstack1l1lll111l_opy_.append(bstack11l11ll1l_opy_(name=str(item[bstack1l111l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ๧")]),
                                             target=bstack11ll1llll1_opy_,
                                             args=(item[bstack1l111l1_opy_ (u"࠭ࡡࡳࡩࠪ๨")],)))
      for t in bstack1l1lll111l_opy_:
        t.start()
      for t in bstack1l1lll111l_opy_:
        t.join()
  else:
    bstack1l11lll1_opy_(bstack11l1ll11l1_opy_)
  if not bstack111l11l1l_opy_:
    bstack1l1l1lll_opy_()
    if(bstack11l111111l_opy_ in [bstack1l111l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ๩"), bstack1l111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ๪")]):
      bstack1l111ll1l1_opy_()
  bstack1ll1lll11_opy_.bstack1lll111l11_opy_()
def browserstack_initialize(bstack1lll1l11l1_opy_=None):
  logger.info(bstack1l111l1_opy_ (u"ࠩࡕࡹࡳࡴࡩ࡯ࡩࠣࡗࡉࡑࠠࡸ࡫ࡷ࡬ࠥࡧࡲࡨࡵ࠽ࠤࠬ๫") + str(bstack1lll1l11l1_opy_))
  run_on_browserstack(bstack1lll1l11l1_opy_, None, True)
@measure(event_name=EVENTS.bstack11ll11ll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1l1l1lll_opy_():
  global CONFIG
  global bstack11ll1l111_opy_
  global bstack1llllll11_opy_
  global bstack1lll111ll_opy_
  global bstack1l1l1111_opy_
  bstack11l11l1l1_opy_.bstack1l11ll1ll1_opy_()
  if cli.is_running():
    bstack11ll111ll_opy_.invoke(bstack1lll1ll1_opy_.bstack1lll11l1l_opy_)
  else:
    bstack1l111l1l1_opy_ = bstack1llll111l_opy_.bstack1llll1ll11_opy_(config=CONFIG)
    bstack1l111l1l1_opy_.bstack1lll1lllll_opy_(CONFIG)
  if bstack11ll1l111_opy_ == bstack1l111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ๬"):
    if not cli.is_enabled(CONFIG):
      bstack1llll1lll1_opy_.stop()
  else:
    bstack1llll1lll1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack11ll11l11_opy_.bstack111lll11ll_opy_()
  if bstack1l111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ๭") in CONFIG and str(CONFIG[bstack1l111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ๮")]).lower() != bstack1l111l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ๯"):
    hashed_id, bstack11ll1l1l1_opy_ = bstack1ll11lll1l_opy_()
  else:
    hashed_id, bstack11ll1l1l1_opy_ = get_build_link()
  bstack111ll11l1_opy_(hashed_id)
  logger.info(bstack1l111l1_opy_ (u"ࠧࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠࡧࡱࡵࠤ࡮ࡪ࠺ࠨ๰") + bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ๱"), bstack1l111l1_opy_ (u"ࠩࠪ๲")) + bstack1l111l1_opy_ (u"ࠪ࠰ࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡩࡥ࠼ࠣࠫ๳") + os.getenv(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ๴"), bstack1l111l1_opy_ (u"ࠬ࠭๵")))
  if hashed_id is not None and bstack11l1lll11l_opy_() != -1:
    sessions = bstack11l11ll1ll_opy_(hashed_id)
    bstack1ll11l111_opy_(sessions, bstack11ll1l1l1_opy_)
  if bstack11ll1l111_opy_ == bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭๶") and bstack1llllll11_opy_ != 0:
    sys.exit(bstack1llllll11_opy_)
  if bstack11ll1l111_opy_ == bstack1l111l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ๷") and bstack1lll111ll_opy_ != 0:
    sys.exit(bstack1lll111ll_opy_)
def bstack111ll11l1_opy_(new_id):
    global bstack1l1lll1111_opy_
    bstack1l1lll1111_opy_ = new_id
def bstack11lll11l_opy_(bstack1l11llllll_opy_):
  if bstack1l11llllll_opy_:
    return bstack1l11llllll_opy_.capitalize()
  else:
    return bstack1l111l1_opy_ (u"ࠨࠩ๸")
@measure(event_name=EVENTS.bstack11l1ll1l11_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll1l1l1ll_opy_(bstack1l1lll1l1l_opy_):
  if bstack1l111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๹") in bstack1l1lll1l1l_opy_ and bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ๺")] != bstack1l111l1_opy_ (u"ࠫࠬ๻"):
    return bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๼")]
  else:
    bstack111l1l11_opy_ = bstack1l111l1_opy_ (u"ࠨࠢ๽")
    if bstack1l111l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ๾") in bstack1l1lll1l1l_opy_ and bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ๿")] != None:
      bstack111l1l11_opy_ += bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ຀")] + bstack1l111l1_opy_ (u"ࠥ࠰ࠥࠨກ")
      if bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠫࡴࡹࠧຂ")] == bstack1l111l1_opy_ (u"ࠧ࡯࡯ࡴࠤ຃"):
        bstack111l1l11_opy_ += bstack1l111l1_opy_ (u"ࠨࡩࡐࡕࠣࠦຄ")
      bstack111l1l11_opy_ += (bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ຅")] or bstack1l111l1_opy_ (u"ࠨࠩຆ"))
      return bstack111l1l11_opy_
    else:
      bstack111l1l11_opy_ += bstack11lll11l_opy_(bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪງ")]) + bstack1l111l1_opy_ (u"ࠥࠤࠧຈ") + (
              bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ຉ")] or bstack1l111l1_opy_ (u"ࠬ࠭ຊ")) + bstack1l111l1_opy_ (u"ࠨࠬࠡࠤ຋")
      if bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠧࡰࡵࠪຌ")] == bstack1l111l1_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤຍ"):
        bstack111l1l11_opy_ += bstack1l111l1_opy_ (u"ࠤ࡚࡭ࡳࠦࠢຎ")
      bstack111l1l11_opy_ += bstack1l1lll1l1l_opy_[bstack1l111l1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧຏ")] or bstack1l111l1_opy_ (u"ࠫࠬຐ")
      return bstack111l1l11_opy_
@measure(event_name=EVENTS.bstack1lll1llll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll1ll11_opy_(bstack11l1l1l111_opy_):
  if bstack11l1l1l111_opy_ == bstack1l111l1_opy_ (u"ࠧࡪ࡯࡯ࡧࠥຑ"):
    return bstack1l111l1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩຒ")
  elif bstack11l1l1l111_opy_ == bstack1l111l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢຓ"):
    return bstack1l111l1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫດ")
  elif bstack11l1l1l111_opy_ == bstack1l111l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤຕ"):
    return bstack1l111l1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪຖ")
  elif bstack11l1l1l111_opy_ == bstack1l111l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥທ"):
    return bstack1l111l1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧຘ")
  elif bstack11l1l1l111_opy_ == bstack1l111l1_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢນ"):
    return bstack1l111l1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬບ")
  elif bstack11l1l1l111_opy_ == bstack1l111l1_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤປ"):
    return bstack1l111l1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪຜ")
  else:
    return bstack1l111l1_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧຝ") + bstack11lll11l_opy_(
      bstack11l1l1l111_opy_) + bstack1l111l1_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪພ")
def bstack11111ll1l_opy_(session):
  return bstack1l111l1_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬຟ").format(
    session[bstack1l111l1_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪຠ")], bstack1ll1l1l1ll_opy_(session), bstack1ll1ll11_opy_(session[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭ມ")]),
    bstack1ll1ll11_opy_(session[bstack1l111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨຢ")]),
    bstack11lll11l_opy_(session[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪຣ")] or session[bstack1l111l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ຤")] or bstack1l111l1_opy_ (u"ࠫࠬລ")) + bstack1l111l1_opy_ (u"ࠧࠦࠢ຦") + (session[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨວ")] or bstack1l111l1_opy_ (u"ࠧࠨຨ")),
    session[bstack1l111l1_opy_ (u"ࠨࡱࡶࠫຩ")] + bstack1l111l1_opy_ (u"ࠤࠣࠦສ") + session[bstack1l111l1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧຫ")], session[bstack1l111l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ຬ")] or bstack1l111l1_opy_ (u"ࠬ࠭ອ"),
    session[bstack1l111l1_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪຮ")] if session[bstack1l111l1_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫຯ")] else bstack1l111l1_opy_ (u"ࠨࠩະ"))
@measure(event_name=EVENTS.bstack1lllll11ll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def bstack1ll11l111_opy_(sessions, bstack11ll1l1l1_opy_):
  try:
    bstack1ll11ll1ll_opy_ = bstack1l111l1_opy_ (u"ࠤࠥັ")
    if not os.path.exists(bstack1l1l111l1_opy_):
      os.mkdir(bstack1l1l111l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l111l1_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨາ")), bstack1l111l1_opy_ (u"ࠫࡷ࠭ຳ")) as f:
      bstack1ll11ll1ll_opy_ = f.read()
    bstack1ll11ll1ll_opy_ = bstack1ll11ll1ll_opy_.replace(bstack1l111l1_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩິ"), str(len(sessions)))
    bstack1ll11ll1ll_opy_ = bstack1ll11ll1ll_opy_.replace(bstack1l111l1_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭ີ"), bstack11ll1l1l1_opy_)
    bstack1ll11ll1ll_opy_ = bstack1ll11ll1ll_opy_.replace(bstack1l111l1_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨຶ"),
                                              sessions[0].get(bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬື")) if sessions[0] else bstack1l111l1_opy_ (u"ຸࠩࠪ"))
    with open(os.path.join(bstack1l1l111l1_opy_, bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲູࠧ")), bstack1l111l1_opy_ (u"ࠫࡼ຺࠭")) as stream:
      stream.write(bstack1ll11ll1ll_opy_.split(bstack1l111l1_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩົ"))[0])
      for session in sessions:
        stream.write(bstack11111ll1l_opy_(session))
      stream.write(bstack1ll11ll1ll_opy_.split(bstack1l111l1_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪຼ"))[1])
    logger.info(bstack1l111l1_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪຽ").format(bstack1l1l111l1_opy_));
  except Exception as e:
    logger.debug(bstack11ll1111l_opy_.format(str(e)))
def bstack11l11ll1ll_opy_(hashed_id):
  global CONFIG
  try:
    bstack1ll11llll_opy_ = datetime.datetime.now()
    host = bstack1l111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ຾") if bstack1l111l1_opy_ (u"ࠩࡤࡴࡵ࠭຿") in CONFIG else bstack1l111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫເ")
    user = CONFIG[bstack1l111l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ແ")]
    key = CONFIG[bstack1l111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨໂ")]
    bstack11l111l1l_opy_ = bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬໃ") if bstack1l111l1_opy_ (u"ࠧࡢࡲࡳࠫໄ") in CONFIG else (bstack1l111l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ໅") if CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ໆ")) else bstack1l111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ໇"))
    host = bstack1llll1l1ll_opy_(cli.config, [bstack1l111l1_opy_ (u"ࠦࡦࡶࡩࡴࠤ່"), bstack1l111l1_opy_ (u"ࠧࡧࡰࡱࡃࡸࡸࡴࡳࡡࡵࡧ້ࠥ"), bstack1l111l1_opy_ (u"ࠨࡡࡱ࡫໊ࠥ")], host) if bstack1l111l1_opy_ (u"ࠧࡢࡲࡳ໋ࠫ") in CONFIG else bstack1llll1l1ll_opy_(cli.config, [bstack1l111l1_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ໌"), bstack1l111l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦໍ"), bstack1l111l1_opy_ (u"ࠥࡥࡵ࡯ࠢ໎")], host)
    url = bstack1l111l1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭໏").format(host, bstack11l111l1l_opy_, hashed_id)
    headers = {
      bstack1l111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ໐"): bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ໑"),
    }
    proxies = bstack111lll1l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies, auth=(user, key))
    if response.json():
      cli.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࡣࡱ࡯ࡳࡵࠤ໒"), datetime.datetime.now() - bstack1ll11llll_opy_)
      return list(map(lambda session: session[bstack1l111l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭໓")], response.json()))
  except Exception as e:
    logger.debug(bstack1111lllll_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11lllll11_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def get_build_link():
  global CONFIG
  global bstack1l1lll1111_opy_
  try:
    if bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ໔") in CONFIG:
      bstack1ll11llll_opy_ = datetime.datetime.now()
      host = bstack1l111l1_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭໕") if bstack1l111l1_opy_ (u"ࠫࡦࡶࡰࠨ໖") in CONFIG else bstack1l111l1_opy_ (u"ࠬࡧࡰࡪࠩ໗")
      user = CONFIG[bstack1l111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ໘")]
      key = CONFIG[bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ໙")]
      bstack11l111l1l_opy_ = bstack1l111l1_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ໚") if bstack1l111l1_opy_ (u"ࠩࡤࡴࡵ࠭໛") in CONFIG else bstack1l111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬໜ")
      url = bstack1l111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫໝ").format(user, key, host, bstack11l111l1l_opy_)
      if cli.is_enabled(CONFIG):
        bstack11ll1l1l1_opy_, hashed_id = cli.bstack1l1l1ll111_opy_()
        logger.info(bstack1lll1lll1_opy_.format(bstack11ll1l1l1_opy_))
        return [hashed_id, bstack11ll1l1l1_opy_]
      else:
        headers = {
          bstack1l111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫໞ"): bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩໟ"),
        }
        if bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ໠") in CONFIG:
          params = {bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭໡"): CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ໢")], bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭໣"): CONFIG[bstack1l111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭໤")]}
        else:
          params = {bstack1l111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ໥"): CONFIG[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ໦")]}
        proxies = bstack111lll1l1l_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1l111l11_opy_ = response.json()[0][bstack1l111l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ໧")]
          if bstack1l1l111l11_opy_:
            bstack11ll1l1l1_opy_ = bstack1l1l111l11_opy_[bstack1l111l1_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ໨")].split(bstack1l111l1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨ໩"))[0] + bstack1l111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫ໪") + bstack1l1l111l11_opy_[
              bstack1l111l1_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ໫")]
            logger.info(bstack1lll1lll1_opy_.format(bstack11ll1l1l1_opy_))
            bstack1l1lll1111_opy_ = bstack1l1l111l11_opy_[bstack1l111l1_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ໬")]
            bstack1l1111ll11_opy_ = CONFIG[bstack1l111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ໭")]
            if bstack1l111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ໮") in CONFIG:
              bstack1l1111ll11_opy_ += bstack1l111l1_opy_ (u"ࠨࠢࠪ໯") + CONFIG[bstack1l111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ໰")]
            if bstack1l1111ll11_opy_ != bstack1l1l111l11_opy_[bstack1l111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ໱")]:
              logger.debug(bstack1l1l11l11l_opy_.format(bstack1l1l111l11_opy_[bstack1l111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ໲")], bstack1l1111ll11_opy_))
            cli.bstack111lll11l_opy_(bstack1l111l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࡫ࡪࡺ࡟ࡣࡷ࡬ࡰࡩࡥ࡬ࡪࡰ࡮ࠦ໳"), datetime.datetime.now() - bstack1ll11llll_opy_)
            return [bstack1l1l111l11_opy_[bstack1l111l1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ໴")], bstack11ll1l1l1_opy_]
    else:
      logger.warning(bstack11ll111l1_opy_)
  except Exception as e:
    logger.debug(bstack1l11111l1_opy_.format(str(e)))
  return [None, None]
def bstack111llllll1_opy_(url, bstack111111111_opy_=False):
  global CONFIG
  global bstack1l11llll1_opy_
  if not bstack1l11llll1_opy_:
    hostname = bstack1ll1l1l1l1_opy_(url)
    is_private = bstack1ll111l1_opy_(hostname)
    if (bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ໵") in CONFIG and not bstack11lll111_opy_(CONFIG[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ໶")])) and (is_private or bstack111111111_opy_):
      bstack1l11llll1_opy_ = hostname
def bstack1ll1l1l1l1_opy_(url):
  return urlparse(url).hostname
def bstack1ll111l1_opy_(hostname):
  for bstack111lllll1_opy_ in bstack1l1l1l1l_opy_:
    regex = re.compile(bstack111lllll1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1l1l11ll_opy_(bstack1l11ll1111_opy_):
  return True if bstack1l11ll1111_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1111ll1l1_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack111llll11_opy_
  bstack11ll11l1l1_opy_ = not (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭໷"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ໸"), None))
  bstack11ll1l1l_opy_ = getattr(driver, bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ໹"), None) != True
  bstack1111l11l_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ໺"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ໻"), None)
  if bstack1111l11l_opy_:
    if not bstack1l11ll1lll_opy_():
      logger.warning(bstack1l111l1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡰࡱࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ໼"))
      return {}
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ໽"))
    logger.debug(perform_scan(driver, driver_command=bstack1l111l1_opy_ (u"ࠩࡨࡼࡪࡩࡵࡵࡧࡖࡧࡷ࡯ࡰࡵࠩ໾")))
    results = bstack1l111lll11_opy_(bstack1l111l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦ໿"))
    if results is not None and results.get(bstack1l111l1_opy_ (u"ࠦ࡮ࡹࡳࡶࡧࡶࠦༀ")) is not None:
        return results[bstack1l111l1_opy_ (u"ࠧ࡯ࡳࡴࡷࡨࡷࠧ༁")]
    logger.error(bstack1l111l1_opy_ (u"ࠨࡎࡰࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡕࡩࡸࡻ࡬ࡵࡵࠣࡻࡪࡸࡥࠡࡨࡲࡹࡳࡪ࠮ࠣ༂"))
    return []
  if not bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack111llll11_opy_) or (bstack11ll1l1l_opy_ and bstack11ll11l1l1_opy_):
    logger.warning(bstack1l111l1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ༃"))
    return {}
  try:
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ༄"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l111l1l_opy_.bstack1ll111ll1_opy_)
    return results
  except Exception:
    logger.error(bstack1l111l1_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ༅"))
    return {}
@measure(event_name=EVENTS.bstack11l111lll1_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack111llll11_opy_
  bstack11ll11l1l1_opy_ = not (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ༆"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ༇"), None))
  bstack11ll1l1l_opy_ = getattr(driver, bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ༈"), None) != True
  bstack1111l11l_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༉"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༊"), None)
  if bstack1111l11l_opy_:
    if not bstack1l11ll1lll_opy_():
      logger.warning(bstack1l111l1_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨ་"))
      return {}
    logger.debug(bstack1l111l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ༌"))
    logger.debug(perform_scan(driver, driver_command=bstack1l111l1_opy_ (u"ࠪࡩࡽ࡫ࡣࡶࡶࡨࡗࡨࡸࡩࡱࡶࠪ།")))
    results = bstack1l111lll11_opy_(bstack1l111l1_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦ༎"))
    if results is not None and results.get(bstack1l111l1_opy_ (u"ࠧࡹࡵ࡮࡯ࡤࡶࡾࠨ༏")) is not None:
        return results[bstack1l111l1_opy_ (u"ࠨࡳࡶ࡯ࡰࡥࡷࡿࠢ༐")]
    logger.error(bstack1l111l1_opy_ (u"ࠢࡏࡱࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡖࡪࡹࡵ࡭ࡶࡶࠤࡘࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ༑"))
    return {}
  if not bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack111llll11_opy_) or (bstack11ll1l1l_opy_ and bstack11ll11l1l1_opy_):
    logger.warning(bstack1l111l1_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧ༒"))
    return {}
  try:
    logger.debug(bstack1l111l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧ༓"))
    logger.debug(perform_scan(driver))
    bstack1ll1ll11l_opy_ = driver.execute_async_script(bstack1l111l1l_opy_.bstack11l1111l11_opy_)
    return bstack1ll1ll11l_opy_
  except Exception:
    logger.error(bstack1l111l1_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ༔"))
    return {}
def bstack1l11ll1lll_opy_():
  global CONFIG
  global bstack111llll11_opy_
  bstack11ll111lll_opy_ = bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ༕"), None) and bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ༖"), None)
  if not bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack111llll11_opy_) or not bstack11ll111lll_opy_:
        logger.warning(bstack1l111l1_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡱࡲࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ༗"))
        return False
  return True
def bstack1l111lll11_opy_(result_type):
    bstack11l11111l_opy_ = bstack1llll1lll1_opy_.current_test_uuid() if bstack1llll1lll1_opy_.current_test_uuid() else bstack11ll11l11_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11l1111l1l_opy_(bstack11l11111l_opy_, result_type))
        try:
            return future.result(timeout=bstack1l1lllll11_opy_)
        except TimeoutError:
            logger.error(bstack1l111l1_opy_ (u"ࠢࡕ࡫ࡰࡩࡴࡻࡴࠡࡣࡩࡸࡪࡸࠠࡼࡿࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠨ༘").format(bstack1l1lllll11_opy_))
        except Exception as ex:
            logger.debug(bstack1l111l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡳࡧࡷࡶ࡮࡫ࡶࡪࡰࡪࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࢁࡽ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࡿࢂࠨ༙").format(result_type, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack11ll111111_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack111l1l11_opy_=bstack1l1l1l1ll1_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack111llll11_opy_
  bstack11ll11l1l1_opy_ = not (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭༚"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ༛"), None))
  bstack1lllll1l1l_opy_ = not (bstack1l1l1l111_opy_(threading.current_thread(), bstack1l111l1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ༜"), None) and bstack1l1l1l111_opy_(
          threading.current_thread(), bstack1l111l1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ༝"), None))
  bstack11ll1l1l_opy_ = getattr(driver, bstack1l111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭༞"), None) != True
  if not bstack11111l11l_opy_.bstack1l1llllll1_opy_(CONFIG, bstack111llll11_opy_) or (bstack11ll1l1l_opy_ and bstack11ll11l1l1_opy_ and bstack1lllll1l1l_opy_):
    logger.warning(bstack1l111l1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ༟"))
    return {}
  try:
    bstack11111lll_opy_ = bstack1l111l1_opy_ (u"ࠨࡣࡳࡴࠬ༠") in CONFIG and CONFIG.get(bstack1l111l1_opy_ (u"ࠩࡤࡴࡵ࠭༡"), bstack1l111l1_opy_ (u"ࠪࠫ༢"))
    session_id = getattr(driver, bstack1l111l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ༣"), None)
    if not session_id:
      logger.warning(bstack1l111l1_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡌࡈࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡦࡵ࡭ࡻ࡫ࡲࠣ༤"))
      return {bstack1l111l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ༥"): bstack1l111l1_opy_ (u"ࠢࡏࡱࠣࡷࡪࡹࡳࡪࡱࡱࠤࡎࡊࠠࡧࡱࡸࡲࡩࠨ༦")}
    if bstack11111lll_opy_:
      try:
        bstack1111l111l_opy_ = {
              bstack1l111l1_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬ༧"): os.environ.get(bstack1l111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ༨"), os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ༩"), bstack1l111l1_opy_ (u"ࠫࠬ༪"))),
              bstack1l111l1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ༫"): bstack1llll1lll1_opy_.current_test_uuid() if bstack1llll1lll1_opy_.current_test_uuid() else bstack11ll11l11_opy_.current_hook_uuid(),
              bstack1l111l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠪ༬"): os.environ.get(bstack1l111l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ༭")),
              bstack1l111l1_opy_ (u"ࠨࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༮"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack1l111l1_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ༯"): os.environ.get(bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ༰"), bstack1l111l1_opy_ (u"ࠫࠬ༱")),
              bstack1l111l1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ༲"): kwargs.get(bstack1l111l1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧ༳"), None) or bstack1l111l1_opy_ (u"ࠧࠨ༴")
          }
        if not hasattr(thread_local, bstack1l111l1_opy_ (u"ࠨࡤࡤࡷࡪࡥࡡࡱࡲࡢࡥ࠶࠷ࡹࡠࡵࡦࡶ࡮ࡶࡴࠨ༵")):
            scripts = {bstack1l111l1_opy_ (u"ࠩࡶࡧࡦࡴࠧ༶"): bstack1l111l1l_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack11lll11ll_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack11lll11ll_opy_[bstack1l111l1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ༷")] = bstack11lll11ll_opy_[bstack1l111l1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ༸")] % json.dumps(bstack1111l111l_opy_)
        bstack1l111l1l_opy_.bstack11l111ll11_opy_(bstack11lll11ll_opy_)
        bstack1l111l1l_opy_.store()
        bstack11ll111ll1_opy_ = driver.execute_script(bstack1l111l1l_opy_.perform_scan)
      except Exception as bstack111ll1ll1l_opy_:
        logger.info(bstack1l111l1_opy_ (u"ࠧࡇࡰࡱ࡫ࡸࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤ༹ࠧ") + str(bstack111ll1ll1l_opy_))
        bstack11ll111ll1_opy_ = {bstack1l111l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ༺"): str(bstack111ll1ll1l_opy_)}
    else:
      bstack11ll111ll1_opy_ = driver.execute_async_script(bstack1l111l1l_opy_.perform_scan, {bstack1l111l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ༻"): kwargs.get(bstack1l111l1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩ༼"), None) or bstack1l111l1_opy_ (u"ࠩࠪ༽")})
    return bstack11ll111ll1_opy_
  except Exception as err:
    logger.error(bstack1l111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠢࡾࢁࠧ༾").format(str(err)))
    return {}