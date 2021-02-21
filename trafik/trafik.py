# Skriv i terminalen: pip install requests
import pickle
import requests
import tkinter as tk
from tkinter import ttk, StringVar
import json

# här ska all stationer och stads förkortning vara för att kunna få information om.
stations_dict = {
'Karlstad':'Ks', 
'Arvika': 'Ar', 
"Bäckebron": "Bäb", 
"Charlottenberg":"Cg", 
"Edane":"En", 
"Fagerås":"Fgå",
"Frykåsen":"Frå",
"Filipstad":"Fid",
"Grums":"Gms",
"Högboda":"Hbd",
"Kil":"Kil",
"Kolsnäs":"Kns",
"Välsviken":"Kvä",
"Lene":"Len",
"Kristinehamn":"Khn",
"Lysvik":"Lyv",
"Nässundet":"Nd",
"Nykroppa":"Nka",
"Oleby":"Ol",
"Rottneros":"Rts",
}

API_KEY = 'aa916ca49ce741d5bc78df1302631bfd'
#PERSONLIG API-NYCKEL'

#den spara det man har sökt på sist
def getDepartures():
    with open('history.json', 'w') as f:

      #Hittar informationen som man har sökt på och vissar den i history.json
      json.dump(list(stations_dict.values()).index(stations_dict[stationer.get()]), f)
      
    """
    Hämtar data från Trafikverket med ett POST-anrop
    """

    request = f"""<REQUEST>
<LOGIN authenticationkey="c090545371474e5abe9f41f8a7c90dee" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationer.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd(07:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(12:00:00)" />
</AND>
</OR>
</AND>
</FILTER>
<INCLUDE>AdvertisedTrainIdent</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>TrackAtLocation</INCLUDE>
<INCLUDE>ToLocation</INCLUDE>
</QUERY>
</REQUEST>"""

#AdvertisedTrainIdent

    # Här sker själva anropet
    url = 'https://api.trafikinfo.trafikverket.se/v1.3/data.json'
    response = requests.post(url, data = request, headers = {'Content-Type': 'text/xml'}, )

    # Formatera svaret från servern som ett json-objekt
    response_json = json.loads(response.text)
    departures = response_json["RESPONSE"]['RESULT'][0]['TrainAnnouncement']

    # Töm svarsrutan
    stationer_text.delete(1.0,"end")

    # så här kan man bestämma hur information ska se ut
    for dep in departures:
        stationer_text.insert(1., '\n\n')
        stationer_text.insert(1., '\n------------------------------------⌡\n')   

        förkortning = dep['ToLocation'][0]['LocationName']
        stationer_text.insert(1., förkortning)
        stationer_text.insert(1., '\n--------------------\n')

        spår ="spår: " + dep['TrackAtLocation']
        stationer_text.insert(1., spår)
        stationer_text.insert(1., '\n--------------------\n')

        tågnummer ="tågnummer: " + dep['AdvertisedTrainIdent']
        stationer_text.insert(1., tågnummer)
        stationer_text.insert(1., '\n--------------------\n')

        datum= "datum och tid: " + dep['AdvertisedTimeAtLocation']
        stationer_text.insert(1., datum)
        stationer_text.insert(1., '\n⌠------------------------------------\n')
          
#----------------------


                                              #Design           
# Det grafiska gränssnittet
root = tk.Tk()
canvas = tk.Canvas(root, height=10000, width=10000)
canvas.configure(background='#e699ff')
canvas.pack()

# Knapp 
button=tk.Button(root, text='Hämta frukt', fg='#6B39CC', command = getDepartures)
button.place(relwidth=0.65, height=75, relx=0.28, rely=0.01)
button.configure(background='#282828')

# Combobox med stationer. Läser in alla "uppslagsord" från stations_dict

f = open ("history.json", "r")
data = int(json.loads(f.read()))
#
stationer = ttk.Combobox(canvas, state='readonly')
stationer['values'] = list(stations_dict.keys())
stationer.current(data)
stationer.place(relwidth=0.2, height=50, relx=0.04, rely=0.13)


# information man får när man söker på nånting 
stationer_text = tk.Text(canvas)
stationer_text.place(relx=0.25, rely=0.13, relwidth=0.7, relheight=0.7)
stationer_text.configure(background='#282828', fg='#ac00e6')


root.mainloop()