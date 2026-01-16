# BMP to Video Converter

A command-line tool to convert sequential bitmap images into a video file.

## Requirements

- Python 3.6+

## Installation

### Install from PyPI (when published)

```bash
pip install bmp-to-vid
```

### Install from source

```bash
git clone https://github.com/yourusername/bmp-to-vid.git
cd bmp-to-vid
pip install .
```

### Install in development mode

```bash
pip install -e .
```

## Usage

After installation, use the `bmp-to-vid` command:

```bash
bmp-to-vid <input_directory> -f <fps> [-o output.mp4]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `input_directory` | Yes | Directory containing BMP files |
| `-f`, `--fps` | Yes | Frames per second for output video |
| `-o`, `--output` | No | Output video path (default: `output.mp4`) |
| `-h`, `--help` | No | Show help message |

### Examples

```bash
# Basic usage at 30 FPS
bmp-to-vid ./frames -f 30

# Custom output filename
bmp-to-vid ./frames -f 24 -o my_video.mp4

# High frame rate video
bmp-to-vid ./frames -f 60 -o smooth.mp4

# Show help
bmp-to-vid --help
```

## Supported File Naming

The tool automatically sorts frames using natural sorting. Any naming pattern with numbers will work:

- `frame_001.bmp`, `frame_002.bmp`, `frame_010.bmp`
- `A_001.bmp`, `A_002.bmp`, `A_010.bmp`
- `img1.bmp`, `img2.bmp`, `img10.bmp`
- `001.bmp`, `002.bmp`, `010.bmp`

Both `.bmp` and `.BMP` extensions are supported.

## Output

- Format: MP4 (H.264 compatible)
- Resolution: Same as input images
- Audio: None

## License

MIT
