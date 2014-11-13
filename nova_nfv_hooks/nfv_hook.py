#!/usr/bin/python

from nova.virt.libvirt import config as vconfig


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
        guest=rv
        image_metadata = args[3]
        img_meta_prop = image_metadata.get('properties', {}) if image_metadata else {}
        if img_meta_prop.get('hw_mem_page_size'):
            guest.membacking=vconfig.LibvirtConfigGuestMemoryBacking()
            size = img_meta_prop.get('hw_mem_page_size')
            if 'large' in size:
                guest.membacking.hugepages=True
        return guest
