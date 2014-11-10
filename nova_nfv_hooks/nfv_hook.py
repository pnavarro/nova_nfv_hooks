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
        guest.membacking=vconfig.LibvirtConfigGuestMemoryBacking()
        guest.membacking.hugepages=True
        #cputune_temp=vconfig.LibvirtConfigGuestCPUTune()
        #pinning_pairs = [(0,3), (1,27), (2,5), (3,29), (4,7), (5,31), (6,9), (7,33), (8,11), (9,35), (10,13), (11,37),
        #                 (12,15), (13,39), (14,17), (15,41), (16,19), (17,43), (18,21), (19,45), (20,23), (21,47)]
        #vcpupin_temp=[]
        #for pair in pinning_pairs:
        #    vcpu = vconfig.LibvirtConfigGuestCPUTuneVCPUPin()
        #    vcpu.vcpu=pair[0]
        #    vcpu.cpuset=pair[1]
        #    vcpupin_temp.append(vcpu)
        #vcpu1=vconfig.LibvirtConfigGuestCPUTuneVCPUPin()
        #vcpu1.vcpu=0
        #vcpu1.cpuset=3
        #cputune_temp.vcpupin=vcpupin_temp
        #guest.cputune=cputune_temp
        return guest
