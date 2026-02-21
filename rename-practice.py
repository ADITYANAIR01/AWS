#!/usr/bin/env python3
"""
AWS Practice File Renaming Tool
Automatically renames screenshots sequentially and videos to match folder name.
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple


def natural_sort_key(filename: str) -> List:
    """
    Generate a key for natural sorting (handles numbers correctly).
    Example: ['1.png', '2.png', '10.png'] instead of ['1.png', '10.png', '2.png']
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', filename)]


def get_folder_name(folder_path: str) -> str:
    """Extract folder name from path and convert to lowercase."""
    path = Path(folder_path)
    folder_name = path.name
    return folder_name.lower()


def is_already_renamed(filename: str, prefix: str) -> bool:
    """Check if file already matches the target naming pattern."""
    # Pattern: prefix-01.ext or prefix.ext (for videos)
    pattern = rf'^{re.escape(prefix)}(-\d+)?\.[\w]+$'
    return bool(re.match(pattern, filename))


def find_media_files(folder_path: str) -> Tuple[List[str], List[str]]:
    """
    Find all image and video files in the folder.
    Returns: (image_files, video_files)
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
    
    images = []
    videos = []
    
    try:
        folder = Path(folder_path)
        if not folder.exists():
            return [], []
        
        for file in folder.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                if ext in image_extensions:
                    images.append(file.name)
                elif ext in video_extensions:
                    videos.append(file.name)
        
        # Sort naturally
        images.sort(key=natural_sort_key)
        videos.sort(key=natural_sort_key)
        
        return images, videos
    
    except Exception as e:
        print(f"Error scanning folder: {e}")
        return [], []


def generate_rename_plan(folder_path: str, images: List[str], videos: List[str], prefix: str) -> List[Tuple[str, str]]:
    """
    Generate a list of (old_name, new_name) tuples for renaming.
    Returns empty list if no changes needed.
    """
    rename_plan = []
    folder = Path(folder_path)
    
    # Process images
    if images:
        # Determine zero-padding based on total count
        total_images = len(images)
        padding = len(str(total_images))  # 2 digits for <100, 3 for <1000, etc.
        if padding < 2:
            padding = 2  # Minimum 2 digits
        
        for idx, old_name in enumerate(images, start=1):
            # Skip if already in correct format
            if is_already_renamed(old_name, prefix):
                continue
            
            ext = Path(old_name).suffix
            new_name = f"{prefix}-{str(idx).zfill(padding)}{ext}"
            
            # Avoid duplicate names
            if new_name != old_name and not (folder / new_name).exists():
                rename_plan.append((old_name, new_name))
    
    # Process videos
    if videos:
        if len(videos) == 1:
            # Single video: rename to {prefix}.ext
            old_name = videos[0]
            ext = Path(old_name).suffix
            new_name = f"{prefix}{ext}"
            
            if not is_already_renamed(old_name, prefix) and new_name != old_name:
                rename_plan.append((old_name, new_name))
        else:
            # Multiple videos: rename to {prefix}-part1.ext, {prefix}-part2.ext, etc.
            for idx, old_name in enumerate(videos, start=1):
                if is_already_renamed(old_name, prefix):
                    continue
                
                ext = Path(old_name).suffix
                new_name = f"{prefix}-part{idx}{ext}"
                
                if new_name != old_name and not (folder / new_name).exists():
                    rename_plan.append((old_name, new_name))
    
    return rename_plan


def display_preview(rename_plan: List[Tuple[str, str]]) -> None:
    """Display a preview of all rename operations."""
    if not rename_plan:
        print("\n✓ All files are already properly named. No changes needed.")
        return
    
    print("\nPreview of changes:")
    print("-" * 60)
    
    # Find max length for alignment
    max_old_len = max(len(old) for old, _ in rename_plan)
    
    for old_name, new_name in rename_plan:
        print(f"  {old_name.ljust(max_old_len)} → {new_name}")
    
    print("-" * 60)
    print(f"Total: {len(rename_plan)} file(s) to rename")


def execute_renaming(folder_path: str, rename_plan: List[Tuple[str, str]]) -> int:
    """
    Execute the renaming operations.
    Returns: number of files successfully renamed
    """
    folder = Path(folder_path)
    success_count = 0
    
    for old_name, new_name in rename_plan:
        try:
            old_path = folder / old_name
            new_path = folder / new_name
            
            old_path.rename(new_path)
            success_count += 1
        
        except Exception as e:
            print(f"  ✗ Error renaming {old_name}: {e}")
    
    return success_count


def move_to_images_folder(folder_path: str) -> int:
    """
    Create an 'images' folder and move all media files into it.
    Returns: number of files successfully moved
    """
    folder = Path(folder_path)
    images_folder = folder / "images"
    
    # Create images folder if it doesn't exist
    try:
        images_folder.mkdir(exist_ok=True)
        print(f"\n📁 Created folder: {images_folder}")
    except Exception as e:
        print(f"\n✗ Error creating images folder: {e}")
        return 0
    
    # Find all media files in the current folder
    media_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', 
                       '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
    
    moved_count = 0
    
    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in media_extensions:
            try:
                destination = images_folder / file.name
                shutil.move(str(file), str(destination))
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Error moving {file.name}: {e}")
    
    return moved_count


def create_readme_file(folder_path: str, prefix: str) -> bool:
    """
    Create a README.md file with the folder name.
    Returns: True if successful, False otherwise
    """
    folder = Path(folder_path)
    readme_name = f"{prefix.upper()}-README.md"
    readme_path = folder / readme_name
    
    try:
        # Create README with basic template
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# {prefix.upper()}\n\n")
            f.write(f"## Overview\n\n")
            f.write(f"\n\n## Screenshots\n\n")
            f.write(f"Images are located in the `images/` folder.\n")
        
        print(f"\n📝 Created README: {readme_name}")
        return True
    
    except Exception as e:
        print(f"\n✗ Error creating README file: {e}")
        return False


def main():
    """Main function."""
    print("\n" + "=" * 60)
    print("  AWS Practice File Renaming Tool")
    print("=" * 60)
    
    # Get folder path from user
    print("\nEnter the folder path (e.g., PRACTICE/EC2):")
    print("or press Ctrl+C to exit")
    
    try:
        folder_path = input("\nFolder path: ").strip()
    except KeyboardInterrupt:
        print("\n\nExited by user.")
        return
    
    if not folder_path:
        print("Error: No folder path provided.")
        return
    
    # Validate folder exists
    folder = Path(folder_path)
    if not folder.exists():
        print(f"\n✗ Error: Folder '{folder_path}' does not exist.")
        return
    
    if not folder.is_dir():
        print(f"\n✗ Error: '{folder_path}' is not a directory.")
        return
    
    # Extract folder name for prefix
    prefix = get_folder_name(folder_path)
    print(f"\nScanning folder: {folder_path}")
    print(f"File prefix: {prefix}")
    
    # Find media files
    images, videos = find_media_files(folder_path)
    
    if not images and not videos:
        print("\n✗ No media files found in this folder.")
        print("  Supported formats: PNG, JPG, JPEG, GIF, BMP (images)")
        print("                     MP4, AVI, MOV, MKV, WEBM, FLV (videos)")
        return
    
    print(f"\nFound {len(images)} image(s) and {len(videos)} video(s)")
    
    # Generate rename plan
    rename_plan = generate_rename_plan(folder_path, images, videos, prefix)
    
    # Display preview
    display_preview(rename_plan)
    
    if not rename_plan:
        return
    
    # Ask for confirmation
    print("\nProceed with renaming? (yes/no):")
    
    try:
        response = input("Your choice: ").strip().lower()
    except KeyboardInterrupt:
        print("\n\nExited by user.")
        return
    
    if response not in ['yes', 'y']:
        print("\nRenaming cancelled.")
        return
    
    # Execute renaming
    print("\nRenaming files...")
    success_count = execute_renaming(folder_path, rename_plan)
    
    print(f"\n✓ Successfully renamed {success_count} file(s)!")
    
    # Move files to images folder
    print("\nMoving files to 'images' folder...")
    moved_count = move_to_images_folder(folder_path)
    
    print(f"\n✓ Successfully moved {moved_count} file(s) to images folder!")
    
    # Create README file
    create_readme_file(folder_path, prefix)


if __name__ == "__main__":
    main()
