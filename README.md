# YT2Grayjay
Simple Scripts to convert youtube History to grayjay history
Update: Now added a Playlist conversion from Freetube to Grayjay. YT is not palnned (use the plugin for that)

We have now 3 of these.  
YTTakeout2Grayjay converts a Google Takeoutfile  
YTWatchmarker2Grayjay converts a exported Watchmarker DB   
FTPlay2Grayjay.py converts a freetube Playlists.db   

What is Watchmarker? - https://github.com/sniklaus/youtube-watchmarker?tab=readme-ov-file  

Another Project does make a full import for Freetube, you may wanna check that one out too.
https://github.com/sixthkrum/newpipe-to-grayjay-export

##Requirements
You need python and a takeout of your youtube history with history set to json format.


## Howto
Download the py script

### YTTakeout2Grayjay
extract watch.history.json from takeoutzip to working directory (in this example we use d:\python as our working directory)
adjust path in the script if using a different one.

run it.

### YTWatchmarker2Grayjay
export the Databasefile (its usually named date.database) renameit to watchmaker.database 
and put it into the working directory (same as with the other script)
run it

### FTPlay2Grayjay.py
export the Databasefile (its usually named freetube-playlists-date.db) renameit to freetube-playlists.db 
and put it into the working directory (same as with the other script)
run it

### To Grayjay
upload grayjay.zip to your phone
import "from grayjay export"
skip everything EXCEPT "import stores - yes, import history - yes"

## Disclaimer
Warning if you have a lot of history set your screentime timeout to max so it doesnt go to sleep during import
it can take a minute

testet with an unholy amount of entrys

Notice, because youtubes JSON does not include duration/watchtime i set a placeholder value that should make it watched no matter what.
Priamry use is to use the watched filter 
