#/bin/bash -f

#
# Witten by Kevin Inscoe (kevin.inscoe@gmail.com) to send email
# when Skywarn spotter activation is requested for the two forecast
# offices I spend time in: MLB and MRX
#
# For more info see https://kevininscoe.com/wiki/index.php/Weather
#

for WFO in 'mlb:FLZ041' 'mrx:TNZ012'
do
        export NWS_WFO_WZONE="${WFO}"
        python3 /home/Cahp_ei5q_e9Zeeye_kobah/bin/nws_spotter_info_statement.py
done
