import sys
import os
import vtk
import imgtools

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

# Very important! The following values are for the virtual fish project
voxel_size = [0.798, 0.798, 2.0]
print("\nIMPORTANT: using the following voxel size: " + str(voxel_size[0]) + ", " + str(voxel_size[1]) + ", " + str(voxel_size[2]))
print("the meshes will be saved in " + output_folder_name)

# The VTK stuff
img_reader = vtk.vtkTIFFReader()
# Gaussian image filter
img_smoother = vtk.vtkImageGaussianSmooth()
img_smoother.SetDimensionality(3)
img_smoother.SetRadiusFactor(3)
# Marching cubes
marching_cubes = vtk.vtkImageMarchingCubes()
marching_cubes.SetValue(0, 128)
# Mesh writer
mesh_writer = vtk.vtkPLYWriter()

# First of all, we collect the names of the tiff files
tiff_file_names = list()

# Get the file names of the tif images in the provided folder
for file_name in os.listdir(input_folder_name):
  full_file_name = os.path.join(input_folder_name, file_name)
  
  # We want files only
  if not os.path.isfile(full_file_name):
    continue
  
  # Get the file extension (in lower case)
  file_ext = os.path.splitext(file_name)[1].lower()

  # We want TIF files only
  if file_ext != ".tif" and file_ext != ".tiff":
    continue

  tiff_file_names.append(file_name)

# Some stuff for the real processing
current_image_index = 1
num_saved_files = 0
error_messages = list()

# Loop over all tif images in the input folder and do the processing
for file_name in tiff_file_names:
  full_file_name = os.path.join(input_folder_name, file_name)
  base_file_name, file_ext = os.path.splitext(file_name)

  print("\n" + full_file_name + " (" + str(current_image_index) + " out of " + str(len(tiff_file_names)) + ")")
  current_image_index += 1
  
  print("  reading data ...")
  img_reader.SetFileName(full_file_name)
  # Can we read the data
  if img_reader.CanReadFile(full_file_name) != 3:
    error_messages.append("could not read " + full_file_name)
    continue
  # Read it
  img_reader.Update()

  print("  smoothing ...")
  img_smoother.SetInputData(img_reader.GetOutput())
  img_smoother.Update()
  smoothed_image = img_smoother.GetOutput()

  print("  setting border to 0 ...")
  imgtools.set_image_border(smoothed_image, 0)
  smoothed_image.SetSpacing(voxel_size[0], voxel_size[1], voxel_size[2])

  print("  marching ...")
  marching_cubes.SetInputData(smoothed_image)
  marching_cubes.Update()

  mesh_output_name = os.path.join(output_folder_name, base_file_name) + ".ply"

  print("  writing ...")
  mesh_writer.SetInputData(marching_cubes.GetOutput())
  mesh_writer.SetFileName(mesh_output_name)
  mesh_writer.Write()
  
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