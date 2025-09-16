import os
import sys

def delete_files(directory):
  pre_existing_files_path = os.path.join(directory, 'img', 'PRE_EXISTING_FILES.txt')
  img_directory = os.path.join(directory, 'img')

  if os.path.exists(pre_existing_files_path):
    with open(pre_existing_files_path, 'r') as file:
      pre_existing_files = file.read().splitlines()
  else:
    pre_existing_files = []

  for filename in os.listdir(img_directory):
    file_path = os.path.join(img_directory, filename)
    if os.path.isfile(file_path) and filename not in pre_existing_files:
      os.remove(file_path)
      print(f"Deleted {file_path}")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Please provide one or more directory names as input.")
    sys.exit(1)

  for directory in sys.argv[1:]:
    print(f"Post script running in {os.getcwd()}")
    if os.path.isdir(directory):
      delete_files(directory)
    else:
      print(f"{directory} is not a valid directory.")
