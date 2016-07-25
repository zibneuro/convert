import subprocess
import sys
import os

def compute_output_mesh_size_in_percent(mesh_file_name):
  try:
    size_in_mb = os.path.getsize(mesh_file_name) / (1024.0 * 1024.0)
  except:
    return 100
  
  if size_in_mb > 3:
    return 25
  if size_in_mb > 1:
    return 50
  if size_in_mb > 0.5:
    return 75
  
  return 100


if len(sys.argv) < 3:
  print("usage:\npython main.py <input folder> <output folder>")
  exit()

# Some parameters
amira_cmd = "/local/software/AmiraZIBEdition-2016.20/bin/AmiraZIBEdition"
amira_script_template_file_name = "./amira_script_template.hx"
real_amira_script_file_name = "./real_amira_script.hx"
input_folder_name = sys.argv[1]
output_folder_name = sys.argv[2]

# The following strings in the Amira script template will be replaced with the real file names and parameter values
input_surface_full_file_name_place_holder = r"<INPUT_SURFACE_FILE_NAME>"
output_surface_full_file_name_place_holder = r"<OUTPUT_SURFACE_FILE_NAME>"
output_mesh_size_percent_place_holder = r"<OUTPUT_MESH_SIZE_PERCENT>"

# Check if the input directory exists
if not os.path.isdir(input_folder_name):
  print("Error: input directory '" + input_folder_name + "' does not exist")
  exit()

# Check if the output directory exists
if not os.path.isdir(output_folder_name):
  print("Error: output directory '" + output_folder_name + "' does not exist")
  exit()

# Load the script template
try:
  amira_script_template_file = open(amira_script_template_file_name)
  amira_script_template_content = amira_script_template_file.read()
  amira_script_template_file.close()
except Exception as e:
  print(e)
  exit()

# Print the arguments used in this script
print("\nusing the following amira: " + amira_cmd)
print("Amira script template: " + amira_script_template_file_name)
print("true Amira script (to be created with the real parameters): " + real_amira_script_file_name)
print("input mesh folder: " + input_folder_name)
print("meshes will be saved in: " + output_folder_name)

ply_file_names = list()

# Get the file names of the PLY meshes in the provided input folder
for file_name in os.listdir(input_folder_name):
  full_file_name = os.path.join(input_folder_name, file_name)
  
  # We want PLY files only
  if os.path.isfile(full_file_name) and os.path.splitext(file_name)[1].lower() == ".ply":
    ply_file_names.append(file_name)

# Indicates the current mesh which is being remeshed
current_mesh_number = 1

# Loop over all meshes in the input folder and remesh them
for file_name in ply_file_names:
  # Compose the input and output file names
  input_surface_full_file_name = os.path.join(input_folder_name, file_name)
  output_surface_full_file_name = os.path.join(output_folder_name, os.path.splitext(file_name)[0] + ".obj")

  print("\n" + str(current_mesh_number) + " out of " + str(len(ply_file_names)))
  print("input: " + input_surface_full_file_name)
  print("output: " + output_surface_full_file_name)
  current_mesh_number += 1

  # get the desired output mesh size
  output_mesh_size_percent = str(compute_output_mesh_size_in_percent(input_surface_full_file_name))
  print("output mesh size = " + output_mesh_size_percent + r"%")

  # Create the Amira script which contains the true file names
  real_amira_script_content = amira_script_template_content.replace(input_surface_full_file_name_place_holder, input_surface_full_file_name)
  real_amira_script_content = real_amira_script_content.replace(output_surface_full_file_name_place_holder, output_surface_full_file_name)
  real_amira_script_content = real_amira_script_content.replace(output_mesh_size_percent_place_holder, output_mesh_size_percent)

  # Save the script in a file
  try:
    real_amira_script_file = open(real_amira_script_file_name, "w")
    real_amira_script_file.write(real_amira_script_content)
    real_amira_script_file.close()
  except Exception as e:
    print(e)
    continue

  print("remeshing ...")
  
  # Call Amira with the created script
  try:
    subprocess.call([amira_cmd, real_amira_script_file_name])
  except Exception as e:
    print(e)
    exit()
    
  print("done")

# We do not need the real Amira script
try:
  os.remove(real_amira_script_file_name)
except Exception:
  pass

print("\nshould have saved " + str(len(ply_file_names)) + " mesh file(s) in " + output_folder_name)
