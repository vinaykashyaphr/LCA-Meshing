#include <iostream>
#include <vtkSmartPointer.h>
#include <vtkXMLPolyDataReader.h>
#include <vtkXMLPolyDataWriter.h>
#include <vtkPLYWriter.h>
#include <vtkPolyData.h>
#include <vtkPointData.h>
#include <vtkDataArray.h>
#include <vtkTubeFilter.h>
#include <vtkTriangleFilter.h>
#include <vtkCleanPolyData.h>



int main() {
    const char* inputFile  = "LCA_Centerline.vtp";
    const char* outputVTP  = "LCA_SurfaceMesh.vtp";
    const char* outputPLY  = "LCA_SurfaceMesh.ply";

    // --- Reading centerline ---
    auto reader = vtkSmartPointer<vtkXMLPolyDataReader>::New();
    reader->SetFileName(inputFile);
    reader->Update();

    vtkPolyData* cl = reader->GetOutput();
    if (!cl || cl->GetNumberOfPoints() == 0) {
        std::cerr << "Error: could not read " << inputFile << "\n";
        return 1;
    }

    if (!cl->GetPointData()->GetArray("Radius")) {
        std::cerr << "Error: 'Radius' array not found in centerline\n";
        return 1;
    }

    // Radius: the active scalar so TubeFilter picks it up
    cl->GetPointData()->SetActiveScalars("Radius");

    // Building tube surface using per-point radius
    auto tube = vtkSmartPointer<vtkTubeFilter>::New();
    tube->SetInputData(cl);
    tube->SetNumberOfSides(24);

    // multiplied by scalar
    tube->SetRadius(1.0);
    tube->SetVaryRadiusToVaryRadiusByScalar();
    tube->CappingOff();
    tube->Update();

    // Triangulating (required for STL)
    auto tri = vtkSmartPointer<vtkTriangleFilter>::New();
    tri->SetInputConnection(tube->GetOutputPort());
    tri->Update();

    // Merging duplicate points from tube seams
    auto clean = vtkSmartPointer<vtkCleanPolyData>::New();
    clean->SetInputConnection(tri->GetOutputPort());
    clean->Update();

    // Writing VTP
    auto vtpWriter = vtkSmartPointer<vtkXMLPolyDataWriter>::New();
    vtpWriter->SetFileName(outputVTP);
    vtpWriter->SetInputConnection(clean->GetOutputPort());
    vtpWriter->Write();
    std::cout << "Wrote " << outputVTP << "\n";

    // Writing PLY
    auto plyWriter = vtkSmartPointer<vtkPLYWriter>::New();
    plyWriter->SetFileName(outputPLY);
    plyWriter->SetInputConnection(clean->GetOutputPort());
    plyWriter->SetFileTypeToBinary();
    plyWriter->Write();
    std::cout << "Wrote " << outputPLY << "\n";

    return 0;
}
