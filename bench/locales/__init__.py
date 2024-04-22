#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import pathlib
from gettext import translation

translations = translation("bench", pathlib.Path(__file__).parent, fallback=True)
translations.install()
_ = translations.gettext
