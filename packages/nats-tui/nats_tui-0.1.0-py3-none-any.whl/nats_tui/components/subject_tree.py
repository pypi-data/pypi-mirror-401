"""Subject tree widget for NATS TUI."""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from textual.message import Message
from textual.widgets import Tree
from textual.widgets.tree import TreeNode


@dataclass
class SubjectNode:
    """Data for a subject tree node."""

    name: str
    full_subject: str
    message_count: int = 0
    last_seen: datetime | None = None
    is_leaf: bool = True

    def increment(self) -> None:
        """Increment message count and update last seen."""
        self.message_count += 1
        self.last_seen = datetime.now()


class SubjectTree(Tree[SubjectNode]):
    """Tree widget for displaying NATS subjects hierarchically."""

    DEFAULT_CSS = """
    SubjectTree {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        background: $surface;
        padding: 0 1;
    }
    SubjectTree:focus {
        border: round $secondary;
    }
    SubjectTree > .tree--cursor {
        background: $secondary;
    }
    """

    BINDINGS: ClassVar = [
        ("enter", "select_subject", "Select"),
    ]

    class SubjectSelected(Message):
        """Posted when a subject is selected."""

        def __init__(self, node: SubjectNode) -> None:
            super().__init__()
            self.node = node

    def __init__(self) -> None:
        super().__init__("Subjects", id="subject_tree")
        self._subjects: dict[str, SubjectNode] = {}
        # Note: Cannot use _nodes - it shadows Textual's internal attribute
        self._subject_nodes: dict[str, TreeNode[SubjectNode]] = {}

    def add_subject(self, subject: str) -> None:
        """Add or update a subject in the tree."""
        parts = subject.split(".")
        full_path = ""
        parent_node = self.root

        for i, part in enumerate(parts):
            full_path = f"{full_path}.{part}" if full_path else part
            is_leaf = i == len(parts) - 1

            if full_path not in self._subject_nodes:
                # Create new node
                node_data = SubjectNode(
                    name=part,
                    full_subject=full_path,
                    is_leaf=is_leaf,
                )
                tree_node = parent_node.add(
                    self._format_label(node_data),
                    data=node_data,
                    expand=True,
                )
                self._subject_nodes[full_path] = tree_node
            else:
                tree_node = self._subject_nodes[full_path]

            # Update counts
            if tree_node.data:
                tree_node.data.increment()
                tree_node.data.is_leaf = is_leaf
                tree_node.set_label(self._format_label(tree_node.data))

            parent_node = tree_node

    def _format_label(self, node: SubjectNode) -> str:
        """Format the label for a tree node."""
        if node.message_count > 0:
            return f"{node.name} ({node.message_count})"
        return node.name

    def clear_subjects(self) -> None:
        """Clear all subjects from the tree."""
        self.clear()
        self._subjects.clear()
        self._subject_nodes.clear()

    def action_select_subject(self) -> None:
        """Handle subject selection."""
        if self.cursor_node and self.cursor_node.data:
            self.post_message(self.SubjectSelected(node=self.cursor_node.data))

    @property
    def selected_subject(self) -> SubjectNode | None:
        """Get the currently selected subject."""
        if self.cursor_node and self.cursor_node.data:
            return self.cursor_node.data
        return None
