#!/usr/bin/python

from nova.network import model as network_model
from nova.pci import manager
from nova.pci import utils
import json

def add_vpci_address_information(self, xml, instance, network_info):
    parser = etree.XMLParser(remove_blank_text=True)
    xml_doc = etree.XML(xml, parser)
    pci_assignement = None
    vf_list = None
    pf_list = None
    source_dev = None

    for vif in network_info:
        mac = vif['address']
        xpath_expression = './/interface/mac[@address=\'%s\']' % mac
        macs = xml_doc.findall(xpath_expression)
        if not pci_assignement and 'pci_assignement' in instance['metadata']:
            pci_assignement = json.loads(instance['metadata']['pci_assignement'].replace('u\'','\'').replace('\'','\"'))
        if vif['vnic_type'] == network_model.VNIC_TYPE_DIRECT:
            if pci_assignement:
                vf_list = pci_assignement['VF']
                profile = vif["profile"]
                pci_slot = profile['pci_slot']
                _append_address(vf_list, macs, pci_slot)

        elif vif['vnic_type'] == network_model.VNIC_TYPE_NORMAL:
            vif_network_label = vif['network']['label']
            vif_network_id = vif['network']['id']
            if pci_assignement:
                if vif_network_label in pci_assignement:
                    source_dev = vif_network_label
                elif vif_network_id in pci_assignement:
                    source_dev = vif_network_id
                if source_dev :
                    pci_list = pci_assignement[source_dev]
                    source = vif_network_label
                    _append_address(pci_list, macs, source)

    for pci_dev in manager.get_instance_pci_devs(instance):
        address_element = _get_address_element_from_pci_address(pci_dev, xml_doc)
        if pci_assignement:
            #Get the PF list
            pf_list = pci_assignement['PF']
            #Iterate until we find a non assiged PF. We know this because the second element is empty
            for pair in pf_list:
                if len(pair[1]) == 0:
                    pair[1] = pci_dev['address']
                    a = pair[0].split(':')
                    b = a[2].split('.')
                    target_type = 'pci'
                    target_domain = '0x'+a[0]
                    target_bus = '0x'+a[1]
                    target_slot = '0x'+b[0]
                    target_function = '0x'+b[1]
                    source = address_element.getparent()
                    hostdev = source.getparent()
                    hostdev.append(etree.Element("address", type=target_type, domain=target_domain, bus=target_bus,
                                             slot=target_slot, function=target_function))
                    break

    xml = etree.tostring(xml_doc, pretty_print=True)
    instance['metadata']['pci_assignement']=str(pci_assignement)
    return xml


def _append_address(pf_list, macs, pci_slot):
    #Iterate until we find a non assiged PF. We know this because the second element is empty
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
            for mac in macs:
                interface_element = mac.getparent()
                interface_element.append(etree.Element("address", type=target_type, domain=target_domain, bus=target_bus,
                                         slot=target_slot, function=target_function))
            break


def _get_address_element_from_pci_address(pci_dev, xml_doc):
    dbsf = utils.parse_address(pci_dev['address'])
    domain, bus, slot, function = dbsf
    # This xpath expression gives me predicate error
    # xpath_expression = './/hostdev/source/address[@domain=\'%s\' and ' \
    #                    '@bus=\'%s\' and @slot=\'%s\'] and @function=\'%s\'' % (domain, bus, slot, function)
    target_domain = '0x' + domain
    xpath_expression = './/hostdev/source/address[@domain=\'%s\']' % target_domain
    addresses = xml_doc.findall(xpath_expression)
    for address in addresses:
        ad_bus = address.get('bus')
        target_bus = '0x' + ad_bus
        ad_slot = address.get('slot')
        target_slot = '0x' + ad_slot
        ad_function = address.get('function')
        target_function = '0x' + ad_function
        if bus in target_bus and slot in target_slot and function in target_function:
            return address

