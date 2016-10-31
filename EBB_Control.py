# Tkinter python 2.7, or tkinter 3.x
# pip install pyserial

from Tkinter import *
import sys
import glob
import serial
import time

# Defaults
h_step_value_default = "8100"
v_step_value_default = "5500"
timeformove = "1000" # eventually make config option

# instance tkinter
master = Tk()
poll = False
master.title("DigiTiler Control")
sendsteps =  StringVar()
sendstring =  StringVar()
strVersion =  StringVar()

global comPort
global comPortName
global serial_list

comPort = serial.Serial()

comPortName = ""

######## CODE ###########
# we need to put in top so buttons know

running = True

# So we can break out of loop if motors go off course
def start():
    """Enable scanning by setting the global flag to True."""
    global running
    running = True

def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False

def motors_disable():
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    comPort.write('EM,0,0\r'.encode('ascii'))  # disable motors


def h_step_forward():
    #comPortName = ser_list_ports_entry.get()
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    sendsteps = h_step_entry.get()
    print(sendsteps)
    sendstring = 'sm,'+timeformove+','+sendsteps+',0,\r'
    print(sendstring)
    comPort.write(sendstring.encode('ascii'))
    strVersion = comPort.readline()

    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

    #Update OFFSETS
    offset = int(str(h_offset_entry.get()))
    #print("offset is: "+str(offset))
    hstep = int(h_step_entry.get())
    offset = offset + hstep
    h_offset_entry.delete(0, END)
    h_offset_entry.insert(0,str(offset))
    #serialPort.close()

def h_step_back():
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    sendsteps = h_step_entry.get()
    sendsteps = "-"+sendsteps
    print(sendsteps)
    sendstring = 'sm,' + timeformove + ',' + sendsteps + ',0,\r'
    print(sendstring)
    comPort.write(sendstring.encode('ascii'))
    strVersion = comPort.readline()
    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

    # Update OFFSETS
    offset = int(str(h_offset_entry.get()))
    # print("offset is: "+str(offset))
    hstep = int(h_step_entry.get()) * -1
    offset = offset + hstep
    h_offset_entry.delete(0, END)
    h_offset_entry.insert(0, str(offset))


def v_step_forward():
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    sendsteps = v_step_entry.get()
    print(sendsteps)
    sendstring = 'sm,' + timeformove + ',0,' + sendsteps + '\r'
    print(sendstring)
    comPort.write(sendstring.encode('ascii'))
    strVersion = comPort.readline()
    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

    # Update OFFSETS
    offset = int(str(v_offset_entry.get()))
    # print("offset is: "+str(offset))
    vstep = int(v_step_entry.get())
    offset = offset + vstep
    v_offset_entry.delete(0, END)
    v_offset_entry.insert(0, str(offset))

def v_step_back():
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    sendsteps = v_step_entry.get()
    sendsteps = "-"+sendsteps
    print(sendsteps)
    sendstring = 'sm,' + timeformove + ',0,' + sendsteps + '\r'
    print(sendstring)
    comPort.write(sendstring.encode('ascii'))
    strVersion = comPort.readline()
    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

    # Update OFFSETS
    offset = int(str(v_offset_entry.get()))
    # print("offset is: "+str(offset))
    vstep = int(v_step_entry.get()) *-1
    offset = offset + vstep
    v_offset_entry.delete(0, END)
    v_offset_entry.insert(0, str(offset))

def h_step_default():
    pass

def v_step_default():
    pass

#Offsets
def h_offset_center():

    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    # set opposite to go back; that is *-1
    hmove = int(h_offset_entry.get()) * -1
    sendsteps = str(hmove)
    print(sendsteps)
    sendstring = 'sm,' + timeformove + ',' + sendsteps + ',0,\r'
    print(sendstring)
    comPort.write(sendstring.encode('ascii'))
    strVersion = comPort.readline()

    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

    # Update OFFSETS
    h_offset_entry.delete(0, END)
    h_offset_entry.insert(0, str("0"))
    # serialPort.close()

def h_offset_fullleft():
    pass

def h_offset_fullright():
    pass

def v_offset_center():
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    # set opposite to go back; that is *-1
    vmove = int(v_offset_entry.get()) * -1
    sendsteps = str(vmove)
    print(sendsteps)
    sendstring = 'sm,' + timeformove + ',0,' + sendsteps + '\r'
    print(sendstring)
    comPort.write(sendstring.encode('ascii'))
    strVersion = comPort.readline()

    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

    # Update OFFSETS
    v_offset_entry.delete(0, END)
    v_offset_entry.insert(0, str("0"))

def v_offset_top():
    pass

def v_offset_bottom():
    pass

### DATA ###

def save_current_values():
    pass

### SERIEAL ####

def list_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    serial_list = []

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            serial_list.append(port)
        except (OSError, serial.SerialException):
            pass
    #ser_list_ports_entry.insert(20,serial_list)
    # Put into optionmenu
    dropdownvariable = StringVar()
    dropdownvariable.set(serial_list[0])

    ser_list_optionmenu = OptionMenu(master, dropdownvariable, *serial_list, command=ser_port_selected)
    ser_list_optionmenu.grid(row=1, column=2, padx=4, pady=4)

    return serial_list

def ser_test_port():
    # we now get through optionmenu
    #comPortName = ser_list_ports_entry.get()
    print("comPortName is: "+comPortName)
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    comPort.write('v\r'.encode('ascii'))
    strVersion = comPort.readline()
    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)
    #serialPort.close()

def shutter_fire():
    comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!
    #S2,27500,5,10,50
    comCMD = 'S2,24000,5\r'.encode('ascii')
    #comCMD = 'TP/r'.encode('ascii')
    print(comCMD)
    comPort.write(comCMD)
    time.sleep(.300)
    comCMD = 'S2,12000,5\r'.encode('ascii')
    comPort.write(comCMD)
    strVersion = comPort.readline()

    status_entry.delete(0, END)
    status_entry.insert(50, strVersion)

##########################
### RUN ROUTINES TILING
###########################
def run_RLBT():

    if running==True:

        # Put camera in start position
        # fire first shutter
        # Open PORT
        comPort = serial.Serial(comPortName, timeout=1.0)  # 1 second timeout!

        # defaults
        hstep = h_step_entry.get()
        vstep = v_step_entry.get()
        htiles = int(h_tiles_entry.get())
        vtiles = int(v_tiles_entry.get())

        for r in range(1,(htiles+1)):

            # Set depending on odd/even row
            vmove = 0  # default

            # If we're at the beginning fire shutter
            if (r==1):
                time.sleep(1.5)
                # fire shutter
                comCMD = 'S2,24000,5\r'.encode('ascii')
                print(comCMD)
                comPort.write(comCMD)
                time.sleep(.450)
                comCMD = 'S2,12000,5\r'.encode('ascii')
                comPort.write(comCMD)
                strVersion = comPort.readline()
                status_entry.delete(0, END)
                status_entry.insert(50, strVersion)

            # Now go through vertical tiles
            for c in range(1, (vtiles)):

                if (r % 2 ==0): # EVEN row
                    # HORIZONTAL
                    hmove = str(int(hstep) * -1)  # reverse
                    # If we're at the end of an odd row, we need to move up at end
                    # VERTICAL
                    if (c==vtiles-1):
                        vmove = vstep
                else: # ODD row
                    # HORIZONTAL
                    hmove = hstep # forward
                    # If we're at the end of an EVEN row, we need to move up at beginning
                    # but not if we're at end row
                    # VERTICAL
                    if (c==vtiles-1):
                        vmove = vstep

                print("vmove is: " + str(vmove))

                # If we're at the end of an odd row, we need to move up at end

                # WE HAVE A HORIZONTAL MOVE
                if (int(hmove)!=0):
                    print('Tile '+str(r)+','+str(c)+' H-Step='+str(hmove))
                    # Move
                    time.sleep(.250) # wait quarter of a second
                    sendstring = 'sm,' + timeformove + ',' + str(hmove) + ',0,\r'
                    comPort.write(sendstring.encode('ascii'))
                    strVersion = comPort.readline()
                    status_entry.delete(0, END)
                    status_entry.insert(50, strVersion)

                    # fire shutter
                    time.sleep(1.5)
                    comCMD = 'S2,24000,5\r'.encode('ascii')
                    print(comCMD)
                    comPort.write(comCMD)
                    time.sleep(.4500)
                    comCMD = 'S2,12000,5\r'.encode('ascii')
                    comPort.write(comCMD)
                    strVersion = comPort.readline()
                    status_entry.delete(0, END)
                    status_entry.insert(50, strVersion)
                    time.sleep(.250)  # wait quarter of a second

                    # check for stop VERTICAL
                    master.update()
                    if (running == False):
                        break

                # WE HAVE A VERTICAL MOVE
                if (int(vmove)!=0):
                    # not last one
                    print('Tile ' + str(r) + ',' + str(c) + ' V-Step=' + str(vmove))
                    # Move
                    time.sleep(.250)  # wait quarter of a second
                    sendstring = 'sm,' + timeformove + ',0,' + str(vmove) + '\r'
                    comPort.write(sendstring.encode('ascii'))
                    strVersion = comPort.readline()
                    status_entry.delete(0, END)
                    status_entry.insert(50, strVersion)

                # If we've made a vertical move Let's fire shutter
                    time.sleep(1.5)
                    # fire shutter
                    comCMD = 'S2,24000,5\r'.encode('ascii')
                    print(comCMD)
                    comPort.write(comCMD)
                    time.sleep(.450)
                    comCMD = 'S2,12000,5\r'.encode('ascii')
                    comPort.write(comCMD)
                    strVersion = comPort.readline()
                    status_entry.delete(0, END)
                    status_entry.insert(50, strVersion)
                    time.sleep(.250)  # wait quarter of a second

                vmove = 0  # back to default

                # 1 would be 1 second .05 half second

            # check for stop HORIZONTAL
            master.update()
            if (running == False):
                break

        status_entry.delete(0,END)
        status_entry.insert(0,"Tiling done")


def ser_port_selected(selected_opt):
    global comPortName
    comPortName = selected_opt
    print("comPortName is now: "+comPortName)

def quit():
    if comPort is not None:
        try:
            comPort.close()
        except serial.SerialException:
            pass

    global master
    quit()

#########################

onrow = 1

# First Row Group description
ser_list_ports_btn = Button(master, text='Get Serial Ports', command=list_serial_ports)
ser_test_port_btn = Button(master, text='Test Port', command=ser_test_port)

ser_list_ports_btn.grid(row=onrow, column=1,padx=4,pady=4)
# optionmenu in column 2 !
ser_test_port_btn.grid(row=onrow, column=3,padx=4,pady=4)

# List Serial Ports
onrow+=1

onrow+=1

# Group description
g1_lbl = Label(master, text="Tile distance values for steppers")
g1_lbl.grid(row=onrow, column=2)
onrow+=1

# H-Step
h_step_lbl = Label(master, text="H Step")
h_step_entry = Entry(master)
h_step_entry.insert(10,h_step_value_default)
h_step_btn_forward = Button(master, text='Forward', command=h_step_forward)
h_step_btn_back = Button(master, text='Back', command=h_step_back)
h_step_btn_default = Button(master, text='Default', command=h_step_default)

h_step_lbl.grid(row=onrow,column=1,padx=4,pady=4)
h_step_entry.grid(row=onrow, column=2,padx=4,pady=4)
h_step_btn_forward.grid(row=onrow, column=3,padx=4,pady=4)
h_step_btn_back.grid(row=onrow, column=4,padx=4,pady=4)
h_step_btn_default.grid(row=onrow, column=5,padx=4,pady=4)

onrow+=1

# V-Step
v_step_lbl = Label(master, text="V Step")
v_step_entry = Entry(master)
v_step_entry.insert(10,v_step_value_default)
v_step_btn_forward = Button(master, text='Up', command=v_step_forward)
v_step_btn_back = Button(master, text='Down', command=v_step_back)
v_step_btn_default = Button(master, text='Default', command=v_step_default)

v_step_lbl.grid(row=onrow,column=1,padx=4,pady=4)
v_step_entry.grid(row=onrow, column=2,padx=4,pady=4)
v_step_btn_forward.grid(row=onrow, column=3,padx=4,pady=4)
v_step_btn_back.grid(row=onrow, column=4,padx=4,pady=4)
v_step_btn_default.grid(row=onrow, column=5,padx=4,pady=4)

onrow+=1

# Second Row Group description
g2_lbl = Label(master, text="Widths (H and V) in Tiles")
g2_lbl.grid(row=onrow, column=2)
onrow+=1

# H Tiles
h_tiles_lbl = Label(master, text="H Tiles")
h_tiles_entry = Entry(master)
h_tiles_entry.insert(2,"7")

h_tiles_lbl.grid(row=onrow,column=1,padx=4,pady=4)
h_tiles_entry.grid(row=onrow, column=2,padx=4,pady=4)

onrow+=1

# V Tiles
v_tiles_lbl = Label(master, text="V Tiles")
v_tiles_entry = Entry(master)
v_tiles_entry.insert(2,"7")

v_tiles_lbl.grid(row=onrow,column=1,padx=4,pady=4)
v_tiles_entry.grid(row=onrow, column=2,padx=4,pady=4)

onrow+=1

############## OFFSETS ####################
# Group description
g1_lbl = Label(master, text="Current Offsets")
g1_lbl.grid(row=onrow, column=2)
onrow+=1

# H-Offset
h_offset_lbl = Label(master, text="H Offset")
h_offset_entry = Entry(master)
h_offset_entry.insert(0,"0")
h_offset_btn_center = Button(master, text='Center', command=h_offset_center)
h_offset_btn_fullleft = Button(master, text='<< Left', command=h_offset_fullleft)
h_offset_btn_fullright = Button(master, text='Right >>', command=h_offset_fullright)

h_offset_lbl.grid(row=onrow,column=1,padx=4,pady=4)
h_offset_entry.grid(row=onrow, column=2,padx=4,pady=4)
h_offset_btn_center.grid(row=onrow, column=3,padx=4,pady=4)
h_offset_btn_fullleft.grid(row=onrow, column=4,padx=4,pady=4)
h_offset_btn_fullright.grid(row=onrow, column=5,padx=4,pady=4)

onrow+=1

# V-Offset
v_offset_lbl = Label(master, text="V Offset")
v_offset_entry = Entry(master)
v_offset_entry.insert(0,"0")
v_offset_btn_center = Button(master, text='Center', command=v_offset_center)
v_offset_btn_top = Button(master, text='<< Top', command=v_offset_top)
v_offset_btn_bottom = Button(master, text='Bottom >>', command=v_offset_bottom)

v_offset_lbl.grid(row=onrow,column=1,padx=4,pady=4)
v_offset_entry.grid(row=onrow, column=2,padx=4,pady=4)
v_offset_btn_center.grid(row=onrow, column=3,padx=4,pady=4)
v_offset_btn_top.grid(row=onrow, column=4,padx=4,pady=4)
v_offset_btn_bottom.grid(row=onrow, column=5,padx=4,pady=4)

onrow+=1

### RUN ROUTINES ####
run_RLBT_btn = Button(master, text='Run R-L-B-T', command=run_RLBT)
run_LRTB_btn = Button(master, text='Run L-R-T-B')
stop_btn = Button(master,text='STOP!',command=stop)
motors_disable_btn = Button(master,text='Motors Disable',command=motors_disable)
shutter_fire_btn = Button(master,text='Fire Shutter',command=shutter_fire)

run_RLBT_btn.grid(row=onrow,column=1,padx=4,pady=4,sticky=W+E+N+S)
run_LRTB_btn.grid(row=onrow,column=2,padx=4,pady=4,sticky=W+E+N+S)
stop_btn.grid(row=onrow,column=3,padx=4,pady=4,sticky=W+E+N+S)
motors_disable_btn.grid(row=onrow,column=4,padx=4,pady=4,sticky=W+E+N+S)
shutter_fire_btn.grid(row=onrow,column=5,padx=4,pady=4,sticky=W+E+N+S)

onrow+=1

### STATUS ###
status_entry = Entry(master)
status_entry.grid(row=onrow,column=0,columnspan=6,padx=4,pady=4,sticky=W+E+N+S)
status_entry.insert(50,"Status...")

onrow+=1

# Final Buttons
# 3rd Row, column 0 and 1

Button(master, text='Save Current Values', command=save_current_values).grid(row=onrow, column=1, sticky=W, padx=10, pady=4)
Button(master, text='Quit', command=quit).grid(row=onrow, column=2, sticky=W, padx=10, pady=4)

# Pack


mainloop( )