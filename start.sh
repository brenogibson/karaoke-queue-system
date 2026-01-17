#!/bin/bash

# Script de inicialização do Karaoke Queue System

echo "🎤 Iniciando Karaoke Queue System..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3."
    exit 1
fi

# Verificar se Flask está instalado
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Instalando dependências..."
    pip3 install -r requirements.txt
fi

# Obter IP local
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "✅ Servidor iniciado com sucesso!"
echo ""
echo "📱 Site Público: http://$IP:5001"
echo "🎛️  Site do DJ:   http://$IP:5001/dj"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Iniciar servidor
python3 app.py
