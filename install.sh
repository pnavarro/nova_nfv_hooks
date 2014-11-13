#!/bin/bash
python setup.py install
cp /usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py* /root/.
rm -rf /usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py*
cp nova_nfv_hooks/driver.py /usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py
service openstack-nova-compute restart