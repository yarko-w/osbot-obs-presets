import obspython as obs
import socket
import struct

# ---------------------------------------------------------------
# CONFIGURATION
# Change HOST if OBSBOT Center is running on a different machine.
# Leave it as 127.0.0.1 if OBS and OBSBOT Center are on the same PC.
# PORT should stay as 8999 unless you have changed it in OBSBOT Center.
# ---------------------------------------------------------------
HOST = "127.0.0.1"
PORT = 8999

# These are populated from the script settings panel in OBS.
# You don't need to edit them here — type your scene names in the
# Scripts window after loading this file into OBS.
scene1 = ""
scene2 = ""
scene3 = ""


def build_osc_packet(address, arg1, arg2):
    # Builds a raw OSC message as bytes to send over UDP.
    # You don't need to edit this.
    def pad(data):
        return data + b'\x00' * ((4 - len(data) % 4) % 4)

    addr = pad(address.encode() + b'\x00')
    tag  = pad(b',ii\x00')
    args = struct.pack('>ii', arg1, arg2)
    return addr + tag + args


def trigger_preset(index):
    # Sends the OSC command to OBSBOT Center to recall a preset.
    # index 0 = Preset 1, index 1 = Preset 2, index 2 = Preset 3.
    # You don't need to edit this.
    packet = build_osc_packet('/OBSBOT/WebCam/Tiny/TriggerPreset', 0, index)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (HOST, PORT))
    sock.close()


def on_scene_change(event):
    # Fires every time the active scene changes in OBS.
    # Compares the new scene name against your three configured scenes
    # and triggers the matching preset.
    if event != obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        return
    source = obs.obs_frontend_get_current_scene()
    name = obs.obs_source_get_name(source)
    obs.obs_source_release(source)

    # ---------------------------------------------------------------
    # SCENE → PRESET MAPPING
    # If you prefer to hardcode your scene names instead of using the
    # settings panel, you can replace scene1/scene2/scene3 here with
    # plain strings. For example:
    #   if name == "Wide Shot":
    #       trigger_preset(0)
    #   elif name == "Close Up":
    #       trigger_preset(1)
    #   elif name == "Audience":
    #       trigger_preset(2)
    # ---------------------------------------------------------------
    if name == scene1:
        trigger_preset(0)
    elif name == scene2:
        trigger_preset(1)
    elif name == scene3:
        trigger_preset(2)


def script_description():
    return "Triggers OBSBOT Tiny SE presets when OBS scenes change."


def script_properties():
    # Defines the input fields shown in the OBS Scripts settings panel.
    # Change the label text (e.g. "Scene → Preset 1") if you want
    # different labels, but keep the keys "scene1", "scene2", "scene3".
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "scene1", "Scene → Preset 1", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "scene2", "Scene → Preset 2", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "scene3", "Scene → Preset 3", obs.OBS_TEXT_DEFAULT)
    return props


def script_update(settings):
    # Reads the scene names from the settings panel each time they change.
    # You don't need to edit this.
    global scene1, scene2, scene3
    scene1 = obs.obs_data_get_string(settings, "scene1")
    scene2 = obs.obs_data_get_string(settings, "scene2")
    scene3 = obs.obs_data_get_string(settings, "scene3")


def script_load(settings):
    # Registers the scene change listener when the script loads.
    obs.obs_frontend_add_event_callback(on_scene_change)


def script_unload():
    # Cleans up the listener when the script is removed or OBS closes.
    obs.obs_frontend_remove_event_callback(on_scene_change)
