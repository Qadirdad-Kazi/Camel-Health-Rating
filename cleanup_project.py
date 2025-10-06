#!/usr/bin/env python3
"""
Project cleanup script to remove unnecessary files and folders
"""

import os
import shutil
import subprocess
from pathlib import Path

def get_folder_size(path):
    """Get folder size in MB"""
    try:
        result = subprocess.run(['du', '-sm', path], capture_output=True, text=True)
        if result.returncode == 0:
            return int(result.stdout.split('\t')[0])
    except:
        pass
    return 0

def cleanup_python_cache():
    """Remove Python cache files"""
    print("🧹 Cleaning Python cache files...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"  ✅ Removed: {dir_path}")
                except Exception as e:
                    print(f"  ❌ Failed to remove {dir_path}: {e}")
    
    # Remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file_name in files:
            if file_name.endswith('.pyc'):
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"  ✅ Removed: {file_path}")
                except Exception as e:
                    print(f"  ❌ Failed to remove {file_path}: {e}")

def cleanup_system_files():
    """Remove system files"""
    print("🧹 Cleaning system files...")
    
    system_files = ['.DS_Store', 'Thumbs.db', 'desktop.ini']
    
    for root, dirs, files in os.walk('.'):
        for file_name in files:
            if file_name in system_files:
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"  ✅ Removed: {file_path}")
                except Exception as e:
                    print(f"  ❌ Failed to remove {file_path}: {e}")

def cleanup_logs():
    """Remove log files"""
    print("🧹 Cleaning log files...")
    
    log_extensions = ['.log', '.tmp', '.temp']
    
    for root, dirs, files in os.walk('.'):
        for file_name in files:
            if any(file_name.endswith(ext) for ext in log_extensions):
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"  ✅ Removed: {file_path}")
                except Exception as e:
                    print(f"  ❌ Failed to remove {file_path}: {e}")

def cleanup_old_venv():
    """Remove old virtual environment"""
    print("🧹 Cleaning old virtual environment...")
    
    venv_path = 'backend/venv_new'
    if os.path.exists(venv_path):
        size_before = get_folder_size(venv_path)
        try:
            shutil.rmtree(venv_path)
            print(f"  ✅ Removed old venv: {venv_path} ({size_before}MB)")
        except Exception as e:
            print(f"  ❌ Failed to remove {venv_path}: {e}")
    else:
        print(f"  ℹ️  {venv_path} not found")

def cleanup_test_files():
    """Remove test files that are not needed"""
    print("🧹 Cleaning test files...")
    
    test_files = [
        'backend/test_advanced_models.py',
        'backend/test_web_api.py', 
        'backend/test_pretrained_models.py',
        'backend/test_open_source_api.py',
        'backend/test_open_source.py',
        'backend/simple_test.py',
        'backend/quick_test.py',
        'backend/use_pretrained_models.py',
        'backend/open_source_alternatives.py',
        'backend/improve_model_accuracy.py',
        'backend/data_quality_improvement.py',
        'backend/advanced_training.py',
        'backend/run_improved_training.py',
        'backend/quick_accuracy_boost.py',
        'backend/install_pretrained_dependencies.py',
        'backend/install_advanced_models.py',
        'backend/test_image.jpg',
        'backend/test_images/',
        'backend/camel_rating_app.egg-info/'
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"  ✅ Removed directory: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"  ✅ Removed file: {file_path}")
            except Exception as e:
                print(f"  ❌ Failed to remove {file_path}: {e}")

def cleanup_uploads():
    """Clean up uploads directory"""
    print("🧹 Cleaning uploads directory...")
    
    uploads_path = 'backend/uploads'
    if os.path.exists(uploads_path):
        size_before = get_folder_size(uploads_path)
        try:
            # Remove all files in uploads but keep the directory
            for file_name in os.listdir(uploads_path):
                file_path = os.path.join(uploads_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"  ✅ Removed: {file_path}")
            print(f"  ✅ Cleaned uploads directory ({size_before}MB)")
        except Exception as e:
            print(f"  ❌ Failed to clean uploads: {e}")

def cleanup_documentation():
    """Remove redundant documentation files"""
    print("🧹 Cleaning documentation files...")
    
    doc_files = [
        'ACCURACY_IMPROVEMENT_GUIDE.md',
        'OPEN_SOURCE_ALTERNATIVES_GUIDE.md',
        'IMPLEMENTATION_SUMMARY.md',
        'HOW_TO_START_APP.md',
        'backend/TRAINING_README.md',
        'backend/TRAINING_SUMMARY.md',
        'backend/WEB_INTEGRATION_STATUS.md',
        'backend/README.md',
        'how to start.txt',
        'to start.rtxt'
    ]
    
    for file_path in doc_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"  ✅ Removed: {file_path}")
            except Exception as e:
                print(f"  ❌ Failed to remove {file_path}: {e}")

def cleanup_training_data():
    """Clean up training data if not needed"""
    print("🧹 Cleaning training data...")
    
    training_path = 'Training Data'
    if os.path.exists(training_path):
        size_before = get_folder_size(training_path)
        response = input(f"  Remove Training Data folder ({size_before}MB)? (y/n): ")
        if response.lower() == 'y':
            try:
                shutil.rmtree(training_path)
                print(f"  ✅ Removed: {training_path} ({size_before}MB)")
            except Exception as e:
                print(f"  ❌ Failed to remove {training_path}: {e}")
        else:
            print(f"  ℹ️  Keeping: {training_path}")

def show_space_saved():
    """Show space saved after cleanup"""
    print("\n📊 SPACE USAGE AFTER CLEANUP:")
    try:
        result = subprocess.run(['du', '-sh', '.'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Total project size: {result.stdout.strip()}")
    except:
        pass

def main():
    """Main cleanup function"""
    print("🚀 PROJECT CLEANUP SCRIPT")
    print("=" * 50)
    
    # Show initial space usage
    print("📊 INITIAL SPACE USAGE:")
    try:
        result = subprocess.run(['du', '-sh', '.'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Total project size: {result.stdout.strip()}")
    except:
        pass
    
    print("\n🧹 STARTING CLEANUP...")
    
    # Run cleanup functions
    cleanup_python_cache()
    cleanup_system_files()
    cleanup_logs()
    cleanup_old_venv()
    cleanup_test_files()
    cleanup_uploads()
    cleanup_documentation()
    cleanup_training_data()
    
    print("\n✅ CLEANUP COMPLETED!")
    show_space_saved()
    
    print("\n💡 KEPT ESSENTIAL FILES:")
    print("  ✅ Core application files")
    print("  ✅ Active virtual environment (backend/venv)")
    print("  ✅ Model files")
    print("  ✅ Docker configuration")
    print("  ✅ Main documentation (README.md)")
    print("  ✅ Production files")
    
    print("\n🎯 PROJECT IS NOW CLEAN AND OPTIMIZED!")

if __name__ == "__main__":
    main()
