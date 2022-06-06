import os 
import base64
import getpass
import smtplib, ssl 
import subprocess
import platform
from time import sleep
from cryptography.fernet import Fernet
from stat import S_IREAD

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

try:
    runningOS = platform.system()
    assert runningOS == "Linux", "This script can be used only in Linux"
except AssertionError as err:
    print(err)
    exit()

if __name__ != "__main__":
    exit()

SEC_KEY = None
#Colors for the interface
LOCK_COLOR = '\033[91m'
DESC_COLOR = '\033[94m'
FULL_COLOR = '\033[93m'
CLEAR_COLOR = '\033[0m'

def create_Sec_Key():
    global SEC_KEY
    pathToKey = os.environ.get('HOME') + '/.sec'
    if not os.path.exists(pathToKey):
        os.mkdir(pathToKey)
    try:
        with open(pathToKey + '/my_key.key', 'rb') as key_file:
            SEC_KEY = key_file.read()
    except FileNotFoundError:
        SEC_KEY = Fernet.generate_key()
        with open(pathToKey + '/my_key.key', 'wb') as key_file:
            key_file.write(SEC_KEY)
            os.chmod(key_file.name, S_IREAD)
        #subprocess.run(["chmod", "-w", pathToKey + '/my_key.key'])
        #subprocess.run(["chmod", "go-r", pathToKey + '/my_key.key'])

create_Sec_Key()

#Sets an interface for the script
print(f""" {LOCK_COLOR}
                __________
                |        |
                |        |
                |        |
        ________|________|__________
        |                          |
        |                          |
        |            * *           |
        |          *     *         |
        |           *   *          |
        |           *   *          |       
        |          *     *         |                 
        |         * * * * *        |
        |                          |
        |                          |
        |__________________________|
{CLEAR_COLOR}
{DESC_COLOR}
==============================================
    KEEP YOUR MESSAGES AND FILES SAFE
==============================================
{CLEAR_COLOR}
{FULL_COLOR}
""")

#Encrypts the message
def encrypt(message):
    return Fernet(SEC_KEY).encrypt(message)
    
#Decrypts the message
def decrypt(chipher):
    return Fernet(SEC_KEY).decrypt(chipher)

#Sends encrypted message by email
def send_Message_By_Email(sender, password, reciever, message):
    try:
        port = 465
        context = ssl.create_default_context()
        print("Sending email.....")
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, reciever, message)
    except:
        raise

#Sends encrypted file by email
def send_File_By_Email(sender, password, reciever, subject, body, file):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    #Se abre el archivo
    attachmente = open(file,'rb')
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachmente.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={file}")
    msg.attach(part)
    msg = msg.as_string()

    #Se envia el correo
    try:
        port = 465
        context = ssl.create_default_context()
        print("Sending email.....")
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, reciever, msg)
    except:
        raise
  
opcion = None
try:
    opcion = int(input("""Choose the option you want
    1. Encrypt message
    2. Decrypt message
    3. Encrypt file
    4. Decrypt file
    5. Exit program\n>"""))
except ValueError:
    print("Invalid option")

if opcion == 1:
    text = bytes(input("Enter the message you want to encrypt: "), 'UTF-8')
    encryptedMessage = encrypt(text)
    print('-'*50," Encrypted message ", '-'*50)
    print(str(encryptedMessage).replace("b'", '').replace('\'', ''))
    sleep(2)

    #Ask if the message is going to be saved to a file
    choice = input("\nWould you like to save your encrypted message to a file (Yes/No) ")
    if choice == "Yes" or choice == "yes" or choice == "Y" or choice == "y":
        fileName = None 
        while True:
            fileName = input("Enter the name of the file or path in which you want to save the message: ")
            #Valida que no se haya dejado el nombre el archivo en blanco
            if not fileName.isspace() and not len(fileName) == 0:
                break
        try:
            with open(fileName, "wb") as file:
                file.write(encryptedMessage)
                os.chmod(file.name, S_IREAD)
                print("File created succesfully")
                sleep(2)
        except:
            print("Sorry, an error ocurred while creating the file")
    
    #Ask if the message is to be sent my email
    choice = input("\nDo you need to send your encrypted message by email (Yes/No) ")
    if choice == "Yes" or choice == "yes" or choice == "Y" or choice == "y":
        print("\nIMPORTANT !!! ONLY GMAIL ACCOUNTS CAN BE USED AS THE SENDER EMAIL")
        print("YOU MUST ACTIVATE THE ACCESS FOR LESS SECURE APPS ON THE SENDER EMAIL !!! OR ELSE IT WON'T WORK")
        sleep(3)
        #Data for the email
        sender = input("\n\tSender email address: ")
        password = getpass.getpass("\tPassword: ", stream=None)
        reciever = input("\tReciever email address: ")
        subject = "Subject: " + input("\tSubject: ") + "\n\n"
        messageToSend = subject + encryptedMessage
        try:
            send_Message_By_Email(sender, password, reciever, messageToSend)
            print("\t\tMessage has been sent !!")
            sleep(2)
        except smtplib.SMTPAuthenticationError:
            print("An authentication error ocurred, please make sure to enter the right information or enable the option for less secure apps")
        except smtplib.SMTPException:
            print("An error ocurred trying to send the email, please make sure you are using a correct gmail account")


elif opcion == 2:
    text = bytes(input("Enter the message you want to decrypt: "), 'UTF-8')
    print('-'*50, " Decrypted message", '-'*50)
    print(str(decrypt(text)).replace("b'", '').replace('\'', ''))
    #.replace("b'", '').replace('\'', '')
    sleep(2)

elif opcion == 3:
    file = input("Enter the path or the name of the file you want to encrypt: ")
    fileEncrypted = None 
    try:
        with open(file, "rb") as f:
            textInFile = f.read()
            fileEncrypted = encrypt(textInFile)

        with open(file, "wb") as f:
            f.write(fileEncrypted)
        #Se tiene que modificar el archivo para que sea de solo lectura
        #Y solo el creador del archivo puede leer el contenido encriptado
        subprocess.run(["chmod", "ug-w", file])
        subprocess.run(["chmod", "go-r", file])
        print("File has been encrypted")
        sleep(2)

        #Se le pregunta al usuario si necesita enviar el archivo encriptado por correo
        choice = input("\nDo you need to send the encrypted file by email (Yes/No): ")
        if choice == "Yes" or choice == "yes" or choice == "Y" or choice == "y":
            print("\nIMPORTANT !!! ONLY GMAIL ACCOUNTS CAN BE USED AS THE SENDER EMAIL")
            print("YOU MUST ACTIVATE THE ACCESS FOR LESS SECURE APPS ON THE SENDER EMAIL !!! OR ELSE IT WON'T WORK")
            sender = input("\n\tSENDER EMAIL ADDRESS: ")
            password = getpass.getpass("\tPASSWORD: ", stream=None)
            reciever = input("\tRECIEVER EMAIL ADDRESS: ")
            subject = input("\tSUBJECT: ")
            body = input("\tBODY: ")
            try:
                send_File_By_Email(sender, password, reciever, subject, body, file)
                print("\t\tFile has been sent !!")
                sleep(2)
            except smtplib.SMTPAuthenticationError:
                print("An authentication error ocurred, please make sure to enter the right information of enable the option for less secure apps")
            except smtplib.SMTPException:
                print("An error ocurred trying to send the email, please make sure you are using a correct gmail account")
            except Exception as ex:
                print(str(ex))

            
    except FileNotFoundError:
        print("The File does not exist or is not located in this directory")
        
elif opcion == 4:
    file = input("Enter the path or the name of the file you want to decrypt: ")
    fileDecrypted = None 
    try:
        with open(file, "rb") as f:
            textInFile = f.read()
            fileDecrypted = decrypt(textInFile)
            #Se tiene que volver a poner el archivo para lectura y escritura
            #Y todos lo pueden volver a leer
            subprocess.run(["chmod", "ug+w", file])
            subprocess.run(["chmod", "go+r", file])

        with open(file, "wb") as f:
            f.write(fileDecrypted)
        
        print("File has been decrypted")
        sleep(2)
    except FileNotFoundError:
        print("The file does not exist or is not located in this directory")

        
