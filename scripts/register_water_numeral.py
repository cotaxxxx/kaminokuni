from __future__ import annotations
import base64, hashlib, io, subprocess, zipfile
from pathlib import Path

BASELINE = {'manuscript/chapters/31-帰国/091-第91話-踏絵.md': 'fa2a8433a720e43f3c8b77af38a1846f8e47fbae', 'manuscript/chapters/31-帰国/092-第92話-ベガ島.md': 'c95627bc1d8431e06e36b0b797f5cb96b09fc88c', 'manuscript/chapters/32-上陸/093-第93話-村長.md': '827bbf8f3666b3ca44427f96fc8975facf6b87da', 'manuscript/chapters/33-発射/096-第96話-暴動.md': 'c802ccd6d654804ab39e3ee99c35d5608fe867a5'}
EXPECTED_SHA256 = {'manuscript/chapters/31-帰国/091-第91話-踏絵.md': 'de8cca72404adf28982ec78664e6749dc8733d3c77d62579443936067931e016', 'manuscript/chapters/31-帰国/092-第92話-ベガ島.md': '72a80984a1ca186234251d4989366b6a62f4ab724faaac9e686265002d5e6d20', 'manuscript/chapters/32-上陸/093-第93話-村長.md': 'b969fcce3de42850a72139377a2a920ff83fa4df787f31ec3b09129443d67ef6', 'manuscript/chapters/33-発射/096-第96話-暴動.md': '50a538171d8932779c3bab48b65b5d809e7b10bc3b09732703bd8a71c61c0e8a', 'manuscript/management/数字規則1.1適用-第91・92・93・96話-登録台帳.md': '9fa483b1fc88aa20afb80176fcbf675456bdb7eb52197eaf4c3c5ea372a7daed', 'canon/WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md': 'd045ed7b08bf0c1ea11c577b96cda47e96422d160acd3685854643196c1f56a3'}
NEW_FILES = [
    "manuscript/management/数字規則1.1適用-第91・92・93・96話-登録台帳.md",
    "canon/WATER_NUMERAL_RULE_APPLICATION_REGISTERED_CANON.md",
]
CHUNKS = [Path(f"scripts/.water_payload_{i}") for i in range(4)]
TEMP_FILES = CHUNKS + [
    Path("scripts/register_water_numeral.py"),
    Path(".github/workflows/register-water-numeral.yml"),
]

def git_blob_sha(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], text=True).strip()

for path, expected in BASELINE.items():
    actual = git_blob_sha(path)
    if actual != expected:
        raise RuntimeError(f"Baseline mismatch for {path}: {actual} != {expected}")

for path in NEW_FILES:
    if Path(path).exists():
        raise RuntimeError(f"New file already exists: {path}")

payload = base64.b64decode("".join(p.read_text(encoding="ascii") for p in CHUNKS))
with zipfile.ZipFile(io.BytesIO(payload)) as zf:
    names = zf.namelist()
    if set(names) != set(EXPECTED_SHA256):
        raise RuntimeError(f"Unexpected archive paths: {names}")
    for name in names:
        target = Path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = zf.read(name)
        if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256[name]:
            raise RuntimeError(f"Payload checksum mismatch: {name}")
        target.write_bytes(data)

for path, expected in EXPECTED_SHA256.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"Written checksum mismatch: {path}")

for path in TEMP_FILES:
    path.unlink()
