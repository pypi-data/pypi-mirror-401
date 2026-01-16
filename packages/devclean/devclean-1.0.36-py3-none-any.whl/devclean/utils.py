import os
import shutil
import fnmatch

BACKUP_DIR_NAME = '.devclean_backup'

def get_backup_path(root_dir):
    return os.path.join(root_dir, BACKUP_DIR_NAME)

def create_backup_for_file(file_path, root_dir):
    backup_root = get_backup_path(root_dir)
    rel_path = os.path.relpath(file_path, root_dir)
    dest_path = os.path.join(backup_root, rel_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(file_path, dest_path)

def restore_backup(root_dir, ui_logger):
    backup_root = get_backup_path(root_dir)

    if not os.path.exists(backup_root):
        ui_logger.log("No backup found to restore.")
        return False

    count = 0
    for root, dirs, files in os.walk(backup_root):
        for file in files:
            backup_file_path = os.path.join(root, file)

            rel_path = os.path.relpath(backup_file_path, backup_root)
            original_path = os.path.join(root_dir, rel_path)

            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            shutil.copy2(backup_file_path, original_path)
            count += 1

    shutil.rmtree(backup_root)
    ui_logger.log(f"Restored {count} files. Backup directory removed.")
    return True


def load_gitignore(root_dir):
    path = os.path.join(root_dir, '.gitignore')
    patterns = []
    patterns.append(BACKUP_DIR_NAME)

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def is_ignored(path, patterns):
    path = path.replace(os.path.sep, '/')
    for pat in patterns:
        if pat.endswith('/') and (path.startswith(pat) or f"/{path}/".endswith(f"/{pat}")):
            return True
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(os.path.basename(path), pat):
            return True
    return False

def scan_directory(root_dir):
    patterns = load_gitignore(root_dir)
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not is_ignored(os.path.relpath(os.path.join(root, d), root_dir), patterns)]
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            if not is_ignored(rel_path, patterns):
                yield full_path
