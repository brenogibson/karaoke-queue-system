#!/bin/bash

# Script de inicialização do Karaokê Queue System (background)

echo "🎤 Iniciando Karaokê Queue System..."

# Matar processos antigos na porta 5001
echo "🔄 Parando processos antigos..."
kill -9 $(lsof -t -i:5001) 2>/dev/null

# Aguardar um momento
sleep 1

# Iniciar servidor em background
echo "🚀 Iniciando servidor..."
cd /home/breno/karaoke-queue-system
python3 app.py > /tmp/karaoke.log 2>&1 &

# Aguardar servidor iniciar
sleep 3

# Verificar se está rodando
if lsof -i:5001 > /dev/null 2>&1; then
    IP=$(hostname -I | awk '{print $1}')
    echo ""
    echo "✅ Servidor iniciado com sucesso!"
    echo ""
    echo "📱 Acesse de qualquer dispositivo na rede:"
    echo "   🎤 Público: http://$IP:5001"
    echo "   🎧 DJ:      http://$IP:5001/dj"
    echo ""
    echo "📋 Ver log:  tail -f /tmp/karaoke.log"
    echo "🛑 Parar:    ~/karaoke-queue-system/stop.sh"
else
    echo "❌ Erro ao iniciar servidor"
    echo "📋 Verifique o log: cat /tmp/karaoke.log"
    exit 1
fi
