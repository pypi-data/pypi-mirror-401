"""Protein Profiling tool for analyzing single protein sequences."""

from typing import List, Optional, TYPE_CHECKING

from .base import BaseTool

if TYPE_CHECKING:
    from ..sdk.session import Session


class ProteinProfiling(BaseTool):
    """Tool for running multiple bioinformatics methods on a single protein sequence.

    This tool reads a protein sequence from a FASTA file and orchestrates the execution
    of various analysis methods (world, cypress_1, etc.) through the Protein Profiling Engine.
    Only the first sequence in the FASTA file is processed.

    Example:
        >>> from valthos import Session
        >>> session = Session()
        >>>
        >>> # Run profiling on a protein from FASTA file
        >>> profiler = session.tools.ProteinProfiling(
        ...     input="s3://bucket/protein.fasta",
        ...     output="s3://bucket/results/profiling.json",
        ...     log_file="s3://bucket/logs/profiling.log",
        ...     methods=["world"]
        ... )
        >>>
        >>> # Validate inputs
        >>> validation = profiler.validate()
        >>> if validation['status'] == 'valid':
        ...     # Submit job
        ...     result = profiler.run()
        ...     print(f"Job ID: {result['job_id']}")
    """

    def __init__(
        self,
        session: "Session",
        input: str,
        output: str,
        log_file: str,
        methods: Optional[List[str]] = None,
        workspace_rid: Optional[str] = None,
        **kwargs
    ):
        """Initialize the Protein Profiling tool.

        Args:
            session: Authenticated Valthos session
            input: Path to FASTA file containing protein sequence(s)
            output: Output path for results (workspace-relative or S3 URL)
            log_file: Path for log file (workspace-relative or S3 URL)
            methods: List of method names to run (default: ["world"])
            workspace_rid: Optional workspace RID for path resolution
            **kwargs: Additional configuration parameters
        """
        # Prepare config dict for the API
        config = {
            "methods": methods or ["world"],
            **kwargs  # Pass through any additional config
        }

        super().__init__(
            session=session,
            module_type="protein_profiling",
            input=input,
            output=output,
            log_file=log_file,
            workspace_rid=workspace_rid,
            **config
        )

        # Store for easy access
        self.input_path = input
        self.methods = config["methods"]

    def __repr__(self) -> str:
        return (
            f"ProteinProfiling(input='{self.input_path}', "
            f"methods={self.methods}, output='{self.output_path}')"
        )