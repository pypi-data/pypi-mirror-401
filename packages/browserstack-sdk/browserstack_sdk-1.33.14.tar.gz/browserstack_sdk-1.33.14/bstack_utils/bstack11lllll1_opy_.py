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
from bstack_utils.constants import bstack11l1l1l1ll1_opy_, bstack11l1l11lll1_opy_, bstack11l11ll11l1_opy_
import tempfile
import json
bstack111l111l111_opy_ = os.getenv(bstack1l11l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡇࡠࡈࡌࡐࡊࠨṦ"), None) or os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠣṧ"))
bstack111l1111l11_opy_ = os.path.join(bstack1l11l1l_opy_ (u"ࠢ࡭ࡱࡪࠦṨ"), bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯࠲ࡩ࡬ࡪ࠯ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠬṩ"))
_1111lll1lll_opy_ = threading.Lock()
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l11l1l_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬṪ"),
      datefmt=bstack1l11l1l_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨṫ"),
      stream=sys.stdout
    )
  return logger
def bstack1l11llllll_opy_(name=__name__, level=logging.DEBUG):
  bstack1l11l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡥࠥࡲ࡯ࡨࡩࡨࡶࠥࡺࡨࡢࡶࠣࡻࡷ࡯ࡴࡦࡵࠣࡳࡳࡲࡹࠡࡶࡲࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯࡮ࡲ࡫ࠥ࡬ࡩ࡭ࡧࠍࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡ࡯ࡦࠣࡱࡦࡴࡡࡨࡧࡶࠤ࡮ࡺࡳࠡࡱࡺࡲࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠠࡩࡣࡱࡨࡱ࡫ࡲࠋࠢࠣࡓࡳࡲࡹࠡࡧࡱࡥࡧࡲࡥࡴࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣ࡭࡫ࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࡡࡏࡓࡌ࡙ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠠࡪࡵࠣࡷࡪࡺࠠࡵࡱࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࡱࡥࡲ࡫࠺ࠡࡎࡲ࡫࡬࡫ࡲࠡࡰࡤࡱࡪࠦࠨࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࡥ࡟࡯ࡣࡰࡩࡤࡥࠩࠋࠢࠣࠤࠥࡲࡥࡷࡧ࡯࠾ࠥࡒ࡯ࡨࡩ࡬ࡲ࡬ࠦ࡬ࡦࡸࡨࡰࠥ࠮ࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡉࡋࡂࡖࡉࠬࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࡲ࡯ࡨࡩ࡬ࡲ࡬࠴ࡌࡰࡩࡪࡩࡷࡀࠠࡄࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡱࡵࡧࡨࡧࡵࠤࡹ࡮ࡡࡵࠢࡺࡶ࡮ࡺࡥࡴࠢࡲࡲࡱࡿࠠࡵࡱࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮࡭ࡱࡪࠤ࠭࡯ࡦࠡࡧࡱࡥࡧࡲࡥࡥࠫࠍࠤࠥࠨࠢࠣṬ")
  logger_name = bstack1l11l1l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡾ࠴ࢂࠨṭ").format(name)
  logger = logging.getLogger(logger_name)
  is_enabled = os.getenv(bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࡡࡏࡓࡌ࡙ࠧṮ"), bstack1l11l1l_opy_ (u"ࠧࠨṯ")).lower() == bstack1l11l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ṱ")
  if not is_enabled:
    logger.setLevel(logging.CRITICAL)
    logger.propagate = False
    return logger
  with _1111lll1lll_opy_:
    if logger.handlers:
      return logger
    bstack111l111l1ll_opy_ = os.path.join(os.getcwd(), bstack1l11l1l_opy_ (u"ࠩ࡯ࡳ࡬࠭ṱ"), bstack1l11l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮࡭ࡱࡪࠫṲ"))
    log_dir = os.path.dirname(bstack111l111l1ll_opy_)
    if not os.path.exists(log_dir):
      os.makedirs(log_dir)
    bstack1111lllll1l_opy_ = logging.FileHandler(bstack111l111l1ll_opy_)
    bstack111l11l1111_opy_ = logging.Formatter(
      fmt=bstack1l11l1l_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢ࡞ࠤࡘࡊࡋ࠮ࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠥࡣࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬṳ"),
      datefmt=bstack1l11l1l_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪṴ"),
    )
    bstack1111lllll1l_opy_.setFormatter(bstack111l11l1111_opy_)
    bstack1111lllll1l_opy_.setLevel(level)
    bstack1111lllll1l_opy_.addFilter(lambda r: r.name != bstack1l11l1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨṵ"))
    logger.addHandler(bstack1111lllll1l_opy_)
    logger.setLevel(level)
    logger.propagate = False
  return logger
def bstack1lll1ll11ll_opy_():
  bstack111l1111lll_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧṶ"), bstack1l11l1l_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢṷ"))
  return logging.DEBUG if bstack111l1111lll_opy_.lower() == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢṸ") else logging.INFO
def bstack1l1l11l1l11_opy_():
  global bstack111l111l111_opy_
  if os.path.exists(bstack111l111l111_opy_):
    os.remove(bstack111l111l111_opy_)
  if os.path.exists(bstack111l1111l11_opy_):
    os.remove(bstack111l1111l11_opy_)
def bstack1l111l1l1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l111ll11_opy_ = log_level
  if bstack1l11l1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬṹ") in config and config[bstack1l11l1l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭Ṻ")] in bstack11l1l11lll1_opy_:
    bstack111l111ll11_opy_ = bstack11l1l11lll1_opy_[config[bstack1l11l1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧṻ")]]
  if config.get(bstack1l11l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨṼ"), False):
    logging.getLogger().setLevel(bstack111l111ll11_opy_)
    return bstack111l111ll11_opy_
  global bstack111l111l111_opy_
  bstack1l111l1l1l_opy_()
  bstack1111llllll1_opy_ = logging.Formatter(
    fmt=bstack1l11l1l_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪṽ"),
    datefmt=bstack1l11l1l_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭Ṿ"),
  )
  bstack1111llll11l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l111l111_opy_)
  file_handler.setFormatter(bstack1111llllll1_opy_)
  bstack1111llll11l_opy_.setFormatter(bstack1111llllll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111llll11l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l11l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫṿ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111llll11l_opy_.setLevel(bstack111l111ll11_opy_)
  logging.getLogger().addHandler(bstack1111llll11l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l111ll11_opy_
def bstack111l111llll_opy_(config):
  try:
    bstack111l11111l1_opy_ = set(bstack11l11ll11l1_opy_)
    bstack1111llll111_opy_ = bstack1l11l1l_opy_ (u"ࠪࠫẀ")
    with open(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧẁ")) as bstack1111lllll11_opy_:
      bstack111l1111111_opy_ = bstack1111lllll11_opy_.read()
      bstack1111llll111_opy_ = re.sub(bstack1l11l1l_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭Ẃ"), bstack1l11l1l_opy_ (u"࠭ࠧẃ"), bstack111l1111111_opy_, flags=re.M)
      bstack1111llll111_opy_ = re.sub(
        bstack1l11l1l_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪẄ") + bstack1l11l1l_opy_ (u"ࠨࡾࠪẅ").join(bstack111l11111l1_opy_) + bstack1l11l1l_opy_ (u"ࠩࠬ࠲࠯ࠪࠧẆ"),
        bstack1l11l1l_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬẇ"),
        bstack1111llll111_opy_, flags=re.M | re.I
      )
    def bstack111l1111l1l_opy_(dic):
      bstack1111llll1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l11111l1_opy_:
          bstack1111llll1l1_opy_[key] = bstack1l11l1l_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨẈ")
        else:
          if isinstance(value, dict):
            bstack1111llll1l1_opy_[key] = bstack111l1111l1l_opy_(value)
          else:
            bstack1111llll1l1_opy_[key] = value
      return bstack1111llll1l1_opy_
    bstack1111llll1l1_opy_ = bstack111l1111l1l_opy_(config)
    return {
      bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨẉ"): bstack1111llll111_opy_,
      bstack1l11l1l_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩẊ"): json.dumps(bstack1111llll1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1111llll1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡪࠫẋ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l11l11l1_opy_ = os.path.join(log_dir, bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩẌ"))
  if not os.path.exists(bstack111l11l11l1_opy_):
    bstack111l11l111l_opy_ = {
      bstack1l11l1l_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥẍ"): str(inipath),
      bstack1l11l1l_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧẎ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪẏ")), bstack1l11l1l_opy_ (u"ࠬࡽࠧẐ")) as bstack111l111l11l_opy_:
      bstack111l111l11l_opy_.write(json.dumps(bstack111l11l111l_opy_))
def bstack111l111l1l1_opy_():
  try:
    bstack111l11l11l1_opy_ = os.path.join(os.getcwd(), bstack1l11l1l_opy_ (u"࠭࡬ࡰࡩࠪẑ"), bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭Ẓ"))
    if os.path.exists(bstack111l11l11l1_opy_):
      with open(bstack111l11l11l1_opy_, bstack1l11l1l_opy_ (u"ࠨࡴࠪẓ")) as bstack111l111l11l_opy_:
        bstack111l111lll1_opy_ = json.load(bstack111l111l11l_opy_)
      return bstack111l111lll1_opy_.get(bstack1l11l1l_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪẔ"), bstack1l11l1l_opy_ (u"ࠪࠫẕ")), bstack111l111lll1_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭ẖ"), bstack1l11l1l_opy_ (u"ࠬ࠭ẗ"))
  except:
    pass
  return None, None
def bstack111l1111ll1_opy_():
  try:
    bstack111l11l11l1_opy_ = os.path.join(os.getcwd(), bstack1l11l1l_opy_ (u"࠭࡬ࡰࡩࠪẘ"), bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ẙ"))
    if os.path.exists(bstack111l11l11l1_opy_):
      os.remove(bstack111l11l11l1_opy_)
  except:
    pass
def bstack1l1111l11_opy_(config):
  try:
    from bstack_utils.helper import bstack11llllll_opy_, bstack11l11l1l1l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l111l111_opy_
    if config.get(bstack1l11l1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪẚ"), False):
      return
    uuid = os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧẛ")) if os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨẜ")) else bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨẝ"))
    if not uuid or uuid == bstack1l11l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪẞ"):
      return
    bstack111l111ll1l_opy_ = [bstack1l11l1l_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩẟ"), bstack1l11l1l_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨẠ"), bstack1l11l1l_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩạ"), bstack111l111l111_opy_, bstack111l1111l11_opy_]
    bstack111l111111l_opy_, root_path = bstack111l111l1l1_opy_()
    if bstack111l111111l_opy_ != None:
      bstack111l111ll1l_opy_.append(bstack111l111111l_opy_)
    if root_path != None:
      bstack111l111ll1l_opy_.append(os.path.join(root_path, bstack1l11l1l_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧẢ")))
    bstack1l111l1l1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩả") + uuid + bstack1l11l1l_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬẤ"))
    with tarfile.open(output_file, bstack1l11l1l_opy_ (u"ࠧࡽ࠺ࡨࡼࠥấ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l111ll1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l111llll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111lllllll_opy_ = data.encode()
        tarinfo.size = len(bstack1111lllllll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111lllllll_opy_))
    bstack1111l1l1_opy_ = MultipartEncoder(
      fields= {
        bstack1l11l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫẦ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l11l1l_opy_ (u"ࠧࡳࡤࠪầ")), bstack1l11l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭Ẩ")),
        bstack1l11l1l_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫẩ"): uuid
      }
    )
    bstack111l11111ll_opy_ = bstack11l11l1l1l_opy_(cli.config, [bstack1l11l1l_opy_ (u"ࠥࡥࡵ࡯ࡳࠣẪ"), bstack1l11l1l_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦẫ"), bstack1l11l1l_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࠧẬ")], bstack11l1l1l1ll1_opy_)
    response = requests.post(
      bstack1l11l1l_opy_ (u"ࠨࡻࡾ࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢậ").format(bstack111l11111ll_opy_),
      data=bstack1111l1l1_opy_,
      headers={bstack1l11l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭Ắ"): bstack1111l1l1_opy_.content_type},
      auth=(config[bstack1l11l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪắ")], config[bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬẰ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l11l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩằ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l11l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪẲ") + str(e))
  finally:
    try:
      bstack1l1l11l1l11_opy_()
      bstack111l1111ll1_opy_()
    except:
      pass