"""Core parser implementation for HP Content Aggregator for Products (CAP) data."""

import csv
import xml.etree.ElementTree as ET
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from .parsers import BaseParser, ImagesParser, ProductParser, DocumentsParser, LinksParser, MarketingMessagingParser, TechSpecsParser


class HPCapParser:
    """Parser for HP Content Aggregator for Products (CAP) XML data files.
    
    This main parser coordinates multiple subparsers to extract different
    sections of the nested XML structure.
    """
    
    def __init__(self):
        self.subparsers: List[BaseParser] = [
            ImagesParser(),
            DocumentsParser(),
            LinksParser(),
            MarketingMessagingParser(),
            TechSpecsParser()
        ]
    
    def parse_file(self, input_file_path: str, output_dir_path: str = None) -> Dict[str, Any]:
        input_path = Path(input_file_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file_path}")
        if not output_dir_path:
            raise ValueError("Output directory path must be provided.")
        if not Path(output_dir_path).exists():
            Path(output_dir_path).mkdir(parents=True, exist_ok=True)
        
        tree = ET.parse(input_file_path)
        root = tree.getroot()

        product = ProductParser().parse(root)
        data = {'product': product}

        self._write_section_to_csv('product', asdict(product), Path(output_dir_path))

        for parser in self.subparsers:
            section_name = parser.get_section_name()
            section_data = parser.parse(root, product.product_number)
            data[section_name] = section_data
            self._write_section_to_csv(section_name, section_data, Path(output_dir_path))

        if marketing_messaging := data.get('marketing_messaging'):
            self._write_wide_csv(marketing_messaging, Path(output_dir_path) / "marketing_messaging_wide.csv")
        
        if tech_specs := data.get('tech_specs'):
            self._write_wide_csv(tech_specs, Path(output_dir_path) / "tech_specs_wide.csv")
        
        return data
    
    def parse_files_batch(self, input_file_paths: List[str], output_dir_path: str) -> None:
        output_dir = Path(output_dir_path)
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
        
        all_marketing_rows = []
        all_tech_rows = []
        
        for input_file_path in input_file_paths:
            input_path = Path(input_file_path)
            if not input_path.exists():
                continue
            
            tree = ET.parse(input_file_path)
            root = tree.getroot()
            
            product = ProductParser().parse(root)
            self._write_section_to_csv('product', asdict(product), output_dir)
            
            for parser in self.subparsers:
                section_name = parser.get_section_name()
                section_data = parser.parse(root, product.product_number)
                
                if section_name == 'marketing_messaging' and section_data:
                    all_marketing_rows.append(section_data)
                elif section_name == 'tech_specs' and section_data:
                    all_tech_rows.append(section_data)
                else:
                    self._write_section_to_csv(section_name, section_data, output_dir)
        
        if all_marketing_rows:
            self._write_wide_csv_batch(all_marketing_rows, output_dir / "marketing_messaging_wide.csv")
        
        if all_tech_rows:
            self._write_wide_csv_batch(all_tech_rows, output_dir / "tech_specs_wide.csv")
    
    def _write_section_to_csv(self, section_name: str, section_data: Any, output_dir: Path) -> None:
        output_file = output_dir / f"{section_name}.csv"
        write_header = not output_file.exists()
        
        with output_file.open(mode='a', newline='', encoding='utf-8') as csvfile:
            if isinstance(section_data, list) and section_data:
                fieldnames = asdict(section_data[0]).keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                for item in section_data:
                    writer.writerow(asdict(item))
            elif isinstance(section_data, dict):
                fieldnames = section_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow(section_data)

    def _build_wide_row(self, data: List[Any]) -> Dict[str, str]:
        product_number = data[0].product_number
        row = {'product_number': product_number}
        for item in data:
            column_name = f"{item.label} ({item.tag_name})"
            row[column_name] = item.text_value
        return row

    def _read_existing_csv(self, output_path: Path) -> Tuple[List[str], List[Dict]]:
        if not output_path.exists():
            return [], []
        
        with output_path.open(mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
        return fieldnames, rows

    def _merge_fieldnames(self, existing_fieldnames: List[str], row: Dict[str, str]) -> List[str]:
        if not existing_fieldnames:
            return list(row.keys())
        
        new_fieldnames = [f for f in row.keys() if f not in existing_fieldnames]
        return existing_fieldnames + new_fieldnames

    def _write_wide_csv(self, data: List[Any], output_file_path: Path) -> None:
        if not data:
            return
        
        row = self._build_wide_row(data)
        existing_fieldnames, existing_rows = self._read_existing_csv(output_file_path)
        fieldnames = self._merge_fieldnames(existing_fieldnames, row)
        
        with output_file_path.open(mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for existing_row in existing_rows:
                writer.writerow(existing_row)
            writer.writerow(row)
    
    def _write_wide_csv_batch(self, data_list: List[List[Any]], output_file_path: Path) -> None:
        if not data_list:
            return
        
        all_rows = []
        all_fieldnames_set = set()
        
        for data in data_list:
            if data:
                row = self._build_wide_row(data)
                all_rows.append(row)
                all_fieldnames_set.update(row.keys())
        
        if not all_rows:
            return
        
        existing_fieldnames, existing_rows = self._read_existing_csv(output_file_path)
        
        if existing_fieldnames:
            all_fieldnames_set.update(existing_fieldnames)
            fieldnames = existing_fieldnames + [f for f in all_fieldnames_set if f not in existing_fieldnames]
        else:
            fieldnames = ['product_number'] + [f for f in all_fieldnames_set if f != 'product_number']
        
        with output_file_path.open(mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for existing_row in existing_rows:
                writer.writerow(existing_row)
            for row in all_rows:
                writer.writerow(row)
            
            
        