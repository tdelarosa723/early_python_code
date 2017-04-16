from Tkinter import *
import sys
import os
from datetime import *
import calendar
import math

buttons=[]

class Application(Frame):
    Frame.defaultfolders = ["Documents", "Images", "Audio", "Code", "Builds", "ProjectFolder"]
    Frame.phases = ["Brainstorming", "Art Concept", "Technical Concept", "Prototyping",
     "Art Design", "Technical Design", "Demo Builds", "User Testing", "Final Build"]
    Frame.phaseimportance = [0.14, 0.28, 0.28, 0.28, 0.38, 0.38, 0.07, 0.07, 0.07]
    #Start
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.makeUI()
    def makeUI(self):
        button_newproject = Button(self, text = "New Project", command = self.createTxt)
        button_openproject = Button(self, text = "Open Project", command = self.opendir)

        button_newproject.grid(row = 1, column = 1, columnspan = 2, sticky = W)
        button_openproject.grid(row = 3, column = 1, sticky = W)

        buttons.append(button_openproject)
        buttons.append(button_newproject)

    def createTxt(self):
        #create a textbox
        self.box_create = Entry(self)
        self.box_create.grid(row = 2, column = 1, sticky = W)
        #create submit button
        self.submit = Button(self, text = "Submit", command = self.createdir)
        self.submit.grid(row = 2, column = 2, sticky = W)

        buttons.append(self.box_create)
        buttons.append(self.submit)

    def createdir(self):
        #create new folder
        self.current = os.getcwd()
        self.newpath = os.path.join(self.current, self.box_create.get())
        os.mkdir(self.newpath)
        #create multiple base folders
        for i in Frame.defaultfolders:
            self.newsubs = os.path.join(self.newpath, i)
            os.mkdir(self.newsubs)
        #start base2
        self.selectdate()

    def opendir(self):
        #create a textbox
        if self.box_create:
            self.box_create.delete(END)
        self.box_open = Entry(self)
        self.box_open.grid(row = 4, column = 1, sticky = W)

    def selectdate(self):
        #destroy all buttons first
        for j in buttons:
            j.destroy()
        #then add new buttons
        #format help
        self.inform1 = Label(self, text="This will be replaced with a calendar picker")
        self.inform1.grid(row = 1, column = 1, columnspan=2, sticky = W)
        #entrybox
        self.box_selectdate = Entry(self)
        self.box_selectdate.grid(row = 2, column = 1, sticky = W)
        #submit button
        self.submit = Button(self, text = "Submit", command = self.newschedule)
        self.submit.grid(row = 2, column = 2, sticky = W)
        #format help
        self.dateformat = Label(self, text="MM/DD/YYYY")
        self.dateformat.grid(row = 3, column = 1, sticky = W)
        #append everything
        #This is not the way i usually do things but this works for now
        buttons.append(self.inform1)
        buttons.append(self.box_selectdate)
        buttons.append(self.submit)
        buttons.append(self.dateformat)

    def newschedule(self):
        #whats today?
        today = date.today()
        #duedate
        duedate = self.box_selectdate.get()
        #figure out how many days in between two dates
        daysleft = date(int(duedate[6:10]), int(duedate[0:2]), int(duedate[3:5])) - today
        #destroy all buttons first
        for j in buttons:
            j.destroy()
        #ALG Designating time chunks based on preset values
        conceptstage = 35
        progressivestage = 65
        sections = 1

        ratioA = float(conceptstage)/float(progressivestage)
        goal = progressivestage * sections
        ratioB = float(conceptstage)/goal
        #average the two ratios
        ratioAVG = (ratioA + ratioB) / 2
        conceptstage = progressivestage * ratioAVG
        progressivestage = 100 - conceptstage
        #now we divide those percentages up into each category
        #now lets organize a schedule based on percentages
        for k in range(0, len(Frame.phases)):
            #calulate workdays
            if k < 4:
                wr = Frame.phaseimportance[k] * conceptstage
                workdays = (wr/100) * daysleft.days
            else:
                wr = Frame.phaseimportance[k] * progressivestage
                workdays = (wr/100) * daysleft.days

            workdays = math.floor((workdays*100)/100)
            #create a label
            newlabel = Label(self, text="%s for %s day(s)" % (Frame.phases[k], workdays))
            #show it on a grid
            newlabel.grid(row=(k+1), column=1, sticky = W)
            #have buttons append it
            buttons.append(newlabel)

root = Tk()
root.title("Indieep")
root.geometry("400x400")
app = Application(root)

root.mainloop()
