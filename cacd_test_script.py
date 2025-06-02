#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para CACD Metadata Analyzer
Cria um vault de exemplo e testa as funcionalidades principais
"""

import os
import sys
import tempfile
import shutil
import yaml
from pathlib import Path

def create_test_vault(base_path: Path):
    """Cria um vault de teste com notas de exemplo"""
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Criar taxonomia de teste simplificada
    test_taxonomy = {
        "História do Brasil": {
            "O período colonial": ["A configuração territorial", "As dimensões econômicas"],
            "O Segundo Reinado (1840-1889)": ["Política externa", "A questão da escravidão"]
        },
        "História Mundial": {
            "Revoluções": ["A Revolução Francesa", "Revoluções no século XX"],
            "As relações internacionais": ["O Concerto Europeu", "A Guerra Fria"]
        },
        "Política Internacional": {
            "O Brasil e a América do Sul": ["Integração na América do Sul", "O MERCOSUL"],
            "Estados Unidos da América": []
        },
        "Geografia": {
            "Geografia política": ["Teorias geopolíticas", "Relações Estado e território"],
            "Geografia Urbana": ["Processo de urbanização", "Metropolização"]
        },
        "ECONOMIA": {
            "Microeconomia": ["Demanda do Consumidor", "Oferta do Produtor"],
            "Macroeconomia": ["Contabilidade Nacional", "Política monetária"]
        }
    }
    
    with open(base_path / "taxonomia_cacd.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(test_taxonomy, f, default_flow_style=False, allow_unicode=True)
    
    # Criar notas de teste
    test_notes = [
        {
            "filename": "revolucao-francesa.md",
            "frontmatter": {"title": "A Revolução Francesa"},
            "content": """
A Revolução Francesa (1789-1799) foi um período de intensa transformação política e social na França. 
Marcou o fim do Antigo Regime e estabeleceu princípios democráticos que influenciaram o mundo todo.

## Causas
- Crise financeira do Estado
- Desigualdades sociais
- Influência do Iluminismo

## Fases
1. **Fase Moderada** (1789-1792)
2. **Fase Radical** (1792-1794) 
3. **Fase Termidoriana** (1794-1799)

## Impacto
A revolução inspirou movimentos liberais em toda a Europa e nas Américas.
"""
        },
        {
            "filename": "guerra-do-paraguai.md",
            "frontmatter": {
                "title": "Guerra do Paraguai",
                "area": "História do Brasil",
                "relevancia_cacd": 5
            },
            "content": """
A Guerra do Paraguai (1864-1870) foi o maior conflito da América do Sul.

## Causas
- Questões geopolíticas na região
- Política expansionista de Solano López
- Interesses econômicos no Rio da Prata

## Participantes
- **Tríplice Aliança**: Brasil, Argentina, Uruguai
- **Paraguai**: sob comando de Francisco Solano López

## Consequências para o Brasil
- Fortalecimento do Exército brasileiro
- Aumento do prestígio internacional
- Impacto na questão abolicionista
"""
        },
        {
            "filename": "mercosul-origem.md",
            "frontmatter": {"title": "Origens do MERCOSUL"},
            "content": """
O Mercado Comum do Sul (MERCOSUL) teve origem nos acordos bilaterais entre Brasil e Argentina.

## Antecedentes
- Processo de redemocratização nos anos 1980
- Necessidade de integração econômica
- Superação das rivalidades históricas

## Tratado de Assunção (1991)
Estabeleceu as bases do MERCOSUL com quatro países fundadores:
- Brasil
- Argentina  
- Uruguai
- Paraguai

## Objetivos
- Livre circulação de bens e serviços
- Tarifa externa comum
- Coordenação de políticas macroeconômicas
"""
        },
        {
            "filename": "urbanizacao-brasil.md",
            "frontmatter": {},
            "content": """
A urbanização no Brasil acelerou-se principalmente após 1950.

## Características
- Migração rural-urbana
- Concentração em metrópoles
- Formação de periferias

## Regiões Metropolitanas
As principais regiões metropolitanas incluem São Paulo, Rio de Janeiro, Belo Horizonte.

## Problemas Urbanos
- Déficit habitacional
- Transporte público deficiente  
- Poluição ambiental
- Violência urbana

## Geografia Urbana
O processo de metropolização criou complexas redes urbanas no território brasileiro.
"""
        },
        {
            "filename": "politica-monetaria.md",
            "frontmatter": {"title": "Política Monetária no Brasil"},
            "content": """
A política monetária é conduzida pelo Banco Central do Brasil.

## Instrumentos
- Taxa básica de juros (SELIC)
- Operações de mercado aberto
- Depósitos compulsórios

## Objetivos
- Controle da inflação
- Estabilidade do sistema financeiro
- Crescimento econômico sustentável

## Regime de Metas de Inflação
Adotado desde 1999, estabelece meta anual para o IPCA.

## Macroeconomia
A política monetária interage com a política fiscal para determinar os resultados macroeconômicos.
"""
        }
    ]
    
    # Criar arquivos das notas
    for note in test_notes:
        content = ""
        if note["frontmatter"]:
            content += "---\n"
            content += yaml.dump(note["frontmatter"], default_flow_style=False, allow_unicode=True)
            content += "---\n"
        content += note["content"]
        
        with open(base_path / note["filename"], 'w', encoding='utf-8') as f:
            f.write(content)
    
    return base_path

def test_analyzer(vault_path: Path, taxonomy_path: Path):
    """Testa o analisador CACD"""
    print(f"🧪 Testando CACD Analyzer...")
    print(f"📁 Vault: {vault_path}")
    print(f"📊 Taxonomia: {taxonomy_path}")
    
    try:
        # Importa o módulo (assumindo que está no PATH ou diretório atual)
        import cacd_metadata_analyzer as analyzer
        
        # Inicializa o analisador
        cacd_analyzer = analyzer.CACDMetadataAnalyzer(
            str(vault_path), 
            str(taxonomy_path)
        )
        
        # Testa scan do vault
        num_notes = cacd_analyzer.scan_vault()
        print(f"✅ {num_notes} notas carregadas")
        
        # Testa análise de uma nota específica
        if "urbanizacao-brasil.md" in cacd_analyzer.notes:
            note = cacd_analyzer.notes["urbanizacao-brasil.md"]
            suggestion = cacd_analyzer.analyze_note(note)
            
            print(f"🔍 Análise da nota '{note.title}':")
            print(f"   - Área sugerida: {suggestion.area}")
            print(f"   - Subárea: {suggestion.subarea}")
            print(f"   - Tags: {suggestion.tags}")
            print(f"   - Relevância: {suggestion.relevancia_cacd}")
            print(f"   - Confiança: {suggestion.confidence:.2f}")
        
        # Testa geração de feedback
        if cacd_analyzer.generate_feedback_file():
            feedback_file = vault_path / "cacd_feedback.md"
            print(f"✅ Arquivo de feedback gerado: {feedback_file}")
            
            # Mostra preview do feedback
            with open(feedback_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:20]  # Primeiras 20 linhas
                print("📄 Preview do feedback:")
                for line in lines:
                    print(f"   {line.rstrip()}")
                if len(lines) == 20:
                    print("   ...")
        
        # Testa geração de relatório
        report_path = cacd_analyzer.generate_study_report()
        if report_path:
            print(f"✅ Relatório gerado: {report_path}")
            
            # Mostra preview do relatório
            with open(report_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:15]
                print("📊 Preview do relatório:")
                for line in lines:
                    print(f"   {line.rstrip()}")
        
        print(f"\n🎉 Teste concluído com sucesso!")
        return True
        
    except ImportError:
        print("❌ Erro: Módulo cacd_metadata_analyzer não encontrado")
        print("   Certifique-se de que o arquivo está no diretório atual ou no PYTHONPATH")
        return False
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def main():
    print("🎯 CACD Metadata Analyzer - Teste de Funcionalidade")
    print("=" * 55)
    
    # Verifica dependências básicas
    try:
        import yaml
        print("✅ PyYAML disponível")
    except ImportError:
        print("❌ PyYAML não encontrado. Instale com: pip install pyyaml")
        return 1
    
    # Cria vault temporário para teste
    with tempfile.TemporaryDirectory(prefix="cacd_test_") as temp_dir:
        temp_path = Path(temp_dir)
        vault_path = create_test_vault(temp_path / "test_vault")
        taxonomy_path = vault_path / "taxonomia_cacd.yaml"
        
        print(f"\n📁 Vault de teste criado em: {vault_path}")
        
        # Lista arquivos criados
        files = list(vault_path.glob("*.md")) + list(vault_path.glob("*.yaml"))
        print(f"📄 Arquivos criados: {len(files)}")
        for file in files:
            print(f"   - {file.name}")
        
        print("\n" + "=" * 55)
        
        # Executa teste
        if test_analyzer(vault_path, taxonomy_path):
            print(f"\n✨ Teste bem-sucedido! O programa está funcionando corretamente.")
            print(f"\n📖 Para usar com seu vault real:")
            print(f"   cacd-analyzer /caminho/para/seu/vault -t taxonomia_cacd.yaml")
            return 0
        else:
            print(f"\n❌ Teste falhou. Verifique a instalação.")
            return 1

if __name__ == "__main__":
    sys.exit(main())
