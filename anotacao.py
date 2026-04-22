import pandas as pd
import csv
import argparse

parser = argparse.ArgumentParser(description='Gera arquivos TXT de anotações por radiologista.')
parser.add_argument('--csv', default='csvs/annotations_train.csv', help='Caminho para o CSV de anotações')
args = parser.parse_args()

df = pd.read_csv(args.csv)

for rad_id, grupo in df.groupby('rad_id'):
    nome_arquivo = f"{rad_id}.txt"
    grupo[['image_id', 'class_name', 'x_min', 'y_min', 'x_max', 'y_max']].to_csv(
        nome_arquivo, 
        header=False, 
        index=False, 
        sep=',', 
        quoting=csv.QUOTE_NONE, 

    )