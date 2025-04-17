import rhinoscriptsyntax as rs

center_pt = rs.AddPoint( (0, 0, 0) )

def cuboctahedron(pt, rotation):
    if rotation >= 2:
        return
        
    len = 30
    
    pt_cord = rs.PointCoordinates(pt)

    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]

    x = len/2
    offsets = [
            (x, x, 0), (x, -x, 0), (-x, x, 0), (-x, -x, 0),  # p_xy plane
            (0, x, x), (0, x, -x), (0, -x, x), (0, -x, -x),  # p_yz plane
            (x, 0, x), (-x, 0, x), (x, 0, -x), (-x, 0, -x)   # p_zx plane
    ]
    pts = []
    lines = []
    for offset in offsets:
        next_pt = (a + offset[0], b + offset[1], c + offset[2])
        pts.append(next_pt)
        line_id = rs.AddLine(pt_cord, next_pt)
        lines.append(line_id)
        cuboctahedron(next_pt, rotation + 1)

cuboctahedron(center_pt, 0)