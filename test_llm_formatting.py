#!/usr/bin/env python3
"""
Script de teste para demonstrar a diferença entre formatação com e sem LLM
"""

# Simulação de respostas do LLM para demonstração
LLM_RESPONSES = {
    "abba dancing queen": "ABBA - Dancing Queen",
    "bohemian rhapsody queen": "Queen - Bohemian Rhapsody",
    "menudo nao se reprima": "Menudo - Não Se Reprima",
    "backstreet boys i want it that way": "Backstreet Boys - I Want It That Way",
    "dancing queen": "ABBA - Dancing Queen",
    "i want it that way backstreet boys": "Backstreet Boys - I Want It That Way",
    "nao se reprima menudo": "Menudo - Não Se Reprima"
}

def format_simple(query):
    """Formatação simples (fallback atual)"""
    words = query.split()
    if len(words) >= 2:
        mid = len(words) // 2
        artist = " ".join(words[:mid]).title()
        song = " ".join(words[mid:]).title()
        return f"{artist} - {song}"
    return query.title()

def format_with_llm(query):
    """Formatação com LLM (simulada)"""
    return LLM_RESPONSES.get(query.lower(), format_simple(query))

# Testes
test_queries = [
    "abba dancing queen",
    "bohemian rhapsody queen",
    "menudo nao se reprima",
    "backstreet boys i want it that way",
    "dancing queen",
    "i want it that way backstreet boys",
    "nao se reprima menudo"
]

print("=" * 100)
print("COMPARAÇÃO: Formatação Simples vs LLM")
print("=" * 100)
print(f"\n{'Query':<40} {'Simples (Fallback)':<30} {'Com LLM':<30}")
print("-" * 100)

for query in test_queries:
    simple = format_simple(query)
    with_llm = format_with_llm(query)
    
    # Marcar se são diferentes
    marker = "❌" if simple != with_llm else "✓"
    
    print(f"{query:<40} {simple:<30} {with_llm:<30} {marker}")

print("\n" + "=" * 100)
print("✓ = Ambos iguais (formatação simples funcionou)")
print("❌ = Diferentes (LLM corrigiu o erro)")
print("=" * 100)
