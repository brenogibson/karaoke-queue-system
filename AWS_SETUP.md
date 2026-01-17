# Configuração AWS para Bedrock

## Opção 1: Usar arquivo .env (Recomendado)

Crie um arquivo `.env` na raiz do projeto:

```bash
AWS_ACCESS_KEY_ID=sua_access_key_aqui
AWS_SECRET_ACCESS_KEY=sua_secret_key_aqui
AWS_REGION=us-east-1
```

## Opção 2: Usar AWS CLI

Configure suas credenciais:

```bash
aws configure
```

## Criar API Key do Bedrock

Para criar uma API key sem data de validade:

```bash
# 1. Criar usuário IAM
aws iam create-user --user-name karaoke-bedrock-user

# 2. Anexar política de acesso ao Bedrock
aws iam attach-user-policy \
  --user-name karaoke-bedrock-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# 3. Criar access key (sem data de validade)
aws iam create-access-key --user-name karaoke-bedrock-user
```

Salve as credenciais retornadas no arquivo `.env`

## Testar Conexão

```bash
python3 -c "from karaoke_agent import test_bedrock_connection; test_bedrock_connection()"
```
