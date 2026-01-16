#!/usr/bin/env python3

import os
import toml
import shutil
import argparse
from .find_dirs import *
from .system_class import *
from .jobs import *

current_supported_jobtype = [
    1.1, 1.2, 1.3, 1.4
]

'''

In this script, first we will read in input directory, output directory, and control file location. 
Then copy the input directory, regenerating the work directory.
Then according to the job type in control file, sub the task one by one to lsf.

'''


def main():
    parser = argparse.ArgumentParser(description='An embedding calculation tool from GGA@PBC to embedded hybrids')
    parser.add_argument('--input', type=str, dest='input_dir', required=True, help='Input directory location')
    parser.add_argument('--output', type=str, dest='output_dir', required=True, help='Output directory location')
    #parser.add_argument('-R', action='store_true', help='If set, will recursively search for input dirs in the input dir. Default is a single dir for calculation.')
    parser.add_argument('-f', type=str, dest='control_file', required=True, help='control file location, must set')
    parser.add_argument('-q', dest='Queue',
                        type = str,
                        default = 'xp72mc10',
                        help = "Queue names. 'xp72mc10' is default."
                        )
    parser.add_argument('-p', dest='Core_Number',
                        type = int,
                        default = 36,
                        help = "Core number used per node: 1/2/3/4/8/28...; 36 is default." 
                        )
    parser.add_argument('--xc', dest='xc_functional', 
                        type = str,
                        default = 'b3lyp',
                        help = "Set xc if REST input generation is needed; b3lyp is default."
                        )
    parser.add_argument('--basis', dest='basis_set',
                        type = str,
                        default = 'def2-SVP',
                        help = "Set basis if REST input generation is needed; def2-SVP is default."
                        )
    args = parser.parse_args()

    # resolve xc for maybe-existing empirical dispersion
    if '-' in args.xc_functional:
        if args.xc_functional == "r-xdh7-scc15":
            functional = "r-xdh7"
            vdw = "scc15"
        func_split = args.xc_functional.split('-')
        if func_split[-1] in ['d3', 'd3bj', 'd4']:
            functional = '-'.join(func_split[:-1])
            vdw = func_split[-1]
        else:
            functional = args.xc_functional
            vdw = None
    else:
        functional = args.xc_functional
        vdw = None

    if args.Queue == "amd9654":
        sub_queue = "AMD9654"
    elif args.Queue == "amd":
        sub_queue = "AMD"
    elif args.Queue == "gaussian":
        sub_queue = "Gaussian"
    elif args.Queue == "igor":
        sub_queue = "Igor"
    else:
        sub_queue = args.Queue

    #first load in the control file
    file_control = toml.load(args.control_file)
    #fill the unset parameters with default values
    if 'jobtype' not in file_control:
        raise ValueError('jobtype not set in control file')
    else:
        file_control['jobtype'] = round(file_control['jobtype'],1)
    if file_control['jobtype'] not in current_supported_jobtype:
        raise ValueError(f'jobtype {file_control["jobtype"]} not supported currently')
    if "force_xyz_output" not in file_control:
        #file_control['force_xyz_output'] = False
        # As DMET calculation is not available now, turn this default to be true.
        file_control['force_xyz_output'] = True
    if "check_base_num_consistant" not in file_control:
        file_control['check_base_num_consistant'] = False
    if "inherit_mult_from_outcar" not in file_control:
        file_control['inherit_mult_from_outcar'] = False
    if 'separation_method' not in file_control:
        file_control['separation_method'] = 1
    if 'absorbate_atoms_num' not in file_control:
        file_control['absorbate_atoms_num'] = 0
    if 'cluster_cutting_major_method' not in file_control:
        raise ValueError('cluster_cutting_major_method not set in control file')
    elif type(file_control['cluster_cutting_major_method']) is not int:
        raise ValueError('cluster_cutting_major_method should be an integer in control file')
    if 'cluster_cutting_minor_method' not in file_control:
        raise ValueError('cluster_cutting_minor_method not set in control file')
    elif type(file_control['cluster_cutting_minor_method']) is not int:
        raise ValueError('cluster_cutting_minor_method should be an integer in control file')
    if 'cluster_radius' not in file_control:
        file_control['cluster_radius'] = 1000.0
    if 'cluster_height' not in file_control:
        file_control['cluster_height'] = 1000.0
    if 'cluster_layers' not in file_control:
        file_control['cluster_layers'] = 1000
    if 'cluster_expand_num' not in file_control:
        file_control['cluster_expand_num'] = 1000
    if 'cluster_ori_point' not in file_control:
        file_control['cluster_ori_point'] = [1000.0,1000.0,1000.0]
    if 'pseudo_cutting' not in file_control:
        file_control['pseudo_cutting'] = False
    if 'charge_cutting' not in file_control:
        file_control['charge_cutting'] = False
    if (int(file_control['jobtype']) == 2 or file_control['jobtype'] == 1.3 or file_control['jobtype'] == 1.4):
        if file_control['pseudo_cutting'] == True:
            if 'pseudo_cutting_sub_method' not in file_control:
                raise ValueError('pseudo_cutting_sub_method not set in control file')
            if type(file_control['pseudo_cutting_sub_method']) is not int:
                raise ValueError('pseudo_cutting_sub_method should be an integer in control file')
            if 'pseudo_radius' not in file_control:
                file_control['pseudo_radius'] = 1000.0
            if 'pseudo_height' not in file_control:
                file_control['pseudo_height'] = 1000.0
            if 'pseudo_layers' not in file_control:
                file_control['pseudo_layers'] = 1000
            if 'pseudo_expand_num' not in file_control:
                file_control['pseudo_expand_num'] = 1000
        if file_control['charge_cutting'] == True:
            if 'charge_cutting_sub_method' not in file_control:
                raise ValueError('charge_cutting_sub_method not set in control file')
            elif type(file_control['charge_cutting_sub_method']) is not int:
                raise ValueError('charge_cutting_sub_method should be an integer in control file')
            if 'charge_radius' not in file_control:
                file_control['charge_radius'] = 1000.0
            if 'charge_height' not in file_control:
                file_control['charge_height'] = 1000.0
            if 'charge_layers' not in file_control:
                file_control['charge_layers'] = 1000

    if 'ctrl_template' not in file_control and (file_control['jobtype'] == 1.2 or file_control['jobtype'] == 1.4):
        print("Warning: ctrl_template not set in control file, all other settings will be default values.")
        file_control['ctrl_template'] = ""


    #check if the input directory exists
    if not os.path.exists(args.input_dir):
        raise ValueError('Input directory does not exist')
    #create the output directory if not exists
    if os.path.exists(args.output_dir):
        #os.system('rm -rf ' + args.output_dir)
        shutil.rmtree(args.output_dir)
    os.makedirs(args.output_dir)

    # 1. 扫描原始目录
    ori_dirs = find_ori_dirs(args.input_dir)
    
    # 2. 实例化所有系统对象
    systems = []
    for ori_dir in ori_dirs:
        sys_obj = Single_Operation_system(ori_dir, args.input_dir, args.output_dir, file_control['jobtype'])
        systems.append(sys_obj)
        
    # 3. 排序：把 "clean" 的放在前面，以便作为基准
    systems.sort(key=lambda x: ("clean" not in x.name, x.name))
    
    # 4. 循环处理
    clean_base_num = None
    
    for sys in systems:
        print(f"Processing {sys.name}...")
        
        # 步骤 1: 准备环境 (copy files)
        sys.init_workspace()
        
        # 步骤 2: 切簇
        # 如果是 clean 系统，切完后记录 base_num
        # 如果是 absorb 系统，传入 base_num 用于检查
        sys.perform_cut(file_control, control_base_num=clean_base_num)
        
        if "clean" in sys.name and file_control.get('check_base_num_consistant'):
            clean_base_num = sys.pure_cluster_num
            
        # 步骤 3: 写出切簇结果
        sys.write_cluster_output(file_control)
        
        # 步骤 4: 如果需要，生成输入文件 (jobtype 1.2/1.4)
        if file_control['jobtype'] in [1.2, 1.4]:
            do_pseudo = (file_control['jobtype'] == 1.4)
            sys.generate_rest_input(
                file_control, 
                functional, 
                args.basis_set, 
                vdw, 
                args.Core_Number, 
                pseudo_calc=do_pseudo
            )


if __name__ == '__main__':
    main()
