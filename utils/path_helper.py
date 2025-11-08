# FINAL PROJECT FLASHCARD APP / utils / path_helper.py

import os

def get_project_root():
    """Get the absolute path to the project root directory"""
    # Get the directory where THIS file is located
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root
    return os.path.dirname(current_file_dir)

def get_asset_path(filename):
    """Get path to any asset file"""
    project_root = get_project_root()
    return os.path.join(project_root, "assets", filename)

def get_icon_path(icon_name):
    """Get path to an icon file"""
    return get_asset_path(icon_name)