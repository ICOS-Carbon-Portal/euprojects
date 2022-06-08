#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    check keys of yaml-files
"""
import os

import yaml

yfiles = [x for x in os.listdir(os.curdir) if x[-5:] == ".yaml"]
template_file = 'template.yaml'

if template_file not in yfiles:
    print('The file template.yaml is not among the other yaml-files.')
    exit(1)

def load_file(yfile) -> dict:
    try:
        with open(yfile, "r", encoding='utf8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(f'Could not parse {yfile}\nException: ', e.__str__())


template = load_file(template_file)

for y in yfiles:
    ydict = load_file(y)
    y_minus_template = set(ydict.keys()).difference(template.keys())
    template_minus_y = set(template.keys()).difference(ydict.keys())
    if y_minus_template:
        print(f'file {y} contain keys that are not in the template: {y_minus_template}')
    if template_minus_y:
        print(f'file {y} misses keys: {template_minus_y}')

    for k,v in template.items():
        if isinstance(v, dict):
            if not isinstance(ydict[k],dict):
                print(f'file {y} has no dict as key{k}')
            else:
                dy = ydict[k]
                y_minus_template = set(dy.keys()).difference(v)
                template_minus_y = set(v).difference(dy.keys())
                if y_minus_template:
                    print(f'------------file {y} contain keys that are not in the template: {y_minus_template}')
                if template_minus_y:
                    print(f'------------file {y} do not have the keys: {template_minus_y}')
        if isinstance(v, list):
            if not isinstance(ydict[k], list):
                print(f'file {y} has no list as key: {k}')
            else:
                print(f'file {y} -- {ydict[k]} --')

for x in template.keys():
    if not isinstance(template[x], list) and not isinstance(template[x], dict):
        continue
    print()
    print(x, template[x])




