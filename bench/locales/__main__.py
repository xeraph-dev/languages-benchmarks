#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import subprocess
from pathlib import Path

for po in Path(__file__).parent.glob("**/*.po"):
    mo = Path(str(po).replace(".po", ".mo"))
    subprocess.run(["msgfmt", "-o", mo, po])
