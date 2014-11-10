#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="nova_nfv_hooks",
    version=5,
    packages=['nova_nfv_hooks'],
    entry_points={
        'nova.hooks': [
            'nfv_hook=nova_nfv_hooks.nfv_hook:NFVHook',
        ]
    },
)
