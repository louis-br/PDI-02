import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE_PREFIX =  'a'
INPUT_IMAGE = '01 - Original.bmp'

def filtro_media_ingenuo(img, janela=3):
    meia_janela = janela//2
    janela_total = (janela)**2
    altura, largura, canais = img.shape
    for y in range(meia_janela, altura - meia_janela):
        for x in range(meia_janela, largura - meia_janela):
            for c in range(canais):
                soma = 0.0
                for dy in range(-meia_janela, meia_janela + 1):
                    for dx in range(-meia_janela, meia_janela + 1):
                        soma += img[y + dy, x + dx, c]
                img[y, x, c] = soma/janela_total
    pass

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

    filtro_media_ingenuo(img, 3)

    cv2.imwrite (f'out/{IMAGE_PREFIX}01 - Borrada.png', img*255)

    #start_time = timeit.default_timer ()
    
    #print ('Tempo: %f' % (timeit.default_timer () - start_time))
    
    #cv2.imwrite ('02 - out.png', img_out*255)


if __name__ == '__main__':
    main ()