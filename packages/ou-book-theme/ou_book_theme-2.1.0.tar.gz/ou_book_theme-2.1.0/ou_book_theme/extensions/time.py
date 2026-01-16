"""Time-related Sphinx directives."""  # noqa: A005

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.docutils import SphinxDirective
from sphinx_design.shared import create_component, is_component


class TimeDirective(SphinxDirective):
    """The TimeDirective directive is used to generate a time block."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        time = create_component(
            "ou-time", classes=["ou-time"], children=[nodes.Text(self.arguments[0], self.arguments[0])]
        )
        return [time]


class TimeLatexTransform(SphinxPostTransform):
    """Transform time containers into the LaTeX specific AST structures."""

    default_priority = 199
    formats = ("latex",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "ou-time")):
            new_nodes = [
                nodes.raw("", r"\outime{", format="latex"),
                *node.children,
                nodes.raw("", r"}", format="latex"),
            ]
            node.replace_self(new_nodes)


def setup(app):
    """Setup the Time extensions."""
    app.add_directive("time", TimeDirective)
    app.add_post_transform(TimeLatexTransform)
