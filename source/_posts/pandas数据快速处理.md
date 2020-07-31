---
title: pandas数据快速处理
date: 2020-07-31 12:24:15
tags: python
---

![](http://img.rc5j.cn/blog20200731122918.png)

销售同事拿到一份数据，但是数据导出列是json,我顺手就帮他处理了下。不得不说 pandas在处理这类问题还是非常效率高的.

<!--more-->

```python
import pandas
import json
data = pandas.read_excel('data.xlsx')

address = data['address'].values.tolist()
ordertime_list = data['order_datetime'].values.tolist()
address_new_list = []
for ad in address:
    addressJson = json.loads(ad)
    address_new_list.append(addressJson[0])

for ad in address_new_list:
    for t in ordertime_list:
        ad['order_time'] = t

df = pandas.DataFrame.from_records(address_new_list)
df.to_excel('new_data.xlsx')




```
