import os
import shutil
from typing import Optional


def get_project_path(projects_root: str, user_id: int, project_name: str) -> str:
    safe_name = project_name.strip().replace('..', '').replace('/', '_').replace('\\', '_')
    return os.path.join(projects_root, str(user_id), safe_name)


def ensure_project_dir(projects_root: str, user_id: int, project_name: str) -> str:
    path = get_project_path(projects_root, user_id, project_name)
    os.makedirs(path, exist_ok=True)
    return path


def create_main_tex(project_path: str) -> None:
    main_tex = os.path.join(project_path, 'main.tex')
    if not os.path.exists(main_tex):
        with open(main_tex, 'w', encoding='utf-8') as f:
            f.write("\\documentclass{article}\n\\begin{document}\nHello, DocCollab!\\end{document}\n")


def rename_project_dir(projects_root: str, user_id: int, old_name: str, new_name: str) -> tuple[bool, Optional[str]]:
    old_path = get_project_path(projects_root, user_id, old_name)
    new_path = get_project_path(projects_root, user_id, new_name)
    if not os.path.exists(old_path):
        return False, 'old_not_found'
    if os.path.exists(new_path):
        return False, 'new_already_exists'
    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    os.rename(old_path, new_path)
    return True, None


def trash_project_dir(projects_root: str, trash_root: str, user_id: int, project_name: str) -> tuple[bool, Optional[str]]:
    src = get_project_path(projects_root, user_id, project_name)
    if not os.path.exists(src):
        return False, 'not_found'
    dst_dir = os.path.join(trash_root, str(user_id))
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, project_name)
    # make unique
    suffix = 1
    base_dst = dst
    while os.path.exists(dst):
        dst = f"{base_dst}_{suffix}"
        suffix += 1
    shutil.move(src, dst)
    return True, None
