#!/usr/bin/env python3
"""Convert sequential bitmap images to video."""

import argparse
import glob
import os
import re
import sys

import cv2


def natural_sort_key(filename):
    """Sort filenames naturally (e.g., frame2 before frame10)."""
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', filename)
    ]


def get_bmp_files(input_dir):
    """Get sorted list of BMP files from directory."""
    patterns = ['*.bmp', '*.BMP']
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(input_dir, pattern)))

    if not files:
        return []

    return sorted(files, key=lambda x: natural_sort_key(os.path.basename(x)))


def create_video(input_dir, output_path, fps):
    """Create video from bitmap images."""
    bmp_files = get_bmp_files(input_dir)

    if not bmp_files:
        print(f"Error: No BMP files found in '{input_dir}'")
        return False

    print(f"Found {len(bmp_files)} BMP files")

    # Read first frame to get dimensions
    first_frame = cv2.imread(bmp_files[0])
    if first_frame is None:
        print(f"Error: Could not read '{bmp_files[0]}'")
        return False

    height, width, _ = first_frame.shape
    print(f"Frame size: {width}x{height}")
    print(f"FPS: {fps}")

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not video_writer.isOpened():
        print("Error: Could not create video writer")
        return False

    # Write frames
    print("Processing frames...")
    for i, bmp_file in enumerate(bmp_files, 1):
        frame = cv2.imread(bmp_file)
        if frame is None:
            print(f"Warning: Could not read '{bmp_file}', skipping")
            continue

        # Resize if dimensions don't match first frame
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))

        video_writer.write(frame)

        # Progress indicator
        if i % 10 == 0 or i == len(bmp_files):
            print(f"  Processed {i}/{len(bmp_files)} frames", end='\r')

    video_writer.release()
    print(f"\nVideo saved to: {output_path}")

    duration = len(bmp_files) / fps
    print(f"Duration: {duration:.2f} seconds")

    return True


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Convert sequential BMP images to video'
    )
    parser.add_argument(
        'input_dir',
        help='Directory containing BMP files'
    )
    parser.add_argument(
        '-o', '--output',
        default='output.mp4',
        help='Output video file path (default: output.mp4)'
    )
    parser.add_argument(
        '-f', '--fps',
        type=float,
        required=True,
        help='Frames per second for the output video'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: '{args.input_dir}' is not a valid directory")
        sys.exit(1)

    if args.fps <= 0:
        print("Error: FPS must be a positive number")
        sys.exit(1)

    success = create_video(args.input_dir, args.output, args.fps)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
