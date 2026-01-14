"""Parser for extracting image data from HP CAP XML."""

from typing import Any, Dict, List
from xml.etree.ElementTree import Element
from hp_cap_parser.models import Image

from .base import BaseParser


class ImagesParser(BaseParser):
    """Parser for extracting image information from HP CAP XML."""
    
    def parse(self, xml_element: Element, product_number) -> Image:
        """Parse image data from the XML element.
        
        Args:
            xml_element: The XML element containing image data.
            
        Returns:
            A dictionary containing parsed image information.
        """
        images=[]
        for img in xml_element.findall('.//images/image'):
            images.append(Image.from_xml_element(img, product_number))
        return images
    
    def get_section_name(self) -> str:
        """Get the section name for images.
        
        Returns:
            The section name 'images'.
        """
        return 'images'
