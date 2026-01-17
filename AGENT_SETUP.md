# Sistema de Agente Flexível

## Modos de Operação

O sistema agora suporta dois modos:

### 1. Modo Direto (Padrão)
- **Quando usar**: Sem credenciais AWS configuradas
- **Como funciona**: Lógica Python direta sem IA
- **Vantagens**: 
  - Rápido e eficiente
  - Não precisa de configuração adicional
  - Sem custos de API

### 2. Modo Strands + Bedrock (Opcional)
- **Quando usar**: Com credenciais AWS configuradas
- **Como funciona**: Usa IA do Bedrock via Strands Agents
- **Vantagens**:
  - Formatação inteligente de nomes
  - Melhor interpretação de queries
  - Pode lidar com pedidos complexos

## Configuração

### Para usar Modo Direto (atual)
Nenhuma configuração necessária! O sistema já está funcionando.

### Para habilitar Modo Strands + Bedrock

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Crie credenciais AWS (veja `AWS_SETUP.md`)

3. Edite `.env` com suas credenciais:
```
AWS_ACCESS_KEY_ID=sua_key
AWS_SECRET_ACCESS_KEY=sua_secret
AWS_REGION=us-east-1
```

4. Reinicie o servidor

## Funcionalidades Implementadas

✅ Download automático de músicas do YouTube  
✅ Busca inteligente com filtro "karaoke"  
✅ Formatação automática "Artista - Música"  
✅ Conversão automática AV1 → H.264 (compatível iPad)  
✅ Modo direto (sem IA) funcional  
✅ Modo Strands (com IA) opcional  
✅ Credenciais seguras (ignoradas no Git)  

## Arquivos de Configuração

- `.env` - Credenciais AWS (ignorado no Git)
- `.env.example` - Template de configuração
- `AWS_SETUP.md` - Guia completo de setup AWS
- `.gitignore` - Atualizado para proteger credenciais
