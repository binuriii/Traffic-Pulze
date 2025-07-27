import tkinter as tk        #abbreviation for 'tkinter'

class HistogramApp:
    def __init__(self, root, data_1, data_2, date):       #inititalize instances of the class
        self.root = root                                  #store the root window
        self.root.title("Histogram")                      #set title as "Hist.." in main window
        self.date = date                                  #store the given date

        #store the two data sets
        self.data_1 = data_1
        self.data_2 = data_2

        #set dimentions 
        self.canvas_width = 1200
        self.canvas_height = 400    #total height of the canvas
        self.padding = 100          #reserved space bottom of the lables

        #set barchart properties
        self.bar_width = 15
        self.barspacing = 0         #no any spaces between same lables
        self.groupspacing = 15      #space between two lables
        self.barchart_width = 0
        
        self.maxValue = max(max(self.data_1.values()), max(self.data_2.values()))         #find max in provided dataset
        self.scale = (self.canvas_height - 2 * self.padding) / self.maxValue              #scale for bar height

        #set colors to text and bars
        self.textcolor = "#747673"
        self.bar1color = "#95fb97"
        self.bar2color = "#ff9496"

        #creates and display a drawning area
        self.canvas = tk.Canvas(
            self.root,
            width = self.canvas_width,
            height = self.canvas_height,
            bg = "#edf2ee",
        )

        self.canvas.pack() #to ensure the canvas added to GUI

        #call methods
        self.drawbars()
        self.drawaxes()
        self.drawlegend()
        self.footer_text()

    def drawaxes(self):
        self.canvas.create_line(                    #use to draw a straight line
            self.padding + self.groupspacing,       #together determine where lin should start
            self.canvas_height - self.padding,      #correct vertical position
            self.barchart_width,                    #end of x axis where the last bar ends
            self.canvas_height - self.padding,      #horizontal line
            width = 1,                              #width of the line
            fill = 'black'                          #color of the line
        )

    def drawbars(self):

        #draw bars for d1 and d2
        x = self.padding + self.groupspacing    #initialize starting x position for the bars
        x2 = 0                                  #end of the first bar

        for label in self.data_1.keys():
            #bar for data_1
            value_1 = self.data_1[label]        #get the value from data_1 for the current label
            bar_height1 = value_1 * self.scale  #calculate height of the bar
            x1 = x                              #starting x position for the first bar
            y1 = self.canvas_height - self.padding      #starting y position
            x2 = x + self.bar_width                     #ending x position
            y2 = self.canvas_height - self.padding - bar_height1    #ending y position
            self.canvas.create_rectangle(x1, y1, x2, y2, outline = "black", fill = self.bar1color)  #draw the rec for the first bar
            #set value on top of the bar
            self.canvas.create_text((x1 + x2) / 2, y2 - 10, text = str(value_1), fill = "#54bc52", font = ("Arial", 10, "bold") )

            #bar for data_2
            value_2 = self.data_2[label]
            bar_height2 = value_2 * self.scale      #calculate height of the second bar
            x1_2 = x2                               #start where the first bar ends
            x2_2 = x1_2 + self.bar_width            #ending x position of the second bar
            y2_2 = self.canvas_height - self.padding - bar_height2   #ending y position   
            self.canvas.create_rectangle(x1_2, y1, x2_2, y2_2, outline = "black", fill = self.bar2color)    #draw the second rectangle
            self.canvas.create_text((x1_2 + x2_2) / 2, y2_2 - 10, text = str(value_2), fill = "#ec7057", font = ("Arial", 10, "bold") )     #place the values on top

            #add a label below each group
            self.canvas.create_text(
                                    (x + x2_2) / 2, #center of the bars
                                    self.canvas_height - self.padding + 15,     #position 15 pixels below the x
                                    text = "{:02d}".format(label),              #format as two digit number
                                    font = ("Arial", 12, "bold"),               #set format style,size and weight
                                    fill = "black",
                                    )
                
            #adjust x to next group of bars
            x = x + 2 * self.bar_width + self.groupspacing      #width of bars and add spaces between them
        
        self.barchart_width = x2 + self.bar_width           #update total width of the bar

    def drawlegend(self):
        #legend drawing
        legend_xstart = 20      #set starting x coordinate
        legend_ystart = 50      #set starting y coordinate

        self.canvas.create_text(
            legend_xstart + 20,     #places title right of the legend box
            legend_ystart - 30,     #places title 30 pixel above the rectangle
            text = "Histogram of Vehicle Frequency per Hour ({}) ".format(self.date),
            anchor = "w",           #align text to the left
            font = ("Arial", 24, "bold"),
            fill = self.textcolor,
        )

        #draw the first rectangle for the legend
        self.canvas.create_rectangle(
            legend_xstart, legend_ystart, legend_xstart + 20, legend_ystart + 20, outline = "black", fill = self.bar1color)
        
        #put a text label next to first rectangle in the legend  
        self.canvas.create_text(
            legend_xstart + 25, legend_ystart + 10, text = "Elm Avenue/Rabbit Road", anchor = "w", font = ("Arial", 12, "bold"), fill = self.textcolor)
            
        self.canvas.create_rectangle(
            legend_xstart, legend_ystart + 30, legend_xstart + 20, legend_ystart + 50, outline = "black", fill = self.bar2color)
            
        self.canvas.create_text(
            legend_xstart + 25, legend_ystart + 40, text = "Hanley Highway/Westway", anchor = "w", font = ("Arial", 12, "bold"), fill = self.textcolor)

    #create footer text bottom of the canvas        
    def footer_text(self):
        self.canvas.create_text(
        self.canvas_width / 2,                      #centers the text horizontally
        self.canvas_height - self.padding + 50,     #position text below x axis
        text = "Hours 00:00 to 24:00",              #static footer text
        fill = self.textcolor,
        font = ("Arial", 14, "bold"),
        )


