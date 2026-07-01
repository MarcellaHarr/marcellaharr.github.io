# build.py
# Generates a styled repo page from meta.yml and content.md
# Usage: python build.py <project-name>

import sys
import shutil
from pathlib import Path

import re

import yaml
import markdown as md_lib

TEMPLATES_DIR  = Path('_templates')
PROJECTS_DIR   = Path('_projects')
OUTPUT_DIR     = Path('repos')
ASSETS_IMG_DIR = Path('assets') / 'img'


# --- Content parser ---

def parse_content(content_md):
    # Strip template preamble — find the first ## heading at the START of a line
    match = re.search(r'^## ', content_md, re.MULTILINE)
    if match:
        content_md = content_md[match.start():]

    draft_count = content_md.count('[DRAFT]')
    if draft_count:
        print(f'  Note: {draft_count} [DRAFT] section(s) still in content.md')

    return md_lib.markdown(content_md, extensions=['extra'])


# --- Resources panel builder ---

def build_resources_html(resources):
    if not resources:
        return '<li><p class="text-body-secondary fst-italic">No resources listed.</p></li>'
    items = []
    for r in resources:
        title = r.get('title', 'Resource')
        url   = r.get('url', '#')
        date  = r.get('date', '')
        items.append(
            f'                <li>\n'
            f'                  <a class="d-flex flex-column flex-lg-row gap-3 align-items-start align-items-lg-center py-3 link-body-emphasis text-decoration-none border-top"\n'
            f'                     href="{url}" target="_blank">\n'
            f'                    <img src="../assets/img/recent-posts-thumbnail.gif" alt="" width="100%" height="32"\n'
            f'                         class="bd-placeholder-img" aria-hidden="true" style="object-fit: cover;" />\n'
            f'                    <div class="col-lg-8">\n'
            f'                      <h6 class="mb-0">{title}</h6>\n'
            f'                      <small class="text-body-secondary">{date}</small>\n'
            f'                    </div>\n'
            f'                  </a>\n'
            f'                </li>'
        )
    return '\n'.join(items)


# --- Image copier ---

def copy_images(project_dir, project_name):
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
    dest_dir = ASSETS_IMG_DIR / project_name
    copied = []
    for file_path in sorted(project_dir.iterdir()):
        if file_path.name.startswith('._'):
            continue
        if file_path.suffix.lower() in image_extensions:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_dir / file_path.name)
            copied.append(file_path.name)
    return copied


# --- Main ---

def main():
    if len(sys.argv) < 2:
        print('Usage: python build.py <project-name>')
        sys.exit(1)

    project_name = sys.argv[1]
    project_dir  = PROJECTS_DIR / project_name

    if not project_dir.exists():
        print(f"Error: folder '_projects/{project_name}' not found.")
        sys.exit(1)

    # Read meta.yml
    meta_path = project_dir / 'meta.yml'
    if not meta_path.exists():
        print(f"Error: meta.yml not found. Copy _templates/meta.yml into _projects/{project_name}/ and fill it in.")
        sys.exit(1)
    with open(meta_path, encoding='utf-8') as f:
        meta = yaml.safe_load(f)

    # Read content.md
    content_path = project_dir / 'content.md'
    if not content_path.exists():
        print(f"Error: content.md not found. Copy _templates/content.md into _projects/{project_name}/ and write your content.")
        sys.exit(1)
    content_md = content_path.read_text(encoding='utf-8')

    # Copy images and report paths
    copied_images = copy_images(project_dir, project_name)
    if copied_images:
        print(f'  Images copied to assets/img/{project_name}/:')
        for img in copied_images:
            print(f'    ![alt text](../assets/img/{project_name}/{img})')

    # Build each HTML piece
    content_html   = parse_content(content_md)
    resources_html = build_resources_html(meta.get('resources', []))

    title       = meta.get('title', 'Untitled Project')
    date        = meta.get('date', '')
    category    = meta.get('category', '')
    description = meta.get('description', '')
    github_url  = meta.get('github_url', '')

    date_line = str(date)
    if category:
        date_line += f' &nbsp;&middot;&nbsp; {category}'

    github_link = ''
    if github_url:
        github_link = f'<p><a href="{github_url}" target="_blank" style="color: #FFFFC0 !important;">View on GitHub &rarr;</a></p>'

    # Read page template
    template_path = TEMPLATES_DIR / 'page.html'
    if not template_path.exists():
        print("Error: _templates/page.html not found.")
        sys.exit(1)
    template = template_path.read_text(encoding='utf-8')

    # Fill in all placeholders
    html = (template
        .replace('{{BUILD_TITLE}}',         title)
        .replace('{{BUILD_DATE_CATEGORY}}', date_line)
        .replace('{{BUILD_DESCRIPTION}}',   description)
        .replace('{{BUILD_CONTENT}}',       content_html)
        .replace('{{BUILD_GITHUB}}',        github_link)
        .replace('{{BUILD_RESOURCES}}',     resources_html)
    )

    # Write output file
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f'{project_name}.html'
    output_path.write_text(html, encoding='utf-8')

    print(f'  Page built: repos/{project_name}.html')
    print(f'\nDone! Open repos/{project_name}.html in VS Code Live Server to preview.')


if __name__ == '__main__':
    main()
