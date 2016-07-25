import subprocess
import platform
import sys
import re
import os

def get_dimensions_in_string(string):
  """We assume that 'string' is of the form *IxJxK*, where I, J and K are the number of pixels along the
  x, y and z axis, respectively, and the * in front and at the back indicates arbitrary non-numerical
  characters. The method returns a triple."""
  rx = re.compile(r"[0-9]+x[0-9]+x[0-9]+")
  res = rx.findall(string)
  if len(res) <= 0:
    return 0, 0, 0

  # Get the dimensions as strings
  dims = res[0].split("x")
  if len(dims) <= 0:
    return 0, 0, 0

  return (dims[0], dims[1], dims[2])


# Make sure we have enough arguments passed by the user
if len(sys.argv) < 3:
  print("usage:\npython3 main.py <input folder> <output folder>")
  exit()

input_folder_name = sys.argv[1]
output_folder_name = sys.argv[2]

# Check if the input directory exists
if not os.path.isdir(input_folder_name):
  print("Error: input directory '" + input_folder_name + "' does not exist")
  exit()

# Check if the output directory exists
if not os.path.isdir(output_folder_name):
  print("Error: output directory '" + output_folder_name + "' does not exist")
  exit()

print("the TIFFs will be saved in " + output_folder_name)

# Check the OS to decide how to call the C++ app which does do real conversion
os_name = platform.system().lower()
# Determine the path to the C++ app depending on the OS
if os_name == "windows":
  raw2tif_app = "./c++/build/Release/raw2tif"
else:
  raw2tif_app = "./c++/build/raw2tif"

print("App for the raw-to-tiff conversion (powered by C++): " + raw2tif_app)

# First of all, we collect the names of the raw files
raw_file_names = list()

# Get the file names of the raw files in the provided folder
for file_name in os.listdir(input_folder_name):
  full_file_name = os.path.join(input_folder_name, file_name)

  # We want files only
  if not os.path.isfile(full_file_name):
    continue

  # Get the file extension (in lower case)
  file_ext = os.path.splitext(file_name)[1].lower()

  # We want .raw files only
  if file_ext != ".raw":
    continue

  raw_file_names.append(file_name)

# Some stuff for the real processing
current_image_index = 1
num_saved_files = 0
error_messages = list()

# Loop over all raw files in the input folder and do the conversion
for file_name in raw_file_names:
  full_file_name = os.path.join(input_folder_name, file_name)
  base_file_name, file_ext = os.path.splitext(file_name)

  print("\n" + str(current_image_index) + " of " + str(len(raw_file_names)))
  current_image_index += 1

  print("extracting the image dimensions from the file name ...")
  dims = get_dimensions_in_string(full_file_name)
  if dims == (0, 0, 0):
    error_messages.append("Couldn't get the dimensions from the string '" + full_file_name + "'")
    continue

  # Build the image name
  tiff_image_output_name = os.path.join(output_folder_name, base_file_name) + ".tiff"

  print("calling '" + raw2tif_app + "' to do the real job:")

  # Try to call the app to make sure it is there
  try:
    subprocess.call([raw2tif_app, dims[0], dims[1], dims[2], full_file_name, tiff_image_output_name])
  except Exception as e:
    print("Couldn't call '" + raw2tif_app + "': " + str(e))
    exit()

  # Check if the file is there
  if os.path.isfile(tiff_image_output_name):
    num_saved_files += 1
  else:
    error_messages.append("could not save " + tiff_image_output_name)

print("\nsaved " + str(num_saved_files) + " mesh file(s)")
print(str(len(error_messages)) + " error(s)")
for error in error_messages:
  print("  " + error)
print("")
