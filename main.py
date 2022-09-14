import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGES = (
    ('a', 'exemplos/a01 - Original.bmp'),
    ('b', 'exemplos/b01 - Original.bmp')
)


def filtro_media_ingenuo(img, janela):
    (h_janela, w_janela) = janela
    meia_altura = h_janela//2
    meia_largura = w_janela//2
    altura, largura = img.shape
    img2 = img.copy()
    for y in range(meia_altura, altura - meia_altura):
        for x in range(meia_largura, largura - meia_largura):
            soma = 0.0
            for dy in range(-meia_altura, meia_altura + 1):
                for dx in range(-meia_largura, meia_largura + 1):
                    soma += img2[y + dy, x + dx]
            img[y, x] = soma/(h_janela*w_janela)


def filtro_media_separavel(img, janela):
    (h_janela, w_janela) = janela
    altura, largura = img.shape
    img2 = img.copy()
    fms_horiz(img, img2, altura, largura, h_janela, w_janela)
    fms_vert(img2, img, altura, largura, h_janela, w_janela)

def fms_horiz(entrada, saida, altura, largura, h, w):
    h2 = h//2
    w2 = w//2
    for y in range(0, altura):
        for x in range(w2, largura - w2):
            soma = 0.0
            for dx in range(-w2, w2 + 1):
                soma += entrada[y, x+dx]
            saida[y,x] = soma/(w)
            
def fms_vert(entrada, saida, altura, largura, h, w):
    h2 = h//2
    w2 = w//2
    for y in range(h2, altura - h2):
        for x in range(0, largura):
            soma = 0.0
            for dy in range(-h2, h2 + 1):
                soma += entrada[y+dy, x]
            saida[y,x] = soma/(h)


def imagem_integral(img):
    integral = np.zeros_like(img)
    altura, largura = integral.shape

    for y in range(altura):
        integral[y, 0] = img[y, 0]
        for x in range(1, largura):
            integral[y, x] = integral[y, x-1] + img[y, x]

    for y in range(1, altura):
        for x in range(largura):
            integral[y, x] = integral[y-1, x] + integral[y, x]
    
    return integral

def filtro_media_integral(img, janela):
    (h_janela, w_janela) = janela
    meia_altura = h_janela//2
    meia_largura = w_janela//2
    altura, largura = img.shape
    integral = imagem_integral(img)
    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            jh2 = min(meia_altura, y, (altura - 1) - y)
            jw2 = min(meia_largura, x, (largura-1) - x)
            br = integral[y + jh2, x + jw2]
            tr = integral[y + jh2, x - jw2 - 1] if x - jw2 - 1 >= 0 else 0
            bl = integral[y - jh2 - 1, x + jw2] if y - jh2 - 1 >= 0 else 0
            tl = integral[y - jh2 - 1, x - jw2 - 1] if y - jh2 - 1 >= 0 and x - jw2 - 1 >= 0 else 0
            soma = br - tr - bl + tl
            img[y, x] = soma/((2*jh2+1)*(2*jw2+1))


TESTES_JANELAS = (
    (5, 9),
)

TESTES_FILTROS = (
    ("Ingenuo",     filtro_media_ingenuo),
    ("Separavel",   filtro_media_separavel),
    ("Integral",    filtro_media_integral),
)

def main ():
    for nome, img in INPUT_IMAGES:
        # Abre a imagem em 3 canais BGR.
        img = cv2.imread (img, cv2.IMREAD_COLOR)
        if img is None:
            print ('Erro abrindo a imagem.\n')
            sys.exit ()

        # Convertemos para float32.
        img = img.astype (np.float32) / 255


        B, G, R = cv2.split(img)

        for nome_filtro, filtro in (TESTES_FILTROS):
            for janela in (TESTES_JANELAS):
                start_time = timeit.default_timer ()

                canais = [B.copy(), G.copy(), R.copy()]
                for canal in canais:
                    filtro(canal, janela)
                saida = cv2.merge(canais)

                (h, w) = janela

                nome_arquivo = f'{nome} - {nome_filtro} {h}x{w}'
                print (f'Tempo {nome_arquivo} : {timeit.default_timer () - start_time}')

                cv2.imwrite (f'out/{nome_arquivo}.png', saida*255)

if __name__ == '__main__':
    main ()