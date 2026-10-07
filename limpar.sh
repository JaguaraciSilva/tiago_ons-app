#!/bin/bash
echo "Limpando recursos não utilizados do Docker..."
docker system prune -a --volumes -f

echo "Limpando cache do APT..."
sudo apt-get clean
sudo apt-get autoremove -y

echo "Limpando cache do Hugging Face..."
rm -rf ./huggingface_cache/*

echo "Limpeza concluída com sucesso!"