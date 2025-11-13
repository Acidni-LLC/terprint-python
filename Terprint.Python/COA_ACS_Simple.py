#ACS_COA_Simple.py
from __future__ import annotations
import re
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

def _parse_date(s: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime object."""
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    
    # Try common date formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
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
    if not s or s.strip().lower() in ['<loq', 'n/a', 'none detected', '-']:
        return None
    
    s = s.strip().replace(",", "").replace("%", "")
    
    # Handle scientific notation
    try:
        return float(s)
    except ValueError:
        # Try to extract first number found
        match = re.search(r'[-+]?\d*\.?\d+([eE][-+]?\d+)?', s)
        if match:
            return float(match.group())
        return None

@dataclass
class ACSAnalyte:
    """Individual analyte/cannabinoid result."""
    name: str
    dilution: Optional[float] = None
    lod_percent: Optional[float] = None
    loq_percent: Optional[float] = None
    result_mg_per_g: Optional[float] = None
    result_percent: Optional[float] = None

@dataclass
class ACSTerpene:
    """Individual terpene result."""
    name: str
    result_mg_per_g: Optional[float] = None
    result_percent: Optional[float] = None

@dataclass
class ACSTestInfo:
    """Test execution details."""
    specimen_weight: Optional[str] = None
    dilution_factor: Optional[float] = None
    sop_method: Optional[str] = None
    prepared_by: Optional[str] = None
    prep_date: Optional[datetime] = None
    analyzed_by: Optional[str] = None
    analysis_date: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    review_date: Optional[datetime] = None
    lab_batch_number: Optional[str] = None

@dataclass
class ACSLabData:
    """Lab identification and certification."""
    name: str = "ACS Laboratory"
    address: Optional[str] = None
    website: Optional[str] = None
    dea_number: Optional[str] = None
    fl_license: Optional[str] = None
    director: Optional[str] = None
    director_credentials: Optional[str] = None
    qa_reviewer: Optional[str] = None
    qa_date: Optional[datetime] = None
    form_number: Optional[str] = None

@dataclass
class ACS_COA_Simple:
    """
    ACS Laboratory Certificate of Analysis parser.
    Focused on data extraction and JSON serialization.
    """
    # Product & Sample Info
    product_name: Optional[str] = None
    sample_matrix: Optional[str] = None
    client: Optional[str] = None
    client_address: Optional[str] = None
    
    # Batch Information
    batch_number: Optional[str] = None
    batch_date: Optional[datetime] = None
    seed_to_sale: Optional[str] = None
    lot_id: Optional[str] = None
    cultivar: Optional[str] = None
    
    # Sample Processing
    order_number: Optional[str] = None
    order_date: Optional[datetime] = None
    sample_number: Optional[str] = None
    sampling_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    
    # Production Info
    test_reg_state: Optional[str] = None
    cultivation_facility: Optional[str] = None
    production_facility: Optional[str] = None
    production_date: Optional[datetime] = None
    
    # Physical Properties
    initial_gross_weight_g: Optional[float] = None
    number_of_units: Optional[int] = None
    net_weight_per_unit_mg: Optional[float] = None
    sampling_method: Optional[str] = None
    
    # Test Results Summary
    test_statuses: Dict[str, str] = field(default_factory=dict)
    
    # Potency Results
    potency_analytes: List[ACSAnalyte] = field(default_factory=list)
    total_active_thc_percent: Optional[float] = None
    total_active_thc_mg: Optional[float] = None
    total_active_cbd_percent: Optional[float] = None
    total_active_cbd_mg: Optional[float] = None
    total_cbg_percent: Optional[float] = None
    total_cbg_mg: Optional[float] = None
    total_cannabinoids_percent: Optional[float] = None
    total_cannabinoids_mg: Optional[float] = None
    
    # Moisture
    moisture_percent: Optional[float] = None
    moisture_action_level: Optional[float] = None
    
    # Terpenes
    terpenes: List[ACSTerpene] = field(default_factory=list)
    total_terpenes_percent: Optional[float] = None
    
    # Test Details
    potency_test_info: ACSTestInfo = field(default_factory=ACSTestInfo)
    moisture_test_info: ACSTestInfo = field(default_factory=ACSTestInfo)
    
    # Lab Info
    lab_data: ACSLabData = field(default_factory=ACSLabData)
    
    # Raw data
    raw_text: Optional[str] = None
    
    @classmethod
    def from_text(cls, text: str) -> "ACS_COA_Simple":
        """Parse ACS COA text and return populated instance."""
        instance = cls(raw_text=text)
        
        if not text:
            return instance
        
        # Helper functions
        def find(pattern: str, group_or_flags: int = 1, flags: Optional[int] = None) -> Optional[str]:
            """
            Find first match and return a capture group as string.
            Backward-friendly:
              - If called as find(pattern, 1) -> group 1 with default flags.
              - If called as find(pattern, re.MULTILINE) -> treats the second arg as flags (group=1).
              - If called as find(pattern, group, flags) -> uses both.
            """
            # Default flags
            default_flags = re.IGNORECASE | re.MULTILINE
            # If flags isn't provided and group_or_flags looks like flags, reinterpret
            if flags is None:
                maybe_flags = group_or_flags
                # Any combination of regex flag bits counts as flags
                known_flags = re.IGNORECASE | re.MULTILINE | re.DOTALL | re.ASCII | re.VERBOSE
                if isinstance(maybe_flags, int) and (maybe_flags & known_flags) != 0:
                    flags = maybe_flags
                    group = 1
                else:
                    group = int(maybe_flags)
                    flags = default_flags
            else:
                group = int(group_or_flags)

            match = re.search(pattern, text, flags)
            if not match:
                return None
            try:
                return match.group(group).strip()
            except IndexError:
                # No such group; return full match
                return match.group(0).strip()

        def find_section(start_pattern: str, end_pattern: Optional[str] = None) -> str:
            start = re.search(start_pattern, text, re.IGNORECASE)
            if not start:
                return ""
            start_pos = start.end()
            if end_pattern:
                end = re.search(end_pattern, text[start_pos:], re.IGNORECASE)
                if end:
                    return text[start_pos:start_pos + end.start()]
            return text[start_pos:start_pos + 1500]

        # Parse Lab Information
        lab_data = ACSLabData()
        
        # Address (first two lines typically)
        addr_match = re.search(r'(\d+[^.]+\.)\s*\n([^,\n]+,\s*FL\s*\d{5})', text)
        if addr_match:
            lab_data.address = f"{addr_match.group(1)} {addr_match.group(2)}"
        
        lab_data.website = find(r'(www\.[^\s\n]+)')
        lab_data.dea_number = find(r'DEA No\.\s*([^\s\n]+)')
        lab_data.fl_license = find(r'FL License #\s*([^\s\n]+)')
        
        # Lab Director
        director_match = re.search(r'Lab Director/Principal Scientist\s*\n\s*([^\n]+)\s*\n\s*([^\n]+)', text, re.IGNORECASE)
        if director_match:
            lab_data.director = director_match.group(1).strip()
            lab_data.director_credentials = director_match.group(2).strip()
        
        # QA Info
        qa_match = re.search(r'QA By:\s*(\d+)\s+on\s+([^\n]+)', text)
        if qa_match:
            lab_data.qa_reviewer = qa_match.group(1)
            lab_data.qa_date = _parse_date(qa_match.group(2))
        
        lab_data.form_number = find(r'Form\s+([A-Z]\d+)')
        instance.lab_data = lab_data
        
        # Product Information
        instance.product_name = find(r'^([A-Z]{3}-[^-]+-[^-]+-[^-]+-[A-Z]-FL)')

        # Sample Matrix
        matrix_match = re.search(r'Sample Matrix:\s*\n\s*([^\n]+)', text, re.IGNORECASE)
        if matrix_match:
            instance.sample_matrix = matrix_match.group(1).strip()
        
        # Client Information
        client_section = find_section(r'Client Information:', r'Batch #')
        if client_section:
            lines = [line.strip() for line in client_section.split('\n') if line.strip()]
            if lines:
                instance.client = lines[0]
                if len(lines) > 1:
                    instance.client_address = ', '.join(lines[1:])
        
        # Batch and Sample Data
        instance.batch_number = find(r'Batch #\s*([^\n]+)')
        instance.batch_date = _parse_date(find(r'Batch Date:\s*([^\n]+)'))
        instance.seed_to_sale = find(r'Seed to Sale #\s*([^\n]+)')
        instance.lot_id = find(r'Lot ID:\s*([^\n]+)')
        instance.cultivar = find(r'Cultivars:\s*([^\n]+)')
        
        instance.order_number = find(r'Order #\s*([^\n]+)')
        instance.order_date = _parse_date(find(r'Order Date:\s*([^\n]+)'))
        instance.sample_number = find(r'Sample #\s*([^\n]+)')
        instance.sampling_date = _parse_date(find(r'Sampling Date:\s*([^\n]+)'))
        instance.completion_date = _parse_date(find(r'Completion Date:\s*([^\n]+)'))
        
        # Production Information
        instance.test_reg_state = find(r'Test Reg State:\s*([^\n]+)')
        instance.cultivation_facility = find(r'Cultivation Facility:\s*([^\n]+)')
        instance.production_facility = find(r'Production Facility:\s*([^\n]+)')
        instance.production_date = _parse_date(find(r'Production Date:\s*([^\n]+)'))
        
        # Physical Properties
        weight_str = find(r'Initial Gross Weight:\s*([^\n]+)')
        if weight_str and 'g' in weight_str.lower():
            instance.initial_gross_weight_g = _parse_float(weight_str)
        
        instance.number_of_units = int(_parse_float(find(r'Number of Units:\s*([^\n]+)')) or 0)
        instance.net_weight_per_unit_mg = _parse_float(find(r'Net Weight per Unit:\s*([^\n]+)'))
        instance.sampling_method = find(r'Sampling Method:\s*([^\n]+)')
        
        # Test Statuses
        status_section = find_section(r'Product Image', r'Potency\s*-')
        test_statuses = {}
        if status_section:
            for match in re.finditer(r'([A-Za-z\s&/]+?)\s+(Tested|Passed|Not Tested|Failed)', status_section, re.IGNORECASE):
                test_name = match.group(1).strip()
                status = match.group(2).strip().upper()
                test_statuses[test_name] = status
        instance.test_statuses = test_statuses
        
        # Potency Analysis
        potency_section = find_section(r'Potency\s*-\s*\d+', r'Moisture|Potency Summary')
        if potency_section:
            # Parse test info
            potency_info = ACSTestInfo()
            potency_info.specimen_weight = find(r'Specimen Weight:\s*([^\n]+)', 1) if find_section(r'Specimen Weight:', r'\n') else None
            potency_info.sop_method = find(r'(SOP\d+\.\d+[^)]*\))', 1) if find_section(r'SOP\d+', r'\)') else None
            
            # Personnel info
            prep_match = re.search(r'Prep\.\s*By:\s*(\d+)\s*\nDate:\s*([^\n]+)', potency_section)
            if prep_match:
                potency_info.prepared_by = prep_match.group(1)
                potency_info.prep_date = _parse_date(prep_match.group(2))
            
            analyzed_match = re.search(r'Analyzed By:\s*(\d+)\s*\nDate:\s*([^\n]+)', potency_section)
            if analyzed_match:
                potency_info.analyzed_by = analyzed_match.group(1)
                potency_info.analysis_date = _parse_date(analyzed_match.group(2))
            
            reviewed_match = re.search(r'Reviewed By:\s*(\d+)\s*\nDate:\s*([^\n]+)', potency_section)
            if reviewed_match:
                potency_info.reviewed_by = reviewed_match.group(1)
                potency_info.review_date = _parse_date(reviewed_match.group(2))
            
            batch_match = re.search(r'Lab Batch #:\s*([^\n]+)', potency_section)
            if batch_match:
                potency_info.lab_batch_number = batch_match.group(1).strip()
            
            instance.potency_test_info = potency_info
            
            # Parse analyte table
            analytes = []
            # Pattern for the data table: Name, Dilution, LOD, LOQ, Result(mg/g), Result(%)
            table_pattern = r'([A-Za-z0-9\-\+\s\(\)]+?)\s+([0-9\.]+)\s+([0-9\.E\-\+]+)\s+([0-9\.]+)\s+([0-9\.]+|<LOQ)\s+([0-9\.]+|<LOQ)'
            
            for match in re.finditer(table_pattern, potency_section):
                analyte = ACSAnalyte(
                    name=match.group(1).strip(),
                    dilution=_parse_float(match.group(2)),
                    lod_percent=_parse_float(match.group(3)),
                    loq_percent=_parse_float(match.group(4)),
                    result_mg_per_g=_parse_float(match.group(5)),
                    result_percent=_parse_float(match.group(6))
                )
                analytes.append(analyte)
            
            instance.potency_analytes = analytes
        
        # Moisture Analysis
        moisture_section = find_section(r'Moisture', r'Potency Summary|Terpenes Summary')
        if moisture_section:
            # Parse moisture test details
            moisture_info = ACSTestInfo()
            moisture_info.specimen_weight = find(r'Specimen Weight:\s*([^\n]+)', 1) if 'Specimen Weight:' in moisture_section else None
            moisture_info.dilution_factor = _parse_float(find(r'Dilution Factor:\s*([^\n]+)', 1)) if 'Dilution Factor:' in moisture_section else None
            
            # Moisture result
            moisture_match = re.search(r'Moisture\s+(\d+)\s+([0-9\.]+)', moisture_section)
            if moisture_match:
                instance.moisture_action_level = _parse_float(moisture_match.group(1))
                instance.moisture_percent = _parse_float(moisture_match.group(2))
            
            instance.moisture_test_info = moisture_info
        
        # Potency Summary
        summary_section = find_section(r'Potency Summary', r'Terpenes Summary|Lab Director')
        if summary_section:
            # Extract THC, CBD, CBG, and total cannabinoids with both % and mg
            thc_match = re.search(r'Total Active THC\s+([0-9\.]+)%\s+([0-9\.]+)\s*mg', summary_section)
            if thc_match:
                instance.total_active_thc_percent = _parse_float(thc_match.group(1))
                instance.total_active_thc_mg = _parse_float(thc_match.group(2))
            
            cbd_match = re.search(r'Total Active CBD\s+([0-9\.]+)%\s+([0-9\.]+)\s*mg', summary_section)
            if cbd_match:
                instance.total_active_cbd_percent = _parse_float(cbd_match.group(1))
                instance.total_active_cbd_mg = _parse_float(cbd_match.group(2))
            
            cbg_match = re.search(r'Total CBG\s+([0-9\.]+)%\s+([0-9\.]+)\s*mg', summary_section)
            if cbg_match:
                instance.total_cbg_percent = _parse_float(cbg_match.group(1))
                instance.total_cbg_mg = _parse_float(cbg_match.group(2))
            
            cannabinoids_match = re.search(r'Total Cannabinoids\s+([0-9\.]+)%\s+([0-9\.]+)\s*mg', summary_section)
            if cannabinoids_match:
                instance.total_cannabinoids_percent = _parse_float(cannabinoids_match.group(1))
                instance.total_cannabinoids_mg = _parse_float(cannabinoids_match.group(2))
        
        # Terpenes Summary
        terpenes_section = find_section(r'Terpenes Summary', r'Lab Director|Definitions')
        if terpenes_section:
            terpenes = []
            # Pattern: Name, Result(mg/g), Result(%)
            terpene_pattern = r'([A-Za-z\-\(\)\+\s]+?)\s+([0-9\.]+)\s+([0-9\.]+)%'
            
            for match in re.finditer(terpene_pattern, terpenes_section):
                terpene = ACSTerpene(
                    name=match.group(1).strip(),
                    result_mg_per_g=_parse_float(match.group(2)),
                    result_percent=_parse_float(match.group(3))
                )
                terpenes.append(terpene)
            
            instance.terpenes = terpenes
            
            # Total terpenes
            total_match = re.search(r'Total Terpenes:\s*([0-9\.]+)%', terpenes_section)
            if total_match:
                instance.total_terpenes_percent = _parse_float(total_match.group(1))
        
        return instance
    
    def to_serializable_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper datetime serialization."""
        def serialize_value(value):
            if isinstance(value, datetime):
                return value.isoformat()
            elif hasattr(value, '__dict__'):
                # Handle dataclasses
                result = {}
                for k, v in value.__dict__.items():
                    result[k] = serialize_value(v)
                return result
            elif isinstance(value, list):
                return [serialize_value(item) for item in value]
            elif isinstance(value, dict):
                return {k: serialize_value(v) for k, v in value.items()}
            else:
                return value

        # Ensure the result is always a dictionary
        if hasattr(self, '__dict__'):
            result = {}
            for k, v in self.__dict__.items():
                result[k] = serialize_value(v)
            return result
        else:
            return {}
    

    def to_json1(self) -> str:
        """Serialize the COA data to JSON."""
        return json.dumps(self.to_serializable_dict(), indent=2)