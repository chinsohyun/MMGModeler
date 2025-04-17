import rhinoscriptsyntax as rs
import Rhino
import Eto.Forms as forms
import Eto.Drawing as drawing
import copy
import json
import os
import logging
import datetime

rs.DefaultRenderer(False)

class RemoteControlPanel(forms.Form):
    def __init__(self):
        self.user = "User 1"
        self.Title = "MMGModeler"
        self.ClientSize = drawing.Size(360, -1)
        
        self.save_directory = os.path.join(os.path.expanduser("~"), "Documents", "MMGModeler")
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)  
        self.save_directory_log  = os.path.join(os.path.expanduser("~"), "Documents", "MMGModeler", "log")
        if not os.path.exists(self.save_directory_log):
            os.makedirs(self.save_directory_log)  
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
        
        self.deleteAll_button = forms.Button(Text="Delete All")
        self.deleteAll_button.Click += self.on_deleteAll_button_click 
        self.deleteAll_button.Size = drawing.Size(120, 35)
        self.deleteAll_button.Enabled = True
        
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
        layout.AddRow(self.deleteAll_button)
        layout.AddRow(" ")
        
        self.Content = layout
        
        self.stop_flag = False
        
        self.coords = []
        self.lines = []
        self.simples = []
        self.shapes = []
        
        self.archive = []
        self.memory = dict()
        self.log = [{"user ID": self.user}]
        
        self.seeds =[]
        self.boundary = None
        self.mouse_data = []
        self.times = []
        self.clicks = []
        
        self.run_timestamp = None
        self.end_timestamp = None
        self.mode = None
        self.seed = None
        
        #auto_log
        self.s_filename = None
        self.l_filename = None
        self.run = False
        self.bbreak = False
        self.back = False
        self.delete = False
        self.redo = False
        self.replace = False
        self.clean = False
        self.load_prev = False
        self.load_after = False
        self.save = False   
        self.deleteAll = False
        
        self.load_log()
        self.memory_progress()

        
    def on_run_button_click(self, sender, e):
        self.run = True
        self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        
        self.run_button.Enabled = False
        self.back_button.Enabled = False
        self.delete_button.Enabled = False
        self.redo_button.Enabled = False
        self.replace_button.Enabled = False
        self.clean_button.Enabled = False
        self.load_button.Enabled = False
        self.save_button.Enabled = False
        self.break_button.Enabled = True
        self.deleteAll_button.Enabled = False
        
        self.stop_flag = False
        
        try:
            if not rs.IsView("Perspective"):
                id = rs.ViewId("Perspective")
                rs.ViewTitle(id)
                print("successfully switch to perspective view")
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
                element((0, 0, 0), 0, threshold, self.coords, self.simples, self.lines, self.shapes, [], [], self.seed, self.times, self.clicks)
                rs.MessageBox(":D \nGenerating elements completed. \nChoose the next mode with seeds.")
            elif self.mode == 1: #Chunk
                rs.ViewDisplayMode('Perspective', 'Arctic')
                chunk((0, 0, 0), 0, self.seed, threshold, self.coords, self.simples, self.lines, self.shapes, self.times, self.clicks)
                rs.MessageBox(":D \nGenerating chunks completed. \nChoose the next mode with seeds.")
            elif self.mode == 2: #Subtract
                views = rs.ViewNames(return_names=False, view_type=1)
                rs.ViewDisplayMode('Perspective', 'Wireframe')
                self.boundary = subtract(None, 0, self.seed, threshold, self.boundary, self.coords, self.simples, self.lines, self.shapes, self.times, self.clicks)
                rs.MessageBox(":D \nSubtraction completed! \nChoose the next mode with seeds")
                rs.ViewDisplayMode('Perspective', 'Arctic')
            self.end_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.seeds = [self.seed] * len(self.simples)
            self.mouse_data.append({"times_len": len(self.times), "clicks_len": len(self.clicks), "time stamps": self.times, "mouse locations": self.clicks})
            self.archive = [] #empty trash

        except Exception as ex:
            print("Error: {}".format(str(ex)))  
               
        finally:
            try:
                self.memory_progress()
                self.run = False
                if self.stop_flag == True:
                    self.bbreak = True
                    self.action_log()
                    self.bbreak = False
            except Exception as ex:
                print("Error: {}".format(str(ex)))
            self.run_button.Enabled = True
            self.back_button.Enabled = True
            self.delete_button.Enabled = True
            self.redo_button.Enabled = True
            self.replace_button.Enabled = True
            self.clean_button.Enabled = True
            self.load_button.Enabled = True
            self.save_button.Enabled = True
            self.break_button.Enabled = False
            self.deleteAll_button.Enabled = True
            #delete the given instruction
            rs.Command("SelPt")
            rs.Command("SelCrv")
            rs.Command("Delete")
        
    def on_break_button_click(self, sender, e):
        # Set the stop flag to True to signal the process to stop
        self.stop_flag = True
        self.end_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")

        rs.MessageBox("Break after mouse click.")
        Rhino.RhinoApp.Wait()
        
    def load_log(self):
        #check whether there is a previous action_log data
        try:
            self.run_timestamp = datetime.datetime.now()
            save_timestamp = datetime.datetime.now().strftime("%Y%m%d")
            self.l_filename = "log_{0}_{1}.json".format(self.user, save_timestamp)
            file_path = os.path.join(self.save_directory_log, self.l_filename)
            print("auto-log is activated")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    self.log = json.load(f)
                print("continue to use the existing log")
                self.log.append("continued: {}".format(str(self.run_timestamp.strftime("%Y%m%d_%H:%M:%S"))))
            self.log.append("initiated: {}".format(str(self.run_timestamp.strftime("%Y%m%d_%H:%M:%S"))))
        except Exception as ex:
            rs.MessageBox("Error load log: {}".format(str(ex)))
        
    def save_trajectory(self, sender=None, e=None):
        try:
            if self.lines == []:
                rs.MessageBox("Nothing to save.")
                return
         
            self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.save = True
            save_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.s_filename = "saved_by{0}_{1}.json".format(self.user, save_timestamp)
            file_path = os.path.join(self.save_directory, self.s_filename)
            
            with open(file_path, "w") as f:
                json.dump(self.memory, f, indent=4)
            self.archive = [] #empty trash
            
            self.action_log()
            self.save = False
            rs.MessageBox("Saved successfully!\n\nFile location:\n{}".format(file_path))
        except Exception as ex:
            rs.MessageBox("Error saving trajectory: {}".format(str(ex)))

    def load_trajectory(self, sender, e):
        try:
            self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.load_prev = True
            self.action_log()
            self.load_prev = False
            print("prevLoad", len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            file_path = rs.OpenFileName("Select a trajectory file", "*.json", self.save_directory)
            if not file_path:
                return
                
            with open(file_path, "r") as f:
                saved_data = json.load(f)
                print(saved_data)
            if isinstance(saved_data, list):
                for dict in reversed(saved_data):
                    if "geometry" in dict:
                        data = dict["geometry"]
                        break
            else: 
                data = saved_data
                
            if data["geometry"]["lines"] == []:
                rs.MessageBox("Nothing to load. ")
                return
                
            #to update the memory
            self.memory["loaded times"].append(str(self.run_timestamp))
            self.memory["geometry"]["seeds"] += data["geometry"]["seeds"]
            self.memory["geometry"]["coords"] += data["geometry"]["coords"]
            self.memory["geometry"]["lines"] += data["geometry"]["lines"]
            self.memory["geometry"]["coords_num"] += data["geometry"]["coords_num"]
            self.memory["geometry"]["lines_num"] += data["geometry"]["lines_num"]
            
            print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            #to add to the current data
            lines = data["geometry"]["lines"]
            seeds = data["geometry"]["seeds"]
            
            print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            simples = []
            dim = 15
            thk = 0.5625 + 0.525
            for i in range(len(lines)):
                simple = set()
                for point in lines[i]:
                    simple.add(tuple(point))
                simples.append(simple)
                pt_cord, next_cord = lines[i] #This sequence is not resolved yet!!!
                self.shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seeds[i]))
            print(simples)
            self.simples += simples
            self.archive = [] #empty trash
            print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            self.load_after = True
            self.action_log()
            self.load_after = False
            print("afterLoad", len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            rs.MessageBox(":D \nLoaded!")
            rs.Command("SelBlockInstance")
            rs.Command("'_Zoom _Selected")
        except Exception as ex:
            rs.MessageBox("Error loading trajectory: {}".format(str(ex)))
        
    def on_back_button_click(self, sender, e):
        try:
            #print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.back = True
            object = self.shapes.pop()
            self.changed_index = len(self.shapes)
            
            if not object:
                return
            else:
                rs.DeleteObject(object)
                
            #save data in archive
            archive = {
                    "coord": self.coords.pop(),
                    "line": self.lines.pop(),
                    "simple": self.simples.pop(),
                    "seed": self.seeds.pop()
            }
            if len(self.coords) == 1:
                self.coords.pop 
            #print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            self.archive.append(archive)
            #print(self.archive)
            
            self.action_log()
            self.back = False
                
        except Exception as ex:
            rs.MessageBox("Error latest deletion: {}".format(str(ex)))
            
    def on_delete_button_click(self, sender, e):
        object = rs.GetObject("Choose object to delete:")
        if not object:
            return
        try:
            #print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.delete = True
            self.changed_index = self.shapes.index(object) 
            print("index", self.changed_index , len(self.coords))
            if self.changed_index < 0 or self.changed_index  > len(self.coords):
                print("Index out of range for deletion.")
            
            archive= {
                    "coord": self.coords.pop(self.changed_index +1), #What if?
                    "line": self.lines.pop(self.changed_index),
                    "simple": self.simples.pop(self.changed_index),
                    "seed": self.seeds.pop(self.changed_index)
            }
            if len(self.coords) == 1:
                self.coords.pop
            
            self.archive.append(archive)
            self.shapes.pop(self.changed_index),
            rs.DeleteObject(object)
            print(archive, self.archive)
            #print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            self.action_log()
            self.delete = False
        except Exception as ex:
            rs.MessageBox("Error deletion: {}".format(str(ex)))

    def on_redo_button_click(self, sender, e):
        dim = 15
        thk = 0.5625 + 0.525
        try:
            self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.redo = True
            if not self.archive:
                print("Nothing to redo")
                return
            self.changed_index = len(self.shapes)
            data = self.archive.pop()
    
            vector = data["line"]
            point = data["coord"]
            simple = data["simple"] #how to use original object_id? 
            
            self.coords.append(point)
            self.lines.append(vector)
            self.simples.append(simple)
            print("data[seed]", data["seed"])
            self.seeds.append(data["seed"])
            print(len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
            pt_cord, next_cord = vector
            object = draw_mode(thk, dim, pt_cord, next_cord, self.seed) ##the set sequence might be problematic
            self.shapes.append(object)
            
            self.action_log()
            self.redo = False
            
        except Exception as ex:
            rs.MessageBox("Error recreating: {}".format(str(ex)))
            
    def on_replace_button_click(self, sender, e):
        
        try:
            self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
            self.replace = True
            new_seed = int(self.seed_input2.Value)
            object = rs.GetObject("Choose object to replace:")
            if not object:
                return
            self.changed_index = self.shapes.index(object) # How to use shape geometry data directly? 
            if self.changed_index < 0 or self.changed_index >= len(self.shapes):
                print("Index out of range for deletion.")
            #handle memory
            vector = self.lines[self.changed_index]
            #print("searching:", vector)
            dict_i = self.memory["geometry"]["lines"].index(vector)
            if dict_i < 0 or dict_i >= self.memory["geometry"]["lines_num"]:
                print("Vector not found in the saved data")
                return
            self.memory["geometry"]["seeds"][dict_i] = new_seed #so simple!
            self.memory["replaced number"] += 1
            #print(self.memory)
            #handle current data
            rs.DeleteObject(object)
            dim = 15
            thk = 0.5625 + 0.525
            pt_cord, next_cord = vector
            self.shapes[self.changed_index] = draw_mode(thk, dim, pt_cord, next_cord, new_seed)
            
            self.action_log()
            self.replace = False
        except Exception as ex:
            rs.MessageBox("An error occurred during replacement:\n" "Error: {}".format(str(ex)))
        
    def on_clean_button_click(self, sender, e):
        self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        self.clean = True
        
        self.coords = []
        self.lines = []
        self.simples = []
        self.shapes = []
        
        self.archive = []
        self.memory = []
        
        self.seeds =[]#
        self.boundary = None
        self.memory = dict()
        self.mouse_data = []
        self.times = []
        self.clicks = []
        self.run_timestamp = None
        self.end_timestamp = None
        self.mode = None
        self.seed = None
        self.memory_progress()

        self.action_log()
        print("Clean", len(self.coords), len(self.lines), len(self.simples), len(self.seeds), len(self.shapes))
        self.clean = False
        rs.MessageBox("Cleaned previous data.")
        
    def on_deleteAll_button_click(self, sender, e):
        self.run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        self.deleteAll = True
        self.save_trajectory()
        self.coords = []
        self.lines = []
        self.simples = []
        self.shapes = []
        
        self.archive = []
        self.memory = []
        
        self.seeds =[]#
        self.boundary = None
        self.memory = dict()
        self.mouse_data = []
        self.times = []
        self.clicks = []
        self.run_timestamp = None
        self.end_timestamp = None
        self.mode = None
        self.seed = None
        
        #delete instance
        rs.Command("SelBlockInstance")
        rs.Command("Delete")
        
        self.memory_progress()
        self.deleteAll = False
        rs.MessageBox("Remove data and geometry you created.")
        
    def memory_progress(self):
        if not self.memory:
            self.memory = {
                "loaded times": [],
                "replaced number": 0,
                "geometry": {
                    "seeds": self.seeds,
                    "coords": self.coords,
                    "coords_num": len(self.coords),
                    "lines": self.lines,
                    "lines_num": len(self.lines),
                }
            }
        else:
            self.memory["geometry"]["seeds"] = self.seeds
            self.memory["geometry"]["coords"] = self.coords
            self.memory["geometry"]["lines"] = self.lines
            self.memory["geometry"]["coords_num"] = len(self.coords)
            self.memory["geometry"]["lines_num"] = len(self.lines)
            
        self.action_log()
        print("Trajectory state has been updated.")
        
    def action_log(self):
        id = len(self.log)-1
        data = dict()
        if self.boundary:
            is_boundary = 1
        else:
            is_boundary = 0
        if self.run: #how to count?
            data = {
                "id": id,
                "action": "Run",
                "time stamp": str(self.run_timestamp)+"-" + str(self.end_timestamp),
                "mode": [self.mode],
                "geometry": self.memory,
                "mouse data": self.mouse_data,
                "archived object info": self.archive,
                "is boundary": is_boundary
            }
        if self.bbreak:
            data = {
                "id": id,
                "action": "Break",
                "time stamp": str(self.end_timestamp),
            }
        if self.back:
            data = {
                "id": id,
                "action": "Back",
                "time stamp": str(self.run_timestamp),
                "undone index" : self.changed_index,
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        if self.delete:
            data = {
                "id": id,
                "action": "Delete",
                "time stamp": str(self.run_timestamp),
                "deleted index": self.changed_index,
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        if self.redo:
            data = {
                "id": id,
                "action": "Redo",
                "time stamp": str(self.run_timestamp),
                "added index": self.changed_index,
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        if self.replace:
            data = {
                "id": id,
                "action": "Replace",
                "time stamp": str(self.run_timestamp),
                "replaced index": self.changed_index,
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        if self.clean:
            data = {
                "id": id,
                "action": "Clean",
                "time stamp": str(self.run_timestamp),
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        if self.load_prev: ##
            data = {
                "id": id,
                "action": "Before Load",
                "geometry": self.memory,
            }
        if self.load_after: ##
            data = {
                "id": id,
                "action": "After Load",
                "time stamp": str(self.run_timestamp),
                "loaded file": self.l_filename,
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        
        if self.save and not self.deleteAll:
            print(00)
            data = {
                "id": id,
                "action": "Save",
                "time stamp": str(self.run_timestamp),
                "saved file": self.s_filename,
                "geometry": self.memory,
                "archived object info": self.archive,
            }
            
        if self.save and self.deleteAll:
            print(11)
            data = {
                "id": id,
                "action": "Saved in delete-all mode",
                "time stamp": str(self.run_timestamp),
                "saved file": self.s_filename,
                "geometry": self.memory,
                "archived object info": self.archive,
            }

        if self.deleteAll and not self.save:
            print(22)
            data = {
                "id": id,
                "action": "Delete All",
                "time stamp": str(self.run_timestamp),
                "geometry": self.memory,
                "archived object info": self.archive,
            }
        if data:
            self.log.append(data)
            
        #autosave
        try:
            save_timestamp = datetime.datetime.now().strftime("%Y%m%d")
            filename = "log_{0}_{1}.json".format(self.user, save_timestamp)
            file_path = os.path.join(self.save_directory_log, filename)
            
            with open(file_path, "w") as f:
                json.dump(self.log, f, indent=4)
            
            print("log saved: {}".format(file_path))
        except Exception as ex:
            rs.MessageBox("Error log action: {}".format(str(ex)))

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
    a = round(float(cord[0]), 0)
    b = round(float(cord[1]), 0)
    c = round(float(cord[2]), 0)
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



#####################################################################


def subtract(pt_cord, rotation, seed, threshold, boundary, coords, simples, lines, shapes, times, clicks):
    dim = 15
    thk = 0.5625 + 0.525
    
    if rotation == 0:
        cur_len = len(coords)
        if boundary == None:
            boundary = rs.GetObject("Choose a boundary object")
        else:
            rs.MessageBox("There is a saved boundary object. \nContinue to build from it..")
            rs.ShowObject(boundary)
            rs.SelectObject(boundary)
            rs.Command("'_Zoom _Selected")
            rs.UnselectAllObjects()
        if coords != [] and any(rs.IsPointInSurface(boundary, point) for point in coords):
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
                        
                time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
                times.append(str(time))
                rs.DeleteObjects(sel_points)
            clicks.append(tuple(pt_cord))
        du = rs.SurfaceDomain(boundary, 0)
        u = du[1]/dim
        dv = rs.SurfaceDomain(boundary, 1)
        v = dv[1]/dim
        if coords == [] or pt_cord == None:
            pt_cord = rs.EvaluateSurface(boundary, u, v)
            
        threshold = int(max(u, v))
        
        if threshold > 4:
            rs.MessageBox("The volume is too big and I'm afraid of time-consuming. \nChange the threshold into 4.")
            threshold = 4
            
        rs.MessageBox("Working.. \nClick OK \nWait until the next instruction popped up. ")
        
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
            if [p_c, n_c] not in simples and [n_c, p_c] not in simples:
                ps = draw_mode(thk, dim, pt_cord, next_cord, seed)
                simples.append([p_c, n_c]) #list of sets
                coords.append(next_cord)
                shapes.append(ps)
                lines.append([tuple(pt_cord), tuple(next_cord)])
            subtract(next_cord, rotation + 1, seed, threshold, boundary, coords, simples, lines, shapes, times, clicks)
            
    if rotation == 0:
        rs.HideObject(boundary)
        #after_len = len(coords)
        #added_num = after_len - cur_len
        
        return boundary



def chunk(pt_cord, rotation, seed, threshold, coords, simples, lines, shapes, times, clicks):
    
    if rotation >= threshold:
        return
    dim = 15
    thk = 0.5625 + 0.525
    sel_points = []
    sel_cords = []
    
    if rotation == 0 and coords == []:
        pt_cord = rs.GetPoint("Select a new center: ")
        coords.append(tuple(pt_cord))
        
        if form.stop_flag: #break before save. 
            return
        time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        times.append(str(time))
    elif coords != []:
        for next_sel in coords: # mark saved points
            sel_points.append(rs.AddPoint(next_sel))
            sel_cords.append(tuple(next_sel))
        cur_len = len(coords)
        pt_cord = rs.GetPoint("Select a new center: ")
        while tuple(pt_cord) not in sel_cords:
            pt_cord = rs.GetPoint("Warning! Please choose from the points: ")
            if pt_cord == None:
                break
        clicks.append(tuple(pt_cord))
        #after_len = len(coords)
        #added_num = after_len - cur_len
        
        rs.DeleteObjects(sel_points)
        sel_cords = []
        if form.stop_flag:
            return
        time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        times.append(str(time))
        #times.extend([str(time)] * added_num)
        
    offset_cords = point_set(pt_cord, dim, thk)
    
    next_pts = []
    for next_cord in offset_cords:
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if [p_c , n_c] not in simples and [n_c, p_c] not in simples: #draw!
            simples.append([p_c , n_c])
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            coords.append(next_cord) #All coordinates become elements. sequence should be identical.
            lines.append([tuple(pt_cord), tuple(next_cord)])
    if rotation == 0:
        rs.Command("SelBlockInstance")
        rs.Command("'_Zoom _Selected")
        rs.UnselectAllObjects()
    chunk(pt_cord, rotation + 1, seed, threshold, coords, simples, lines, shapes, times, clicks)



def element(pt_cord, rotation, threshold, coords, simples, lines, shapes, three_set, center_mark, seed, times, clicks):
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
        while True:
            for point in coords:  #mark next centers
                translation = (point[0]-0.5, point[1]-0.5, point[2])
                rect = rs.AddRectangle(xy, 1, 1)
                rs.MoveObject(rect, translation)
                start_points.append(rs.AddPoint(point))
                temp_circle.append(rect)
                
            #pt_cord updated
            if rotation != 0 and rotation < 5:
                rs.MessageBox("Hi there! \nChoose next center every 3 point selection.")
            prev_cord = pt_cord
            pt_cord = rs.GetPoint("Select a new center: ") 
            
            if rotation == 0 and clicks == []:
                clicks.append(tuple(pt_cord))
                coords.append(tuple(pt_cord))
                time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
                times.append(str(time))
            else:
                clicks.append(tuple(pt_cord))
                while tuple(pt_cord) not in coords:
                    pt_cord = rs.GetPoint("Warning! Please choose from the points: ")
                    if pt_cord == None:
                        break
                #coords.append(tuple(pt_cord))
                time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
                times.append(str(time))
    
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
            temp_circle = []
            offset_cords = point_set(pt_cord, dim, thk)
            #for line in lines: #debug
            #    a, b = line
            #    rs.AddLine(a, b)
            for cord in offset_cords:  #mark next points
                if [tuple(pt_cord), tuple(cord)] not in lines and [tuple(cord), tuple(pt_cord)] not in lines:#### 
                    point = rs.AddPoint(cord)
                    next_points.append(point)
                    temp_circle.append(rs.AddCircle(point, 2))

            if not temp_circle:
                rs.MessageBox("Warning! Please choose a valid center point. Restarting selection.")
                continue
            else:
                break
                
        next_cord = rs.GetPoint("Select the next point: ")
        
        while tuple(next_cord) not in offset_cords:
            next_cord = rs.GetPoint("Warning! Please choose from the points 0: ")
            if pt_cord == None:
                break
        clicks.append(tuple(next_cord))
        rs.DeleteObjects(next_points)
        rs.DeleteObjects(temp_circle)
        if form.stop_flag:
            rs.DeleteObjects(center_mark)
            return
        time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        times.append(str(time))
            
        #start draw according to the mode
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if [p_c, n_c] not in simples and [n_c, p_c] not in simples: #draw!
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            simples.append([p_c, n_c])
            lines.append([tuple(pt_cord), tuple(next_cord)])
        if rotation == 0:
            rs.Command("SelBlockInstance")
            rs.Command("'_Zoom _Selected")
            rs.UnselectAllObjects()
            
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
                addition = rs.VectorAdd(point, pt_cord)
                #print("rule2", {tuple(pt_cord), tuple(addition)}, "lines", lines)
                if [tuple(pt_cord), tuple(addition)] not in lines and [tuple(addition), tuple(pt_cord)] not in lines:####
                    next_point = rs.AddPoint(rs.VectorAdd(point, pt1))
                    next_points.append(next_point)
                    next_coords.append(tuple(rs.VectorAdd(point, pt1)))
                    temp_circle.append(rs.AddCircle(next_point, 2))
                
        next_cord = rs.GetPoint("Select the next point: ")
        
        while tuple(next_cord) not in next_coords:
            next_cord = rs.GetPoint("Warning! Please choose from the points 1: ")
            if pt_cord == None:
                break
        clicks.append(tuple(next_cord))
        rs.DeleteObjects(next_points)
        rs.DeleteObjects(temp_circle)
        if form.stop_flag:
            rs.DeleteObjects(center_mark)
            return
        time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        times.append(str(time))
            
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
        if [p_c, n_c] not in simples and [n_c, p_c] not in simples : #draw!
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            simples.append([p_c, n_c])
            lines.append([tuple(pt_cord), tuple(next_cord)])
        
    elif rotation % 3 == 2: ############################################################2
        offset_cords = point_set(pt_cord, dim, thk)

        for set in three_set:
            for item in set:
                vec = rs.VectorAdd(item, pt_cord)
                if [tuple(pt_cord), tuple(vec)] not in lines and [tuple(vec), tuple(pt_cord)] not in lines:####

                    next_point = rs.AddPoint(rs.VectorAdd(item, pt_cord))
                    next_points.append(next_point)
                    next_coords.append(tuple(rs.VectorAdd(item, pt_cord)))
                    temp_circle.append(rs.AddCircle(next_point, 2))
                
        next_cord = rs.GetPoint("Select the next point: ")
        
        while tuple(next_cord) not in next_coords:
            next_cord = rs.GetPoint("Warning! Please choose from the points 2: ")
            if pt_cord == None:
                break
        clicks.append(tuple(next_cord))
        rs.DeleteObjects(next_points)
        rs.DeleteObjects(temp_circle)
        if form.stop_flag:
            rs.DeleteObjects(center_mark)
            return
        time = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        times.append(str(time))
        
        p_c = round_point(pt_cord)
        n_c = round_point(next_cord)
        if [p_c, n_c] not in simples and [n_c, p_c] not in simples: #draw!
            shapes.append(draw_mode(thk, dim, pt_cord, next_cord, seed))
            simples.append([p_c, n_c])
            lines.append([tuple(pt_cord), tuple(next_cord)])
        three_set=[]
        
    coords.append(tuple(next_cord))
    element(pt_cord, rotation + 1, threshold, coords, simples, lines, shapes, three_set, center_mark, seed, times, clicks)


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



