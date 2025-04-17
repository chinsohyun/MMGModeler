import rhinoscriptsyntax as rs
import Rhino
import Eto.Forms as forms
import Eto.Drawing as drawing
import copy
import json
import os
import datetime

rs.DefaultRenderer(False)


class RemoteControlPanel(forms.Form):
    def __init__(self):
        self.Title = "MMGModeler"
        self.ClientSize = drawing.Size(360, -1)
        
        self.save_directory = os.path.join(os.path.expanduser("~"), "Documents", "MMGModeler")
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)  

        self.seed_label = forms.Label(Text="  Seed shape(0-7):")
        self.seed_label.Size = drawing.Size(-1, 30)
        self.seed_input = forms.NumericUpDown(Value=0, MinValue=0, MaxValue=7)
        self.seed_input.Size = drawing.Size(-1, 30)

        self.mode_label = forms.Label(Text="  Mode:")
        self.mode_input = forms.ComboBox()
        self.mode_input.Items.Add("ElementMode")
        self.mode_input.Items.Add("ChunkMode")
        self.mode_input.Items.Add("SubtractMode")
        self.mode_input.SelectedIndex = 0 

        self.threshold_label = forms.Label(Text="  Threshold:")
        self.threshold_input = forms.TextBox()
        self.threshold_input.Text = "10"

        self.run_button = forms.Button(Text="Run")
        self.run_button.Click += self.on_run_button_click
        self.run_button.Size = drawing.Size(120, 30)
        
        self.break_button = forms.Button(Text="Break")
        self.break_button.Click += self.on_break_button_click
        self.break_button.Size = drawing.Size(120, 30)
        self.break_button.Enabled = False  
        
        self.back_button = forms.Button(Text="Back")
        self.back_button.Click += self.on_back_button_click 
        self.back_button.Size = drawing.Size(120, 35)
        self.back_button.Enabled = True 
        
        self.delete_button = forms.Button(Text="Delete")
        self.delete_button.Click += self.on_delete_button_click 
        self.delete_button.Size = drawing.Size(120, 35)
        self.delete_button.Enabled = True 
        
        self.redo_button = forms.Button(Text="Redo")
        self.redo_button.Click += self.on_redo_button_click 
        self.redo_button.Size = drawing.Size(120, 35)
        self.redo_button.Enabled = True 

        self.seed_label2 = forms.Label(Text="  Change seed(0-7):")
        self.seed_input2 = forms.NumericUpDown(Value=2, MinValue=0, MaxValue=7)

        self.replace_button = forms.Button(Text="Replace")
        self.replace_button.Click += self.on_replace_button_click 
        self.replace_button.Size = drawing.Size(120, 35)
        self.replace_button.Enabled = True 
        
        descrip1 = ("Seed shapes \n"
                    "Seed 0: Circular\n"
                    "Seed 1: Square\n"
                    "Seed 2:'Z'\n"
                    "Seed 3: Linear\n"
                    "Seed 4: Lieul\n"
                    "Seed 5: Concave\n"
                    "Seed 6: Arc\n"
                    "Seed 7: 'L'\n"
                   )
                   
        descrip2 = ("Modes \n"
            "'incremental unit'\n"
            "1. Element\n"
            "2. Chunk\n"
            "3. Subtract"
           )
        self.description1 = forms.Label(Text= descrip1)
        self.description2 = forms.Label(Text= descrip2)
        
        panel1 = forms.Panel()
        panel1.Padding = drawing.Padding(10)  
        panel1.Content = self.description1
        panel2 = forms.Panel()
        panel2.Padding = drawing.Padding(10)  
        panel2.Content = self.description2
       
        self.clean_button = forms.Button(Text="Clean")
        self.clean_button.Click += self.on_clean_button_click 
        self.clean_button.Size = drawing.Size(120, 35)
        self.clean_button.Enabled = True 
        
        self.load_button = forms.Button(Text="Load")
        self.load_button.Click += self.load_trajectory
        self.load_button.Size = drawing.Size(120, 35)
        self.load_button.Enabled = True 
        
        self.save_button = forms.Button(Text="Save")
        self.save_button.Click += self.save_trajectory
        self.save_button.Size = drawing.Size(120, 35)
        self.save_button.Enabled = True 
        
        layout = forms.DynamicLayout()
        layout.AddRow(" ")
        layout.AddRow(self.seed_label, self.seed_input, None )
        layout.AddRow(self.mode_label, self.mode_input, self.run_button)
        layout.AddRow(self.threshold_label, self.threshold_input, self.break_button)
        layout.AddRow(None, "\n --------- Edit --------")
        layout.AddRow(" ")
        layout.AddRow(self.back_button, self.delete_button, self.redo_button)
        layout.AddRow(self.seed_label2, self.seed_input2, self.replace_button)
        layout.AddRow(None, "\n ----- Description -----")
        layout.AddRow(panel1, panel2)
        layout.AddRow(self.clean_button, self.load_button, self.save_button)
        layout.AddRow(" ")
        
        self.Content = layout
        
        self.stop_flag = False
        
        self.coords = []
        self.lines = []
        self.simples = []
        self.shapes = []
        
        self.archive = []
        self.memory = []
        
        self.seeds =[]#
        self.boundary = None
        
        self.run_timestamp = None
        self.end_timestamp = None
        self.mode = None
        self.seed = None

        
    def on_run_button_click(self, sender, e):
        self.run_timestamp = datetime.datetime.now()
        
        self.run_button.Enabled = False
        self.back_button.Enabled = False
        self.delete_button.Enabled = False
        self.redo_button.Enabled = False
        self.replace_button.Enabled = False
        self.clean_button.Enabled = False
        self.load_button.Enabled = False
        self.save_button.Enabled = False
        self.break_button.Enabled = True
        self.stop_flag = False
        
        try:
            self.seed = int(self.seed_input.Value)
            self.mode = self.mode_input.SelectedIndex  
            threshold_str = self.threshold_input.Text
            if threshold_str == "":  # Ensure threshold is not empty
                rs.MessageBox("Threshold value is required.")
                return
            threshold = int(threshold_str)
            
        except ValueError:
            rs.MessageBox("Invalid input. Please enter valid numbers.")
            return
                
        try:            
            if self.mode == 0: #Element
                rs.ViewDisplayMode('Perspective', 'Arctic')
                three_set = []  
                element((0, 0, 0), 0, threshold, self.coords, self.simples, self.lines, self.shapes, [], [], self.seed)
                rs.MessageBox(":D \nGenerating elements completed. \nChoose the next mode with seeds.")
            elif self.mode == 1: #Chunk
                rs.ViewDisplayMode('Perspective', 'Arctic')
                chunk((0, 0, 0), 0, self.seed, threshold, self.coords, self.simples, self.lines, self.shapes)
                rs.MessageBox(":D \nGenerating chunks completed. \nChoose the next mode with seeds.")
            elif self.mode == 2: #Subtract
                views = rs.ViewNames(return_names=False, view_type=1)
                rs.ViewDisplayMode('Perspective', 'Wireframe')
                self.boundary = subtract(None, 0, self.seed, threshold, self.boundary, self.coords, self.simples, self.lines, self.shapes)
                rs.MessageBox(":D \nSubtraction completed! \nChoose the next mode with seeds")
                rs.ViewDisplayMode('Perspective', 'Arctic')
            self.end_timestamp = datetime.datetime.now()
            
            self.seeds = [self.seed] * threshold

            data = {
                "running time": str(self.end_timestamp - self.run_timestamp),
                "mode":self.mode,
                "seed":self.seed,
                "geometry": {
                    "coords": self.coords,
                    "lines": self.lines,
                }
            }
            self.memory.append(data)
            self.archive = [] #empty trash

        except Exception as ex:
            rs.MessageBox("An error occurred: {}".format(str(ex)))
    
        finally:
            self.run_button.Enabled = True
            self.back_button.Enabled = True
            self.delete_button.Enabled = True
            self.redo_button.Enabled = True
            self.replace_button.Enabled = True
            self.clean_button.Enabled = True
            self.load_button.Enabled = True
            self.save_button.Enabled = True
            self.break_button.Enabled = False
            
    def on_break_button_click(self, sender, e):
        # Set the stop flag to True to signal the process to stop
        self.stop_flag = True
        rs.MessageBox("Break after mouse click.")
        Rhino.RhinoApp.Wait()
        
    def save_trajectory(self, sender=None, e=None):
        try:
            save_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = "traj_{}.json".format(save_timestamp)
            file_path = os.path.join(self.save_directory, filename)
            
            with open(file_path, "w") as f:
                json.dump(self.memory, f, indent=4)
            rs.MessageBox("Trajectory saved successfully!\n\nFile location:\n{}".format(file_path))
        except Exception as ex:
            rs.MessageBox("Error saving trajectory: {}".format(str(ex)))

    def load_trajectory(self, sender, e):
        try:
            file_path = rs.OpenFileName("Select a trajectory file", "*.json", self.save_directory)
            if not file_path:
                return
                
            with open(file_path, "r") as f:
                saved_data = json.load(f)
            self.memory += saved_data
            print(self.memory)
            for data in saved_data:
                lines = data["geometry"]["lines"]
                coords = data["geometry"]["coords"]
                mode = data["mode"]
                self.seed = data["seed"]
                
                self.coords += coords
                self.lines += lines

                simples = []
                dim = 15
                thk = 0.5625 + 0.525
                for line in lines:
                    simple = set()
                    for point in line:
                        simple.add(tuple(point))
                    simples.append(simple)
                    pt_cord, next_cord = line
                    self.shapes.append(draw_mode(thk, dim, pt_cord, next_cord, self.seed))
                    
                self.simples += simples

            print(len(self.coords), len(self.lines), len(self.shapes), len(self.simples), self.seed)
        except Exception as ex:
            rs.MessageBox("Error loading trajectory: {}".format(str(ex)))
        
    def on_back_button_click(self, sender, e):
        try:
            object = self.shapes.pop()
            if not object:
                return
            #save data in archive
            data = {
                    "coord": self.coords.pop(),
                    "line": self.lines.pop(),
                    "shape": object,
                    "simple": self.simples.pop(),
                    "seed": self.seeds.pop()
            }
            self.archive.append(data)
            print("archive", len(self.archive))
            print(len(self.coords), len(self.lines), len(self.shapes), len(self.simples), self.seed)
            if object: 
                rs.DeleteObject(object)
                
        except Exception as ex:
            rs.MessageBox("Error latest deletion: {}".format(str(ex)))
            
    def on_delete_button_click(self, sender, e):
        object = rs.GetObject("Choose object to delete:")
        
        if not object:
            return
        try:
            index = self.shapes.index(object) 
            print(index, len(self.coords))
            if index < 0 or index > len(self.coords):
                print("Index out of range for deletion.")
            print("get data")
            print(len(self.coords), len(self.lines), len(self.shapes), len(self.simples), self.seed)
            data = {
                    "coord": self.coords.pop(index+1), #What if?
                    "line": self.lines.pop(index),
                    "shape": self.shapes.pop(index),
                    "simple": self.simples.pop(index),
                    "seed": self.seeds.pop(index)
            }
            print(data)
            self.archive.append(data)
            print("archive", len(self.archive))
            print(len(self.coords), len(self.lines), len(self.shapes), len(self.simples), self.seed)
            rs.DeleteObject(object)
        except Exception as ex:
            rs.MessageBox("Error deletion: {}".format(str(ex)))

    def on_redo_button_click(self, sender, e):
        dim = 15
        thk = 0.5625 + 0.525
        try:
            if not self.archive:
                return
            data = self.archive.pop()
    
            vector = data["line"]
            point = data["coord"]
            simple = data["simple"] #how to use original object_id? 
            
            self.coords.append(point)
            self.lines.append(vector)
            self.simples.append(simple)
            self.seed = data["seed"]
    
            pt_cord, next_cord = vector
            object = draw_mode(thk, dim, pt_cord, next_cord, self.seed) ##the set sequence might be problematic
            self.shapes.append(object)
            print(len(self.coords), len(self.lines), len(self.shapes), len(self.simples), self.seed)
            
        except Exception as ex:
            rs.MessageBox("Error recreating: {}".format(str(ex)))
            
    def on_replace_button_click(self, sender, e):
        try:
            new_seed = int(self.seed_input2.Value)
            object = rs.GetObject("Choose object to replace:")
            if not object:
                return
            index = self.shapes.index(object) 
            if index < 0 or index > len(self.coords):
                print("Index out of range for deletion.")
                
            #handle memory
            vector = self.lines[index]
            #print("searching:", vector)
            memory_i = -1
            dict_i = -1
            for i, dict in enumerate(self.memory):
                if vector in dict["geometry"]["lines"]:
                    dict_i = dict["geometry"]["lines"].index(vector)
                    memory_i = i
                    break
            if memory_i == -1 or dict_i == -1:
                print("Vector not found in the saved data")
                return
            data = self.memory[memory_i]
            data1 = copy.deepcopy(data)
            data2 = copy.deepcopy(data)
            data_seed = {
                "running time": "replaced" + str(datetime.datetime.now()),
                "mode": data["mode"],
                "seed": new_seed,
                "geometry": {
                    "coords": [self.coords[dict_i]],
                    "lines": [self.lines[dict_i]],
                },
            }
            
            data1["geometry"]["coords"] = data["geometry"]["coords"][:dict_i + 1]
            data1["geometry"]["lines"] = data["geometry"]["lines"][:dict_i]
            data2["geometry"]["coords"] = data["geometry"]["coords"][dict_i + 2:]
            data2["geometry"]["lines"] = data["geometry"]["lines"][dict_i + 1:]
            
            if dict_i != 0:
                self.memory[memory_i] = data1  
            self.memory.insert(memory_i + 1, data_seed) 
            self.memory.insert(memory_i + 2, data2)  
            
            #clean self.memory
            self.memory = [dict for dict in self.memory if dict['geometry']['coords'] or dict['geometry']['lines']]
            
            #handle current data
            rs.DeleteObject(object)
            dim = 15
            thk = 0.5625 + 0.525
            pt_cord, next_cord = vector
            self.shapes[index] = draw_mode(thk, dim, pt_cord, next_cord, new_seed)
            
        except Exception as ex:
            rs.MessageBox("An error occurred during replacement: {}".format(str(ex)))
        
    def on_clean_button_click(self, sender, e):
        self.coords = []
        self.lines = []
        self.simples = []
        self.shapes = []
        
        self.archive = []
        self.memory = []
        
        self.modes = []#
        self.seeds =[]#
        self.boundary = None
        rs.MessageBox("Cleaned previous data.")


###############################################################################


def select_shape(seed):
    if seed == 0:
        block = "f_circle"
    elif seed == 1:
        block = "e_square"
    elif seed == 2:
        block = "b_z"
    elif seed == 3:
        block = "a_linear"
    elif seed == 4:
        block = "g_lieul"
    elif seed == 5:
        block = "g_arch"
    elif seed == 6:
        block = "d_arc"
    elif seed == 7:
        block = "c_L"

    return block

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

def round_point(cord):
    a = round(float(cord[0]), 2)
    b = round(float(cord[1]), 2)
    c = round(float(cord[2]), 2)
    return((a, b, c))

def draw_mode(thk, dim, pt_cord, next_cord, seed):
    x = next_cord[0] - pt_cord[0]  # p_yz plane
    y = next_cord[1] - pt_cord[1]  # p_zx plane
    z = next_cord[2] - pt_cord[2]  # p_xy plane
    
    r2 = None
    dis = dim + thk * 2 
    direction = (0, 0, 0)
    direction = rs.VectorAdd(pt_cord, (0, 0, 0)) #add vector to the origin!
    
    m = rs.XformIdentity()
    
    if x == 0:# p_yz plane
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
    block = select_shape(seed)
    ps = rs.InsertBlock2(block, xform)
    return ps


#####################################################################

#def interpreter(seed, lines):
#    dim = 15
#    thk = 0.5625 + 0.525
#    
#    for line in lines:
#        pt_cord, next_cord = line
#        draw_mode(thk, dim, pt_cord, next_cord, seed)
    

#####################################################################


def subtract(pt_cord, rotation, seed, threshold, boundary, coords, simples, lines, shapes):
    dim = 15
    thk = 0.5625 + 0.525
    
    if rotation == 0:
        if boundary == None:
            boundary = rs.GetObject("Choose a boundary object")
        else:
            rs.MessageBox("There is a saved boundary object. \nContinue to build from it..")
        if coords != []:
            sel_points = []
            sel_cords = []
            for next_sel in coords: # mark saved points
                if rs.IsPointInSurface(boundary, next_sel):
                    sel_points.append(rs.AddPoint(next_sel))
                    sel_cords.append(tuple(next_sel))
                
            pt_cord = rs.GetPoint("Select a starting center: ")
            if sel_cords: 
                while tuple(pt_cord) not in sel_cords:
                    pt_cord = rs.GetPoint("Warning! Please choose from the points: ")
                    if pt_cord == None:
                        break
                rs.DeleteObjects(sel_points)
                
        du = rs.SurfaceDomain(boundary, 0)
        u = du[1]/dim
        dv = rs.SurfaceDomain(boundary, 1)
        v = dv[1]/dim
        if coords == [] or pt_cord == None:
            pt_cord = rs.EvaluateSurface(boundary, u, v)
        threshold = int(max(u, v))
        if threshold > 5:
            rs.MessageBox("The volume is too big and I'm afraid of time-consuming. \nChange the threshold into 5.")
            threshold = 5
        rs.MessageBox("Subtraction is now working.... \nClick OK and WAIT until the next instruction popped up. ")
        
    if rotation >= threshold:
        return
        
    if form.stop_flag:
        return
        
    offset_cords = point_set(pt_cord, dim, thk)
            
    for next_cord in offset_cords:
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if form.stop_flag:
            return
            
        if rs.IsPointInSurface(boundary, next_cord):
            if {p_c, n_c} not in simples:
                ps = draw_mode(thk, dim, pt_cord, next_cord, seed)
                simples.append({p_c, n_c}) #list of sets
                coords.append(next_cord)
                shapes.append(ps)
                lines.append([tuple(pt_cord), tuple(next_cord)])
            subtract(next_cord, rotation + 1, seed, threshold, boundary, coords, simples, lines, shapes)
            
    if rotation == 0:
        rs.HideObject(boundary)
        return boundary



def chunk(pt_cord, rotation, seed, threshold, coords, simples, lines, shapes):
    
    if rotation >= threshold:
        return
    dim = 15
    thk = 0.5625 + 0.525
    sel_points = []
    sel_cords = []
    
    if rotation == 0 and coords == []:
        pt_cord = rs.GetPoint("Select a new center: ")
        if form.stop_flag: #break before save. 
            return
        coords.append(tuple(pt_cord))
            
    elif coords != []:
        for next_sel in coords: # mark saved points
            sel_points.append(rs.AddPoint(next_sel))
            sel_cords.append(tuple(next_sel))
            
        pt_cord = rs.GetPoint("Select a new center: ")
        while tuple(pt_cord) not in sel_cords:
            pt_cord = rs.GetPoint("Warning! Please choose from the points: ")
            if pt_cord == None:
                break
        rs.DeleteObjects(sel_points)
        sel_cords = []
        if form.stop_flag:
            return
        
    offset_cords = point_set(pt_cord, dim, thk)
    
    next_pts = []
    for next_cord in offset_cords:
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if {p_c , n_c} not in simples: #draw!
            simples.append({p_c , n_c})
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            coords.append(next_cord) #All coordinates become elements. sequence should be identical.
            lines.append([tuple(pt_cord), tuple(next_cord)])
            
    chunk(pt_cord, rotation + 1, seed, threshold, coords, simples, lines, shapes)



def element(pt_cord, rotation, threshold, coords, simples, lines, shapes, three_set, center_mark, seed):

    if rotation >= threshold:
        rs.DeleteObjects(center_mark)
        return

    dim = 15  #real size
    thk = 0.5625 + 0.525
    
    #start_points
    temp_circle = []

    #next_points
    next_points = []
    next_coords = []
    
    if rotation %3 == 0: ############################################################0
        xy = rs.WorldXYPlane()
        start_points= []
        for point in coords:  #mark next centers
            translation = (point[0]-0.5, point[1]-0.5, point[2])
            rect = rs.AddRectangle(xy, 1, 1)
            rs.MoveObject(rect, translation)
            start_points.append(rs.AddPoint(point))
            temp_circle.append(rect)
            
        #pt_cord updated
        if rotation != 0 and rotation < 5:
            rs.MessageBox("Hi there! \nChoose next center every 3 point selection.")
        pt_cord = rs.GetPoint("Select a new center: ") 
        if rotation == 0 and coords == []:
            coords.append(tuple(pt_cord)) 
        else:
            while tuple(pt_cord) not in coords:
                pt_cord = rs.GetPoint("Warning! Please choose from the points: ")
                if pt_cord == None:
                    break
        rs.DeleteObjects(temp_circle)
        rs.DeleteObjects(start_points)
            
        if center_mark != []:
            rs.DeleteObjects(center_mark)
        if form.stop_flag:
            return
        
        center_a = rs.AddRectangle(xy, 1.5, 1.5)  #mark center!
        translation = (pt_cord[0]-0.75, pt_cord[1]-0.75, pt_cord[2])
        rs.MoveObject(center_a, translation)
        center_b = rs.RotateObject(center_a, pt_cord, 90, [0,1,0], True)
        center_c = rs.RotateObject(center_a, pt_cord, 90, [1,0,0], True)
        center_mark = [center_a, center_b, center_c]
        
        #update offset_cords
        offset_cords = point_set(pt_cord, dim, thk)
        
        for cord in offset_cords:  #mark next points
            point = rs.AddPoint(cord)
            next_points.append(point)
            temp_circle.append(rs.AddCircle(point, 2))
            
        next_cord = rs.GetPoint("Select the next point: ")
        while tuple(next_cord) not in offset_cords:
            next_cord = rs.GetPoint("Warning! Please choose from the points: ")
            if pt_cord == None:
                break
        rs.DeleteObjects(next_points)
        rs.DeleteObjects(temp_circle)
        if form.stop_flag:
            rs.DeleteObjects(center_mark)
            return
            
        #start draw according to the mode
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if {p_c, n_c} not in simples: #draw!
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            simples.append({p_c, n_c})
            lines.append([tuple(pt_cord), tuple(next_cord)])
    
    if rotation % 3 == 1:  ############################################################1

        pt1 = pt_cord       #       Configuration rule 2, new offset_cords      
        pt2 = coords[-1] #selected point just before
        vec = rs.VectorSubtract(pt2, pt1)
        a = vec[0]
        b = vec[1]
        c = vec[2]
        x = dim + 2* thk
        
        
        if a == 0: # p_yz plane      #       update offset_cords
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
                next_coords.append(tuple(rs.VectorAdd(point, pt1)))
                temp_circle.append(rs.AddCircle(next_point, 2))
                
        next_cord = rs.GetPoint("Select the next point: ")
        while tuple(next_cord) not in next_coords:
            next_cord = rs.GetPoint("Warning! Please choose from the points: ")
            if pt_cord == None:
                break
        rs.DeleteObjects(next_points)
        rs.DeleteObjects(temp_circle)
        if form.stop_flag:
            rs.DeleteObjects(center_mark)
            return
        #save the three sets
        next_vec = next_cord - pt_cord
        a = next_vec[0] - vec[0]
        b = next_vec[1] - vec[1]
        c = next_vec[2] - vec[2]
        
        if (a, b, c).count(0) == 1:
            for set in offset_cords:
                for point in set:
                    if ((a == 0 and next_vec[0] == point[0]) or
                        (b == 0 and next_vec[1] == point[1]) or
                        (c == 0 and next_vec[2] == point[2]) and  
                        (set not in three_set) ):
                            three_set.append(set)
        else:
            for set in offset_cords: # aligned
                first, second = set
                if a == 0 and next_vec[0] != 0:
                    if first[0] == second[0] and first[0] == next_vec[0] and set not in three_set: 
                        three_set.append(set)

                if b == 0 and next_vec[1] != 0:
                    if first[1] == second[1] and first[1] == next_vec[1] and set not in three_set:
                        three_set.append(set)
                if c == 0 and next_vec[2] != 0:
                    if first[2] == second[2] and first[2] == next_vec[2] and set not in three_set:
                        three_set.append(set)

        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if {p_c, n_c} not in simples: #draw!
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            simples.append({p_c, n_c})
            lines.append([tuple(pt_cord), tuple(next_cord)])
        
    elif rotation % 3 == 2: ############################################################2

        offset_cords = point_set(pt_cord, dim, thk)
        for set in three_set:
            for item in set:
                next_point = rs.AddPoint(rs.VectorAdd(item, pt_cord))
                next_points.append(next_point)
                next_coords.append(tuple(rs.VectorAdd(item, pt_cord)))
                temp_circle.append(rs.AddCircle(next_point, 2))
                
        next_cord = rs.GetPoint("Select the next point: ")
        while tuple(next_cord) not in next_coords:
            next_cord = rs.GetPoint("Warning! Please choose from the points: ")
            if pt_cord == None:
                break
        rs.DeleteObjects(next_points)
        rs.DeleteObjects(temp_circle)
        if form.stop_flag:
            rs.DeleteObjects(center_mark)
            return
            
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if {p_c, n_c} not in simples: #draw!
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            simples.append({p_c, n_c})
            lines.append([tuple(pt_cord), tuple(next_cord)])
        three_set=[]
        
    coords.append(tuple(next_cord))
    element(pt_cord, rotation + 1, threshold, coords, simples, lines, shapes, three_set, center_mark, seed)


form = RemoteControlPanel()
form.Show()

##debug
#coord_container = []
#line_container = []
#shape_container = []
#boundary = None 
#subtract((0, 0, 0), 0, 0, 4, boundary, coord_container, line_container, shape_container)
#chunk((0, 0, 0), 0, 0, 4, coord_container, line_container, shape_container)
#element((0, 0, 0), 0, 4, coord_container, shape_container, [], line_container, [], [], 0)
#print("coord: ", len(coord_container), ": ", coord_container)
#print("line: ", len(line_container), ": ", line_container)
#print("shape: ", len(shape_container), ": ", shape_container)



