from PIL import Image,ImageFont,ImageDraw
def create_image(text,color):
    # if text are in web server file ,load it else: create new file
    img = Image.new("RGB",(600,300),color)
    name = "Username : " + text
    font = ImageFont.truetype("times.ttf",40)
    width,height = font.getsize(name)
    
    draw = ImageDraw.Draw(img)
    draw.text((((600-width)/2),((300-height)/2)),name,font=font,fill="white")
    img.save("{}.png".format(text),"PNG")
    img = Image.open("{}.png".format(text))
    return img
#test
#a = create_image("Nuieasy","blue")
#a.show()