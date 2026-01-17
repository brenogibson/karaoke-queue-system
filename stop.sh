#!/bin/bash

# Script para parar o Karaokê Queue System

echo "🛑 Parando Karaokê Queue System..."

if lsof -i:5001 > /dev/null 2>&1; then
    kill -9 $(lsof -t -i:5001) 2>/dev/null
    sleep 1
    echo "✅ Servidor parado"
else
    echo "ℹ️  Servidor não está rodando"
fi
