#/bin/bash

#
# Witten my Kevin Inscoe (kevin@inscoe.org) to send email
# when Skywarn spotter activation is requested
#

for WFO in MLB MRX
do
	echo "HWO statement for $WFO..."
	echo " "
	URL="https://forecast.weather.gov/product.php?site=NWS&issuedby=`echo $WFO`&product=HWO&format=txt&version=1&glossary=0"
# SPOTTER INFORMATION STATEMENT
	#curl -s "$URL" | html2text | grep -i -A 4 "Spotter activation" 
	#curl -s "$URL" | html2text | grep -i -A 7 "SPOTTER INFORMATION STATEMENT" | sed -e 's/\$\$//g'
	curl -s "$URL" | html2text | grep -i -A 10 "SPOTTER INFORMATION STATEMENT" | sed -e '/=========/q'
	echo " "
	echo "For full outlook click on $URL"
	echo " "
done
