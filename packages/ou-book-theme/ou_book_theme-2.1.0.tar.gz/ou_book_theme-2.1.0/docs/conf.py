project = "OU Book Theme"
author = "Mark Hall"
root_doc = "index"
extensions = ["myst_parser", "ou_book_theme", "sphinx_external_toc", "sphinxcontrib.mermaid"]
language = "en"
project_copyright = "2023-%Y"

numfig = True

html_title = "OU Book Theme"
html_theme = "ou_book_theme"

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

latex_toplevel_sectioning = "chapter"
latex_elements = {
    "maketitle": r"\maketitle",
    "preamble": r"\usepackage{ou-book-theme}",
    "sphinxsetup": """OuterLinkColor={RGB}{171,92,74},%
        InnerLinkColor={RGB}{171,92,74},%
        pre_background-TeXcolor={RGB}{255,255,255},%
        pre_border-radius=0pt,%
        pre_padding-top=0.8em,%
        pre_padding-bottom=0.8em,%
        pre_border-left-width=0pt,%
        pre_border-right-width=0pt,%
""",
}
