from __future__ import annotations
import re
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

def _parse_date(s: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime object."""
    if not s:
        return None
    s = s.strip()
    
    formats = [
        "%m/%d/%y %H:%M",
        "%m/%d/%y",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

def _parse_float(s: Optional[str]) -> Optional[float]:
    """Parse string to float, handling special cases."""
    if not s or s.strip().lower() in ['<loq', '<loq%', 'nd', 'n/a', '--', 'not tested', 'not applicable']:
        return None
    
    s = s.strip().replace(",", "").replace("%", "").replace("mg", "").replace("g", "")
    
    try:
        return float(s)
    except ValueError:
        match = re.search(r'[-+]?\d*\.?\d+', s)
        if match:
            return float(match.group())
        return None

@dataclass
class ModernCannaAnalyte:
    """Individual cannabinoid result from Modern Canna."""
    name: str
    percent: Optional[float] = None
    mg: Optional[float] = None

def _sanitize_name(name: str) -> str:
    """Remove leading/trailing whitespace and ensure name starts with alphanumeric character."""
    if not name:
        return name
    # Strip whitespace, newlines, and other whitespace characters
    name = name.strip()
    # Don't strip leading parentheses for specific terpene names
    if name.startswith('(+/-)-') or name.startswith('(R)-(+)-') or name.startswith('(S)-(-)-'):
        return name
    # Remove leading non-alphanumeric characters
    name = re.sub(r'^[^a-zA-Z0-9]+', '', name)
    return name

@dataclass
class ModernCannaTerpene:
    """Individual terpene result from Modern Canna."""
    name: str
    percent: Optional[float] = None
    
    def __post_init__(self):
        """Sanitize name after initialization."""
        self.name = _sanitize_name(self.name)

@dataclass
class ModernCannaTestStatus:
    """Test result status."""
    test_name: str
    status: str  # PASS, FAIL, Completed, Not Tested, Not Applicable

@dataclass
class ModernCanna_COA:
    """
    Modern Canna Laboratory Certificate of Analysis parser.
    Handles both format variants (with and without mg values in potency details).
    """
    # Lab Info
    lab_name: str = "Modern Canna"
    lab_address: str = "4705 Old Rd 37, Lakeland, FL 33813"
    lab_license: str = "CMTL-0005"
    lab_accreditation: str = "102020"
    lab_director: Optional[str] = None
    lab_cso: Optional[str] = None
    lab_phone: str = "863-608-7800"
    lab_website: str = "www.moderncanna.com"
    
    # Client & Product Info
    client: str = "Trulieve"
    client_address: Optional[str] = None
    batch_number: Optional[str] = None
    sample_alias: Optional[str] = None
    sample_matrix: Optional[str] = None
    lab_id: Optional[str] = None
    cultivar: Optional[str] = None
    
    # Dates
    sample_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    
    # Potency Results
    cannabinoids: List[ModernCannaAnalyte] = field(default_factory=list)
    total_thc_percent: Optional[float] = None
    total_thc_mg: Optional[float] = None
    total_cbd_percent: Optional[float] = None
    total_cbd_mg: Optional[float] = None
    total_cbg_percent: Optional[float] = None
    total_cbg_mg: Optional[float] = None
    total_cbn_percent: Optional[float] = None
    total_cbn_mg: Optional[float] = None
    total_active_cannabinoids_percent: Optional[float] = None
    total_active_cannabinoids_mg: Optional[float] = None
    
    # Terpenes
    terpenes: List[ModernCannaTerpene] = field(default_factory=list)
    total_terpenes_percent: Optional[float] = None
    
    # Test Statuses
    test_results: List[ModernCannaTestStatus] = field(default_factory=list)
    
    # Raw data
    raw_text: Optional[str] = None
    
    @classmethod
    def from_text(cls, text: str) -> "ModernCanna_COA":
        """Parse Modern Canna COA text."""
        instance = cls(raw_text=text)
        
        if not text:
            return instance
        
        def find(pattern: str, group: int = 1) -> Optional[str]:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if not match:
                return None
            try:
                return match.group(group).strip()
            except IndexError:
                return None
        
        # Client and Sample Info
        instance.client_address = find(r'Trulieve\s*\n\s*([^\n]+)')
        instance.batch_number = find(r'(\d{5}_\d{10})')
        instance.sample_alias = find(r'Sample Alias:\s*([^\n]+)')
        instance.sample_matrix = find(r'Sample Matrix:\s*([^\n]+)')
        instance.lab_id = find(r'Lab ID:\s*([^\n]+)')
        instance.cultivar = find(r'Cultivar:\s*([^\n]+)')
        
        # Dates
        instance.sample_date = _parse_date(find(r'Sample Date:\s*([^\n]+)'))
        instance.received_date = _parse_date(find(r'Received:\s*([^\n]+)'))
        instance.completed_date = _parse_date(find(r'Completed:\s*([^\n]+)'))
        
        # Lab personnel
        instance.lab_director = find(r'Laboratory Director\s*\n\s*([^\n]+)') or find(r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*\n\s*Laboratory Director')
        instance.lab_cso = find(r'Chief Scientific Officer\s*\n\s*([^\n]+)') or find(r'([A-Z][a-z]+\s+[A-Z][a-z]+,\s*M\.S\.)\s*\n\s*Chief Scientific Officer')
        
        # Parse Cannabinoids from POTENCY DETAILS section
        cannabinoids = []
        
        # Look for the potency details section
        if 'POTENCY DETAILS' in text:
            potency_section = text.split('POTENCY DETAILS')[1]
            # End at TERPENES or Total THC
            if 'TERPENES' in potency_section:
                potency_section = potency_section.split('TERPENES')[0]
            elif 'Total THC' in potency_section:
                potency_section = potency_section.split('Total THC')[0]
            
            # Pattern 1: percent with % symbol (format 4)
            # Lines like: " 80.7%  delta 9-THC"
            pattern1 = r'^\s*([0-9\.<>]+)%?\s+([A-Za-z0-9\s\-]+)\s*$'
            
            for match in re.finditer(pattern1, potency_section, re.MULTILINE):
                percent_str = match.group(1).strip()
                name = match.group(2).strip()
                
                if name and not name.lower().startswith('analyte'):
                    cannabinoid = ModernCannaAnalyte(
                        name=name,
                        percent=_parse_float(percent_str),
                        mg=None
                    )
                    cannabinoids.append(cannabinoid)
        
        # Alternative: parse from lines with name first
        # Pattern: " delta 9-THC    81.1    811" or " delta 9-THC  80.7%"
        if not cannabinoids:
            cannabinoid_pattern = r'^\s*([A-Za-z0-9\s\-]+?)\s+([0-9\.<>A-Z]+)\s*([0-9\.<>A-Z]+)?\s*$'
            
            for match in re.finditer(cannabinoid_pattern, text, re.MULTILINE):
                name = match.group(1).strip()
                val1 = match.group(2).strip()
                val2 = match.group(3).strip() if match.group(3) else None
                
                # Skip headers
                if 'Analyte' in name or 'mg' in name or '%' in name:
                    continue
                
                # Check if this looks like a cannabinoid
                common_cannabinoids = ['thc', 'cbd', 'cbg', 'cbn', 'cbc', 'thcv', 'cbdv', 'delta']
                if any(c in name.lower() for c in common_cannabinoids):
                    cannabinoid = ModernCannaAnalyte(
                        name=name,
                        percent=_parse_float(val1),
                        mg=_parse_float(val2) if val2 else None
                    )
                    cannabinoids.append(cannabinoid)
        
        instance.cannabinoids = cannabinoids
        
        # Parse summary totals
        thc_match = re.search(r'Total THC\s+([0-9\.]+)%\s+\(([0-9\.]+)\s*mg\)', text)
        if thc_match:
            instance.total_thc_percent = _parse_float(thc_match.group(1))
            instance.total_thc_mg = _parse_float(thc_match.group(2))
        
        cbd_match = re.search(r'Total CBD\s+([0-9\.]+)%\s+\(([0-9\.]+)\s*mg\)', text)
        if cbd_match:
            instance.total_cbd_percent = _parse_float(cbd_match.group(1))
            instance.total_cbd_mg = _parse_float(cbd_match.group(2))
        
        cbg_match = re.search(r'Total CBG\s+([0-9\.]+)%\s+\(([0-9\.]+)\s*mg\)', text)
        if cbg_match:
            instance.total_cbg_percent = _parse_float(cbg_match.group(1))
            instance.total_cbg_mg = _parse_float(cbg_match.group(2))
        
        cbn_match = re.search(r'Total CBN\s+([0-9\.]+)%\s+\(([0-9\.]+)\s*mg\)', text)
        if cbn_match:
            instance.total_cbn_percent = _parse_float(cbn_match.group(1))
            instance.total_cbn_mg = _parse_float(cbn_match.group(2))
        
        # Total Active Cannabinoids or Total Cannabinoids
        active_match = re.search(r'Total (?:Active )?Cannabinoids\s+([0-9\.]+)%\s+\(([0-9\.]+)\s*mg\)', text)
        if active_match:
            instance.total_active_cannabinoids_percent = _parse_float(active_match.group(1))
            instance.total_active_cannabinoids_mg = _parse_float(active_match.group(2))
        
        # Parse Terpenes
        terpenes = []
        if 'TERPENES' in text or 'Total Terpenes' in text:
            # Find terpene section
            terpene_section = text
            if 'TERPENES SUMMARY' in text:
                terpene_section = text.split('TERPENES SUMMARY')[1].split('Total CBD')[0]
            elif 'TERPENES' in text and 'Analyte' in text:
                # Find section between TERPENES and Total THC
                terp_start = text.find('TERPENES')
                if terp_start > 0:
                    terpene_section = text[terp_start:terp_start+2000]
                    if 'Total THC' in terpene_section:
                        terpene_section = terpene_section.split('Total THC')[0]
            
            # Total terpenes
            total_terp_match = re.search(r'Total Terpenes[:\s]*([0-9\.]+)%', terpene_section)
            if total_terp_match:
                instance.total_terpenes_percent = _parse_float(total_terp_match.group(1))
            
            # Individual terpenes - pattern: name then percent
            # " beta-Caryophyllene  0.632" or "0.632 \n beta-Caryophyllene"
            terpene_pattern = r'^\s*([A-Za-z\-\(\)\+\/\s]+?)\s+([0-9\.]+)\s*$'
            
            for match in re.finditer(terpene_pattern, terpene_section, re.MULTILINE):
                name = match.group(1).strip()
                percent_str = match.group(2).strip()
                
                # Skip headers and non-terpene lines
                if 'Analyte' in name or 'Total' in name or '%' in name:
                    continue
                
                # Common terpenes check
                common_terpenes = ['caryophyllene', 'limonene', 'myrcene', 'linalool', 'humulene', 
                                 'pinene', 'bisabolol', 'terpineol', 'terpinolene', 'camphene', 
                                 'borneol', 'guaiol', 'ocimene', 'fenchyl']
                
                if any(t in name.lower() for t in common_terpenes):
                    terpene = ModernCannaTerpene(
                        name=name,
                        percent=_parse_float(percent_str)
                    )
                    terpenes.append(terpene)
        
        instance.terpenes = terpenes
        
        # Parse Test Statuses
        test_results = []
        if 'ANALYSIS SUMMARY' in text:
            summary_section = text.split('ANALYSIS SUMMARY')[0]
            
            test_patterns = [
                'Potency', 'Homogeneity', 'Terpenes', 'Residual Solvents', 
                '% Moisture', 'Water Activity', 'Foreign Matter', 'Pesticides',
                'Mycotoxins', 'Heavy Metals', 'Microbials', 'Label Claim'
            ]
            
            for test_name in test_patterns:
                match = re.search(f'{test_name}\\s+(Completed|Not Tested|PASS|FAIL|Not Applicable)', text, re.IGNORECASE)
                if match:
                    test_results.append(ModernCannaTestStatus(
                        test_name=test_name,
                        status=match.group(1).upper()
                    ))
        
        instance.test_results = test_results
        
        return instance
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif hasattr(obj, '__dict__'):
                return {k: serialize(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            return obj
        
        return serialize(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_json(self, filepath: str, indent: int = 2) -> None:
        """Save as JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json(indent=indent))
    
    def __str__(self) -> str:
        return f"ModernCanna_COA(batch={self.batch_number}, lab_id={self.lab_id})"