import Rhino
import rhinoscriptsyntax as rs

surface = rs.GetObject("select")
print(1, surface)
if surface:
    moments1 = rs.SurfaceAreaMoments(surface)
    print(2, moments1)
    if moments1:
        area_moments = moments1[6]  
        print(3, area_moments)
        rs.AddPoint(area_moments)
    geom = rs.coercegeometry(surface)
    amp = Rhino.Geometry.AreaMassProperties.Compute(geom)
    
    if amp:
        inertia = amp.CentroidCoordinatesPrincipalMomentsOfInertia()
        print(inertia)