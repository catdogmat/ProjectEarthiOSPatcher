import ctypes

try:
    import customtkinter
    import threading
    from tkinter.filedialog import askopenfilename
    import os
    import zipfile
    import shutil
    import patcher
except ImportError:
    ctypes.windll.user32.MessageBoxW(0, "You need to install the required packages to run this program.", "Error", 1)
    exit(1)

try:
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, f"An error occurred while setting the appearance mode: {e}", "Error", 1)
    exit(1)

try:
    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("400x650")
    app.title("Project Earth Patcher")
except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, f"An error occurred while creating the window: {e}", "Error", 1)
    exit(1)

def cleanup():
    try:
        if os.path.exists('data/ipa.zip'):
            os.remove('data/ipa.zip')
        if os.path.exists('data/ipa.ipa'):
            os.remove('data/ipa.ipa')
        if shutil.os.path.exists('data/ipa'):
            shutil.rmtree('data/ipa')
        if shutil.os.path.exists('data'):
            shutil.rmtree('data')
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"An error occurred while cleaning up: {e}", "Error", 1)
        exit(1)

try:
    os.makedirs("data", exist_ok=True)
except Exception as e:
    cleanup()
    ctypes.windll.user32.MessageBoxW(0, f"An error occurred while creating the data directory: {e}", "Error", 1)
    exit(1)


def log(level, text, prefix):
    print(f"[{prefix}] {level}: {text}")
    textbox.configure(state="normal")
    textbox.insert("end", f"[{prefix}] {level}: {text}\n")
    textbox.configure(state="disabled")


def patch_sync():
    button.configure(state="disabled")
    ip = ip_entry.get()
    ip_entry.configure(state="disabled")
    if len(ip) > 27:
        log("ERROR", "IP too long!", "PATCHER")
        cleanup()
        ctypes.windll.user32.MessageBoxW(0, f"Please enter a valid IP!", "Error", 1)
        return
    log("INFO", f"Starting to patch with ip: {ip}", "PATCHER")
    filename = askopenfilename(title="Select the .ipa file", filetypes=[("IPA files", "*.ipa")])
    if filename == '':
        log("ERROR", "No file selected", "PATCHER")
        cleanup()
        ctypes.windll.user32.MessageBoxW(0, f"Please select a file!", "Error", 1)
        return
    shutil.copyfile(filename, "./data/ipa.zip")
    # extract the zip
    log("INFO", "Extracting the ipa", "PATCHER")
    with zipfile.ZipFile("./data/ipa.zip", 'r') as zip_ref:
        zip_ref.extractall("./data/ipa")
    # check payload
    if not patcher.hex_bytes_in_file("68747470733A2F2F6C6F6361746F722E6D6365736572762E6E6574", "./data/ipa/Payload/minecraftearthtf.app/minecraftearthtf"):
        log("INFO", "This file is encrypted!", "PATCHER")
        ctypes.windll.user32.MessageBoxW(0, f"This file is encrypted!", "Error", 1)
        cleanup()
        return
    else:
        log("INFO", "This file is not encrypted and ready to patch!", "PATCHER")
    # patch the file
    log("INFO", "Patching the file", "PATCHER")
    log("INFO", "Patching App Name", "PATCHER")
    patcher.patch_app_name()
    log("INFO", "Patched App Name", "PATCHER")
    log("INFO", "Removing DRM", "PATCHER")
    patcher.remove_drm()
    log("INFO", "Removed DRM", "PATCHER")
    log("INFO", "Removing Useless Files", "PATCHER")
    patcher.remove_useless_files()
    log("INFO", "Removed Useless Files", "PATCHER")
    log("INFO", "Patching IP", "PATCHER")
    patcher.patch_ip(ip)
    log("INFO", "Patched IP", "PATCHER")
    log("INFO", "Patching Sunset Time", "PATCHER")
    patcher.patch_sunset_time()
    log("INFO", "Patched Sunset Time", "PATCHER")
    # zip the file
    log("INFO", "Zipping the file", "PATCHER")
    patcher.zip_folder_contents("./data/ipa/", "./ipa.ipa")
    log("INFO", "Zipped the file", "PATCHER")
    log("INFO", "Patching done!", "PATCHER")
    cleanup()

def patch():
    # Patch method in a new thread
    threading.Thread(target=patch_sync).start()

patcher_label = customtkinter.CTkLabel(master=app, text="Project Earth Patcher", font=("Arial", 20))
patcher_label.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

# IP Textbox
ip_label = customtkinter.CTkLabel(master=app, text="Server IP:")
ip_label.place(relx=0.2, rely=0.4, anchor=customtkinter.CENTER)

ip_entry = customtkinter.CTkEntry(master=app)
ip_entry.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Patch!", command=patch)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

textbox = customtkinter.CTkTextbox(app, state="disabled")
textbox.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)


app.mainloop()