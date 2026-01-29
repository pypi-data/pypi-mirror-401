"""
Command-line interface for embedding-eval.

Usage:
    embedding-eval compare --doc document.txt --qa qa_pairs.json --models st:bge-base st:minilm
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="embedding-eval",
        description="Fair embedding model evaluation with independent parameter optimization",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Compare command
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare embedding models with fair optimization",
    )
    compare_parser.add_argument(
        "--doc",
        type=Path,
        required=True,
        help="Path to document file (txt, md)",
    )
    compare_parser.add_argument(
        "--qa",
        type=Path,
        required=True,
        help="Path to Q&A pairs JSON file",
    )
    compare_parser.add_argument(
        "--models",
        nargs="+",
        default=["st:bge-base"],
        help="Model specifications (e.g., st:bge-base st:minilm)",
    )
    compare_parser.add_argument(
        "--chunk-sizes",
        nargs="+",
        type=int,
        default=[256, 384, 512],
        help="Chunk sizes to evaluate",
    )
    compare_parser.add_argument(
        "--overlaps",
        nargs="+",
        type=int,
        default=[25, 50, 100],
        help="Overlap sizes to evaluate",
    )
    compare_parser.add_argument(
        "--top-ks",
        nargs="+",
        type=int,
        default=[5, 10, 15],
        help="Top-k values to evaluate",
    )
    compare_parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON file for results",
    )
    compare_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    # Version command
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    if args.command == "compare":
        run_compare(args)
    else:
        parser.print_help()
        sys.exit(1)


def run_compare(args):
    """Run the compare command."""
    from embedding_eval import run_fair_comparison

    # Load document
    if not args.doc.exists():
        print(f"Error: Document not found: {args.doc}", file=sys.stderr)
        sys.exit(1)

    doc_content = args.doc.read_text()

    # Load Q&A pairs
    if not args.qa.exists():
        print(f"Error: Q&A file not found: {args.qa}", file=sys.stderr)
        sys.exit(1)

    with open(args.qa) as f:
        qa_pairs = json.load(f)

    if not isinstance(qa_pairs, list):
        print("Error: Q&A file must contain a JSON array", file=sys.stderr)
        sys.exit(1)

    # Run comparison
    results = run_fair_comparison(
        models=args.models,
        doc_content=doc_content,
        qa_pairs=qa_pairs,
        chunk_sizes=args.chunk_sizes,
        overlaps=args.overlaps,
        top_ks=args.top_ks,
        verbose=not args.quiet,
    )

    # Save results if output specified
    if args.output:
        output_data = []
        for r in results:
            output_data.append(
                {
                    "model_spec": r.model_spec,
                    "model_name": r.model_name,
                    "dimensions": r.dimensions,
                    "best_accuracy": r.best_accuracy,
                    "best_params": r.best_params,
                    "baseline_accuracy": r.baseline_accuracy,
                    "improvement_pct": r.improvement_pct,
                    "ci_lower": r.ci_lower,
                    "ci_upper": r.ci_upper,
                    "configurations_tested": r.configurations_tested,
                    "optimization_time_seconds": r.optimization_time_seconds,
                }
            )

        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)

        if not args.quiet:
            print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
