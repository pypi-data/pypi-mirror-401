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
from bstack_utils.constants import (bstack1ll1l1l1_opy_, bstack1ll1l1l1l1_opy_, bstack1lll111lll_opy_,
                                    bstack11l1l1l11ll_opy_, bstack11l1l11l1l1_opy_, bstack11l11ll11l1_opy_, bstack11l1l11l11l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1111l1111_opy_, bstack1l1111l11l_opy_
from bstack_utils.proxy import bstack1l1111lll1_opy_, bstack111111l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11lllll1_opy_
from bstack_utils.bstack111l11ll_opy_ import bstack11lllll11l_opy_
from browserstack_sdk._version import __version__
bstack11llllll_opy_ = Config.bstack1llll1111_opy_()
logger = bstack11lllll1_opy_.get_logger(__name__, bstack11lllll1_opy_.bstack1lll1ll11ll_opy_())
bstack11l1l1l11l_opy_ = bstack11lllll1_opy_.bstack1l11llllll_opy_(__name__)
def bstack11l1lll1ll1_opy_(config):
    return config[bstack1l11l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᮴")]
def bstack11l1lllll11_opy_(config):
    return config[bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᮵")]
def bstack11ll1lll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111llllll11_opy_(obj):
    values = []
    bstack111l1l1ll11_opy_ = re.compile(bstack1l11l1l_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ᮶"), re.I)
    for key in obj.keys():
        if bstack111l1l1ll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111lllll111_opy_(config):
    tags = []
    tags.extend(bstack111llllll11_opy_(os.environ))
    tags.extend(bstack111llllll11_opy_(config))
    return tags
def bstack11l1111llll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l1l11ll1_opy_(bstack11l1111lll1_opy_):
    if not bstack11l1111lll1_opy_:
        return bstack1l11l1l_opy_ (u"ࠫࠬ᮷")
    return bstack1l11l1l_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨ᮸").format(bstack11l1111lll1_opy_.name, bstack11l1111lll1_opy_.email)
def bstack11ll1111lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l1lll11l_opy_ = repo.common_dir
        info = {
            bstack1l11l1l_opy_ (u"ࠨࡳࡩࡣࠥ᮹"): repo.head.commit.hexsha,
            bstack1l11l1l_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᮺ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l11l1l_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᮻ"): repo.active_branch.name,
            bstack1l11l1l_opy_ (u"ࠤࡷࡥ࡬ࠨᮼ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l11l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᮽ"): bstack111l1l11ll1_opy_(repo.head.commit.committer),
            bstack1l11l1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᮾ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l11l1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᮿ"): bstack111l1l11ll1_opy_(repo.head.commit.author),
            bstack1l11l1l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᯀ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l11l1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᯁ"): repo.head.commit.message,
            bstack1l11l1l_opy_ (u"ࠣࡴࡲࡳࡹࠨᯂ"): repo.git.rev_parse(bstack1l11l1l_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᯃ")),
            bstack1l11l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᯄ"): bstack111l1lll11l_opy_,
            bstack1l11l1l_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᯅ"): subprocess.check_output([bstack1l11l1l_opy_ (u"ࠧ࡭ࡩࡵࠤᯆ"), bstack1l11l1l_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᯇ"), bstack1l11l1l_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᯈ")]).strip().decode(
                bstack1l11l1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᯉ")),
            bstack1l11l1l_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᯊ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l11l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᯋ"): repo.git.rev_list(
                bstack1l11l1l_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᯌ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1111l1l1_opy_ = []
        for remote in remotes:
            bstack111ll111lll_opy_ = {
                bstack1l11l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯍ"): remote.name,
                bstack1l11l1l_opy_ (u"ࠨࡵࡳ࡮ࠥᯎ"): remote.url,
            }
            bstack11l1111l1l1_opy_.append(bstack111ll111lll_opy_)
        bstack111l1lllll1_opy_ = {
            bstack1l11l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᯏ"): bstack1l11l1l_opy_ (u"ࠣࡩ࡬ࡸࠧᯐ"),
            **info,
            bstack1l11l1l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᯑ"): bstack11l1111l1l1_opy_
        }
        bstack111l1lllll1_opy_ = bstack111llllllll_opy_(bstack111l1lllll1_opy_)
        return bstack111l1lllll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l11l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᯒ").format(err))
        return {}
def bstack11l11111111_opy_(bstack111llll111l_opy_=None):
    bstack1l11l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࡣ࡯ࡰࡾࠦࡦࡰࡴࡰࡥࡹࡺࡥࡥࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡻࡳࡦࠢࡦࡥࡸ࡫ࡳࠡࡨࡲࡶࠥ࡫ࡡࡤࡪࠣࡪࡴࡲࡤࡦࡴࠣ࡭ࡳࠦࡴࡩࡧࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡔ࡯࡯ࡧ࠽ࠤࡒࡵ࡮ࡰ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩ࠮ࠣࡹࡸ࡫ࡳࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡡ࡯ࡴ࠰ࡪࡩࡹࡩࡷࡥࠪࠬࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡋ࡭ࡱࡶࡼࠤࡱ࡯ࡳࡵࠢ࡞ࡡ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡲࡴࠦࡳࡰࡷࡵࡧࡪࡹࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧ࠰ࠥࡸࡥࡵࡷࡵࡲࡸ࡛ࠦ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡴࡦࡺࡨࡴ࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࠢࡩࡳࡱࡪࡥࡳࡵࠣࡸࡴࠦࡡ࡯ࡣ࡯ࡽࡿ࡫ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡭࡫ࡶࡸ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡥ࡫ࡦࡸࡸ࠲ࠠࡦࡣࡦ࡬ࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡧࠠࡧࡱ࡯ࡨࡪࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᯓ")
    if bstack111llll111l_opy_ is None:
        bstack111llll111l_opy_ = [os.getcwd()]
    elif isinstance(bstack111llll111l_opy_, list) and len(bstack111llll111l_opy_) == 0:
        return []
    results = []
    for folder in bstack111llll111l_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l11l1l_opy_ (u"ࠧࡌ࡯࡭ࡦࡨࡶࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥᯔ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l11l1l_opy_ (u"ࠨࡰࡳࡋࡧࠦᯕ"): bstack1l11l1l_opy_ (u"ࠢࠣᯖ"),
                bstack1l11l1l_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᯗ"): [],
                bstack1l11l1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᯘ"): [],
                bstack1l11l1l_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥᯙ"): bstack1l11l1l_opy_ (u"ࠦࠧᯚ"),
                bstack1l11l1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨᯛ"): [],
                bstack1l11l1l_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᯜ"): bstack1l11l1l_opy_ (u"ࠢࠣᯝ"),
                bstack1l11l1l_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣᯞ"): bstack1l11l1l_opy_ (u"ࠤࠥᯟ"),
                bstack1l11l1l_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨᯠ"): bstack1l11l1l_opy_ (u"ࠦࠧᯡ")
            }
            bstack111ll11111l_opy_ = repo.active_branch.name
            bstack11l111l1ll1_opy_ = repo.head.commit
            result[bstack1l11l1l_opy_ (u"ࠧࡶࡲࡊࡦࠥᯢ")] = bstack11l111l1ll1_opy_.hexsha
            bstack111ll11l11l_opy_ = _11l111ll1l1_opy_(repo)
            logger.debug(bstack1l11l1l_opy_ (u"ࠨࡂࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠿ࠦࠢᯣ") + str(bstack111ll11l11l_opy_) + bstack1l11l1l_opy_ (u"ࠢࠣᯤ"))
            if bstack111ll11l11l_opy_:
                try:
                    bstack11l11111ll1_opy_ = repo.git.diff(bstack1l11l1l_opy_ (u"ࠣ࠯࠰ࡲࡦࡳࡥ࠮ࡱࡱࡰࡾࠨᯥ"), bstack1ll1lll1l1l_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃ᯦ࠢ")).split(bstack1l11l1l_opy_ (u"ࠪࡠࡳ࠭ᯧ"))
                    logger.debug(bstack1l11l1l_opy_ (u"ࠦࡈ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡧ࡫ࡴࡸࡧࡨࡲࠥࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠥࡧ࡮ࡥࠢࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠿ࠦࠢᯨ") + str(bstack11l11111ll1_opy_) + bstack1l11l1l_opy_ (u"ࠧࠨᯩ"))
                    result[bstack1l11l1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᯪ")] = [f.strip() for f in bstack11l11111ll1_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1lll1l1l_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᯫ")))
                except Exception:
                    logger.debug(bstack1l11l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡢࡳࡣࡱࡧ࡭ࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠱ࠤࡋࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡲࡦࡥࡨࡲࡹࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠣᯬ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l11l1l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᯭ")] = _11l1111ll1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l11l1l_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᯮ")] = _11l1111ll1l_opy_(commits[:5])
            bstack111lll1l1l1_opy_ = set()
            bstack111l1ll11l1_opy_ = []
            for commit in commits:
                logger.debug(bstack1l11l1l_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲ࡯ࡴ࠻ࠢࠥᯯ") + str(commit.message) + bstack1l11l1l_opy_ (u"ࠧࠨᯰ"))
                bstack111ll1l1ll1_opy_ = commit.author.name if commit.author else bstack1l11l1l_opy_ (u"ࠨࡕ࡯࡭ࡱࡳࡼࡴࠢᯱ")
                bstack111lll1l1l1_opy_.add(bstack111ll1l1ll1_opy_)
                bstack111l1ll11l1_opy_.append({
                    bstack1l11l1l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥ᯲ࠣ"): commit.message.strip(),
                    bstack1l11l1l_opy_ (u"ࠣࡷࡶࡩࡷࠨ᯳"): bstack111ll1l1ll1_opy_
                })
            result[bstack1l11l1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥ᯴")] = list(bstack111lll1l1l1_opy_)
            result[bstack1l11l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦ᯵")] = bstack111l1ll11l1_opy_
            result[bstack1l11l1l_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦ᯶")] = bstack11l111l1ll1_opy_.committed_datetime.strftime(bstack1l11l1l_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࠢ᯷"))
            if (not result[bstack1l11l1l_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ᯸")] or result[bstack1l11l1l_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣ᯹")].strip() == bstack1l11l1l_opy_ (u"ࠣࠤ᯺")) and bstack11l111l1ll1_opy_.message:
                bstack111l1l11l1l_opy_ = bstack11l111l1ll1_opy_.message.strip().splitlines()
                result[bstack1l11l1l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ᯻")] = bstack111l1l11l1l_opy_[0] if bstack111l1l11l1l_opy_ else bstack1l11l1l_opy_ (u"ࠥࠦ᯼")
                if len(bstack111l1l11l1l_opy_) > 2:
                    result[bstack1l11l1l_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ᯽")] = bstack1l11l1l_opy_ (u"ࠬࡢ࡮ࠨ᯾").join(bstack111l1l11l1l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l11l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤ࠭࡬࡯࡭ࡦࡨࡶ࠿ࠦࡻࡾࠫ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ᯿").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111llll11ll_opy_(result)
    ]
    return filtered_results
def _111llll11ll_opy_(result):
    bstack1l11l1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡧ࡯ࡴࡪࡸࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡧࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡵࡸࡰࡹࠦࡩࡴࠢࡹࡥࡱ࡯ࡤࠡࠪࡱࡳࡳ࠳ࡥ࡮ࡲࡷࡽࠥ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠤࡦࡴࡤࠡࡣࡸࡸ࡭ࡵࡲࡴࠫ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᰀ")
    return (
        isinstance(result.get(bstack1l11l1l_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᰁ"), None), list)
        and len(result[bstack1l11l1l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᰂ")]) > 0
        and isinstance(result.get(bstack1l11l1l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᰃ"), None), list)
        and len(result[bstack1l11l1l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᰄ")]) > 0
    )
def _11l111ll1l1_opy_(repo):
    bstack1l11l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡲࡺࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶ࡫ࡩࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡶࡪࡶ࡯ࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢ࡫ࡥࡷࡪࡣࡰࡦࡨࡨࠥࡴࡡ࡮ࡧࡶࠤࡦࡴࡤࠡࡹࡲࡶࡰࠦࡷࡪࡶ࡫ࠤࡦࡲ࡬ࠡࡘࡆࡗࠥࡶࡲࡰࡸ࡬ࡨࡪࡸࡳ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡨࡲࡢࡰࡦ࡬ࠥ࡯ࡦࠡࡲࡲࡷࡸ࡯ࡢ࡭ࡧ࠯ࠤࡪࡲࡳࡦࠢࡑࡳࡳ࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᰅ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111lll11l1l_opy_ = origin.refs[bstack1l11l1l_opy_ (u"࠭ࡈࡆࡃࡇࠫᰆ")]
            target = bstack111lll11l1l_opy_.reference.name
            if target.startswith(bstack1l11l1l_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨᰇ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l11l1l_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩᰈ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _11l1111ll1l_opy_(commits):
    bstack1l11l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡊࡩࡹࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡧࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᰉ")
    bstack11l11111ll1_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111lll11l11_opy_ in diff:
                        if bstack111lll11l11_opy_.a_path:
                            bstack11l11111ll1_opy_.add(bstack111lll11l11_opy_.a_path)
                        if bstack111lll11l11_opy_.b_path:
                            bstack11l11111ll1_opy_.add(bstack111lll11l11_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l11111ll1_opy_)
def bstack111llllllll_opy_(bstack111l1lllll1_opy_):
    bstack11l1111l1ll_opy_ = bstack111ll111111_opy_(bstack111l1lllll1_opy_)
    if bstack11l1111l1ll_opy_ and bstack11l1111l1ll_opy_ > bstack11l1l1l11ll_opy_:
        bstack111llll1l1l_opy_ = bstack11l1111l1ll_opy_ - bstack11l1l1l11ll_opy_
        bstack111ll1lll1l_opy_ = bstack111ll1111l1_opy_(bstack111l1lllll1_opy_[bstack1l11l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᰊ")], bstack111llll1l1l_opy_)
        bstack111l1lllll1_opy_[bstack1l11l1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᰋ")] = bstack111ll1lll1l_opy_
        logger.info(bstack1l11l1l_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢᰌ")
                    .format(bstack111ll111111_opy_(bstack111l1lllll1_opy_) / 1024))
    return bstack111l1lllll1_opy_
def bstack111ll111111_opy_(bstack11lll11l11_opy_):
    try:
        if bstack11lll11l11_opy_:
            bstack111lll1ll11_opy_ = json.dumps(bstack11lll11l11_opy_)
            bstack111ll1lllll_opy_ = sys.getsizeof(bstack111lll1ll11_opy_)
            return bstack111ll1lllll_opy_
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨᰍ").format(e))
    return -1
def bstack111ll1111l1_opy_(field, bstack111ll1lll11_opy_):
    try:
        bstack11l111l11l1_opy_ = len(bytes(bstack11l1l11l1l1_opy_, bstack1l11l1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᰎ")))
        bstack111llll1ll1_opy_ = bytes(field, bstack1l11l1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᰏ"))
        bstack111lll11lll_opy_ = len(bstack111llll1ll1_opy_)
        bstack11l11111l1l_opy_ = ceil(bstack111lll11lll_opy_ - bstack111ll1lll11_opy_ - bstack11l111l11l1_opy_)
        if bstack11l11111l1l_opy_ > 0:
            bstack111l1ll111l_opy_ = bstack111llll1ll1_opy_[:bstack11l11111l1l_opy_].decode(bstack1l11l1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᰐ"), errors=bstack1l11l1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪᰑ")) + bstack11l1l11l1l1_opy_
            return bstack111l1ll111l_opy_
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤᰒ").format(e))
    return field
def bstack11l1111l1_opy_():
    env = os.environ
    if (bstack1l11l1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᰓ") in env and len(env[bstack1l11l1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᰔ")]) > 0) or (
            bstack1l11l1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᰕ") in env and len(env[bstack1l11l1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᰖ")]) > 0):
        return {
            bstack1l11l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᰗ"): bstack1l11l1l_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦᰘ"),
            bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᰙ"): env.get(bstack1l11l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᰚ")),
            bstack1l11l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰛ"): env.get(bstack1l11l1l_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤᰜ")),
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰝ"): env.get(bstack1l11l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᰞ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠥࡇࡎࠨᰟ")) == bstack1l11l1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᰠ") and bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢᰡ"))):
        return {
            bstack1l11l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰢ"): bstack1l11l1l_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤᰣ"),
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰤ"): env.get(bstack1l11l1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᰥ")),
            bstack1l11l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰦ"): env.get(bstack1l11l1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣᰧ")),
            bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰨ"): env.get(bstack1l11l1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤᰩ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠢࡄࡋࠥᰪ")) == bstack1l11l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨᰫ") and bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤᰬ"))):
        return {
            bstack1l11l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᰭ"): bstack1l11l1l_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢᰮ"),
            bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᰯ"): env.get(bstack1l11l1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨᰰ")),
            bstack1l11l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰱ"): env.get(bstack1l11l1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᰲ")),
            bstack1l11l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰳ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᰴ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠦࡈࡏࠢᰵ")) == bstack1l11l1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᰶ") and env.get(bstack1l11l1l_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋ᰷ࠢ")) == bstack1l11l1l_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤ᰸"):
        return {
            bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᰹"): bstack1l11l1l_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦ᰺"),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᰻"): None,
            bstack1l11l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᰼"): None,
            bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᰽"): None
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤ᰾")) and env.get(bstack1l11l1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥ᰿")):
        return {
            bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᱀"): bstack1l11l1l_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧ᱁"),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᱂"): env.get(bstack1l11l1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤ᱃")),
            bstack1l11l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᱄"): None,
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᱅"): env.get(bstack1l11l1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᱆"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠣࡅࡌࠦ᱇")) == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᱈") and bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤ᱉"))):
        return {
            bstack1l11l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᱊"): bstack1l11l1l_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦ᱋"),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᱌"): env.get(bstack1l11l1l_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥᱍ")),
            bstack1l11l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᱎ"): None,
            bstack1l11l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᱏ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᱐"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠦࡈࡏࠢ᱑")) == bstack1l11l1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ᱒") and bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤ᱓"))):
        return {
            bstack1l11l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱔"): bstack1l11l1l_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦ᱕"),
            bstack1l11l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᱖"): env.get(bstack1l11l1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤ᱗")),
            bstack1l11l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᱘"): env.get(bstack1l11l1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᱙")),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᱚ"): env.get(bstack1l11l1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᱛ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠣࡅࡌࠦᱜ")) == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᱝ") and bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨᱞ"))):
        return {
            bstack1l11l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᱟ"): bstack1l11l1l_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧᱠ"),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᱡ"): env.get(bstack1l11l1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦᱢ")),
            bstack1l11l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᱣ"): env.get(bstack1l11l1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᱤ")),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᱥ"): env.get(bstack1l11l1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢᱦ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠧࡉࡉࠣᱧ")) == bstack1l11l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᱨ") and bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥᱩ"))):
        return {
            bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᱪ"): bstack1l11l1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧᱫ"),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᱬ"): env.get(bstack1l11l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᱭ")),
            bstack1l11l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᱮ"): env.get(bstack1l11l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣᱯ")) or env.get(bstack1l11l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᱰ")),
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱱ"): env.get(bstack1l11l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᱲ"))
        }
    if bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᱳ"))):
        return {
            bstack1l11l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᱴ"): bstack1l11l1l_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧᱵ"),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᱶ"): bstack1l11l1l_opy_ (u"ࠢࡼࡿࡾࢁࠧᱷ").format(env.get(bstack1l11l1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᱸ")), env.get(bstack1l11l1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩᱹ"))),
            bstack1l11l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᱺ"): env.get(bstack1l11l1l_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥᱻ")),
            bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᱼ"): env.get(bstack1l11l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᱽ"))
        }
    if bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤ᱾"))):
        return {
            bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᱿"): bstack1l11l1l_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦᲀ"),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᲁ"): bstack1l11l1l_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥᲂ").format(env.get(bstack1l11l1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫᲃ")), env.get(bstack1l11l1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧᲄ")), env.get(bstack1l11l1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨᲅ")), env.get(bstack1l11l1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬᲆ"))),
            bstack1l11l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᲇ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᲈ")),
            bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᲉ"): env.get(bstack1l11l1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᲊ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢ᲋")) and env.get(bstack1l11l1l_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ᲌")):
        return {
            bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᲍"): bstack1l11l1l_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦ᲎"),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᲏"): bstack1l11l1l_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢᲐ").format(env.get(bstack1l11l1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᲑ")), env.get(bstack1l11l1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫᲒ")), env.get(bstack1l11l1l_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧᲓ"))),
            bstack1l11l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᲔ"): env.get(bstack1l11l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᲕ")),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᲖ"): env.get(bstack1l11l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᲗ"))
        }
    if any([env.get(bstack1l11l1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᲘ")), env.get(bstack1l11l1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᲙ")), env.get(bstack1l11l1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᲚ"))]):
        return {
            bstack1l11l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᲛ"): bstack1l11l1l_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤᲜ"),
            bstack1l11l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᲝ"): env.get(bstack1l11l1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᲞ")),
            bstack1l11l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᲟ"): env.get(bstack1l11l1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᲠ")),
            bstack1l11l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᲡ"): env.get(bstack1l11l1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᲢ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᲣ")):
        return {
            bstack1l11l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᲤ"): bstack1l11l1l_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦᲥ"),
            bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᲦ"): env.get(bstack1l11l1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣᲧ")),
            bstack1l11l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᲨ"): env.get(bstack1l11l1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢᲩ")),
            bstack1l11l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᲪ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᲫ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧᲬ")) or env.get(bstack1l11l1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢᲭ")):
        return {
            bstack1l11l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᲮ"): bstack1l11l1l_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣᲯ"),
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᲰ"): env.get(bstack1l11l1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᲱ")),
            bstack1l11l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᲲ"): bstack1l11l1l_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦᲳ") if env.get(bstack1l11l1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢᲴ")) else None,
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᲵ"): env.get(bstack1l11l1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧᲶ"))
        }
    if any([env.get(bstack1l11l1l_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᲷ")), env.get(bstack1l11l1l_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᲸ")), env.get(bstack1l11l1l_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᲹ"))]):
        return {
            bstack1l11l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᲺ"): bstack1l11l1l_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦ᲻"),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᲼"): None,
            bstack1l11l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᲽ"): env.get(bstack1l11l1l_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧᲾ")),
            bstack1l11l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᲿ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᳀"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢ᳁")):
        return {
            bstack1l11l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᳂"): bstack1l11l1l_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤ᳃"),
            bstack1l11l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᳄"): env.get(bstack1l11l1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᳅")),
            bstack1l11l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᳆"): bstack1l11l1l_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦ᳇").format(env.get(bstack1l11l1l_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ᳈"))) if env.get(bstack1l11l1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣ᳉")) else None,
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᳊"): env.get(bstack1l11l1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᳋"))
        }
    if bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤ᳌"))):
        return {
            bstack1l11l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳍"): bstack1l11l1l_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦ᳎"),
            bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᳏"): env.get(bstack1l11l1l_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤ᳐")),
            bstack1l11l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᳑"): env.get(bstack1l11l1l_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥ᳒")),
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᳓"): env.get(bstack1l11l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇ᳔ࠦ"))
        }
    if bstack11lll1l1l_opy_(env.get(bstack1l11l1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖ᳕ࠦ"))):
        return {
            bstack1l11l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᳖"): bstack1l11l1l_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨ᳗"),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᳘"): bstack1l11l1l_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽ᳙ࠣ").format(env.get(bstack1l11l1l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬ᳚")), env.get(bstack1l11l1l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭᳛")), env.get(bstack1l11l1l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆ᳜ࠪ"))),
            bstack1l11l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᳝"): env.get(bstack1l11l1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝᳞ࠢ")),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᳟ࠧ"): env.get(bstack1l11l1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢ᳠"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠣࡅࡌࠦ᳡")) == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫᳢ࠢ") and env.get(bstack1l11l1l_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎ᳣ࠥ")) == bstack1l11l1l_opy_ (u"ࠦ࠶ࠨ᳤"):
        return {
            bstack1l11l1l_opy_ (u"ࠧࡴࡡ࡮ࡧ᳥ࠥ"): bstack1l11l1l_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨ᳦"),
            bstack1l11l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᳧ࠥ"): bstack1l11l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀ᳨ࠦ").format(env.get(bstack1l11l1l_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭ᳩ"))),
            bstack1l11l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᳪ"): None,
            bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᳫ"): None,
        }
    if env.get(bstack1l11l1l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣᳬ")):
        return {
            bstack1l11l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᳭ࠦ"): bstack1l11l1l_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤᳮ"),
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᳯ"): None,
            bstack1l11l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᳰ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦᳱ")),
            bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᳲ"): env.get(bstack1l11l1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᳳ"))
        }
    if any([env.get(bstack1l11l1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤ᳴")), env.get(bstack1l11l1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢᳵ")), env.get(bstack1l11l1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨᳶ")), env.get(bstack1l11l1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥ᳷"))]):
        return {
            bstack1l11l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᳸"): bstack1l11l1l_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢ᳹"),
            bstack1l11l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᳺ"): None,
            bstack1l11l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᳻"): env.get(bstack1l11l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᳼")) or None,
            bstack1l11l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᳽"): env.get(bstack1l11l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᳾"), 0)
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᳿")):
        return {
            bstack1l11l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᴀ"): bstack1l11l1l_opy_ (u"ࠧࡍ࡯ࡄࡆࠥᴁ"),
            bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᴂ"): None,
            bstack1l11l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᴃ"): env.get(bstack1l11l1l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᴄ")),
            bstack1l11l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴅ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤᴆ"))
        }
    if env.get(bstack1l11l1l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᴇ")):
        return {
            bstack1l11l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᴈ"): bstack1l11l1l_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤᴉ"),
            bstack1l11l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᴊ"): env.get(bstack1l11l1l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᴋ")),
            bstack1l11l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᴌ"): env.get(bstack1l11l1l_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᴍ")),
            bstack1l11l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴎ"): env.get(bstack1l11l1l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᴏ"))
        }
    return {bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᴐ"): None}
def get_host_info():
    return {
        bstack1l11l1l_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤᴑ"): platform.node(),
        bstack1l11l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥᴒ"): platform.system(),
        bstack1l11l1l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᴓ"): platform.machine(),
        bstack1l11l1l_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᴔ"): platform.version(),
        bstack1l11l1l_opy_ (u"ࠦࡦࡸࡣࡩࠤᴕ"): platform.architecture()[0]
    }
def bstack111l111l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111llll1111_opy_():
    if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ᴖ")):
        return bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᴗ")
    return bstack1l11l1l_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭ᴘ")
def bstack111l1l111ll_opy_(driver):
    info = {
        bstack1l11l1l_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴙ"): driver.capabilities,
        bstack1l11l1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ᴚ"): driver.session_id,
        bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᴛ"): driver.capabilities.get(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᴜ"), None),
        bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᴝ"): driver.capabilities.get(bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᴞ"), None),
        bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᴟ"): driver.capabilities.get(bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᴠ"), None),
        bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᴡ"):driver.capabilities.get(bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᴢ"), None),
    }
    if bstack111llll1111_opy_() == bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᴣ"):
        if bstack1l1ll1l111_opy_():
            info[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᴤ")] = bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᴥ")
        elif driver.capabilities.get(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᴦ"), {}).get(bstack1l11l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᴧ"), False):
            info[bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᴨ")] = bstack1l11l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᴩ")
        else:
            info[bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᴪ")] = bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᴫ")
    return info
def bstack1l1ll1l111_opy_():
    if bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᴬ")):
        return True
    if bstack11lll1l1l_opy_(os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᴭ"), None)):
        return True
    return False
def bstack111l1l11lll_opy_(bstack11l1111l111_opy_, url, response, headers=None, data=None):
    bstack1l11l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡄࡸ࡭ࡱࡪࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡱࡵࡧࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࡷࠥ࡬࡯ࡳࠢࡵࡩࡶࡻࡥࡴࡶ࠲ࡶࡪࡹࡰࡰࡰࡶࡩࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡷࡵࡦࡵࡷࡣࡹࡿࡰࡦ࠼ࠣࡌ࡙࡚ࡐࠡ࡯ࡨࡸ࡭ࡵࡤࠡࠪࡊࡉ࡙࠲ࠠࡑࡑࡖࡘ࠱ࠦࡥࡵࡥ࠱࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡵࡳ࡮࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸ࡛ࠥࡒࡍ࠱ࡨࡲࡩࡶ࡯ࡪࡰࡷࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡳࡧࡰࡥࡤࡶࠣࡪࡷࡵ࡭ࠡࡴࡨࡵࡺ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡭࡫ࡡࡥࡧࡵࡷ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡩࡧࡤࡨࡪࡸࡳࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨࡦࡺࡡ࠻ࠢࡕࡩࡶࡻࡥࡴࡶࠣࡎࡘࡕࡎࠡࡦࡤࡸࡦࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡆࡰࡴࡰࡥࡹࡺࡥࡥࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫ࠠࡸ࡫ࡷ࡬ࠥࡸࡥࡲࡷࡨࡷࡹࠦࡡ࡯ࡦࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡪࡡࡵࡣࠍࠤࠥࠦࠠࠣࠤࠥᴮ")
    bstack111ll1l1l11_opy_ = {
        bstack1l11l1l_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥᴯ"): headers,
        bstack1l11l1l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᴰ"): bstack11l1111l111_opy_.upper(),
        bstack1l11l1l_opy_ (u"ࠦࡦ࡭ࡥ࡯ࡶࠥᴱ"): None,
        bstack1l11l1l_opy_ (u"ࠧ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠢᴲ"): url,
        bstack1l11l1l_opy_ (u"ࠨࡪࡴࡱࡱࠦᴳ"): data
    }
    try:
        bstack111lll11111_opy_ = response.json()
    except Exception:
        bstack111lll11111_opy_ = response.text
    bstack111ll1ll11l_opy_ = {
        bstack1l11l1l_opy_ (u"ࠢࡣࡱࡧࡽࠧᴴ"): bstack111lll11111_opy_,
        bstack1l11l1l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࡄࡱࡧࡩࠧᴵ"): response.status_code
    }
    return {
        bstack1l11l1l_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᴶ"): bstack111ll1l1l11_opy_,
        bstack1l11l1l_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᴷ"): bstack111ll1ll11l_opy_
    }
def bstack11l111ll11_opy_(bstack11l1111l111_opy_, url, data, config):
    headers = config.get(bstack1l11l1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᴸ"), None)
    proxies = bstack1l1111lll1_opy_(config, url)
    auth = config.get(bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᴹ"), None)
    response = requests.request(
            bstack11l1111l111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack111l1l11lll_opy_(bstack11l1111l111_opy_, url, response, headers, data)
        bstack11l1l1l11l_opy_.debug(json.dumps(log_message, separators=(bstack1l11l1l_opy_ (u"࠭ࠬࠨᴺ"), bstack1l11l1l_opy_ (u"ࠧ࠻ࠩᴻ"))))
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࡻࡾࠤᴼ").format(e))
    return response
def bstack1ll111llll_opy_(bstack1lllll11_opy_, size):
    bstack11l111l111_opy_ = []
    while len(bstack1lllll11_opy_) > size:
        bstack1l1l1llll_opy_ = bstack1lllll11_opy_[:size]
        bstack11l111l111_opy_.append(bstack1l1l1llll_opy_)
        bstack1lllll11_opy_ = bstack1lllll11_opy_[size:]
    bstack11l111l111_opy_.append(bstack1lllll11_opy_)
    return bstack11l111l111_opy_
def bstack11l111ll11l_opy_(message, bstack111ll1llll1_opy_=False):
    os.write(1, bytes(message, bstack1l11l1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᴽ")))
    os.write(1, bytes(bstack1l11l1l_opy_ (u"ࠪࡠࡳ࠭ᴾ"), bstack1l11l1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᴿ")))
    if bstack111ll1llll1_opy_:
        with open(bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫᵀ") + os.environ[bstack1l11l1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᵁ")] + bstack1l11l1l_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬᵂ"), bstack1l11l1l_opy_ (u"ࠨࡣࠪᵃ")) as f:
            f.write(message + bstack1l11l1l_opy_ (u"ࠩ࡟ࡲࠬᵄ"))
def bstack1l1l11ll1ll_opy_():
    return os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᵅ")].lower() == bstack1l11l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᵆ")
def bstack11ll11ll1l_opy_():
    return bstack1111l11111_opy_().replace(tzinfo=None).isoformat() + bstack1l11l1l_opy_ (u"ࠬࡠࠧᵇ")
def bstack111lll11ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l11l1l_opy_ (u"࡚࠭ࠨᵈ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l11l1l_opy_ (u"࡛ࠧࠩᵉ")))).total_seconds() * 1000
def bstack111ll1ll111_opy_(timestamp):
    return bstack111l1l1lll1_opy_(timestamp).isoformat() + bstack1l11l1l_opy_ (u"ࠨ࡜ࠪᵊ")
def bstack111ll1l11ll_opy_(bstack111ll1ll1l1_opy_):
    date_format = bstack1l11l1l_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧᵋ")
    bstack111lll1l11l_opy_ = datetime.datetime.strptime(bstack111ll1ll1l1_opy_, date_format)
    return bstack111lll1l11l_opy_.isoformat() + bstack1l11l1l_opy_ (u"ࠪ࡞ࠬᵌ")
def bstack111ll111l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᵍ")
    else:
        return bstack1l11l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᵎ")
def bstack11lll1l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l11l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᵏ")
def bstack11l111111ll_opy_(val):
    return val.__str__().lower() == bstack1l11l1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᵐ")
def error_handler(bstack111l1llll1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l1llll1l_opy_ as e:
                print(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᵑ").format(func.__name__, bstack111l1llll1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l1l1l1ll_opy_(bstack111lllllll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lllllll1_opy_(cls, *args, **kwargs)
            except bstack111l1llll1l_opy_ as e:
                print(bstack1l11l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᵒ").format(bstack111lllllll1_opy_.__name__, bstack111l1llll1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l1l1l1ll_opy_
    else:
        return decorator
def bstack111111lll_opy_(bstack1lllllll1ll_opy_):
    if os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᵓ")) is not None:
        return bstack11lll1l1l_opy_(os.getenv(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᵔ")))
    if bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᵕ") in bstack1lllllll1ll_opy_ and bstack11l111111ll_opy_(bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᵖ")]):
        return False
    if bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᵗ") in bstack1lllllll1ll_opy_ and bstack11l111111ll_opy_(bstack1lllllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᵘ")]):
        return False
    return True
def bstack1111ll11_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l111l1l1l_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤᵙ"), None)
        return bstack11l111l1l1l_opy_ is None or bstack11l111l1l1l_opy_ == bstack1l11l1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᵚ")
    except Exception as e:
        return False
def bstack1ll1111l1_opy_(hub_url, CONFIG):
    if bstack1ll1l1ll11_opy_() <= version.parse(bstack1l11l1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫᵛ")):
        if hub_url:
            return bstack1l11l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᵜ") + hub_url + bstack1l11l1l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥᵝ")
        return bstack1ll1l1l1l1_opy_
    if hub_url:
        return bstack1l11l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᵞ") + hub_url + bstack1l11l1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᵟ")
    return bstack1lll111lll_opy_
def bstack111l1ll1lll_opy_():
    return isinstance(os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᵠ")), str)
def bstack111llll1l1_opy_(url):
    return urlparse(url).hostname
def bstack1ll1ll1ll_opy_(hostname):
    for bstack111l1l1ll_opy_ in bstack1ll1l1l1_opy_:
        regex = re.compile(bstack111l1l1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111llll11l1_opy_(bstack111lll111ll_opy_, file_name, logger):
    bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠪࢂࠬᵡ")), bstack111lll111ll_opy_)
    try:
        if not os.path.exists(bstack1ll1lll1_opy_):
            os.makedirs(bstack1ll1lll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠫࢃ࠭ᵢ")), bstack111lll111ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l11l1l_opy_ (u"ࠬࡽࠧᵣ")):
                pass
            with open(file_path, bstack1l11l1l_opy_ (u"ࠨࡷࠬࠤᵤ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1111l1111_opy_.format(str(e)))
def bstack111llll1l11_opy_(file_name, key, value, logger):
    file_path = bstack111llll11l1_opy_(bstack1l11l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᵥ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1lll_opy_ = json.load(open(file_path, bstack1l11l1l_opy_ (u"ࠨࡴࡥࠫᵦ")))
        else:
            bstack1lll1lll_opy_ = {}
        bstack1lll1lll_opy_[key] = value
        with open(file_path, bstack1l11l1l_opy_ (u"ࠤࡺ࠯ࠧᵧ")) as outfile:
            json.dump(bstack1lll1lll_opy_, outfile)
def bstack11lll1l11_opy_(file_name, logger):
    file_path = bstack111llll11l1_opy_(bstack1l11l1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᵨ"), file_name, logger)
    bstack1lll1lll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l11l1l_opy_ (u"ࠫࡷ࠭ᵩ")) as bstack11l1lll11l_opy_:
            bstack1lll1lll_opy_ = json.load(bstack11l1lll11l_opy_)
    return bstack1lll1lll_opy_
def bstack1lll1l1ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᵪ") + file_path + bstack1l11l1l_opy_ (u"࠭ࠠࠨᵫ") + str(e))
def bstack1ll1l1ll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l11l1l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᵬ")
def bstack1lllll111l_opy_(config):
    if bstack1l11l1l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᵭ") in config:
        del (config[bstack1l11l1l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᵮ")])
        return False
    if bstack1ll1l1ll11_opy_() < version.parse(bstack1l11l1l_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᵯ")):
        return False
    if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l11l1l_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᵰ")):
        return True
    if bstack1l11l1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᵱ") in config and config[bstack1l11l1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᵲ")] is False:
        return False
    else:
        return True
def bstack1ll111l111_opy_(args_list, bstack111lll1lll1_opy_):
    index = -1
    for value in bstack111lll1lll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll111111l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll111111l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111l1ll11l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111l1ll11l_opy_ = bstack111l1ll11l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l11l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᵳ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᵴ"), exception=exception)
    def bstack1lllll1ll11_opy_(self):
        if self.result != bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᵵ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l11l1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᵶ") in self.exception_type:
            return bstack1l11l1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᵷ")
        return bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᵸ")
    def bstack111l1ll1l1l_opy_(self):
        if self.result != bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᵹ"):
            return None
        if self.bstack111l1ll11l_opy_:
            return self.bstack111l1ll11l_opy_
        return bstack111l1ll11ll_opy_(self.exception)
def bstack111l1ll11ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1llllll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll1ll11ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11111111_opy_(config, logger):
    try:
        import playwright
        bstack111ll11llll_opy_ = playwright.__file__
        bstack111ll1l111l_opy_ = os.path.split(bstack111ll11llll_opy_)
        bstack111l1l1l111_opy_ = bstack111ll1l111l_opy_[0] + bstack1l11l1l_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᵺ")
        os.environ[bstack1l11l1l_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᵻ")] = bstack111111l1l_opy_(config)
        with open(bstack111l1l1l111_opy_, bstack1l11l1l_opy_ (u"ࠩࡵࠫᵼ")) as f:
            bstack1l1ll1llll_opy_ = f.read()
            bstack11l111l11ll_opy_ = bstack1l11l1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᵽ")
            bstack111ll1l1lll_opy_ = bstack1l1ll1llll_opy_.find(bstack11l111l11ll_opy_)
            if bstack111ll1l1lll_opy_ == -1:
              process = subprocess.Popen(bstack1l11l1l_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᵾ"), shell=True, cwd=bstack111ll1l111l_opy_[0])
              process.wait()
              bstack111l1ll1111_opy_ = bstack1l11l1l_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᵿ")
              bstack111ll11l111_opy_ = bstack1l11l1l_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᶀ")
              bstack11l111l1l11_opy_ = bstack1l1ll1llll_opy_.replace(bstack111l1ll1111_opy_, bstack111ll11l111_opy_)
              with open(bstack111l1l1l111_opy_, bstack1l11l1l_opy_ (u"ࠧࡸࠩᶁ")) as f:
                f.write(bstack11l111l1l11_opy_)
    except Exception as e:
        logger.error(bstack1l1111l11l_opy_.format(str(e)))
def bstack1ll1ll1l11_opy_():
  try:
    bstack111lll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᶂ"))
    bstack111lllll11l_opy_ = []
    if os.path.exists(bstack111lll1ll1l_opy_):
      with open(bstack111lll1ll1l_opy_) as f:
        bstack111lllll11l_opy_ = json.load(f)
      os.remove(bstack111lll1ll1l_opy_)
    return bstack111lllll11l_opy_
  except:
    pass
  return []
def bstack1l11ll1111_opy_(bstack1ll11lll11_opy_):
  try:
    bstack111lllll11l_opy_ = []
    bstack111lll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᶃ"))
    if os.path.exists(bstack111lll1ll1l_opy_):
      with open(bstack111lll1ll1l_opy_) as f:
        bstack111lllll11l_opy_ = json.load(f)
    bstack111lllll11l_opy_.append(bstack1ll11lll11_opy_)
    with open(bstack111lll1ll1l_opy_, bstack1l11l1l_opy_ (u"ࠪࡻࠬᶄ")) as f:
        json.dump(bstack111lllll11l_opy_, f)
  except:
    pass
def bstack111llll11_opy_(logger, bstack111llllll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᶅ"), bstack1l11l1l_opy_ (u"ࠬ࠭ᶆ"))
    if test_name == bstack1l11l1l_opy_ (u"࠭ࠧᶇ"):
        test_name = threading.current_thread().__dict__.get(bstack1l11l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᶈ"), bstack1l11l1l_opy_ (u"ࠨࠩᶉ"))
    bstack111l1l1l1l1_opy_ = bstack1l11l1l_opy_ (u"ࠩ࠯ࠤࠬᶊ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111llllll1l_opy_:
        bstack1l11l1111_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᶋ"), bstack1l11l1l_opy_ (u"ࠫ࠵࠭ᶌ"))
        bstack1lll1ll1l_opy_ = {bstack1l11l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᶍ"): test_name, bstack1l11l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᶎ"): bstack111l1l1l1l1_opy_, bstack1l11l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᶏ"): bstack1l11l1111_opy_}
        bstack11l111l111l_opy_ = []
        bstack111l1lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᶐ"))
        if os.path.exists(bstack111l1lll111_opy_):
            with open(bstack111l1lll111_opy_) as f:
                bstack11l111l111l_opy_ = json.load(f)
        bstack11l111l111l_opy_.append(bstack1lll1ll1l_opy_)
        with open(bstack111l1lll111_opy_, bstack1l11l1l_opy_ (u"ࠩࡺࠫᶑ")) as f:
            json.dump(bstack11l111l111l_opy_, f)
    else:
        bstack1lll1ll1l_opy_ = {bstack1l11l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᶒ"): test_name, bstack1l11l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᶓ"): bstack111l1l1l1l1_opy_, bstack1l11l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᶔ"): str(multiprocessing.current_process().name)}
        if bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᶕ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lll1ll1l_opy_)
  except Exception as e:
      logger.warn(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᶖ").format(e))
def bstack111llllll1_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫᶗ"))
    try:
      bstack111lll1l1ll_opy_ = []
      bstack1lll1ll1l_opy_ = {bstack1l11l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᶘ"): test_name, bstack1l11l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᶙ"): error_message, bstack1l11l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᶚ"): index}
      bstack111l1l1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᶛ"))
      if os.path.exists(bstack111l1l1ll1l_opy_):
          with open(bstack111l1l1ll1l_opy_) as f:
              bstack111lll1l1ll_opy_ = json.load(f)
      bstack111lll1l1ll_opy_.append(bstack1lll1ll1l_opy_)
      with open(bstack111l1l1ll1l_opy_, bstack1l11l1l_opy_ (u"࠭ࡷࠨᶜ")) as f:
          json.dump(bstack111lll1l1ll_opy_, f)
    except Exception as e:
      logger.warn(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᶝ").format(e))
    return
  bstack111lll1l1ll_opy_ = []
  bstack1lll1ll1l_opy_ = {bstack1l11l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶞ"): test_name, bstack1l11l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᶟ"): error_message, bstack1l11l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᶠ"): index}
  bstack111l1l1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᶡ"))
  lock_file = bstack111l1l1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫᶢ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l1l1ll1l_opy_):
          with open(bstack111l1l1ll1l_opy_, bstack1l11l1l_opy_ (u"࠭ࡲࠨᶣ")) as f:
              content = f.read().strip()
              if content:
                  bstack111lll1l1ll_opy_ = json.load(open(bstack111l1l1ll1l_opy_))
      bstack111lll1l1ll_opy_.append(bstack1lll1ll1l_opy_)
      with open(bstack111l1l1ll1l_opy_, bstack1l11l1l_opy_ (u"ࠧࡸࠩᶤ")) as f:
          json.dump(bstack111lll1l1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l11l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣᶥ").format(e))
def bstack1llll11111_opy_(bstack1ll111l1ll_opy_, name, logger):
  try:
    bstack1lll1ll1l_opy_ = {bstack1l11l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᶦ"): name, bstack1l11l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᶧ"): bstack1ll111l1ll_opy_, bstack1l11l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᶨ"): str(threading.current_thread()._name)}
    return bstack1lll1ll1l_opy_
  except Exception as e:
    logger.warn(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᶩ").format(e))
  return
def bstack111lll1111l_opy_():
    return platform.system() == bstack1l11l1l_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧᶪ")
def bstack1ll1ll11l1_opy_(bstack111l1l1l11l_opy_, config, logger):
    bstack111ll11ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l1l1l11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᶫ").format(e))
    return bstack111ll11ll11_opy_
def bstack111lllll1l1_opy_(bstack11l1111111l_opy_, bstack11l111l1lll_opy_):
    bstack111l1lll1ll_opy_ = version.parse(bstack11l1111111l_opy_)
    bstack11l11111lll_opy_ = version.parse(bstack11l111l1lll_opy_)
    if bstack111l1lll1ll_opy_ > bstack11l11111lll_opy_:
        return 1
    elif bstack111l1lll1ll_opy_ < bstack11l11111lll_opy_:
        return -1
    else:
        return 0
def bstack1111l11111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1l1lll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111lll1llll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l111ll11_opy_(options, framework, config, bstack11lll1ll1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l11l1l_opy_ (u"ࠨࡩࡨࡸࠬᶬ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11ll111ll_opy_ = caps.get(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᶭ"))
    bstack111ll11l1l1_opy_ = True
    bstack11l11lll_opy_ = os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᶮ")]
    bstack1ll111ll1ll_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᶯ"), False)
    if bstack1ll111ll1ll_opy_:
        bstack1lll111ll11_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᶰ"), {})
        bstack1lll111ll11_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᶱ")] = os.getenv(bstack1l11l1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᶲ"))
        bstack11ll1111111_opy_ = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᶳ"), bstack1l11l1l_opy_ (u"ࠩࡾࢁࠬᶴ"))).get(bstack1l11l1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᶵ"))
    if bstack11l111111ll_opy_(caps.get(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᶶ"))) or bstack11l111111ll_opy_(caps.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᶷ"))):
        bstack111ll11l1l1_opy_ = False
    if bstack1lllll111l_opy_({bstack1l11l1l_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᶸ"): bstack111ll11l1l1_opy_}):
        bstack11ll111ll_opy_ = bstack11ll111ll_opy_ or {}
        bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᶹ")] = bstack111lll1llll_opy_(framework)
        bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᶺ")] = bstack1l1l11ll1ll_opy_()
        bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᶻ")] = bstack11l11lll_opy_
        bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᶼ")] = bstack11lll1ll1_opy_
        if bstack1ll111ll1ll_opy_:
            bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᶽ")] = bstack1ll111ll1ll_opy_
            bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᶾ")] = bstack1lll111ll11_opy_
            bstack11ll111ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶿ")][bstack1l11l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᷀")] = bstack11ll1111111_opy_
        if getattr(options, bstack1l11l1l_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᷁"), None):
            options.set_capability(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵ᷂ࠪ"), bstack11ll111ll_opy_)
        else:
            options[bstack1l11l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᷃")] = bstack11ll111ll_opy_
    else:
        if getattr(options, bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ᷄"), None):
            options.set_capability(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᷅"), bstack111lll1llll_opy_(framework))
            options.set_capability(bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᷆"), bstack1l1l11ll1ll_opy_())
            options.set_capability(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᷇"), bstack11l11lll_opy_)
            options.set_capability(bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᷈"), bstack11lll1ll1_opy_)
            if bstack1ll111ll1ll_opy_:
                options.set_capability(bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᷉"), bstack1ll111ll1ll_opy_)
                options.set_capability(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ᷊ࠩ"), bstack1lll111ll11_opy_)
                options.set_capability(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᷋"), bstack11ll1111111_opy_)
        else:
            options[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᷌")] = bstack111lll1llll_opy_(framework)
            options[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᷍")] = bstack1l1l11ll1ll_opy_()
            options[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥ᷎ࠩ")] = bstack11l11lll_opy_
            options[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱ᷏ࠩ")] = bstack11lll1ll1_opy_
            if bstack1ll111ll1ll_opy_:
                options[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᷐")] = bstack1ll111ll1ll_opy_
                options[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᷑")] = bstack1lll111ll11_opy_
                options[bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᷒")][bstack1l11l1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᷓ")] = bstack11ll1111111_opy_
    return options
def bstack111ll1l1l1l_opy_(bstack11l111111l1_opy_, framework):
    bstack11lll1ll1_opy_ = bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣᷔ"))
    if bstack11l111111l1_opy_ and len(bstack11l111111l1_opy_.split(bstack1l11l1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᷕ"))) > 1:
        ws_url = bstack11l111111l1_opy_.split(bstack1l11l1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᷖ"))[0]
        if bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᷗ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111lll111l1_opy_ = json.loads(urllib.parse.unquote(bstack11l111111l1_opy_.split(bstack1l11l1l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᷘ"))[1]))
            bstack111lll111l1_opy_ = bstack111lll111l1_opy_ or {}
            bstack11l11lll_opy_ = os.environ[bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᷙ")]
            bstack111lll111l1_opy_[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᷚ")] = str(framework) + str(__version__)
            bstack111lll111l1_opy_[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᷛ")] = bstack1l1l11ll1ll_opy_()
            bstack111lll111l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᷜ")] = bstack11l11lll_opy_
            bstack111lll111l1_opy_[bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᷝ")] = bstack11lll1ll1_opy_
            bstack11l111111l1_opy_ = bstack11l111111l1_opy_.split(bstack1l11l1l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᷞ"))[0] + bstack1l11l1l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᷟ") + urllib.parse.quote(json.dumps(bstack111lll111l1_opy_))
    return bstack11l111111l1_opy_
def bstack1l1l111111_opy_():
    global bstack1ll1lllll1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1lllll1_opy_ = BrowserType.connect
    return bstack1ll1lllll1_opy_
def bstack111lllll_opy_(framework_name):
    global bstack1ll1ll1l1_opy_
    bstack1ll1ll1l1_opy_ = framework_name
    return framework_name
def bstack11ll1ll1_opy_(self, *args, **kwargs):
    global bstack1ll1lllll1_opy_
    try:
        global bstack1ll1ll1l1_opy_
        if bstack1l11l1l_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᷠ") in kwargs:
            kwargs[bstack1l11l1l_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᷡ")] = bstack111ll1l1l1l_opy_(
                kwargs.get(bstack1l11l1l_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᷢ"), None),
                bstack1ll1ll1l1_opy_
            )
    except Exception as e:
        logger.error(bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢᷣ").format(str(e)))
    return bstack1ll1lllll1_opy_(self, *args, **kwargs)
def bstack111l1l11l11_opy_(bstack111l1l1llll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1111lll1_opy_(bstack111l1l1llll_opy_, bstack1l11l1l_opy_ (u"ࠣࠤᷤ"))
        if proxies and proxies.get(bstack1l11l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᷥ")):
            parsed_url = urlparse(proxies.get(bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᷦ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᷧ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᷨ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l11l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᷩ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l11l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᷪ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1l1111_opy_(bstack111l1l1llll_opy_):
    bstack111lllll1ll_opy_ = {
        bstack11l1l11l11l_opy_[bstack111l1ll1ll1_opy_]: bstack111l1l1llll_opy_[bstack111l1ll1ll1_opy_]
        for bstack111l1ll1ll1_opy_ in bstack111l1l1llll_opy_
        if bstack111l1ll1ll1_opy_ in bstack11l1l11l11l_opy_
    }
    bstack111lllll1ll_opy_[bstack1l11l1l_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᷫ")] = bstack111l1l11l11_opy_(bstack111l1l1llll_opy_, bstack11llllll_opy_.get_property(bstack1l11l1l_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᷬ")))
    bstack111ll1111ll_opy_ = [element.lower() for element in bstack11l11ll11l1_opy_]
    bstack11l1111ll11_opy_(bstack111lllll1ll_opy_, bstack111ll1111ll_opy_)
    return bstack111lllll1ll_opy_
def bstack11l1111ll11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l11l1l_opy_ (u"ࠥ࠮࠯࠰ࠪࠣᷭ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1111ll11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1111ll11_opy_(item, keys)
def bstack1l1l1ll11ll_opy_():
    bstack11l1111l11l_opy_ = [os.environ.get(bstack1l11l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡎࡒࡅࡔࡡࡇࡍࡗࠨᷮ")), os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠧࢄࠢᷯ")), bstack1l11l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᷰ")), os.path.join(bstack1l11l1l_opy_ (u"ࠧ࠰ࡶࡰࡴࠬᷱ"), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᷲ"))]
    for path in bstack11l1111l11l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l11l1l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᷳ") + str(path) + bstack1l11l1l_opy_ (u"ࠥࠫࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨᷴ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l11l1l_opy_ (u"ࠦࡌ࡯ࡶࡪࡰࡪࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠢࡩࡳࡷࠦࠧࠣ᷵") + str(path) + bstack1l11l1l_opy_ (u"ࠧ࠭ࠢ᷶"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l11l1l_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨ᷷") + str(path) + bstack1l11l1l_opy_ (u"ࠢࠨࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡬ࡦࡹࠠࡵࡪࡨࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶ࠲᷸ࠧ"))
            else:
                logger.debug(bstack1l11l1l_opy_ (u"ࠣࡅࡵࡩࡦࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ᷹ࠡࠩࠥ") + str(path) + bstack1l11l1l_opy_ (u"ࠤࠪࠤࡼ࡯ࡴࡩࠢࡺࡶ࡮ࡺࡥࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲ࠳ࠨ᷺"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l11l1l_opy_ (u"ࠥࡓࡵ࡫ࡲࡢࡶ࡬ࡳࡳࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥࠢࡩࡳࡷࠦࠧࠣ᷻") + str(path) + bstack1l11l1l_opy_ (u"ࠦࠬ࠴ࠢ᷼"))
            return path
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡻࡰࠡࡨ࡬ࡰࡪࠦࠧࡼࡲࡤࡸ࡭ࢃࠧ࠻᷽ࠢࠥ") + str(e) + bstack1l11l1l_opy_ (u"ࠨࠢ᷾"))
    logger.debug(bstack1l11l1l_opy_ (u"ࠢࡂ࡮࡯ࠤࡵࡧࡴࡩࡵࠣࡪࡦ࡯࡬ࡦࡦ࠱᷿ࠦ"))
    return None
@measure(event_name=EVENTS.bstack11l11lll1l1_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack1lll1l11l1l_opy_(binary_path, bstack1ll1lll1lll_opy_, bs_config):
    logger.debug(bstack1l11l1l_opy_ (u"ࠣࡅࡸࡶࡷ࡫࡮ࡵࠢࡆࡐࡎࠦࡐࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦ࠽ࠤࢀࢃࠢḀ").format(binary_path))
    bstack11l111l1111_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪḁ")
    bstack111ll11lll1_opy_ = {
        bstack1l11l1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨḂ"): __version__,
        bstack1l11l1l_opy_ (u"ࠦࡴࡹࠢḃ"): platform.system(),
        bstack1l11l1l_opy_ (u"ࠧࡵࡳࡠࡣࡵࡧ࡭ࠨḄ"): platform.machine(),
        bstack1l11l1l_opy_ (u"ࠨࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠦḅ"): bstack1l11l1l_opy_ (u"ࠧ࠱ࠩḆ"),
        bstack1l11l1l_opy_ (u"ࠣࡵࡧ࡯ࡤࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠢḇ"): bstack1l11l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩḈ")
    }
    bstack111l1ll1l11_opy_(bstack111ll11lll1_opy_)
    try:
        if binary_path:
            if bstack111lll1111l_opy_():
                bstack111ll11lll1_opy_[bstack1l11l1l_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨḉ")] = subprocess.check_output([binary_path, bstack1l11l1l_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧḊ")]).strip().decode(bstack1l11l1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫḋ"))
            else:
                bstack111ll11lll1_opy_[bstack1l11l1l_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫḌ")] = subprocess.check_output([binary_path, bstack1l11l1l_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣḍ")], stderr=subprocess.DEVNULL).strip().decode(bstack1l11l1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧḎ"))
        response = requests.request(
            bstack1l11l1l_opy_ (u"ࠩࡊࡉ࡙࠭ḏ"),
            url=bstack11lllll11l_opy_(bstack11l1l111111_opy_),
            headers=None,
            auth=(bs_config[bstack1l11l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬḐ")], bs_config[bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧḑ")]),
            json=None,
            params=bstack111ll11lll1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l11l1l_opy_ (u"ࠬࡻࡲ࡭ࠩḒ") in data.keys() and bstack1l11l1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬḓ") in data.keys():
            logger.debug(bstack1l11l1l_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣḔ").format(bstack111ll11lll1_opy_[bstack1l11l1l_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ḕ")]))
            if bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬḖ") in os.environ:
                logger.debug(bstack1l11l1l_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑࠦࡩࡴࠢࡶࡩࡹࠨḗ"))
                data[bstack1l11l1l_opy_ (u"ࠫࡺࡸ࡬ࠨḘ")] = os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨḙ")]
            bstack11l11111l11_opy_ = bstack111ll11l1ll_opy_(data[bstack1l11l1l_opy_ (u"࠭ࡵࡳ࡮ࠪḚ")], bstack1ll1lll1lll_opy_)
            bstack11l111l1111_opy_ = os.path.join(bstack1ll1lll1lll_opy_, bstack11l11111l11_opy_)
            os.chmod(bstack11l111l1111_opy_, 0o777) # bstack111ll1l11l1_opy_ permission
            return bstack11l111l1111_opy_
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢḛ").format(e))
    return binary_path
def bstack111l1ll1l11_opy_(bstack111ll11lll1_opy_):
    try:
        if bstack1l11l1l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧḜ") not in bstack111ll11lll1_opy_[bstack1l11l1l_opy_ (u"ࠩࡲࡷࠬḝ")].lower():
            return
        if os.path.exists(bstack1l11l1l_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧḞ")):
            with open(bstack1l11l1l_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨḟ"), bstack1l11l1l_opy_ (u"ࠧࡸࠢḠ")) as f:
                bstack111ll111ll1_opy_ = {}
                for line in f:
                    if bstack1l11l1l_opy_ (u"ࠨ࠽ࠣḡ") in line:
                        key, value = line.rstrip().split(bstack1l11l1l_opy_ (u"ࠢ࠾ࠤḢ"), 1)
                        bstack111ll111ll1_opy_[key] = value.strip(bstack1l11l1l_opy_ (u"ࠨࠤ࡟ࠫࠬḣ"))
                bstack111ll11lll1_opy_[bstack1l11l1l_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩḤ")] = bstack111ll111ll1_opy_.get(bstack1l11l1l_opy_ (u"ࠥࡍࡉࠨḥ"), bstack1l11l1l_opy_ (u"ࠦࠧḦ"))
        elif os.path.exists(bstack1l11l1l_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦḧ")):
            bstack111ll11lll1_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭Ḩ")] = bstack1l11l1l_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧḩ")
    except Exception as e:
        logger.debug(bstack1l11l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥḪ") + e)
@measure(event_name=EVENTS.bstack11l1l11ll1l_opy_, stage=STAGE.bstack11l1llllll_opy_)
def bstack111ll11l1ll_opy_(bstack111llll1lll_opy_, bstack111ll1l1111_opy_):
    logger.debug(bstack1l11l1l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦḫ") + str(bstack111llll1lll_opy_) + bstack1l11l1l_opy_ (u"ࠥࠦḬ"))
    zip_path = os.path.join(bstack111ll1l1111_opy_, bstack1l11l1l_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥḭ"))
    bstack11l11111l11_opy_ = bstack1l11l1l_opy_ (u"ࠬ࠭Ḯ")
    with requests.get(bstack111llll1lll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l11l1l_opy_ (u"ࠨࡷࡣࠤḯ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l11l1l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤḰ"))
    with zipfile.ZipFile(zip_path, bstack1l11l1l_opy_ (u"ࠨࡴࠪḱ")) as zip_ref:
        bstack111l1lll1l1_opy_ = zip_ref.namelist()
        if len(bstack111l1lll1l1_opy_) > 0:
            bstack11l11111l11_opy_ = bstack111l1lll1l1_opy_[0] # bstack111ll11ll1l_opy_ bstack11l11ll1l11_opy_ will be bstack111l1llll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111ll1l1111_opy_)
        logger.debug(bstack1l11l1l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣḲ") + str(bstack111ll1l1111_opy_) + bstack1l11l1l_opy_ (u"ࠥࠫࠧḳ"))
    os.remove(zip_path)
    return bstack11l11111l11_opy_
def get_cli_dir():
    bstack11l111ll111_opy_ = bstack1l1l1ll11ll_opy_()
    if bstack11l111ll111_opy_:
        bstack1ll1lll1lll_opy_ = os.path.join(bstack11l111ll111_opy_, bstack1l11l1l_opy_ (u"ࠦࡨࡲࡩࠣḴ"))
        if not os.path.exists(bstack1ll1lll1lll_opy_):
            os.makedirs(bstack1ll1lll1lll_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1lll1lll_opy_
    else:
        raise FileNotFoundError(bstack1l11l1l_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣḵ"))
def bstack1ll11llll11_opy_(bstack1ll1lll1lll_opy_):
    bstack1l11l1l_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥḶ")
    bstack111ll1ll1ll_opy_ = [
        os.path.join(bstack1ll1lll1lll_opy_, f)
        for f in os.listdir(bstack1ll1lll1lll_opy_)
        if os.path.isfile(os.path.join(bstack1ll1lll1lll_opy_, f)) and f.startswith(bstack1l11l1l_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣḷ"))
    ]
    if len(bstack111ll1ll1ll_opy_) > 0:
        return max(bstack111ll1ll1ll_opy_, key=os.path.getmtime) # get bstack111lll1l111_opy_ binary
    return bstack1l11l1l_opy_ (u"ࠣࠤḸ")
def bstack11ll1111l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1lllll1l1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1lllll1l1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l11l1l1l_opy_(data, keys, default=None):
    bstack1l11l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡥ࡫࡫࡬ࡺࠢࡪࡩࡹࠦࡡࠡࡰࡨࡷࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡦࡺࡡ࠻ࠢࡗ࡬ࡪࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡹࡵࠠࡵࡴࡤࡺࡪࡸࡳࡦ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠ࡬ࡧࡼࡷ࠿ࠦࡁࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢ࡮ࡩࡾࡹ࠯ࡪࡰࡧ࡭ࡨ࡫ࡳࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡧࡩࡥࡺࡲࡴ࠻࡙ࠢࡥࡱࡻࡥࠡࡶࡲࠤࡷ࡫ࡴࡶࡴࡱࠤ࡮࡬ࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡵࡩࡹࡻࡲ࡯࠼ࠣࡘ࡭࡫ࠠࡷࡣ࡯ࡹࡪࠦࡡࡵࠢࡷ࡬ࡪࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡢࡶ࡫࠰ࠥࡵࡲࠡࡦࡨࡪࡦࡻ࡬ࡵࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠯ࠌࠣࠤࠥࠦࠢࠣࠤḹ")
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
def bstack111llll1ll_opy_(bstack111ll111l1l_opy_, key, value):
    bstack1l11l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡹࡵࡲࡦࠢࡆࡐࡎࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹࠠ࡮ࡣࡳࡴ࡮ࡴࡧࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡬ࡪࡡࡨࡲࡻࡥࡶࡢࡴࡶࡣࡲࡧࡰ࠻ࠢࡇ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࠡ࡯ࡤࡴࡵ࡯࡮ࡨࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࡰ࡫ࡹ࠻ࠢࡎࡩࡾࠦࡦࡳࡱࡰࠤࡈࡒࡉࡠࡅࡄࡔࡘࡥࡔࡐࡡࡆࡓࡓࡌࡉࡈࠌࠣࠤࠥࠦࠠࠡࠢࠣࡺࡦࡲࡵࡦ࠼࡚ࠣࡦࡲࡵࡦࠢࡩࡶࡴࡳࠠࡤࡱࡰࡱࡦࡴࡤࠡ࡮࡬ࡲࡪࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠌࠣࠤࠥࠦࠢࠣࠤḺ")
    if key in bstack11l1llll1_opy_:
        bstack1llll111l_opy_ = bstack11l1llll1_opy_[key]
        if isinstance(bstack1llll111l_opy_, list):
            for env_name in bstack1llll111l_opy_:
                bstack111ll111l1l_opy_[env_name] = value
        else:
            bstack111ll111l1l_opy_[bstack1llll111l_opy_] = value