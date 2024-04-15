import subprocess
from pathlib import Path

for po in Path(__file__).parent.glob("**/*.po"):
    mo = Path(str(po).replace(".po", ".mo"))
    subprocess.run(["msgfmt", "-o", mo, po])
