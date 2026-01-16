import re

LANG_MAP = {
    'c_style': ['js', 'jsx', 'ts', 'tsx', 'css', 'scss', 'c', 'cpp', 'java', 'go', 'rs', 'php', 'swift', 'kt'],
    'python_style': ['py'],
    'hash_style': ['rb', 'sh', 'yaml', 'yml', 'dockerfile', 'makefile', 'pl'],
    'sql_style': ['sql'],
    'html_style': ['html', 'xml', 'vue', 'svg']
}

def get_cleaner_for_extension(ext):
    ext = ext.lower().strip('.')
    for style, extensions in LANG_MAP.items():
        if ext in extensions:
            # Ищем функцию по шаблону remove_<style>_comments
            func_name = f"remove_{style}_comments"
            if func_name in globals():
                return globals()[func_name]
    return None

def remove_c_style_comments(text):
    def replacer(match):
        return match.group(1) if match.group(1) else ''
    pattern = re.compile(
        r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')|(/\*.*?\*/|//[^\r\n]*)',
        re.DOTALL
    )
    return pattern.sub(replacer, text)

def remove_python_style_comments(text):
    def replacer(match):
        return match.group(1) if match.group(1) else ''

    pattern = re.compile(
        r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')|(#.*)',
        re.DOTALL
    )
    return pattern.sub(replacer, text)

def remove_hash_style_comments(text):
    def replacer(match): return match.group(1) if match.group(1) else ''
    pattern = re.compile(r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')|(#.*)', re.DOTALL)
    return pattern.sub(replacer, text)

def remove_sql_style_comments(text):
    def replacer(match): return match.group(1) if match.group(1) else ''
    pattern = re.compile(
        r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')|(/\*.*?\*/|--[^\r\n]*)',
        re.DOTALL
    )
    return pattern.sub(replacer, text)

def remove_html_style_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
