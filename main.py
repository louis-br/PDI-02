import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE_PREFIX =  'a'
INPUT_IMAGE = '01 - Original.bmp'

def filtro_media_ingenuo(img, janela):
    meia_janela = janela//2
    janela_total = (janela)**2
    altura, largura = img.shape
    img2 = img.copy()
    for y in range(meia_janela, altura - meia_janela):
        for x in range(meia_janela, largura - meia_janela):
            soma = 0.0
            for dy in range(-meia_janela, meia_janela + 1):
                for dx in range(-meia_janela, meia_janela + 1):
                    soma += img2[y + dy, x + dx]
            img[y, x] = soma/janela_total


def filtro_media_separavel(img, janela):
    meia_janela = janela//2
    altura, largura = img.shape
    img2 = img.copy()
    fms_horiz(img, img2, meia_janela, altura, largura, janela)
    fms_vert(img2, img, meia_janela, altura, largura, janela)

def fms_horiz(entrada, saida, meia_janela, altura, largura, janela):
    for y in range(meia_janela, altura - meia_janela):
        for x in range(meia_janela, largura - meia_janela):
            soma = 0.0
            for dy in range(-meia_janela, meia_janela + 1):
                soma += entrada[y+dy, x]
            saida[y,x] = soma/janela

def fms_vert(entrada, saida, meia_janela, altura, largura, janela):
    for y in range(meia_janela, altura - meia_janela):
        for x in range(meia_janela, largura - meia_janela):
            soma = 0.0
            for dx in range(-meia_janela, meia_janela + 1):
                soma += entrada[y, x+dx]
            saida[y,x] = soma/janela


def main ():
    IMAGE_PREFIX = sys.argv[1] if len(sys.argv) > 1 else INPUT_IMAGE_PREFIX
    INPUT = IMAGE_PREFIX + INPUT_IMAGE

    # Abre a imagem em 3 canais BGR.
    img = cv2.imread (f'exemplos/{INPUT}', cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # Convertemos para float32.
    img = img.astype (np.float32) / 255

    B, G, R = cv2.split(img)

    for canal in (B, G, R):
        filtro_media_ingenuo(canal, 7)

    img = cv2.merge([B, G, R])

    cv2.imwrite (f'out/{IMAGE_PREFIX}01 - Borrada.png', img*255)

    #start_time = timeit.default_timer ()
    
    #print ('Tempo: %f' % (timeit.default_timer () - start_time))
    
    #cv2.imwrite ('02 - out.png', img_out*255)


if __name__ == '__main__':
    main ()