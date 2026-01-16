import os
import shutil



def check_outcar_finished(outcar):
    # check if the OUTCAR is finished
    with open(outcar, 'r') as f:
        # read the last 10 lines of the file
        lines = f.readlines()[-20:]
        for line in lines:
            if 'General timing and accounting informations for this job' in line:
                return True
    return False


def find_ori_dirs(given_dir, supress=False):
    # walk through the directory, if OUTCAR, CONTCAR, and POSCAR are present, then add the directory to the list as a finished directory
    finished_dirs = []
    for root, dirs, files in os.walk(given_dir):
        if 'OUTCAR' in files and 'CONTCAR' in files and 'POSCAR' in files and 'POTCAR' in files and 'KPOINTS' in files:
            if check_outcar_finished(os.path.join(root, 'OUTCAR')):
                #use absolute path
                finished_dirs.append(os.path.abspath(root))
                if not supress:
                    print(f'Adding path: {os.path.abspath(root)}')
            else:
                if not supress:
                    print(f'{os.path.abspath(root)} is not finished correctly, thus omitted')
    return finished_dirs

def find_run_dirs(given_dir):
    run_dirs = []
    for root, dirs, files in os.walk(given_dir):
        if 'ctrl.in' in files:
            run_dirs.append(os.path.abspath(root))
    return run_dirs


def regenerate_run_dirs(work_dir,run_dir, pseudo_dir):
    # 需要把之前workdir里面的目录重整为新的run_dir
    # 比如之前有~/workdir/absorb/H/run, ~/workdir/absorb/CO/run, ~/workdir/clean-opt/run等等文件夹
    # 现在需要把这些文件夹重整为~/run_dir/absorb/H, ~/run_dir/absorb/CO, ~/run_dir/clean-opt
    # 需要把之前的文件夹内的ctrl.in复制到新的目录中
    # 去掉多余的run层级
    ori_run_dirs = find_run_dirs(work_dir)
    for dir in ori_run_dirs:
        # Create the corresponding directory structure in the new root
        relative_path = os.path.relpath(dir, work_dir)
        #remove the last run
        relative_path = os.path.dirname(relative_path)
        new_dir = os.path.join(run_dir, relative_path)
        os.makedirs(new_dir, exist_ok=True)

        # Move the specified files to the new ref directory
        for file_name in ['ctrl.in']:
            file_path = os.path.join(dir, file_name)
            if os.path.exists(file_path):
                shutil.copy(file_path, os.path.join(new_dir, file_name))
    tmp_run_dirs = find_run_dirs(run_dir)
    #list all pseudo files in pseudo_dir
    pseudo_files = os.listdir(pseudo_dir)
    for dir in tmp_run_dirs:
        #soft link all files in pseudo_dir to each run_dir
        for file_name in pseudo_files:
            file_path = os.path.join(pseudo_dir, file_name)
            if os.path.exists(file_path):
                os.symlink(file_path, os.path.join(dir, file_name))
