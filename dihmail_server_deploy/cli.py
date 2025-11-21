import sys
from db import init_db
from mail import ensure_user, new_alias_for_user, send_message, get_inbox, get_message_detail, decrypt_message_id
from address import build_address

USAGE = """dihmail CLI commands:\n  create-user <local>\n  alias <local>\n  send <sender_local> <recipient_address> <message>\n  inbox <local>\n  rawmsg <message_id>\n  decrypt <message_id>\n"""

def main(argv):
    if len(argv) < 2:
        print(USAGE)
        return
    cmd = argv[1]
    init_db()
    if cmd == "create-user":
        if len(argv) != 3:
            print("Usage: create-user <local>")
            return
        local = argv[2]
        ensure_user(local)
        print(f"Created/exists primary address: {build_address(local)}")
    elif cmd == "alias":
        if len(argv) != 3:
            print("Usage: alias <local>")
            return
        local = argv[2]
        addr = new_alias_for_user(local)
        print(f"New alias: {addr} -> primary {build_address(local)}")
    elif cmd == "send":
        if len(argv) < 5:
            print("Usage: send <sender_local> <recipient_address> <message>")
            return
        sender = argv[2]
        recipient = argv[3]
        message = " ".join(argv[4:])
        result = send_message(sender, recipient, message)
        print(f"Stored message id={result['message_id']} ciphertext={result['ciphertext']} key={result['key']}")
    elif cmd == "inbox":
        if len(argv) != 3:
            print("Usage: inbox <local>")
            return
        local = argv[2]
        msgs = get_inbox(local)
        if not msgs:
            print("Inbox empty")
            return
        for mid, sender, recipient, created in msgs:
            print(f"[{mid}] from={sender} at={created}")
    elif cmd == "rawmsg":
        if len(argv) != 3:
            print("Usage: rawmsg <message_id>")
            return
        mid = int(argv[2])
        detail = get_message_detail(mid)
        print(detail)
    elif cmd == "decrypt":
        if len(argv) != 3:
            print("Usage: decrypt <message_id>")
            return
        mid = int(argv[2])
        plaintext = decrypt_message_id(mid)
        print(f"Plaintext: {plaintext}")
    else:
        print(USAGE)

if __name__ == "__main__":
    main(sys.argv)
