# OBSBOT Preset Script — Setup Guide

This script automatically moves your OBSBOT Tiny SE camera to a preset position whenever you switch scenes in OBS.

---

## What You Need

- A Windows 11 PC running OBS Studio
- OBSBOT Center installed and running
- Your OBSBOT Tiny SE camera connected via USB
- The script file: `obsbot_preset_script.py`
- Preset positions already saved in OBSBOT Center (up to 3)

---

## Step 1 — Install Python 3.12

OBS requires a specific version of Python to run scripts. Follow these steps carefully.

1. Open your web browser and go to: **https://www.python.org/downloads/**
2. Find **Python 3.12** in the list (do not use a newer version — OBS may not be compatible)
3. Click on **Python 3.12.x** to open its download page
4. Scroll down to the **Files** section at the bottom
5. Download **Windows installer (64-bit)**
6. Once downloaded, open the `.exe` file to start the installer
7. On the first screen, **tick the box that says "Add Python to PATH"** before clicking Install
8. Click **Install Now** and follow the prompts through to completion

---

## Step 2 — Find the Python Path

OBS needs to know the folder where Python was installed. To find it:

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

## Step 3 — Add the Python Path to OBS

1. Open **OBS Studio**
2. In the menu bar click **Tools → Scripts**
3. Click the **Python Settings** tab at the top of the Scripts window
4. In the **Python Install Path** field, paste the path you copied in Step 2
5. You should see a message saying **"Python loaded successfully"**
   - If it does not load, double check the path was copied correctly and that Python 3.12 is installed

---

## Step 4 — Add the Script to OBS

1. In the Scripts window, click the **Lua/Python Scripts** tab
2. Click the **+** button at the bottom left
3. Browse to wherever you saved `obsbot_preset.py` and select it
4. The script will appear in the list and load automatically

---

## Step 5 — Enter Your Scene Names

1. Click on `obsbot_preset.py` in the scripts list to select it
2. On the right side panel you will see fields labelled **Scene → Preset 1**, **Scene → Preset 2**, and so on
3. Type the name of your OBS scene next to the preset you want it to trigger

For example:

| Field | Scene Name You Type |
|---|---|
| Scene → Preset 1 | Wide Shot |
| Scene → Preset 2 | Podium |
| Scene → Preset 3 | Demo |

> **Important:** The scene name must match exactly as it appears in OBS, including capital letters and spaces. For example `Wide Shot` is not the same as `wide shot`.

> **Note:** You only need to fill in the slots you are using. Leave the rest blank.

---

## Step 6 — Test It

1. Make sure **OBSBOT Center** is open and your camera is connected
2. Switch to one of the scenes you configured in OBS
3. The camera should move to the matching preset position

If the camera does not move, check the following:
- OBSBOT Center is running in the background
- The scene name in the script settings matches exactly
- The preset positions have been saved in OBSBOT Center beforehand

---

## Preset Positions — Quick Reminder

Your OBSBOT Tiny SE supports **3 preset positions**. These are saved inside OBSBOT Center, not in this script. If you have not set them up yet:

1. Open **OBSBOT Center**
2. Manually move the camera to the position you want
3. Save it as Preset 1, 2, or 3 inside the app

The script then recalls those saved positions automatically when you switch scenes.
