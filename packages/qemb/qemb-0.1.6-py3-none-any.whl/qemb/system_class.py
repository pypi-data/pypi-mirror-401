import os
import math
import shutil
import numpy as np
from .tackle_poscar import read_poscar, write_poscar, write_xyz, merge_elements
from .cut_cluster import cut_cluster
from .write_inputs import write_rest_input

def count_mult(atoms):
    #define a dict, key is the atom symbol, value is the electron of the atom
    atom_dict = {
        "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10,
        "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20,
        "Sc": 21, "Ti": 22, "V": 23, "Cr": 24, "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30,
        "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "Y": 39, "Zr": 40,
        "Nb": 41, "Mo": 42, "Tc": 43, "Ru": 44, "Rh": 45, "Pd": 46, "Ag": 47, "Cd": 48, "In": 49, "Sn": 50,
        "Sb": 51, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "La": 57, "Ce": 58, "Pr": 59, "Nd": 60,
        "Pm": 61, "Sm": 62, "Eu": 63, "Gd": 64, "Tb": 65, "Dy": 66, "Ho": 67, "Er": 68, "Tm": 69, "Yb": 70,
        "Lu": 71, "Hf": 72, "Ta": 73, "W": 74, "Re": 75, "Os": 76, "Ir": 77, "Pt": 78, "Au": 79, "Hg": 80,
        "Tl": 81, "Pb": 82, "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89, "Th": 90,
        "Pa": 91, "U": 92, "Np": 93, "Pu": 94, "Am": 95, "Cm": 96, "Bk": 97, "Cf": 98, "Es": 99, "Fm": 100,
        "Md": 101, "No": 102, "Lr": 103, "Rf": 104, "Db": 105, "Sg": 106, "Bh": 107, "Hs": 108, "Mt": 109,
        "Ds": 110, "Rg": 111, "Cn": 112, "Nh": 113, "Fl": 114, "Mc": 115, "Lv": 116, "Ts": 117, "Og": 118
    }
    #count the electron number
    electron_num = 0
    for atom in atoms:
        #if the atom is not in the dict, return error and quit
        if atom not in atom_dict.keys():
            print("Error: atom {0} not in the dict".format(atom))
            quit()
        else:
            electron_num += atom_dict[atom]
    #if the electron number is odd, return 2, else return 1
    if electron_num % 2 == 0:
        return 0
    else:
        return 1

def inherit_mult(log):
    with open(log,"r") as f:
        #reverse the lines
        lines = f.readlines()[::-1]
        #find the first line that contains "Total mag(uB)"
        for line in lines:
            #get the total mag(uB) value
            if 'number of electron' in line:
                raw_mag = abs(float(line.strip().split()[5]))
                num_ele = round(float(line.strip().split()[3]),ndigits=0)
                #print("raw_mag: ",raw_mag)
                #print("num_ele: ",num_ele)
                break
        if num_ele % 2 == 0:
            if math.ceil(round(raw_mag,ndigits=1)) == 0:
                mag = 1
            else:
                mag = 3
        else:
            mag = 2
            #round the value to int
            #mag = math.ceil(round(raw_mag,ndigits=1)) + 1
        return mag


class Single_Operation_system:
    """
    A class for a single system. Contains working directory info and operations.
    """
    def __init__(self, ori_abs_path, input_root, output_root, job_type):
        """
        初始化系统路径信息
        :param ori_abs_path: 原始 VASP 计算目录的绝对路径 (from find_ori_dirs)
        :param input_root: 原始输入的根目录 (cli --input)
        :param output_root: 输出的根目录 (cli --output)
        """
        self.ori_root = ori_abs_path
        
        # 计算相对路径，例如 'absorb/CO-bridge'
        self.rel_path = os.path.relpath(ori_abs_path, input_root)
        self.name = self.rel_path  # 可以用相对路径作为系统名称
        
        # 设定新的根目录
        self.rebased_root = os.path.join(output_root, self.rel_path)
        self.rebased_ref = os.path.join(self.rebased_root, 'ref')
        self.rebased_run = os.path.join(self.rebased_root, 'run')
        
        # 状态储存 (替代 jobs.py 中的 global 变量和临时返回)
        self.pure_cluster_num = 0
        self.cluster_atoms = []
        self.environ_atoms = []
        self.cluster_atoms_num = []
        self.environ_atoms_num = []
        self.pseudo_atoms = []
        self.charge_atoms = []
        self.cluster_output_type = None # "Free", "XYZ", "Embedding"
        
        # 缓存读取的结构信息，避免重复 IO
        self.ref_atoms = []
        self.ref_scale_factor = 1.0
        self.ref_lattice = []

    def init_workspace(self):
        """
        对应原 find_dirs.py 中的 regenerate_dirs 逻辑。
        创建目录，复制 POTCAR/KPOINTS/CONTCAR，并清洗 CONTCAR。
        """
        if not os.path.exists(self.rebased_ref):
            os.makedirs(self.rebased_ref)
        
        # 复制文件
        for file_name in ['POTCAR', 'CONTCAR', 'KPOINTS']:
            src_file = os.path.join(self.ori_root, file_name)
            dst_file = os.path.join(self.rebased_ref, file_name)
            if os.path.exists(src_file):
                # 只有当目标不存在或需要覆盖时才复制
                if not os.path.exists(dst_file):
                    shutil.copy(src_file, dst_file)
        
        # 执行 clean_contcar (逻辑来自 find_dirs.py)
        # 注意：clean_contcar 原函数依赖 os.chdir，建议重写为不依赖 chdir 的版本，
        # 或者在这里临时切换目录。为了稳健性，建议直接在这里实现清洗逻辑。
        self._clean_contcar_to_poscar()

    def _clean_contcar_to_poscar(self):
        """内部方法：将 CONTCAR 清洗为 POSCAR"""
        contcar_path = os.path.join(self.rebased_ref, 'CONTCAR')
        poscar_path = os.path.join(self.rebased_ref, 'POSCAR')
        
        if os.path.exists(poscar_path):
            return # 已经存在则跳过

        if os.path.exists(contcar_path):
            with open(contcar_path, 'r') as f:
                lines = f.readlines()
            # 简单的清洗逻辑，去除空行等
            valid_lines = []
            for i, line in enumerate(lines):
                if i < 6:
                    valid_lines.append(line)
                    continue
                if not line.strip():
                    break
                valid_lines.append(line)
            
            with open(poscar_path, 'w') as f:
                f.writelines(valid_lines)
            
            # 可选：重命名 CONTCAR 以备份
            os.rename(contcar_path, os.path.join(self.rebased_ref, 'CONTCAR.old'))

    def load_structure(self):
        """读取 POSCAR"""
        poscar_path = os.path.join(self.rebased_ref, 'POSCAR')
        if not os.path.exists(poscar_path):
            raise FileNotFoundError(f"POSCAR not found in {self.rebased_ref}")
        self.ref_atoms, _, self.ref_scale_factor, self.ref_lattice = read_poscar(poscar_path)

    def perform_cut(self, file_control, control_base_num=None):
        """
        对应原 jobs.py 中的 job_1_1。
        执行切簇操作。
        """
        # 如果还没读取结构，先读取
        if not self.ref_atoms:
            self.load_structure()

        # 调用核心切簇函数
        # 注意：cut_cluster 是纯函数，输入参数，返回结果
        self.cluster_atoms, self.pseudo_atoms, self.environ_atoms, self.cluster_output_type, self.pure_cluster_num = cut_cluster(
            self.ref_atoms, self.ref_scale_factor, self.ref_lattice, file_control
        )

        # 检查原子数一致性 (逻辑来自 job_1_1)
        if file_control.get('check_base_num_consistant', False):
            if "clean" in self.name:
                # 如果自己就是 clean system，不需要检查，只需返回自己的 num 供别人检查
                pass 
            elif "absorb" in self.name and control_base_num is not None:
                if self.pure_cluster_num != control_base_num:
                    # 这里可以加入你的自动调整半径重试逻辑 (retry logic)
                    # 为了简洁，这里只抛出异常或打印警告
                    print(f"Warning: Atom number mismatch in {self.name}. Got {self.pure_cluster_num}, expected {control_base_num}")
                    raise ValueError("The number of atoms in dir " + self.name + " is not consistent with the clean dir.")
                    # raise ValueError(...) 视需求而定

    def write_cluster_output(self, file_control):
        """
        将切好的簇写入文件 (POSCAR.cluster 或 .xyz)
        """
        # 确保目录存在
        # os.makedirs(self.rebased_run, exist_ok=True) # 输出通常还在 ref 里，看你原逻辑

        # 根据 cluster_output_type 决定输出格式 (逻辑来自 job_1_1)
        if self.cluster_output_type == "Free":
            write_poscar(self.cluster_atoms, os.path.join(self.rebased_ref, 'POSCAR.cluster'), self.ref_scale_factor, self.ref_lattice)
            write_poscar(self.environ_atoms, os.path.join(self.rebased_ref, 'POSCAR.environ'), self.ref_scale_factor, self.ref_lattice)
        
        elif self.cluster_output_type == "XYZ" or self.cluster_output_type == "Embedding":
            write_xyz(self.cluster_atoms, os.path.join(self.rebased_ref, 'cluster.xyz'), self.ref_scale_factor, self.ref_lattice)
            if self.cluster_output_type == "Embedding":
                if len(self.pseudo_atoms) > 0:
                    write_xyz(self.pseudo_atoms, os.path.join(self.rebased_ref, 'pseudos.xyz'), self.ref_scale_factor, self.ref_lattice)
                if len(self.environ_atoms) > 0: # 注意：原代码这里写的是 charges.xyz
                    write_xyz(self.environ_atoms, os.path.join(self.rebased_ref, 'charges.xyz'), self.ref_scale_factor, self.ref_lattice)

    def generate_rest_input(self, file_control, functional, basis, vdw, cores, pseudo_calc=False):
        """
        对应原 jobs.py 中的 job_1_2。
        生成 REST 输入文件。
        """
        if not os.path.exists(self.rebased_run):
            os.makedirs(self.rebased_run)
            
        # 确定自旋 (逻辑来自 job_1_2)
        # 这里需要重新实现 count_mult 或者从 jobs 导入
        # 这里的 elements 获取方式改为从 self.cluster_atoms 获取，不需要重新读文件
        elements = [atom[0] for atom in self.cluster_atoms]
        element_merged = merge_elements(elements)
        total_num = len(elements)
        if file_control["inherit_mult_from_outcar"]:
            log_path = os.path.join(self.ori_root, "OUTCAR")
            spin = inherit_mult(log_path)
        else:
            #determine the spin multiplicity
            #count and decide how to determine the spin of the cluster
            #if the cluster has no or little metal atoms, then decide it simply by the number of electrons
            #if the cluster has metal atoms and percentage is more than 50%, then split the cluster,
            #determine the spin of the metal and absorbant separately
            split_flag = False
            #note this will only satisfy tmp types of nowadays.
            nowadays_metals = ['Cu', 'Ag', 'Au', 'Pt']
            for key in element_merged:
                if key in nowadays_metals:
                    if element_merged[key] / total_num > 0.5 or self.pure_cluster_num / total_num > 0.6:
                        split_flag = key
                        break
            if split_flag != False:
                tmp_clu = [element for element in elements if element == split_flag]
                tmp_abs = [element for element in elements if element != split_flag]
                spin = count_mult(tmp_clu) + count_mult(tmp_abs) + 1
            else:
                spin = count_mult(elements) + 1
        
        # 路径处理：write_rest_input 需要的是相对路径或绝对路径
        cluster_xyz_path = os.path.abspath(os.path.join(self.rebased_ref, "cluster.xyz"))
        pseudo_xyz_path = os.path.abspath(os.path.join(self.rebased_ref, "pseudos.xyz"))
        charge_xyz_path = os.path.abspath(os.path.join(self.rebased_ref, "charges.xyz"))
        
        # 切换目录到 run 生成文件，或者修改 write_rest_input 接受输出路径
        curr_dir = os.getcwd()
        os.chdir(self.rebased_run)
        
        write_rest_input(
            xyz=cluster_xyz_path,
            functional=functional,
            basis=basis,
            vdw=vdw,
            charge=0, # 或者是计算出的电荷
            mult=spin,
            proc=cores,
            pseudo_calc=pseudo_calc,
            ctrl_template=file_control["ctrl_template"],
            pseudo_xyz=pseudo_xyz_path if os.path.exists(pseudo_xyz_path) else None,
            charge_xyz=charge_xyz_path if os.path.exists(charge_xyz_path) else None
        )
        os.chdir(curr_dir)