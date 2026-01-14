"""Parser for extracting product data from HP CAP XML."""

from typing import Any, Dict
from xml.etree.ElementTree import Element

from hp_cap_parser.models import Product

from .base import BaseParser


class ProductParser(BaseParser):
    """Parser for extracting product information from HP CAP XML."""
    
    def parse(self, xml_element: Element) -> Product:
     """
        Parse product data from XML element
        
        Args:
            element: XML item element
            
        Returns:
            Product data model
        """
     return Product.from_xml_element(xml_element)
        
    
    def get_section_name(self) -> str:
        """Get the section name for product data.
        
        Returns:
            The section name 'product'.
        """
        return 'product'
