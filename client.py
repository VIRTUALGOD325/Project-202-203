import socket 
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 8000

#nickname = input("ENTER YOU NICNAME")


client.connect((ip_address, port))

print("CONNECTED TO SERVER")

class GUI:
    def __init__(self):
        
        self.Window = Tk()
        
        self.Window.withdraw()
        
        self.login = Toplevel()
        self.login.title("LOGIN PAGE")
       
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)
        
        self.pls = Label(self.login,text="PLEASE LOGIN TO CONTINUE",justify=CENTER,font="Helvetica 14 bold")
        self.pls.place(relheight=0.15,relx=0.2,rely=0.07)
        
        
        self.labelName = Label(self.login,text="NAME: ",font="Helvetica 12")
        self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)
        
        self.entryName = Entry(self.login,font="Helvetica 12")
        self.entryName.place(relwidth=0.4,relheight=0.12,relx=0.35,rely=0.2)
        self.entryName.focus()
        
        self.submitButton = Button(self.login,text="JOIN",font="Helvetica 14 bold",
                                        command=lambda:self.goAhead(self.entryName.get()))
        self.submitButton.place(relx=0.4,rely=0.55)

        self.Window.mainloop()
    

    def layout(self,name):
        self.name = name

        self.Window.deiconify()

        self.Window.title("GROUP CHAT")

        self.Window.resizable(height=False, width=False)

        self.Window.configure(width=470,height=550,bg="#17202A")

        self.headLabel = Label(self.Window,text=self.name,fg="#eaecee",
                                    bg="#17202A",font="Helvetica",pady=8)
        
        self.headLabel.place(relwidth=1)

        self.line = Label(self.Window,width=450,bg="#ABB2B9")
        self.line.place(relwidth=1,rely=0.06,relheight=0.012)

        self.textCons = Text(self.Window,width=20,height=2,bg="#17202A",fg="#17202A"
                                ,font="Helvetica",padx=5,pady=5)
        self.textCons.place(relheight=0.74,relwidth=1,rely=0.08)

        self.bottomLabel = Label(self.Window,bg="#ABB2B9",height=80)
        self.bottomLabel.place(relwidth=1,rely=0.82)

        self.entryMessage = Entry(self.bottomLabel, fg="#eaecee", bg="#2C3E50", font="Helvetica")
        self.entryMessage.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entryMessage.focus()

        self.messageButton = Button(self.bottomLabel, text="SEND", font="Helvetica", 
                                        width=20, bg="#ABB2B9",command=lambda:self.sendButton(self.entryMessage.get()))
        self.messageButton.place(relwidth=0.22,relheight=0.06,relx=0.77,rely=0.008)
        
        self.textCons.configure(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=0.97)
        scrollbar.configure(command=self.textCons.yview)

        self.textCons.configure(state=DISABLED)


    def sendButton(self,message):
        self.textCons.configure(state=DISABLED)
        self.message = message
        self.entryMessage.delete(0,END)

        sendThread = Thread(target=self.write)
        sendThread.start()

    
    def showMessage(self,message):
        self.textCons.configure(state=NORMAL)
        self.textCons.insert(END,message + "\n\n")
        self.textCons.configure(state=DISABLED)
        self.textCons.see(END)
        



    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == "NICKNAME":
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMessage(message)
            except:
                print("ERROR OCCURED TRY AGAIN LATER")
                client.close()
                break

    
    def write(self):
        self.textCons.configure(state=DISABLED)
        while True:
            message = "{}: {}".format(self.name,self.message)
            client.send(message.encode('utf-8'))
            self.showMessage(message)
            break


    def goAhead(self,name):
        self.login.destroy()
        self.layout(name)

        rcv = Thread(target=self.receive)
        rcv.start()




g = GUI()




