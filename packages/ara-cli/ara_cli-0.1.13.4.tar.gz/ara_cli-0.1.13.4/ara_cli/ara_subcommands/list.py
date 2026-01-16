import typer
from ara_cli.error_handler import AraError
from typing import Optional, List, Tuple
from .common import MockArgs
from ara_cli.completers import DynamicCompleters
from ara_cli.ara_command_action import list_action


def _validate_extension_options(
    include_extension: Optional[List[str]], exclude_extension: Optional[List[str]]
) -> None:
    """Validate that include and exclude extension options are mutually exclusive."""
    if include_extension and exclude_extension:
        raise AraError(
            "--include-extension/-i and --exclude-extension/-e are mutually exclusive"
        )


def _validate_exclusive_options(
    branch: bool,
    children: bool,
    data: bool,
) -> None:
    """Validate that branch, children, and data options are mutually exclusive."""
    exclusive_options = [branch, children, data]
    true_options = [opt for opt in exclusive_options if opt]
    if len(true_options) > 1:
        raise AraError("--branch, --children, and --data are mutually exclusive")


def list_main(
    classifier: Optional[str] = typer.Argument(
        None,
        help="The classifier of the artefact",
        autocompletion=DynamicCompleters.create_classifier_completer(),
    ),
    artefact_name: Optional[str] = typer.Argument(
        None,
        help="The name of the artefact",
        autocompletion=DynamicCompleters.create_artefact_name_completer(),
    ),
    include_content: Optional[List[str]] = typer.Option(
        None,
        "-I",
        "--include-content",
        help="filter for files which include given content",
    ),
    exclude_content: Optional[List[str]] = typer.Option(
        None,
        "-E",
        "--exclude-content",
        help="filter for files which do not include given content",
    ),
    include_tags: Optional[List[str]] = typer.Option(
        None, "--include-tags", help="filter for files which include given tags"
    ),
    exclude_tags: Optional[List[str]] = typer.Option(
        None, "--exclude-tags", help="filter for files which do not include given tags"
    ),
    include_extension: Optional[List[str]] = typer.Option(
        None,
        "-i",
        "--include-extension",
        "--include-classifier",
        help="list of extensions to include in listing",
    ),
    exclude_extension: Optional[List[str]] = typer.Option(
        None,
        "-e",
        "--exclude-extension",
        "--exclude-classifier",
        help="list of extensions to exclude from listing",
    ),
    branch: bool = typer.Option(
        False,
        "-b",
        "--branch",
        help="List artefacts in the parent chain (requires classifier and artefact_name)",
    ),
    children: bool = typer.Option(
        False,
        "-c",
        "--children",
        help="List child artefacts (requires classifier and artefact_name)",
    ),
    data: bool = typer.Option(
        False,
        "-d",
        "--data",
        help="List file in the data directory (requires classifier and artefact_name)",
    ),
):
    """List files with optional tags.

    Examples:
        ara list feature my_feature --data --include-extension .md
        ara list --include-extension .feature
        ara list userstory my_story --children
        ara list userstory my_story --branch --include-extension .businessgoal
        ara list --include-content "example content" --include-extension .task
    """
    _validate_extension_options(include_extension, exclude_extension)
    _validate_exclusive_options(branch, children, data)

    # If classifier is provided but no artefact_name, and no other specific flags are set,
    # treat it as a filter by classifier (extension).
    # This supports "ara list feature" -> lists all features.
    if classifier and not artefact_name and not (branch or children or data):
        # We append the classifier (prefixed with '.') to include_extension
        # This assumes classifier names correspond to extensions (e.g. 'feature' -> '.feature')
        # existing logic usually expects the extension format.
        ext = f".{classifier}"
        if include_extension:
            include_extension.append(ext)
        else:
            include_extension = [ext]
        # Clear classifier from args so it doesn't trigger other logic
        classifier = None

    args = MockArgs(
        classifier=classifier,
        artefact_name=artefact_name,
        include_content=include_content,
        exclude_content=exclude_content,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        include_extension=include_extension,
        exclude_extension=exclude_extension,
        branch=branch,
        children=children,
        data=data,
    )

    list_action(args)


def register(parent: typer.Typer):
    help_text = "List files with optional tags"
    parent.command(name="list", help=help_text)(list_main)
