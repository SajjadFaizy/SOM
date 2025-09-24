



# -------------- MUSS AUSFÜHRLICH AUSGEFÜLLT WERDEN -------------- #




# Supported data-types in MQTT
- strings
- Numbers (formated as strings)
- JSON (formated as string)
- XML (formated as string)

# Dictionary

**Broker:**
> MQTT sofware administrating the data transfers between publishers and subscribers (Mosquitto, EMQX, etc.)

**Host:**
> Physical or virtual device where the Broker is being executed (Server, Raspberry, etc.)

**Topic:**
> Named channel for organizing and transferring data between publishers and subscribers


# Mosquitto commands

**Initialize Mosquito:**
`sudo systemctl start mosquitto`

**Verify server status:**
`sudo systemctl status mosquitto`

**Enable Mosquitto to start automatically on boot:**
`sudo systemctl enable mosquitto`

**Initiate broker in "verbose" mode to see connection messages and real-time activity:**
`mosquitto -v`