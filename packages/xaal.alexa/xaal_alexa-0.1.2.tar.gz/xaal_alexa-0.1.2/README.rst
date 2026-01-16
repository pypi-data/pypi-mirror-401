xaal.alexa
==========
This package provides a xAAL gateway for all Alexa devices associated to an account. 
Right now, the gateway supports TTS. 


Install
=======
- Download the remote script: https://github.com/thorsten-gehrig/alexa-remote-control
- Edit / run the remote script
- Try the gateway: python -m xaal.alexa
- Edit the config file to add Alexa Echo devices (or Group) (find them w/ alexa-remote-control.sh -a)
  You can omit the address.
- re-run the gateway
- done


Notes
=====
The gateway provides a special Alexa (virtual) device called LastAlexa. This is the 
lattest used device. 


Usage
=====
You can trigger a xAAL scenario throught the xaal.fauxmo package. And use the LastAlexa
device to answer to the user throught the scenario.
