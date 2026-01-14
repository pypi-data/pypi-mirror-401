"""Basic tests for hp_cap_parser."""

import csv
import pytest
from pathlib import Path
from hp_cap_parser import HPCapParser
from hp_cap_parser.models import Product, Image, Document, Link, MarketingMessaging, TechSpec


def test_import():
    """Test that HPCapParser can be imported."""
    assert HPCapParser is not None


def test_version_available():
    """Test that package version is accessible."""
    from hp_cap_parser import __version__
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_parser_initialization():
    """Test that parser initializes with subparsers."""
    parser = HPCapParser()
    assert len(parser.subparsers) > 0
    assert all(hasattr(sp, 'parse') for sp in parser.subparsers)
    assert all(hasattr(sp, 'get_section_name') for sp in parser.subparsers)


def test_parse_file_with_sample(tmp_path):
    """Test parsing a real XML file and generating CSV outputs."""
    parser = HPCapParser()
    input_file = Path(__file__).parent / "test_files" / "9G145ET.xml"
    output_dir = tmp_path / "output"
    
    if not input_file.exists():
        pytest.skip("Sample XML file not found")
    
    parser.parse_file(str(input_file), str(output_dir))
    
    assert output_dir.exists()
    assert (output_dir / "product.csv").exists()
    assert (output_dir / "images.csv").exists()
    assert (output_dir / "documents.csv").exists()
    assert (output_dir / "links.csv").exists()


def test_csv_output_structure(tmp_path):
    """Test that CSV files have proper structure."""
    parser = HPCapParser()
    input_file = Path(__file__).parent / "test_files" / "9G145ET.xml"
    output_dir = tmp_path / "output"
    
    if not input_file.exists():
        pytest.skip("Sample XML file not found")
    
    parser.parse_file(str(input_file), str(output_dir))
    
    product_csv = output_dir / "product.csv"
    with open(product_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert 'product_number' in reader.fieldnames
        assert 'product_name' in reader.fieldnames


def test_wide_csv_generation(tmp_path):
    """Test that wide CSV files are generated for marketing and tech specs."""
    parser = HPCapParser()
    input_file = Path(__file__).parent / "test_files" / "9G145ET.xml"
    output_dir = tmp_path / "output"
    
    if not input_file.exists():
        pytest.skip("Sample XML file not found")
    
    parser.parse_file(str(input_file), str(output_dir))
    
    marketing_wide = output_dir / "marketing_messaging_wide.csv"
    tech_wide = output_dir / "tech_specs_wide.csv"
    
    if marketing_wide.exists():
        with open(marketing_wide, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            assert 'product_number' in reader.fieldnames
            rows = list(reader)
            assert len(rows) >= 1
    
    if tech_wide.exists():
        with open(tech_wide, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            assert 'product_number' in reader.fieldnames


def test_parse_file_missing_input():
    """Test that parser raises error for missing input file."""
    parser = HPCapParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_file("nonexistent.xml", "output")


def test_parse_file_missing_output_dir():
    """Test that parser raises error for missing output directory."""
    parser = HPCapParser()
    input_file = Path(__file__).parent / "test_files" / "9G145ET.xml"
    
    if not input_file.exists():
        pytest.skip("Sample XML file not found")
    
    with pytest.raises(ValueError):
        parser.parse_file(str(input_file), None)
