# gaanadl-cli

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Download high-quality music from Gaana with metadata and synced lyrics.

## Features

- 🎵 Download tracks, albums, playlists, and artist discographies
- 🔥 Trending and new releases download
- 🔍 Search across Gaana's catalog
- 🎤 Synced lyrics from [LRCLIB](https://lrclib.net)
- 📀 11 output formats (FLAC, MP3, Opus, and more)
- 🏷️ Full metadata + cover art embedding
- ⚡ Fast parallel downloads

## Install

**Requirements:** Python 3.8+ and [FFmpeg](https://ffmpeg.org/download.html)

```bash
pip install gaanadl-cli
```

Or install from source:
```bash
git clone https://github.com/notdeltaxd/gaanadl-cli.git
cd gaanadl-cli
pip install -e .
```

## Usage

```bash
# Download by URL or seokey
gaana https://gaana.com/song/manjha
gaana manjha

# Download album/playlist
gaana https://gaana.com/album/kesariya-from-brahmastra-hindi
gaana https://gaana.com/playlist/hindi-top-50

# Search and download
gaana -s "arijit singh" -t album

# Specify format
gaana manjha -f mp3
```

### Trending & New Releases

```bash
# Download trending tracks (default: Hindi)
gaana --trending
gaana --trending en
gaana --trending pa

# Download new releases
gaana --new-releases
gaana --new-releases en

# Limit number of tracks
gaana --trending hi --limit 5
gaana --new-releases --limit 10
```

### Preview Mode

Use `--show-results` to preview content **without downloading**:

```bash
# Preview trending tracks
gaana --trending hi --limit 10 --show-results

# Preview new releases
gaana --new-releases en --show-results

# Preview search results
gaana -s "arijit singh" -t artist --show-results

# Preview playlist/album tracks
gaana https://gaana.com/playlist/... --show-results
```

> **Note:** When using `--show-results`, no files will be downloaded. This is for preview only.

Run `gaana --help` for all options.

## Formats

| Lossless | Lossy |
|----------|-------|
| flac (default), alac, wav, aiff | mp3, aac, m4a, opus, ogg, wma |

## API

Uses the [Gaana Music API](https://github.com/notdeltaxd/Gaana-API).

## License

MIT
