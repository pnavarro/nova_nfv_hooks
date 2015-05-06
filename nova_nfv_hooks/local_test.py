# Threading example
import time
from lxml import etree
from io import StringIO

def my_hook(xml):
    xml = ''

if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    xml_doc = etree.parse('domain.xml', parser)
    #xml = '<a xmlns="test"><b xmlns="test"/></a>'
    #xml_doc = etree.XML(xml, parser)
    mac = 'fa:16:3e:4f:0a:1e'
    #xpath_expression = '//interface/mac[@address=\'%s\']' % mac
    #macs = xml_doc.findall(xpath_expression)
    #for mac in macs:
        # interface_element = mac.getparent()
        # new_address = etree.SubElement(interface_element, "address")
    xml_str = etree.tostring(xml_doc, pretty_print=True)
    mac_address_str = '<mac address="%s"/>' % mac
    index = xml_str.find(mac_address_str)
    target_type = 'pci'
    target_domain = '0x0000'
    target_bus = '0x00'
    target_slot = '0x11'
    target_function = '0x0'
    address_str = '<address type=\"pci\" domain=\"%(domain)s\" bus=\"%(bus)s\" slot=\"%(slot)s\" ' \
                  'function=\"%(function)s\"/>' % {'domain':target_domain,
                                                  'bus': target_bus,
                                                  'slot': target_slot,
                                                  'function': target_function}
    my_hook(xml_str)

    print xml_str

    # <interface type="hostdev" managed="yes">
    #   <mac address="fa:16:3e:9a:6a:d1"/>
    #   <source>
    #     <address type="pci" domain="0x0000" bus="0x02" slot="0x11" function="0x7"/>
    #   </source>
    #   <vlan>
    #     <tag id="3013"/>
    #   </vlan>
    #   <address bus="0x00" domain="0x0000" function="0x0" slot="0x11" type="pci"/>
    # </interface>

    # RESULTING

    # <interface type='hostdev' managed='yes'>
    #   <mac address='fa:16:3e:9a:6a:d1'/>
    #   <driver name='vfio'/>
    #   <source>
    #     <address type='pci' domain='0x0000' bus='0x02' slot='0x11' function='0x7'/>
    #   </source>
    #   <vlan>
    #     <tag id='3013'/>
    #   </vlan>
    #   <alias name='hostdev0'/>
    #   <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    # </interface>


