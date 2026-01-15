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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
import threading
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l11l1l111_opy_, bstack11l11ll11l1_opy_, bstack11l1l111lll_opy_
import tempfile
import json
bstack1111lllll11_opy_ = os.getenv(bstack1l111l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦẇ"), None) or os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨẈ"))
bstack1111llll1l1_opy_ = os.path.join(bstack1l111l1_opy_ (u"ࠧࡲ࡯ࡨࠤẉ"), bstack1l111l1_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪẊ"))
_1111lll11ll_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l111l1_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪẋ"),
      datefmt=bstack1l111l1_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭Ẍ"),
      stream=sys.stdout
    )
  return logger
def bstack1l11llll1l_opy_(name=__name__, level=logging.DEBUG):
  bstack1l111l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡰࡴ࡭ࡧࡦࡴࠣࡸ࡭ࡧࡴࠡࡹࡵ࡭ࡹ࡫ࡳࠡࡱࡱࡰࡾࠦࡴࡰࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴࡬ࡰࡩࠣࡪ࡮ࡲࡥࠋࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࡴࡤࠡ࡯ࡤࡲࡦ࡭ࡥࡴࠢ࡬ࡸࡸࠦ࡯ࡸࡰࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠐࠠࠡࡑࡱࡰࡾࠦࡥ࡯ࡣࡥࡰࡪࡹࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡ࡫ࡩࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔ࡟ࡍࡑࡊࡗࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠥ࡯ࡳࠡࡵࡨࡸࠥࡺ࡯ࠡࡣࠣࡸࡷࡻࡴࡩࡻࠣࡺࡦࡲࡵࡦࠌࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠ࡯ࡣࡰࡩ࠿ࠦࡌࡰࡩࡪࡩࡷࠦ࡮ࡢ࡯ࡨࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣࡣࡤࡴࡡ࡮ࡧࡢࡣ࠮ࠐࠠࠡࠢࠣࡰࡪࡼࡥ࡭࠼ࠣࡐࡴ࡭ࡧࡪࡰࡪࠤࡱ࡫ࡶࡦ࡮ࠣࠬࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࡇࡉࡇ࡛ࡇࠪࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࡰࡴ࡭ࡧࡪࡰࡪ࠲ࡑࡵࡧࡨࡧࡵ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢ࡯ࡳ࡬࡭ࡥࡳࠢࡷ࡬ࡦࡺࠠࡸࡴ࡬ࡸࡪࡹࠠࡰࡰ࡯ࡽࠥࡺ࡯ࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠢࠫ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠩࠋࠢࠣࠦࠧࠨẍ")
  logger_name = bstack1l111l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡼ࠲ࢀࠦẎ").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔ࡟ࡍࡑࡊࡗࠬẏ"), bstack1l111l1_opy_ (u"ࠬ࠭Ẑ")).lower() == bstack1l111l1_opy_ (u"࠭ࡴࡳࡷࡨࠫẑ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1111lll11ll_opy_:
    if logger.handlers:
      return logger
    bstack1111ll1ll1l_opy_ = os.path.join(os.getcwd(), bstack1l111l1_opy_ (u"ࠧ࡭ࡱࡪࠫẒ"), bstack1l111l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡲ࡯ࡨࠩẓ"))
    log_dir = os.path.dirname(bstack1111ll1ll1l_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111lll1lll_opy_ = logging.FileHandler(bstack1111ll1ll1l_opy_)
    bstack1111lllll1l_opy_ = logging.Formatter(
      fmt=bstack1l111l1_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠ࡜ࠢࡖࡈࡐ࠳ࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠣࡡࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪẔ"),
      datefmt=bstack1l111l1_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨẕ"),
    )
    bstack1111lll1lll_opy_.setFormatter(bstack1111lllll1l_opy_)
    bstack1111lll1lll_opy_.setLevel(level)
    bstack1111lll1lll_opy_.addFilter(lambda r: r.name != bstack1l111l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ẖ"))
    logger.addHandler(bstack1111lll1lll_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1ll1ll11l1l_opy_():
  bstack111l11111ll_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡉࡋࡂࡖࡉࠥẗ"), bstack1l111l1_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧẘ"))
  return logging.DEBUG if bstack111l11111ll_opy_.lower() == bstack1l111l1_opy_ (u"ࠢࡵࡴࡸࡩࠧẙ") else logging.INFO
def bstack1l1l1ll1l1l_opy_():
  global bstack1111lllll11_opy_
  if os.path.exists(bstack1111lllll11_opy_):
    os.remove(bstack1111lllll11_opy_)
  if os.path.exists(bstack1111llll1l1_opy_):
    os.remove(bstack1111llll1l1_opy_)
def bstack1lll111l11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack1111lll11l1_opy_ = log_level
  if bstack1l111l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪẚ") in config and config[bstack1l111l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫẛ")] in bstack11l11ll11l1_opy_:
    bstack1111lll11l1_opy_ = bstack11l11ll11l1_opy_[config[bstack1l111l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬẜ")]]
  if config.get(bstack1l111l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ẝ"), False):
    logging.getLogger().setLevel(bstack1111lll11l1_opy_)
    return bstack1111lll11l1_opy_
  global bstack1111lllll11_opy_
  bstack1lll111l11_opy_()
  bstack111l1111lll_opy_ = logging.Formatter(
    fmt=bstack1l111l1_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨẞ"),
    datefmt=bstack1l111l1_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫẟ"),
  )
  bstack1111lllllll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111lllll11_opy_)
  file_handler.setFormatter(bstack111l1111lll_opy_)
  bstack1111lllllll_opy_.setFormatter(bstack111l1111lll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111lllllll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l111l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩẠ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111lllllll_opy_.setLevel(bstack1111lll11l1_opy_)
  logging.getLogger().addHandler(bstack1111lllllll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111lll11l1_opy_
def bstack111l111111l_opy_(config):
  try:
    bstack1111ll1lll1_opy_ = set(bstack11l1l111lll_opy_)
    bstack111l111l111_opy_ = bstack1l111l1_opy_ (u"ࠨࠩạ")
    with open(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬẢ")) as bstack1111llllll1_opy_:
      bstack1111llll1ll_opy_ = bstack1111llllll1_opy_.read()
      bstack111l111l111_opy_ = re.sub(bstack1l111l1_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫả"), bstack1l111l1_opy_ (u"ࠫࠬẤ"), bstack1111llll1ll_opy_, flags=re.M)
      bstack111l111l111_opy_ = re.sub(
        bstack1l111l1_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨấ") + bstack1l111l1_opy_ (u"࠭ࡼࠨẦ").join(bstack1111ll1lll1_opy_) + bstack1l111l1_opy_ (u"ࠧࠪ࠰࠭ࠨࠬầ"),
        bstack1l111l1_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪẨ"),
        bstack111l111l111_opy_, flags=re.M | re.I
      )
    def bstack111l1111ll1_opy_(dic):
      bstack1111lll1l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111ll1lll1_opy_:
          bstack1111lll1l1l_opy_[key] = bstack1l111l1_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ẩ")
        else:
          if isinstance(value, dict):
            bstack1111lll1l1l_opy_[key] = bstack111l1111ll1_opy_(value)
          else:
            bstack1111lll1l1l_opy_[key] = value
      return bstack1111lll1l1l_opy_
    bstack1111lll1l1l_opy_ = bstack111l1111ll1_opy_(config)
    return {
      bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭Ẫ"): bstack111l111l111_opy_,
      bstack1l111l1_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧẫ"): json.dumps(bstack1111lll1l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack1111llll11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l111l1_opy_ (u"ࠬࡲ࡯ࡨࠩẬ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1111lll1111_opy_ = os.path.join(log_dir, bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹࠧậ"))
  if not os.path.exists(bstack1111lll1111_opy_):
    bstack1111lll1l11_opy_ = {
      bstack1l111l1_opy_ (u"ࠢࡪࡰ࡬ࡴࡦࡺࡨࠣẮ"): str(inipath),
      bstack1l111l1_opy_ (u"ࠣࡴࡲࡳࡹࡶࡡࡵࡪࠥắ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨẰ")), bstack1l111l1_opy_ (u"ࠪࡻࠬằ")) as bstack1111ll1llll_opy_:
      bstack1111ll1llll_opy_.write(json.dumps(bstack1111lll1l11_opy_))
def bstack111l11111l1_opy_():
  try:
    bstack1111lll1111_opy_ = os.path.join(os.getcwd(), bstack1l111l1_opy_ (u"ࠫࡱࡵࡧࠨẲ"), bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫẳ"))
    if os.path.exists(bstack1111lll1111_opy_):
      with open(bstack1111lll1111_opy_, bstack1l111l1_opy_ (u"࠭ࡲࠨẴ")) as bstack1111ll1llll_opy_:
        bstack111l1111111_opy_ = json.load(bstack1111ll1llll_opy_)
      return bstack111l1111111_opy_.get(bstack1l111l1_opy_ (u"ࠧࡪࡰ࡬ࡴࡦࡺࡨࠨẵ"), bstack1l111l1_opy_ (u"ࠨࠩẶ")), bstack111l1111111_opy_.get(bstack1l111l1_opy_ (u"ࠩࡵࡳࡴࡺࡰࡢࡶ࡫ࠫặ"), bstack1l111l1_opy_ (u"ࠪࠫẸ"))
  except:
    pass
  return None, None
def bstack111l1111l1l_opy_():
  try:
    bstack1111lll1111_opy_ = os.path.join(os.getcwd(), bstack1l111l1_opy_ (u"ࠫࡱࡵࡧࠨẹ"), bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫẺ"))
    if os.path.exists(bstack1111lll1111_opy_):
      os.remove(bstack1111lll1111_opy_)
  except:
    pass
def bstack11l1l111_opy_(config):
  try:
    from bstack_utils.helper import bstack1l1l1111_opy_, bstack1llll1l1ll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111lllll11_opy_
    if config.get(bstack1l111l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨẻ"), False):
      return
    uuid = os.getenv(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬẼ")) if os.getenv(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ẽ")) else bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦẾ"))
    if not uuid or uuid == bstack1l111l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨế"):
      return
    bstack1111lll1ll1_opy_ = [bstack1l111l1_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧỀ"), bstack1l111l1_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭ề"), bstack1l111l1_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧỂ"), bstack1111lllll11_opy_, bstack1111llll1l1_opy_]
    bstack111l1111l11_opy_, root_path = bstack111l11111l1_opy_()
    if bstack111l1111l11_opy_ != None:
      bstack1111lll1ll1_opy_.append(bstack111l1111l11_opy_)
    if root_path != None:
      bstack1111lll1ll1_opy_.append(os.path.join(root_path, bstack1l111l1_opy_ (u"ࠧࡤࡱࡱࡪࡹ࡫ࡳࡵ࠰ࡳࡽࠬể")))
    bstack1lll111l11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧỄ") + uuid + bstack1l111l1_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪễ"))
    with tarfile.open(output_file, bstack1l111l1_opy_ (u"ࠥࡻ࠿࡭ࡺࠣỆ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111lll1ll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l111111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111lll111l_opy_ = data.encode()
        tarinfo.size = len(bstack1111lll111l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111lll111l_opy_))
    bstack1ll1llllll_opy_ = MultipartEncoder(
      fields= {
        bstack1l111l1_opy_ (u"ࠫࡩࡧࡴࡢࠩệ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l111l1_opy_ (u"ࠬࡸࡢࠨỈ")), bstack1l111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫỉ")),
        bstack1l111l1_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩỊ"): uuid
      }
    )
    bstack1111llll111_opy_ = bstack1llll1l1ll_opy_(cli.config, [bstack1l111l1_opy_ (u"ࠣࡣࡳ࡭ࡸࠨị"), bstack1l111l1_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤỌ"), bstack1l111l1_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥọ")], bstack11l11l1l111_opy_)
    response = requests.post(
      bstack1l111l1_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧỎ").format(bstack1111llll111_opy_),
      data=bstack1ll1llllll_opy_,
      headers={bstack1l111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫỏ"): bstack1ll1llllll_opy_.content_type},
      auth=(config[bstack1l111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨỐ")], config[bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪố")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧỒ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l111l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨồ") + str(e))
  finally:
    try:
      bstack1l1l1ll1l1l_opy_()
      bstack111l1111l1l_opy_()
    except:
      pass