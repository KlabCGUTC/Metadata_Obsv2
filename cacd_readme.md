# CACD Metadata Analyzer - Versão Otimizada

🎯 **Analisador de metadados otimizado para estudos do CACD (Concurso de Admissão à Carreira Diplomática)**

## ✨ Características Principais

- ⚡ **Rápido**: Usa correspondência de palavras-chave em vez de IA
- 🎯 **Preciso**: Baseado na taxonomia oficial do CACD  
- 🧠 **Inteligente**: Gera tags e conexões relevantes automaticamente
- 🔍 **Controlado**: Permite revisão manual antes de aplicar mudanças
- 📊 **Analítico**: Produz relatórios úteis para planejamento de estudos

## 🚀 Instalação Rápida

```bash
# 1. Clone ou baixe os arquivos
git clone <repositório> # ou baixe manualmente

# 2. Execute o instalador
chmod +x install.sh
./install.sh

# 3. Teste a instalação
python3 test_cacd.py
```

## 📋 Dependências

- Python 3.6+
- PyYAML
- (Opcionais: requests para futuras extensões)

## 🎮 Uso Básico

### Comando Principal
```bash
cacd-analyzer /caminho/para/vault -t taxonomia_cacd.yaml
```

### Workflow Completo
```bash
# 1. Análise inicial (gera feedback)
cacd-analyzer meu-vault/ -t taxonomia_cacd.yaml

# 2. Revisar arquivo 'cacd_feedback.md' no vault
# (marcar [x] para aprovar sugestões)

# 3. Aplicar mudanças aprovadas  
cacd-analyzer meu-vault/ -t taxonomia_cacd.yaml -m process

# 4. Gerar relatório de estudos
cacd-analyzer meu-vault/ -t taxonomia_cacd.yaml -m report
```

## 📊 Metadados Gerados

O programa adiciona os seguintes campos ao frontmatter das suas notas:

```yaml
---
title: "Política Externa do Segundo Reinado"
area: "História do Brasil"                    # Área do conhecimento
subarea: "O Segundo Reinado (1840-1889)"      # Subdivisão
topico: "Política externa"                    # Tópico específico
tags:                                         # Tags relevantes (max 5)
  - brasil
  - politica-brasileira  
  - relações-internacionais
  - imperio
relevancia_cacd: 4                           # Relevância 1-5
conexoes:                                     # Notas relacionadas
  - "Guerra do Paraguai"
  - "Questões com o Reino Unido"
---
```

## 🎯 Taxonomia CACD

Baseado no edital oficial, o programa classifica conteúdo nas seguintes áreas:

### 📚 Matérias Principais
- **Língua Portuguesa**: Gramática, redação, literatura
- **Língua Inglesa**: Compreensão, tradução, redação avançada  
- **História do Brasil**: Colônia → República atual
- **História Mundial**: Revoluções, relações internacionais, ideologias
- **Política Internacional**: Diplomacia brasileira, organismos internacionais
- **Geografia**: População, economia espacial, geopolítica
- **Economia**: Micro/macro, internacional, história econômica brasileira
- **Direito**: Constitucional, administrativo, internacional público
- **Línguas Opcionais**: Espanhol ou Francês

### 🏷️ Sistema de Tags

O programa gera tags específicas por área:

- **História**: `brasil`, `colônia`, `império`, `república`, `internacional`
- **Economia**: `macroeconomia`, `política-fiscal`, `comércio-internacional`  
- **Direito**: `constitucional`, `administrativo`, `internacional-público`
- **Geografia**: `território`, `população`, `meio-ambiente`, `urbanização`
- **Política Internacional**: `diplomacia`, `onu`, `mercosul`, `geopolítica`

### ⭐ Níveis de Relevância CACD

- **5 ⭐⭐⭐⭐⭐**: Crítico - tópicos centrais do concurso
- **4 ⭐⭐⭐⭐**: Muito importante - frequente nas provas
- **3 ⭐⭐⭐**: Importante - conhecimento esperado
- **2 ⭐⭐**: Complementar - contexto adicional
- **1 ⭐**: Básico - fundamentos/introdução

## 🔧 Opções Avançadas

### Modos de Operação
```bash
-m analyze   # Gera feedback (padrão)
-m feedback  # Atualiza arquivo de feedback
-m process   # Aplica mudanças aprovadas
-m report    # Gera relatório de estudos
```

### Configurações
```bash
--min-confidence 0.5  # Confiança mínima (0.0-1.0)
-v                    # Saída verbosa para debug
--help               # Ajuda completa
```

## 📈 Relatórios de Estudo

O programa gera relatórios detalhados incluindo:

### Estatísticas Gerais
- Total de notas no vault
- Cobertura de metadados  
- Distribuição por área de conhecimento

### Análise de Lacunas
- Áreas com baixa cobertura (< 5 notas)
- Sugestões de tópicos para estudar

### Priorização
- Lista de notas de alta relevância para revisão
- Sequências recomendadas de estudo

## 🛠️ Arquivos do Projeto

```
cacd-analyzer/
├── cacd_metadata_analyzer.py  # Programa principal
├── taxonomia_cacd.yaml        # Taxonomia oficial CACD
├── install.sh                 # Script de instalação  
├── test_cacd.py              # Script de teste
├── README.md                 # Este arquivo
└── examples/                 # Exemplos de uso
```

## 🔍 Como Funciona

### 1. Correspondência de Palavras-Chave
```python
# O programa constrói um mapa de palavras da taxonomia
{
  "revolução": [("História Mundial", "Revoluções", "Revolução Francesa")],
  "mercosul": [("Política Internacional", "Brasil e América do Sul", "MERCOSUL")],
  "urbanização": [("Geografia", "Geografia Urbana", "Processo de urbanização")]
}
```

### 2. Análise de Conteúdo
- Normaliza texto (remove acentos, pontuação)
- Conta correspondências com palavras-chave
- Calcula confiança baseada na frequência
- Seleciona classificação com maior pontuação

### 3. Geração de Tags
- Tags baseadas na área de conhecimento
- Tags por palavras-chave específicas
- Tags por padrões (tratados, guerras, etc.)
- Máximo de 5 tags por nota

### 4. Cálculo de Relevância
```python
# Fatores considerados:
- Área de conhecimento (algumas são prioritárias)
- Confiança da classificação  
- Tamanho do conteúdo
- Presença de termos técnicos
```

## 🎓 Estratégias de Estudo Recomendadas

### 📅 Configuração Inicial
1. Execute análise completa do vault
2. Revise sugestões em pequenos lotes
3. Aprove classificações óbvias primeiro
4. Gere relatório inicial para ver panorama

### 🔄 Uso Contínuo  
1. Adicione notas normalmente
2. Execute análise semanalmente
3. Processe apenas novas sugestões
4. Use relatório para planejar estudos

### 🎯 Preparação Final
1. Foque em notas de relevância 4-5
2. Use conexões para revisão integrada  
3. Cubra lacunas identificadas no relatório
4. Crie sequências de estudo por área

## 🚨 Solução de Problemas

### Instalação
```bash
# Dependências em falta
pip install --user pyyaml

# PATH não configurado
export PATH="$HOME/.local/bin:$PATH"

# Teste básico
python3 -c "import yaml; print('OK')"
```

### Uso
```bash
# Programa não encontra vault
cacd-analyzer "$(pwd)/meu-vault" -t taxonomia.yaml

# Taxonomia não encontrada  
cacd-analyzer vault/ -t "/caminho/completo/taxonomia_cacd.yaml"

# Debug detalhado
cacd-analyzer vault/ -t taxonomia.yaml -v
```

### Muitas Sugestões Incorretas
```bash
# Aumente a confiança mínima
cacd-analyzer vault/ -t taxonomia.yaml --min-confidence 0.6

# Ou revise a taxonomia personalizada
```

## 📞 Suporte

Para problemas ou melhorias:

1. **Debug**: Execute com `-v` para logs detalhados
2. **Teste**: Use `python3 test_cacd.py` para verificar funcionamento  
3. **Backup**: O programa cria `.bak` dos arquivos originais automaticamente

## 🎯 Objetivos do Projeto

Este analisador foi criado especificamente para:

✅ **Economizar tempo** na organização de estudos  
✅ **Manter precisão** baseada no edital oficial  
✅ **Fornecer insights** úteis sobre progresso dos estudos  
✅ **Facilitar revisões** através de conexões inteligentes  
✅ **Identificar lacunas** no conhecimento

O programa equilibra **velocidade** e **utilidade**, sendo ideal para candidatos que precisam organizar grandes volumes de conteúdo de estudo de forma eficiente e estratégica.

---

**Desenvolvido especificamente para candidatos ao CACD** 🇧🇷
