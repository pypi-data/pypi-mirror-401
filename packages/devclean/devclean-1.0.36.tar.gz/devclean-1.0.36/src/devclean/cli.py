import sys
import argparse
import time

class UI:
    def __init__(self, quiet=False):
        self.quiet = quiet
        self.total = 0
        self.current = 0

    def log(self, message):
        if not self.quiet:
            print(message)

    def init_progress(self, total):
        self.total = total
        self.current = 0
        self._print_bar()

    def update_progress(self):
        self.current += 1
        self._print_bar()

    def _print_bar(self):
        if self.quiet: return
        percent = 100 * (self.current / float(self.total)) if self.total > 0 else 100
        bar_len = 30
        filled = int(bar_len * self.current // self.total) if self.total > 0 else bar_len
        bar = '=' * filled + '-' * (bar_len - filled)
        sys.stdout.write(f'\rProgress: [{bar}] {percent:.0f}%')
        sys.stdout.flush()

    def finish(self, scanned, changed, backup_created=False):
        if self.quiet: return
        sys.stdout.write('\n')
        print("-" * 50)
        print(f"Scan complete.")
        print(f"Files scanned:  {scanned}")
        print(f"Files modified: {changed}")
        if backup_created:
            print(f"Backup saved to: .devclean_backup/ (Use --restore to undo)")
        print("-" * 50)

def parse_args():
    parser = argparse.ArgumentParser(
        description="DevClean: CLI tool to strip comments and formatting files safely.",
        epilog="Examples:\n  devclean                  # Standard cleanup with backup\n  devclean --no-backup      # Cleanup without safety net\n  devclean --restore        # Undo last cleanup\n  devclean -c src/          # Remove comments only in src/",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('path', nargs='?', default='.', help='Target directory or file path')

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--full', action='store_true', default=True, help='Clean comments AND format whitespace (Default)')
    mode_group.add_argument('-c', '--comments-only', action='store_true', help='Remove comments only')
    mode_group.add_argument('-f', '--formatting-only', action='store_true', help='Fix whitespace only')

    parser.add_argument('--no-backup', action='store_true', help='Disable automatic backup creation')
    parser.add_argument('--restore', action='store_true', help='Restore files from the last backup')

    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress output')

    args = parser.parse_args()

    if args.comments_only or args.formatting_only:
        args.full = False

    return args
