# Threading example
import time
import json
from lxml import etree
from io import StringIO

if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    xml_doc = etree.parse('domain.xml', parser)
    instance_metadata_element = xml_doc.find(".//metadata/instance_metadata")
    metadata_dic = {'pci_assignement': "{\"VF\":[[\"0000:00:12.0\",\"\"], [\"0000:00:13.0\",\"\"]]}"}
    if instance_metadata_element is not None:
        instance_metadata = instance_metadata_element.text
        instance_metadata_dict = json.loads(instance_metadata)
        pci_assignement = json.loads(instance_metadata_dict['pci_assignement'].replace('u\'', '\'').replace('\'', '\"'))
    else:
        metadata_element = xml_doc.find("metadata")
        metadata_text = json.dumps(metadata_dic)
        instance_metadata_element = etree.Element("instance_metadata")
        instance_metadata_element.text = metadata_text
        metadata_element.append(instance_metadata_element)
    xml_str = etree.tostring(xml_doc, pretty_print=True)
    print xml_str
    instance_metadata_element = xml_doc.find(".//metadata/instance_metadata")
    if instance_metadata_element is not None:
        instance_metadata = instance_metadata_element.text
        instance_metadata_dict = json.loads(instance_metadata)
        pci_assignement = json.loads(instance_metadata_dict['pci_assignement'].replace('u\'', '\'').replace('\'', '\"'))
    else:
        metadata_element = xml_doc.find("metadata")
        metadata_text = json.dumps(metadata_dic)
        instance_metadata_element = etree.Element("instance_metadata")
        instance_metadata_element.text = metadata_text
        metadata_element.append(instance_metadata_element)
    xml_str = etree.tostring(xml_doc, pretty_print=True)
    print xml_str


