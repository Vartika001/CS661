from vtk import *

reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

## Query the no of dimensions of the dataset
#######################################
dimCells = data.GetDimensions()

# Taking the input of the isovale you want to query 
isovalue = None
while isovalue is None or not (-1438 < isovalue < 630):
    try:
        isovalue = float(input("Enter an isovalue between -1438 and 630: "))
        if not (-1438 <= isovalue <= 630):
            print("Error: Isovalue out of range. Please enter a valid isovalue.")
    except ValueError:
        print("Error: Please enter a valid numeric isovalue.")


# Helper fuction to find out the point location of interpolation
def point(p1,p2,isovalue):
    return (isovalue-p1)/(p2-p1)


# Helper function to insert the point to be connected in a cell
def helper(arr,press,i,j):
    lst=[]
    count=0
    if(arr[0]^arr[1]):
        lst.append((i+point(press[0],press[1],isovalue),j,25))
    if(arr[1]^arr[2]):
        lst.append((i+1,j+point(press[1],press[2],isovalue),25))
    if(arr[2]^arr[3]):
        lst.append((i+1-point(press[2],press[3],isovalue),j+1,25))
    if(arr[3]^arr[0]):
        lst.append((i,j+1-point(press[3],press[0],isovalue),25))
    return lst
        

## main code to perform all the things 
points = vtkPoints()
cellarr = vtkCellArray()
sumofpressure=0
totalcount=0
i=0
j=0
arr = []
while(i<dimCells[0]-1):
    while(j<dimCells[1]-1):
        press=[]
        arr=[]
        val1 = data.GetScalarComponentAsDouble(i,j,25,0)
        if(val1>=isovalue):
            arr.append(1)
        else:
            arr.append(0)
        val2 = data.GetScalarComponentAsDouble(i+1,j,25,0)
        if(val2>=isovalue):
            arr.append(1)
        else:
            arr.append(0)
        val3 = data.GetScalarComponentAsDouble(i+1,j+1,25,0)
        if(val3>=isovalue):
            arr.append(1)
        else:
            arr.append(0)
        val4 = data.GetScalarComponentAsDouble(i,j+1,25,0)
        if(val4>=isovalue):
            arr.append(1)
        else:
            arr.append(0)
        press.append(val1)
        press.append(val2)
        press.append(val3)
        press.append(val4)
        
        lt= helper(arr,press,i,j)
        if len(lt)>=2:
            points.InsertNextPoint(lt[0])
            points.InsertNextPoint(lt[1])
        line = vtkLine()
        line.GetPointIds().SetId(0, points.GetNumberOfPoints()-2)
        line.GetPointIds().SetId(1, points.GetNumberOfPoints()-1)

        cellarr.InsertNextCell(line)
        j+=1
    j=1    
    i+=1

obj = vtkPolyData()
obj.SetPoints(points)
obj.SetLines(cellarr)


writer = vtkXMLPolyDataWriter()
writer.SetInputData(obj)
writer.SetFileName("isocontour"+str(isovalue)+".vtp")
writer.Write()