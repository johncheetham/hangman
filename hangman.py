#!/usr/bin/env python

#
#   Hangman V 0.1 June 2009
#
#   Copyright (C) 2009 John Cheetham    
#
#   web   : http://www.johncheetham.com/projects/hangman
#   email : developer@johncheetham.com
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#    
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pygtk
pygtk.require('2.0')
import gtk
import pango
import random

class Hangman:
          
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    imagebase = 'images/hm-'
    
    def callback(self, widget, guess):
        #print "key - %s was pressed" % guess 
        if guess == 'Quit':
            gtk.main_quit()            
            return False
        elif guess == 'PlayAgain':
            self.word = self.getWord()
            self.lcaseword = self.word.lower()
            self.imageidx = 0
            self.image.set_from_file(Hangman.imagebase +
                                     str(self.imageidx) + '.jpg')
            self.mask = ''
            for c in self.word:
                if c == ' ':
                    self.mask=self.mask + ' '
                else:
                    self.mask=self.mask + '-' 
            self.masklabel.set_text(self.mask)
            for i in range(0, 26): 
                self.a_button[i].set_sensitive(True)
                self.a_button[i].show() 
            self.msglabel.set_text \
                 ('Score : ' + str(self.score) + ' ' * 9 + '\n\n\n\n') 
            self.gameover = False
        else:          
            self.processKeyPress(guess)           
        
    def delete_event(self, widget, event, data=None):        
        gtk.main_quit()
        return False
    
    def key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        #print "Key %s (%d) was pressed" % (keyname, event.keyval)
        self.processKeyPress(keyname)        

    def __init__(self):   

        self.gameover = False  
        self.word = self.getWord()
        self.lcaseword = self.word.lower()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)        
        self.window.set_title("Hangman")       
        self.window.connect("delete_event", self.delete_event)   
        self.window.connect("key_press_event", self.key_press_event)         
        self.window.set_border_width(10)
        
        # 2 rows, 26 columns          
        table = gtk.Table(2, 13, True)        

        vbox = gtk.VBox(False, 10)
        self.window.add(vbox)

        # Hangman image
        hbox = gtk.HBox(False, 0)
        frame = gtk.Frame() 
        self.image = gtk.Image()
        self.imageidx = 0
        self.image.set_from_file(Hangman.imagebase+str(self.imageidx) + '.jpg')
        frame.add(self.image)             
        hbox.pack_start(frame, True, False, 0)
        
        self.score = 0
        self.msglabel = gtk.Label \
                        ('Score : ' + str(self.score) + ' ' * 9 + '\n\n\n\n')
                        
        self.msglabel.modify_font(pango.FontDescription("sans 15"))          
        hbox.pack_start(self.msglabel, True, False, 0) 
                
        vbox.pack_start(hbox, False, False, 0) 
       
        frame = gtk.Frame()         
        
        self.mask=''
        for c in self.word:
            if c == ' ':
                self.mask = self.mask+' '
            else:
                self.mask = self.mask+'-' 
        
        self.masklabel = gtk.Label(self.mask)
        self.masklabel.modify_font(pango.FontDescription("sans 27"))         
        vbox.pack_start(self.masklabel, False, False, 0) 

        frame = gtk.Frame()         

        left = 0
        top = 0
        i = 0 
        self.a_button = []
        for letter in Hangman.ALPHABET.upper():            
            self.button1 = gtk.Button(letter)
            self.button1.connect("clicked", self.callback, letter) 
            self.a_button.append(self.button1)           
            if left == 13:
                left = 0
                top += 1       
            table.attach(self.button1, left, left + 1, top, top + 1)
            left += 1           
            i += 1
        frame.add(table)
        vbox.pack_start(frame, False, False, 0)             
                   
        hbox = gtk.HBox(True, 0)
        self.button = gtk.Button('Quit')  
        self.button.connect("clicked", self.callback, 'Quit') 
        hbox.pack_start(self.button, True, False, 0)  
        self.button = gtk.Button('Play Again')  
        self.button.connect("clicked", self.callback, 'PlayAgain') 
        hbox.pack_start(self.button, False, False, 0)   
                
        vbox.pack_start(hbox, True, False, 0)     

        self.window.show_all ()

    def processKeyPress(self,guess):
        #print 'in pkp %s' % guess                
               
        # ignore keys if gameover.
        # only options available are quit and play again buttons  
        if self.gameover:
            return

        lcguess = guess.lower()
        # ignore invalid key presses
        if lcguess not in Hangman.ALPHABET:
            return         

        # if key already pressed (button not visible) then ignore
        if not self.a_button[Hangman.ALPHABET.find(lcguess)].props.visible:
            return

        # key press was valid alphabetic and not already used.
        # Make button invisible. 
        self.a_button[Hangman.ALPHABET.find(lcguess)].hide()  

        # check if guess was in the word 
        i = 0
        mask = ''            
        goodguess = False
        for c in self.lcaseword:            
            if c == lcguess:
                mask=mask+self.word[i]
                goodguess = True
            else:
                mask = mask+self.mask[i]    
            i += 1 

        self.mask=mask        
        self.masklabel.set_text(mask)

        # guess wasn't in the word so display the next hangman image 
        if not goodguess:
            self.imageidx += 1
            self.image.set_from_file(Hangman.imagebase+str(self.imageidx) +
                                     '.jpg') 
            # if the final image then game over (player loses)
            if self.imageidx == 10:                         
                self.score -= 1     
                self.msglabel.set_text \
                     ('Score : ' + str(self.score) + '\n\nYou Lose' +
                      '\nThe answer was:\n' + self.word) 
                for i in range(0, 26): 
                    self.a_button[i].set_sensitive(False)  
                self.gameover = True    

        # check if word completed
        if mask == self.word:            
            self.score += 1    
            self.msglabel.set_text('Score : ' + str(self.score) + '\n\nYou Win') 
            for i in range(0, 26): 
                self.a_button[i].set_sensitive(False)      
            self.gameover = True  

    def getWord(self):
        f = open('data/words.txt')
        list=f.readlines()   
        f.close()                 
        return list[int(random.random() * len(list))].rstrip('\n')

if __name__ == "__main__":
    hm = Hangman()  
    gtk.main()      
    
