#include <vtkImageData.h>
#include <vtkTIFFWriter.h>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <vector>

using namespace std;

bool load_pixels(const char* input_file_name, size_t num_bytes_per_pixel, size_t num_pixels, void* pixels)
{
  FILE *file = fopen(input_file_name, "rb");
  if (!file)
  {
    cerr << "Error: couldn't open '" << input_file_name << "'\n";
    return false;
  }

  size_t num_bytes_to_read = num_bytes_per_pixel*num_pixels;
  
  // Copy the file content into the buffer
  size_t read_bytes = fread(pixels, 1, num_bytes_to_read, file);
  
  // We do not need the file any more
  fclose(file);

  // Did we manage to read the right number of bytes?
  if (read_bytes != num_bytes_to_read)
  {
    cerr << "Error: couldn't read all bytes from '" << input_file_name << "'\n";
    return false;
  }

  return true;
}

//===========================================================================================================

int main(int argc, char *argv[])
{
  if (argc < 5)
  {
    cout << "\nusage:\nraw2tif <num_pixels_x> <num_pixels_y> <num_pixels_z> <input_16bit_per_pixel.raw> <output.tiff>\n\n";
    return -1;
  }

  // Get the image size
  int dims[3] = {atoi(argv[1]), atoi(argv[2]), atoi(argv[3])};
  // Get the input file
  const char* input_file_name = argv[4];
  // Get the output file
  const char* output_file_name = argv[5];

  cout << "input  = " << input_file_name << endl;
  cout << "output = " << output_file_name << endl;
  cout << "dims   = [" << dims[0] << ", " << dims[1] << ", " << dims[2] << "]\n";

  // Create a VTK image
  vtkImageData* vtk_img = vtkImageData::New();
  vtk_img->SetExtent(0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1);
  vtk_img->AllocateScalars(VTK_UNSIGNED_SHORT, 1);

  // Load the pixels from the file to the VTK image
  cout << "copying pixels from file to image ... \n";
  bool success = load_pixels(input_file_name, /*bytes per pixel=*/2, dims[0]*dims[1]*dims[2],
    vtk_img->GetScalarPointer(0, 0, 0));

  if (!success)
  {
    cerr << "Error: couldn't load the pixels from '" << input_file_name << "'\n";
    vtk_img->Delete();
    return -1;
  }

  cout << "saving as tif ...\n";
  // Create a TIFF writer and save the image
  vtkTIFFWriter* tiff_writer = vtkTIFFWriter::New();
  tiff_writer->SetInputData(vtk_img);
  tiff_writer->SetFileName(output_file_name);
  tiff_writer->Write();
  
  // Clean up
  vtk_img->Delete();
  tiff_writer->Delete();

  cout << "done\n";
  
  return 0;
}
