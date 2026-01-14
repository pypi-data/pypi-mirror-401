"""Parser for extracting document data from HP CAP XML."""

from typing import Any, Dict, List
from xml.etree.ElementTree import Element

from hp_cap_parser.models import Document

from .base import BaseParser


class DocumentsParser(BaseParser):
    """Parser for extracting document information from HP CAP XML."""
    
    def parse(self, xml_element: Element, product_number: str) -> List[Document]:
        """Parse document data from the XML element.
        
        Args:
            xml_element: The XML element containing document data.
            product_number: The product number to associate with documents.
            
        Returns:
            A list of Document objects.
        """
        documents = []
        for doc in xml_element.findall('.//documents/document'):
            documents.append(Document.from_xml_element(doc, product_number))
        return documents
    
    def get_section_name(self) -> str:
        """Get the section name for documents.
        
        Returns:
            The section name 'documents'.
        """
        return 'documents'
