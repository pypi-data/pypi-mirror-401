import os
import shutil
import re

def ToPrefabAfter(path='.'):
    # 检查 docs/prefab 目录是否存在
    source_dir = os.path.join(path, 'docs', 'prefab')
    if not os.path.exists(source_dir):
        print("docs/prefab 目录不存在，跳过移动操作")
        return

    # 检查 src 目录是否存在
    src_dir = os.path.join(path, 'src')
    if not os.path.exists(src_dir):
        os.makedirs(src_dir)
        print("已创建 src 目录")

    # 移动 docs/prefab 到 src/prefab
    dest_dir = os.path.join(src_dir, 'prefab')
    if os.path.exists(dest_dir):
        # 如果目标目录已存在，先删除
        shutil.rmtree(dest_dir)
        print("已删除现有 src/prefab 目录")

    shutil.move(source_dir, dest_dir)
    print("已将 docs/prefab 移动到 src/prefab")

    # 检查并修改 src/main.py 文件
    main_py_path = os.path.join(src_dir, 'main.py')
    if not os.path.exists(main_py_path):
        print("src/main.py 文件不存在，跳过导入语句添加操作")
        return

    # 读取文件内容
    with open(main_py_path, 'r') as f:
        lines = f.readlines()

    # 检查是否存在 from prefab import * 语句
    has_prefab_import = False
    import_end_line = 0

    for i, line in enumerate(lines):
        if re.search(r'from\s+prefab\s+import\s+\*', line):
            has_prefab_import = True
            break
        # 检查是否为导入语句
        if re.match(r'^(from|import)\s+', line.strip()):
            import_end_line = i + 1  # 记录导入语句的结束位置（下一行）

    if not has_prefab_import:
        # 在导入语句的末尾插入 from prefab import * 语句
        if import_end_line > 0:
            # 在导入语句末尾插入
            lines.insert(import_end_line, 'from prefab import *\n')
        else:
            # 如果没有导入语句，在文件开头插入
            lines.insert(0, 'from prefab import *\n')
        
        # 写回文件
        with open(main_py_path, 'w') as f:
            f.writelines(lines)
        print("已在 src/main.py 中导入语句末尾追加 from prefab import * 语句")
    else:
        print("src/main.py 中已存在 from prefab import * 语句，跳过添加操作")

if __name__ == "__main__":
    ToPrefabAfter('.')
