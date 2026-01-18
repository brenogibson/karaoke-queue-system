# Configuração do LLM para Formatação Inteligente

O sistema usa um LLM para formatar corretamente os nomes das músicas no padrão "Artista - Música".

## Por que usar LLM?

O LLM identifica corretamente:
- Qual parte é o artista e qual é a música
- Nomes de artistas compostos (ex: "Backstreet Boys")
- Músicas com nomes longos
- Casos ambíguos (ex: "bohemian rhapsody queen" → "Queen - Bohemian Rhapsody")

## Ordem de Prioridade

O sistema tenta usar LLMs nesta ordem:

1. **AWS Bedrock** (Claude 3 Haiku) - se credenciais AWS configuradas
2. **Groq API** (Llama 3.3 70B) - se GROQ_API_KEY configurada
3. **Fallback simples** - divide query ao meio

## Opção 1: AWS Bedrock (Recomendado se você já usa AWS)

### Vantagens
- ✅ Integrado com sua infraestrutura AWS
- ✅ Claude 3 Haiku (rápido e preciso)
- ✅ Sem necessidade de API keys adicionais
- ✅ Billing consolidado na AWS

### Como configurar

Veja `AWS_SETUP.md` para instruções completas.

Resumo:
```bash
# Configure credenciais AWS
aws configure

# Ou adicione ao .env:
AWS_ACCESS_KEY_ID=sua_key
AWS_SECRET_ACCESS_KEY=sua_secret
AWS_REGION=us-east-1
```

### Custo
- Claude 3 Haiku: ~$0.00025 por requisição (muito barato)
- Free tier: 2 meses grátis para novos clientes

## Opção 2: Groq API (Gratuito)

### Vantagens
- ✅ Completamente gratuito
- ✅ Rápido (modelo Llama 3.3 70B)
- ✅ Sem necessidade de conta AWS
- ✅ Limites generosos

### Como configurar

1. Acesse: https://console.groq.com/keys
2. Crie uma conta gratuita (sem cartão de crédito)
3. Clique em "Create API Key"
4. Dê um nome (ex: "karaoke-system")
5. Copie a chave gerada
6. Adicione ao arquivo `.env`:
```bash
GROQ_API_KEY=gsk_sua_chave_aqui
```
7. Reinicie o servidor

## Opção 3: Sem LLM (Fallback)

Se não configurar nenhuma das opções acima, o sistema usa lógica simples:
- Divide a query ao meio
- Primeira metade = Artista
- Segunda metade = Música

**Limitação**: Pode errar em casos como "bohemian rhapsody queen"

## Testar

```bash
cd ~/karaoke-queue-system
python3 << 'EOF'
from karaoke_agent import format_song_name

# Testes
queries = [
    "abba dancing queen",
    "bohemian rhapsody queen",
    "menudo nao se reprima",
    "backstreet boys i want it that way"
]

for q in queries:
    print(f"{q:40} → {format_song_name(q)}")
EOF
```

## Comparação

| Característica | Bedrock | Groq | Fallback |
|---------------|---------|------|----------|
| Custo | ~$0.0003/req | Grátis | Grátis |
| Qualidade | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Velocidade | Rápido | Muito rápido | Instantâneo |
| Setup | AWS account | API key | Nenhum |
| Requer internet | Sim | Sim | Não |

