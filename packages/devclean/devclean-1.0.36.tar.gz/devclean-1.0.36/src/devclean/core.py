import os
import shutil
from . import cleaners, formatters, utils
from .cli import parse_args, UI

def process_file(file_path, args, root_dir):
    ext = os.path.splitext(file_path)[1]
    cleaner_func = cleaners.get_cleaner_for_extension(ext)

    if not cleaner_func and not args.formatting_only:
        return False

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            original = f.read()

        content = original

        if (args.full or args.comments_only) and cleaner_func:
            content = cleaner_func(content)

        if args.full or args.formatting_only:
            content = formatters.format_whitespace(content)

        if content != original:
            if not args.no_backup:
                utils.create_backup_for_file(file_path, root_dir)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

    except Exception:
        return False

    return False

def main():
    args = parse_args()
    ui = UI(quiet=args.quiet)
    target = os.path.abspath(args.path)

    root_dir = target if os.path.isdir(target) else os.path.dirname(target)

    if args.restore:
        ui.log(f"Restoring backup in: {root_dir}")
        utils.restore_backup(root_dir, ui)
        return

    if os.path.isfile(target):
        ui.log(f"Processing single file: {target}")
        if process_file(target, args, root_dir):
            ui.log("File cleaned.")
        return

    backup_path = utils.get_backup_path(root_dir)
    if not args.no_backup and os.path.exists(backup_path):
        shutil.rmtree(backup_path)

    ui.log(f"DevClean started in: {target}")
    if not args.no_backup:
        ui.log("Backup enabled (use --restore to undo)")

    ui.log("Scanning files...")
    all_files = list(utils.scan_directory(target))
    total_files = len(all_files)

    if total_files == 0:
        ui.log("No matching files found.")
        return

    ui.init_progress(total_files)
    changed_count = 0

    for file_path in all_files:
        if process_file(file_path, args, root_dir):
            changed_count += 1
        ui.update_progress()

    ui.finish(total_files, changed_count, backup_created=(not args.no_backup and changed_count > 0))

if __name__ == "__main__":
    main()
