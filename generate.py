"""
Example special syntax for tutorials:

# Hidden in speaker-notes, rendered as code in notebook
:::::: {.practice-input}
```code
1 +
```
::::::

# Rendered as code in speaker-notes, and collapsible section in notebook
:::::: {.practice-output}
```code
1 + 1
```
::::::

# Shorthand for an empty practice-input and a practice-output
:::::: {.practice}
```code
5 + 5
```
::::::

# Highlighted in speaker-notes, hidden in notebook
:::::: {.speaker-notes}
Only seen in the speaker notes
::::::
"""

from pathlib import Path
import re
import subprocess

base_url = 'https://ben-denham.github.io/python-eda'
raw_repo_url = 'https://raw.githubusercontent.com/ben-denham/python-eda/main'
colab_url = 'https://colab.research.google.com/github/ben-denham/python-eda/blob/main'
curriculum_dir = Path(__file__).parent


def main():
    tutorial_dirs = sorted([
        child for child in curriculum_dir.iterdir()
        if child.is_dir() and child.name.startswith(f'tutorial_')
    ])

    for tutorial_dir in tutorial_dirs:
        tutorial_path = tutorial_dir / 'tutorial.md'
        with tutorial_path.open() as tutorial_file:
            tutorial_content = tutorial_file.read()

        # Generate speaker notes HTML
        subprocess.run(
            [
                'pandoc',
                '-s', '--embed-resources',
                '--css', str(curriculum_dir / 'speaker-notes.css'),
                '-o', str(tutorial_dir / 'speaker_notes.html'),
                '-f', 'markdown',
            ],
            check=True,
            text=True,
            input=tutorial_content,
        )

        def re_cell(class_name):
            return re.compile(
                (r'\n::::::[ ]*\{[ ]*\.'
                 + str(class_name)
                 + r'[ ]*\}\n(?P<cell>.*?)\n::::::\n'),
                flags=re.DOTALL,
            )

        nb_tutorial_content = tutorial_content
        # Remove speaker notes from notebook
        nb_tutorial_content = re.sub(
            re_cell('speaker-notes'),
            '',
            nb_tutorial_content,
        )
        # Expand practice into practice-input and practice-output
        nb_tutorial_content = re.sub(
            re_cell('practice'),
            r'''
:::::: {.practice-input}
```code
```
::::::

:::::: {.practice-output}
\g<cell>
::::::
            ''',
            nb_tutorial_content,
        )
        # Convert practice-input to simple code cell.
        nb_tutorial_content = re.sub(
            re_cell('practice-input'),
            r'''
\g<cell>
            ''',
            nb_tutorial_content,
        )
        # Convert practice-output into a hidden <details> element.
        nb_tutorial_content = re.sub(
            re_cell('practice-output'),
            r'''
:::::: {.cell .markdown}
<details>
<summary>Reveal correct code</summary>
\g<cell>
</details>
::::::
            ''',
            nb_tutorial_content,
        )

        # Generate notebook
        notebook_path = str(tutorial_dir / f'python_eda_{tutorial_dir.name}.ipynb')
        subprocess.run(
            [
                'pandoc', '-s',
                '-o', notebook_path,
                '-f', 'markdown',
            ],
            check=True,
            text=True,
            input=nb_tutorial_content,
        )
        # Quick fix for `"execution_count": null` that JupyterLite doesn't like.
        subprocess.run([
            f'''jq '.cells[] |= if has("execution_count") then .execution_count = 0 else . end' {notebook_path} > {notebook_path}.tmp && mv {notebook_path}.tmp {notebook_path}''',
        ], check=True, shell=True)

if __name__ == '__main__':
    main()
