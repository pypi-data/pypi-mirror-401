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
import os
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11l111ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11ll_opy_ import bstack11lllll11l_opy_
class bstack1l1l11lll_opy_:
  working_dir = os.getcwd()
  bstack1l1ll1l111_opy_ = False
  config = {}
  bstack11l11111l11_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪᾞ")
  binary_path = bstack1l11l1l_opy_ (u"ࠪࠫᾟ")
  bstack1llllll11ll1_opy_ = bstack1l11l1l_opy_ (u"ࠫࠬᾠ")
  bstack1lllllll11_opy_ = False
  bstack1llllll1l1l1_opy_ = None
  bstack1llllllll11l_opy_ = {}
  bstack1lllllll11l1_opy_ = 300
  bstack111111ll111_opy_ = False
  logger = None
  bstack1llllll1ll11_opy_ = False
  bstack1l111l11l_opy_ = False
  percy_build_id = None
  bstack1111111l11l_opy_ = bstack1l11l1l_opy_ (u"ࠬ࠭ᾡ")
  bstack11111111l11_opy_ = {
    bstack1l11l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᾢ") : 1,
    bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᾣ") : 2,
    bstack1l11l1l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ᾤ") : 3,
    bstack1l11l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩᾥ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111111llll_opy_(self):
    bstack1lllllll11ll_opy_ = bstack1l11l1l_opy_ (u"ࠪࠫᾦ")
    bstack11111l111l1_opy_ = sys.platform
    bstack1111111lll1_opy_ = bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᾧ")
    if re.match(bstack1l11l1l_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧᾨ"), bstack11111l111l1_opy_) != None:
      bstack1lllllll11ll_opy_ = bstack11l11ll111l_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢᾩ")
      self.bstack1111111l11l_opy_ = bstack1l11l1l_opy_ (u"ࠧ࡮ࡣࡦࠫᾪ")
    elif re.match(bstack1l11l1l_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨᾫ"), bstack11111l111l1_opy_) != None:
      bstack1lllllll11ll_opy_ = bstack11l11ll111l_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥᾬ")
      bstack1111111lll1_opy_ = bstack1l11l1l_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨᾭ")
      self.bstack1111111l11l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡼ࡯࡮ࠨᾮ")
    else:
      bstack1lllllll11ll_opy_ = bstack11l11ll111l_opy_ + bstack1l11l1l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣᾯ")
      self.bstack1111111l11l_opy_ = bstack1l11l1l_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᾰ")
    return bstack1lllllll11ll_opy_, bstack1111111lll1_opy_
  def bstack1111111ll1l_opy_(self):
    try:
      bstack1llllll1llll_opy_ = [os.path.join(expanduser(bstack1l11l1l_opy_ (u"ࠢࡿࠤᾱ")), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᾲ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llllll1llll_opy_:
        if(self.bstack111111l1l11_opy_(path)):
          return path
      raise bstack1l11l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᾳ")
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧᾴ").format(e))
  def bstack111111l1l11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llllllll1ll_opy_(self, bstack1llllll1ll1l_opy_):
    return os.path.join(bstack1llllll1ll1l_opy_, self.bstack11l11111l11_opy_ + bstack1l11l1l_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥ᾵"))
  def bstack1llllllll1l1_opy_(self, bstack1llllll1ll1l_opy_, bstack1lllllll1lll_opy_):
    if not bstack1lllllll1lll_opy_: return
    try:
      bstack11111111111_opy_ = self.bstack1llllllll1ll_opy_(bstack1llllll1ll1l_opy_)
      with open(bstack11111111111_opy_, bstack1l11l1l_opy_ (u"ࠧࡽࠢᾶ")) as f:
        f.write(bstack1lllllll1lll_opy_)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥᾷ"))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᾸ").format(e))
  def bstack111111l11ll_opy_(self, bstack1llllll1ll1l_opy_):
    try:
      bstack11111111111_opy_ = self.bstack1llllllll1ll_opy_(bstack1llllll1ll1l_opy_)
      if os.path.exists(bstack11111111111_opy_):
        with open(bstack11111111111_opy_, bstack1l11l1l_opy_ (u"ࠣࡴࠥᾹ")) as f:
          bstack1lllllll1lll_opy_ = f.read().strip()
          return bstack1lllllll1lll_opy_ if bstack1lllllll1lll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᾺ").format(e))
  def bstack1111111l111_opy_(self, bstack1llllll1ll1l_opy_, bstack1lllllll11ll_opy_):
    bstack11111l11111_opy_ = self.bstack111111l11ll_opy_(bstack1llllll1ll1l_opy_)
    if bstack11111l11111_opy_:
      try:
        bstack1llllll1l11l_opy_ = self.bstack111111l1ll1_opy_(bstack11111l11111_opy_, bstack1lllllll11ll_opy_)
        if not bstack1llllll1l11l_opy_:
          self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧΆ"))
          return True
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥᾼ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦ᾽").format(e))
    return False
  def bstack111111l1ll1_opy_(self, bstack11111l11111_opy_, bstack1lllllll11ll_opy_):
    try:
      headers = {
        bstack1l11l1l_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨι"): bstack11111l11111_opy_
      }
      response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠧࡈࡇࡗࠫ᾿"), bstack1lllllll11ll_opy_, {}, {bstack1l11l1l_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤ῀"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦ῁").format(e))
  @measure(event_name=EVENTS.bstack11l11llll1l_opy_, stage=STAGE.bstack11l1llllll_opy_)
  def bstack1llllll11l1l_opy_(self, bstack1lllllll11ll_opy_, bstack1111111lll1_opy_):
    try:
      bstack1llllllllll1_opy_ = self.bstack1111111ll1l_opy_()
      bstack111111lll1l_opy_ = os.path.join(bstack1llllllllll1_opy_, bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ῂ"))
      bstack111111l1lll_opy_ = os.path.join(bstack1llllllllll1_opy_, bstack1111111lll1_opy_)
      if self.bstack1111111l111_opy_(bstack1llllllllll1_opy_, bstack1lllllll11ll_opy_): # if bstack1lllllll1l11_opy_, bstack1l11ll111ll_opy_ bstack1lllllll1lll_opy_ is bstack11111111l1l_opy_ to bstack111lll1l111_opy_ version available (response 304)
        if os.path.exists(bstack111111l1lll_opy_):
          self.logger.info(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨῃ").format(bstack111111l1lll_opy_))
          return bstack111111l1lll_opy_
        if os.path.exists(bstack111111lll1l_opy_):
          self.logger.info(bstack1l11l1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥῄ").format(bstack111111lll1l_opy_))
          return self.bstack11111111lll_opy_(bstack111111lll1l_opy_, bstack1111111lll1_opy_)
      self.logger.info(bstack1l11l1l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦ῅").format(bstack1lllllll11ll_opy_))
      response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠧࡈࡇࡗࠫῆ"), bstack1lllllll11ll_opy_, {}, {})
      if response.status_code == 200:
        bstack11111l111ll_opy_ = response.headers.get(bstack1l11l1l_opy_ (u"ࠣࡇࡗࡥ࡬ࠨῇ"), bstack1l11l1l_opy_ (u"ࠤࠥῈ"))
        if bstack11111l111ll_opy_:
          self.bstack1llllllll1l1_opy_(bstack1llllllllll1_opy_, bstack11111l111ll_opy_)
        with open(bstack111111lll1l_opy_, bstack1l11l1l_opy_ (u"ࠪࡻࡧ࠭Έ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11l1l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤῊ").format(bstack111111lll1l_opy_))
        return self.bstack11111111lll_opy_(bstack111111lll1l_opy_, bstack1111111lll1_opy_)
      else:
        raise(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣΉ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢῌ").format(e))
  def bstack111111l11l1_opy_(self, bstack1lllllll11ll_opy_, bstack1111111lll1_opy_):
    try:
      retry = 2
      bstack111111l1lll_opy_ = None
      bstack1llllll11lll_opy_ = False
      while retry > 0:
        bstack111111l1lll_opy_ = self.bstack1llllll11l1l_opy_(bstack1lllllll11ll_opy_, bstack1111111lll1_opy_)
        bstack1llllll11lll_opy_ = self.bstack111111l1111_opy_(bstack1lllllll11ll_opy_, bstack1111111lll1_opy_, bstack111111l1lll_opy_)
        if bstack1llllll11lll_opy_:
          break
        retry -= 1
      return bstack111111l1lll_opy_, bstack1llllll11lll_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦ῍").format(e))
    return bstack111111l1lll_opy_, False
  def bstack111111l1111_opy_(self, bstack1lllllll11ll_opy_, bstack1111111lll1_opy_, bstack111111l1lll_opy_, bstack111111l111l_opy_ = 0):
    if bstack111111l111l_opy_ > 1:
      return False
    if bstack111111l1lll_opy_ == None or os.path.exists(bstack111111l1lll_opy_) == False:
      self.logger.warn(bstack1l11l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨ῎"))
      return False
    bstack11111111ll1_opy_ = bstack1l11l1l_opy_ (u"ࡴࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫ࠣࡠࡩ࠱࡜࠯࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭ࠥ῏")
    command = bstack1l11l1l_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩῐ").format(bstack111111l1lll_opy_)
    bstack1llllll1l1ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11111111ll1_opy_, bstack1llllll1l1ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥῑ"))
      return False
  def bstack11111111lll_opy_(self, bstack111111lll1l_opy_, bstack1111111lll1_opy_):
    try:
      working_dir = os.path.dirname(bstack111111lll1l_opy_)
      shutil.unpack_archive(bstack111111lll1l_opy_, working_dir)
      bstack111111l1lll_opy_ = os.path.join(working_dir, bstack1111111lll1_opy_)
      os.chmod(bstack111111l1lll_opy_, 0o755)
      return bstack111111l1lll_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨῒ"))
  def bstack1lllllll1ll1_opy_(self):
    try:
      bstack1lllllllllll_opy_ = self.config.get(bstack1l11l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬΐ"))
      bstack1lllllll1ll1_opy_ = bstack1lllllllllll_opy_ or (bstack1lllllllllll_opy_ is None and self.bstack1l1ll1l111_opy_)
      if not bstack1lllllll1ll1_opy_ or self.config.get(bstack1l11l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ῔"), None) not in bstack11l11ll1lll_opy_:
        return False
      self.bstack1lllllll11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ῕").format(e))
  def bstack111111ll11l_opy_(self):
    try:
      bstack111111ll11l_opy_ = self.percy_capture_mode
      return bstack111111ll11l_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥῖ").format(e))
  def init(self, bstack1l1ll1l111_opy_, config, logger):
    self.bstack1l1ll1l111_opy_ = bstack1l1ll1l111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lllllll1ll1_opy_():
      return
    self.bstack1llllllll11l_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩῗ"), {})
    self.percy_capture_mode = config.get(bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧῘ"))
    try:
      bstack1lllllll11ll_opy_, bstack1111111lll1_opy_ = self.bstack1111111llll_opy_()
      self.bstack11l11111l11_opy_ = bstack1111111lll1_opy_
      bstack111111l1lll_opy_, bstack1llllll11lll_opy_ = self.bstack111111l11l1_opy_(bstack1lllllll11ll_opy_, bstack1111111lll1_opy_)
      if bstack1llllll11lll_opy_:
        self.binary_path = bstack111111l1lll_opy_
        thread = Thread(target=self.bstack111111111l1_opy_)
        thread.start()
      else:
        self.bstack1llllll1ll11_opy_ = True
        self.logger.error(bstack1l11l1l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤῙ").format(bstack111111l1lll_opy_))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢῚ").format(e))
  def bstack11111l1111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡪࠫΊ"), bstack1l11l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫ῜"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨ῝").format(logfile))
      self.bstack1llllll11ll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ῞").format(e))
  @measure(event_name=EVENTS.bstack11l1l111l11_opy_, stage=STAGE.bstack11l1llllll_opy_)
  def bstack111111111l1_opy_(self):
    bstack111111111ll_opy_ = self.bstack111111ll1ll_opy_()
    if bstack111111111ll_opy_ == None:
      self.bstack1llllll1ll11_opy_ = True
      self.logger.error(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢ῟"))
      return False
    bstack111111lllll_opy_ = [bstack1l11l1l_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨῠ") if self.bstack1l1ll1l111_opy_ else bstack1l11l1l_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪῡ")]
    bstack111l11l11l1_opy_ = self.bstack11111l11l1l_opy_()
    if bstack111l11l11l1_opy_ != None:
      bstack111111lllll_opy_.append(bstack1l11l1l_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨῢ").format(bstack111l11l11l1_opy_))
    env = os.environ.copy()
    env[bstack1l11l1l_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨΰ")] = bstack111111111ll_opy_
    env[bstack1l11l1l_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤῤ")] = os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨῥ"), bstack1l11l1l_opy_ (u"ࠫࠬῦ"))
    bstack1llllll1l111_opy_ = [self.binary_path]
    self.bstack11111l1111l_opy_()
    self.bstack1llllll1l1l1_opy_ = self.bstack1111111l1l1_opy_(bstack1llllll1l111_opy_ + bstack111111lllll_opy_, env)
    self.logger.debug(bstack1l11l1l_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨῧ"))
    bstack111111l111l_opy_ = 0
    while self.bstack1llllll1l1l1_opy_.poll() == None:
      bstack1llllllll111_opy_ = self.bstack1lllllll1l1l_opy_()
      if bstack1llllllll111_opy_:
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤῨ"))
        self.bstack111111ll111_opy_ = True
        return True
      bstack111111l111l_opy_ += 1
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥῩ").format(bstack111111l111l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨῪ").format(bstack111111l111l_opy_))
    self.bstack1llllll1ll11_opy_ = True
    return False
  def bstack1lllllll1l1l_opy_(self, bstack111111l111l_opy_ = 0):
    if bstack111111l111l_opy_ > 10:
      return False
    try:
      bstack1111111l1ll_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩΎ"), bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫῬ"))
      bstack1llllll11l11_opy_ = bstack1111111l1ll_opy_ + bstack11l1l1l1l11_opy_
      response = requests.get(bstack1llllll11l11_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪ῭"), {}).get(bstack1l11l1l_opy_ (u"ࠬ࡯ࡤࠨ΅"), None)
      return True
    except:
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ`"))
      return False
  def bstack111111ll1ll_opy_(self):
    bstack1lllllll1111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࠫ῰") if self.bstack1l1ll1l111_opy_ else bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ῱")
    bstack1111111ll11_opy_ = bstack1l11l1l_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧῲ") if self.config.get(bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩῳ")) is None else True
    bstack11l1ll1ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁࠧῴ").format(self.config[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ῵")], bstack1lllllll1111_opy_, bstack1111111ll11_opy_)
    if self.percy_capture_mode:
      bstack11l1ll1ll1l_opy_ += bstack1l11l1l_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽࠣῶ").format(self.percy_capture_mode)
    uri = bstack11lllll11l_opy_(bstack11l1ll1ll1l_opy_)
    try:
      response = bstack11l111ll11_opy_(bstack1l11l1l_opy_ (u"ࠧࡈࡇࡗࠫῷ"), uri, {}, {bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭Ὸ"): (self.config[bstack1l11l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫΌ")], self.config[bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭Ὼ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lllllll11_opy_ = data.get(bstack1l11l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬΏ"))
        self.percy_capture_mode = data.get(bstack1l11l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪῼ"))
        os.environ[bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫ´")] = str(self.bstack1lllllll11_opy_)
        os.environ[bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ῾")] = str(self.percy_capture_mode)
        if bstack1111111ll11_opy_ == bstack1l11l1l_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ῿") and str(self.bstack1lllllll11_opy_).lower() == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ "):
          self.bstack1l111l11l_opy_ = True
        if bstack1l11l1l_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ ") in data:
          return data[bstack1l11l1l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ ")]
        else:
          raise bstack1l11l1l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬ ").format(data)
      else:
        raise bstack1l11l1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣ ").format(e))
  def bstack11111l11l1l_opy_(self):
    bstack111111lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦ "))
    try:
      if bstack1l11l1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ ") not in self.bstack1llllllll11l_opy_:
        self.bstack1llllllll11l_opy_[bstack1l11l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ ")] = 2
      with open(bstack111111lll11_opy_, bstack1l11l1l_opy_ (u"ࠫࡼ࠭ ")) as fp:
        json.dump(self.bstack1llllllll11l_opy_, fp)
      return bstack111111lll11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ ").format(e))
  def bstack1111111l1l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111111l11l_opy_ == bstack1l11l1l_opy_ (u"࠭ࡷࡪࡰࠪ​"):
        bstack111111l1l1l_opy_ = [bstack1l11l1l_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ‌"), bstack1l11l1l_opy_ (u"ࠨ࠱ࡦࠫ‍")]
        cmd = bstack111111l1l1l_opy_ + cmd
      cmd = bstack1l11l1l_opy_ (u"ࠩࠣࠫ‎").join(cmd)
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢ‏").format(cmd))
      with open(self.bstack1llllll11ll1_opy_, bstack1l11l1l_opy_ (u"ࠦࡦࠨ‐")) as bstack1llllll1lll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llllll1lll1_opy_, text=True, stderr=bstack1llllll1lll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llllll1ll11_opy_ = True
      self.logger.error(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ‑").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111111ll111_opy_:
        self.logger.info(bstack1l11l1l_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢ‒"))
        cmd = [self.binary_path, bstack1l11l1l_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥ–")]
        self.bstack1111111l1l1_opy_(cmd)
        self.bstack111111ll111_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ—").format(cmd, e))
  def bstack1ll11l1l1l_opy_(self):
    if not self.bstack1lllllll11_opy_:
      return
    try:
      bstack1111111111l_opy_ = 0
      while not self.bstack111111ll111_opy_ and bstack1111111111l_opy_ < self.bstack1lllllll11l1_opy_:
        if self.bstack1llllll1ll11_opy_:
          self.logger.info(bstack1l11l1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢ―"))
          return
        time.sleep(1)
        bstack1111111111l_opy_ += 1
      os.environ[bstack1l11l1l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩ‖")] = str(self.bstack11111l11l11_opy_())
      self.logger.info(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧ‗"))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ‘").format(e))
  def bstack11111l11l11_opy_(self):
    if self.bstack1l1ll1l111_opy_:
      return
    try:
      bstack1lllllll111l_opy_ = [platform[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ’")].lower() for platform in self.config.get(bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ‚"), [])]
      bstack1lllllllll11_opy_ = sys.maxsize
      bstack111111ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩ‛")
      for browser in bstack1lllllll111l_opy_:
        if browser in self.bstack11111111l11_opy_:
          bstack11111l11ll1_opy_ = self.bstack11111111l11_opy_[browser]
        if bstack11111l11ll1_opy_ < bstack1lllllllll11_opy_:
          bstack1lllllllll11_opy_ = bstack11111l11ll1_opy_
          bstack111111ll1l1_opy_ = browser
      return bstack111111ll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ“").format(e))
  @classmethod
  def bstack111ll11ll_opy_(self):
    return os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ”"), bstack1l11l1l_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪ„")).lower()
  @classmethod
  def bstack1ll111l1l_opy_(self):
    return os.getenv(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ‟"), bstack1l11l1l_opy_ (u"࠭ࠧ†"))
  @classmethod
  def bstack1l11llll1l1_opy_(cls, value):
    cls.bstack1l111l11l_opy_ = value
  @classmethod
  def bstack1lllllllll1l_opy_(cls):
    return cls.bstack1l111l11l_opy_
  @classmethod
  def bstack1l11llll11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111111llll1_opy_(cls):
    return cls.percy_build_id