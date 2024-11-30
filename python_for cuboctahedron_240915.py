import rhinoscriptsyntax as rs

rs.DefaultRenderer(False)

def square(w, l, offset, pt_cord, next_cord): #3
    rs.DefaultRenderer(False)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]

    if offset[0] == 0:
        pt0 = rs.AddPoint((a, b , c + offset[2] * 2 * w/l))
        pt1 = rs.AddPoint((a, b + offset[1] * 0.2, c + offset[2] * 2 * w/l))
        pt1a = rs.AddPoint((a, b + offset[1] * 0.2, c + offset[2]* (1-2 * w/l))) 
        pt2 = rs.AddPoint((a, b + offset[1] * 0.8 , c + offset[2]* (1-2 * w/l)))
        pt2a = rs.AddPoint((a, b + offset[1] * 0.8 , c + offset[2]* 2 * w/l))
        npt = rs.AddPoint((next_cord[0], next_cord[1], c + offset[2]* (1-2 * w/l)))
        ptb = rs.AddPoint((a, b, next_cord[2]))
        nptb = rs.AddPoint((next_cord[0], next_cord[1], c))
        
    elif offset[1] == 0:
        pt0 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c))
        pt1 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c + offset[2] * 0.2))
        pt1a = rs.AddPoint((a + offset[0] * (1-2 * w/l), b, c + offset[2] * 0.2))
        pt2 = rs.AddPoint((a + offset[0] * (1-2 * w/l), b, c + offset[2] * 0.8))
        pt2a = rs.AddPoint((a + offset[0] * 2 * w/l, b, c + offset[2] * 0.8))
        npt = rs.AddPoint((a + offset[0]* (1-2 * w/l), next_cord[1], next_cord[2]))
        ptb = rs.AddPoint((next_cord[0], b, c))
        nptb = rs.AddPoint((a, next_cord[1], next_cord[2]))

    elif offset[2] == 0:
        pt0 = rs.AddPoint((a, b + offset[1] * 2 * w/l, c))
        pt1 = rs.AddPoint((a + offset[0] * 0.2, b + offset[1] * 2 * w/l, c))
        pt1a = rs.AddPoint((a + offset[0] * 0.2, b + offset[1] * (1-2 * w/l), c))
        pt2 = rs.AddPoint((a + offset[0] * 0.8, b + offset[1] * (1-2 * w/l), c))
        pt2a = rs.AddPoint((a + offset[0] * 0.8, b + offset[1] * 2 * w/l, c))
        npt = rs.AddPoint((next_cord[0], b + offset[1] * (1-2 * w/l), next_cord[2]))
        ptb = rs.AddPoint((a, next_cord[1], c))
        nptb = rs.AddPoint((next_cord[0], b, next_cord[2]))

    rect = [pt1, pt1a, pt2, pt2a, pt1]
    big_rect = [pt_cord, ptb, next_cord, nptb, pt_cord]
#    poly_points = [pt0, pt1, pt1a, pt2, pt2a, npt]
    rs.HideObjects(rect)
    rs.HideObjects([ptb, nptb])
#    polyline = rs.AddPolyline(rect)
    polyline1 = rs.AddPolyline(big_rect)
    
    polyline2 = rs.AddPolyline([pt0, pt1, pt2, npt])
#    rs.AddSweep2(big_rect, big_rect, False )
    return [polyline1, polyline2]
    
def diagonal(w, l, offset, pt_cord, next_cord): #0
    rs.DefaultRenderer(False)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]
    
    if offset[0] == 0:
        pt0 = rs.AddPoint((a, b , c + offset[2] * 2 * w/l))
        pt1 = rs.AddPoint((a, b + offset[1] * 0.1, c + offset[2] * 2 * w/l))
        pt2 = rs.AddPoint((a, b + offset[1] * 0.9, c + offset[2] * (1-2 * w/l)))
        npt = rs.AddPoint((next_cord[0], next_cord[1], c + offset[2] * (1-2 * w/l)))

    elif offset[1] == 0:
        pt0 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c))
        pt1 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c + offset[2] * 0.1))
        pt2 = rs.AddPoint((a + offset[0] *(1-2 * w/l), b, c + offset[2] * 0.9))
        npt = rs.AddPoint((a + offset[0] *(1-2 * w/l), next_cord[1], next_cord[2]))

    elif offset[2] == 0:
        pt0 = rs.AddPoint((a, b + offset[1] * 2 * w/l, c))
        pt1 = rs.AddPoint((a + offset[0] * 0.1, b + offset[1] * 2 * w/l, c))
        pt2 = rs.AddPoint((a + offset[0] * 0.9, b + offset[1]  * (1-2 * w/l), c))
        npt = rs.AddPoint((next_cord[0], b + offset[1] * (1-2*w/l), next_cord[2]))


    poly_points = [pt0, pt1, pt2, npt]
    rs.HideObjects(poly_points)
    polyline = rs.AddPolyline(poly_points)
    return polyline
    
    
def triangle_shape(w, l, offset, pt_cord, next_cord): #2
    rs.DefaultRenderer(False)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]
        
    if offset[0] == 0:
        pt0 = rs.AddPoint((a, b , c + offset[2] * 2 * w/l))
        pt1 = rs.AddPoint((a, b + offset[1] * 0.5, c + offset[2] * 2 * w/l))
        pt2 = rs.AddPoint((a, b + offset[1] * 0.95 , c + offset[2]* (1-2 * w/l)))
        npt = rs.AddPoint((next_cord[0], next_cord[1], c + offset[2]* (1-2 * w/l)))
        
    elif offset[1] == 0:
        pt0 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c))
        pt1 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c + offset[2] * 0.5))
        pt2 = rs.AddPoint((a + offset[0] * (1-2 * w/l), b, c + offset[2] * 0.95))
        npt = rs.AddPoint((a + offset[0]* (1-2 * w/l), next_cord[1], next_cord[2]))

    elif offset[2] == 0:
        pt0 = rs.AddPoint((a, b + offset[1] * 2 * w/l, c))
        pt1 = rs.AddPoint((a + offset[0] * 0.5, b + offset[1] * 2 * w/l, c))
        pt2 = rs.AddPoint((a + offset[0] * 0.95, b + offset[1] * (1-2 * w/l), c))
        npt = rs.AddPoint((next_cord[0], b + offset[1] * (1-2 * w/l), next_cord[2]))

    poly_points = [pt0, pt1, pt2, npt]
    rs.HideObjects(poly_points)
    polyline = rs.AddPolyline(poly_points)
    return polyline
    
def z_shape(w, l, offset, pt_cord, next_cord): #1
    rs.DefaultRenderer(False)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]
    
    if offset[0] == 0:
        pt0 = rs.AddPoint((a, b , c + offset[2] * 2 * w/l))
        pt1 = rs.AddPoint((a, b + offset[1] * 0.5, c + offset[2] * 2 * w/l))
        pt2 = rs.AddPoint((a, b + offset[1] * 0.5, c + offset[2] * (1-2 * w/l)))
        npt = rs.AddPoint((next_cord[0], next_cord[1], c + offset[2] * (1-2 * w/l)))

    elif offset[1] == 0:
        pt0 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c))
        pt1 = rs.AddPoint((a + offset[0] * 2 * w/l, b, c + offset[2] * 0.5))
        pt2 = rs.AddPoint((a + offset[0] * (1-2 * w/l), b, c + offset[2] * 0.5))
        npt = rs.AddPoint((a + offset[0] * (1-2 * w/l), next_cord[1], next_cord[2]))

    elif offset[2] == 0:
        pt0 = rs.AddPoint((a, b + offset[1] * 2 * w/l, c))
        pt1 = rs.AddPoint((a + offset[0] * 0.5, b + offset[1] * 2 * w/l, c))
        pt2 = rs.AddPoint((a + offset[0] * 0.5, b + offset[1] * (1-2 * w/l), c))
        npt = rs.AddPoint((next_cord[0], b + offset[1] * (1-2 * w/l), next_cord[2]))

    poly_points = [pt0, pt1, pt2, npt]
    rs.HideObjects(poly_points)
    polyline = rs.AddPolyline(poly_points)
    return polyline

def surface(w, l, offset, pt_cord, next_cord): #4
    rs.DefaultRenderer(False)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]

    if offset[0] == 0:
        pt0 = rs.AddPoint((a, b, c + offset[2] * 4 * w/l))
        pt1 = rs.AddPoint((a, b + offset[1] * 4 * w/l, c + offset[2] * 4 * w/l))
        pt2 = rs.AddPoint((a, b + offset[1] * 4 * w/l, c))
        
        pt3 = rs.AddPoint((a, b + offset[1], c + offset[2] * (1-4 * w/l)))
        pt4 = rs.AddPoint((a, b + offset[1] * (1-4 * w/l), c + offset[2] * (1-4 * w/l)))
        pt5 = rs.AddPoint((a, b + offset[1] * (1-4 * w/l), c + offset[2]))
        
        ptb = rs.AddPoint((a, b, next_cord[2]))
        nptb = rs.AddPoint((next_cord[0], next_cord[1], c))
        
    elif offset[1] == 0:
        pt0 = rs.AddPoint((a + offset[0] * 4 * w/l, b, c))
        pt1 = rs.AddPoint((a + offset[0] * 4 * w/l, b, c + offset[2] * 4 * w/l))
        pt2 = rs.AddPoint((a, b, c + offset[2] * 4 * w/l))
        
        pt3 = rs.AddPoint((a + offset[0] * (1-4 * w/l), b, c + offset[2]))
        pt4 = rs.AddPoint((a + offset[0] * (1-4 * w/l), b, c + offset[2] * (1-4 * w/l)))
        pt5 = rs.AddPoint((a + offset[0], b, c + offset[2] * (1-4 * w/l)))
        
        ptb = rs.AddPoint((next_cord[0], b, c))
        nptb = rs.AddPoint((a, next_cord[1], next_cord[2]))

    elif offset[2] == 0:
        pt0 = rs.AddPoint((a, b + offset[1] * 4 * w/l, c))
        pt1 = rs.AddPoint((a + offset[0] * 4 * w/l, b + offset[1] * 4 * w/l, c))
        pt2 = rs.AddPoint((a + offset[0] * 4 * w/l, b, c))
        
        pt3 = rs.AddPoint((a + offset[0], b + offset[1] * (1-4 * w/l), c))
        pt4 = rs.AddPoint((a + offset[0] * (1-4 * w/l), b + offset[1] * (1-4 * w/l), c))
        pt5 = rs.AddPoint((a + offset[0] * (1-4 * w/l), b + offset[1], c))

        ptb = rs.AddPoint((a, next_cord[1], c))
        nptb = rs.AddPoint((next_cord[0], b, next_cord[2]))

    big_rect = [pt_cord, ptb, next_cord, nptb, pt_cord]
    small_rect1 = [pt_cord, pt0, pt1, pt2, pt_cord]
    small_rect2 = [next_cord, pt3, pt4, pt5, next_cord]
    square1 = rs.AddPolyline(big_rect)
    point = rs.CurveAreaCentroid(square1)
    
    square2 = rs.ScaleObject(square1, point[0], [0.8, 0.8, 0.8])
    square3 = rs.AddPolyline(small_rect1)
    square4 = rs.AddPolyline(small_rect2)

    rs.HideObjects([square1, square2, square3, square4])
    assemble = rs.CurveBooleanUnion([square2, square3, square4])
    rs.AddPlanarSrf(assemble)
    return assemble, square1
    
def cuboctahedron(pt, rotation, mode, number, container):
    rs.DefaultRenderer(False)
    if rotation >= number:
        return
    len = 30
    width = 1
    
    
    pt_cord = rs.PointCoordinates(pt)
    container.append(pt_cord)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]

    x = len/2
    
    offsets = [
            (x, x, 0), (x, -x, 0), (-x, x, 0), (-x, -x, 0),  # p_xy plane
            (0, x, x), (0, x, -x), (0, -x, x), (0, -x, -x),  # p_yz plane
            (x, 0, x), (-x, 0, x), (x, 0, -x), (-x, 0, -x)   # p_zx plane
    ]
            
    for offset in offsets:
        next_pt = rs.AddPoint((a + offset[0], b + offset[1], c + offset[2]))
        rs.HideObjects([pt, next_pt])
        next_cord = rs.PointCoordinates(next_pt)
#        rs.HideObjects(next_pt)
        if next_cord not in container:
            if mode in [0, 1, 2]:
                if mode == 0:
                     polyline = diagonal(width, len, offset, pt_cord, next_cord)
        
                elif mode == 1:
                     polyline = z_shape(width, len, offset, pt_cord, next_cord)

                elif mode == 2:
                     polyline = triangle_shape(width, len, offset, pt_cord, next_cord)

                rs.HideObjects(polyline)
                #offset
                if offset[0] == 0:
                    pl1 = rs.OffsetCurve(polyline, pt_cord, width, [1, 0, 0])
                    pl2 = rs.OffsetCurve(polyline, pt_cord, -width, [1, 0, 0])
                if offset[1] == 0:
                    pl1 = rs.OffsetCurve(polyline, pt_cord, width, [0, 1, 0])
                    pl2 = rs.OffsetCurve(polyline, pt_cord, -width, [0, 1, 0])
                if offset[2] == 0:
                    pl1 = rs.OffsetCurve(polyline, pt_cord, width, [0, 0, 1])
                    pl2 = rs.OffsetCurve(polyline, pt_cord, -width, [0, 0, 1])
                shape1 = rs.AddLine(rs.CurveStartPoint(pl1), rs.CurveStartPoint(pl2))
                shape2 = rs.AddLine(rs.CurveEndPoint(pl1), rs.CurveEndPoint(pl2))
#                rs.AddSweep1(shape1, [pl1, pl2], True)
    
            else:
                 if mode == 3:
                    polylines = square(width, len, offset, pt_cord, next_cord)
                 
                 elif mode == 4:
                    polylines = surface(width, len, offset, pt_cord, next_cord)
                    rs.ScaleObject(polylines[1], rs.CurveAreaCentroid(polylines[1])[0], [0.3, 0.3, 0.3])
                                  
            cuboctahedron(next_pt, rotation + 1, mode, number, container)
#        rs.AddTextDot(rotation, rs.PointCoordinates(next_pt))

center_pt = rs.AddPoint( (0, 0, 0) )
container = []
cuboctahedron(center_pt, 0, 4, 1, container)


