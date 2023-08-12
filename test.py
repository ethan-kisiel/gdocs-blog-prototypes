import json
from doc_objs import *

json_data = None
with open('test.json', 'r') as json_file:
    json_string = ""
    for line in json_file.readlines():
        json_string += line

    json_data = json.loads(json_string)
    

def get_colors_tuple(rgb_color):
    color_list = []
    try:
        color_list.append(rgb_color["red"] * 255)
    except Exception as e:
        print(e)
        return tuple(color_list)

    try:
        color_list.append(rgb_color["blue"] * 255)
    except:
        return tuple(color_list)
    
    try:
        color_list.append(rgb_color["green"] * 255)
    except:
        return tuple(color_list)
    
    return tuple(color_list)
        
def make_text_element(element) -> Optional[TextElement]:
    kwargs = {}

    text_run = element.get("textRun")
    if text_run is not None:
        try:
            text_body = text_run.get("content")
            if text_body is not None:
                kwargs["text_body"] = text_body
        except:
            pass
        
        try:
            url = text_run.get("textStyle").get("link").get("url")
            if url is not None:
                kwargs["url"] = url
        except:
            pass
        
        try:
            text_color = text_run.get("textStyle").get("foregroundColor").get("color").get("rgbColor")
            if text_color is not None:
                kwargs["text_color"] = get_colors_tuple(text_color)
                print(kwargs)
        except:
            pass
        
        try:
            background_color = text_run.get("textStyle").get("backgroundColor").get("color").get("rgbColor")
            if background_color is not None:
                kwargs["background_color"] = get_colors_tuple(background_color)
                print(kwargs)
        except:
            pass
        
        try:
            bold = text_run.get("textStyle").get("bold")
            italic = text_run.get("textStyle").get("italic")
            underline = text_run.get("textStyle").get("italic")
            
            if bold is not None:
                kwargs["bold"] = bold
            if italic is not None:
                kwargs["italic"] = italic
            if underline is not None:
                kwargs["underline"] = underline
        except:
            pass
        
    else:
        return None
    
    return TextElement(kwargs)
    
def make_image_element(embedded_object) -> Optional[ImageElement]:
    kwargs = {}

    try:
        uri = embedded_object.get("imageProperties").get("contentUri")
        
        kwargs["uri"] = uri
    except:
        pass
    
    try:
        width = embedded_object.get("size").get("width").get("magnitude")
        height = embedded_object.get("size").get("height").get("magnitude")
        
        kwargs["width"] = width
        kwargs["height"] = height
    except:
        pass
    
    return ImageElement(kwargs)
    

 
if json_data is not None:
    paragraphs = []
    
    content = json_data.get("body").get("content")
    if not content:
        content = []
    for content_item in content:
        try:
            paragraph = content_item["paragraph"]
            elements = []
            for element in paragraph["elements"]:
                try:
                    inline_object_id = element.get("inlineObjectElement").get("inlineObjectId")
                    embedded_object = (json_data.get("inlineObjects")
                                       .get(inline_object_id)
                                       .get("inlineObjectProperties")
                                       .get("embeddedObject"))

                    elements.append(make_image_element(embedded_object))
                    
                except:
                    elements.append(make_text_element(element))
                #print(elements[-1].html)
            paragraphs.append(Paragraph(elements))
        except Exception as e:
            print(e)
    document = Document(title=json_data.get("title"), paragraphs=paragraphs)
    
    
    with open('test.html', 'w') as html_file:
        html_file.write(document.html)