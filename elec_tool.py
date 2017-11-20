__author__ = 'Admin'

import numpy
import signal
# http://docs.scipy.org/doc/scipy/reference/signal.html


def normalizeComponent(componentToFit):
    order = math.floor(math.log10(componentToFit))
    normalizedValue = componentToFit / math.pow(10,order)
    return order, normalizedValue



# Uses logarithmic nature of resistances to approximate best fit without iterating through the list
# currently fails for best approximation close to the next decade for 5% tolerance, maybe use the
# circular nature of python array indexing (or use a mod)

def fitComponent(componentToFit, tolerance=5):
    if (tolerance == 1):
        E_val = np.array(np.round(np.power(10, (np.arange(0, 96, 1) / 96)), 2))
    else:
        E_val = np.array(
            [1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5,
             8.2, 9.1])
    #print(E_val)
    [order, normalizedComponent] = normalizeComponent(componentToFit)

    index = int(np.floor(np.log10(normalizedComponent) * (len(E_val) - 1)))
    print(E_val[index])
    if abs(E_val[index + 1] - normalizedComponent) < abs(E_val[index] - normalizedComponent):
        index = index + 1
    elif abs(E_val[index - 1] - normalizedComponent) < abs(E_val[index] - normalizedComponent):
        index = index - 1
    return E_val[index] * math.pow(10, order)


def fitFilter(cut_off_freq, filter_type, resistance_val, capacitance_val):
    return 0

# This is a naive way to fit voltage dividers. With some TLC it could provide optimization and a way to better choose values (based on
# your applications needs)
def fitVoltageDivider(vcc, vout, current):
    rTotal = vcc / current
    rOut = vout / current
    rIn = rTotal - rOut
    return np.array([fitComponent(rIn), fitComponent(rOut)])


