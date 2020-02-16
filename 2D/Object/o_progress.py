# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:34:04 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Object-progress
"""

import copy as cp
import numpy as np

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_matrix_outline as C_M_O
import calculation_image_smoothing as C_I_S

import operation_path as O_P

from o_sphere import sphere

from variable_yade_color import yade_rgb_list,yade_rgb_map

#==============================================================================
#object progress to manage data efficiently
#==============================================================================            
class progress:
    
    def __init__(self,
                 map_tag_id=None,
                 map_id_spheres=None,
                 list_spheres=None,
                 case=None,
                 shape=None,
                 percentage=None,
                 
                 rgb_map=None,
                 img_tag=None,
                 structural_deformation=None,
                 fracture=None,

                 outline_stress=None,
                 outline_strain=None,
                 outline_velocity=None,
                 outline_displacement=None,
                 
                 x_normal_stress=None,
                 y_normal_stress=None,
                 shear_stress=None,
                 mean_normal_stress=None,
                 maximal_shear_stress=None,
                 
                 periodical_x_normal_strain=None,
                 periodical_y_normal_strain=None,
                 periodical_shear_strain=None,
                 periodical_volumrtric_strain=None,
                 periodical_distortional_strain=None,
                 
                 cumulative_x_normal_strain=None,
                 cumulative_y_normal_strain=None,
                 cumulative_shear_strain=None,
                 cumulative_volumrtric_strain=None,
                 cumulative_distortional_strain=None,
                 
                 instantaneous_x_normal_strain=None,
                 instantaneous_y_normal_strain=None,
                 instantaneous_shear_strain=None,
                 instantaneous_volumrtric_strain=None,
                 instantaneous_distortional_strain=None,
                 
                 resultant_velocity=None,
                 x_velocity=None,
                 y_velocity=None,
                 
                 cumulative_displacement=None,
                 cumulative_x_displacement=None,
                 cumulative_y_displacement=None,
                 
                 periodical_displacement=None,
                 periodical_x_displacement=None,
                 periodical_y_displacement=None,
                 
                 instantaneous_displacement=None,
                 instantaneous_x_displacement=None,
                 instantaneous_y_displacement=None,
                 
                 map_stress_or_strain=None,
                 map_velocity_or_displacement=None):
        
        self.map_tag_id=map_tag_id
        self.map_id_spheres=map_id_spheres
        self.list_spheres=list_spheres
        self.case=case
        self.shape=shape
        self.percentage=percentage
        
        self.rgb_map=rgb_map
        self.img_tag=img_tag
        self.structural_deformation=structural_deformation
        self.fracture=fracture
        
        self.outline_stress=outline_stress
        self.outline_strain=outline_strain
        self.outline_velocity=outline_velocity
        self.outline_displacement=outline_displacement
        
        self.x_normal_stress=x_normal_stress
        self.y_normal_stress=y_normal_stress
        self.shear_stress=shear_stress
        self.mean_normal_stress=mean_normal_stress
        self.maximal_shear_stress=maximal_shear_stress
        
        self.periodical_x_normal_strain=periodical_x_normal_strain
        self.periodical_y_normal_strain=periodical_y_normal_strain
        self.periodical_shear_strain=periodical_shear_strain
        self.periodical_volumrtric_strain=periodical_volumrtric_strain
        self.periodical_distortional_strain=periodical_distortional_strain
        
        self.cumulative_x_normal_strain=cumulative_x_normal_strain
        self.cumulative_y_normal_strain=cumulative_y_normal_strain
        self.cumulative_shear_strain=cumulative_shear_strain
        self.cumulative_volumrtric_strain=cumulative_volumrtric_strain
        self.cumulative_distortional_strain=cumulative_distortional_strain
        
        self.instantaneous_x_normal_strain=instantaneous_x_normal_strain
        self.instantaneous_y_normal_strain=instantaneous_y_normal_strain
        self.instantaneous_shear_strain=instantaneous_shear_strain
        self.instantaneous_volumrtric_strain=instantaneous_volumrtric_strain
        self.instantaneous_distortional_strain=instantaneous_distortional_strain
        
        self.resultant_velocity=resultant_velocity
        self.x_velocity=x_velocity
        self.y_velocity=y_velocity
        
        self.cumulative_displacement=cumulative_displacement
        self.cumulative_x_displacement=cumulative_x_displacement
        self.cumulative_y_displacement=cumulative_y_displacement
        
        self.periodical_displacement=periodical_displacement
        self.periodical_x_displacement=periodical_x_displacement
        self.periodical_y_displacement=periodical_y_displacement
        
        self.instantaneous_displacement=instantaneous_displacement
        self.instantaneous_x_displacement=instantaneous_x_displacement
        self.instantaneous_y_displacement=instantaneous_y_displacement
        
        self.map_stress_or_strain=map_stress_or_strain
        self.map_velocity_or_displacement=map_velocity_or_displacement
        
    def InitCalculation(self,file_path):
        
        #all lines
        lines=open(file_path,'r').readlines()
        
        #correct legnth of each line
        correct_length=len(lines[0].strip('\n').split(','))
    
        list_spheres=[]
        
        #traverse all lines
        for this_line in lines:
            
            this_list=this_line.strip('\n').split(',')
            
            #judge if total length is OK
            if len(this_list)!=correct_length:
                        
                continue
        
            #define new sphere object
            new_sphere=sphere()
            
            new_sphere.Id=int(this_list[0])
            new_sphere.radius=float(this_list[1])
            new_sphere.color=[float(this_str) for this_str in this_list[2:5]] 
            new_sphere.position=np.array([float(this_str) for this_str in this_list[5:8]])
            new_sphere.velocity=np.array([float(this_str) for this_str in this_list[8:11]])
            new_sphere.stress_tensor=np.array([float(this_str) for this_str in this_list[11:]])
         
            #plane: default XoY
            new_sphere.plane='XoY'
            
            #3D tensor length is correct
            if len(new_sphere.stress_tensor)!=9:
                
                continue
            
            #judge if there is inf
            if np.inf in new_sphere.stress_tensor or -np.inf in new_sphere.stress_tensor:
       
                continue
            
            #judge if there is nan
            for this_element in new_sphere.stress_tensor:
            
                if np.isnan(this_element):
      
                    continue
               
            new_sphere.Init()
            
            list_spheres.append(new_sphere)
                
        #id and tag list
        list_id=[this_sphere.Id for this_sphere in list_spheres]
        list_tag=[yade_rgb_list.index(this_sphere.color) for this_sphere in list_spheres]
        
        #construct map between id and tag
        map_id_tag=dict(zip(list_id,list_tag))
        
        list_set_tag=list(set(list_tag))
            
        #construct map between tag and id list
        self.map_tag_list_id={}
        
        for this_tag in list_set_tag:
            
            self.map_tag_list_id[this_tag]=[]
            
        for this_id in list_id:
            
            self.map_tag_list_id[map_id_tag[this_id]].append(this_id)
        
        #construct map between id and spheres
        self.map_id_spheres=dict(zip(list_id,list_spheres))
        
    def InitVisualization(self,progress_path,lite):
        
        if '100-500' in progress_path:
        
            self.shape=(100,500)
            
        if '100-1000' in progress_path:
            
            self.shape=(100,1000)   
            
        if '100-200' in progress_path:
            
            self.shape=(100,350) 
            
        #map between tag and YADE rgb
        self.rgb_map=yade_rgb_map
        
        #progress percentage
        self.percentage=O_P.ProgressPercentageFromTXT(progress_path)
        
        #img tag and img rgb of structural deformation
        self.img_tag=C_M.ImportMatrixFromTXT(progress_path)
        self.structural_deformation=C_I.ImageTag2RGB(self.img_tag,self.rgb_map)
        
        if not lite:
            
            list_post_fix=['stress\\mean normal',
                           'stress\\maximal shear',
                           'periodical strain\\volumetric',
                           'periodical strain\\distortional',
                           'cumulative strain\\volumetric',
                           'cumulative strain\\distortional']
            
            #containing result matrix
            matrix_list=[]
            
            for this_post_fix in list_post_fix:
                
                #stress and strain itself
                file_path=progress_path.replace('structural deformation',this_post_fix)
                
                matrix_list.append(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(file_path))))
                
            self.mean_normal_stress,\
            self.maximal_shear_stress,\
            self.periodical_volumrtric_strain,\
            self.periodical_distortional_strain,\
            self.cumulative_volumrtric_strain,\
            self.cumulative_distortional_strain=matrix_list
            
            #construct a map between post fix name and matrix
            list_post_fix=['Mean Normal Stress',
                           'Maximal Shear Stress',
                           'Volumetric Strain-Periodical',
                           'Distortional Strain-Periodical',
                           'Volumetric Strain-Cumulative',
                           'Distortional Strain-Cumulative']
            
            #stress and strain map
            self.stress_or_strain=dict(zip(list_post_fix,matrix_list))
        
            #fracture matrix
            self.fracture=cp.deepcopy(self.stress_or_strain['Distortional Strain-Cumulative'])
            
            '''they are different for the existence of gradient calculation'''
            #stress outline
            self.outline_stress=C_M_O.OutlineFromMatrix(self.stress_or_strain['Mean Normal Stress'])
         
            #stress outline
            self.outline_strain=C_M_O.OutlineFromMatrix(self.stress_or_strain['Volumetric Strain-Periodical'])
        