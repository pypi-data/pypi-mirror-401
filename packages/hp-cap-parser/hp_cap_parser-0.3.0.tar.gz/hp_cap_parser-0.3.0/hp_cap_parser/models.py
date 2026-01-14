"""Product data models"""

from dataclasses import dataclass


@dataclass
class Product:
    """Product data model"""
    pmoid: str
    product_number: str
    product_name: str
    culture_code: str
    item_level: str
    product_line: str
    last_update_date: str
            
    @classmethod
    def from_xml_element(cls, element) -> 'Product':
        """Create Product from XML element"""
        return cls(
            pmoid=element.get('pmoid', ''),
            product_number=element.get('number', ''),
            product_name=element.get('name', ''),
            culture_code=element.get('culturecode', ''),
            item_level=element.get('itemlevel', ''),
            product_line=element.get('productline', ''),
            last_update_date=element.get('lastupdatedate', '')
        )


@dataclass
class ContentItem:
    """Content/specification item"""
    product_number: str
    section_name: str
    label: str
    value: str
    tag_name: str


@dataclass
class PLCData:
    """Product lifecycle data"""
    product_number: str
    full_date: str = ''
    obsolete_date: str = ''
    end_of_service_date: str = ''


@dataclass
class Document:
    """Document data"""
    product_number: str
    full_title: str = ''
    description: str = ''
    document_type: str = ''
    language_label: str = ''
    url: str = ''
    master_object_name: str = ''
    language_code: str = ''

    @classmethod
    def from_xml_element(cls, element, product_number) -> 'Document':
        """Create Document from XML element"""
        return cls(
            product_number=product_number,
            full_title=element.findtext('full_title', ''),
            description=element.findtext('description', ''),
            document_type=element.findtext('document_type', ''),
            language_label=element.findtext('language_label', ''),
            url=element.findtext('url', ''),
            master_object_name=element.findtext('master_object_name', ''),
            language_code=element.findtext('language_code', ''),
        )



@dataclass
class Image:
    """Image data"""
    product_number: str
    full_title: str = ''
    image_url_http: str = ''
    image_url_https: str = ''
    content_type: str = ''
    pixel_width: str = ''
    pixel_height: str = ''
    dpi_resolution: str = ''
    orientation: str = ''
    background: str = ''

    @classmethod
    def from_xml_element(cls, element, product_number) -> 'Image':
        """Create Image from XML element"""
        return cls(
            product_number=product_number,
            full_title=element.findtext('full_title', ''),
            image_url_http=element.findtext('image_url_http', ''),
            image_url_https=element.findtext('image_url_https', ''),
            content_type=element.findtext('content_type', ''),
            pixel_width=element.findtext('pixel_width', ''),
            pixel_height=element.findtext('pixel_height', ''),
            dpi_resolution=element.findtext('dpi_resolution', ''),
            orientation=element.findtext('orientation', ''),
            background=element.findtext('background', '')
        )

@dataclass
class Link:
    """Link data"""
    product_number: str
    type: str = ''
    pmoid: str = ''
    num: str = ''
    name: str = ''
    full_date: str = ''
    obsolete_date: str = ''
    marketing_sub_category: str = ''
    marketing_category: str = ''
    product_type: str = ''

    @classmethod
    def from_xml_element(cls, element, product_number) -> 'Link':
        """Create Link from XML element"""
        return cls(
            product_number=product_number,
            type=element.findtext('type', ''),
            pmoid=element.findtext('pmoid', ''),
            num=element.findtext('num', ''),
            name=element.findtext('name', ''),
            full_date=element.findtext('full_date', ''),
            obsolete_date=element.findtext('obsolete_date', ''),
            marketing_sub_category=element.findtext('marketing_sub_category', ''),
            marketing_category=element.findtext('marketing_category', ''),
            product_type=element.findtext('product_type', '')
        )


@dataclass
class MarketingMessaging:
    """Marketing messaging content item"""
    product_number: str
    section_name: str
    tag_name: str
    label: str = ''
    text_value: str = ''
    src_culture_code: str = ''

    @classmethod
    def from_xml_element(cls, element, product_number: str, section_name: str, tag_name: str) -> 'MarketingMessaging':
        """Create MarketingMessaging from XML element"""
        return cls(
            product_number=product_number,
            section_name=section_name,
            tag_name=tag_name,
            label=element.get('label', ''),
            text_value=element.text or '',
            src_culture_code=element.get('src_culture_code', '')
        )


@dataclass
class TechSpec:
    """Technical specification item"""
    product_number: str
    section_name: str
    tag_name: str
    label: str = ''
    text_value: str = ''
    src_culture_code: str = ''

    @classmethod
    def from_xml_element(cls, element, product_number: str, section_name: str, tag_name: str) -> 'TechSpec':
        """Create TechSpec from XML element"""
        return cls(
            product_number=product_number,
            section_name=section_name,
            tag_name=tag_name,
            label=element.get('label', ''),
            text_value=element.text or '',
            src_culture_code=element.get('src_culture_code', '')
        )