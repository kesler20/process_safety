from tkinter import *
from app.data_processing import DataProcessing

root = Tk()
root.title('Process Safety Gui')
root_height = 900
root_width = 700
root.geometry(f'{root_height}x{root_width}')
_id = 0
data = DataProcessing([])

canvas = Canvas(root, width=root_width - 50, height=root_height - 50,bg='white')
canvas.pack(pady=30)

gate_width, gate_height = 105, 120
and_gate = data.resize_image(gate_width,gate_height,'AND-gate.png')
or_gate =data.resize_image(gate_width,gate_height,'R.png')
transfer_gate = data.resize_image(gate_width,gate_height,'TRANSFER.png')
primary_gate = data.resize_image(gate_width,gate_height,'primary.PNG')
box = data.resize_image(gate_width,gate_height,'blue-box.png')

class MoveGate:
    def __init__(self, gate_id):
        self.gate_id = gate_id

        if gate_id == 1:
            self.gate_object = and_gate

        elif gate_id == 2:
            self.gate_object = or_gate

        elif gate_id == 3:
            self.gate_object = transfer_gate

        elif gate_id == 4:
            self.gate_object = primary_gate

        elif gate_id == 5:
            self.gate_object = box

        else:
            self.gate_object = and_gate

        global root
        global canvas
        global my_label
        global _id
        global data

        canvas.bind('<B1-Motion>', self._start_moving)
    
    def _start_moving(self,event):
        
        if self.gate_id == 1:
            operator = 'AND'
            filename = 'AND-gate.png'
        elif self.gate_id == 2:
            filename = 'R.png'
            operator = 'OR'
        elif self.gate_id == 3:
            filename = 'TRANSFER.png'
            operator = 'TRANSFER'
        elif self.gate_id == 4:
            operator = 'PRIMARY'
            filename = 'primary.PNG'
        elif self.gate_id == 5:
            filename = 'blue-box.png'
            operator = 'BOX'
            canvas.create_text(event.x,event.y,text=textbox_description.get(), tags=operator)
        
        self.gate_object = data.resize_image(gate_width,gate_height,filename)
        canvas.delete(operator)
        _id = canvas.create_image(event.x,event.y,image=self.gate_object)
        if self.gate_id == 5:
            canvas.create_text(event.x,event.y,text=textbox_description.get(), tags=operator)
        
        my_label.config(text=f'Object id :{_id}, x Coordinates :{event.x}, y Coordinates :{event.y}')

def get_gate(operator):

    global and_gate 
    global or_gate 
    global transfer_gate 
    global _id
    h = gate_height
    w = gate_width

    if operator == 'AND':
        _id = canvas.create_image(h,w, image=and_gate, tags=operator)
    elif operator == 'OR':
        _id = canvas.create_image(h,w, image=or_gate, tags=operator)
    elif operator == 'TRANSFER':
        _id = canvas.create_image(h,w, image=transfer_gate, tags=operator)
    elif operator == 'PRIMARY':
        _id = canvas.create_image(h,w, image=primary_gate, tags=operator)
    elif operator == 'BOX':
        _id = canvas.create_image(h,w, image=box, tags=operator)
        canvas.create_text(h,w,text=textbox_description.get(), tags=operator)

def make_line():
    global canvas
    global gate_height
    global data

    x1 = canvas.coords(object_to_move_from.get())[0]
    y1 = canvas.coords(object_to_move_from.get())[1]
    x2, y2 = data.from_string_comma_string_to_int(object_to_move_to.get())

    y1 -= gate_height/2
    y2 += gate_height/2

    canvas.create_line(x1,y1,x2,y2)

def AND():
    global movegate 

    movegate = MoveGate(1)

    get_gate('AND')

def OR():
    global movegate 
    
    movegate = MoveGate(2)

    
    get_gate('OR')

def TRANSFER():
    global movegate 
    
    movegate = MoveGate(3)
    
    get_gate('TRANSFER')

def BOX():
    global movegate 
    
    movegate = MoveGate(5)

    get_gate('BOX')

def PRIMARY():
    global movegate 
    
    movegate = MoveGate(4)

    get_gate('PRIMARY')

def move_obj():
    global movegate 

    _id = object_to_move_from.get()

    operator = object_to_move_from.get()
    get_gate(operator)

plotline_btn = Button(root, width=10, height=30, text='Make line', command=make_line)
plotline_btn.pack(side=LEFT, padx=20, pady=25)

plotline_btn = Button(root, width=10, height=30, text='GET AND', command=AND)
plotline_btn.pack(side=LEFT, padx=20, pady=25) 

plotline_btn = Button(root, width=10, height=30, text='GET OR', command=OR)
plotline_btn.pack(side=LEFT, padx=20, pady=25) 

plotline_btn = Button(root, width=10, height=30, text='GET TRANSFER', command=TRANSFER)
plotline_btn.pack(side=LEFT, padx=20, pady=25)

plotline_btn = Button(root, width=10, height=30, text='GET BOX', command=BOX)
plotline_btn.pack(side=LEFT, padx=20, pady=25)

plotline_btn = Button(root, width=10, height=30, text='GET PRIMARY', command=PRIMARY)
plotline_btn.pack(side=LEFT, padx=20, pady=25) 

plotline_btn = Button(root, width=10, height=30, text='MOVE GATE', command=move_obj)
plotline_btn.pack(side=LEFT, padx=20, pady=25) 

my_label = Label(root, text='')
my_label.pack(pady=20)

width = 40
object_to_move_from = Entry(root, width=width)
object_to_move_from.insert(0,'Enter id of objct you want to move from')
object_to_move_from.pack(side=RIGHT, padx=width + 10)

object_to_move_to = Entry(root, width=40)
object_to_move_to.insert(1,'Enter object to move to')
object_to_move_to.pack(side=RIGHT)

textbox_description = Entry(root, width=40)
textbox_description.insert(1,'Enter textbox description')
textbox_description.place(x=100, y=100)
textbox_description.pack()


root.mainloop()