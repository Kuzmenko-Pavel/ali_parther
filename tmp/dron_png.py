import math
from PIL import Image
import base64

js_body = """
var ifrm = document.createElement("iframe");
ifrm.setAttribute("srcdoc", "<p>Приветули!</p><p>Что скажеш насчет кода?</p><p>Кто меня нарисовал?</p>");
ifrm.style.width = "640px";
ifrm.style.height = "480px";        
document.body.innerHTML = '';
document.body.appendChild(ifrm);
"""
encodedBytes = base64.b64encode(js_body.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")
js_code = "data:text/javascript;base64," + encodedStr

js_code_len = len(js_code)

background = Image.open("main_image.png")
bg_w, bg_h = background.size

img_w = bg_w
img_h = bg_h + math.ceil(float(js_code_len) / bg_w)
print()

img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
pixels = img.load()

i=0
for y in range(0, img_h):
    if y < bg_h:
        continue
    for x in range(0, img_w):
        if i < js_code_len:
            symbol = ord(js_code[i])
            pixels[x, y] = (210, 171, 104, symbol)
        i += 1

img.paste(background, (0, 0))
img.save("telochka.png", "PNG")




# img = Image.new("RGB", (iHeight, iWidth), (0, 0, 0, 0))
# img_w, img_h = img.size
# pixels = img.load()
#
# i=0
# for y in range(0, iHeight):
#     for x in range(0, iWidth):e
#         if i < js_code_len:
#             symbol = ord(js_code[i])
#             pixels[x, y] = (symbol, symbol, symbol)
#         i += 1
#
# offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
# background.paste(img, offset)
# background.save('out.png')
#
# img.save("dron1.png", "PNG")
