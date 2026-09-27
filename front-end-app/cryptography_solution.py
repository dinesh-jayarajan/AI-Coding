from cryptography.fernet import Fernet


def encrdecr(keyval, textencr, textdecr):
    main_list = []
    fernet = Fernet(keyval)

    encr_bytes = textencr.encode() if isinstance(textencr, str) else textencr
    encrypted_text = fernet.encrypt(encr_bytes)
    main_list.append(encrypted_text)

    decr_bytes = textdecr.encode() if isinstance(textdecr, str) else textdecr
    decrypted_text = fernet.decrypt(decr_bytes)
    main_list.append(decrypted_text.decode())

    return main_list
