#!/usr/bin/python

from nova import exception
from nova.pci import pci_utils
from nova.virt.libvirt import config as vconfig
from nova.openstack.common import log as logging
from nova.network import model as network_model
from lxml import etree
import json

# The process is to contruct guest = vconfig.LibvirtConfigGuest() process and then call to_xml.
# Hook en el método _get_guest_xml
# https://libvirt.org/formatdomain.html#elementsAddress

LOG = logging.getLogger(__name__)

class NFVHook (object):

    logfile = '/var/log/nova/hook-pre.log'

    def pre(self, *args, **kwargs):
        with open(self.logfile, 'a') as fd:
            print >>fd, 'BEGIN PRE'
            for i, arg in enumerate(args):
                print >>fd, '%d: %s' % (i, arg)
            for k, v in kwargs.items():
                print >>fd, '%s=%s' % (k, v)
            print >>fd, 'END PRE'

    def post(self, rv, *args, **kwargs):
        xml=rv
        instance = args[2]
        network_info = args[3]

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
        LOG.debug('THE MODIFIED XML BY THE HOOK: %s' % xml)
        return xml

        # Llamar LibvirtConfigObject.parse_str
        # Para cada una de las macs de las vifs
        # Encontrar el elemento interface del XML
        # Añadir un source