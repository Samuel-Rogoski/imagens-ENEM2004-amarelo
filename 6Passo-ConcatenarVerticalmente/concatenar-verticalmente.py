"""
Propósito: concatenas verticalmente as imagens de cada pasta vinda do passo 5
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "divididas-sem-bordas-do-meio" do passo 5 para essa pasta do passo 6
OBS2: não compensa concatenar as páginas inteiras. Tenha isso em mente para o passo 7. Concatene apenas as colunas.
"""

from PIL import Image
import os
import re

pasta_imagens = "sem-bordas-externas"
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

def get_sort_key(nome_arquivo):
    # Extrai o número da página e converte para inteiro
    match = re.search(r'pagina_enem_(\d+)_', nome_arquivo)
    if match:
        return int(match.group(1))  # <-- CONVERTE PARA INTEIRO AQUI
    else:
        # Fallback: tenta extrair qualquer número do nome do arquivo
        numeros = re.findall(r'\d+', nome_arquivo)
        if numeros:
            return int(numeros[0])
        return 0

# Lista todos os arquivos PNG na pasta
arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('.png')]

# Ordenação personalizada com verificação
def custom_sort(nome):
    try:
        # Tenta extrair o número da página
        match = re.search(r'pagina_enem_(\d+)_', nome)
        if match:
            return int(match.group(1))
        # Se não encontrar o padrão, tenta qualquer número
        numeros = re.findall(r'\d+', nome)
        if numeros:
            return int(numeros[0])
    except:
        pass
    return 0

arquivos.sort(key=custom_sort)

# Mostra a ordem para debug
print("Ordem dos arquivos após ordenação:")
for i, arquivo in enumerate(arquivos, 1):
    print(f"{i}: {arquivo}")

# Carrega as imagens
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")  # Para verificar a ordem

# Verifica se as imagens estão na ordem correta
if imagens:
    print(f"\nPrimeira imagem: {arquivos[0]}")
    print(f"Última imagem: {arquivos[-1]}")

# Encontra a largura máxima entre todas as imagens
largura_max = max(img.width for img in imagens)

# Calcula a altura total
altura_total = sum(img.height for img in imagens)

# Cria uma nova imagem com a largura máxima e altura total
imagem_final = Image.new('RGB', (largura_max, altura_total))

# Cola as imagens verticalmente
y = 0
for img in imagens:
    # Centraliza a imagem horizontalmente se ela for menor que a largura máxima
    x = (largura_max - img.width) // 2
    imagem_final.paste(img, (x, y))
    y += img.height

# Salva a imagem final
imagem_final.save(os.path.join(pasta_saida, 'paginas_concatenadas_verticalmente.png'))
print(f"\nImagens concatenadas verticalmente! Total de {len(imagens)} páginas.")
print(f"Ordem final dos arquivos: {arquivos}")