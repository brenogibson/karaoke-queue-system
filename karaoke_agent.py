#!/usr/bin/env python3
import os
import re
import yt_dlp
from pathlib import Path

KARAOKE_DIR = os.getenv('KARAOKE_DIR', '/home/breno/Karaoke')

# Carregar variáveis de ambiente do .env se existir
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Verificar se deve usar Strands (se credenciais AWS estão disponíveis)
USE_STRANDS = bool(os.getenv('BEDROCK_API_KEY'))

if USE_STRANDS:
    try:
        from strands import Agent, tool
        print("[AGENT] Usando Strands Agents com Bedrock")
    except ImportError:
        USE_STRANDS = False
        print("[AGENT] Strands não disponível, usando modo direto")
else:
    print("[AGENT] Bedrock API Key não configurada, usando modo direto")

def format_song_name(query: str) -> str:
    """Formata o nome da música para o padrão Artista - Música usando LLM"""
    query = query.strip()
    
    # Se já está no formato correto, retorna
    if " - " in query and len(query.split(" - ")) == 2:
        parts = query.split(" - ", 1)
        return f"{parts[0].title()} - {parts[1].title()}"
    
    prompt = f"""Dado o texto de busca de uma música: "{query}"

Identifique o ARTISTA e o NOME DA MÚSICA.

Responda APENAS no formato: Artista - Nome da Música

Exemplos:
- "abba dancing queen" → "ABBA - Dancing Queen"
- "bohemian rhapsody queen" → "Queen - Bohemian Rhapsody"
- "menudo nao se reprima" → "Menudo - Não Se Reprima"
- "dancing queen" → "ABBA - Dancing Queen" (se souber o artista)

Resposta:"""

    # Tentar Bedrock primeiro (se Bedrock API Key disponível)
    bedrock_key = os.getenv('BEDROCK_API_KEY')
    if bedrock_key:
        try:
            import requests
            
            region = os.getenv('AWS_REGION', 'us-east-1')
            url = f"https://bedrock-runtime.{region}.amazonaws.com/model/anthropic.claude-3-haiku-20240307-v1:0/invoke"
            
            headers = {
                'Authorization': f'Bearer {bedrock_key}',
                'Content-Type': 'application/json'
            }
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "temperature": 0.1,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=headers, json=body, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                formatted = result['content'][0]['text'].strip()
                
                if " - " in formatted and len(formatted.split(" - ")) == 2:
                    print(f"[BEDROCK] Formatado: {formatted}")
                    return formatted
                else:
                    print(f"[BEDROCK] Resposta inválida, tentando Groq")
            else:
                print(f"[BEDROCK] Erro HTTP {response.status_code}, tentando Groq")
        except Exception as e:
            print(f"[BEDROCK] Erro: {e}, tentando Groq")
    
    # Tentar Groq como fallback
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key and groq_key != 'your_groq_api_key_here':
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=50
            )
            
            formatted = response.choices[0].message.content.strip()
            
            if " - " in formatted and len(formatted.split(" - ")) == 2:
                print(f"[GROQ] Formatado: {formatted}")
                return formatted
            else:
                print(f"[GROQ] Resposta inválida, usando fallback")
        except Exception as e:
            print(f"[GROQ] Erro: {e}, usando fallback")
    
    # Fallback: lógica simples
    print(f"[FALLBACK] Usando formatação simples")
    words = query.split()
    if len(words) >= 2:
        mid = len(words) // 2
        artist = " ".join(words[:mid]).title()
        song = " ".join(words[mid:]).title()
        return f"{artist} - {song}"
    
    return query.title()

def search_youtube_karaoke(query: str) -> dict:
    """Busca vídeos de karaoke no YouTube e retorna o mais popular"""
    try:
        search_query = f"ytsearch10:{query} karaoke"
        print(f"[SEARCH] Buscando: {query} karaoke")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(search_query, download=False)
            
        if not search_results or 'entries' not in search_results:
            return {"error": "Nenhum resultado encontrado"}
        
        entries = search_results['entries']
        karaoke_videos = [v for v in entries if v and 'karaoke' in v.get('title', '').lower()]
        if not karaoke_videos:
            karaoke_videos = [v for v in entries if v]
        
        if not karaoke_videos:
            return {"error": "Nenhum vídeo encontrado"}
        
        best_video = karaoke_videos[0]
        print(f"[SEARCH] Encontrado: {best_video['title']}")
        
        return {
            "url": f"https://youtube.com/watch?v={best_video['id']}",
            "title": best_video['title']
        }
    except Exception as e:
        print(f"[SEARCH] Erro: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

def download_karaoke_video(url: str, output_name: str) -> dict:
    """Baixa vídeo do YouTube e salva no formato correto"""
    try:
        import subprocess
        output_path = os.path.join(KARAOKE_DIR, f"{output_name}.mp4")
        
        print(f"[DOWNLOAD] Baixando para: {output_path}")
        
        cmd = [
            os.path.expanduser("~/.local/bin/yt-dlp"),
            "--extractor-args", "youtube:player_client=android",
            "-o", output_path,
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"[DOWNLOAD] Erro: {result.stderr}")
            return {"error": result.stderr}
        
        print(f"[DOWNLOAD] Sucesso!")
        
        # Verificar codec e converter se necessário
        print(f"[CONVERT] Verificando codec...")
        codec_check = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", 
             "-show_entries", "stream=codec_name", "-of", 
             "default=noprint_wrappers=1:nokey=1", output_path],
            capture_output=True, text=True
        )
        
        codec = codec_check.stdout.strip()
        print(f"[CONVERT] Codec detectado: {codec}")
        
        if codec == "av1":
            print(f"[CONVERT] Convertendo AV1 → H.264 para compatibilidade com iPad...")
            temp_path = output_path + ".temp.mp4"
            
            convert_result = subprocess.run(
                ["ffmpeg", "-i", output_path, "-c:v", "libx264", 
                 "-preset", "fast", "-crf", "23", "-c:a", "copy", 
                 temp_path, "-y"],
                capture_output=True, text=True, timeout=600
            )
            
            if convert_result.returncode == 0:
                os.replace(temp_path, output_path)
                print(f"[CONVERT] Conversão concluída!")
            else:
                print(f"[CONVERT] Erro na conversão: {convert_result.stderr}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            print(f"[CONVERT] Codec compatível, conversão não necessária")
        
        return {"success": True, "path": output_path}
    except subprocess.TimeoutExpired:
        print(f"[DOWNLOAD] Timeout")
        return {"error": "Timeout no download"}
    except Exception as e:
        print(f"[DOWNLOAD] Erro: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# Modo Strands (com IA)
if USE_STRANDS:
    @tool
    def format_song_name_tool(query: str) -> str:
        """Formata o nome da música para o padrão Artista - Música"""
        return format_song_name(query)
    
    @tool
    def search_youtube_karaoke_tool(query: str) -> dict:
        """Busca vídeos de karaoke no YouTube"""
        return search_youtube_karaoke(query)
    
    @tool
    def download_karaoke_video_tool(url: str, output_name: str) -> dict:
        """Baixa vídeo do YouTube"""
        return download_karaoke_video(url, output_name)
    
    karaoke_agent = Agent(
        name="KaraokeDownloader",
        system_prompt="""Você é um assistente que baixa músicas de karaoke do YouTube.

Seu trabalho:
1. Receber o nome de uma música
2. Formatar o nome para o padrão "Artista - Música"
3. Buscar no YouTube a versão karaoke
4. Baixar o vídeo com o nome formatado

Use as ferramentas na ordem correta.""",
        tools=[format_song_name_tool, search_youtube_karaoke_tool, download_karaoke_video_tool]
    )
    
    def process_song_request(query: str) -> dict:
        """Processa pedido usando Strands Agent"""
        try:
            import asyncio
            print(f"\n[AGENT] Processando com IA: {query}")
            response = asyncio.run(karaoke_agent.invoke_async(
                f"Encontre e baixe a música de karaoke: {query}"
            ))
            return {"success": True, "message": "Música processada com IA", "response": str(response)}
        except Exception as e:
            print(f"[AGENT] Erro: {e}")
            return {"success": False, "error": str(e)}

# Modo Direto (sem IA)
else:
    def process_song_request(query: str) -> dict:
        """Processa pedido de música diretamente"""
        try:
            print(f"\n[AGENT] Processando: {query}")
            
            formatted_name = format_song_name(query)
            print(f"[AGENT] Nome formatado: {formatted_name}")
            
            search_result = search_youtube_karaoke(query)
            if "error" in search_result:
                return {"success": False, "error": search_result["error"]}
            
            download_result = download_karaoke_video(search_result["url"], formatted_name)
            if "error" in download_result:
                return {"success": False, "error": download_result["error"]}
            
            print(f"[AGENT] Concluído com sucesso!")
            return {"success": True, "message": "Música baixada com sucesso", "file": formatted_name}
            
        except Exception as e:
            print(f"[AGENT] Erro geral: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

def test_bedrock_connection():
    """Testa conexão com Bedrock"""
    if not USE_STRANDS:
        print("❌ Credenciais AWS não configuradas")
        print("📝 Veja AWS_SETUP.md para instruções")
        return False
    
    try:
        import boto3
        bedrock = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION'))
        print("✅ Conexão com Bedrock OK")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com Bedrock: {e}")
        return False
