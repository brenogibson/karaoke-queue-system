# 🎤 Karaokê Queue System

Sistema de fila de karaokê com interface web para público e DJ.

## 📋 Características

- **Interface Pública**: Usuários escolhem músicas e adicionam à fila
- **Interface DJ**: Controle completo da fila e reprodução
- **PWA**: Instalável como app no iPad/iPhone/Mac
- **Drag & Drop**: Reordene músicas arrastando
- **Compatibilidade iOS**: Vídeos H.264, controles nativos no iPad
- **Rede Local**: Acesse de qualquer dispositivo na mesma rede

## 🚀 Início Rápido

### Opção 1: Iniciar Manualmente (Recomendado para testes)

```bash
cd ~/karaoke-queue-system
./start.sh
```

Pressione `Ctrl+C` para parar.

### Opção 2: Iniciar em Background

```bash
~/karaoke-queue-system/start-bg.sh
```

Para parar:
```bash
~/karaoke-queue-system/stop.sh
```

### Opção 3: Iniciar Automaticamente no Boot (Serviço)

```bash
# Instalar serviço
sudo cp ~/karaoke-queue-system/karaoke.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable karaoke
sudo systemctl start karaoke

# Verificar status
sudo systemctl status karaoke

# Ver logs
sudo journalctl -u karaoke -f

# Parar serviço
sudo systemctl stop karaoke

# Desabilitar auto-start
sudo systemctl disable karaoke
```

## 📱 Acessar o Sistema

Após iniciar, acesse de qualquer dispositivo na rede:

- **🎤 Público**: `http://192.168.3.106:5001`
- **🎧 DJ**: `http://192.168.3.106:5001/dj`

*(Substitua o IP pelo seu IP local)*

## 📲 Instalar como App (PWA)

### iPad/iPhone

1. Abra no Safari: `http://192.168.3.106:5001/dj`
2. Toque em **Compartilhar** (ícone ⬆️)
3. Role e toque em **"Adicionar à Tela de Início"**
4. Confirme

### Mac (Chrome/Edge)

1. Abra no Chrome/Edge
2. Clique no ícone **⊕** na barra de endereço
3. Clique em **"Instalar"**

## 📁 Estrutura do Projeto

```
karaoke-queue-system/
├── app.py                  # Servidor Flask
├── karaoke_agent.py        # Agent para download de músicas
├── templates/
│   ├── public.html         # Interface pública
│   └── dj.html            # Interface DJ
├── static/
│   ├── icon.png           # Ícone público
│   ├── icon-dj.png        # Ícone DJ
│   └── sw.js              # Service Worker (PWA)
├── manifest.json          # Manifest público
├── manifest-dj.json       # Manifest DJ
├── requirements.txt       # Dependências Python
├── start.sh              # Iniciar (foreground)
├── start-bg.sh           # Iniciar (background)
├── stop.sh               # Parar servidor
├── karaoke.service       # Serviço systemd
└── README.md             # Este arquivo
```

## 🎵 Vídeos de Karaokê

Os vídeos ficam em: `/media/breno/External/Karaoke`

### Converter vídeos AV1 para H.264 (iOS)

```bash
~/convert_av1_to_h264.sh
```

## 🔧 Comandos Úteis

```bash
# Ver log em tempo real
tail -f /tmp/karaoke.log

# Verificar se está rodando
lsof -i:5001

# Parar manualmente
kill $(lsof -t -i:5001)

# Ver IP local
hostname -I

# Testar servidor
curl http://localhost:5001
```

## 🛠️ Requisitos

- Python 3
- Flask
- Acesso à rede local
- Vídeos em formato MP4 (H.264 para iOS)

## 📝 Instalação de Dependências

```bash
cd ~/karaoke-queue-system
pip3 install -r requirements.txt
```

## 🔥 Firewall

Se necessário, libere a porta:

```bash
sudo ufw allow 5001/tcp
```

## 🎮 Controles do DJ

- **▶ Próxima**: Tocar próxima música
- **⛶ Tela Cheia**: Modo fullscreen
- **🔄 Atualizar**: Recarregar fila
- **🗑️ Limpar Fila**: Remover todas as músicas
- **⏮ ⏭**: Música anterior/próxima
- **▶/⏸**: Play/Pause
- **🔊**: Controle de volume (apenas PC)
- **Clicar na música**: Tocar imediatamente
- **Arrastar música**: Reordenar fila

## 🌐 Repositório

https://github.com/brenogibson/karaoke-queue-system

## 📄 Licença

MIT
