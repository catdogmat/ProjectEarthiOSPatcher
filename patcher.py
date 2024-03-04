import os
import shutil
import zipfile

def ascii_to_hex(input_string):
    if len(input_string) < 27:
        input_string = input_string.ljust(27, '\x00')
    hex_string = input_string.encode().hex()
    return hex_string

def replace_bytes_in_file(file_path, offset, search_bytes, replace_bytes):
    with open(file_path, 'rb+') as file:
        file.seek(offset)

        # Read the content at the specified offset
        data = file.read(len(search_bytes))

        # Check if the bytes at the specified offset match the search_bytes
        if data == search_bytes:
            # Move the file pointer back to the beginning of the replacement area
            file.seek(offset)

            # Replace the bytes with the new ones
            file.write(replace_bytes)
        else:
            pass

def replace_hex_bytes(file_path, search_hex, replace_hex):
    with open(file_path, 'rb') as file:
        file_data = file.read()

    search_bytes = bytes.fromhex(search_hex)
    replace_bytes = bytes.fromhex(replace_hex)

    # Search for the hex bytes in the file data
    index = file_data.find(search_bytes)

    if index != -1:
        # Replace the hex bytes with the new hex bytes
        file_data = file_data[:index] + replace_bytes + file_data[index + len(search_bytes):]

        with open(file_path, 'wb') as file:
            file.write(file_data)
    else:
        pass

def rmtree(directory_path):
    # Use tqdm to create the progress bar
    # Walk through the directory and remove each item
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
    # Finally, remove the top-level directory itself
    os.rmdir(directory_path)

def hex_bytes_in_file(hex_sequence, file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        hex_content = ''.join([format(byte, '02x') for byte in file_content])

        hex_sequence = hex_sequence.lower()  # Convert to lowercase for case-insensitive comparison
        return hex_sequence in hex_content

def zip_folder_contents(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=arcname)

def patch_app_name():
    plistlocation = './data/ipa/Payload/minecraftearthtf.app/Info.plist'
    plist = open(plistlocation, mode='r')
    plistdata = plist.readlines()
    plistmod = []
    for x in plistdata:
        y = x
        if 'Minecraft Earth' in x:
            y = y.replace('Minecraft Earth', 'Project Earth')
        plistmod.append(y)
    plist.close()
    plist = open(plistlocation, mode='w')
    plist.writelines(plistmod)
    plist.close()

def remove_drm():
    codesig = './data/ipa/Payload/minecraftearthtf.app/_CodeSignature/'
    scinfo = './data/ipa/Payload/minecraftearthtf.app/SC_Info/'
    if os.path.exists(codesig):
        print("Removing Code Signature")
        rmtree(codesig)
        print("Removed Code Signature")
    if os.path.exists(scinfo):
        print("Removing SC_Info")
        rmtree(scinfo)
        print("Removed SC_Info")

def remove_useless_files():
    rndfile = './data/ipa/Payload/minecraftearthtf.app/Zachary@Cracks( 14.4 ok)'
    if os.path.exists(rndfile):
        os.remove(rndfile)

def patch_ip(ip):
    ipinhex = ascii_to_hex(ip)
    oldip = '68747470733A2F2F6C6F6361746F722E6D6365736572762E6E6574'
    replace_hex_bytes('./data/ipa/Payload/minecraftearthtf.app/minecraftearthtf', oldip, ipinhex)

def patch_sunset_time():
    file_path = './data/ipa/Payload/minecraftearthtf.app/minecraftearthtf'
    offset = 0x1129080
    search_bytes = b'\xEA\x05\x00\x54'
    replace_bytes = b'\xE1\x05\x00\x54'

    replace_bytes_in_file(file_path, offset, search_bytes, replace_bytes)