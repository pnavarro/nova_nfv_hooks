#!/bin/bash
yum install -y patch
python setup.py install
cp /usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py* /root/.
patch /usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py < nova_nfv_hooks/driver_other_hook.patch
cp -r nova_nfv_hooks/hooks /usr/lib/python2.7/site-packages/nova/virt/libvirt/.
service openstack-nova-compute restart