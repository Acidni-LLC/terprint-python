
from __future__ import annotations
from binascii import Error
import re
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from bcolors import bcolors

try:
    from dateutil import parser as date_parser  # type: ignore
    _HAS_DATEUTIL = True
except Exception:
    _HAS_DATEUTIL = False


def _parse_date(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    if _HAS_DATEUTIL:
        try:
            return date_parser.parse(s)
        except Exception:
            return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y-%m-%d %H:%M", "%m/%d/%Y %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        except Exception:
            return None
    return None


def _parse_float(s: Optional[str]) -> Optional[float]:
    if not s:
        return None
    s = s.strip().replace(",", "")
    m = re.search(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?", s)
    if not m:
        return None
    try:
        return float(m.group(0))
    except Exception:
        return None


@dataclass
class AnalyteResult:
    name: str
    result_mg_per_g: Optional[float] = None     # mg/g (if available)
    percent: Optional[float] = None            # %
    mg_per_unit: Optional[float] = None        # mg per unit (if available)
    lod: Optional[float] = None                # LOD value (if present)
    notes: Optional[str] = None


@dataclass
class TerpeneResult:
    name: str
    result_ug_per_g: Optional[float] = None    # ug/g (as seen in some reports)
    percent: Optional[float] = None


@dataclass
class COA:
    # Metadata
    product_name: Optional[str] = None
    description: Optional[str] = None
    matrix: Optional[str] = None
    client: Optional[str] = None
    client_address: Optional[str] = None
    order_number: Optional[str] = None
    sample_number: Optional[str] = None
    receipt_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    sampling_date: Optional[datetime] = None
    sampled_gross_weight_g: Optional[float] = None
    sampling_method: Optional[str] = None

    # Batch & production ids
    batch_number: Optional[str] = None
    batch_date: Optional[datetime] = None
    seed_to_sale: Optional[str] = None
    lot_id: Optional[str] = None
    cultivars: Optional[List[str]] = field(default_factory=list)
    test_reg_state: Optional[str] = None
    cultivation_facility: Optional[str] = None
    production_facility: Optional[str] = None
    production_date: Optional[datetime] = None

    # Summary statuses: e.g. {"Potency": "TESTED", "Mycotoxins": "PASSED", ...}
    summary_status: Dict[str, str] = field(default_factory=dict)

    # Potency details
    potency_analytes: List[AnalyteResult] = field(default_factory=list)
    total_thc_percent: Optional[float] = None
    total_cbd_percent: Optional[float] = None
    total_cannabinoids_percent: Optional[float] = None
    total_thc_mg_per_unit: Optional[float] = None
    total_cannabinoids_mg_per_unit: Optional[float] = None

    # Terpenes
    terpenes: List[TerpeneResult] = field(default_factory=list)
    total_terpenes_percent: Optional[float] = None

    # Lab info
    lab_name: Optional[str] = None
    lab_license: Optional[str] = None
    lab_director: Optional[str] = None

    # raw
    raw_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
            # convert lists of dataclasses
            if isinstance(v, list):
                new_list = []
                for item in v:
                    if hasattr(item, "__dict__"):
                        new_list.append({**item.__dict__})
                    else:
                        new_list.append(item)
                d[k] = new_list
        return d

    def __str__(self) -> str:
        return f"COA(product={self.product_name!r}, sample={self.sample_number!r}, batch={self.batch_number!r})"
    def to_json(self, *, indent: Optional[int] = 2, ensure_ascii: bool = False) -> str:
        """
        Return a JSON string for this COA.
        - indent: pretty-print indent (None for compact)
        - ensure_ascii: pass-through to json.dumps (False to keep unicode)
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=ensure_ascii)

    def save_json(self, path: str, *, indent: Optional[int] = 2, ensure_ascii: bool = False) -> None:
        """
        Write the JSON representation to `path`.
        Overwrites existing file.
        """
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=indent, ensure_ascii=ensure_ascii)
    @classmethod
    def from_text(cls, text: str) -> "COA":
        """
        Heuristic parser for COA-like text. This attempts to extract common fields and lists.
        Not guaranteed to capture every layout exactly, but works for the sample you provided.
        """
        if not text:
            return cls(raw_text=text)
        def find_byline(intext: str, texttofind: str, aboveorbelow: str) -> Optional[str]:
            try: 
                text = ""
                linenumcounter = 0
                offset =0
                linenum = 0
                if(aboveorbelow == "above"):
                    offset = -1
                if(aboveorbelow == "below"):
                    offset = 1 
                for line in intext.splitlines():
                    linenumcounter = linenumcounter + 1
                #    print("if text in line :" +texttofind +"|" + line)
                    if texttofind == line:
                        linenum = linenumcounter +offset
                        print ('found at line:', linenum)
                linenumcounter = 0
                for line in intext.splitlines():
                    linenumcounter = linenumcounter + 1
                    if linenumcounter == linenum:
                        text = line.strip()
                        print ('found:', text)
                
            except Error as ex:
                
                print(bcolors.FAIL + "Error : "+Error.description + bcolors.ENDC)
 
                
            return text

        def find_single(pattern: str) -> Optional[str]:
            m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
            return m.group(1).strip() if m else None

        def find_all_rows(section_header_regex: str, row_pattern: str) -> List[re.Match]:
            # find header, then capture following lines matching row pattern until blank line or next header
            hdr = re.search(section_header_regex, text, flags=re.IGNORECASE)
            if not hdr:
                return []
            start = hdr.end()
            tail = text[start:start + 2000]  # limit scan size a bit (heuristic)
            return list(re.finditer(row_pattern, tail, flags=re.IGNORECASE | re.MULTILINE))

        # Basic metadata
        product_name = find_byline(text,"Cannabis FL","above")
        order_number = find_single(r"Order\s*#:\s*([^\r\n]+)") or find_single(r"Order #\s*([^\r\n]+)")
        sample_number = find_single(r"Sample\s*#:\s*([^\r\n]+)") or find_single(r"Sample #:\s*([^\r\n]+)")
        receipt_date = _parse_date(find_single(r"Receipt Date:\s*([^\r\n]+)"))
        completion_date = _parse_date(find_single(r"Completion Date:\s*([^\r\n]+)"))
        sampling_date = _parse_date(find_single(r"Sampling Date:\s*([^\r\n]+)"))

        sampled_gross_weight_str = find_single(r"Sampled Gross Weight:\s*([^\r\n]+)") or find_single(r"Sampled Gross Weight:\s*([^\r\n]+)")
        sampled_gross_weight_g = None
        if sampled_gross_weight_str:
            # extract numeric and unit
            m = re.search(r"([-+]?\d*\.?\d+)\s*(g|kg|mg)?", sampled_gross_weight_str.replace(",", ""), flags=re.IGNORECASE)
            if m:
                val = float(m.group(1))
                unit = (m.group(2) or "g").lower()
                if unit == "g":
                    sampled_gross_weight_g = val
                elif unit == "mg":
                    sampled_gross_weight_g = val / 1000.0
                elif unit == "kg":
                    sampled_gross_weight_g = val * 1000.0

        sampling_method = find_single(r"Sampling Method:\s*([^\r\n]+)")

        # Batch/product info
        batch_number = find_single(r"Batch\s*#:\s*([^\r\n]+)") or find_single(r"Batch\s*#\s*:\s*([^\r\n]+)")
        batch_date = _parse_date(find_single(r"Batch Date:\s*([^\r\n]+)"))
        seed_to_sale = find_single(r"Seed to Sale\s*#:\s*([^\r\n]+)")
        lot_id = find_single(r"Lot ID:\s*([^\r\n]+)")
        cultivars_raw = find_single(r"Cultivars:\s*([^\r\n]+)")
        cultivars = [c.strip() for c in cultivars_raw.split(",")] if cultivars_raw else []

        test_reg_state = find_single(r"Test Reg State:\s*([^\r\n]+)")
        cultivation_facility = find_single(r"Cultivation Facility:\s*([^\r\n]+)")
        production_facility = find_single(r"Production Facility:\s*([^\r\n]+)")
        production_date = _parse_date(find_single(r"Production Date:\s*([^\r\n]+)"))

        # Summary statuses (top of file in your sample)
        summary_status = {}
        # look for lines that have uppercase words and PASSED/TESTED/NOT TESTED/NOT TESTED etc
        for m in re.finditer(r"([A-Z][A-Za-z &/]+)\s*\n\s*(TESTED|PASSED|NOT TESTED|NOT TESTED|NOT\s*TESTED|FAILED|N/A)", text, flags=re.IGNORECASE):
            k = m.group(1).strip()
            v = m.group(2).strip().upper()
            summary_status[k] = v
        # Also try inline forms like "Potency TESTED"
        for m in re.finditer(r"\b(Potency|Mycotoxins|Terpenes|Microbials|Pesticides|Total Yeast and Mold|Total Contaminant Load|Water Activity|Residual Solvents|Moisture|Heavy Metals|Filth and Foreign Material|Total Aerobic Bacteria|Homogeneity)\b[^\S\r\n]*\n?[^\S\r\n]*(TESTED|PASSED|NOT TESTED|NOT TESTED|FAILED|N/A)", text, flags=re.IGNORECASE):
            summary_status[m.group(1).strip()] = m.group(2).strip().upper()

        # Potency analytes: look for table-like rows: Name followed by numeric columns
        potency_analytes: List[AnalyteResult] = []
        # Rough pattern: analyte name at line start followed by numbers across columns
        for m in re.finditer(r"^\s*([A-Za-z0-9\-\s\(\)]+?)\s{2,}([<>A-Za-z0-9\.\-\/]+)\s+([0-9\.\-NDAa/]+)?\s+([0-9\.\-NDAa/]+)?\s*([0-9\.\-NDAa/]+)?", text, flags=re.MULTILINE):
            name = m.group(1).strip()
            cols = [m.group(i) for i in range(2, 6)]
            # attempt to assign columns heuristically
            r_mg_g = _parse_float(cols[0])
            pct = _parse_float(cols[1]) or _parse_float(cols[2])
            mg_unit = _parse_float(cols[2]) or _parse_float(cols[3])
            potency_analytes.append(AnalyteResult(name=name, result_mg_per_g=r_mg_g, percent=pct, mg_per_unit=mg_unit))

        # If no analytes found with above heuristic, also scan some common labels individually
        if not potency_analytes:
            # capture lines like "THCA 894 10.7 1.07 0.000008"
            for m in re.finditer(r"^\s*([A-Za-z0-9\-\+ ]{2,20})\s+([0-9\.\-<>NDAa]+)\s+([0-9\.\-<>NDAa]+)\s+([0-9\.\-<>NDAa]+)\s+([0-9\.\-<>NDAa]+)", text, flags=re.MULTILINE):
                name = m.group(1).strip()
                r_mg_g = _parse_float(m.group(2))
                pct = _parse_float(m.group(3))
                mg_unit = _parse_float(m.group(4))
                lod = _parse_float(m.group(5))
                excludeList = {"lab director"}
                cr = AnalyteResult(name=name, result_mg_per_g=r_mg_g, percent=pct, mg_per_unit=mg_unit, lod=lod)
                if(cr.name.lower() not in excludeList):
                    potency_analytes.append(cr)

        # Potency summary totals
        total_thc_percent = _parse_float(find_single(r"Total THC\s*[:\-]?\s*([0-9\.\%]+)")) or _parse_float(find_single(r"Total THC\s*[:\-]?\s*([0-9\.\-]+)%"))
        total_cbd_percent = _parse_float(find_single(r"Total CBD\s*[:\-]?\s*([0-9\.\%]+)"))
        total_cannabinoids_percent = _parse_float(find_single(r"Total Cannabinoids\s*[:\-]?\s*([0-9\.\%]+)"))
        total_thc_mg_per_unit = _parse_float(find_single(r"Total THC/Unit\s*[:\-]?\s*([0-9\.\sA-Za-z]+)")) or _parse_float(find_single(r"Total THC/Unit\s*([0-9\.\-]+)"))
        total_cannabinoids_mg_per_unit = _parse_float(find_single(r"Total Cannabinoids/Unit\s*[:\-]?\s*([0-9\.\-]+)"))

        # Terpenes: scan lines showing name and two numeric columns (result and percent)
        terpenes: List[TerpeneResult] = []
        for m in re.finditer(r"^\s*([A-Za-z\-\s]+)\s+([0-9\.\-]+)\s+([0-9\.\-]+)", text, flags=re.MULTILINE):
            name = m.group(1).strip()
            val1 = _parse_float(m.group(2))
            val2 = _parse_float(m.group(3))
            # Heuristic: if second value is large (1000s) it's likely ug/g; keep both as fields
            # Many reports place ug/g then % or ug/g then mg/g — store as ug/g and percent (if percent looks like fraction)
            excludeList = {"thca","cbga","lab director","cbg"}
            tr = TerpeneResult(name=name, result_ug_per_g=val1, percent=val2)
            if(tr.name.lower() not in excludeList):
                terpenes.append(tr)

        # total terpenes
        total_terpenes_percent = _parse_float(find_single(r"Total Terpenes[:\s]*([0-9\.\%]+)")) or _parse_float(find_single(r"Total Terpenes[:\s]*([0-9\.\-]+)%"))

        # lab info
        lab_name = find_single(r"^(.+?)\s*\n.*Lic #",) or find_single(r"Method Testing Laboratories") or find_single(r"ACS Laboratory")
        lab_license = find_single(r"Lic #\s*([A-Za-z0-9\-\_]+)")
        lab_director = find_single(r"Lab Director\s*[:\s]*([^\r\n]+)")

        return cls(
            product_name=product_name,
            description=find_single(r"Description:\s*([^\r\n]+)"),
            matrix=find_single(r"Matrix:\s*([^\r\n]+)"),
            client=find_single(r"Client:\s*([^\r\n]+)"),
            client_address=find_single(r"Address:\s*([^\r\n]+)"),
            order_number=order_number,
            sample_number=sample_number,
            receipt_date=receipt_date,
            completion_date=completion_date,
            sampling_date=sampling_date,
            sampled_gross_weight_g=sampled_gross_weight_g,
            sampling_method=sampling_method,
            batch_number=batch_number,
            batch_date=batch_date,
            seed_to_sale=seed_to_sale,
            lot_id=lot_id,
            cultivars=cultivars,
            test_reg_state=test_reg_state,
            cultivation_facility=cultivation_facility,
            production_facility=production_facility,
            production_date=production_date,
            summary_status=summary_status,
            total_thc_percent=total_thc_percent,
            total_cbd_percent=total_cbd_percent,
            total_cannabinoids_percent=total_cannabinoids_percent,
            total_thc_mg_per_unit=total_thc_mg_per_unit,
            total_cannabinoids_mg_per_unit=total_cannabinoids_mg_per_unit,
            total_terpenes_percent=total_terpenes_percent,
            lab_name=lab_name,
            lab_license=lab_license,
            lab_director=lab_director,
            terpenes=terpenes,
            potency_analytes=potency_analytes,
            raw_text=text
        )