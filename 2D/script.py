# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:14:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

from __init__ import *

case_path=r'D:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single base uplift bT=2.4 uH=20 uW=200 uO=400'

#step 1
#C_C_E.CaseCalculation(case_path,which_mode_list=['Stress','-Cumulative'],exception='final only')

#step 2
case_path=case_path.replace('input','output')

V_C.CaseVisualization(case_path)
##      
#case_folder=r'H:\GitHub\YADE\Controlling-Simulation\2D\extension 100-200\input'
#
#for this_case_name in os.listdir(case_folder):
#    
#    C_C_E.CaseCalculation(case_folder+'\\'+this_case_name,which_mode_list=['structural_deformation'],final_only=False)
#
import numpy as np
import matplotlib.pyplot as plt

#figure,ax=plt.subplots()
#
#this_ax=plt.subplot(211)
#
#mat=np.array([[1,2,1],[3,4,5]])
#
#a=np.gradient(mat,axis=1)
#b=np.gradient(mat,axis=0)