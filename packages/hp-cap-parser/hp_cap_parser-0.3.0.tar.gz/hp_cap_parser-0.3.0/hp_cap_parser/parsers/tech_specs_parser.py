"""Parser for extracting technical specifications from HP CAP XML."""

from typing import Any, Dict, List
from xml.etree.ElementTree import Element

from hp_cap_parser.models import TechSpec

from .base import BaseParser


class TechSpecsParser(BaseParser):
    """Parser for extracting technical specifications from HP CAP XML."""
    
    def parse(self, xml_element: Element, product_number: str) -> List[TechSpec]:
        """Parse technical specifications data from the XML element.
        
        Args:
            xml_element: The XML element containing tech specs data.
            product_number: The product number to associate with tech specs.
                
        Returns:
            A list of TechSpec objects.
        """
        tech_specs_list = []
        
        # Find the tech_specs section
        for tech_specs in xml_element.findall('.//tech_specs'):
            # Process all subsections within tech_specs
            for subsection in tech_specs:
                section_name = subsection.tag
                for element in subsection:
                    tech_specs_list.append(
                        TechSpec.from_xml_element(
                            element, product_number, section_name, element.tag
                        )
                    )
        
        return tech_specs_list
    
    def get_section_name(self) -> str:
        """Get the section name for tech specs.
        
        Returns:
            The section name 'tech_specs'.
        """
        return 'tech_specs'
