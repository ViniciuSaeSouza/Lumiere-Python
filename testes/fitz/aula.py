import pytesseract
import cv2

#C:\Users\Saes\AppData\Local\Programs\Tesseract-OCR

caminho = r"C:\Users\Saes\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = caminho
#passo 1: Ler a imagem
imagem = cv2.imread("contapdf.png")

# passo 2: pedir pro tesseract extrair o texto da imagem
texto = pytesseract.image_to_string(imagem, lang="por")

print(texto)
