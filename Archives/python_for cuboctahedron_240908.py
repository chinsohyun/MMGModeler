import rhinoscriptsyntax as rs

rs.DefaultRenderer(False)

def diagonal(w, l, offset, pt_cord, next_cord):
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
    
#    lines = []
#    line_id = rs.AddLine(pt1, pt2)
#    lines.append(line_id)
#    return lines
    
def triangle_shape(w, l, offset, pt_cord, next_cord):
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
        npt = rs.AddPoint((a + offset[2]* (1-2 * w/l), next_cord[1], next_cord[2]))

    elif offset[2] == 0:
        pt0 = rs.AddPoint((a, b + offset[1] * 2 * w/l, c))
        pt1 = rs.AddPoint((a + offset[0] * 0.5, b + offset[1] * 2 * w/l, c))
        pt2 = rs.AddPoint((a + offset[0] * 0.95, b + offset[1] * (1-2 * w/l), c))
        npt = rs.AddPoint((next_cord[0], b + offset[1] * (1-2 * w/l), next_cord[2]))

    poly_points = [pt0, pt1, pt2, npt]
    rs.HideObjects(poly_points)
    polyline = rs.AddPolyline(poly_points)
    return polyline
    
def z_shape(w, l, offset, pt_cord, next_cord):
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
        next_cord = rs.PointCoordinates(next_pt)
#        rs.HideObjects(next_pt)
        if next_cord not in container:
            if mode == 0:
                 polyline = diagonal(width, len, offset, pt_cord, next_cord)
    
            elif mode == 1:
                 polyline = z_shape(width, len, offset, pt_cord, next_cord)
                 
    
            elif mode == 2:
                 polyline = triangle_shape(width, len, offset, pt_cord, next_cord)
            rs.HideObjects(polyline)
            
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
            rs.AddSweep1(shape1, [pl1, pl2], True)
            cuboctahedron(next_pt, rotation + 1, mode, number, container)
#        rs.AddTextDot(rotation, rs.PointCoordinates(next_pt))

    

center_pt = rs.AddPoint( (0, 0, 0) )
container = []
cuboctahedron(center_pt, 0, 0, 2, container)


