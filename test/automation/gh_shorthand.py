import sys; sys.exit(0)

# --- #

import pathlib, markdown, markdownify

docs = Path('./docs')

for file in docs:
    markdown.markdown(
        input=file,
        output=file,
        extensions=['mdx_gh_links'],
        extension_configs={
            'mdx_gh_links': {'user': 'foo', 'repo': 'bar'}
        }
    )
    back_converted_markdown = md(
        html_output,
        heading_style="ATX",      # Restores '#' headers instead of '===' underlines
        bullets="-",              # Restores '-' instead of default '*' bullets
        strong_em_symbol="*",     # Ensures '**' is used for bold text
    )
