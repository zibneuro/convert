import sys
import os
import vtk
from obj import OBJReader

# Make sure we have enough arguments passed by the user
if len(sys.argv) < 3:
  print("usage:\npython main.py <input folder> <output folder>")
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

print("\nthe .ply meshes will be saved in " + output_folder_name)

# The IO objects
obj_reader = OBJReader()
ply_writer = vtk.vtkPLYWriter()
ply_writer.SetFileTypeToBinary()

# First of all, we collect the names of the OBJ files
obj_file_names = list()

# Get the file names of the OBJ meshes in the provided folder
for file_name in os.listdir(input_folder_name):
  full_file_name = os.path.join(input_folder_name, file_name)
  # We want files only
  if not os.path.isfile(full_file_name):
    continue
  # Get the file extension (in lower case)
  file_ext = os.path.splitext(file_name)[1].lower()
  # We want OBJ files only
  if file_ext != ".obj":
    continue
  # We want that name
  obj_file_names.append(file_name)

# Some stuff for the processing
current_mesh_index = 1
num_saved_files = 0
error_messages = list()

# Loop over all meshes in the input folder and save them in PLY format
for file_name in obj_file_names:
  full_file_name = os.path.join(input_folder_name, file_name)
  base_file_name, file_ext = os.path.splitext(file_name)

  print("\n" + full_file_name + " (" + str(current_mesh_index) + " out of " + str(len(obj_file_names)) + ")")
  current_mesh_index += 1

  print("  reading OBJ ...")
  obj_reader.SetFileName(full_file_name)
  vtk_mesh = obj_reader.GetOutput()
  
  if vtk_mesh.GetNumberOfPoints() <= 0:
    error_messages.append("could not read " + full_file_name)
    continue

  # Construct the PLY output name
  mesh_output_name = os.path.join(output_folder_name, base_file_name) + ".ply"

  print("  writing PLY ...")
  ply_writer.SetInputData(vtk_mesh)
  ply_writer.SetFileName(mesh_output_name)
  ply_writer.Write()

  if os.path.isfile(mesh_output_name):
    num_saved_files += 1
    print("  saved " + mesh_output_name)
  else:
    error_messages.append("could not save " + mesh_output_name)

print("\nsaved " + str(num_saved_files) + " mesh file(s)")
print(str(len(error_messages)) + " error(s)")
for error in error_messages:
  print("  " + error)
print("")
