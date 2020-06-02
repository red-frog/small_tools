import re

s = '探寻<font color=red>华</font><font color=red>测</font>采购新模式背后的故事——访<font color=red>华</font><font color=red>测</font>检<font color=red>测</font>认证集团副总裁钱峰'
print(s)
rule_sub = [
    # re.compile('[^>]<font color=red>.{1}</font>[^<]'),
    re.compile('[^>]<font color=red>.</font>[^<]'),
    re.compile('[^>]<font color=red>.</font>$'),
    re.compile('^<font color=red>.</font>[^<]'),
    # re.compile('</font>[^<]'),
]

new_s = s
for rule_sub_item in rule_sub:
    ret_s_list = re.findall(rule_sub_item,new_s)
    if len(ret_s_list) > 0:
        for ret_s in ret_s_list:
            real_s_rule = re.compile('>(.)<')
            real_s = re.findall(real_s_rule, ret_s)[0]
            if ret_s[0] != '>':
                real_s = ret_s[0] + real_s
            if ret_s[-1] != '<':
                real_s = real_s + ret_s[-1]
            new_s = re.sub(ret_s, real_s, new_s)
            print(new_s)

    # new_s = re.sub(rule_sub_item, '', new_s)
print(new_s)
