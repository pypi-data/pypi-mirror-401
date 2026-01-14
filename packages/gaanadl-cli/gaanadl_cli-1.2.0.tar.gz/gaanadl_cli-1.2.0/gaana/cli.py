"""
CLI Entry Point.
Command-line interface for Gaana music downloader.
"""

import argparse
import sys
from typing import Optional

from .main import GaanaDownloader
from .api import GaanaAPI
from .printer import (
    print_banner, info, success, warning, error as print_error,
    print_search_results, console
)
from .utils import parse_gaana_url, is_url
from .errors import GaanaError


def print_colored_help():
    """Print beautiful colored help using Rich."""
    console.print()
    console.print("[bold cyan]GAANA CLI[/bold cyan] - Download high-quality music from Gaana", style="bold")
    console.print()
    
    # Usage
    console.print("[bold yellow]USAGE:[/bold yellow]")
    console.print("  gaana [cyan]<url_or_seokey>[/cyan] [dim][options][/dim]")
    console.print("  gaana [cyan]-s <query>[/cyan] [dim][options][/dim]")
    console.print()
    
    # Arguments
    console.print("[bold yellow]ARGUMENTS:[/bold yellow]")
    console.print("  [cyan]url_or_seokey[/cyan]    Gaana URL or seokey (e.g. manjha, tera-fitoor)")
    console.print()
    
    # Options
    console.print("[bold yellow]OPTIONS:[/bold yellow]")
    options = [
        ("-s, --search", "QUERY", "Search for content instead of direct download"),
        ("-t, --type", "TYPE", "Content type: [green]auto[/green], track, album, playlist, artist"),
        ("-q, --quality", "LEVEL", "Audio quality: low, medium, [green]high[/green]"),
        ("-f, --format", "FMT", "Output format (see FORMATS below)"),
        ("-o, --output", "DIR", "Output directory [dim](default: ./Music)[/dim]"),
        ("--trending", "LANG", "Download trending tracks [dim](hi, en, pa)[/dim]"),
        ("--new-releases", "LANG", "Download new releases [dim](hi, en, pa)[/dim]"),
        ("--limit", "NUM", "Limit for trending/new-releases [dim](default: 10)[/dim]"),
        ("--workers", "NUM", "Parallel download workers [dim](default: 4)[/dim]"),
        ("--no-lyrics", "", "Don't fetch synced lyrics from LRCLIB"),
        ("--no-banner", "", "Don't show ASCII art banner"),
        ("-v, --version", "", "Show version and exit"),
        ("-h, --help", "", "Show this help message"),
    ]
    for opt, meta, desc in options:
        if meta:
            console.print(f"  [cyan]{opt}[/cyan] [dim]{meta}[/dim]")
            console.print(f"      {desc}")
        else:
            console.print(f"  [cyan]{opt}[/cyan]  {desc}")
    console.print()
    
    # Formats
    console.print("[bold yellow]FORMATS:[/bold yellow]")
    console.print("  [bold green]Lossless:[/bold green] [cyan]flac[/cyan] [dim](default)[/dim], [cyan]alac[/cyan], [cyan]wav[/cyan], [cyan]aiff[/cyan]")
    console.print("  [bold blue]Lossy:[/bold blue]    [cyan]mp3[/cyan] [dim](320k)[/dim], [cyan]aac[/cyan], [cyan]m4a[/cyan], [cyan]opus[/cyan], [cyan]ogg[/cyan], [cyan]wma[/cyan]")
    console.print()
    
    # Examples
    console.print("[bold yellow]EXAMPLES:[/bold yellow]")
    examples = [
        ("gaana [cyan]manjha[/cyan]", "Download track by seokey"),
        ("gaana [cyan]https://gaana.com/song/manjha[/cyan]", "Download from URL"),
        ("gaana [cyan]-s \"arijit singh\"[/cyan] --show-results", "Search and show results"),
        ("gaana [cyan]-s \"kesariya\"[/cyan] -t album", "Search and download album"),
        ("gaana [cyan]manjha[/cyan] -f mp3 -o ./Music", "Download as MP3"),
        ("gaana [cyan]https://gaana.com/playlist/...[/cyan]", "Download entire playlist"),
    ]
    for cmd, desc in examples:
        console.print(f"  {cmd}")
        console.print(f"      [dim]{desc}[/dim]")
    console.print()


class ColoredHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom formatter that triggers colored help."""
    pass


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="gaana",
        description="Download high-quality music from Gaana",
        formatter_class=ColoredHelpFormatter,
        add_help=False,  # We'll handle help ourselves
    )
    
    # Positional argument
    parser.add_argument(
        "url_or_id",
        nargs="?",
        help="Gaana URL or seokey",
    )
    
    # Search mode
    parser.add_argument(
        "-s", "--search",
        metavar="QUERY",
        help="Search for content instead of direct download",
    )
    
    # Content type
    parser.add_argument(
        "-t", "--type",
        choices=["auto", "track", "song", "album", "playlist", "artist"],
        default="auto",
        help="Content type (default: auto-detect from URL)",
    )
    
    # Quality
    parser.add_argument(
        "-q", "--quality",
        choices=["low", "medium", "high"],
        default="high",
        help="Audio quality (default: high)",
    )
    
    # Output format
    parser.add_argument(
        "-f", "--format",
        choices=["flac", "alac", "wav", "aiff", "mp3", "aac", "m4a", "opus", "ogg", "vorbis", "wma"],
        default="flac",
        help="Output audio format (default: flac). Lossless: flac, alac, wav, aiff. Lossy: mp3, aac, m4a, opus, ogg, wma",
    )
    
    # Output directory
    parser.add_argument(
        "-o", "--output",
        default="./Music",
        help="Output directory (default: ./Music)",
    )
    
    # Temp directory
    parser.add_argument(
        "--temp-dir",
        help="Temporary directory for segments (default: output/temp)",
    )
    
    # Naming formats
    parser.add_argument(
        "--format-folder",
        type=int,
        choices=[1, 2, 3, 4],
        default=3,
        help="Folder naming format: 1={artist}, 2={album}, 3={artist}/{album}, 4={artist} - {album}",
    )
    
    parser.add_argument(
        "--format-track",
        type=int,
        choices=[1, 2, 3, 4],
        default=2,
        help="Track naming format: 1={title}, 2={num}. {title}, 3={artist} - {title}, 4={num}. {artist} - {title}",
    )
    
    # Workers
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel download workers (default: 4)",
    )
    
    # Trending/New Releases
    parser.add_argument(
        "--trending",
        metavar="LANG",
        nargs="?",
        const="hi",
        help="Download trending tracks (language: hi, en, pa, etc.)",
    )
    
    parser.add_argument(
        "--new-releases",
        metavar="LANG",
        nargs="?",
        const="hi",
        help="Download new releases (language: hi, en, pa, etc.)",
    )
    
    # Search limit
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Limit for search/trending/new-releases (default: 10)",
    )
    
    # Flags
    parser.add_argument(
        "--show-results",
        action="store_true",
        help="Show search results without downloading",
    )
    
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Don't show ASCII art banner",
    )
    
    parser.add_argument(
        "--no-lyrics",
        action="store_true",
        help="Don't fetch synced lyrics from LRCLIB",
    )
    
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        dest="show_version",
        help="Show version and exit",
    )
    
    parser.add_argument(
        "-h", "--help",
        action="store_true",
        dest="show_help",
        help="Show help message",
    )
    
    return parser


def run_search(args, api: GaanaAPI):
    """Run search and display results."""
    results = api.search(args.search, limit=args.limit)
    
    if not any(results.values()):
        print_error("No results found")
        return
    
    # Display all result types
    for result_type in ["songs", "albums", "playlists", "artists"]:
        if results.get(result_type):
            print_search_results(results, result_type)
            console.print()


def run_download(args, downloader: GaanaDownloader):
    """Run download based on arguments."""
    identifier = args.url_or_id
    content_type = args.type
    
    # Auto-detect from URL
    if content_type == "auto" and is_url(identifier):
        detected_type, extracted_id = parse_gaana_url(identifier)
        if detected_type:
            content_type = detected_type
            info(f"Detected content type: {content_type}")
    
    api = downloader.api
    
    # Handle --show-results for playlist/album
    if args.show_results:
        from .printer import print_playlist_info, print_tracks_list, print_album_info
        
        if content_type == "playlist":
            playlist = api.get_playlist(identifier)
            print_playlist_info(playlist)
            tracks = playlist.get("tracks", [])[:args.limit]
            print_tracks_list(tracks, f"📋 Playlist Tracks (showing {len(tracks)})")
            return
        elif content_type == "album":
            album = api.get_album(identifier)
            print_album_info(album)
            tracks = album.get("tracks", [])[:args.limit]
            print_tracks_list(tracks, f"💿 Album Tracks")
            return
    
    # Normalize type names and download
    if content_type in ["track", "song", "auto"]:
        downloader.download_track(identifier)
    elif content_type == "album":
        downloader.download_album(identifier)
    elif content_type == "playlist":
        downloader.download_playlist(identifier)
    elif content_type == "artist":
        downloader.download_artist_top(identifier)


def run_search_download(args, downloader: GaanaDownloader):
    """Search and download first result."""
    content_type = args.type
    
    # Normalize type
    if content_type in ["track", "song", "auto"]:
        content_type = "songs"
    elif content_type == "album":
        content_type = "albums"
    elif content_type == "playlist":
        content_type = "playlists"
    elif content_type == "artist":
        content_type = "artists"
    
    downloader.search_and_download(
        args.search,
        content_type=content_type,
        limit=1,
    )


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show colored help
    if args.show_help:
        print_colored_help()
        sys.exit(0)
    
    # Show rich version
    if args.show_version:
        from . import __version__
        print_banner()
        console.print(f"[bold cyan]Version:[/bold cyan] {__version__}")
        console.print(f"[bold cyan]Python:[/bold cyan] {sys.version.split()[0]}")
        console.print(f"[bold cyan]GitHub:[/bold cyan] https://github.com/notdeltaxd/gaanadl-cli")
        console.print(f"[bold cyan]PyPI:[/bold cyan] https://pypi.org/project/gaanadl-cli/")
        sys.exit(0)
    
    # Show banner
    if not args.no_banner:
        print_banner()
    
    # Validate arguments - show colored help if nothing provided
    if not args.url_or_id and not args.search and not args.trending and not getattr(args, 'new_releases', None):
        print_colored_help()
        sys.exit(1)
    
    try:
        # Initialize downloader
        downloader = GaanaDownloader(
            output_dir=args.output,
            temp_dir=args.temp_dir,
            output_format=args.format,
            quality=args.quality,
            workers=args.workers,
            folder_format=args.format_folder,
            track_format=args.format_track,
            lyrics=not args.no_lyrics,
        )
        
        api = downloader.api
        
        # Check API health
        if not api.health_check():
            warning("API may be unavailable, proceeding anyway...")
        
        # Execute based on mode
        if args.trending:
            if args.show_results:
                tracks = api.get_trending(args.trending, args.limit)
                from .printer import print_tracks_list
                print_tracks_list(tracks, f"🔥 Trending Tracks ({args.trending.upper()})")
            else:
                downloader.download_trending(args.trending, args.limit)
        elif getattr(args, 'new_releases', None):
            if args.show_results:
                data = api.get_new_releases(args.new_releases)
                tracks = data.get("tracks", [])[:args.limit]
                from .printer import print_tracks_list
                print_tracks_list(tracks, f"🎁 New Releases ({args.new_releases.upper()})")
            else:
                downloader.download_new_releases(args.new_releases, args.limit)
        elif args.search:
            if args.show_results:
                run_search(args, api)
            else:
                run_search_download(args, downloader)
        else:
            run_download(args, downloader)
        
        success("Done!")
        
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted by user[/dim]")
        sys.exit(130)
    except GaanaError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
