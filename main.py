import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGES = (
    ('a', 'exemplos/a01 - Original.bmp'),
    ('b', 'exemplos/b01 - Original.bmp')
)


def filtro_media_ingenuo(img, janela):
    h_jan, w_jan = (v//2 for v in janela)
    area_janela = janela[0]*janela[1]
    altura, largura = img.shape
    img2 = img.copy()
    for y in range(h_jan, altura - h_jan):
        for x in range(w_jan, largura - w_jan):
            soma = 0.0
            for dy in range(-h_jan, h_jan + 1):
                for dx in range(-w_jan, w_jan + 1):
                    soma += img2[y + dy, x + dx]
            img[y, x] = soma/area_janela


def filtro_media_separavel(img, janela):
    altura, largura = img.shape
    img2 = img.copy()
    fms_horiz(img, img2, altura, largura, janela[1])
    fms_vert(img2, img, altura, largura, janela[0])

def fms_horiz(entrada, saida, altura, largura, janela):
    w_jan = janela//2
    for y in range(0, altura):
        for x in range(w_jan, largura - w_jan):
            soma = 0.0
            for dx in range(-w_jan, w_jan + 1):
                soma += entrada[y, x+dx]
            saida[y,x] = soma/janela
            
def fms_vert(entrada, saida, altura, largura, janela):
    h_jan = janela//2
    for y in range(h_jan, altura - h_jan):
        for x in range(0, largura):
            soma = 0.0
            for dy in range(-h_jan, h_jan + 1):
                soma += entrada[y+dy, x]
            saida[y,x] = soma/janela


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
    h_jan, w_jan = (v//2 for v in janela)
    altura, largura = img.shape
    integral = imagem_integral(img)
    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            hj = min(h_jan, y, (altura-1)  - y)
            wj = min(w_jan, x, (largura-1) - x)

            br = integral[y + hj, x + wj]
            tr = integral[y + hj, x - wj - 1] if x - wj - 1 >= 0 else 0
            bl = integral[y - hj - 1, x + wj] if y - hj - 1 >= 0 else 0
            tl = integral[y - hj - 1, x - wj - 1] if y - hj - 1 >= 0 and x - wj - 1 >= 0 else 0

            soma = br - tr - bl + tl
            img[y, x] = soma/((2*hj+1)*(2*wj+1))


TESTES_JANELAS = (
    (3, 3),
    (11, 15),
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

                nome_arquivo = f'{nome} - {nome_filtro} {janela[0]}x{janela[1]}'
                print (f'Tempo {nome_arquivo} : {timeit.default_timer () - start_time}')

                cv2.imwrite (f'out/{nome_arquivo}.png', saida*255)

if __name__ == '__main__':
    main ()