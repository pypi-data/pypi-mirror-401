"""Genome Profiling tool for analyzing genome sequences."""

from typing import List, Optional, TYPE_CHECKING

from .base import BaseTool

if TYPE_CHECKING:
    from ..sdk.session import Session


class GenomeProfiling(BaseTool):
    """Tool for extracting and profiling proteins from a genome sequence.

    This tool reads a genome sequence from a FASTA file, performs ORF detection on that
    sequence, translates the ORFs to proteins, and runs the sequence profiling engine
    on each protein in parallel. Only the first sequence in the FASTA file is processed.

    Example:
        >>> from valthos import Session
        >>> session = Session()
        >>>
        >>> # Run profiling on a genome from FASTA file
        >>> profiler = session.tools.GenomeProfiling(
        ...     input="s3://bucket/genome.fasta",
        ...     output="s3://bucket/results/genome_profiling.json",
        ...     log_file="s3://bucket/logs/genome_profiling.log",
        ...     methods=["world"],
        ...     min_orf_length=90,  # Minimum 30 amino acids
        ...     include_reverse_strand=True
        ... )
        >>>
        >>> # Validate inputs
        >>> validation = profiler.validate()
        >>> if validation['status'] == 'valid':
        ...     # Estimate runtime
        ...     estimate = profiler.estimate()
        ...     print(f"Estimated time: {estimate['estimated_time_minutes']} minutes")
        ...     print(f"Estimated ORFs: {estimate['details']['estimated_orfs']}")
        ...
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
        min_orf_length: int = 90,
        include_reverse_strand: bool = True,
        workspace_rid: Optional[str] = None,
        **kwargs
    ):
        """Initialize the Genome Profiling tool.

        Args:
            session: Authenticated Valthos session
            input: Path to FASTA file containing genome sequence(s)
            output: Output path for results (workspace-relative or S3 URL)
            log_file: Path for log file (workspace-relative or S3 URL)
            methods: List of method names to run on each protein (default: ["world"])
            min_orf_length: Minimum ORF length in nucleotides (default: 90 = 30 amino acids)
            include_reverse_strand: Whether to find ORFs on reverse strand (default: True)
            workspace_rid: Optional workspace RID for path resolution
            **kwargs: Additional configuration parameters
        """
        # Prepare config dict for the API
        config = {
            "methods": methods or ["world"],
            "min_orf_length": min_orf_length,
            "include_reverse_strand": include_reverse_strand,
            **kwargs  # Pass through any additional config
        }

        super().__init__(
            session=session,
            module_type="genome_profiling",
            input=input,
            output=output,
            log_file=log_file,
            workspace_rid=workspace_rid,
            **config
        )

        # Store for easy access
        self.input_path = input
        self.methods = config["methods"]
        self.min_orf_length = min_orf_length
        self.include_reverse_strand = include_reverse_strand

    def __repr__(self) -> str:
        return (
            f"GenomeProfiling(input='{self.input_path}', "
            f"methods={self.methods}, "
            f"output='{self.output_path}')"
        )