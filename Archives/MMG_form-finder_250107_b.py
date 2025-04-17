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
    
    polyline = rs.AddPolyline(poly_points)
    rs.DeleteObjects(poly_points)
    return polyline

def surface(w, l, offset, pt_cord, next_cord): #4
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
    rs.HideObjects([pt0, pt1, pt2, pt3, pt4, pt5, nptb, ptb])
    square1 = rs.AddPolyline(big_rect)
    point = rs.CurveAreaCentroid(square1)
    
    square2 = rs.ScaleObject(square1, point[0], [0.8, 0.8, 0.8])
    square3 = rs.AddPolyline(small_rect1)
    square4 = rs.AddPolyline(small_rect2)

    rs.HideObjects([square1, square2, square3, square4])
    assemble = rs.CurveBooleanUnion([square2, square3, square4])
    
    return assemble

def cuboctahedron_symmetry(pt_cord, rotation, mode, number, container, boundary, ps_box, c_box):
    rs.DefaultRenderer(False)
    print(boundary)
    if rotation >= number:
        
        delete_list = []
        for i in range(len(c_box)):
            print("c_box", c_box)
            if not rs.IsPointInSurface(boundary, c_box[i]):
                delete_list.append(ps_box[i])
                rs.HideObjects(delete_list)

        return
    length = 30
    width = 1
    

    container.append(pt_cord)
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]

    x = length/2
    
    offsets = [
            (x, x, 0), (x, -x, 0), (-x, x, 0), (-x, -x, 0),  # p_xy plane
            (0, x, x), (0, x, -x), (0, -x, x), (0, -x, -x),  # p_yz plane
            (x, 0, x), (-x, 0, x), (x, 0, -x), (-x, 0, -x)   # p_zx plane
    ]
            
    for offset in offsets:
        next_pt = rs.AddPoint((a + offset[0], b + offset[1], c + offset[2]))
        rs.HideObject(next_pt)
        next_cord = rs.PointCoordinates(next_pt)

        if next_cord not in container:
            if mode in [0, 1, 2]:
                if mode == 0:
                     polyline = diagonal(width, length, offset, pt_cord, next_cord)
        
                elif mode == 1:
                     polyline = z_shape(width, length, offset, pt_cord, next_cord)

                elif mode == 2:
                     polyline = triangle_shape(width, length, offset, pt_cord, next_cord)

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
                ps = rs.AddPlanarSrf([shape1, pl1, shape2, pl2])
                rs.DeleteObjects([shape1, pl1, shape2, pl2])
            else:
                 if mode == 3:
                    polylines = square(width, length, offset, pt_cord, next_cord)
                 
                 elif mode == 4:
                    polylines = surface(width, length, offset, pt_cord, next_cord)
                    
                 ps = rs.AddPlanarSrf(polylines)
                 if type(polylines) == list:
                     rs.DeleteObjects(polylines)
                 else:
                    rs.DeleteObject(polylines)
            c_box.append(next_cord)
            ps_box.append(ps)
           
            cuboctahedron_symmetry(next_cord, rotation + 1, mode, number, container, brep, ps_box, c_box)

def cuboctahedron(pt_cord, rotation, mode, number, container):
    rs.DefaultRenderer(False)
    if rotation >= number:
        return
    len = 30
    width = 1
    

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
    
    next_pts = []
    for offset in offsets:
        next_pt = rs.AddPoint((a + offset[0], b + offset[1], c + offset[2]))
        next_pts.append(next_pt)
        next_cord = rs.PointCoordinates(next_pt)
        
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
                
                ps = rs.AddPlanarSrf([shape1, pl1, shape2, pl2])
            else:
                 if mode == 3:
                    polylines = square(width, len, offset, pt_cord, next_cord)
                 
                 elif mode == 4:
                    polylines = surface(width, len, offset, pt_cord, next_cord)
                    
                    rs.AddPlanarSrf(polylines)
    pick_pt = rs.GetPoint("Select the next point: ", (0, 0, 0))
    
    cuboctahedron(pick_pt, rotation + 1, mode, number, container)


def point_set(pt_cord, dim, thk):
    x = 2 * thk  + dim 
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]
    offset_cords = [
        (a + x, b + x, c), (a + x, b - x, c), (a - x, b + x, c), (a - x, b - x, c),  # p_xy plane
        (a, b + x, c + x), (a, b + x, c - x), (a, b - x, c + x), (a, b - x, c - x),  # p_yz plane
        (a + x, b, c + x), (a - x, b, c + x), (a + x, b, c - x), (a - x, b, c - x)   # p_zx plane
    ]
    return offset_cords

def draw_mode(thk, dim, pt_cord, next_cord):
    x = next_cord[0] - pt_cord[0]  # p_yz plane
    y = next_cord[1] - pt_cord[1]  # p_zx plane
    z = next_cord[2] - pt_cord[2]  # p_xy plane
    
    r2 = None
    dis = dim + thk * 2 
    direction = (0, 0, 0)
    direction = rs.VectorAdd(pt_cord, (0, 0, 0)) #add vector to the origin!
    if x == 0:# p_yz plane
        
        m = rs.XformIdentity()
        normal = (0, 1, 0)
        degree = 90
        if y > 0 and z < 0: #4
            m = rs.XformMirror(pt_cord, (0, 1, 0)) #normal vector is based on original point. weird. 
        if y < 0 and z > 0: #2
            direction = (-dis, -dis, 0)#sign opposite, why/?
            direction = rs.VectorAdd(pt_cord, (-dis, -dis, 0))
            m = rs.XformMirror(pt_cord, (0, 1, 0))
        if y < 0 and z < 0: #3
            direction = (-dis, -dis, 0)#sign opposite
            direction = rs.VectorAdd(pt_cord, (-dis, -dis, 0))
        r2 = rs.XformRotation2(90, ( 0, 0, 1 ), pt_cord)
        
    if y == 0: # p_zx plane
        m = rs.XformIdentity()
        normal = (1, 0, 0)
        degree = -90
        if z < 0 and x > 0: #4
            direction = rs.VectorAdd(pt_cord, (-dis, -dis, 0))
            m = rs.XformMirror(pt_cord, (0, 1, 0))
        if z > 0 and x < 0: #2
            m = rs.XformMirror(pt_cord, (0, 1, 0))
        if z < 0 and x < 0: #3
            direction = rs.VectorAdd(pt_cord, (-dis, -dis, 0))
        r2 = rs.XformRotation2(-90, ( 0, 0, 1 ) , pt_cord)
        
    if z == 0: # p_xy plane
        m = rs.XformIdentity()
        if y < 0 and x > 0:
            m = rs.XformMirror(pt_cord, (0, 1, 0))
        if y > 0 and x < 0:
            direction = rs.VectorAdd(pt_cord, (-dis, -dis, 0))
            m = rs.XformMirror(pt_cord, (0, 1, 0))
        if y < 0 and x < 0:
            direction = rs.VectorAdd(pt_cord, (-dis, -dis, 0))
    
    t = rs.XformTranslation(direction)
    s = rs.XformScale( (dim, dim, dim) )

    if r2:
        r1 = rs.XformRotation2(degree, normal, pt_cord)
        xform = r1 * r2 * m * t * s
    else:
        xform = m * t * s
    ps = rs.InsertBlock2("sample", xform)

    return ps


def element_mode(pt_cord, rotation, mode, threshold, container, three_set):

    if rotation >= threshold:
        return
    print(container)
    dim = 15  #real size
#    width = 1 #need further modification
    thk = 0.56 + 0.53
    offset_cords = point_set(pt_cord, dim, thk)
    
    #start_points
    temp_circle = []

    #next_points
    next_points = []
    
    if rotation %3 == 0: #need further modification
        print("initial round")
        start_points= []
        for start_cord in container:
            start_points.append(rs.AddPoint(start_cord))
            temp_circle.append(rs.AddCircle(start_cord, 2))
            
        #pt_cord updated
        pt_cord = rs.GetPoint("Select a new center: ") #, container[-1]
        
        if rotation == 0 and pt_cord != center_cord:
            container[0] = pt_cord
        rs.DeleteObjects(temp_circle)
        
        #update offset_cords
        offset_cords = point_set(pt_cord, dim, thk)
        #hide start_points
        rs.HideObjects(start_points)
       
        temp_circle = []
        for cord in offset_cords:
            point = rs.AddPoint(cord)
            next_points.append(point)
            temp_circle.append(rs.AddCircle(point, 2))
            
        next_cord = rs.GetPoint("Select the next point: ")#, next_points[0]
        rs.HideObjects(next_points)
        rs.DeleteObjects(temp_circle)
        
        #start draw according to the mode
        if next_cord not in container:
            ps = draw_mode(thk, dim, pt_cord, next_cord)
    
    if rotation % 3 == 1:  ###############
        print("first round")
        pt1 = pt_cord
        pt2 = container[-1] #selected point just before
        vec = pt2 - pt1
        a = vec[0]
        b = vec[1]
        c = vec[2]
        x = dim + 2* thk
        
        #update offset_cords
        if a == 0: # p_yz plane
            offset_cords = [[(a + x, b, 0), (a - x, b, 0)], #perpendicular
                        [(a + x, 0, c), (a - x, 0, c)],
                        [(a + x, b, 0), (a, b, -c)], #extension
                        [(a - x, b, 0), (a, b, -c)],
                        [(a + x, 0, c), (a, -b, c)],
                        [(a - x, 0, c), (a, -b, c)]]
        if b == 0: # p_zx plane
            offset_cords = [[(a, b + x, 0), (a, b - x, 0)],
                        [(0, b + x, c), (0, b - x, c)],
                        [(a, b + x, 0), (a, b, -c)], #extension
                        [(a, b - x, 0), (a, b, -c)],
                        [(0, b + x, c), (-a, b, c)],
                        [(0, b - x, c), (-a, b, c)]]
        if c == 0: # p_xy plane
            offset_cords = [[(0, b, c + x), (0, b, c - x)],
                        [(a, 0, c + x), (a, 0, c - x)],
                        [(0, b, c + x), (-a, b, c)], #extension
                        [(0, b, c - x), (-a, b, c)],
                        [(a, 0, c + x), (a, -b, c)],
                        [(a, 0, c - x), (a, -b, c)]]
        
        for set in offset_cords:
            for point in set:
                next_point = rs.AddPoint(rs.VectorAdd(point, pt1))
                next_points.append(next_point)
                temp_circle.append(rs.AddCircle(next_point, 2))
        next_cord = rs.GetPoint("Select the next point: ")#, next_points[0]
        
        rs.HideObjects(next_points)
        rs.DeleteObjects(temp_circle)
        
        #save the three sets
        next_vec = next_cord - pt_cord
        a = next_vec[0] - vec[0]
        b = next_vec[1] - vec[1]
        c = next_vec[2] - vec[2]
        
        if (a, b, c).count(0) == 1:
            print(1)
            for set in offset_cords:
                for point in set:
                    if ((a == 0 and next_vec[0] == point[0]) or
                        (b == 0 and next_vec[1] == point[1]) or
                        (c == 0 and next_vec[2] == point[2]) and
                        (set not in three_set) ):
                            three_set.append(set)
        else:
            print("aligned")
            for set in offset_cords:
                first, second = set
                if a == 0 and next_vec[0] != 0:
                    if first[0] == second[0] and first[0] == next_vec[0] and set not in three_set:
                        print(1, first, second, next_vec)
                        three_set.append(set)
                if b == 0 and next_vec[1] != 0:
                    if first[1] == second[1] and first[1] == next_vec[1] and set not in three_set:
                        print(2, first, second, next_vec)
                        three_set.append(set)
                if c == 0 and next_vec[2] != 0:
                    if first[2] == second[2] and first[2] == next_vec[2] and set not in three_set:
                        print(3, first, second, next_vec)
                        three_set.append(set)
            
        ps = draw_mode(thk, dim, pt_cord, next_cord)

    elif rotation % 3 == 2:###############
        print("second round")
        for set in three_set:
            for item in set:
                if item != tuple(container[-1]):
                    next_point = rs.AddPoint(rs.VectorAdd(item, pt_cord))
                    next_points.append(next_point)
                    temp_circle.append(rs.AddCircle(next_point, 2))
                
        next_cord = rs.GetPoint("Select the next point: ")#, next_points[0]
        rs.HideObjects(next_points)
        rs.DeleteObjects(temp_circle)
        
        ps = draw_mode(thk, dim, pt_cord, next_cord)
        three_set=[]
        
    container.append(next_cord)
    element_mode(pt_cord, rotation + 1, mode, threshold, container, three_set)




center_pt = rs.AddPoint( (0, 0, 0) )
#brep = rs.AddSphere((0, 0, 0), 30)
#brep = rs.GetObject("select 3D object")
rs.HideObject(center_pt)
center_cord = rs.PointCoordinates(center_pt)
container = [center_cord] #trajectory
ps_box = [] #A
c_box = [] #A
three_set=[] #C
threshold = 30   #rds s.GetInteger("Insert the rotation rumber: ", 3)
#cuboctahedron_symmetry(center_cord, 0, 4, threshold, container, brep, ps_box, c_box)
#cuboctahedron(center_cord, 0, 0, threshold, container)
element_mode(center_cord, 0, 0, threshold, container, three_set)
#rs.HideObject(brep)


