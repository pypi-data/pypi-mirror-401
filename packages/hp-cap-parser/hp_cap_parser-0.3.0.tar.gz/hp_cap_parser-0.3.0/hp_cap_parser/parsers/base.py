"""Base parser class for HP CAP XML subparsers."""

from abc import ABC, abstractmethod
from typing import Any, Dict
from xml.etree.ElementTree import Element


class BaseParser(ABC):
    """Abstract base class for XML subparsers.
    
    Each subparser is responsible for extracting and processing
    a specific section of the nested HP CAP XML structure.
    """
    
    @abstractmethod
    def parse(self, xml_element: Element) -> Dict[str, Any]:
        """Parse a section of the XML tree.
        
        Args:
            xml_element: The XML element to parse.
            
        Returns:
            A dictionary containing the parsed data from this section.
        """
        pass
    
    @abstractmethod
    def get_section_name(self) -> str:
        """Get the name of the section this parser handles.
        
        Returns:
            The section name (e.g., 'images', 'product').
        """
        pass
