import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import os, sys
import requests, json
import urllib

__addon__       = xbmcaddon.Addon(id='plugin.audio.hamishandandy')
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
__debugging__  = __addon__.getSetting('debug')

MODE_STREAM_PODCAST = 1

baseModeUrl = 'plugin://plugin.audio.hamishandandy/'
podcastUrl = baseModeUrl + '?mode=1'

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon('plugin.audio.hamishandandy')
pluginpath = addon.getAddonInfo('path')
vicon = os.path.join(pluginpath,'icon.png')
fanart = os.path.join(pluginpath,'fanart.jpg')

def getPodcasts():
    r = requests.get('http://mobile-backend.libsyn.com/app/items/app_id/handa/destination_id/97431/version/1.20.7/offset/0/size/30')
    json_obj = json.loads(r.text)
    return json_obj
                
def listPodcasts(folder=True, total=0):
	podcasts = getPodcasts()
        for podcast in podcasts:
            track_title = urllib.quote_plus(podcast['item_title'])
            track_artist = urllib.quote_plus(podcast['item_body'])
            item=xbmcgui.ListItem(urllib.unquote_plus(track_title) + " - " + urllib.unquote_plus(track_artist))
            item.setProperty( "IsPlayable", "true" )
            for stream in podcast['roles']:
                    if stream['role_tag'] == "mobile_audio_low":
                        track_url =  str(stream['content_url'])
            u = podcastUrl+'&track_url='+str(track_url)+'&track_title='+str(track_title)+"&track_artist="+str(track_artist)
            xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=False,totalItems=total)
	xbmcplugin.endOfDirectory(pluginhandle)

def playPodcast(track_url, track_title, track_artist):
    item = xbmcgui.ListItem(path=track_url )
    item.setProperty( "IsPlayable", "true" )    
    item.setInfo('music', {'title': urllib.unquote_plus(track_title), 'artist' : urllib.unquote_plus(track_artist)})
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if __debugging__ :
        xbmc.log(paramstring)
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
mode=None
try: mode=int(params["mode"])
except: pass
itemId=0
try: itemId=int(params["id"])
except: pass
name = None
try: name=urllib.unquote_plus(params["name"])
except: pass

if mode==None:
	listPodcasts()    
elif mode==MODE_STREAM_PODCAST :
	xbmc.log('PLAY PODCAST')
	playPodcast(params['track_url'], params['track_title'], params['track_artist'])
