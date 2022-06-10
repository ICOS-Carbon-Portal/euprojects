#!/usr/bin/env python
# coding: utf-8


import query_icos
query_icos.get_list_platforms()
query_icos.get_list_variables()
ds = query_icos.query_datasets(variables=['temperature'],temporal=['2021-01-01','2021-12-31'])

for d in ds:
    print(d)

query_icos.query_datasets(variables=['n2o'],temporal=['2018-01-01','2018-12-31'])

data = query_icos.read_dataset('https://meta.icos-cp.eu/objects/MEQ1hOwDjVYBQky5u3-BVFxf')
data

