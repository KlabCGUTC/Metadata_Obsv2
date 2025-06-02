#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CACD Metadata Analyzer - Versão Otimizada
Analisador de metadados para vault Obsidian focado em estudos para CACD
Equilibra velocidade com precisão e utilidade para estudos

Autor: Assistente Claude
Versão: 2.0
"""

import os
import sys
import yaml
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import unicodedata

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Note:
    """Representa uma nota do vault"""
    id: str
    title: str
    content: str
    frontmatter: Dict[str, Any]
    file_path: str
    last_modified: datetime
    
    def __post_init__(self):
        if not self.title and 'title' in self.frontmatter:
            self.title = self.frontmatter['title']
        elif not self.title:
            self.title = Path(self.file_path).stem

@dataclass
class MetadataSuggestion:
    """Sugestão de metadados para uma nota"""
    note_id: str
    area: Optional[str] = None
    subarea: Optional[str] = None
    topico: Optional[str] = None
    tags: List[str] = None
    relevancia_cacd: Optional[int] = None
    conexoes: List[str] = None
    confidence: float = 0.0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.conexoes is None:
            self.conexoes = []

class CACDTaxonomyAnalyzer:
    """Analisador da taxonomia CACD otimizado para velocidade"""
    
    def __init__(self, taxonomy_path: str):
        self.taxonomy_path = taxonomy_path
        self.taxonomy = self._load_taxonomy()
        self.keyword_map = self._build_keyword_map()
        self.areas = list(self.taxonomy.keys())
        
    def _load_taxonomy(self) -> Dict:
        """Carrega a taxonomia CACD"""
        try:
            with open(self.taxonomy_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar taxonomia: {e}")
            return {}
    
    def _normalize_text(self, text: str) -> str:
        """Normaliza texto para busca (remove acentos, lowcase)"""
        if not text:
            return ""
        # Remove acentos
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        # Converte para minúsculas e remove caracteres especiais
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Remove espaços extras
        text = ' '.join(text.split())
        return text
    
    def _build_keyword_map(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """Constrói mapa de palavras-chave para classificação rápida"""
        keyword_map = defaultdict(list)
        
        for area, content in self.taxonomy.items():
            area_norm = self._normalize_text(area)
            
            # Adiciona palavras da área
            for word in area_norm.split():
                if len(word) > 2:  # Ignora palavras muito curtas
                    keyword_map[word].append((area, None, None))
            
            if isinstance(content, dict):
                for subarea, topics in content.items():
                    subarea_norm = self._normalize_text(subarea)
                    
                    # Adiciona palavras da subárea
                    for word in subarea_norm.split():
                        if len(word) > 2:
                            keyword_map[word].append((area, subarea, None))
                    
                    if isinstance(topics, list):
                        for topic in topics:
                            if isinstance(topic, str):
                                topic_norm = self._normalize_text(topic)
                                
                                # Adiciona palavras do tópico
                                for word in topic_norm.split():
                                    if len(word) > 2:
                                        keyword_map[word].append((area, subarea, topic))
        
        return dict(keyword_map)
    
    def classify_text(self, text: str, title: str = "") -> Tuple[str, str, str, float]:
        """Classifica texto usando correspondência de palavras-chave"""
        combined_text = f"{title} {text}".strip()
        normalized_text = self._normalize_text(combined_text)
        
        if not normalized_text:
            return None, None, None, 0.0
        
        words = normalized_text.split()
        matches = defaultdict(int)
        
        # Conta correspondências para cada classificação
        for word in words:
            if word in self.keyword_map:
                for area, subarea, topic in self.keyword_map[word]:
                    key = (area, subarea, topic)
                    matches[key] += 1
        
        if not matches:
            return None, None, None, 0.0
        
        # Encontra a melhor correspondência
        best_match = max(matches.items(), key=lambda x: x[1])
        (area, subarea, topic), score = best_match
        
        # Calcula confiança baseada na pontuação e tamanho do texto
        confidence = min(score / max(len(words) * 0.1, 1), 1.0)
        
        return area, subarea, topic, confidence

class CACDTagGenerator:
    """Gerador de tags específicas para CACD"""
    
    def __init__(self):
        # Tags comuns por área de conhecimento
        self.area_tags = {
            "Língua Portuguesa": ["gramática", "ortografia", "redação", "literatura", "linguística"],
            "Língua Inglesa": ["inglês", "tradução", "gramática-inglesa", "vocabulário"],
            "História do Brasil": ["brasil", "colônia", "império", "república", "política-brasileira"],
            "História Mundial": ["internacional", "guerra", "revolução", "imperialismo", "ideologia"],
            "Política Internacional": ["diplomacia", "relações-internacionais", "onu", "mercosul", "geopolítica"],
            "Geografia": ["território", "população", "economia-espacial", "meio-ambiente", "urbanização"],
            "ECONOMIA": ["macroeconomia", "microeconomia", "política-fiscal", "comércio-internacional", "desenvolvimento"],
            "DIREITO": ["constitucional", "administrativo", "internacional-público", "tratados", "soberania"],
            "LÍNGUA ESPANHOLA": ["espanhol", "tradução-espanhol", "america-latina"],
            "LÍNGUA FRANCESA": ["francês", "tradução-francês", "francofonia"]
        }
        
        # Palavras-chave que geram tags específicas
        self.keyword_tags = {
            "constituição": "constitucional",
            "mercosul": "integração-regional",
            "onu": "multilateralismo",
            "guerra": "conflitos",
            "paz": "paz-segurança",
            "economia": "análise-econômica",
            "política": "ciência-política",
            "diplomacia": "ação-diplomática",
            "território": "geografia-política",
            "população": "demografia",
            "meio ambiente": "sustentabilidade",
            "brasil": "brasil-estudos",
            "direitos humanos": "direitos-humanos",
            "comércio": "comércio-internacional"
        }
    
    def generate_tags(self, text: str, title: str, area: str = None) -> List[str]:
        """Gera tags relevantes para CACD"""
        combined_text = f"{title} {text}".lower()
        tags = set()
        
        # Tags baseadas na área
        if area and area in self.area_tags:
            # Adiciona 1-2 tags da área se relevantes
            area_words = self.area_tags[area]
            for tag in area_words[:2]:  # Limita para não sobrecarregar
                if any(word in combined_text for word in tag.split('-')):
                    tags.add(tag)
        
        # Tags baseadas em palavras-chave específicas
        for keyword, tag in self.keyword_tags.items():
            if keyword in combined_text:
                tags.add(tag)
        
        # Tags baseadas em padrões específicos do CACD
        if re.search(r'\b(tratado|acordo|convenção)\b', combined_text):
            tags.add("instrumentos-jurídicos")
        
        if re.search(r'\b(guerra|conflito|paz)\b', combined_text):
            tags.add("segurança-internacional")
        
        if re.search(r'\b(desenvolvimento|crescimento|econômico)\b', combined_text):
            tags.add("desenvolvimento-econômico")
        
        return list(tags)[:5]  # Limita a 5 tags para manter relevância

class CACDMetadataAnalyzer:
    """Analisador principal de metadados CACD"""
    
    def __init__(self, vault_path: str, taxonomy_path: str, config: Dict = None):
        self.vault_path = Path(vault_path)
        self.config = config or self._default_config()
        
        # Inicializa componentes
        self.taxonomy_analyzer = CACDTaxonomyAnalyzer(taxonomy_path)
        self.tag_generator = CACDTagGenerator()
        
        # Estado interno
        self.notes: Dict[str, Note] = {}
        self.metadata_cache = {}
        
        logger.info(f"CACD Analyzer inicializado para vault: {vault_path}")
    
    def _default_config(self) -> Dict:
        """Configuração padrão"""
        return {
            "min_content_length": 50,  # Tamanho mínimo para análise
            "max_tags": 5,             # Máximo de tags por nota
            "relevancia_threshold": 0.3, # Threshold mínimo de confiança
            "conexoes_max": 3,         # Máximo de conexões sugeridas
            "feedback_file": "cacd_feedback.md",
            "cache_file": ".cacd_cache.json",
            "backup_original": True
        }
    
    def scan_vault(self) -> int:
        """Escaneia o vault e carrega notas"""
        markdown_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in markdown_files:
            # Pula arquivos de sistema
            if file_path.name.startswith('.') or 'template' in file_path.name.lower():
                continue
                
            try:
                note = self._load_note(file_path)
                if note:
                    self.notes[note.id] = note
            except Exception as e:
                logger.warning(f"Erro ao carregar {file_path}: {e}")
        
        logger.info(f"Carregadas {len(self.notes)} notas")
        return len(self.notes)
    
    def _load_note(self, file_path: Path) -> Optional[Note]:
        """Carrega uma nota individual"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrai frontmatter
            frontmatter = {}
            clean_content = content
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        clean_content = parts[2].strip()
                    except yaml.YAMLError:
                        pass
            
            # Cria ID relativo ao vault
            note_id = str(file_path.relative_to(self.vault_path))
            
            return Note(
                id=note_id,
                title=frontmatter.get('title', file_path.stem),
                content=clean_content,
                frontmatter=frontmatter,
                file_path=str(file_path),
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime)
            )
            
        except Exception as e:
            logger.error(f"Erro ao carregar nota {file_path}: {e}")
            return None
    
    def analyze_note(self, note: Note) -> MetadataSuggestion:
        """Analisa uma nota e gera sugestões de metadados"""
        # Verifica se já tem metadados completos
        if self._has_complete_metadata(note):
            return MetadataSuggestion(note_id=note.id, confidence=1.0)
        
        # Análise de classificação
        area, subarea, topico, confidence = self.taxonomy_analyzer.classify_text(
            note.content, note.title
        )
        
        # Geração de tags
        tags = self.tag_generator.generate_tags(note.content, note.title, area)
        
        # Cálculo de relevância CACD
        relevancia = self._calculate_relevancia_cacd(note, area, confidence)
        
        # Sugestão de conexões
        conexoes = self._suggest_connections(note, area, subarea)
        
        return MetadataSuggestion(
            note_id=note.id,
            area=area,
            subarea=subarea,
            topico=topico,
            tags=tags,
            relevancia_cacd=relevancia,
            conexoes=conexoes,
            confidence=confidence
        )
    
    def _has_complete_metadata(self, note: Note) -> bool:
        """Verifica se a nota já tem metadados completos"""
        fm = note.frontmatter
        required_fields = ['area', 'relevancia_cacd']
        return all(field in fm and fm[field] for field in required_fields)
    
    def _calculate_relevancia_cacd(self, note: Note, area: str, confidence: float) -> int:
        """Calcula relevância para o CACD (1-5)"""
        if not area or confidence < self.config['relevancia_threshold']:
            return 1
        
        # Fatores de relevância
        base_score = 3  # Pontuação base
        
        # Ajusta baseado na área (algumas são mais importantes)
        high_priority_areas = [
            "Política Internacional", "História do Brasil", 
            "DIREITO", "ECONOMIA", "Geografia"
        ]
        
        if area in high_priority_areas:
            base_score += 1
        
        # Ajusta baseado na confiança
        if confidence > 0.7:
            base_score += 1
        elif confidence < 0.4:
            base_score -= 1
        
        # Ajusta baseado no tamanho do conteúdo
        content_length = len(note.content)
        if content_length > 1000:
            base_score += 1
        elif content_length < 200:
            base_score -= 1
        
        return max(1, min(5, base_score))
    
    def _suggest_connections(self, note: Note, area: str, subarea: str) -> List[str]:
        """Sugere conexões com outras notas"""
        connections = []
        note_words = set(self.taxonomy_analyzer._normalize_text(
            f"{note.title} {note.content}"
        ).split())
        
        for other_note_id, other_note in self.notes.items():
            if other_note_id == note.id:
                continue
            
            # Verifica similaridade de área/subárea
            other_area = other_note.frontmatter.get('area')
            other_subarea = other_note.frontmatter.get('subarea')
            
            if other_area == area or other_subarea == subarea:
                connections.append(other_note.title)
                if len(connections) >= self.config['conexoes_max']:
                    break
        
        return connections
    
    def generate_feedback_file(self) -> bool:
        """Gera arquivo de feedback para revisão manual"""
        suggestions_to_review = []
        
        for note in self.notes.values():
            if not self._has_complete_metadata(note):
                suggestion = self.analyze_note(note)
                if suggestion.area:  # Só inclui se houve sugestão
                    suggestions_to_review.append(suggestion)
        
        if not suggestions_to_review:
            logger.info("Todas as notas já possuem metadados completos")
            return False
        
        feedback_path = self.vault_path / self.config['feedback_file']
        
        try:
            with open(feedback_path, 'w', encoding='utf-8') as f:
                f.write("# CACD - Revisão de Metadados\n\n")
                f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write("**Instruções:** Marque com [x] para aprovar, [ ] para rejeitar\n\n")
                
                for suggestion in suggestions_to_review:
                    note = self.notes[suggestion.note_id]
                    f.write(f"## Nota: {note.title}\n")
                    f.write(f"**Arquivo:** `{suggestion.note_id}`\n")
                    f.write(f"**Confiança:** {suggestion.confidence:.2f}\n\n")
                    
                    if suggestion.area:
                        f.write(f"- **Área:** {suggestion.area}\n")
                        f.write(f"  - Decisão: [ ]\n")
                    
                    if suggestion.subarea:
                        f.write(f"- **Subárea:** {suggestion.subarea}\n")
                        f.write(f"  - Decisão: [ ]\n")
                    
                    if suggestion.topico:
                        f.write(f"- **Tópico:** {suggestion.topico}\n")
                        f.write(f"  - Decisão: [ ]\n")
                    
                    if suggestion.tags:
                        f.write(f"- **Tags:** {', '.join(suggestion.tags)}\n")
                        f.write(f"  - Decisão: [ ]\n")
                    
                    if suggestion.relevancia_cacd:
                        f.write(f"- **Relevância CACD:** {suggestion.relevancia_cacd}/5\n")
                        f.write(f"  - Decisão: [ ]\n")
                    
                    if suggestion.conexoes:
                        f.write(f"- **Conexões:** {', '.join(suggestion.conexoes)}\n")
                        f.write(f"  - Decisão: [ ]\n")
                    
                    f.write("\n---\n\n")
            
            logger.info(f"Arquivo de feedback gerado: {feedback_path}")
            logger.info(f"Total de sugestões: {len(suggestions_to_review)}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar arquivo de feedback: {e}")
            return False
    
    def process_feedback_file(self) -> bool:
        """Processa arquivo de feedback e aplica mudanças aprovadas"""
        feedback_path = self.vault_path / self.config['feedback_file']
        
        if not feedback_path.exists():
            logger.error("Arquivo de feedback não encontrado")
            return False
        
        try:
            with open(feedback_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Processa aprovações
            current_note = None
            approved_changes = defaultdict(dict)
            
            for line in content.split('\n'):
                # Identifica nota atual
                if line.startswith('## Nota:'):
                    current_note = line.replace('## Nota:', '').strip()
                
                # Processa aprovações
                elif '- Decisão: [x]' in line:
                    prev_line = content.split('\n')[content.split('\n').index(line) - 1]
                    
                    if current_note and '**' in prev_line:
                        field_match = re.search(r'\*\*(.+?):\*\* (.+)', prev_line)
                        if field_match:
                            field_name = field_match.group(1).lower()
                            field_value = field_match.group(2)
                            
                            # Mapeia nomes de campos
                            field_mapping = {
                                'área': 'area',
                                'subárea': 'subarea', 
                                'tópico': 'topico',
                                'tags': 'tags',
                                'relevância cacd': 'relevancia_cacd',
                                'conexões': 'conexoes'
                            }
                            
                            if field_name in field_mapping:
                                mapped_field = field_mapping[field_name]
                                
                                # Processa valor baseado no tipo
                                if mapped_field == 'tags':
                                    approved_changes[current_note][mapped_field] = [
                                        tag.strip() for tag in field_value.split(',')
                                    ]
                                elif mapped_field == 'relevancia_cacd':
                                    approved_changes[current_note][mapped_field] = int(field_value.split('/')[0])
                                elif mapped_field == 'conexoes':
                                    approved_changes[current_note][mapped_field] = [
                                        conn.strip() for conn in field_value.split(',')
                                    ]
                                else:
                                    approved_changes[current_note][mapped_field] = field_value
            
            # Aplica mudanças aprovadas
            changes_applied = 0
            for note_title, changes in approved_changes.items():
                note = self._find_note_by_title(note_title)
                if note and self._apply_metadata_changes(note, changes):
                    changes_applied += 1
            
            logger.info(f"Aplicadas mudanças em {changes_applied} notas")
            
            # Move arquivo de feedback para backup
            backup_path = feedback_path.with_suffix('.processed.md')
            feedback_path.rename(backup_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar feedback: {e}")
            return False
    
    def _find_note_by_title(self, title: str) -> Optional[Note]:
        """Encontra nota pelo título"""
        for note in self.notes.values():
            if note.title == title:
                return note
        return None
    
    def _apply_metadata_changes(self, note: Note, changes: Dict) -> bool:
        """Aplica mudanças de metadados a uma nota"""
        try:
            file_path = Path(note.file_path)
            
            # Backup se configurado
            if self.config['backup_original']:
                backup_path = file_path.with_suffix('.bak')
                if not backup_path.exists():
                    file_path.rename(backup_path)
                    file_path = backup_path.with_suffix('.md')
            
            # Lê conteúdo atual
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Atualiza frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                    except yaml.YAMLError:
                        frontmatter = {}
                    main_content = parts[2]
                else:
                    frontmatter = {}
                    main_content = content
            else:
                frontmatter = {}
                main_content = content
            
            # Aplica mudanças
            frontmatter.update(changes)
            
            # Reconstrói arquivo
            new_content = "---\n"
            new_content += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
            new_content += "---\n"
            new_content += main_content
            
            # Salva
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Atualiza nota em memória
            note.frontmatter.update(changes)
            
            logger.debug(f"Metadados atualizados para: {note.title}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao aplicar mudanças para {note.title}: {e}")
            return False
    
    def generate_study_report(self) -> str:
        """Gera relatório de estudos baseado nos metadados"""
        report_path = self.vault_path / "cacd_study_report.md"
        
        # Coleta estatísticas
        area_stats = defaultdict(int)
        relevancia_stats = defaultdict(int)
        total_notes = len(self.notes)
        notes_with_metadata = 0
        
        for note in self.notes.values():
            fm = note.frontmatter
            if fm.get('area'):
                notes_with_metadata += 1
                area_stats[fm['area']] += 1
            
            if fm.get('relevancia_cacd'):
                relevancia_stats[fm['relevancia_cacd']] += 1
        
        # Gera relatório
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# Relatório de Estudos CACD\n\n")
                f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                
                f.write("## Estatísticas Gerais\n\n")
                f.write(f"- **Total de notas:** {total_notes}\n")
                f.write(f"- **Notas com metadados:** {notes_with_metadata}\n")
                f.write(f"- **Cobertura:** {notes_with_metadata/total_notes*100:.1f}%\n\n")
                
                f.write("## Distribuição por Área\n\n")
                for area, count in sorted(area_stats.items(), key=lambda x: x[1], reverse=True):
                    percentage = count / notes_with_metadata * 100
                    f.write(f"- **{area}:** {count} notas ({percentage:.1f}%)\n")
                
                f.write("\n## Distribuição por Relevância CACD\n\n")
                for relevancia in range(5, 0, -1):
                    count = relevancia_stats.get(relevancia, 0)
                    if count > 0:
                        percentage = count / notes_with_metadata * 100
                        stars = "⭐" * relevancia
                        f.write(f"- **Nível {relevancia} {stars}:** {count} notas ({percentage:.1f}%)\n")
                
                # Sugestões de estudo
                f.write("\n## Sugestões de Estudo\n\n")
                
                # Áreas com menos cobertura
                min_coverage_areas = [area for area, count in area_stats.items() if count < 5]
                if min_coverage_areas:
                    f.write("### Áreas com baixa cobertura (menos de 5 notas):\n")
                    for area in min_coverage_areas:
                        f.write(f"- {area}\n")
                    f.write("\n")
                
                # Notas de alta relevância para revisão
                high_relevance_notes = [
                    note for note in self.notes.values() 
                    if note.frontmatter.get('relevancia_cacd', 0) >= 4
                ]
                
                if high_relevance_notes:
                    f.write("### Notas de Alta Relevância para Revisão:\n")
                    for note in sorted(high_relevance_notes, 
                                     key=lambda x: x.frontmatter.get('relevancia_cacd', 0), 
                                     reverse=True)[:10]:
                        rel = note.frontmatter.get('relevancia_cacd', 0)
                        area = note.frontmatter.get('area', 'N/A')
                        f.write(f"- **{note.title}** (Rel: {rel}, Área: {area})\n")
            
            logger.info(f"Relatório de estudos gerado: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return ""

def main():
    parser = argparse.ArgumentParser(description="CACD Metadata Analyzer - Versão Otimizada")
    parser.add_argument("vault_path", help="Caminho para o vault Obsidian")
    parser.add_argument("-t", "--taxonomy", required=True, help="Caminho para arquivo de taxonomia CACD")
    parser.add_argument("-m", "--mode", choices=["analyze", "feedback", "process", "report"], 
                       default="analyze", help="Modo de operação")
    parser.add_argument("-v", "--verbose", action="store_true", help="Saída verbosa")
    parser.add_argument("--min-confidence", type=float, default=0.3, 
                       help="Confiança mínima para sugestões")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Verifica se os caminhos existem
    vault_path = Path(args.vault_path)
    taxonomy_path = Path(args.taxonomy)
    
    if not vault_path.exists():
        logger.error(f"Vault não encontrado: {vault_path}")
        return 1
    
    if not taxonomy_path.exists():
        logger.error(f"Arquivo de taxonomia não encontrado: {taxonomy_path}")
        return 1
    
    # Configuração personalizada
    config = {
        "relevancia_threshold": args.min_confidence,
        "min_content_length": 50,
        "max_tags": 5,
        "conexoes_max": 3,
        "feedback_file": "cacd_feedback.md",
        "backup_original": True
    }
    
    # Inicializa analisador
    analyzer = CACDMetadataAnalyzer(str(vault_path), str(taxonomy_path), config)
    
    # Executa modo selecionado
    try:
        analyzer.scan_vault()
        
        if args.mode == "analyze":
            logger.info("Executando análise completa...")
            if analyzer.generate_feedback_file():
                print(f"✅ Arquivo de feedback gerado. Revise e execute com --mode process")
            else:
                print("ℹ️  Todas as notas já possuem metadados completos")
        
        elif args.mode == "feedback":
            if analyzer.generate_feedback_file():
                print(f"✅ Arquivo de feedback atualizado")
            else:
                print("ℹ️  Nenhuma nova sugestão encontrada")
        
        elif args.mode == "process":
            if analyzer.process_feedback_file():
                print("✅ Feedback processado e metadados aplicados")
            else:
                print("❌ Erro ao processar feedback")
                return 1
        
        elif args.mode == "report":
            report_path = analyzer.generate_study_report()
            if report_path:
                print(f"✅ Relatório de estudos gerado: {report_path}")
            else:
                print("❌ Erro ao gerar relatório")
                return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
