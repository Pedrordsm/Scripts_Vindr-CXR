import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Gera gráficos de barras para as métricas por classe.')
parser.add_argument('--metricas', default='metricas.txt', help='Caminho para o arquivo de métricas')
args = parser.parse_args()

with open(args.metricas, 'r') as f:
    linha = f.readline()
    while linha != '':
        if linha.startswith("Classe:"):
            classe = linha.split(":")[1].strip()
            precision = float(f.readline().split(":")[1].strip())
            recall = float(f.readline().split(":")[1].strip())
            mAP50_95 = float(f.readline().split("95:")[1].strip())
            mAP50 = float(f.readline().split(":")[1].strip())
            
            # Criar o gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(['Precision', 'Recall', 'mAP@0.5:0.95', 'mAP@0.5'], [precision, recall, mAP50_95, mAP50], color=['blue', 'orange', 'green', 'red'])
            plt.title(f'Métricas para a Classe: {classe}')
            plt.ylabel('Valor')
            plt.ylim(0, 1)
            plt.grid(axis='y')
            plt.savefig(f'métricas_{classe}.png')
        
        linha = f.readline()