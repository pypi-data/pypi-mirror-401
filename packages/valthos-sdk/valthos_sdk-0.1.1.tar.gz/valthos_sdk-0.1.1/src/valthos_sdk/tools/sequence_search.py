"""Sequence Search tool for finding similar proteins using MMseqs2."""

from typing import Optional, TYPE_CHECKING

from .base import BaseTool

if TYPE_CHECKING:
    from ..sdk.session import Session


class SequenceSearch(BaseTool):
    """Tool for searching protein similarities using MMseqs2.

    Takes a protein sequence string and searches for similar proteins in an
    MMseqs2 database. Results include e-values, percent identity, and taxonomy.

    Example:
        >>> from valthos import Session
        >>> session = Session()
        >>>
        >>> searcher = session.tools.SequenceSearch(
        ...     sequence="MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNL",
        ...     output="s3://bucket/results/search_results.json",
        ...     log_file="s3://bucket/logs/search.log",
        ...     num_hits=50,
        ...     sensitivity=7.5,
        ...     target_database="default"  # or "select_agents"
        ... )
        >>>
        >>> validation = searcher.validate()
        >>> if validation['status'] == 'valid':
        ...     result = searcher.run()
        ...     print(f"Job ID: {result['job_id']}")
    """

    def __init__(
        self,
        session: "Session",
        sequence: str,
        output: str,
        log_file: str,
        protein_id: str = "query",
        target_database: Optional[str] = None,
        num_hits: int = 10,
        sensitivity: float = 7.5,
        start_sens: Optional[float] = 1.0,
        sens_steps: Optional[int] = 3,
        threads: int = 4,
        split_memory_limit: Optional[int] = None,
        db_load_mode: int = 2,
        force_db_download: bool = False,
        backend: str = "modal",
        workspace_rid: Optional[str] = None,
        **kwargs
    ):
        """Initialize the Sequence Search tool.

        Args:
            session: Authenticated Valthos session
            sequence: Protein sequence string to search
            output: Output path for results (workspace-relative or S3 URL)
            log_file: Path for log file (workspace-relative or S3 URL)
            protein_id: Identifier for the query protein (default: "query")
            target_database: Target database to search. Options: 'default', 'select_agents'.
                Defaults to 'default' if not specified.
            num_hits: Maximum number of hits to return (default: 10)
            sensitivity: MMseqs2 search sensitivity (default: 7.5)
            start_sens: Starting sensitivity for iterative search (default: 1.0)
            sens_steps: Number of sensitivity steps (default: 3)
            threads: Number of threads to use (default: 4)
            split_memory_limit: Memory limit for splits in MB (default: None)
            db_load_mode: Database load mode (default: 2)
            force_db_download: Force re-download of the database (default: False)
            backend: Compute backend to use (default: "modal")
            workspace_rid: Optional workspace RID for path resolution
            **kwargs: Additional configuration parameters
        """
        # Build config with sequence and search parameters
        config = {
            "sequence": sequence,
            "protein_id": protein_id,
            "num_hits": num_hits,
            "sensitivity": sensitivity,
            "start_sens": start_sens,
            "sens_steps": sens_steps,
            "threads": threads,
            "db_load_mode": db_load_mode,
            "force_db_download": force_db_download,
            "backend": backend,
            **kwargs
        }

        if target_database is not None:
            config["target_database"] = target_database
        if split_memory_limit is not None:
            config["split_memory_limit"] = split_memory_limit

        super().__init__(
            session=session,
            module_type="sequence_search",
            input="sequence_search",  # Placeholder - actual sequence is in config
            output=output,
            log_file=log_file,
            workspace_rid=workspace_rid,
            **config
        )

        # Store for easy access
        self.sequence = sequence
        self.protein_id = protein_id
        self.target_database = target_database
        self.num_hits = num_hits
        self.sensitivity = sensitivity

    def __repr__(self) -> str:
        seq_preview = self.sequence[:20] + "..." if len(self.sequence) > 20 else self.sequence
        db_info = self.target_database or "default"
        return (
            f"SequenceSearch(sequence='{seq_preview}', "
            f"target_database='{db_info}', "
            f"num_hits={self.num_hits}, sensitivity={self.sensitivity})"
        )
