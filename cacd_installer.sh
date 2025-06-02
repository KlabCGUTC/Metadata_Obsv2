#!/bin/bash
# Script de instalação para CACD Metadata Analyzer - Versão Otimizada

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

# Instalar dependências
echo "📦 Instalando dependências..."
python3 -m pip install --user pyyaml 2>/dev/null || {
    echo "⚠️  Instalando PyYAML..."
    python3 -m pip install --user pyyaml
}

# Configurar diretórios
INSTALL_DIR="$HOME/.local/share/cacd-analyzer"
BIN_DIR="$HOME/.local/bin"
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# Copiar arquivos
echo "📂 Instalando arquivos..."
cp "$SCRIPT_DIR"/*.py "$INSTALL_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR"/*.yaml "$INSTALL_DIR/" 2>/dev/null || true
chmod +x "$INSTALL_DIR"/*.py

# Criar comando principal
cat > "$BIN_DIR/cacd-analyzer" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/cacd-analyzer"
if [ -f "$INSTALL_DIR/cacd_metadata_analyzer.py" ]; then
    exec python3 "$INSTALL_DIR/cacd_metadata_analyzer.py" "$@"
else
    echo "❌ CACD Analyzer não encontrado em $INSTALL_DIR"
    exit 1
fi
EOF
chmod +x "$BIN_DIR/cacd-analyzer"

# Verificar instalação
if [ -f "$INSTALL_DIR/taxonomia_cacd.yaml" ]; then
    TAXONOMY_STATUS="✅ Taxonomia incluída"
    TAXONOMY_ARG="taxonomia_cacd.yaml"
else
    TAXONOMY_STATUS="⚠️  Use sua própria taxonomia"
    TAXONOMY_ARG="/caminho/para/taxonomia.yaml"
fi

# Verificar PATH
PATH_STATUS="✅ Pronto para usar"
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    PATH_STATUS="⚠️  Adicione ao PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "🎉 Instalação concluída!"
echo "======================"
echo "$TAXONOMY_STATUS"
echo "$PATH_STATUS"
echo ""
echo "🚀 Uso rápido:"
echo "   cacd-analyzer /seu/vault -t $TAXONOMY_ARG"
echo ""
echo "📖 Teste:"
echo "   python3 $INSTALL_DIR/test_cacd.py"
echo ""
