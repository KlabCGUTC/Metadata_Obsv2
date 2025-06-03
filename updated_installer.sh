#!/bin/bash
# Script de instalação para CACD Metadata Analyzer
# Usa requirements.txt para gerenciar dependências

set -e

echo "🎯 CACD Metadata Analyzer - Instalação"
echo "====================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 necessário. Instale primeiro:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   Fedora: sudo dnf install python3 python3-pip"  
    echo "   macOS: brew install python3"
    exit 1
fi

echo "✅ Python: $(python3 --version)"

# Verificar pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip não encontrado. Instale primeiro:"
    echo "   Ubuntu/Debian: sudo apt install python3-pip"
    echo "   Fedora: sudo dnf install python3-pip"
    exit 1
fi

# Configurar diretórios
INSTALL_DIR="$HOME/.local/share/cacd-analyzer"
BIN_DIR="$HOME/.local/bin"
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# Instalar dependências via requirements.txt
echo "📦 Instalando dependências..."
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    python3 -m pip install --user -r "$SCRIPT_DIR/requirements.txt"
    echo "✅ Dependências instaladas via requirements.txt"
else
    echo "⚠️  requirements.txt não encontrado, instalando manualmente..."
    python3 -m pip install --user PyYAML
fi

# Copiar arquivos do projeto
echo "📂 Instalando arquivos..."

# Arquivos principais
for file in "cacd_metadata_analyzer.py" "test_cacd.py" "requirements.txt"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        cp "$SCRIPT_DIR/$file" "$INSTALL_DIR/"
        [ "$file" == "*.py" ] && chmod +x "$INSTALL_DIR/$file"
    fi
done

# Taxonomia CACD (se disponível)
if [ -f "$SCRIPT_DIR/taxonomia_cacd.yaml" ]; then
    cp "$SCRIPT_DIR/taxonomia_cacd.yaml" "$INSTALL_DIR/"
    TAXONOMY_STATUS="✅ Taxonomia CACD incluída"
    TAXONOMY_PATH="$INSTALL_DIR/taxonomia_cacd.yaml"
else
    TAXONOMY_STATUS="⚠️  Taxonomia não encontrada - use sua própria"
    TAXONOMY_PATH="/caminho/para/sua/taxonomia.yaml"
fi

# Criar executável principal
cat > "$BIN_DIR/cacd-analyzer" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/cacd-analyzer"
MAIN_SCRIPT="$INSTALL_DIR/cacd_metadata_analyzer.py"

if [ -f "$MAIN_SCRIPT" ]; then
    exec python3 "$MAIN_SCRIPT" "$@"
else
    echo "❌ CACD Analyzer não encontrado em $INSTALL_DIR"
    echo "Execute novamente o script de instalação."
    exit 1
fi
EOF
chmod +x "$BIN_DIR/cacd-analyzer"

# Criar comando de teste
cat > "$BIN_DIR/cacd-test" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/cacd-analyzer"
TEST_SCRIPT="$INSTALL_DIR/test_cacd.py"

if [ -f "$TEST_SCRIPT" ]; then
    exec python3 "$TEST_SCRIPT" "$@"
else
    echo "❌ Script de teste não encontrado em $INSTALL_DIR"
    exit 1
fi
EOF
chmod +x "$BIN_DIR/cacd-test"

# Verificar PATH
PATH_STATUS="✅ Comandos prontos para usar"
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    PATH_STATUS="⚠️  Adicione ao PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Teste rápido da instalação
echo "🧪 Testando instalação..."
if python3 -c "import yaml; print('✅ PyYAML OK')" 2>/dev/null; then
    DEPS_STATUS="✅ Dependências OK"
else
    DEPS_STATUS="❌ Erro nas dependências"
fi

# Resumo da instalação
echo ""
echo "🎉 Instalação concluída!"
echo "======================"
echo "$TAXONOMY_STATUS"
echo "$DEPS_STATUS"  
echo "$PATH_STATUS"
echo ""
echo "📋 Arquivos instalados em: $INSTALL_DIR"
echo "🔧 Comandos disponíveis:"
echo "   cacd-analyzer - Programa principal"
echo "   cacd-test     - Teste de funcionalidade"
echo ""
echo "🚀 Primeiros passos:"
echo ""
echo "1. Testar instalação:"
echo "   cacd-test"
echo ""
echo "2. Analisar seu vault:"
echo "   cacd-analyzer /caminho/vault -t $TAXONOMY_PATH"
echo ""
echo "3. Ver todas as opções:"
echo "   cacd-analyzer --help"
echo ""

# Instalar dependências adicionais (opcional)
if [ "$1" == "--dev" ]; then
    echo "📚 Instalando dependências de desenvolvimento..."
    python3 -m pip install --user pytest black flake8 2>/dev/null || true
fi

echo "💡 Para atualizar: execute este script novamente"
echo "🗑️  Para remover: rm -rf $INSTALL_DIR $BIN_DIR/cacd-*"
echo ""
