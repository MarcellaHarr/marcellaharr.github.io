# extract.py
# Extracts text from project files and creates reference.md + content.md
# Usage: python extract.py <project-name>

import sys
from pathlib import Path

import docx
import pypdf
import nbformat


# --- Part 1: File type handlers ---

def read_text_file(path):
    return path.read_text(encoding='utf-8')


def read_docx(path):
    doc = docx.Document(path)
    return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())


def read_pdf(path):
    reader = pypdf.PdfReader(path)
    pages = [page.extract_text() for page in reader.pages]
    return '\n\n'.join(p for p in pages if p)


def read_notebook(path):
    with open(path, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    chunks = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            chunks.append(cell.source)
        elif cell.cell_type == 'code' and cell.source.strip():
            chunks.append(f'```python\n{cell.source}\n```')
    return '\n\n'.join(chunks)


# --- Part 2: File type router ---

TEXT_EXTENSIONS  = {'.md', '.txt', '.py', '.js', '.html', '.css', '.r', '.sql'}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
SKIP_FILES       = {'meta.yml', 'content.md', 'reference.md'}


def extract_from_file(path):
    ext = path.suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return read_text_file(path)
    elif ext == '.docx':
        return read_docx(path)
    elif ext == '.pdf':
        return read_pdf(path)
    elif ext == '.ipynb':
        return read_notebook(path)
    return None  # unsupported type — skip silently


# --- Part 3: Main logic ---

def main():
    if len(sys.argv) < 2:
        print('Usage: python extract.py <project-name>')
        sys.exit(1)

    project_name = sys.argv[1]
    project_dir  = Path('_projects') / project_name

    if not project_dir.exists():
        print(f"Error: folder '_projects/{project_name}' not found.")
        sys.exit(1)

    extracted = {}  # filename -> extracted text
    images    = []  # image filenames (noted, not read)

    for file_path in sorted(project_dir.iterdir()):
        if file_path.name in SKIP_FILES:
            continue
        if file_path.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(file_path.name)
            continue
        text = extract_from_file(file_path)
        if text and text.strip():
            extracted[file_path.name] = text.strip()

    if not extracted and not images:
        print('No supported files found in the project folder.')
        sys.exit(1)

    # Write reference.md — full extracted text for your eyes only
    reference_path = project_dir / 'reference.md'
    with open(reference_path, 'w', encoding='utf-8') as f:
        f.write(f'# Reference — {project_name}\n\n')
        f.write('> Auto-generated. Use this as reference while writing content.md.\n\n')
        for filename, text in extracted.items():
            f.write(f'---\n\n## From: {filename}\n\n{text}\n\n')
        if images:
            f.write('---\n\n## Images found\n\n')
            for img in images:
                f.write(f'- {img}\n')
    print('  reference.md written')

    # Write content.md — only if it does not already exist
    content_path = project_dir / 'content.md'
    if content_path.exists():
        print('  content.md already exists — skipping to protect your work.')
    else:
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write('## Overview\n\n')
            f.write('[DRAFT] Write your project overview here.\n\n')

            for filename, text in extracted.items():
                label   = Path(filename).stem.replace('-', ' ').replace('_', ' ').title()
                preview = text[:600] + ('...' if len(text) > 600 else '')
                f.write(f'## {label}\n\n')
                f.write(f'[DRAFT] {preview}\n\n')

            f.write('## Conclusion\n\n')
            f.write('[DRAFT] Write your conclusion here.\n\n')
        print('  content.md written with [DRAFT] sections')

    if images:
        print(f'  Images noted: {", ".join(images)}')

    print(f'\nNext steps:')
    print(f'  1. Review:  _projects/{project_name}/reference.md')
    print(f'  2. Edit:    _projects/{project_name}/content.md')
    print(f'  3. Run:     python build.py {project_name}')


if __name__ == '__main__':
    main()
