#!/usr/bin/env python3
"""Build the access-code version of the Flipped planner for GitHub Pages.

    FLIPPED_CODE=<access code> python3 build.py <app.html> <site folder>

The planner page is encrypted with a key made from the access code
(PBKDF2-SHA256 then AES-256-GCM). Only the encrypted page is written to the
site folder; the plain page and the access code are never written there.
"""
import base64, hashlib, os, sys, time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 600_000
HERE = os.path.dirname(os.path.abspath(__file__))
CDN = "https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"
PWA = ('<link rel="manifest" href="manifest.webmanifest">\n'
       '<meta name="theme-color" content="#F7F2EA">\n'
       '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">\n'
       '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
       '<meta name="mobile-web-app-capable" content="yes">\n'
       '<meta name="apple-mobile-web-app-capable" content="yes">\n'
       '<meta name="apple-mobile-web-app-title" content="Flipped">\n'
       '<meta name="apple-mobile-web-app-status-bar-style" content="default">')


def main():
    code = os.environ.get("FLIPPED_CODE", "")
    if not code:
        sys.exit("Set FLIPPED_CODE to the access code.")
    src, out = sys.argv[1], sys.argv[2]
    app = open(src, encoding="utf-8").read()
    assert app.count(CDN) == 1, "PDF library address not found once"
    app = app.replace(CDN, "pdf-lib.min.js")
    assert app.count("<title>") == 1
    app = app.replace("<title>", '<meta name="robots" content="noindex,nofollow">\n' + PWA + "\n<title>", 1)
    # A fixed salt keeps the key the same from build to build, so a device that
    # ticked "Remember on this device" stays signed in after an update. The salt
    # is public in the page either way.
    salt = hashlib.sha256(b"flipped-by-amkar gate salt v1").digest()[:16]
    key = hashlib.pbkdf2_hmac("sha256", code.encode("utf-8"), salt, ITER, 32)
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, app.encode("utf-8"), None)
    page = open(os.path.join(HERE, "loader.html"), encoding="utf-8").read()
    b64 = lambda x: base64.b64encode(x).decode("ascii")
    for k, v in (("__PWA__", PWA), ("__PAYLOAD__", b64(ct)), ("__SALT__", b64(salt)),
                 ("__IV__", b64(iv)), ("__ITER__", str(ITER))):
        assert page.count(k) == 1, k
        page = page.replace(k, v)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    stamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    sw = open(os.path.join(HERE, "sw.js"), encoding="utf-8").read().replace("__BUILD__", stamp)
    with open(os.path.join(out, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    print("built", os.path.join(out, "index.html"), len(page), "bytes; app", len(app), "bytes; build", stamp)


if __name__ == "__main__":
    main()
