from typing import Optional

def get_css_color(color: tuple[float, ...]) -> str:
    css_color = ""
    if color is not None:
        try:
            red = color[0]
        except:
            return css_color
            
        try:
            blue = color[1]
        except:
            blue = 0
        
        try:
            green = color[2]
        except:
            green = 0

    css_color = f"rgb({red}, {green}, {blue})"

    return css_color

def stringify_attributes(attributes: dict[str: str]) -> str:
    '''
    This takes a dictionary of css attributes and converts them to a single combined string
    separated by semicolons as would be seen in css
    '''
    stringified_attributes = ""
    try:
        attribute_strings = [f"{key}: {attributes[key]};" for key in attributes.keys()]
    except AttributeError:
        return stringified_attributes
    
    for attribute in attribute_strings:
        stringified_attributes += attribute
    
    return stringified_attributes

def get_css(attributes: dict[str: str]) -> str:
    '''
    This just places the stringified attributes into a style="" string and returns that
    '''
    css_tag = f'style="{stringify_attributes(attributes)}"'
    
    return css_tag

class ParagraphElement:
    pass


class TextElement(ParagraphElement):
    '''
    Represents a text element, which will be a part of a paragraph/any kind of text
    which correlates to a "textRun" in google docs api
    '''

    text_body: str
    url: Optional[str]

    text_color: Optional[tuple[float, ...]]
    background_color: Optional[tuple[float, ...]]

    bold: bool
    italic: bool
    underline: bool
    


    def __init__(self, kwargs):
        self.text_body = kwargs.get("text_body", "")
        self.url = kwargs.get("url", None)

        self.text_color = kwargs.get("text_color", None)
        self.background_color = kwargs.get("background_color", None)

        self.bold = kwargs.get("bold", False)
        self.italic = kwargs.get("italic", False)
        self.underline = kwargs.get("underline", False)
        
    
    @property
    def html(self):
        text_style = {}
        if self.text_color is not None:
            if get_css_color(self.text_color) != "":
                text_style["color"] = get_css_color(self.text_color)
        
        if self.background_color is not None:
            if get_css(self.background_color) != "":
                text_style["background-color"] = get_css_color(self.background_color)
        
        if self.bold:
            text_style["font-weight"] = "bold"
        if self.italic:
            text_style["font-style"] = "italic"
        if self.underline:
            text_style["text-decoration"] = "underline"
        
        if self.url is not None:
            html_string = f'<a href="{self.url}" {get_css(text_style)}>{self.text_body}</a>'
        else:
            html_string = f"<span {get_css(text_style)}>{self.text_body}</span>"

        return html_string
    
class ImageElement(ParagraphElement):
    uri: str
    
    width: int
    height: int
    
    def __init__(self, kwargs):
        self.uri = kwargs.get("uri", "")
        
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        
    
    @property
    def html(self):
        img_html = f'<img src="{self.uri}" style="width: {self.width}px;height: {self.height}px;">'
        
        return img_html

    
class Paragraph:
    text_elements: list[ParagraphElement]
    
    def __init__(self, text_elements: list[TextElement]):
        self.text_elements = text_elements

    @property
    def html(self):
        html_string = "<p>"
        for element in self.text_elements:
            if element is not None:
                html_string += element.html
        html_string += "</p>"

        return html_string

class Document:
    title: str
    paragraphs: list[Paragraph]

    def __init__(self, title: str, paragraphs: list[Paragraph]):
        self.title = title
        self.paragraphs = paragraphs
    
    @property
    def html(self):
        html_string = f'<h1 class="document-title"> </h1>'
        html_string += '<div class="document-body">'
        for paragraph in self.paragraphs:
            html_string += paragraph.html
        
        html_string += "</div>"
        
        return html_string
