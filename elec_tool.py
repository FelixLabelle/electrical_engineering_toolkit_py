__author__ = 'Admin'

from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, Radiobutton
import numpy
import signal
# http://docs.scipy.org/doc/scipy/reference/signal.html

E96_vals = numpy.array(numpy.round(numpy.power(10,(numpy.arange(0, 96, 1)/96)),2))
E24_vals = numpy.array([1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1])
E_val = E96_vals
def main():

    #for i in range(100,1000,10):
     #   print(resistance_fit(i))
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()
    return 1


def order_of_resistance(res2fit):
    order = 0;
    while res2fit >= 10:
        res2fit/=10
        order+=1
    return order,res2fit


def resistance_fit(res2fit):
    [order, res2fit] = order_of_resistance(res2fit)
    index = int(numpy.floor(numpy.log10(res2fit)*(len(E_val)-1)))

    if abs(E_val[index+1]-res2fit) < abs(E_val[index]-res2fit):
        index = index+1
    elif abs(E_val[index-1]-res2fit) < abs(E_val[index]-res2fit):
        index = index-1
    return E_val[index]*numpy.power(10,order)

def voltage_divider_fit(vcc,vout,current):
    r_total = vcc/current
    r_out =  vout/current
    r_in = r_total-r_out
    return numpy.array([resistance_fit(r_in), resistance_fit(r_out)])


def passive_fitted_filter(cut_off_freq,filter_type,resistance_val,capacitance_val):
    return 0

class MyFirstGUI:
    def __init__(self, master):

        # init values
        self.is_e24 = 0;
        self.entered_number = 0

        # init window
        self.master = master
        master.title("Resistance normalizer")

        # Set up buttons and such
        self.label = Label(master, text="Please enter the resistance you wish to normalize")
        self.label.pack()
        self.radio_button = Radiobutton(master, text="E24 Series", variable = self.is_e24, value = 0,command = self.radio_select()).pack(anchor=W)
        self.radio_button = Radiobutton(master, text="E96 Series", variable = self.is_e24, value = 1,command = self.radio_select()).pack(anchor=W)

        self.res_val = Entry(master)
        self.res_val.pack()
        self.res_val.delete(0, END)
        self.res_val.insert(0, "1000")


        self.normalize_button = Button(master, text="Normalize", command=self.normalize)
        self.normalize_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()
    def radio_select(self):
        global E_val
        E_val = (E96_vals,E24_vals)[self.is_e24]


    def normalize(self):

        if self.validate():
            res_val = resistance_fit(self.entered_number);
            #print(res_val) #debugging option
            self.res_val.delete(0,END)
            self.res_val.insert(0, res_val)
        else:
            print("Not a valid value")


    def validate(self):

        try:
            self.entered_number = float(self.res_val.get())
            return True
        except ValueError:
            return False






if __name__ == "__main__":
    main()