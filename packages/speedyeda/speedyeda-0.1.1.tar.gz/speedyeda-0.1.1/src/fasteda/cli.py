"""
Command-line interface for FastEDA.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from fasteda.loader import load_data
from fasteda.analysis import analyze
from fasteda.display import display_results, print_success, print_error, print_info
from fasteda.visualize import generate_plots
from fasteda.report import save_report
from fasteda.presets import apply_preset, list_presets
from fasteda.interactive import (
    interactive_column_selection,
    interactive_plot_selection,
    interactive_preset_selection,
    interactive_export_options,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="🚀 FastEDA - One-line data exploration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fasteda sales.csv
  fasteda survey.xlsx --fun
  fasteda products.csv --preset ecommerce
  fasteda data.csv --interactive
  fasteda file1.csv file2.csv --batch
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='Dataset file(s) to analyze (CSV, Excel, JSON, Parquet)'
    )
    
    parser.add_argument(
        '--fun',
        action='store_true',
        help='Enable fun mode with emojis and colorful output'
    )
    
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show summary mode (same as default)'
    )
    
    parser.add_argument(
        '--plots',
        action='store_true',
        help='Generate and save visualizations'
    )
    
    parser.add_argument(
        '--save',
        type=str,
        metavar='FILE',
        help='Save report to file (e.g., report.json or report.txt)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode with guided prompts'
    )
    
    parser.add_argument(
        '--preset',
        type=str,
        choices=list_presets(),
        help='Use a preset configuration'
    )
    
    parser.add_argument(
        '--columns',
        type=str,
        help='Comma-separated list of columns to analyze'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process multiple files in batch mode'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress terminal output'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='fasteda_output',
        help='Directory for output files (default: fasteda_output)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='fasteda 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Process files
    if len(args.files) > 1 or args.batch:
        # Batch mode
        process_batch(args)
    else:
        # Single file mode
        process_single_file(args.files[0], args)


def process_single_file(filepath: str, args):
    """Process a single file."""
    try:
        # Load data
        if not args.quiet:
            print_info(f"Loading {filepath}...", args.fun)
        
        df = load_data(filepath)
        
        if not args.quiet:
            print_success(f"Loaded {len(df):,} rows × {len(df.columns)} columns", args.fun)
        
        # Interactive mode
        selected_columns = None
        preset_config = None
        
        if args.interactive:
            # Interactive column selection
            selected_columns = interactive_column_selection(df)
            
            # Interactive preset selection
            preset_name = interactive_preset_selection()
            if preset_name:
                preset_config = apply_preset(df, preset_name)
                if preset_config['focus_columns']:
                    selected_columns = preset_config['focus_columns']
        
        elif args.preset:
            # Apply preset
            preset_config = apply_preset(df, args.preset)
            if preset_config['focus_columns']:
                selected_columns = preset_config['focus_columns']
        
        elif args.columns:
            # Manual column selection
            selected_columns = [col.strip() for col in args.columns.split(',')]
            # Validate columns exist
            selected_columns = [col for col in selected_columns if col in df.columns]
        
        # Perform analysis
        if not args.quiet:
            print_info("Analyzing dataset...", args.fun)
        
        results = analyze(df, fun=args.fun, columns=selected_columns)
        
        # Display results
        if not args.quiet:
            display_results(results, args.fun)
        
        # Generate plots
        if args.plots or args.interactive:
            output_dir = Path(args.output_dir)
            if not args.quiet:
                print_info(f"Generating visualizations...", args.fun)
            
            plot_results = generate_plots(df, output_dir=output_dir)
            
            if not args.quiet and plot_results:
                print_success(f"Plots saved to {output_dir}/", args.fun)
        
        # Save report
        save_path = args.save
        if args.interactive and not save_path:
            save_path = interactive_export_options()
        
        if save_path:
            save_report(results, save_path)
            if not args.quiet:
                print_success(f"Report saved to {save_path}", args.fun)
        
        if not args.quiet:
            print_success("Analysis complete! ✨", args.fun)
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)


def process_batch(args):
    """Process multiple files in batch mode."""
    print_info(f"Processing {len(args.files)} files in batch mode...", args.fun)
    
    for idx, filepath in enumerate(args.files, 1):
        print_info(f"\n[{idx}/{len(args.files)}] Processing {filepath}", args.fun)
        
        try:
            df = load_data(filepath)
            results = analyze(df, fun=args.fun)
            
            # Save each report
            file_stem = Path(filepath).stem
            output_dir = Path(args.output_dir) / file_stem
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save text report
            report_path = output_dir / f"{file_stem}_report.txt"
            save_report(results, str(report_path))
            
            # Generate plots
            if args.plots:
                generate_plots(df, output_dir=output_dir)
            
            print_success(f"✓ {filepath} -> {output_dir}/", args.fun)
        
        except Exception as e:
            print_error(f"✗ {filepath}: {str(e)}")
            continue
    
    print_success(f"\nBatch processing complete! Results in {args.output_dir}/", args.fun)


if __name__ == '__main__':
    main()
