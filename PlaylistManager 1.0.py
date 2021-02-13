import webbrowser
import json
import os

#########################################################
# Ville Lindberg "Ohjelmoinnin perusteet"- harjoitustyö #
#########################################################

#metodeita millä playlist dataa käsitellään, tiedoston muokkausta, lukemista yms.
def viewAllPlaylists(playlistdata): #metodi joka vastaa listojen tarkatelusta: Valmis
    print("")
    if(len(playlistdata)!=0):
        for plist in playlistdata:
            print(plist)
    else:
        print("Yhtään soittolistaa ei löytynyt: Syötä tyhjä poistuaksesi\n")

def deletePlaylist(playlist,playlistdata):
    print("")
    try:
        playlistdata.pop(playlist)
        writeToJson(playlistdata)
        print("Soittolista poistettu")
    except:
        print("Soittolistaa ei ole!")

def viewSongs(playlist,playlistdata): #Näyttää kaikki listalla olevat kappaleet: Valmis
    try:
        print("")
        print("Listalla '"+playlist+"' on kappaleet: ")
        for indexofsongs,songs in enumerate(playlistdata[playlist]):
            for keys in playlistdata[playlist][indexofsongs]:
                print(keys)
        return True
    except:
        print("Jokin meni pieleen!")
        return False

def deleteSong(song,playlist,playlistdata): #Poistaa nimen perusteellaa listalta kappaleen: Valmis
    print("")
    for indexofsongs,songs in enumerate(playlistdata[playlist]):
        for keys in playlistdata[playlist][indexofsongs]:
            if(keys==song):
                print(str(keys)+" Poistettu!")
                playlistdata[playlist].pop(indexofsongs)
    writeToJson(data)

def addSongToPlaylist(playlist,songname,songid,playlistdata): #Lisää yhden kappaleen soittolistalle ja kirjoittaa sen jsoniin: Valmis
    print("")
    tempdict={}
    tempdict[songname]=songid
    playlistdata[playlist].append(tempdict)
    writeToJson(playlistdata)
    print(songname+" lisätty!")

def createPlayList(listname,data): #Luo tyhjän soittolistan: Valmis
    print("")
    data[listname]=[]
    print("Soittolista: "+listname+" luotu")
    writeToJson(data)

def urlConstructor(playlist,playlistdata): #Raketaa listojen pohjalta urlin joka voidaan avata: Valmis
    try:
        url="http://www.youtube.com/watch_videos?video_ids="
        for indexofsongs,songs in enumerate(playlistdata[playlist]): #{x[],y[],z[]}
            for songid in playlistdata[playlist][indexofsongs]: #indexi [x,y,z]
                url=url+str(playlistdata[playlist][indexofsongs][songid]+",")#{k,n}
        url=url[0:len(url)-1] #poistetaan viimeinen pilkku
        return url
    except:
        print("Syötit nimen väärin!")

def urlOpener(url): #Valmis
    try:
        webbrowser.open(url,new=2)
    except:
        print("Soittolistaa ei voitu avata!")

#datan lukeminen,kirjoittaminen sekä tyhjän tiedoston teko: Valmiita ja toimivia
def jsonLoad():
    try:
        with open("playlists.json","r") as jf:
            #print("Reading datafile")
            return json.load(jf)
    except:
        createEmptyJson()

def createEmptyJson():
    with open("playlists.json","w") as jf:
        jf.write(json.dumps({}))
    print("Empty datafile created")

def writeToJson(data):
        with open("playlists.json","w") as jf:
            jf.write(json.dumps(data))
    
#komentorivihallintaa
def menu1(data):
    viewAllPlaylists(data)
    print("")
    chosenplaylist=input("Valitse tarkasteltava soittolista -> ")
    ulos=True
    while(ulos):
        if viewSongs(chosenplaylist,data):
            print("")
            chosenoption=input("1. Poista jokin kappale, 2. Lisää kappale, 3. Poista nykyinen soittolista, 4. Poistu -> ")
            if chosenoption == "1":
                deleteSong(input("Syötä poistettavan kappaleen nimi -> "),chosenplaylist,data)
                writeToJson(data)
            elif chosenoption=="2":
                addSongToPlaylist(chosenplaylist,input("Syötä uuden kappaleen nimi -> "),input("Syötä uuden kappaleen videoID (Youtube urlissa oleva 'watch?v=' jälkeinen koodi) -> "),data)
            elif chosenoption=="3":
                deletePlaylist(chosenplaylist,data)
                ulos=False
            elif chosenoption=="4":
                break
            else:
                continue
        else:
            break
    
def menu2(data):
    print("")
    viewAllPlaylists(data)
    print("")
    chosenplaylist=input("Valitse toistettava soittolista: ")
    urlOpener(urlConstructor(chosenplaylist,data))

#Tähä tulee koko soittolist tiedoston data
data=jsonLoad()
if(data==None): #varmistetaan ettei tiedoston luonnin jälkeen dataksi jää None
    data=jsonLoad() #näin data saa arvoksi tyhjän hajautustaulun
print("Käyttäjätilivapaa Youtube playlistmanager")
while(True):
    userinput=input("1.Tarkastele/muokkaa soittolistoja, 2. Toista soittolista, 3. Luo tyhjä soittolista tai  4. Poistu -> ")
    if(userinput=="1"):
        menu1(data)
    elif(userinput=="2"):
        menu2(data)
        data=jsonLoad()
    elif userinput =="3":
        createPlayList(input("Syötä uuden soittolistan nimi -> "),data)
        data=jsonLoad()
    elif(userinput=="4"):
        print("Ohjelma sulkeutuu...")
        break
    else:
        continue