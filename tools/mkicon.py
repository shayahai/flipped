import asyncio
from playwright.async_api import async_playwright
HTML="""<!doctype html><html><head><style>
html,body{margin:0;width:512px;height:512px;background:#3B2C22;overflow:hidden}
.f{position:absolute;inset:0;display:grid;place-items:center;font:800 300px/1 "Inter","Helvetica Neue",Arial,sans-serif;color:#F7F2EA;transform:scaleX(-1)}
.b{position:absolute;left:0;right:0;bottom:74px;text-align:center;font:500 22px/1 "Inter",Arial,sans-serif;letter-spacing:.34em;color:#A68A6D;text-indent:.34em}
</style></head><body><div class="f"><span style="margin-top:-34px">F</span></div><div class="b">BY AMKAR</div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":512,"height":512});await pg.set_content(HTML);await pg.wait_for_timeout(300)
        await pg.screenshot(path="icons/icon-512.png");await b.close()
asyncio.run(main())
from PIL import Image
im=Image.open("icons/icon-512.png").convert("RGB")
im.resize((192,192),Image.LANCZOS).save("icons/icon-192.png");im.resize((180,180),Image.LANCZOS).save("icons/apple-touch-icon.png");im.save("icons/icon-512.png")
print("icons ok")
