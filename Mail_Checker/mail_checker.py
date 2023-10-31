#This script gives you the subject of mails received from a given list of mail addresses
import imaplib



user = 'Your Gamil address'
password = 'Your password'

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, password)
mail.list()

mail.select("inbox")  # connects to your inbox, change the argument to access different categories.


def readMails(address):
    result, data = mail.search(None, '(FROM '+'"'+address+'")')         #If you would like to view mails that are sent to another mail, change FROM into TO 

    ids = data[0]  # data is a list.
    id_list = ids.split()  
    latest_email_id = id_list[-1]  # gets the latest mail from the particular user

   
    result, data = mail.fetch(latest_email_id, "(RFC822)")

    
    basic_email = data[0][1]
    # contains all information including payloads and html content

    index_start1 = basic_email.index(b'Subject')           #Starting index for your subject
    index_end1 = index_start1 + 40                         # Change the value of 40 into any other value to suit your preferences
    

    subject = basic_email[index_start1:index_end1]           #seperating the subject alone from the rest of the basic email
    

    
    subject = subject.strip(b'b\'Subject:')               #removing additional unneccessary data from the subject
    subject_end = subject.index(b'\r')

    print('-------FROM '+address+'-------\n\n')                        #Printing the emails
    print("Subject: ", subject[0:subject_end], '\n\n')
   


listOfMails = ['mail1@gmail.com','mail2@gmail.com']           #Modify the list contents here to suit you. If you would like to view mails 
                                                                                                    #  from say, 'abc@gmail.com' change 'mail1@gmail.com' to 'abc@gmail.com'
for addresses in listOfMails:
    readMails(addresses)