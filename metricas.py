from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description='Avalia um modelo YOLO e salva as métricas em arquivo TXT.')
parser.add_argument('--modelo', help='Caminho para os pesos do modelo')
parser.add_argument('--saida', default='metricas.txt', help='Arquivo de saída das métricas')
args = parser.parse_args()

modelo = YOLO(args.modelo)

results = modelo.val()

metricas = results.summary()

with open(args.saida, 'w') as f:
        
    for cls in metricas:
        f.write(f"Classe: {cls['Class']}\n")
        f.write(f"Precision: {cls['Box-P']:.4f}\n")
        f.write(f"Recall: {cls['Box-R']:.4f}\n")
        f.write(f"mAP@0.5:0.95: {cls['mAP50-95']:.4f}\n")
        f.write(f"mAP@0.5: {cls['mAP50']:.4f}\n")
        f.write("\n")