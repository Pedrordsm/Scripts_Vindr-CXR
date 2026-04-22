import os
import glob
from ensemble_boxes import weighted_boxes_fusion

PASTA_ENTRADA = "/local/onde/estao/os/arquivos/txt" 
PASTA_SAIDA   = "resultado"
IOU_CONSENSO = 0.5

SCORE_1_ANOTADOR   = 0.4
SCORE_2_ANOTADORES = 0.7
SCORE_3_ANOTADORES = 1.0

WBF_IOU_THR  = 0.5
WBF_SKIP_THR = 0.001

def ler_arquivo_yolo(caminho_arquivo):

    boxes  = []
    labels = []

    if not os.path.exists(caminho_arquivo):
        print("arquivo não encontrado")
        return boxes, labels

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split()

            classe   = int(partes[0])
            x_centro = float(partes[1])
            y_centro = float(partes[2])
            largura  = float(partes[3])
            altura   = float(partes[4])

            x1 = x_centro - largura / 2
            y1 = y_centro - altura  / 2
            x2 = x_centro + largura / 2
            y2 = y_centro + altura  / 2

            x1 = max(0.0, min(1.0, x1))
            y1 = max(0.0, min(1.0, y1))
            x2 = max(0.0, min(1.0, x2))
            y2 = max(0.0, min(1.0, y2))

            #farantir que x2 > x1 e y2 > y1 
            if x2 <= x1:
                x2 = x1 + 0.001
            if y2 <= y1:
                y2 = y1 + 0.001

            boxes.append([x1, y1, x2, y2])
            labels.append(classe)
    return boxes, labels

def calcular_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    if x2 <= x1 or y2 <= y1:
        return 0.0

    area_intersecao = (x2 - x1) * (y2 - y1)
    area_box1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area_box2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    area_uniao = area_box1 + area_box2 - area_intersecao

    #caixas internas em outras
    if area_uniao == 0:
        return 1.0
    
    return area_intersecao / area_uniao if area_uniao > 0 else 0.0


def calcular_scores(boxes, labels, iou_consenso=IOU_CONSENSO):
    n = len(boxes)
    scores = [0.0] * n
    for i in range(n):

        concordancias = 0 

        for j in range(n):
            if i == j:
                continue
            if labels[i] != labels[j]:
                continue

            iou = calcular_iou(boxes[i], boxes[j])

            if iou > iou_consenso:
                concordancias += 1
        if concordancias >= 2:
            scores[i] = SCORE_3_ANOTADORES
        elif concordancias == 1:
            scores[i] = SCORE_2_ANOTADORES
        else:
            scores[i] = SCORE_1_ANOTADOR 
    return scores

def aplicar_wbf(boxes, scores, labels, wbf_iou_thr=WBF_IOU_THR):
    
    if not boxes:
        return [], [], []

    boxes_fundidas, scores_fundidos, labels_fundidos = weighted_boxes_fusion(
        [boxes], [scores], [labels], weights=[1.0], iou_thr=wbf_iou_thr, skip_box_thr=WBF_SKIP_THR
    )

    return boxes_fundidas.tolist(), scores_fundidos.tolist(), labels_fundidos.tolist()

def salvar_arquivo_yolo(boxes, scores, labels, caminho_saida):

    with open(caminho_saida, 'w') as arquivo:
        for box, score, label in zip(boxes, scores, labels):
            x1, y1, x2, y2 = box

            x_centro = (x1 + x2) / 2
            y_centro = (y1 + y2) / 2
            largura  = x2 - x1
            altura   = y2 - y1

            arquivo.write(f"{int(label)} {x_centro:.6f} {y_centro:.6f} {largura:.6f} {altura:.6f}\n")

def processar_pasta(pasta_entrada=PASTA_ENTRADA, pasta_saida=PASTA_SAIDA, iou_consenso=IOU_CONSENSO, wbf_iou_thr=WBF_IOU_THR):

    os.makedirs(pasta_saida, exist_ok=True)

    arquivos = glob.glob(os.path.join(pasta_entrada, "*.txt"))

    if not arquivos:
        print("Nenhum arquivo .txt encontrado")
        return

    for caminho_arquivo in arquivos:

        nome_arquivo = os.path.basename(caminho_arquivo)

        boxes, labels = ler_arquivo_yolo(caminho_arquivo)

        caminho_saida = os.path.join(pasta_saida, nome_arquivo)

        # manter anotações vazias
        if not boxes:
            open(caminho_saida, 'w').close()
            continue

        scores = calcular_scores(boxes, labels, iou_consenso)

        boxes_wbf, scores_wbf, labels_wbf = aplicar_wbf(boxes, scores, labels, wbf_iou_thr)

        salvar_arquivo_yolo(boxes_wbf, scores_wbf, labels_wbf, caminho_saida)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Aplica Weighted Boxes Fusion (WBF) em anotações YOLO.')
    parser.add_argument('--entrada', default=PASTA_ENTRADA, help='Pasta com os arquivos TXT de entrada')
    parser.add_argument('--saida', default=PASTA_SAIDA, help='Pasta de saída dos resultados (padrão: resultado)')
    parser.add_argument('--iou-consenso', type=float, default=IOU_CONSENSO, help='IoU mínimo para considerar concordância entre anotadores (padrão: 0.5)')
    parser.add_argument('--wbf-iou', type=float, default=WBF_IOU_THR, help='Threshold de IoU para o WBF (padrão: 0.5)')
    args = parser.parse_args()

    processar_pasta(args.entrada, args.saida, args.iou_consenso, args.wbf_iou)
