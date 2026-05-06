# OBSBOT Preset Script — Setup Guide

This script automatically moves your OBSBOT Tiny SE camera to a preset position whenever you switch scenes in OBS.

---

## What You Need

- A Windows 11 PC running OBS Studio
- OBSBOT Center installed and running
- Your OBSBOT Tiny SE camera connected via USB
- The script file: `obsbot_preset.py`
- Preset positions already saved in OBSBOT Center (up to 3)

---

## Step 1 — Enable OSC in OBSBOT Center

This is the most important step. The script will not work unless OSC is turned on inside OBSBOT Center.

1. Open **OBSBOT Center**
2. Click the **Settings** icon (cog symbol)
3. Look for an **OSC** or **External Control** section
4. Turn the OSC toggle **ON** if there is the option
5. Confirm the Connection is `UDP`, the Host IP is set to `127.0.0.1` and the port is `16284` (these are the defaults)
6. Leave OBSBOT Center running in the background — closing it stops OSC

---

## Step 2 — Install Python 3.12

OBS requires a specific version of Python to run scripts.

1. Open your web browser and go to: **https://www.python.org/downloads/**
2. Find **Python 3.12** in the list (do not use a newer version — OBS may not be compatible)
3. Click on **Python 3.12.x** to open its download page
4. Scroll down to the **Files** section at the bottom
5. Download **Windows installer (64-bit)**
6. Once downloaded, open the `.exe` file to start the installer
7. On the first screen, **tick the box that says "Add Python to PATH"** before clicking Install
8. Click **Install Now** and follow the prompts through to completion

---

## Step 3 — Find the Python Path

OBS needs to know the folder where Python was installed.

1. Click the **Start** button and search for **Command Prompt**, then open it
2. Type the following and press Enter:

```
python -c "import sys; print(sys.prefix)"
```

3. You will see a path printed, for example:

```
C:\Users\YourName\AppData\Local\Programs\Python\Python312
```

4. **Copy that entire path** — you will need it in the next step

---

## Step 4 — Add the Python Path to OBS

1. Open **OBS Studio**
2. In the menu bar click **Tools → Scripts**
3. Click the **Python Settings** tab at the top of the Scripts window
4. In the **Python Install Path** field, paste the path you copied in Step 3
5. You should see a message saying **"Python loaded successfully"**

---

## Step 5 — Add the Script to OBS

1. In the Scripts window, click the **Lua/Python Scripts** tab
2. Click the **+** button at the bottom left
3. Browse to wherever you saved `obsbot_preset.py` and select it
4. The script will appear in the list and load automatically

---

## Step 6 — Enter Your Scene Names

1. Click on `obsbot_preset.py` in the scripts list to select it
2. On the right side panel you will see fields labelled **Scene → Preset 1**, **Scene → Preset 2**, and **Scene → Preset 3**
3. Type the name of your OBS scene next to the preset you want it to trigger

For example:

| Field | Scene Name You Type |
|---|---|
| Scene → Preset 1 | Wide Shot |
| Scene → Preset 2 | Speaker |
| Scene → Preset 3 | Audience |

> **Important:** The scene name must match exactly as it appears in OBS, including capital letters and spaces. For example `Wide Shot` is not the same as `wide shot`.

---

## Step 7 — Test It

The script settings panel includes **three test buttons** so you can confirm OSC is working before going live:

1. Make sure OBSBOT Center is open with OSC enabled
2. Click **Test Preset 1** in the script settings
3. The camera should move to Preset 1 immediately

If the camera moves, you are good — switch between your configured scenes and the camera will follow.

If it does not move, see the troubleshooting section below.

---

## Troubleshooting

### Open the log file

The script writes a log of everything it does. To open it:

1. Press **Windows + R**, type `%TEMP%`, press Enter
2. Find the file **`obsbot_preset.log`**
3. Open it with Notepad

The log will show whether the OSC commands are being sent successfully and whether scene changes are being detected.

### Camera does not move when testing

Check the following in order:
- Is **OBSBOT Center** open? (it must be running, not just installed)
- Is **OSC enabled** inside OBSBOT Center settings?
- Is the camera connected and visible inside OBSBOT Center?
- Have the **3 preset positions been saved** inside OBSBOT Center?
- Is the port set to **16284** in both the script and OBSBOT Center?

### Scene change does not trigger a preset

- Click the script in the OBS Scripts list and check the scene name fields are filled in
- Open the log file and look for `Scene changed to: '...'` — does the name match exactly?
- Capital letters and spaces matter

### Click the Reconnect button

If OBSBOT Center was started after OBS, click **Reconnect to OBSBOT** in the script settings to re-establish the connection.

---

## Preset Positions — Quick Reminder

Your OBSBOT Tiny SE supports **3 preset positions**. These are saved inside OBSBOT Center, not in this script. If you have not set them up yet:

1. Open **OBSBOT Center**
2. Manually move the camera to the position you want
3. Save it as Preset 1, 2, or 3 inside the app

The script then recalls those saved positions automatically when you switch scenes.
