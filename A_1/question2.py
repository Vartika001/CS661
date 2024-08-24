import vtk
from vtk import *

# Reading the data

reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')
reader.Update()
data = reader.GetOutput()

volume = vtk.vtkVolume()

# Create a vtkVolumeProperty object
volumeProperty = vtk.vtkVolumeProperty()

# Set the transfer functions for color and opacity
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-4931.54, 0, 1, 1)   # blue
colorFunc.AddRGBPoint(-2508.95, 0, 0, 1)   # yellow
colorFunc.AddRGBPoint(-1873.9 , 0, 0, 0.5)  
colorFunc.AddRGBPoint(-1027.16 , 1, 0, 0)  
colorFunc.AddRGBPoint(-298.031  , 1, 0.4, 0)  
colorFunc.AddRGBPoint(2594.97  , 1, 1, 0)  
volumeProperty.SetColor(colorFunc)

opacityFunc = vtk.vtkPiecewiseFunction()
opacityFunc.AddPoint(-4931.54, 1.0)   # fully transparent
opacityFunc.AddPoint(101.815, 0.002)   # partially opaque
opacityFunc.AddPoint(2594.97, 0.0)   # fully opaque
volumeProperty.SetScalarOpacity(opacityFunc)

#setting up mapper

mapper = vtkSmartVolumeMapper()
mapper.SetInputData(data)

volumeproperties = vtkVolumeProperty()
volumeproperties.SetColor(colorFunc )
volumeproperties.SetScalarOpacity(opacityFunc)

volume = vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(volumeproperties)

#setting the outline functions
outlineFilter = vtk.vtkOutlineFilter()
outlineFilter.SetInputData(volume.GetMapper().GetInput())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineFilter.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

usePhongShading = input("Enter Y/y if you want to use Phong shading :").lower()

if usePhongShading == "y":
    # Create a phong shading function and set it to the volume property
    volumeProperty = volume.GetProperty()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.5)
    volumeProperty.SetDiffuse(0.5)
    volumeProperty.SetSpecular(0.5)
    volumeProperty.SetSpecularPower(10)
    volume.SetProperty(volumeProperty)


renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.AddActor(outlineActor)
# Set up the render window and interactor
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(1000, 1000)
renderWindow.AddRenderer(renderer)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)
interactor.Initialize()
interactor.Start()