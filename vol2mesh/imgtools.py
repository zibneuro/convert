import vtk

def set_image_border(image, value):
  """Sets the border pixels of 'image' to 0. The method assumes that image is 3D. If it is 1D or 2D whole image will be set to 0."""
  if not isinstance(image, vtk.vtkImageData):
    raise TypeError("the input has to be of type vtkImageData")

  if image.GetNumberOfScalarComponents() != 1:
    raise ValueError("the input image data should have 1 scalar component")

  extent = image.GetExtent()

  # There are six planes that we have to set to 0
  # xy plane
  for x in range(extent[0], extent[1] + 1):
    for y in range(extent[2], extent[3] + 1):
      image.SetScalarComponentFromFloat(x, y, extent[4], 0, value)
      image.SetScalarComponentFromFloat(x, y, extent[5], 0, value)
  # xz plane
  for x in range(extent[0], extent[1] + 1):
    for z in range(extent[4], extent[5] + 1):
      image.SetScalarComponentFromFloat(x, extent[2], z, 0, value)
      image.SetScalarComponentFromFloat(x, extent[3], z, 0, value)
  # yz plane
  for y in range(extent[2], extent[3] + 1):
    for z in range(extent[4], extent[5] + 1):
      image.SetScalarComponentFromFloat(extent[0], y, z, 0, value)
      image.SetScalarComponentFromFloat(extent[1], y, z, 0, value)
