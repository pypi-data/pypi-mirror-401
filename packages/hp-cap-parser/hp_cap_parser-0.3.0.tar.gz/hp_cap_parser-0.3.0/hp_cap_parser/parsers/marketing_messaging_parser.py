"""Parser for extracting link data from HP CAP XML."""

from typing import Any, Dict, List
from xml.etree.ElementTree import Element

from hp_cap_parser.models import MarketingMessaging

from .base import BaseParser


class MarketingMessagingParser(BaseParser):
    """Parser for extracting marketing messaging information from HP CAP XML."""
    
    def parse(self, xml_element: Element, product_number: str) -> List[MarketingMessaging]:
        """Parse marketing messaging data from the XML element.
        
        Args:
            xml_element: The XML element containing marketing messaging data.
            product_number: The product number to associate with marketing messaging.
                
        Returns:
            A list of MarketingMessaging objects.
        """
        marketing_messaging_list = []
        
        # Find the content section
        for content in xml_element.findall('.//content'):
            # Process <features> section
            features = content.find('features')
            if features is not None:
                for subsection in features:
                    section_name = subsection.tag
                    for element in subsection:
                        marketing_messaging_list.append(
                            MarketingMessaging.from_xml_element(
                                element, product_number, section_name, element.tag
                            )
                        )
            
            # Process <special_features> section
            special_features = content.find('special_features')
            if special_features is not None:
                for subsection in special_features:
                    section_name = subsection.tag
                    for element in subsection:
                        marketing_messaging_list.append(
                            MarketingMessaging.from_xml_element(
                                element, product_number, section_name, element.tag
                            )
                        )
        
        return marketing_messaging_list
    
    def get_section_name(self) -> str:
        """Get the section name for marketing messaging.
        
        Returns:
            The section name 'marketing_messaging'.
        """
        return 'marketing_messaging'
