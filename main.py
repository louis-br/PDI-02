import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE_PREFIX =  'a'
INPUT_IMAGE = '01 - Original.bmp'


def main ():
    INPUT_IMAGE_PREFIX = sys.argv[1] if len(sys.argv) > 1 else INPUT_IMAGE_PREFIX
    INPUT_IMAGE = INPUT_IMAGE_PREFIX + INPUT_IMAGE

    # Abre a imagem em 3 canais BGR.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # Convertemos para float32.
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    #img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    #cv2.imwrite ('01 - out.png', img*255)

    #start_time = timeit.default_timer ()
    
    #print ('Tempo: %f' % (timeit.default_timer () - start_time))
    
    #cv2.imwrite ('02 - out.png', img_out*255)


if __name__ == '__main__':
    main ()