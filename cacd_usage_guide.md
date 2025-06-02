# CACD Metadata Analyzer - Guia de Uso

## 🎯 Visão Geral

O CACD Metadata Analyzer é um programa otimizado para gerar metadados úteis para seus estudos do Concurso de Admissão à Carreira Diplomática (CACD). Ele analisa suas notas no Obsidian e sugere classificações baseadas na taxonomia oficial do concurso.

## ⚡ Principais Vantagens

- **Velocidade**: Usa correspondência de palavras-chave em vez de AI, sendo muito mais rápido
- **Precisão**: Baseado na taxonomia oficial do CACD
- **Utilidade**: Gera tags, conexões e relevância específicas para o concurso
- **Controle**: Permite revisão manual antes de aplicar mudanças

## 📦 Instalação

```bash
# 1. Baixe os arquivos necessários
# 2. Execute o instalador
chmod +x install.sh
./install.sh

# 3. Adicione ao PATH (se necessário)
export PATH="$HOME/.local/bin:$PATH"
```

## 🚀 Uso Básico

### 1. Primeira Análise

```bash
# Analisa seu vault e gera arquivo de feedback
cacd-analyzer /caminho/para/seu/vault -t taxonomia_cacd.yaml
```

Isso criará um arquivo `cacd_feedback.md` no seu vault com sugestões para revisão.

### 2. Revisão Manual

Abra o arquivo `cacd_feedback.md` e revise as sugestões:

```markdown
## Nota: Revolução Francesa
**Arquivo:** `historia/revolucao-francesa.md`
**Confiança:** 0.85

- **Área:** História Mundial
  - Decisão: [x]  ← Marque [x] para aprovar

- **Subárea:** Revoluções
  - Decisão: [ ]  ← Deixe [ ] para rejeitar

- **Tags:** revolução, frança, liberalismo
  - Decisão: [x]

- **Relevância CACD:** 5/5
  - Decisão: [x]
```

### 3. Aplicar Mudanças

```bash
# Aplica as mudanças aprovadas
cacd-analyzer /caminho/para/seu/vault -t taxonomia_cacd.yaml -m process
```

### 4. Relatório de Estudos

```bash
# Gera relatório com estatísticas de estudos
cacd-analyzer /caminho/para/seu/vault -t taxonomia_cacd.yaml -m report
```

## 🔧 Opções Avançadas

### Modos de Operação

```bash
# Apenas gerar feedback (padrão)
cacd-analyzer vault/ -t taxonomia.yaml -m analyze

# Atualizar arquivo de feedback
cacd-analyzer vault/ -t taxonomia.yaml -m feedback

# Processar feedback aprovado
cacd-analyzer vault/ -t taxonomia.yaml -m process

# Gerar relatório de estudos
cacd-analyzer vault/ -t taxonomia.yaml -m report
```

### Configurações

```bash
# Ajustar confiança mínima (0.0 a 1.0)
cacd-analyzer vault/ -t taxonomia.yaml --min-confidence 0.5

# Saída verbosa para debugging
cacd-analyzer vault/ -t taxonomia.yaml -v
```

## 📊 Metadados Gerados

O programa gera os seguintes metadados para suas notas:

### Frontmatter Example
```yaml
---
title: "A Política Externa do Segundo Reinado"
area: "História do Brasil"
subarea: "O Segundo Reinado (1840-1889)"
topico: "Política externa"
tags: 
  - brasil
  - politica-brasileira
  - relações-internacionais
  - imperio
relevancia_cacd: 4
conexoes:
  - "Guerra do Paraguai"
  - "Questões com o Reino Unido"
---
```

### Campos Explicados

- **area**: Área principal do conhecimento (baseada na taxonomia CACD)
- **subarea**: Subdivisão da área
- **topico**: Tópico específico dentro da subárea
- **tags**: Tags relevantes para CACD (máximo 5)
- **relevancia_cacd**: Relevância para o concurso (1-5)
- **conexoes**: Sugestões de notas relacionadas

## 🎯 Estratégias de Estudo

### 1. Identificar Lacunas
O relatório mostra áreas com baixa cobertura:
```markdown
### Áreas com baixa cobertura (menos de 5 notas):
- Língua Francesa
- Direito Internacional Privado
```

### 2. Priorizar Revisão
Use a relevância CACD para focar nos tópicos mais importantes:
- **Nível 5 ⭐⭐⭐⭐⭐**: Crítico para o concurso
- **Nível 4 ⭐⭐⭐⭐**: Muito importante
- **Nível 3 ⭐⭐⭐**: Importante
- **Nível 2 ⭐⭐**: Complementar
- **Nível 1 ⭐**: Básico/introdutório

### 3. Usar Conexões
As conexões sugeridas ajudam a:
- Criar mapas mentais
- Identificar temas transversais
- Estabelecer sequências lógicas de estudo

## 🔍 Taxonomia CACD

O programa usa a taxonomia oficial que inclui:

### Matérias Principais
- **Língua Portuguesa**: Gramática, redação, literatura
- **Língua Inglesa**: Compreensão, tradução, redação
- **História do Brasil**: Do período colonial ao século XXI
- **História Mundial**: Estruturas econômicas, revoluções, relações internacionais
- **Política Internacional**: Política externa brasileira, organizações internacionais
- **Geografia**: População, economia, geopolítica, meio ambiente
- **Economia**: Micro, macro, internacional, história econômica
- **Direito**: Constitucional, administrativo, internacional
- **Línguas Opcionais**: Espanhol ou Francês

### Tags Automáticas por Área

O programa gera tags específicas baseadas no conteúdo:

- **História**: brasil, colônia, império, república, internacional
- **Economia**: macroeconomia, política-fiscal, comércio-internacional
- **Direito**: constitucional, administrativo, internacional-público
- **Geografia**: território, população, meio-ambiente, urbanização
- **Política Internacional**: diplomacia, onu, mercosul, geopolítica

## 🛠️ Solução de Problemas

### Programa não encontra notas
```bash
# Verifique se o caminho está correto
ls /caminho/para/vault/*.md

# Use caminho absoluto
cacd-analyzer "$(pwd)/meu-vault" -t taxonomia_cacd.yaml
```

### Taxonomia não encontrada
```bash
# Verifique se o arquivo existe
ls taxonomia_cacd.yaml

# Use caminho completo
cacd-analyzer vault/ -t "/caminho/completo/taxonomia_cacd.yaml"
```

### Muitas sugestões incorretas
```bash
# Aumente a confiança mínima
cacd-analyzer vault/ -t taxonomia.yaml --min-confidence 0.6
```

### Depuração
```bash
# Use modo verboso para ver detalhes
cacd-analyzer vault/ -t taxonomia.yaml -v
```

## 📈 Workflow Recomendado

### Configuração Inicial
1. Instale o programa
2. Execute análise inicial
3. Revise e aprove sugestões em lotes pequenos
4. Gere relatório para ver progresso

### Uso Contínuo
1. Adicione novas notas normalmente
2. Execute análise semanalmente
3. Revise apenas novas sugestões
4. Use relatório para planejar estudos

### Preparação para Prova
1. Gere relatório final
2. Foque em notas de alta relevância
3. Use conexões para revisão integrada
4. Identifique e cubra lacunas restantes

## 💡 Dicas de Produtividade

1. **Títulos Descritivos**: Use títulos claros que reflitam o conteúdo
2. **Conteúdo Estruturado**: Organize notas com seções claras
3. **Palavras-Chave**: Inclua termos técnicos relevantes
4. **Revisão Regular**: Processe feedback semanalmente
5. **Backup**: O programa faz backup automático dos arquivos originais

## 🆘 Suporte

Para problemas ou dúvidas:
1. Execute com `-v` para logs detalhados
2. Verifique se todos os arquivos estão no lugar correto
3. Confirme que as dependências estão instaladas
4. Use o modo `feedback` para regenerar sugestões

O programa foi projetado para ser uma ferramenta de produtividade para seus estudos CACD, economizando tempo na organização enquanto mantém a qualidade e precisão necessárias para um concurso de alto nível.
