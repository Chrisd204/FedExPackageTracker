import requests as Req
import xmltodict as xmld
import json
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os

BackgroundImage = 'background.jpg path'
FedexLogoImage = 'logo.png path'
mastericon = 'mastericon.png path'

Key = ''
Password = ''
AccountNumber = ''
MeterNumber = ''


def events_topleft_label(package):
   try:
      status_event = package['http://fedex.com/ws/track/v18:EventDescription']
      status_desc = package['http://fedex.com/ws/track/v18:StatusExceptionDescription']
      time_stamp = package['http://fedex.com/ws/track/v18:Timestamp']
      
      FinalString = "Status Event:%s\nDescription:%s\nEvent Time: %s\n"  % (status_event,status_desc,time_stamp)
   except:
      FinalString = "EvT1:To report a bug, please use the information below.\n\nYour Company IT Dept\n600 Jackson St.\nPrinceton, NJ 08542\nHelp Desk Line 888.999.1000"
      try:
         recent_event = package['http://fedex.com/ws/track/v18:EventDescription']
         time_stamp2 = package['http://fedex.com/ws/track/v18:Timestamp']

         FinalString = "Recent Event: %s\nEvent Time: %s" % (recent_event,time_stamp2)
      except:
         FinalString = "EvT2:To report a bug, please use the information below.\n\nYour Company IT Dept\n600 Jackson St.\nPrinceton, NJ 08542\nHelp Desk Line 888.999.1000"

   return FinalString


def execption_topleft_label(package):
   try:
      status_desc = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:Events']['http://fedex.com/ws/track/v18:EventDescription']

      FinalString = "Recent Event: %s" % (status_desc)
   except:
      track_number = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:TrackingNumber']
   
      FinalString = "ExT1:Tracking number "+track_number+" cannot be found. Please check the number or contact the sender.If you believe you have recieved this notification in error, please resubmit, or contact FedEx directly.\n\n\n1.800.GoFedEx 1.800.463.3339."

   return FinalString

def events_bottomleft_label(package):
   try:
      current_city = package['http://fedex.com/ws/track/v18:Address']['http://fedex.com/ws/track/v18:City']
      current_state = package['http://fedex.com/ws/track/v18:Address']['http://fedex.com/ws/track/v18:StateOrProvinceCode']
      current_zipcode = package['http://fedex.com/ws/track/v18:Address']['http://fedex.com/ws/track/v18:PostalCode']

      FinalString = "Current Location:%s,%s %s\n\n\n1.800.GoFedEx 1.800.463.3339."% (current_city,current_state,current_zipcode)
      
   except:

      FinalString = "EvB1:Looks like we couldn't find the current location of this package. Please contact sender to make sure this shipment has not been canceled."+ render4

   return FinalString
def execption_botttomleft_label(package):
   try:
      service_type = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:OperatingCompanyOrCarrierDescription']
      shipper_city = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:ShipperAddress']['http://fedex.com/ws/track/v18:City']
      shipper_state = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:ShipperAddress']['http://fedex.com/ws/track/v18:StateOrProvinceCode']
      dest_city = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:DestinationAddress']['http://fedex.com/ws/track/v18:City']
      dest_state = package['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:DestinationAddress']['http://fedex.com/ws/track/v18:StateOrProvinceCode']
      
      FinalString = "Services Rendered: %s\nShipper: %s,%s\nDestination: %s,%s\n" % (service_type,shipper_city,shipper_state,dest_city,dest_state)
   except:
      FinalString = "ExB1:To report a bug, please use the information below.\n\nYour Company IT Dept\n600 Jackson St.\nPrinceton, NJ 08542\nHelp Desk Line 888.999.1000"
   
   return FinalString



def inquiry_number(return_):
    try:
      os.system('clear')
      url = "https://ws.fedex.com:443/web-services" # Will need to change out Url depending on production vs testing.
      headers = {"content-type" : "application/soap+xml"}
      body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://fedex.com/ws/track/v18">
         <soapenv:Header/>
         <soapenv:Body>
            <TrackRequest>
               <WebAuthenticationDetail>
                  <UserCredential>
                     <Key>"""+Key+"""</Key>
                     <Password>"""+Password+"""</Password>
                  </UserCredential>
               </WebAuthenticationDetail>
               <ClientDetail>
                  <AccountNumber>"""+AccountNumber+"""</AccountNumber>
                  <MeterNumber>"""+MeterNumber+"""</MeterNumber>
               </ClientDetail>
               <TransactionDetail>
                  <CustomerTransactionId>Track_v18</CustomerTransactionId>
               </TransactionDetail>
               <Version>
                  <ServiceId>trck</ServiceId>
                  <Major>18</Major>
                  <Intermediate>0</Intermediate>
                  <Minor>0</Minor>
               </Version>
               <SelectionDetails>
                  <PackageIdentifier>
                     <Type>TRACKING_NUMBER_OR_DOORTAG</Type>
                     <Value>"""+return_+"""</Value>
                  </PackageIdentifier>
               </SelectionDetails>
               <ProcessingOptions>INCLUDE_DETAILED_SCANS</ProcessingOptions>
            </TrackRequest>
         </soapenv:Body>
      </soapenv:Envelope>
      """
      response = Req.post(url, data = body, headers = headers)
      PreData = response.content
      RealData = json.loads(json.dumps(xmld.parse(PreData,process_namespaces=True)))
      Data = RealData['http://schemas.xmlsoap.org/soap/envelope/:Envelope']['http://schemas.xmlsoap.org/soap/envelope/:Body']['http://fedex.com/ws/track/v18:TrackReply']['http://fedex.com/ws/track/v18:CompletedTrackDetails']['http://fedex.com/ws/track/v18:TrackDetails']['http://fedex.com/ws/track/v18:Events']
      current_event = Data[0]
      #print(len(current_event))
      #print(current_event)
      topleft_label['text'] = events_topleft_label(current_event)
      bottomleft_label['text'] = events_bottomleft_label(current_event)
      
    except: #Most recent location
      response = Req.post(url, data = body, headers = headers)
      PreData = response.content
      RealData = json.loads(json.dumps(xmld.parse(PreData,process_namespaces=True)))
      topleft_label['text'] = execption_topleft_label(RealData)
      bottomleft_label['text'] = execption_botttomleft_label(RealData)
      #print(RealData)


# *** pre defined height and width *****

win_height = 500
win_width = 800
# *** Setup for Gui ****
root = tk.Tk()
root.resizable(0,0)
root.geometry('{0}x{1}'.format(win_width,win_height))
root.title("Package Tracker")


canvas = tk.Canvas(root, height=win_height, width=win_width)
canvas.pack()

top_banner = tk.Label(canvas, text="Beta Version 1.0", bg="#fe9209", foreground="white",bd=1)
top_banner.pack(side='top',fill='both')

bottom_banner = tk.Label(canvas, text="Package Tracker: Written by Chris Durham : Powered by FedEx Web Services", bg="#ff3300", foreground="white",bd=1)
bottom_banner.pack(side='bottom',fill='both')

load = Image.open(BackgroundImage)
render = ImageTk.PhotoImage(load) #changed from TK
img = tk.Label(canvas, image=render)
img.pack()

frame = tk.Frame(root, bg='#4d0066', bd=4)
frame.place(relx=0.5, rely=0.06, relwidth=0.75, relheight=0.10, anchor='n') #fills frameapt-get install python3-pil python3-pil.imagetk

right_frame = tk.Frame(root, bd=4, bg='#ffffff')
right_frame.place(relx=0.62, rely=0.40, relwidth=0.29, relheight=0.32, anchor='w')

entry = tk.Entry(frame, font=('Linux Hint', 18))
entry.place(relwidth=0.68, relheight=1)


button = tk.Button(frame,text= "Track Package",font=('Lucida Fax Demibold', 17), bg='#ff3300',justify='center',command=lambda: inquiry_number(entry.get()))
button.place(relx=0.7,relheight=1, relwidth=0.3)


topleft_frame = tk.Frame(root, bg='#4d0066', bd=5)
topleft_frame.place(relx=0.03, rely=0.20, relwidth=0.52, relheight=0.30, anchor='nw')

topleft_label = tk.Label(topleft_frame, font=('Linux Hint', 12), anchor='nw', justify='left', bd=2, wraplength=400)
topleft_label.place(relwidth=1, relheight=1)


bottomleft_frame = tk.Frame(root, bg='#4d0066', bd=5)
bottomleft_frame.place(relx=0.03, rely=0.55, relwidth=0.52, relheight=0.32, anchor='nw')

bottomleft_label = tk.Label(bottomleft_frame, font=('Linux Hint', 12), anchor='nw', justify='left', bd=2, wraplength=400)
bottomleft_label.place(relwidth=1, relheight=1)

load2 = Image.open(FedexLogoImage).resize((225,205))
render2 = ImageTk.PhotoImage(load2) #changed from TK
img2 = tk.Label(right_frame, image=render2)
img2.pack()

load3 = Image.open(mastericon).resize((225,205))
render3 = ImageTk.PhotoImage(load3) 

root.iconphoto(False,render3)
root.mainloop()