import rhinoscriptsyntax as rs
import Eto.Forms as forms
import Eto.Drawing as drawing

# class StopRecursionException(Exception):
#     pass

class RemoteControlPanel(forms.Form):
    def __init__(self):
        self.Title = "A Minimal Making Grammar"
        self.ClientSize = drawing.Size(300, 115)

        self.seed_label = forms.Label(Text="Seed type(0-4):")
        self.seed_input = forms.NumericUpDown(Value=0, MinValue=0, MaxValue=4)

        self.mode_label = forms.Label(Text="Mode:")
        self.mode_input = forms.ComboBox()
        self.mode_input.Items.Add("Mode 1")
        self.mode_input.Items.Add("Mode 2")
        self.mode_input.Items.Add("Mode 3")
        self.mode_input.SelectedIndex = 2 

        self.threshold_label = forms.Label(Text="Threshold(# of generation):")
        self.threshold_input = forms.TextBox()

        self.run_button = forms.Button(Text="Run")
        self.run_button.Click += self.on_run_button_click

#        self.break_button = forms.Button(Text="Break")
#        self.break_button.Click += self.on_break_button_click
#        self.break_button.Enabled = False  
        
        layout = forms.DynamicLayout()
        layout.AddRow(self.seed_label, self.seed_input)
        layout.AddRow(self.mode_label, self.mode_input)
        layout.AddRow(self.threshold_label, self.threshold_input)
        layout.AddRow(None, self.run_button)
#        layout.AddRow(None, self.break_button)
        
        self.Content = layout
        
        self.stop_flag = False

        
    def on_run_button_click(self, sender, e):
        try:
            seed = int(self.seed_input.Value)
            mode = self.mode_input.SelectedIndex  
            threshold_str = self.threshold_input.Text
            if threshold_str == "":  # Ensure threshold is not empty
                rs.MessageBox("Threshold value is required.")
                return
            threshold = int(threshold_str)
    
            center_cord = (0, 0, 0)   
            container = [center_cord]
                    
            if mode == 0: #mode 1
                ps_box = [] 
                c_box = [] 
                brep = rs.AddSphere((0, 0, 0), 30)
                # brep = rs.GetObject("select 3D object")
                cuboctahedron_symmetry(center_cord, 0, seed, threshold, container, brep, ps_box, c_box)
                rs.DeleteObject(brep)
            elif mode == 1: #mode 2
                cuboctahedron(center_cord, 0, seed, threshold, container)
    
            elif mode == 2: #mode 3
                three_set = []  
                center_pt = rs.AddPoint( (0, 0, 0) )
                center_cord = rs.PointCoordinates(center_pt)   
                container = [center_cord]
                cuboctahedron_unit(center_cord, 0, seed, threshold, container, three_set)
                
        # except StopRecursionException:
        #     # Handle stop recursion exception to exit gracefully
        #     rs.MessageBox("Process was stopped.")
            
        except Exception as ex:
            # Handle unexpected errors gracefully
            rs.MessageBox("An error occurred: {}".format(str(ex)))
        
#        finally:
#            # Disable the break button once the process is done
#            self.stop_flag = True
#            self.break_button.Enabled = False
            

###############################################################################

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
    
    if rotation >= number:
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

        if rs.IsPointInSurface(boundary, next_cord):
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
                
                cuboctahedron_symmetry(next_cord, rotation + 1, mode, number, container, boundary, ps_box, c_box)


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


def point_set(pt_cord, len):
    x = len/2
    a = pt_cord[0]
    b = pt_cord[1]
    c = pt_cord[2]
    offset_cords = [
        (a + x, b + x, c), (a + x, b - x, c), (a - x, b + x, c), (a - x, b - x, c),  # p_xy plane
        (a, b + x, c + x), (a, b + x, c - x), (a, b - x, c + x), (a, b - x, c - x),  # p_yz plane
        (a + x, b, c + x), (a - x, b, c + x), (a + x, b, c - x), (a - x, b, c - x)   # p_zx plane
    ]
    return offset_cords

def draw_mode(mode, width, len, offset, pt_cord, next_cord):
    
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
         ps = rs.AddPlanarSrf(polylines)
    return ps

#def point_set_when_rotation_1(point):
#    pass


def cuboctahedron_unit(pt_cord, rotation, mode, threshold, container, three_set):

    if rotation >= threshold:
        return
        
    len = 30
    width = 1
    offset_cords = point_set(pt_cord, len)
    
    #s_points
    temp_circle = []
    if rotation == 3:
        rotation = 0
        s_points= []
        for s_point in container:
            s_points.append(rs.AddPoint(s_point))
            
            temp_circle.append(rs.AddCircle(s_point, 3))
            
        #pt_cord updated
        pt_cord = rs.GetPoint("Select a new center: ", container[-1])
        rs.DeleteObjects(temp_circle)
        #update offset_cords
        offset_cords = point_set(pt_cord, len)
        #hide s_points
        rs.HideObjects(s_points)
        
        
    #n_points
    n_points = []
    
    if rotation == 1:  ###############

        pt1 = pt_cord
        pt2 = container[-1] #selected point just before
        vec = pt2 - pt1
        a = vec[0]
        b = vec[1]
        c = vec[2]
        x = len/2
        if a == 0:
            offset_cords = [[(a + x, b, 0), (a - x, b, 0)], #perpendicular
                        [(a + x, 0, c), (a - x, 0, c)],
                        [(a + x, b, 0), (a, b, -c)], #extension
                        [(a - x, b, 0), (a, b, -c)],
                        [(a + x, 0, c), (a, -b, c)],
                        [(a - x, 0, c), (a, -b, c)]]
        if b == 0:
            offset_cords = [[(a, b + x, 0), (a, b - x, 0)],
                        [(0, b + x, c), (0, b - x, c)],
                        [(a, b + x, 0), (a, b, -c)], #extension
                        [(a, b - x, 0), (a, b, -c)],
                        [(0, b + x, c), (-a, b, c)],
                        [(0, b - x, c), (-a, b, c)]]
        if c == 0:
            offset_cords = [[(0, b, c + x), (0, b, c - x)],
                        [(a, 0, c + x), (a, 0, c - x)],
                        [(0, b, c + x), (-a, b, c)], #extension
                        [(0, b, c - x), (-a, b, c)],
                        [(a, 0, c + x), (a, -b, c)],
                        [(a, 0, c - x), (a, -b, c)]]
        
        for set in offset_cords:
            for point in set:
                n_point = rs.AddPoint(rs.VectorAdd(point, pt1))
                n_points.append(n_point)
        next_cord = rs.GetPoint("Select the next point: ", n_points[0])
        
        rs.HideObjects(n_points)
        
        #save the three sets
        for set in offset_cords:
            three_set.append(set)

        offset = [0,0,0]
        for i in range(3):
            offset[0] = next_cord[0] - pt_cord[0]
            offset[1] = next_cord[1] - pt_cord[1]
            offset[2] = next_cord[2] - pt_cord[2]
        #condition unecessary
        ps = draw_mode(mode, width, len, offset, pt_cord, next_cord)

    elif rotation == 2:###############

        for set in three_set:
            #if statement necessary
            for item in set:
                #condition unecessary
                n_point = rs.AddPoint(rs.VectorAdd(item, pt_cord))
                n_points.append(n_point)
        next_cord = rs.GetPoint("Select the next point: ", n_points[0])
        print(tuple(next_cord), tuple(pt_cord))
        rs.HideObjects(n_points)
        
        offset = [0,0,0]
        for i in range(3):
            offset[0] = next_cord[0] - pt_cord[0]
            offset[1] = next_cord[1] - pt_cord[1]
            offset[2] = next_cord[2] - pt_cord[2]
        #condition unecessary
        ps = draw_mode(mode, width, len, offset, pt_cord, next_cord)
        three_set=[]
        
    else: ###############

        for cord in offset_cords:
            point = rs.AddPoint(cord)
            n_points.append(point)
            
        next_cord = rs.GetPoint("Select the next point: ", n_points[0])
        rs.HideObjects(n_points)
        offset = next_cord - pt_cord
        
        #start draw according to the mode
        if next_cord not in container:
            ps = draw_mode(mode, width, len, offset, pt_cord, next_cord)

            
    container.append(next_cord)
    cuboctahedron_unit(pt_cord, rotation + 1, mode, threshold, container, three_set)
        

form = RemoteControlPanel()
form.Show()