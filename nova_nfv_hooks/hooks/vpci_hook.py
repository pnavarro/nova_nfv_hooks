#!/usr/bin/python

from nova.openstack.common import log as logging
from nova.network import model as network_model
from lxml import etree
import json

LOG = logging.getLogger(__name__)


def add_vpci_address_information(self, xml, instance, network_info):
    parser = etree.XMLParser(remove_blank_text=True)
    xml_doc = etree.XML(xml, parser)
    pci_assignement = None
    pf_list = None

    for vif in network_info:
        if vif['vnic_type'] == network_model.VNIC_TYPE_DIRECT:
            mac = vif['address']
            xpath_expression = './/interface/mac[@address=\'%s\']' % mac
            macs = xml_doc.findall(xpath_expression)
                        #Load PCI assignement from metadata
            if not pci_assignement and 'pci_assignement' in instance['metadata']:
                pci_assignement = json.loads(instance['metadata']['pci_assignement'].replace('u\'','\'').
                                            replace('\'','\"'))

                pf_list = pci_assignement['PF']

                #Iterate until we find a non assiged PF. We know this because the second element is empty
                profile = vif["profile"]
                pci_slot = profile['pci_slot']
                for pair in pf_list:
                    if len(pair[1]) == 0:
                        pair[1] = pci_slot
                        a = pair[0].split(':')
                        b = a[2].split('.')
                        target_type = 'pci'
                        target_domain = '0x'+a[0]
                        target_bus = '0x'+a[1]
                        target_slot = '0x'+b[0]
                        target_function = '0x'+b[1]
                        LOG.debug('Adding elements to the interface tree: %s' % pci_slot)
                        for mac in macs:
                            interface_element = mac.getparent()
                            interface_element.append(etree.Element("address", type=target_type, domain=target_domain, bus=target_bus,
                                                     slot=target_slot, function=target_function))
                        break
    xml = etree.tostring(xml_doc, pretty_print=True)
    LOG.debug('The modified xml of the vPCI hook: %s' % xml)
    instance['metadata']['pci_assignement']=str(pci_assignement)
    return xml