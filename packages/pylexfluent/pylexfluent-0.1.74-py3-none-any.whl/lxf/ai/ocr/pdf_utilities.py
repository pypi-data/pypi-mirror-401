import os
import cv2
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import img2pdf

import glob

def empty_folder(path:str) :
    files = glob.glob(path)
    for f in files:
        os.remove(f)

def remove_highligth(source:str, target:str)-> tuple[int,str] :
    """
    Docstring for remove highligh from images of PDF and return a PDF images with the b&w converted images 
    
    :param source: Description
    :type source: str
    :param target: Description
    :type target: str
    :return: Description
    :rtype: tuple[int, str]
    """
    if os.path.exists(source) is False :
        return -1 , f"{source} est introuvable"
    
    images = convert_from_path(source)
    if images == None : 
        return -2 , f"Aucune image extraite du fichier {source}"
    if os.path.exists("./data/temp") is False : 
        os.makedirs("./data/temp")
        
    imgs=[]
    for i in range(len(images)):    
    ## Save image to file
            img_path=f"./data/temp/page_{i}.jpeg"
            images[i].save(img_path,'JPEG')          
            image = cv2.imread(img_path)
            # Convert to Gray
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)            
            gray_path= f"./data/temp/gray_page_{i}.png"
            cv2.imwrite(gray_path,gray)
            # display(gray_path)
            min=155
            max=255
            source=gray
            thresh, img_bw = cv2.threshold(source,min,max,cv2.THRESH_BINARY)
            black_white_path =f"./data/temp/bw_page{i}.png"
            cv2.imwrite(black_white_path, img_bw)
            #display(black_white_path)
            imgs.append(black_white_path)            
            os.remove(img_path)
            
    # Save all converted images in a pdf
    # opening from filename
    # specify paper size (A4)
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_A4 = img2pdf.get_layout_fun(a4inpt)
    with open(target,"wb+") as f:
        f.write(img2pdf.convert(imgs,layout_fun=layout_A4))
    # remove all tempory file
    empty_folder("./data/temp/*.png")
    if os.path.exists(target) is True :
        return 0, target
    return -3, f"Le fichier {target} n'a pu être créé"