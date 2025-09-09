import os
import shutil
import sys

def process_directory(directory):
  img_dir = os.path.join(directory, 'img')

  # Check if img directory exists
  if not os.path.exists(img_dir):
    os.makedirs(img_dir)
  else:
    # Check if img directory is empty
    if os.listdir(img_dir):
      existing_files_path = os.path.join(img_dir, 'PRE_EXISTING_FILES.txt')
      with open(existing_files_path, 'w') as f:
        for file_name in os.listdir(img_dir):
          if file_name != 'PRE_EXISTING_FILES.txt':
            f.write(file_name + '\n')

  # Copy files from subtopics to img directory
  topics_dir = os.path.join(directory, 'topics')
  if os.path.exists(topics_dir):
    for subtopic in os.listdir(topics_dir):
      subtopic_img_dir = os.path.join(topics_dir, subtopic, 'img')
      if os.path.exists(subtopic_img_dir):
        for file_name in os.listdir(subtopic_img_dir):
          src_file = os.path.join(subtopic_img_dir, file_name)
          dst_file = os.path.join(img_dir, file_name)
          try:
            shutil.copy(src_file, dst_file)
            print(f"Copied {file_name} to top-level img directory.")
          except shutil.SameFileError:
            print(f"Skipping {file_name} as it already exists in {directory}/img directory.")
          except Exception as e:
            print(f"An error occurred while copying {file_name}: {str(e)}")

if __name__ == "__main__":
  directories = sys.argv[1:]
  for directory in directories:
    process_directory(directory)
