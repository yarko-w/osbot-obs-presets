import obspython as obs
import socket
import struct
import logging
import os

# ---------------------------------------------------------------
# CONFIGURATION
# Change HOST if OBSBOT Center is running on a different machine.
# Leave it as 127.0.0.1 if OBS and OBSBOT Center are on the same PC.
# PORT is the OSC port that OBSBOT Center listens on.
# Default is 16284 — only change if you have changed it inside
# the OBSBOT Center OSC settings.
# ---------------------------------------------------------------
HOST = "127.0.0.1"
PORT = 16284

# ---------------------------------------------------------------
# LOGGING
# Logs are written to obsbot_preset.log in the system temp folder.
# On Windows you can open it by typing %TEMP% into Explorer.
# ---------------------------------------------------------------
log_path = os.path.join(os.environ.get("TEMP", os.getcwd()), "obsbot_preset.log")
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

# These are populated from the script settings panel in OBS.
# You don't need to edit them here — type your scene names in the
# Scripts window after loading this file into OBS.
scene1 = ""
scene2 = ""
scene3 = ""

# Module-level UDP socket reused across calls. You don't need to edit this.
sock = None


def build_osc_packet(address, *args):
    # Builds a raw OSC message as bytes to send over UDP.
    # Accepts an arbitrary number of integer arguments.
    # You don't need to edit this.
    def pad_string(s):
        b = s.encode() + b'\x00'
        b += b'\x00' * ((4 - len(b) % 4) % 4)
        return b

    addr_bytes = pad_string(address)
    type_tag = ',' + 'i' * len(args)
    tag_bytes = pad_string(type_tag)
    arg_bytes = b''.join(struct.pack('>i', a) for a in args)
    return addr_bytes + tag_bytes + arg_bytes


def send_osc(address, *args):
    # Sends an OSC message over UDP to OBSBOT Center.
    # You don't need to edit this.
    global sock
    try:
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        packet = build_osc_packet(address, *args)
        sock.sendto(packet, (HOST, PORT))
        log.debug(f"Sent OSC: {address} args={args} ({len(packet)} bytes) to {HOST}:{PORT}")
        return True
    except Exception as e:
        log.error(f"Failed to send OSC {address}: {e}")
        return False


def connect_to_obsbot():
    # Sends the Connected handshake to OBSBOT Center.
    # OBSBOT Center requires this before it will accept other commands.
    # You don't need to edit this.
    log.info("Sending Connected handshake to OBSBOT Center")
    send_osc('/OBSBOT/WebCam/General/Connected', 1)


def disconnect_from_obsbot():
    # Tells OBSBOT Center we are stopping. Polite cleanup.
    # You don't need to edit this.
    log.info("Sending Disconnected message to OBSBOT Center")
    send_osc('/OBSBOT/WebCam/General/Disconnected', 1)


def trigger_preset(index):
    # Sends the OSC command to OBSBOT Center to recall a preset.
    # index 0 = Preset 1, index 1 = Preset 2, index 2 = Preset 3.
    # You don't need to edit this.
    if send_osc('/OBSBOT/WebCam/Tiny/TriggerPreset', 0, index):
        log.info(f"Preset {index + 1} triggered")
    else:
        log.error(f"Preset {index + 1} failed to send")


def on_scene_change(event):
    # Fires every time the active scene changes in OBS.
    # Compares the new scene name against your three configured scenes
    # and triggers the matching preset.
    if event != obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        return

    source = obs.obs_frontend_get_current_scene()
    name = obs.obs_source_get_name(source)
    obs.obs_source_release(source)

    log.debug(f"Scene changed to: '{name}'")
    log.debug(f"Configured — P1: '{scene1}' | P2: '{scene2}' | P3: '{scene3}'")

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
        log.info(f"Matched Preset 1 for scene '{name}'")
        trigger_preset(0)
    elif name == scene2:
        log.info(f"Matched Preset 2 for scene '{name}'")
        trigger_preset(1)
    elif name == scene3:
        log.info(f"Matched Preset 3 for scene '{name}'")
        trigger_preset(2)
    else:
        log.debug(f"No preset match for scene '{name}' — no action taken")


def script_description():
    return ("Triggers OBSBOT Tiny SE presets when OBS scenes change.\n"
            "OBSBOT Center must be running with OSC enabled in its settings.")


def script_properties():
    # Defines the input fields shown in the OBS Scripts settings panel.
    # Change the label text (e.g. "Scene → Preset 1") if you want
    # different labels, but keep the keys "scene1", "scene2", "scene3".
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "scene1", "Scene → Preset 1", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "scene2", "Scene → Preset 2", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "scene3", "Scene → Preset 3", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "test1", "Test Preset 1", lambda p, prop: trigger_preset(0))
    obs.obs_properties_add_button(props, "test2", "Test Preset 2", lambda p, prop: trigger_preset(1))
    obs.obs_properties_add_button(props, "test3", "Test Preset 3", lambda p, prop: trigger_preset(2))
    obs.obs_properties_add_button(props, "reconnect", "Reconnect to OBSBOT", lambda p, prop: connect_to_obsbot())
    return props


def script_update(settings):
    # Reads the scene names from the settings panel each time they change.
    # You don't need to edit this.
    global scene1, scene2, scene3
    scene1 = obs.obs_data_get_string(settings, "scene1")
    scene2 = obs.obs_data_get_string(settings, "scene2")
    scene3 = obs.obs_data_get_string(settings, "scene3")
    log.info(f"Settings updated — P1: '{scene1}' | P2: '{scene2}' | P3: '{scene3}'")


def script_load(settings):
    # Registers the scene change listener and connects to OBSBOT Center.
    log.info("=" * 60)
    log.info("OBSBOT Preset script loaded")
    log.info(f"Log file: {log_path}")
    log.info(f"Target: {HOST}:{PORT}")
    obs.obs_frontend_add_event_callback(on_scene_change)
    connect_to_obsbot()


def script_unload():
    # Cleans up the listener and notifies OBSBOT Center we are leaving.
    log.info("Script unloading")
    disconnect_from_obsbot()
    obs.obs_frontend_remove_event_callback(on_scene_change)
    global sock
    if sock:
        sock.close()
        sock = None
