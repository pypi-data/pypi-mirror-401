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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1l1l1l_opy_, bstack11lllllll1_opy_, bstack1l11lll111_opy_,
                                    bstack11l1l111111_opy_, bstack11l1l111l1l_opy_, bstack11l1l111lll_opy_, bstack11l11l1l1l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l111l_opy_, bstack11l1lll111_opy_
from bstack_utils.proxy import bstack111lll1l1l_opy_, bstack11ll11l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll1lll11_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack11ll11ll1_opy_
from browserstack_sdk._version import __version__
bstack1l1l1111_opy_ = Config.bstack1llll1ll11_opy_()
logger = bstack1ll1lll11_opy_.get_logger(__name__, bstack1ll1lll11_opy_.bstack1ll1ll11l1l_opy_())
bstack1l1111ll1_opy_ = bstack1ll1lll11_opy_.bstack1l11llll1l_opy_(__name__)
def bstack11l1ll1llll_opy_(config):
    return config[bstack1l111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᯕ")]
def bstack11l1llll1l1_opy_(config):
    return config[bstack1l111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᯖ")]
def bstack1l11l1l1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111l1l11l1l_opy_(obj):
    values = []
    bstack111l11ll1ll_opy_ = re.compile(bstack1l111l1_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧᯗ"), re.I)
    for key in obj.keys():
        if bstack111l11ll1ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1ll1ll1_opy_(config):
    tags = []
    tags.extend(bstack111l1l11l1l_opy_(os.environ))
    tags.extend(bstack111l1l11l1l_opy_(config))
    return tags
def bstack111ll11111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l111111ll_opy_(bstack111l1l111ll_opy_):
    if not bstack111l1l111ll_opy_:
        return bstack1l111l1_opy_ (u"ࠩࠪᯘ")
    return bstack1l111l1_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦᯙ").format(bstack111l1l111ll_opy_.name, bstack111l1l111ll_opy_.email)
def bstack11ll11111ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l11lll1l_opy_ = repo.common_dir
        info = {
            bstack1l111l1_opy_ (u"ࠦࡸ࡮ࡡࠣᯚ"): repo.head.commit.hexsha,
            bstack1l111l1_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣᯛ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l111l1_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨᯜ"): repo.active_branch.name,
            bstack1l111l1_opy_ (u"ࠢࡵࡣࡪࠦᯝ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l111l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦᯞ"): bstack11l111111ll_opy_(repo.head.commit.committer),
            bstack1l111l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥᯟ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l111l1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥᯠ"): bstack11l111111ll_opy_(repo.head.commit.author),
            bstack1l111l1_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤᯡ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l111l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᯢ"): repo.head.commit.message,
            bstack1l111l1_opy_ (u"ࠨࡲࡰࡱࡷࠦᯣ"): repo.git.rev_parse(bstack1l111l1_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤᯤ")),
            bstack1l111l1_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᯥ"): bstack111l11lll1l_opy_,
            bstack1l111l1_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶ᯦ࠧ"): subprocess.check_output([bstack1l111l1_opy_ (u"ࠥ࡫࡮ࡺࠢᯧ"), bstack1l111l1_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢᯨ"), bstack1l111l1_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣᯩ")]).strip().decode(
                bstack1l111l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᯪ")),
            bstack1l111l1_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤᯫ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l111l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᯬ"): repo.git.rev_list(
                bstack1l111l1_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤᯭ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l1l1ll1l_opy_ = []
        for remote in remotes:
            bstack111ll1111ll_opy_ = {
                bstack1l111l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᯮ"): remote.name,
                bstack1l111l1_opy_ (u"ࠦࡺࡸ࡬ࠣᯯ"): remote.url,
            }
            bstack111l1l1ll1l_opy_.append(bstack111ll1111ll_opy_)
        bstack111ll11llll_opy_ = {
            bstack1l111l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯰ"): bstack1l111l1_opy_ (u"ࠨࡧࡪࡶࠥᯱ"),
            **info,
            bstack1l111l1_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳ᯲ࠣ"): bstack111l1l1ll1l_opy_
        }
        bstack111ll11llll_opy_ = bstack111lll1llll_opy_(bstack111ll11llll_opy_)
        return bstack111ll11llll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l111l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀ᯳ࠦ").format(err))
        return {}
def bstack111ll1111l1_opy_(bstack111lll1l1l1_opy_=None):
    bstack1l111l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡊࡩࡹࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡹࡰࡦࡥ࡬ࡪ࡮ࡩࡡ࡭࡮ࡼࠤ࡫ࡵࡲ࡮ࡣࡷࡸࡪࡪࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡹࡸ࡫ࠠࡤࡣࡶࡩࡸࠦࡦࡰࡴࠣࡩࡦࡩࡨࠡࡨࡲࡰࡩ࡫ࡲࠡ࡫ࡱࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥ࠮࡬ࡪࡵࡷ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡒࡴࡴࡥ࠻ࠢࡐࡳࡳࡵ࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠬࠡࡷࡶࡩࡸࠦࡣࡶࡴࡵࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡟ࡴࡹ࠮ࡨࡧࡷࡧࡼࡪࠨࠪ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡶࡴࡺࠢ࡯࡭ࡸࡺࠠ࡜࡟࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡰࡲࠤࡸࡵࡵࡳࡥࡨࡷࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥ࠮ࠣࡶࡪࡺࡵࡳࡰࡶࠤࡠࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡲࡤࡸ࡭ࡹ࠺ࠡࡏࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥࡹࡰࡦࡥ࡬ࡪ࡮ࡩࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࡶࡲࠤࡦࡴࡡ࡭ࡻࡽࡩࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡲࡩࡴࡶ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡪࡩࡤࡶࡶ࠰ࠥ࡫ࡡࡤࡪࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡥࠥ࡬࡯࡭ࡦࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᯴")
    if bstack111lll1l1l1_opy_ is None:
        bstack111lll1l1l1_opy_ = [os.getcwd()]
    elif isinstance(bstack111lll1l1l1_opy_, list) and len(bstack111lll1l1l1_opy_) == 0:
        return []
    results = []
    for folder in bstack111lll1l1l1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l111l1_opy_ (u"ࠥࡊࡴࡲࡤࡦࡴࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣ᯵").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l111l1_opy_ (u"ࠦࡵࡸࡉࡥࠤ᯶"): bstack1l111l1_opy_ (u"ࠧࠨ᯷"),
                bstack1l111l1_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧ᯸"): [],
                bstack1l111l1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣ᯹"): [],
                bstack1l111l1_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣ᯺"): bstack1l111l1_opy_ (u"ࠤࠥ᯻"),
                bstack1l111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦ᯼"): [],
                bstack1l111l1_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧ᯽"): bstack1l111l1_opy_ (u"ࠧࠨ᯾"),
                bstack1l111l1_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨ᯿"): bstack1l111l1_opy_ (u"ࠢࠣᰀ"),
                bstack1l111l1_opy_ (u"ࠣࡲࡵࡖࡦࡽࡄࡪࡨࡩࠦᰁ"): bstack1l111l1_opy_ (u"ࠤࠥᰂ")
            }
            bstack11l11111l1l_opy_ = repo.active_branch.name
            bstack111l1l111l1_opy_ = repo.head.commit
            result[bstack1l111l1_opy_ (u"ࠥࡴࡷࡏࡤࠣᰃ")] = bstack111l1l111l1_opy_.hexsha
            bstack111ll11l111_opy_ = _11l11111ll1_opy_(repo)
            logger.debug(bstack1l111l1_opy_ (u"ࠦࡇࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠽ࠤࠧᰄ") + str(bstack111ll11l111_opy_) + bstack1l111l1_opy_ (u"ࠧࠨᰅ"))
            if bstack111ll11l111_opy_:
                try:
                    bstack111ll1lllll_opy_ = repo.git.diff(bstack1l111l1_opy_ (u"ࠨ࠭࠮ࡰࡤࡱࡪ࠳࡯࡯࡮ࡼࠦᰆ"), bstack1ll1ll1111l_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᰇ")).split(bstack1l111l1_opy_ (u"ࠨ࡞ࡱࠫᰈ"))
                    logger.debug(bstack1l111l1_opy_ (u"ࠤࡆ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡥࡩࡹࡽࡥࡦࡰࠣࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿࠣࡥࡳࡪࠠࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿ࠽ࠤࠧᰉ") + str(bstack111ll1lllll_opy_) + bstack1l111l1_opy_ (u"ࠥࠦᰊ"))
                    result[bstack1l111l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᰋ")] = [f.strip() for f in bstack111ll1lllll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1ll1111l_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᰌ")))
                except Exception:
                    logger.debug(bstack1l111l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠯ࠢࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡷ࡫ࡣࡦࡰࡷࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠨᰍ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l111l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᰎ")] = _111llll1lll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l111l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᰏ")] = _111llll1lll_opy_(commits[:5])
            bstack111l1l1111l_opy_ = set()
            bstack111llllll11_opy_ = []
            for commit in commits:
                logger.debug(bstack1l111l1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰ࡭ࡹࡀࠠࠣᰐ") + str(commit.message) + bstack1l111l1_opy_ (u"ࠥࠦᰑ"))
                bstack111ll11ll1l_opy_ = commit.author.name if commit.author else bstack1l111l1_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧᰒ")
                bstack111l1l1111l_opy_.add(bstack111ll11ll1l_opy_)
                bstack111llllll11_opy_.append({
                    bstack1l111l1_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᰓ"): commit.message.strip(),
                    bstack1l111l1_opy_ (u"ࠨࡵࡴࡧࡵࠦᰔ"): bstack111ll11ll1l_opy_
                })
            result[bstack1l111l1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᰕ")] = list(bstack111l1l1111l_opy_)
            result[bstack1l111l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᰖ")] = bstack111llllll11_opy_
            result[bstack1l111l1_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᰗ")] = bstack111l1l111l1_opy_.committed_datetime.strftime(bstack1l111l1_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠧᰘ"))
            if (not result[bstack1l111l1_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᰙ")] or result[bstack1l111l1_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᰚ")].strip() == bstack1l111l1_opy_ (u"ࠨࠢᰛ")) and bstack111l1l111l1_opy_.message:
                bstack111l1l1ll11_opy_ = bstack111l1l111l1_opy_.message.strip().splitlines()
                result[bstack1l111l1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᰜ")] = bstack111l1l1ll11_opy_[0] if bstack111l1l1ll11_opy_ else bstack1l111l1_opy_ (u"ࠣࠤᰝ")
                if len(bstack111l1l1ll11_opy_) > 2:
                    result[bstack1l111l1_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᰞ")] = bstack1l111l1_opy_ (u"ࠪࡠࡳ࠭ᰟ").join(bstack111l1l1ll11_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࠫࡪࡴࡲࡤࡦࡴ࠽ࠤࢀࢃࠩ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥᰠ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111ll11ll11_opy_(result)
    ]
    return filtered_results
def _111ll11ll11_opy_(result):
    bstack1l111l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡎࡥ࡭ࡲࡨࡶࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡪࡨࠣࡥࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡮ࡹࠠࡷࡣ࡯࡭ࡩࠦࠨ࡯ࡱࡱ࠱ࡪࡳࡰࡵࡻࠣࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡤࡲࡩࠦࡡࡶࡶ࡫ࡳࡷࡹࠩ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᰡ")
    return (
        isinstance(result.get(bstack1l111l1_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᰢ"), None), list)
        and len(result[bstack1l111l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᰣ")]) > 0
        and isinstance(result.get(bstack1l111l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᰤ"), None), list)
        and len(result[bstack1l111l1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᰥ")]) > 0
    )
def _11l11111ll1_opy_(repo):
    bstack1l111l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡘࡷࡿࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡩࡧࠣࡦࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡴࡨࡴࡴࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡩࡣࡵࡨࡨࡵࡤࡦࡦࠣࡲࡦࡳࡥࡴࠢࡤࡲࡩࠦࡷࡰࡴ࡮ࠤࡼ࡯ࡴࡩࠢࡤࡰࡱࠦࡖࡄࡕࠣࡴࡷࡵࡶࡪࡦࡨࡶࡸ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡦࡷࡧ࡮ࡤࡪࠣ࡭࡫ࠦࡰࡰࡵࡶ࡭ࡧࡲࡥ࠭ࠢࡨࡰࡸ࡫ࠠࡏࡱࡱࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᰦ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111ll1lll1l_opy_ = origin.refs[bstack1l111l1_opy_ (u"ࠫࡍࡋࡁࡅࠩᰧ")]
            target = bstack111ll1lll1l_opy_.reference.name
            if target.startswith(bstack1l111l1_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭ᰨ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l111l1_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧᰩ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111llll1lll_opy_(commits):
    bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᰪ")
    bstack111ll1lllll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111lll11ll1_opy_ in diff:
                        if bstack111lll11ll1_opy_.a_path:
                            bstack111ll1lllll_opy_.add(bstack111lll11ll1_opy_.a_path)
                        if bstack111lll11ll1_opy_.b_path:
                            bstack111ll1lllll_opy_.add(bstack111lll11ll1_opy_.b_path)
    except Exception:
        pass
    return list(bstack111ll1lllll_opy_)
def bstack111lll1llll_opy_(bstack111ll11llll_opy_):
    bstack111lll11l1l_opy_ = bstack111l1lllll1_opy_(bstack111ll11llll_opy_)
    if bstack111lll11l1l_opy_ and bstack111lll11l1l_opy_ > bstack11l1l111111_opy_:
        bstack111l1l11ll1_opy_ = bstack111lll11l1l_opy_ - bstack11l1l111111_opy_
        bstack111l1lll1l1_opy_ = bstack111l1l11111_opy_(bstack111ll11llll_opy_[bstack1l111l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᰫ")], bstack111l1l11ll1_opy_)
        bstack111ll11llll_opy_[bstack1l111l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᰬ")] = bstack111l1lll1l1_opy_
        logger.info(bstack1l111l1_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧᰭ")
                    .format(bstack111l1lllll1_opy_(bstack111ll11llll_opy_) / 1024))
    return bstack111ll11llll_opy_
def bstack111l1lllll1_opy_(bstack11ll11ll11_opy_):
    try:
        if bstack11ll11ll11_opy_:
            bstack111l1l1l1l1_opy_ = json.dumps(bstack11ll11ll11_opy_)
            bstack11l111111l1_opy_ = sys.getsizeof(bstack111l1l1l1l1_opy_)
            return bstack11l111111l1_opy_
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦᰮ").format(e))
    return -1
def bstack111l1l11111_opy_(field, bstack111ll111l1l_opy_):
    try:
        bstack111l1l1l11l_opy_ = len(bytes(bstack11l1l111l1l_opy_, bstack1l111l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᰯ")))
        bstack111lllll11l_opy_ = bytes(field, bstack1l111l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᰰ"))
        bstack111ll1l1lll_opy_ = len(bstack111lllll11l_opy_)
        bstack111lll11l11_opy_ = ceil(bstack111ll1l1lll_opy_ - bstack111ll111l1l_opy_ - bstack111l1l1l11l_opy_)
        if bstack111lll11l11_opy_ > 0:
            bstack111l1l1l111_opy_ = bstack111lllll11l_opy_[:bstack111lll11l11_opy_].decode(bstack1l111l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᰱ"), errors=bstack1l111l1_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨᰲ")) + bstack11l1l111l1l_opy_
            return bstack111l1l1l111_opy_
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢᰳ").format(e))
    return field
def bstack11lll11l1_opy_():
    env = os.environ
    if (bstack1l111l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᰴ") in env and len(env[bstack1l111l1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᰵ")]) > 0) or (
            bstack1l111l1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᰶ") in env and len(env[bstack1l111l1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉ᰷ࠧ")]) > 0):
        return {
            bstack1l111l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᰸"): bstack1l111l1_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤ᰹"),
            bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᰺"): env.get(bstack1l111l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᰻")),
            bstack1l111l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᰼"): env.get(bstack1l111l1_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢ᰽")),
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᰾"): env.get(bstack1l111l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᰿"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠣࡅࡌࠦ᱀")) == bstack1l111l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᱁") and bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧ᱂"))):
        return {
            bstack1l111l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᱃"): bstack1l111l1_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢ᱄"),
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᱅"): env.get(bstack1l111l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᱆")),
            bstack1l111l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᱇"): env.get(bstack1l111l1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨ᱈")),
            bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᱉"): env.get(bstack1l111l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢ᱊"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠧࡉࡉࠣ᱋")) == bstack1l111l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ᱌") and bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢᱍ"))):
        return {
            bstack1l111l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᱎ"): bstack1l111l1_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧᱏ"),
            bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᱐"): env.get(bstack1l111l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦ᱑")),
            bstack1l111l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᱒"): env.get(bstack1l111l1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᱓")),
            bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᱔"): env.get(bstack1l111l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᱕"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠤࡆࡍࠧ᱖")) == bstack1l111l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ᱗") and env.get(bstack1l111l1_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧ᱘")) == bstack1l111l1_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᱙"):
        return {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᱚ"): bstack1l111l1_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᱛ"),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱜ"): None,
            bstack1l111l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱝ"): None,
            bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᱞ"): None
        }
    if env.get(bstack1l111l1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᱟ")) and env.get(bstack1l111l1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᱠ")):
        return {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᱡ"): bstack1l111l1_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᱢ"),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱣ"): env.get(bstack1l111l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᱤ")),
            bstack1l111l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᱥ"): None,
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᱦ"): env.get(bstack1l111l1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᱧ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠨࡃࡊࠤᱨ")) == bstack1l111l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᱩ") and bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᱪ"))):
        return {
            bstack1l111l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᱫ"): bstack1l111l1_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᱬ"),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᱭ"): env.get(bstack1l111l1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᱮ")),
            bstack1l111l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᱯ"): None,
            bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᱰ"): env.get(bstack1l111l1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᱱ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠤࡆࡍࠧᱲ")) == bstack1l111l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᱳ") and bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᱴ"))):
        return {
            bstack1l111l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᱵ"): bstack1l111l1_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᱶ"),
            bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᱷ"): env.get(bstack1l111l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᱸ")),
            bstack1l111l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱹ"): env.get(bstack1l111l1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᱺ")),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᱻ"): env.get(bstack1l111l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᱼ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠨࡃࡊࠤᱽ")) == bstack1l111l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ᱾") and bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦ᱿"))):
        return {
            bstack1l111l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᲀ"): bstack1l111l1_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᲁ"),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᲂ"): env.get(bstack1l111l1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᲃ")),
            bstack1l111l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᲄ"): env.get(bstack1l111l1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᲅ")),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᲆ"): env.get(bstack1l111l1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᲇ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠥࡇࡎࠨᲈ")) == bstack1l111l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᲉ") and bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᲊ"))):
        return {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᲋"): bstack1l111l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥ᲌"),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᲍"): env.get(bstack1l111l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᲎")),
            bstack1l111l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᲏"): env.get(bstack1l111l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᲐ")) or env.get(bstack1l111l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᲑ")),
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᲒ"): env.get(bstack1l111l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᲓ"))
        }
    if bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᲔ"))):
        return {
            bstack1l111l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᲕ"): bstack1l111l1_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᲖ"),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᲗ"): bstack1l111l1_opy_ (u"ࠧࢁࡽࡼࡿࠥᲘ").format(env.get(bstack1l111l1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᲙ")), env.get(bstack1l111l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᲚ"))),
            bstack1l111l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᲛ"): env.get(bstack1l111l1_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᲜ")),
            bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᲝ"): env.get(bstack1l111l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᲞ"))
        }
    if bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᲟ"))):
        return {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᲠ"): bstack1l111l1_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᲡ"),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᲢ"): bstack1l111l1_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᲣ").format(env.get(bstack1l111l1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᲤ")), env.get(bstack1l111l1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᲥ")), env.get(bstack1l111l1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭Ღ")), env.get(bstack1l111l1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᲧ"))),
            bstack1l111l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᲨ"): env.get(bstack1l111l1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᲩ")),
            bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᲪ"): env.get(bstack1l111l1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᲫ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᲬ")) and env.get(bstack1l111l1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᲭ")):
        return {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᲮ"): bstack1l111l1_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᲯ"),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᲰ"): bstack1l111l1_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᲱ").format(env.get(bstack1l111l1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭Ჲ")), env.get(bstack1l111l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᲳ")), env.get(bstack1l111l1_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᲴ"))),
            bstack1l111l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᲵ"): env.get(bstack1l111l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᲶ")),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᲷ"): env.get(bstack1l111l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᲸ"))
        }
    if any([env.get(bstack1l111l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᲹ")), env.get(bstack1l111l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᲺ")), env.get(bstack1l111l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤ᲻"))]):
        return {
            bstack1l111l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᲼"): bstack1l111l1_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᲽ"),
            bstack1l111l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᲾ"): env.get(bstack1l111l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᲿ")),
            bstack1l111l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᳀"): env.get(bstack1l111l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᳁")),
            bstack1l111l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᳂"): env.get(bstack1l111l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᳃"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ᳄")):
        return {
            bstack1l111l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᳅"): bstack1l111l1_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤ᳆"),
            bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᳇"): env.get(bstack1l111l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨ᳈")),
            bstack1l111l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᳉"): env.get(bstack1l111l1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧ᳊")),
            bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳋"): env.get(bstack1l111l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨ᳌"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥ᳍")) or env.get(bstack1l111l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ᳎")):
        return {
            bstack1l111l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᳏"): bstack1l111l1_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨ᳐"),
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᳑"): env.get(bstack1l111l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᳒")),
            bstack1l111l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᳓"): bstack1l111l1_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤ᳔") if env.get(bstack1l111l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈ᳕ࠧ")) else None,
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴ᳖ࠥ"): env.get(bstack1l111l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖ᳗ࠥ"))
        }
    if any([env.get(bstack1l111l1_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗ᳘ࠦ")), env.get(bstack1l111l1_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔ᳙ࠣ")), env.get(bstack1l111l1_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ᳚"))]):
        return {
            bstack1l111l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳛"): bstack1l111l1_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤ᳜"),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲ᳝ࠢ"): None,
            bstack1l111l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᳞ࠢ"): env.get(bstack1l111l1_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆ᳟ࠥ")),
            bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳠"): env.get(bstack1l111l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᳡"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉ᳢ࠧ")):
        return {
            bstack1l111l1_opy_ (u"ࠥࡲࡦࡳࡥ᳣ࠣ"): bstack1l111l1_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫᳤ࠢ"),
            bstack1l111l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᳥ࠣ"): env.get(bstack1l111l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐ᳦ࠧ")),
            bstack1l111l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᳧"): bstack1l111l1_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤ᳨").format(env.get(bstack1l111l1_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᳩ"))) if env.get(bstack1l111l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨᳪ")) else None,
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᳫ"): env.get(bstack1l111l1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᳬ"))
        }
    if bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟᳭ࠢ"))):
        return {
            bstack1l111l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᳮ"): bstack1l111l1_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤᳯ"),
            bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᳰ"): env.get(bstack1l111l1_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢᳱ")),
            bstack1l111l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᳲ"): env.get(bstack1l111l1_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣᳳ")),
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᳴"): env.get(bstack1l111l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᳵ"))
        }
    if bstack11lll111_opy_(env.get(bstack1l111l1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤᳶ"))):
        return {
            bstack1l111l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳷"): bstack1l111l1_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦ᳸"),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᳹"): bstack1l111l1_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᳺ").format(env.get(bstack1l111l1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪ᳻")), env.get(bstack1l111l1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫ᳼")), env.get(bstack1l111l1_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨ᳽"))),
            bstack1l111l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᳾"): env.get(bstack1l111l1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧ᳿")),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴀ"): env.get(bstack1l111l1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᴁ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠨࡃࡊࠤᴂ")) == bstack1l111l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᴃ") and env.get(bstack1l111l1_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᴄ")) == bstack1l111l1_opy_ (u"ࠤ࠴ࠦᴅ"):
        return {
            bstack1l111l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᴆ"): bstack1l111l1_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᴇ"),
            bstack1l111l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᴈ"): bstack1l111l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᴉ").format(env.get(bstack1l111l1_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫᴊ"))),
            bstack1l111l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᴋ"): None,
            bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴌ"): None,
        }
    if env.get(bstack1l111l1_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᴍ")):
        return {
            bstack1l111l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᴎ"): bstack1l111l1_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢᴏ"),
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᴐ"): None,
            bstack1l111l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᴑ"): env.get(bstack1l111l1_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤᴒ")),
            bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴓ"): env.get(bstack1l111l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᴔ"))
        }
    if any([env.get(bstack1l111l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᴕ")), env.get(bstack1l111l1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᴖ")), env.get(bstack1l111l1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᴗ")), env.get(bstack1l111l1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᴘ"))]):
        return {
            bstack1l111l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᴙ"): bstack1l111l1_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᴚ"),
            bstack1l111l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᴛ"): None,
            bstack1l111l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᴜ"): env.get(bstack1l111l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᴝ")) or None,
            bstack1l111l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᴞ"): env.get(bstack1l111l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᴟ"), 0)
        }
    if env.get(bstack1l111l1_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᴠ")):
        return {
            bstack1l111l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴡ"): bstack1l111l1_opy_ (u"ࠥࡋࡴࡉࡄࠣᴢ"),
            bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴣ"): None,
            bstack1l111l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᴤ"): env.get(bstack1l111l1_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᴥ")),
            bstack1l111l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᴦ"): env.get(bstack1l111l1_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᴧ"))
        }
    if env.get(bstack1l111l1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᴨ")):
        return {
            bstack1l111l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᴩ"): bstack1l111l1_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢᴪ"),
            bstack1l111l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᴫ"): env.get(bstack1l111l1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᴬ")),
            bstack1l111l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᴭ"): env.get(bstack1l111l1_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᴮ")),
            bstack1l111l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴯ"): env.get(bstack1l111l1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᴰ"))
        }
    return {bstack1l111l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴱ"): None}
def get_host_info():
    return {
        bstack1l111l1_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢᴲ"): platform.node(),
        bstack1l111l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣᴳ"): platform.system(),
        bstack1l111l1_opy_ (u"ࠢࡵࡻࡳࡩࠧᴴ"): platform.machine(),
        bstack1l111l1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᴵ"): platform.version(),
        bstack1l111l1_opy_ (u"ࠤࡤࡶࡨ࡮ࠢᴶ"): platform.architecture()[0]
    }
def bstack11l111l11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111lll1111l_opy_():
    if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᴷ")):
        return bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᴸ")
    return bstack1l111l1_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫᴹ")
def bstack111ll1l1ll1_opy_(driver):
    info = {
        bstack1l111l1_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᴺ"): driver.capabilities,
        bstack1l111l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᴻ"): driver.session_id,
        bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᴼ"): driver.capabilities.get(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᴽ"), None),
        bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᴾ"): driver.capabilities.get(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᴿ"), None),
        bstack1l111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᵀ"): driver.capabilities.get(bstack1l111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᵁ"), None),
        bstack1l111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪᵂ"):driver.capabilities.get(bstack1l111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᵃ"), None),
    }
    if bstack111lll1111l_opy_() == bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᵄ"):
        if bstack11ll1ll1l_opy_():
            info[bstack1l111l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᵅ")] = bstack1l111l1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪᵆ")
        elif driver.capabilities.get(bstack1l111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᵇ"), {}).get(bstack1l111l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᵈ"), False):
            info[bstack1l111l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᵉ")] = bstack1l111l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᵊ")
        else:
            info[bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᵋ")] = bstack1l111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᵌ")
    return info
def bstack11ll1ll1l_opy_():
    if bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᵍ")):
        return True
    if bstack11lll111_opy_(os.environ.get(bstack1l111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᵎ"), None)):
        return True
    return False
def bstack111lll1ll11_opy_(bstack111lll1l111_opy_, url, response, headers=None, data=None):
    bstack1l111l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡂࡶ࡫࡯ࡨࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡯ࡳ࡬ࠦࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠰ࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡰࡴ࡭ࡧࡪࡰࡪࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡵࡺ࡫ࡳࡵࡡࡷࡽࡵ࡫࠺ࠡࡊࡗࡘࡕࠦ࡭ࡦࡶ࡫ࡳࡩࠦࠨࡈࡇࡗ࠰ࠥࡖࡏࡔࡖ࠯ࠤࡪࡺࡣ࠯ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡺࡸ࡬࠻ࠢࡕࡩࡶࡻࡥࡴࡶ࡙ࠣࡗࡒ࠯ࡦࡰࡧࡴࡴ࡯࡮ࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡱࡥ࡮ࡪࡩࡴࠡࡨࡵࡳࡲࠦࡲࡦࡳࡸࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡩࡦࡪࡥࡳࡵ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡮ࡥࡢࡦࡨࡶࡸࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦࡤࡸࡦࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡌࡖࡓࡓࠦࡤࡢࡶࡤࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡋࡵࡲ࡮ࡣࡷࡸࡪࡪࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠥࡽࡩࡵࡪࠣࡶࡪࡷࡵࡦࡵࡷࠤࡦࡴࡤࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠋࠢࠣࠤࠥࠨࠢࠣᵏ")
    bstack111l1l1lll1_opy_ = {
        bstack1l111l1_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣᵐ"): headers,
        bstack1l111l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᵑ"): bstack111lll1l111_opy_.upper(),
        bstack1l111l1_opy_ (u"ࠤࡤ࡫ࡪࡴࡴࠣᵒ"): None,
        bstack1l111l1_opy_ (u"ࠥࡩࡳࡪࡰࡰ࡫ࡱࡸࠧᵓ"): url,
        bstack1l111l1_opy_ (u"ࠦ࡯ࡹ࡯࡯ࠤᵔ"): data
    }
    try:
        bstack111lllll1l1_opy_ = response.json()
    except Exception:
        bstack111lllll1l1_opy_ = response.text
    bstack111lll1lll1_opy_ = {
        bstack1l111l1_opy_ (u"ࠧࡨ࡯ࡥࡻࠥᵕ"): bstack111lllll1l1_opy_,
        bstack1l111l1_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࡉ࡯ࡥࡧࠥᵖ"): response.status_code
    }
    return {
        bstack1l111l1_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᵗ"): bstack111l1l1lll1_opy_,
        bstack1l111l1_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᵘ"): bstack111lll1lll1_opy_
    }
def bstack11l1l1l1l_opy_(bstack111lll1l111_opy_, url, data, config):
    headers = config.get(bstack1l111l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᵙ"), None)
    proxies = bstack111lll1l1l_opy_(config, url)
    auth = config.get(bstack1l111l1_opy_ (u"ࠪࡥࡺࡺࡨࠨᵚ"), None)
    response = requests.request(
            bstack111lll1l111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack111lll1ll11_opy_(bstack111lll1l111_opy_, url, response, headers, data)
        bstack1l1111ll1_opy_.debug(json.dumps(log_message, separators=(bstack1l111l1_opy_ (u"ࠫ࠱࠭ᵛ"), bstack1l111l1_opy_ (u"ࠬࡀࠧᵜ"))))
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࢀࢃࠢᵝ").format(e))
    return response
def bstack11ll1llll_opy_(bstack1llll11l_opy_, size):
    bstack1ll1l111_opy_ = []
    while len(bstack1llll11l_opy_) > size:
        bstack1lllll11l_opy_ = bstack1llll11l_opy_[:size]
        bstack1ll1l111_opy_.append(bstack1lllll11l_opy_)
        bstack1llll11l_opy_ = bstack1llll11l_opy_[size:]
    bstack1ll1l111_opy_.append(bstack1llll11l_opy_)
    return bstack1ll1l111_opy_
def bstack111lll111ll_opy_(message, bstack111llll11ll_opy_=False):
    os.write(1, bytes(message, bstack1l111l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᵞ")))
    os.write(1, bytes(bstack1l111l1_opy_ (u"ࠨ࡞ࡱࠫᵟ"), bstack1l111l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᵠ")))
    if bstack111llll11ll_opy_:
        with open(bstack1l111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩᵡ") + os.environ[bstack1l111l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᵢ")] + bstack1l111l1_opy_ (u"ࠬ࠴࡬ࡰࡩࠪᵣ"), bstack1l111l1_opy_ (u"࠭ࡡࠨᵤ")) as f:
            f.write(message + bstack1l111l1_opy_ (u"ࠧ࡝ࡰࠪᵥ"))
def bstack1l1l1l11l1l_opy_():
    return os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᵦ")].lower() == bstack1l111l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᵧ")
def bstack11llll1111_opy_():
    return bstack1111l1l1ll_opy_().replace(tzinfo=None).isoformat() + bstack1l111l1_opy_ (u"ࠪ࡞ࠬᵨ")
def bstack111llllllll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l111l1_opy_ (u"ࠫ࡟࠭ᵩ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l111l1_opy_ (u"ࠬࡠࠧᵪ")))).total_seconds() * 1000
def bstack111lll1ll1l_opy_(timestamp):
    return bstack111l1llllll_opy_(timestamp).isoformat() + bstack1l111l1_opy_ (u"࡚࠭ࠨᵫ")
def bstack111ll1l1111_opy_(bstack111l1l11l11_opy_):
    date_format = bstack1l111l1_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬᵬ")
    bstack11l1111l1l1_opy_ = datetime.datetime.strptime(bstack111l1l11l11_opy_, date_format)
    return bstack11l1111l1l1_opy_.isoformat() + bstack1l111l1_opy_ (u"ࠨ࡜ࠪᵭ")
def bstack111ll111ll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᵮ")
    else:
        return bstack1l111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵯ")
def bstack11lll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l111l1_opy_ (u"ࠫࡹࡸࡵࡦࠩᵰ")
def bstack111ll1l1l1l_opy_(val):
    return val.__str__().lower() == bstack1l111l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᵱ")
def error_handler(bstack111llll1l11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111llll1l11_opy_ as e:
                print(bstack1l111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᵲ").format(func.__name__, bstack111llll1l11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111ll11l11l_opy_(bstack111l1llll1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l1llll1l_opy_(cls, *args, **kwargs)
            except bstack111llll1l11_opy_ as e:
                print(bstack1l111l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᵳ").format(bstack111l1llll1l_opy_.__name__, bstack111llll1l11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111ll11l11l_opy_
    else:
        return decorator
def bstack11lll1lll_opy_(bstack1lllllll1l1_opy_):
    if os.getenv(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᵴ")) is not None:
        return bstack11lll111_opy_(os.getenv(bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᵵ")))
    if bstack1l111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᵶ") in bstack1lllllll1l1_opy_ and bstack111ll1l1l1l_opy_(bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᵷ")]):
        return False
    if bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᵸ") in bstack1lllllll1l1_opy_ and bstack111ll1l1l1l_opy_(bstack1lllllll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᵹ")]):
        return False
    return True
def bstack1lllllll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1111l11l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢᵺ"), None)
        return bstack11l1111l11l_opy_ is None or bstack11l1111l11l_opy_ == bstack1l111l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᵻ")
    except Exception as e:
        return False
def bstack1lllllll11_opy_(hub_url, CONFIG):
    if bstack111l1111l_opy_() <= version.parse(bstack1l111l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᵼ")):
        if hub_url:
            return bstack1l111l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᵽ") + hub_url + bstack1l111l1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᵾ")
        return bstack11lllllll1_opy_
    if hub_url:
        return bstack1l111l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᵿ") + hub_url + bstack1l111l1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᶀ")
    return bstack1l11lll111_opy_
def bstack111ll11l1ll_opy_():
    return isinstance(os.getenv(bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᶁ")), str)
def bstack1ll1l1l1l1_opy_(url):
    return urlparse(url).hostname
def bstack1ll111l1_opy_(hostname):
    for bstack111lllll1_opy_ in bstack1l1l1l1l_opy_:
        regex = re.compile(bstack111lllll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1111llll_opy_(bstack111ll1ll11l_opy_, file_name, logger):
    bstack1lll1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠨࢀࠪᶂ")), bstack111ll1ll11l_opy_)
    try:
        if not os.path.exists(bstack1lll1l1l1_opy_):
            os.makedirs(bstack1lll1l1l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠩࢁࠫᶃ")), bstack111ll1ll11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l111l1_opy_ (u"ࠪࡻࠬᶄ")):
                pass
            with open(file_path, bstack1l111l1_opy_ (u"ࠦࡼ࠱ࠢᶅ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l111l_opy_.format(str(e)))
def bstack11l1111ll1l_opy_(file_name, key, value, logger):
    file_path = bstack11l1111llll_opy_(bstack1l111l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᶆ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11lll1ll1_opy_ = json.load(open(file_path, bstack1l111l1_opy_ (u"࠭ࡲࡣࠩᶇ")))
        else:
            bstack11lll1ll1_opy_ = {}
        bstack11lll1ll1_opy_[key] = value
        with open(file_path, bstack1l111l1_opy_ (u"ࠢࡸ࠭ࠥᶈ")) as outfile:
            json.dump(bstack11lll1ll1_opy_, outfile)
def bstack1l1l11l1l_opy_(file_name, logger):
    file_path = bstack11l1111llll_opy_(bstack1l111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᶉ"), file_name, logger)
    bstack11lll1ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l111l1_opy_ (u"ࠩࡵࠫᶊ")) as bstack1l1111l1_opy_:
            bstack11lll1ll1_opy_ = json.load(bstack1l1111l1_opy_)
    return bstack11lll1ll1_opy_
def bstack111lll1l11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᶋ") + file_path + bstack1l111l1_opy_ (u"ࠫࠥ࠭ᶌ") + str(e))
def bstack111l1111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l111l1_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᶍ")
def bstack1llllllll_opy_(config):
    if bstack1l111l1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᶎ") in config:
        del (config[bstack1l111l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᶏ")])
        return False
    if bstack111l1111l_opy_() < version.parse(bstack1l111l1_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᶐ")):
        return False
    if bstack111l1111l_opy_() >= version.parse(bstack1l111l1_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᶑ")):
        return True
    if bstack1l111l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᶒ") in config and config[bstack1l111l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᶓ")] is False:
        return False
    else:
        return True
def bstack1lll11l1l1_opy_(args_list, bstack111l1ll1lll_opy_):
    index = -1
    for value in bstack111l1ll1lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1lll11l1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1lll11l1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111l111lll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111l111lll_opy_ = bstack111l111lll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l111l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᶔ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᶕ"), exception=exception)
    def bstack1lllll111ll_opy_(self):
        if self.result != bstack1l111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᶖ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l111l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᶗ") in self.exception_type:
            return bstack1l111l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᶘ")
        return bstack1l111l1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᶙ")
    def bstack11l1111111l_opy_(self):
        if self.result != bstack1l111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᶚ"):
            return None
        if self.bstack111l111lll_opy_:
            return self.bstack111l111lll_opy_
        return bstack111l1llll11_opy_(self.exception)
def bstack111l1llll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111lll11111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1l1l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111llll1_opy_(config, logger):
    try:
        import playwright
        bstack111lll111l1_opy_ = playwright.__file__
        bstack111l1l11lll_opy_ = os.path.split(bstack111lll111l1_opy_)
        bstack111l1ll11l1_opy_ = bstack111l1l11lll_opy_[0] + bstack1l111l1_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᶛ")
        os.environ[bstack1l111l1_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᶜ")] = bstack11ll11l1l_opy_(config)
        with open(bstack111l1ll11l1_opy_, bstack1l111l1_opy_ (u"ࠧࡳࠩᶝ")) as f:
            bstack11l1lllll_opy_ = f.read()
            bstack111lll11lll_opy_ = bstack1l111l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᶞ")
            bstack111llll111l_opy_ = bstack11l1lllll_opy_.find(bstack111lll11lll_opy_)
            if bstack111llll111l_opy_ == -1:
              process = subprocess.Popen(bstack1l111l1_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᶟ"), shell=True, cwd=bstack111l1l11lll_opy_[0])
              process.wait()
              bstack111llll1ll1_opy_ = bstack1l111l1_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᶠ")
              bstack111ll111111_opy_ = bstack1l111l1_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᶡ")
              bstack111l1ll111l_opy_ = bstack11l1lllll_opy_.replace(bstack111llll1ll1_opy_, bstack111ll111111_opy_)
              with open(bstack111l1ll11l1_opy_, bstack1l111l1_opy_ (u"ࠬࡽࠧᶢ")) as f:
                f.write(bstack111l1ll111l_opy_)
    except Exception as e:
        logger.error(bstack11l1lll111_opy_.format(str(e)))
def bstack1lll1l1ll1_opy_():
  try:
    bstack111l11lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᶣ"))
    bstack111l11lll11_opy_ = []
    if os.path.exists(bstack111l11lllll_opy_):
      with open(bstack111l11lllll_opy_) as f:
        bstack111l11lll11_opy_ = json.load(f)
      os.remove(bstack111l11lllll_opy_)
    return bstack111l11lll11_opy_
  except:
    pass
  return []
def bstack111lll1111_opy_(bstack11lll1l111_opy_):
  try:
    bstack111l11lll11_opy_ = []
    bstack111l11lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᶤ"))
    if os.path.exists(bstack111l11lllll_opy_):
      with open(bstack111l11lllll_opy_) as f:
        bstack111l11lll11_opy_ = json.load(f)
    bstack111l11lll11_opy_.append(bstack11lll1l111_opy_)
    with open(bstack111l11lllll_opy_, bstack1l111l1_opy_ (u"ࠨࡹࠪᶥ")) as f:
        json.dump(bstack111l11lll11_opy_, f)
  except:
    pass
def bstack111l11l11_opy_(logger, bstack111l1ll11ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l111l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᶦ"), bstack1l111l1_opy_ (u"ࠪࠫᶧ"))
    if test_name == bstack1l111l1_opy_ (u"ࠫࠬᶨ"):
        test_name = threading.current_thread().__dict__.get(bstack1l111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᶩ"), bstack1l111l1_opy_ (u"࠭ࠧᶪ"))
    bstack111lllll111_opy_ = bstack1l111l1_opy_ (u"ࠧ࠭ࠢࠪᶫ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l1ll11ll_opy_:
        bstack1l1l11111l_opy_ = os.environ.get(bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᶬ"), bstack1l111l1_opy_ (u"ࠩ࠳ࠫᶭ"))
        bstack11ll1ll1_opy_ = {bstack1l111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᶮ"): test_name, bstack1l111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᶯ"): bstack111lllll111_opy_, bstack1l111l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᶰ"): bstack1l1l11111l_opy_}
        bstack11l1111l1ll_opy_ = []
        bstack111ll11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᶱ"))
        if os.path.exists(bstack111ll11l1l1_opy_):
            with open(bstack111ll11l1l1_opy_) as f:
                bstack11l1111l1ll_opy_ = json.load(f)
        bstack11l1111l1ll_opy_.append(bstack11ll1ll1_opy_)
        with open(bstack111ll11l1l1_opy_, bstack1l111l1_opy_ (u"ࠧࡸࠩᶲ")) as f:
            json.dump(bstack11l1111l1ll_opy_, f)
    else:
        bstack11ll1ll1_opy_ = {bstack1l111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶳ"): test_name, bstack1l111l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᶴ"): bstack111lllll111_opy_, bstack1l111l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᶵ"): str(multiprocessing.current_process().name)}
        if bstack1l111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᶶ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11ll1ll1_opy_)
  except Exception as e:
      logger.warn(bstack1l111l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᶷ").format(e))
def bstack1llll11lll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩᶸ"))
    try:
      bstack111lll1l1ll_opy_ = []
      bstack11ll1ll1_opy_ = {bstack1l111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᶹ"): test_name, bstack1l111l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᶺ"): error_message, bstack1l111l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᶻ"): index}
      bstack11l11111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᶼ"))
      if os.path.exists(bstack11l11111111_opy_):
          with open(bstack11l11111111_opy_) as f:
              bstack111lll1l1ll_opy_ = json.load(f)
      bstack111lll1l1ll_opy_.append(bstack11ll1ll1_opy_)
      with open(bstack11l11111111_opy_, bstack1l111l1_opy_ (u"ࠫࡼ࠭ᶽ")) as f:
          json.dump(bstack111lll1l1ll_opy_, f)
    except Exception as e:
      logger.warn(bstack1l111l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᶾ").format(e))
    return
  bstack111lll1l1ll_opy_ = []
  bstack11ll1ll1_opy_ = {bstack1l111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᶿ"): test_name, bstack1l111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᷀"): error_message, bstack1l111l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᷁"): index}
  bstack11l11111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰ᷂ࠪ"))
  lock_file = bstack11l11111111_opy_ + bstack1l111l1_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩ᷃")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l11111111_opy_):
          with open(bstack11l11111111_opy_, bstack1l111l1_opy_ (u"ࠫࡷ࠭᷄")) as f:
              content = f.read().strip()
              if content:
                  bstack111lll1l1ll_opy_ = json.load(open(bstack11l11111111_opy_))
      bstack111lll1l1ll_opy_.append(bstack11ll1ll1_opy_)
      with open(bstack11l11111111_opy_, bstack1l111l1_opy_ (u"ࠬࡽࠧ᷅")) as f:
          json.dump(bstack111lll1l1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l111l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨ࠼ࠣࡿࢂࠨ᷆").format(e))
def bstack1l1111ll1l_opy_(bstack111ll1l1ll_opy_, name, logger):
  try:
    bstack11ll1ll1_opy_ = {bstack1l111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᷇"): name, bstack1l111l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᷈"): bstack111ll1l1ll_opy_, bstack1l111l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ᷉"): str(threading.current_thread()._name)}
    return bstack11ll1ll1_opy_
  except Exception as e:
    logger.warn(bstack1l111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃ᷊ࠢ").format(e))
  return
def bstack111ll1l11l1_opy_():
    return platform.system() == bstack1l111l1_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬ᷋")
def bstack1ll11l111l_opy_(bstack111ll11lll1_opy_, config, logger):
    bstack111ll1l111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111ll11lll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ᷌").format(e))
    return bstack111ll1l111l_opy_
def bstack11l111l1111_opy_(bstack111ll1l1l11_opy_, bstack111l1lll1ll_opy_):
    bstack111lllllll1_opy_ = version.parse(bstack111ll1l1l11_opy_)
    bstack11l11111l11_opy_ = version.parse(bstack111l1lll1ll_opy_)
    if bstack111lllllll1_opy_ > bstack11l11111l11_opy_:
        return 1
    elif bstack111lllllll1_opy_ < bstack11l11111l11_opy_:
        return -1
    else:
        return 0
def bstack1111l1l1ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1llllll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111ll1ll1l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll11l1ll_opy_(options, framework, config, bstack1lll1111l1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l111l1_opy_ (u"࠭ࡧࡦࡶࠪ᷍"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1llll11l_opy_ = caps.get(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᷎"))
    bstack111lllll1ll_opy_ = True
    bstack1l1llll11_opy_ = os.environ[bstack1l111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ᷏࠭")]
    bstack1l1lllllll1_opy_ = config.get(bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ᷐ࠩ"), False)
    if bstack1l1lllllll1_opy_:
        bstack1ll1lll11ll_opy_ = config.get(bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᷑"), {})
        bstack1ll1lll11ll_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧ᷒")] = os.getenv(bstack1l111l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᷓ"))
        bstack11l1lllll11_opy_ = json.loads(os.getenv(bstack1l111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᷔ"), bstack1l111l1_opy_ (u"ࠧࡼࡿࠪᷕ"))).get(bstack1l111l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᷖ"))
    if bstack111ll1l1l1l_opy_(caps.get(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨᷗ"))) or bstack111ll1l1l1l_opy_(caps.get(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪᷘ"))):
        bstack111lllll1ll_opy_ = False
    if bstack1llllllll_opy_({bstack1l111l1_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦᷙ"): bstack111lllll1ll_opy_}):
        bstack1l1llll11l_opy_ = bstack1l1llll11l_opy_ or {}
        bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᷚ")] = bstack111ll1ll1l1_opy_(framework)
        bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᷛ")] = bstack1l1l1l11l1l_opy_()
        bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᷜ")] = bstack1l1llll11_opy_
        bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᷝ")] = bstack1lll1111l1_opy_
        if bstack1l1lllllll1_opy_:
            bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᷞ")] = bstack1l1lllllll1_opy_
            bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᷟ")] = bstack1ll1lll11ll_opy_
            bstack1l1llll11l_opy_[bstack1l111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᷠ")][bstack1l111l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᷡ")] = bstack11l1lllll11_opy_
        if getattr(options, bstack1l111l1_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᷢ"), None):
            options.set_capability(bstack1l111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᷣ"), bstack1l1llll11l_opy_)
        else:
            options[bstack1l111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᷤ")] = bstack1l1llll11l_opy_
    else:
        if getattr(options, bstack1l111l1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᷥ"), None):
            options.set_capability(bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᷦ"), bstack111ll1ll1l1_opy_(framework))
            options.set_capability(bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᷧ"), bstack1l1l1l11l1l_opy_())
            options.set_capability(bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᷨ"), bstack1l1llll11_opy_)
            options.set_capability(bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᷩ"), bstack1lll1111l1_opy_)
            if bstack1l1lllllll1_opy_:
                options.set_capability(bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᷪ"), bstack1l1lllllll1_opy_)
                options.set_capability(bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᷫ"), bstack1ll1lll11ll_opy_)
                options.set_capability(bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᷬ"), bstack11l1lllll11_opy_)
        else:
            options[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᷭ")] = bstack111ll1ll1l1_opy_(framework)
            options[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᷮ")] = bstack1l1l1l11l1l_opy_()
            options[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᷯ")] = bstack1l1llll11_opy_
            options[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᷰ")] = bstack1lll1111l1_opy_
            if bstack1l1lllllll1_opy_:
                options[bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᷱ")] = bstack1l1lllllll1_opy_
                options[bstack1l111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᷲ")] = bstack1ll1lll11ll_opy_
                options[bstack1l111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᷳ")][bstack1l111l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᷴ")] = bstack11l1lllll11_opy_
    return options
def bstack111ll111l11_opy_(bstack111lll1l11l_opy_, framework):
    bstack1lll1111l1_opy_ = bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠦࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡒࡕࡓࡉ࡛ࡃࡕࡡࡐࡅࡕࠨ᷵"))
    if bstack111lll1l11l_opy_ and len(bstack111lll1l11l_opy_.split(bstack1l111l1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᷶"))) > 1:
        ws_url = bstack111lll1l11l_opy_.split(bstack1l111l1_opy_ (u"࠭ࡣࡢࡲࡶࡁ᷷ࠬ"))[0]
        if bstack1l111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯᷸ࠪ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l11ll1l1_opy_ = json.loads(urllib.parse.unquote(bstack111lll1l11l_opy_.split(bstack1l111l1_opy_ (u"ࠨࡥࡤࡴࡸࡃ᷹ࠧ"))[1]))
            bstack111l11ll1l1_opy_ = bstack111l11ll1l1_opy_ or {}
            bstack1l1llll11_opy_ = os.environ[bstack1l111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊ᷺ࠧ")]
            bstack111l11ll1l1_opy_[bstack1l111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᷻")] = str(framework) + str(__version__)
            bstack111l11ll1l1_opy_[bstack1l111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᷼")] = bstack1l1l1l11l1l_opy_()
            bstack111l11ll1l1_opy_[bstack1l111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪ᷽ࠧ")] = bstack1l1llll11_opy_
            bstack111l11ll1l1_opy_[bstack1l111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ᷾")] = bstack1lll1111l1_opy_
            bstack111lll1l11l_opy_ = bstack111lll1l11l_opy_.split(bstack1l111l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ᷿࠭"))[0] + bstack1l111l1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧḀ") + urllib.parse.quote(json.dumps(bstack111l11ll1l1_opy_))
    return bstack111lll1l11l_opy_
def bstack1111l1l11_opy_():
    global bstack11ll11lll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11ll11lll_opy_ = BrowserType.connect
    return bstack11ll11lll_opy_
def bstack111ll1l111_opy_(framework_name):
    global bstack1lll11ll1l_opy_
    bstack1lll11ll1l_opy_ = framework_name
    return framework_name
def bstack1111l1lll_opy_(self, *args, **kwargs):
    global bstack11ll11lll_opy_
    try:
        global bstack1lll11ll1l_opy_
        if bstack1l111l1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ḁ") in kwargs:
            kwargs[bstack1l111l1_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧḂ")] = bstack111ll111l11_opy_(
                kwargs.get(bstack1l111l1_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨḃ"), None),
                bstack1lll11ll1l_opy_
            )
    except Exception as e:
        logger.error(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧḄ").format(str(e)))
    return bstack11ll11lll_opy_(self, *args, **kwargs)
def bstack111ll1llll1_opy_(bstack111l1l1l1ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111lll1l1l_opy_(bstack111l1l1l1ll_opy_, bstack1l111l1_opy_ (u"ࠨࠢḅ"))
        if proxies and proxies.get(bstack1l111l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨḆ")):
            parsed_url = urlparse(proxies.get(bstack1l111l1_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢḇ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬḈ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ḉ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧḊ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l111l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨḋ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11lll11_opy_(bstack111l1l1l1ll_opy_):
    bstack111l1ll1111_opy_ = {
        bstack11l11l1l1l1_opy_[bstack111llll1111_opy_]: bstack111l1l1l1ll_opy_[bstack111llll1111_opy_]
        for bstack111llll1111_opy_ in bstack111l1l1l1ll_opy_
        if bstack111llll1111_opy_ in bstack11l11l1l1l1_opy_
    }
    bstack111l1ll1111_opy_[bstack1l111l1_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨḌ")] = bstack111ll1llll1_opy_(bstack111l1l1l1ll_opy_, bstack1l1l1111_opy_.get_property(bstack1l111l1_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢḍ")))
    bstack111l1ll1l1l_opy_ = [element.lower() for element in bstack11l1l111lll_opy_]
    bstack111l11ll11l_opy_(bstack111l1ll1111_opy_, bstack111l1ll1l1l_opy_)
    return bstack111l1ll1111_opy_
def bstack111l11ll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l111l1_opy_ (u"ࠣࠬ࠭࠮࠯ࠨḎ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l11ll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l11ll11l_opy_(item, keys)
def bstack1l1l1lll1ll_opy_():
    bstack111ll1lll11_opy_ = [os.environ.get(bstack1l111l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡌࡐࡊ࡙࡟ࡅࡋࡕࠦḏ")), os.path.join(os.path.expanduser(bstack1l111l1_opy_ (u"ࠥࢂࠧḐ")), bstack1l111l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫḑ")), os.path.join(bstack1l111l1_opy_ (u"ࠬ࠵ࡴ࡮ࡲࠪḒ"), bstack1l111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ḓ"))]
    for path in bstack111ll1lll11_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l111l1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢḔ") + str(path) + bstack1l111l1_opy_ (u"ࠣࠩࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦḕ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l111l1_opy_ (u"ࠤࡊ࡭ࡻ࡯࡮ࡨࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠠࡧࡱࡵࠤࠬࠨḖ") + str(path) + bstack1l111l1_opy_ (u"ࠥࠫࠧḗ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l111l1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦḘ") + str(path) + bstack1l111l1_opy_ (u"ࠧ࠭ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡪࡤࡷࠥࡺࡨࡦࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴ࠰ࠥḙ"))
            else:
                logger.debug(bstack1l111l1_opy_ (u"ࠨࡃࡳࡧࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࠧࠣḚ") + str(path) + bstack1l111l1_opy_ (u"ࠢࠨࠢࡺ࡭ࡹ࡮ࠠࡸࡴ࡬ࡸࡪࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰ࠱ࠦḛ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l111l1_opy_ (u"ࠣࡑࡳࡩࡷࡧࡴࡪࡱࡱࠤࡸࡻࡣࡤࡧࡨࡨࡪࡪࠠࡧࡱࡵࠤࠬࠨḜ") + str(path) + bstack1l111l1_opy_ (u"ࠤࠪ࠲ࠧḝ"))
            return path
        except Exception as e:
            logger.debug(bstack1l111l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡹࡵࠦࡦࡪ࡮ࡨࠤࠬࢁࡰࡢࡶ࡫ࢁࠬࡀࠠࠣḞ") + str(e) + bstack1l111l1_opy_ (u"ࠦࠧḟ"))
    logger.debug(bstack1l111l1_opy_ (u"ࠧࡇ࡬࡭ࠢࡳࡥࡹ࡮ࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠤḠ"))
    return None
@measure(event_name=EVENTS.bstack11l1l1111l1_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack1lll111111l_opy_(binary_path, bstack1ll1l11l1ll_opy_, bs_config):
    logger.debug(bstack1l111l1_opy_ (u"ࠨࡃࡶࡴࡵࡩࡳࡺࠠࡄࡎࡌࠤࡕࡧࡴࡩࠢࡩࡳࡺࡴࡤ࠻ࠢࡾࢁࠧḡ").format(binary_path))
    bstack111l1ll1l11_opy_ = bstack1l111l1_opy_ (u"ࠧࠨḢ")
    bstack111ll111lll_opy_ = {
        bstack1l111l1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ḣ"): __version__,
        bstack1l111l1_opy_ (u"ࠤࡲࡷࠧḤ"): platform.system(),
        bstack1l111l1_opy_ (u"ࠥࡳࡸࡥࡡࡳࡥ࡫ࠦḥ"): platform.machine(),
        bstack1l111l1_opy_ (u"ࠦࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠤḦ"): bstack1l111l1_opy_ (u"ࠬ࠶ࠧḧ"),
        bstack1l111l1_opy_ (u"ࠨࡳࡥ࡭ࡢࡰࡦࡴࡧࡶࡣࡪࡩࠧḨ"): bstack1l111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧḩ")
    }
    bstack11l1111l111_opy_(bstack111ll111lll_opy_)
    try:
        if binary_path:
            if bstack111ll1l11l1_opy_():
                bstack111ll111lll_opy_[bstack1l111l1_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ḫ")] = subprocess.check_output([binary_path, bstack1l111l1_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥḫ")]).strip().decode(bstack1l111l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩḬ"))
            else:
                bstack111ll111lll_opy_[bstack1l111l1_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩḭ")] = subprocess.check_output([binary_path, bstack1l111l1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨḮ")], stderr=subprocess.DEVNULL).strip().decode(bstack1l111l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬḯ"))
        response = requests.request(
            bstack1l111l1_opy_ (u"ࠧࡈࡇࡗࠫḰ"),
            url=bstack11ll11ll1_opy_(bstack11l11lll1ll_opy_),
            headers=None,
            auth=(bs_config[bstack1l111l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪḱ")], bs_config[bstack1l111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬḲ")]),
            json=None,
            params=bstack111ll111lll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l111l1_opy_ (u"ࠪࡹࡷࡲࠧḳ") in data.keys() and bstack1l111l1_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪḴ") in data.keys():
            logger.debug(bstack1l111l1_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨḵ").format(bstack111ll111lll_opy_[bstack1l111l1_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫḶ")]))
            if bstack1l111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪḷ") in os.environ:
                logger.debug(bstack1l111l1_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦḸ"))
                data[bstack1l111l1_opy_ (u"ࠩࡸࡶࡱ࠭ḹ")] = os.environ[bstack1l111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭Ḻ")]
            bstack111l11llll1_opy_ = bstack111llllll1l_opy_(data[bstack1l111l1_opy_ (u"ࠫࡺࡸ࡬ࠨḻ")], bstack1ll1l11l1ll_opy_)
            bstack111l1ll1l11_opy_ = os.path.join(bstack1ll1l11l1ll_opy_, bstack111l11llll1_opy_)
            os.chmod(bstack111l1ll1l11_opy_, 0o777) # bstack111llll1l1l_opy_ permission
            return bstack111l1ll1l11_opy_
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧḼ").format(e))
    return binary_path
def bstack11l1111l111_opy_(bstack111ll111lll_opy_):
    try:
        if bstack1l111l1_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬḽ") not in bstack111ll111lll_opy_[bstack1l111l1_opy_ (u"ࠧࡰࡵࠪḾ")].lower():
            return
        if os.path.exists(bstack1l111l1_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥḿ")):
            with open(bstack1l111l1_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦṀ"), bstack1l111l1_opy_ (u"ࠥࡶࠧṁ")) as f:
                bstack111llll11l1_opy_ = {}
                for line in f:
                    if bstack1l111l1_opy_ (u"ࠦࡂࠨṂ") in line:
                        key, value = line.rstrip().split(bstack1l111l1_opy_ (u"ࠧࡃࠢṃ"), 1)
                        bstack111llll11l1_opy_[key] = value.strip(bstack1l111l1_opy_ (u"࠭ࠢ࡝ࠩࠪṄ"))
                bstack111ll111lll_opy_[bstack1l111l1_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧṅ")] = bstack111llll11l1_opy_.get(bstack1l111l1_opy_ (u"ࠣࡋࡇࠦṆ"), bstack1l111l1_opy_ (u"ࠤࠥṇ"))
        elif os.path.exists(bstack1l111l1_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤṈ")):
            bstack111ll111lll_opy_[bstack1l111l1_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫṉ")] = bstack1l111l1_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬṊ")
    except Exception as e:
        logger.debug(bstack1l111l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣṋ") + e)
@measure(event_name=EVENTS.bstack11l11l11lll_opy_, stage=STAGE.bstack11l11l11l1_opy_)
def bstack111llllll1l_opy_(bstack111ll1l11ll_opy_, bstack111l1lll11l_opy_):
    logger.debug(bstack1l111l1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤṌ") + str(bstack111ll1l11ll_opy_) + bstack1l111l1_opy_ (u"ࠣࠤṍ"))
    zip_path = os.path.join(bstack111l1lll11l_opy_, bstack1l111l1_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣṎ"))
    bstack111l11llll1_opy_ = bstack1l111l1_opy_ (u"ࠪࠫṏ")
    with requests.get(bstack111ll1l11ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l111l1_opy_ (u"ࠦࡼࡨࠢṐ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l111l1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢṑ"))
    with zipfile.ZipFile(zip_path, bstack1l111l1_opy_ (u"࠭ࡲࠨṒ")) as zip_ref:
        bstack11l1111ll11_opy_ = zip_ref.namelist()
        if len(bstack11l1111ll11_opy_) > 0:
            bstack111l11llll1_opy_ = bstack11l1111ll11_opy_[0] # bstack111l1lll111_opy_ bstack11l11llll11_opy_ will be bstack111l1l1llll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l1lll11l_opy_)
        logger.debug(bstack1l111l1_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨṓ") + str(bstack111l1lll11l_opy_) + bstack1l111l1_opy_ (u"ࠣࠩࠥṔ"))
    os.remove(zip_path)
    return bstack111l11llll1_opy_
def get_cli_dir():
    bstack11l1111lll1_opy_ = bstack1l1l1lll1ll_opy_()
    if bstack11l1111lll1_opy_:
        bstack1ll1l11l1ll_opy_ = os.path.join(bstack11l1111lll1_opy_, bstack1l111l1_opy_ (u"ࠤࡦࡰ࡮ࠨṕ"))
        if not os.path.exists(bstack1ll1l11l1ll_opy_):
            os.makedirs(bstack1ll1l11l1ll_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l11l1ll_opy_
    else:
        raise FileNotFoundError(bstack1l111l1_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨṖ"))
def bstack1ll1ll1ll1l_opy_(bstack1ll1l11l1ll_opy_):
    bstack1l111l1_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣṗ")
    bstack111ll1ll111_opy_ = [
        os.path.join(bstack1ll1l11l1ll_opy_, f)
        for f in os.listdir(bstack1ll1l11l1ll_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l11l1ll_opy_, f)) and f.startswith(bstack1l111l1_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨṘ"))
    ]
    if len(bstack111ll1ll111_opy_) > 0:
        return max(bstack111ll1ll111_opy_, key=os.path.getmtime) # get bstack11l11111lll_opy_ binary
    return bstack1l111l1_opy_ (u"ࠨࠢṙ")
def bstack11ll111l111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11l11111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll11l11111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1llll1l1ll_opy_(data, keys, default=None):
    bstack1l111l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡣࡩࡩࡱࡿࠠࡨࡧࡷࠤࡦࠦ࡮ࡦࡵࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡤࡸࡦࡀࠠࡕࡪࡨࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡷࡳࠥࡺࡲࡢࡸࡨࡶࡸ࡫࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡱࡥࡺࡵ࠽ࠤࡆࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠ࡬ࡧࡼࡷ࠴࡯࡮ࡥ࡫ࡦࡩࡸࠦࡲࡦࡲࡵࡩࡸ࡫࡮ࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡥࡧࡣࡸࡰࡹࡀࠠࡗࡣ࡯ࡹࡪࠦࡴࡰࠢࡵࡩࡹࡻࡲ࡯ࠢ࡬ࡪࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡳࡧࡷࡹࡷࡴ࠺ࠡࡖ࡫ࡩࠥࡼࡡ࡭ࡷࡨࠤࡦࡺࠠࡵࡪࡨࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡧࡴࡩ࠮ࠣࡳࡷࠦࡤࡦࡨࡤࡹࡱࡺࠠࡪࡨࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠴ࠊࠡࠢࠣࠤࠧࠨࠢṚ")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default
def bstack11ll1l1lll_opy_(bstack111ll1ll1ll_opy_, key, value):
    bstack1l111l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡷࡳࡷ࡫ࠠࡄࡎࡌࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠥࡳࡡࡱࡲ࡬ࡲ࡬ࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡱ࡯࡟ࡦࡰࡹࡣࡻࡧࡲࡴࡡࡰࡥࡵࡀࠠࡅ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾࡀࠠࡌࡧࡼࠤ࡫ࡸ࡯࡮ࠢࡆࡐࡎࡥࡃࡂࡒࡖࡣ࡙ࡕ࡟ࡄࡑࡑࡊࡎࡍࠊࠡࠢࠣࠤࠥࠦࠠࠡࡸࡤࡰࡺ࡫࠺ࠡࡘࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࡬ࡪࡰࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠊࠡࠢࠣࠤࠧࠨࠢṛ")
    if key in bstack1l1l11llll_opy_:
        bstack11lll1llll_opy_ = bstack1l1l11llll_opy_[key]
        if isinstance(bstack11lll1llll_opy_, list):
            for env_name in bstack11lll1llll_opy_:
                bstack111ll1ll1ll_opy_[env_name] = value
        else:
            bstack111ll1ll1ll_opy_[bstack11lll1llll_opy_] = value