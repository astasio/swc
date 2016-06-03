#!/usr/bin/env python

import os
import gio
import atk
import gtk
import cairo
import pango
import pangocairo
import Image
from cairo import ImageSurface

cx=gtk.Label("0")
#tmp="c:\\tmp\\" #WIN
tmp="/tmp/"  #LINUX
#try:   #WIN
#    os.system("mkdir "+tmp)
#except:
#    pass

def warning(message):
	msg=gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,"Inserisci il nome del file!")	
	msg.run()
	msg.destroy()

def control():
	if img1.get_pixbuf()==None or img2.get_pixbuf()==None or img3.get_pixbuf()==None:
		butt4.hide() 
	else:
  		butt4.show()   


def motion_cb(wid, context, x, y, time):
   context.drag_status(gtk.gdk.ACTION_COPY, time)
   return True

def drop_cb(wid, context, x, y, time):
   wid.drag_get_data(context, context.targets[-1], time)
   return True

def got_data_cb(widget, context, x, y, selection, target_type, timestamp):
	a = selection.data.strip('\r\n\x00').split("file://")[-1] #LINUX
  #  a = selection.data.strip('\r\n\x00').split("file:///")[-1] #WIN
	f=a.replace("%20"," ")
	resize(f,widget)
	context.finish(True, False, timestamp)

def resize(img,widget):
	def progress():
		name=img.split("/")[-1]
		im1=Image.open(tmp+name+"scaled.png")
		x=cx.get_text()	
		im2=im1.crop((int(x),0,int(x)+240,400))
		im2.save(tmp+name+"resized.jpg")
		widget.set_from_file(tmp+name+"resized.jpg")
		control()
		w.destroy()
	
	def move_rectangle():
		x=im.get_pointer()[0]		
		cr=im.window.cairo_create()
		cr.set_source_surface(sf)
		cr.paint()
		cr.set_source_rgba(0,0,0,1)
		cr.rectangle(x,0,240,400)	
		cr.stroke()	
		cx.set_text(str(x))
	
	im1=Image.open(img)
	a,b,c,d=im1.getbbox()
	x=(400*c)/d
	y=400
	im2=im1.resize((x,y),Image.ANTIALIAS)
	name=img.split("/")[-1]
	im2.save(tmp+name+"scaled.png")
	w=gtk.Window()
	w.set_size_request(x,y+30)
	w.set_resizable(False)
	w.set_title("Ritaglio Immagine..")
	vb=gtk.VBox()
	w.add(vb)
	im=gtk.DrawingArea()
	im.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON1_MOTION_MASK)
	vb.add(im)
	im.connect("motion-notify-event", lambda *w: move_rectangle())	
	im.connect("expose-event", lambda *w: move_rectangle())
	butt=gtk.Button("Ok")	
	butt.set_size_request(80,30)
	vb.add(butt)
	vb.set_child_packing(butt,expand=False,fill=False, padding=0,pack_type=gtk.PACK_END)
	butt.connect("clicked",lambda *w: progress())		
	w.show_all()
	sf=ImageSurface.create_from_png(tmp+name+"scaled.png")	

def salva():
	def saving():
		im1=img1.get_pixbuf()
		im1.save(tmp+"uno.png","png")
		im2=img2.get_pixbuf()
		im2.save(tmp+"due.png","png")
		im3=img3.get_pixbuf()        
		im3.save(tmp+"tre.png","png")
		im1=Image.open(tmp+"uno.png")
		im2=Image.open(tmp+"due.png")
		im3=Image.open(tmp+"tre.png")		
		image=im1.crop((0,0,720,400))	
		image.paste(im2,(240,0))
		image.paste(im3,(480,0))
		if (w3.get_filename()==None):
			warning("inserisci il nome del file!")
		else:
			f=w3.get_filename()        	
			image.save(f+".jpg")
			img1.clear()
			img2.clear()
			img3.clear()    
			control()
			w3.hide()

	w3=gtk.FileChooserDialog(title="Salva in..",parent=w,action=gtk.FILE_CHOOSER_ACTION_SAVE)
	w3.set_select_multiple(False)
	w3.show()
	butt=gtk.Button('salva Wallpaper')
	butt.show()
	w3.set_extra_widget(butt)
	butt.connect('clicked',lambda *w: saving())
        
w=gtk.Window()
w.set_resizable(False)
w.set_title('Samsung Wallpapers Creator 0.3 by Antonio Stasio :)')
w.set_size_request(720,500)
w.connect('destroy',gtk.main_quit)
w.show()

vbox=gtk.VBox()
w.add(vbox)
vbox.show()

lbl1=gtk.Label('Trascina le foto per la creazione del wallpaper')
vbox.add(lbl1)
vbox.set_child_packing(lbl1,expand=False,fill=False, padding=0,
                pack_type=gtk.PACK_START)
lbl1.show()

hbox=gtk.HBox()
vbox.add(hbox)
hbox.show()
hbox.set_homogeneous(True)

img1=gtk.Image()
hbox.add(img1)
hbox.set_child_packing(img1,expand=True,fill=True, padding=0,
                pack_type=gtk.PACK_START)
img1.drag_dest_set(0, [], 0)
img1.connect('drag_motion', motion_cb)
img1.connect('drag_drop', drop_cb)
img1.connect('drag_data_received', got_data_cb)
img1.show()

img2=gtk.Image()
hbox.add(img2)
hbox.set_child_packing(img2,expand=True,fill=True, padding=0,
                pack_type=gtk.PACK_START)
img2.drag_dest_set(0, [], 0)
img2.connect('drag_motion', motion_cb)
img2.connect('drag_drop', drop_cb)
img2.connect('drag_data_received', got_data_cb)
img2.show()

img3=gtk.Image()
hbox.add(img3)
hbox.set_child_packing(img3,expand=True,fill=True, padding=0,
                pack_type=gtk.PACK_START)
img3.drag_dest_set(0, [], 0)
img3.connect('drag_motion', motion_cb)
img3.connect('drag_drop', drop_cb)
img3.connect('drag_data_received', got_data_cb)
img3.show()

hbox1=gtk.HBox()
vbox.add(hbox1)
vbox.set_child_packing(hbox1,expand=False,fill=False, padding=0,
                pack_type=gtk.PACK_START)
hbox1.show()

butt4=gtk.Button('genera wallpaper')
vbox.add(butt4)
vbox.set_child_packing(butt4,expand=False,fill=False, padding=10,
                pack_type=gtk.PACK_START)
butt4.hide()
butt4.connect('clicked',lambda *w: salva())

gtk.main()

