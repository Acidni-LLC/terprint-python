from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Tuple
import re

try:
    # dateutil is very flexible; use if available
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
    # Try a few common formats
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    # Last ditch: try to extract yyyy-mm-dd via regex
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        except Exception:
            return None
    return None


def _parse_number(s: Optional[str]) -> Optional[float]:
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    s = s.replace(",", "")
    m = re.search(r"([-+]?\d*\.?\d+)", s)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None


def _parse_weight_to_grams(s: Optional[str]) -> Optional[float]:
    """
    Parse strings like '684.000 g' or '3500.000 mg' and convert to grams.
    Returns grams as float, or None.
    """
    if not s:
        return None
    s = s.strip().lower()
    m = re.search(r"([-+]?\d*\.?\d+)\s*(mg|g|kg)?", s)
    if not m:
        return None
    val = float(m.group(1))
    unit = m.group(2) or "g"
    if unit == "mg":
        return val / 1000.0
    if unit == "kg":
        return val * 1000.0
    return val  # grams


@dataclass
class Batch:
    batch_number: Optional[str] = None
    batch_date: Optional[datetime] = None
    seed_to_sale: Optional[str] = None
    lot_id: Optional[str] = None
    cultivars: Optional[List[str]] = field(default_factory=list)
    test_reg_state: Optional[str] = None
    cultivation_facility: Optional[str] = None
    production_facility: Optional[str] = None
    production_date: Optional[datetime] = None
    order_number: Optional[str] = None
    order_date: Optional[datetime] = None
    sample_number: Optional[str] = None
    sampling_date: Optional[datetime] = None
    lab_batch_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    initial_gross_weight_g: Optional[float] = None  # grams
    number_of_units: Optional[int] = None
    net_weight_per_unit_mg: Optional[float] = None  # mg
    sampling_method: Optional[str] = None
    raw_text: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        # convert datetimes to ISO strings for serialization
        for k, v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
        return d

    def __str__(self) -> str:
        return f"Batch(batch_number={self.batch_number!r}, batch_date={self.batch_date!r})"

    @classmethod
    def from_text(cls, text: str) -> "Batch":
        """
        Parse a report text and return a Batch instance.
        Fields not found will remain None.
        """
        if not text:
            return cls(raw_text=text)

        def _find(pattern: str) -> Optional[str]:
            m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
            return m.group(1).strip() if m else None

        batch_number = _find(r"Batch\s*#\s*([^\r\n]+)")
        batch_date = _parse_date(_find(r"Batch Date:\s*([^\r\n]+)"))
        seed_to_sale = _find(r"Seed to Sale\s*#\s*([^\r\n]+)")
        lot_id = _find(r"Lot ID:\s*([^\r\n]+)")
        cultivars_raw = _find(r"Cultivars:\s*([^\r\n]+)")
        cultivars = [c.strip() for c in cultivars_raw.split(",")] if cultivars_raw else []
        test_reg_state = _find(r"Test Reg State:\s*([^\r\n]+)")
        cultivation_facility = _find(r"Cultivation Facility:\s*([^\r\n]+)")
        production_facility = _find(r"Production Facility:\s*([^\r\n]+)")
        production_date = _parse_date(_find(r"Production Date:\s*([^\r\n]+)"))
        order_number = _find(r"Order\s*#\s*([^\r\n]+)")
        order_date = _parse_date(_find(r"Order Date:\s*([^\r\n]+)"))
        sample_number = _find(r"Sample\s*#\s*([^\r\n]+)")
        sampling_date = _parse_date(_find(r"Sampling Date:\s*([^\r\n]+)"))
        lab_batch_date = _parse_date(_find(r"Lab Batch Date:\s*([^\r\n]+)"))
        completion_date = _parse_date(_find(r"Completion Date:\s*([^\r\n]+)"))
        initial_gross_weight_g = _parse_weight_to_grams(_find(r"Initial Gross Weight:\s*([^\r\n]+)"))
        number_of_units_val = _find(r"Number of Units:\s*([^\r\n]+)")
        number_of_units = None
        if number_of_units_val:
            try:
                number_of_units = int(re.sub(r"[^\d\-]", "", number_of_units_val))
            except Exception:
                number_of_units = None
        net_weight_str = _find(r"Net Weight per Unit:\s*([^\r\n]+)")
        # keep net weight stored as mg when possible
        net_weight_per_unit_mg = None
        if net_weight_str:
            # parse numeric and unit
            m = re.search(r"([-+]?\d*\.?\d+)\s*(mg|g|kg)?", net_weight_str.strip(), flags=re.IGNORECASE)
            if m:
                val = float(m.group(1))
                unit = (m.group(2) or "mg").lower()
                if unit == "mg":
                    net_weight_per_unit_mg = val
                elif unit == "g":
                    net_weight_per_unit_mg = val * 1000.0
                elif unit == "kg":
                    net_weight_per_unit_mg = val * 1_000_000.0

        sampling_method = _find(r"Sampling Method:\s*([^\r\n]+)")

        return cls(
            batch_number=batch_number,
            batch_date=batch_date,
            seed_to_sale=seed_to_sale,
            lot_id=lot_id,
            cultivars=cultivars,
            test_reg_state=test_reg_state,
            cultivation_facility=cultivation_facility,
            production_facility=production_facility,
            production_date=production_date,
            order_number=order_number,
            order_date=order_date,
            sample_number=sample_number,
            sampling_date=sampling_date,
            lab_batch_date=lab_batch_date,
            completion_date=completion_date,
            initial_gross_weight_g=initial_gross_weight_g,
            number_of_units=number_of_units,
            net_weight_per_unit_mg=net_weight_per_unit_mg,
            sampling_method=sampling_method,
            raw_text=text,
        )