#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：jupyter_notebook 
@File    ：思维导图.py
@IDE     ：PyCharm 
@Author  ：何郴
@Date    ：2025/4/28 14:25 
@Describe：--
'''

from graphviz import Digraph

# 创建思维导图
dot = Digraph(comment='DANMF 推导思维导图', format='png')
dot.attr(rankdir='LR', size='10,5')

# 总体结构
dot.node('Start', '目标函数定义')
dot.node('U_i', 'U_i 更新推导')
dot.node('V_p', 'V_p 更新推导')
dot.node('V_i', 'V_i 更新推导')
dot.node('KKT', '应用 KKT 条件')
dot.node('Update_U', 'U_i 更新公式\n(Ui ← Ui ⊙ 2ΨᵀAVpᵀΦᵀ / Πi)')
dot.node('Update_Vp', 'Vp 更新公式\n(Vp ← Vp ⊙ (2ΨᵀA + λVpA)/(ΨᵀΨVp + Vp + λVpD))')
dot.node('Update_Vi', 'Vi 更新公式\n(Vi ← Vi ⊙ 2ΨᵀA / (ΨᵀΨVi + Vi))')
dot.node('Finish', '完成')

# 连接关系
dot.edges([
    ('Start', 'U_i'),
    ('Start', 'V_p'),
    ('Start', 'V_i'),
    ('U_i', 'KKT'),
    ('V_p', 'KKT'),
    ('V_i', 'KKT'),
    ('KKT', 'Update_U'),
    ('KKT', 'Update_Vp'),
    ('KKT', 'Update_Vi'),
    ('Update_U', 'Finish'),
    ('Update_Vp', 'Finish'),
    ('Update_Vi', 'Finish')
])

# 渲染思维导图
dot.render('/mnt/data/DANMF_derivation_mindmap', view=False)
'/mnt/data/DANMF_derivation_mindmap.png'
