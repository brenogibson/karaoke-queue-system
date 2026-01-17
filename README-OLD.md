# Karaoke Queue System 🎤

Sistema de karaokê com fila de músicas, permitindo que o público escolha músicas enquanto o DJ controla a reprodução.

## Funcionalidades

### Site Público (`/`)
- 📋 Lista completa de músicas disponíveis
- 🔍 Busca em tempo real por artista ou música
- ➕ Adicionar músicas à fila
- 🎵 **Pedir músicas que não estão na lista** (download automático do YouTube)
- 📱 Interface responsiva para celular e tablet

### Site do DJ (`/dj`)
- 🎵 Visualização da fila de músicas
- ▶️ Player de vídeo com controles personalizados
- ⏮️ Anterior / ⏭️ Próxima música
- 🔄 Atualização automática da fila (5s)
- 📏 Barra lateral redimensionável
- ⛶ Modo tela cheia
- 🗑️ Limpar fila

## Instalação

### Requisitos
- Python 3.6+
- Flask
- yt-dlp
- ffmpeg (para conversão de vídeos)
- (Opcional) AWS Credentials para usar IA com Bedrock

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/karaoke-queue-system.git
cd karaoke-queue-system
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o diretório dos vídeos:
Edite o arquivo `karaoke_agent.py` e altere a variável `KARAOKE_DIR`:
```python
KARAOKE_DIR = "/caminho/para/seus/videos"
```

4. (Opcional) Configure AWS Bedrock para IA:
```bash
cp .env.example .env
# Edite .env com suas credenciais AWS
```
Veja `AWS_SETUP.md` para instruções detalhadas.

5. Inicie o servidor:
```bash
python app.py
```

6. Acesse os sites:
- Site Público: `http://localhost:5001`
- Site do DJ: `http://localhost:5001/dj`

## Configuração de Rede Local

Para acessar de outros dispositivos na rede:

1. Descubra seu IP local:
```bash
hostname -I
```

2. Libere a porta no firewall (Ubuntu/Debian):
```bash
sudo ufw allow 5001/tcp
```

3. Acesse de qualquer dispositivo:
- `http://SEU_IP:5001` (público)
- `http://SEU_IP:5001/dj` (DJ)

## Estrutura do Projeto

```
karaoke-queue-system/
├── app.py                 # Servidor Flask principal
├── templates/
│   ├── public.html       # Interface pública
│   └── dj.html           # Interface do DJ
├── requirements.txt      # Dependências Python
├── README.md            # Este arquivo
└── .gitignore           # Arquivos ignorados
```

## Formato dos Vídeos

Os vídeos devem estar no formato:
- `Artista - Música.mp4`

Exemplo:
- `Queen - Bohemian Rhapsody.mp4`
- `The Beatles - Hey Jude.mp4`

## Como Usar

1. **Público**: Acessa o site principal, busca músicas e adiciona à fila
2. **DJ**: Monitora a fila no site `/dj` e controla a reprodução
3. As músicas tocam automaticamente na ordem da fila
4. O DJ pode pular, voltar ou remover músicas conforme necessário

## Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Armazenamento**: JSON (fila temporária)

## Licença

MIT License

## Autor

Desenvolvido com ❤️ para festas e eventos de karaokê!
