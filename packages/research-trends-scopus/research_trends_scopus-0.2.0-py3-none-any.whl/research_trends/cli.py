"""
Command-line interface for Research Trends.

Provides CLI commands for searching, analyzing, and visualizing research data.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from research_trends import __version__
from research_trends.config import Config


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog='research-trends',
        description='Research Trends - Analyze research publication trends from Scopus',
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for publications')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument(
        '--years',
        help='Year range (e.g., 2020-2025)',
        type=str
    )
    search_parser.add_argument(
        '--max-results',
        help='Maximum number of results',
        type=int,
        default=500
    )
    search_parser.add_argument(
        '--output',
        '-o',
        help='Output file path (JSON)',
        type=str
    )
    search_parser.add_argument(
        '--api-key',
        help='Scopus API key',
        type=str
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze publication data')
    analyze_parser.add_argument('input', help='Input JSON file from search')
    analyze_parser.add_argument(
        '--output',
        '-o',
        help='Output file for analysis results',
        type=str
    )
    analyze_parser.add_argument(
        '--format',
        help='Output format (json, csv, text)',
        choices=['json', 'csv', 'text'],
        default='text'
    )
    
    # Dashboard command
    dash_parser = subparsers.add_parser('dashboard', help='Launch interactive dashboard')
    dash_parser.add_argument('input', help='Input JSON file from search')
    dash_parser.add_argument(
        '--port',
        '-p',
        help='Port number',
        type=int,
        default=8050
    )
    dash_parser.add_argument(
        '--host',
        help='Host address',
        type=str,
        default='127.0.0.1'
    )
    dash_parser.add_argument(
        '--debug',
        help='Enable debug mode',
        action='store_true'
    )
    
    # Recommend command
    rec_parser = subparsers.add_parser('recommend', help='Get research recommendations')
    rec_parser.add_argument('input', help='Input JSON file from search')
    rec_parser.add_argument(
        '--top',
        '-n',
        help='Number of recommendations per category',
        type=int,
        default=5
    )
    rec_parser.add_argument(
        '--output',
        '-o',
        help='Output file for recommendations',
        type=str
    )
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_parser.add_argument(
        '--init',
        help='Create default configuration file',
        action='store_true'
    )
    config_parser.add_argument(
        '--show',
        help='Show current configuration',
        action='store_true'
    )
    
    return parser


def cmd_search(args: argparse.Namespace) -> int:
    """Execute the search command."""
    from research_trends.client import ScopusClient
    from research_trends.models import SearchResult
    
    # Parse year range
    start_year = None
    end_year = None
    
    if args.years:
        try:
            parts = args.years.split('-')
            start_year = int(parts[0])
            end_year = int(parts[1]) if len(parts) > 1 else None
        except (ValueError, IndexError):
            print(f"Error: Invalid year range format: {args.years}")
            return 1
    
    # Create client
    try:
        client = ScopusClient(api_key=args.api_key)
        
        print(f"Searching for: {args.query}")
        
        result = client.search(
            query=args.query,
            start_year=start_year,
            end_year=end_year,
            max_results=args.max_results,
        )
        
        print(f"\nFound {result.total_results} total results")
        print(f"Retrieved {len(result.publications)} publications")
        
        # Save results
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(result.to_dict(), f, indent=2, default=str)
            print(f"\nResults saved to: {output_path}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_analyze(args: argparse.Namespace) -> int:
    """Execute the analyze command."""
    from research_trends.analyzer import TrendAnalyzer
    from research_trends.models import SearchResult
    
    # Load data
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        result = SearchResult.from_dict(data)
        analyzer = TrendAnalyzer(result)
        summary = analyzer.summary()
        
        if args.format == 'json':
            output = json.dumps(summary, indent=2, default=str)
        elif args.format == 'csv':
            import pandas as pd
            df = analyzer.to_dataframe()
            output = df.to_csv(index=False)
        else:
            # Text format
            lines = [
                "=" * 50,
                "RESEARCH TRENDS ANALYSIS",
                "=" * 50,
                "",
                f"Total Publications: {summary['total_publications']}",
                f"Year Range: {summary['year_range'][0]} - {summary['year_range'][1]}",
                f"Unique Authors: {summary['unique_authors']}",
                f"Unique Affiliations: {summary['unique_affiliations']}",
                f"Unique Keywords: {summary['unique_keywords']}",
                f"Open Access Ratio: {summary['open_access_ratio']:.1%}",
                "",
                "Citation Statistics:",
                f"  Total: {summary['citation_stats']['total']}",
                f"  Mean: {summary['citation_stats']['mean']:.1f}",
                f"  Median: {summary['citation_stats']['median']:.1f}",
                f"  Max: {summary['citation_stats']['max']}",
                "",
                "Top Authors:",
            ]
            
            for author, count in analyzer.get_top_authors(10):
                lines.append(f"  - {author}: {count}")
            
            lines.extend([
                "",
                "Top Keywords:",
            ])
            
            for keyword, count in analyzer.get_top_keywords(10):
                lines.append(f"  - {keyword}: {count}")
            
            output = "\n".join(lines)
        
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                f.write(output)
            print(f"Analysis saved to: {output_path}")
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_dashboard(args: argparse.Namespace) -> int:
    """Execute the dashboard command."""
    from research_trends.analyzer import TrendAnalyzer
    from research_trends.dashboard import Dashboard
    from research_trends.models import SearchResult
    
    # Load data
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        result = SearchResult.from_dict(data)
        analyzer = TrendAnalyzer(result)
        dashboard = Dashboard(analyzer)
        
        dashboard.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
        )
        
        return 0
        
    except ImportError as e:
        print(f"Error: {e}")
        print("Install dashboard dependencies with: pip install research-trends-scopus[notebook]")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_recommend(args: argparse.Namespace) -> int:
    """Execute the recommend command."""
    from research_trends.analyzer import TrendAnalyzer
    from research_trends.recommender import Recommender
    from research_trends.models import SearchResult
    
    # Load data
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        result = SearchResult.from_dict(data)
        analyzer = TrendAnalyzer(result)
        recommender = Recommender(analyzer)
        
        report = recommender.to_report()
        
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Recommendations saved to: {output_path}")
        else:
            print(report)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_config(args: argparse.Namespace) -> int:
    """Execute the config command."""
    if args.init:
        try:
            config_path = Config.create_default_config()
            print(f"Created default configuration at: {config_path}")
            print("Edit this file to add your Scopus API key.")
            return 0
        except Exception as e:
            print(f"Error creating config: {e}")
            return 1
    
    if args.show:
        try:
            config = Config()
            print("Current configuration:")
            for key, value in config.to_dict().items():
                if key == 'api_key' and value:
                    value = value[:4] + '****' + value[-4:]
                print(f"  {key}: {value}")
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    print("Use --init to create config or --show to display it")
    return 0


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    commands = {
        'search': cmd_search,
        'analyze': cmd_analyze,
        'dashboard': cmd_dashboard,
        'recommend': cmd_recommend,
        'config': cmd_config,
    }
    
    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)
    
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
