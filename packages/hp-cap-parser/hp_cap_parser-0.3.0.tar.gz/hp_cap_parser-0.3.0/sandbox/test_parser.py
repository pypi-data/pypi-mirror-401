"""Sandbox script for testing the HP CAP parser."""

from hp_cap_parser import HPCapParser

# Example usage
if __name__ == "__main__":
    parser = HPCapParser()
    parser.parse_file("tests/test_files/9G145ET.xml", "test_output")
