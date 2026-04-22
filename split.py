import os
import random
import shutil

def split_dataset(images_dir, labels_dir, split_pct=0.2, seed=42):
    random.seed(seed)

    # Listar imagens
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    images = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in exts]

    # Filtrar apenas as que têm label correspondente
    pairs = []
    for img in sorted(images):
        stem = os.path.splitext(img)[0]
        label = stem + '.txt'
        if os.path.exists(os.path.join(labels_dir, label)):
            pairs.append((img, label))
        else:
            print(f"Aviso: label não encontrado para {img}")

    random.shuffle(pairs)

    n_val = int(len(pairs) * split_pct)
    val_pairs = pairs[:n_val]
    train_pairs = pairs[n_val:]

    # Criar pastas de saída
    for folder in ['val/images', 'val/labels', 'train/images', 'train/labels']:
        os.makedirs(folder, exist_ok=True)

    for img, lbl in val_pairs:
        shutil.copy2(os.path.join(images_dir, img), os.path.join('val/images', img))
        shutil.copy2(os.path.join(labels_dir, lbl), os.path.join('val/labels', lbl))

    for img, lbl in train_pairs:
        shutil.copy2(os.path.join(images_dir, img), os.path.join('train/images', img))
        shutil.copy2(os.path.join(labels_dir, lbl), os.path.join('train/labels', lbl))

    print(f"Treino: {len(train_pairs)} | Validação: {len(val_pairs)}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Divide dataset em treino e validação.')
    parser.add_argument('--images', required=True, help='Pasta de imagens')
    parser.add_argument('--labels', required=True, help='Pasta de labels')
    parser.add_argument('--pct', type=float, default=0.2, help='Porcentagem para validação (padrão: 0.2)')
    parser.add_argument('--seed', type=int, default=42, help='Seed para reprodutibilidade (padrão: 42)')
    args = parser.parse_args()

    split_dataset(args.images, args.labels, args.pct, args.seed)
