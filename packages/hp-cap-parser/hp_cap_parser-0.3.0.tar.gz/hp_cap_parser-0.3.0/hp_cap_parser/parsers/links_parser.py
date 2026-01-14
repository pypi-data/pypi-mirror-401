"""Parser for extracting link data from HP CAP XML."""

from typing import Any, Dict, List
from xml.etree.ElementTree import Element

from hp_cap_parser.models import Link

from .base import BaseParser


class LinksParser(BaseParser):
    """Parser for extracting link information from HP CAP XML."""
    
    def parse(self, xml_element: Element, product_number: str) -> List[Link]:
        """Parse link data from the XML element.
        
        Args:
            xml_element: The XML element containing link data.
            product_number: The product number to associate with links.
            
        Returns:
            A list of Link objects.
        """
        links = []
        for link in xml_element.findall('.//links/link'):
            links.append(Link.from_xml_element(link, product_number))
        return links
    
    def get_section_name(self) -> str:
        """Get the section name for links.
        
        Returns:
            The section name 'links'.
        """
        return 'links'
