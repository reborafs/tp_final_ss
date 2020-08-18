import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def pulseTrain (freq, time, fs = 44100):
    '''
    '''
    period = 1/freq
    ones = np.ones(round((period/2)*fs))
    zeros = np.zeros(round((period/2)*fs))
    pulse_train = np.hstack((ones,zeros))
    
    while len(pulse_train) < time*fs:
        pulse_train = np.hstack((pulse_train,pulse_train))
    
    return pulse_train[:round(time*fs)]

def sincFunction (arg, time, fs = 44100):
    '''
    '''
    vector_t = np.linspace(-time/2, time/2, round(time*fs))
    sinc = np.sin(arg*vector_t)/(arg*vector_t)
    return sinc

def a_n(signal, period, n_harmonic, fs = 44100):
    '''
    '''
    signal = signal[:round(period*fs)]
    vectorT = np.arange(0, len(signal))/fs
    signal = signal * np.cos((2*n_harmonic*np.pi*vectorT)/period)
    coeff_a = (2/period) * np.trapz(signal, vectorT)
    
    return coeff_a

def b_n(signal, period, n_harmonic, fs = 44100):
    '''
    '''
    
    signal = signal[:round(period*fs)]
    vectorT = np.arange(0, len(signal))/fs
    signal = signal * np.sin((2*n_harmonic*np.pi*vectorT)/period)
    coeff_b = (2/period) * np.trapz(signal, vectorT)
    
    return coeff_b

def fourierSeries(signal, period, stop_at_error, value , fs = 44100):
    '''
    '''
    time = len(signal)/fs
    vector_t = np.linspace(0, time, round(time*fs))
    fourier_series = 1/2 * a_n(signal, period, 0, fs)
    
    if stop_at_error == True :
        min_error = value
        n = 0
        while msError(signal, fourier_series) > min_error:
            n += 1
            fourier_series += (a_n(signal,period,n,fs) * 
                                   np.cos((vector_t*n*2*np.pi)/period)
                            + b_n(signal,period,n,fs) * 
                                   np.sin((vector_t*n*2*np.pi)/period))
        
    elif stop_at_error == False:
        max_harmonics = value
        for n in range(1, max_harmonics+1):
            fourier_series += (a_n(signal,period,n,fs) * 
                                     np.cos((vector_t*n*2*np.pi)/period)
                                + b_n(signal,period,n,fs) * 
                                     np.sin((vector_t*n*2*np.pi)/period))    
    
    return (fourier_series, n, msError(signal, fourier_series))


def msError(signal, fourier_series):
    '''
    '''
    ms_error = ((fourier_series - signal)**2).mean()
    return ms_error*100

def gibbsCheck(signal, fourier_series):
    '''
    '''
    norm_signal = signal/max(abs(signal))
    norm_fourier = fourier_series/max(abs(signal))
    max_error = abs(max(norm_signal)-max(norm_fourier))
    min_error = abs(min(norm_signal)-min(norm_fourier))
    if abs(min_error-max_error) < 0.001:
        return (max_error+min_error)*100
    elif min_error < max_error:
        return max_error*100
    else:
        return min_error*100
    
def dirichletCheck (signal, fs):
    pass

def pulseMainFunction (time, freq, method, value, fs = 44100):
    # Building signal
    vector_t = np.linspace(0, time, round(time*fs))
    signal = pulseTrain(freq, time, fs)
    
    # Choosing method
    if method == 'Error [%]':
        stop_at_error = True
    elif method == 'Armónicos [n]':
        stop_at_error = False
        value = int(value)
        value = value 
    
    # Building Fourier Series
    fourier_tuple = fourierSeries(signal, 1/freq, stop_at_error, value, fs)
    fourier_series = fourier_tuple[0]
    n_harmonics = fourier_tuple[1]
    ms_error = fourier_tuple[2]
    gibbs = gibbsCheck(signal, fourier_series)
    
    if ((1/2*freq) > time ):
        msg = "La señal representada es una constante, no un tren de pulsos. Para corregir esto ingrese un valor de tiempo mayor a la mitad del período."
    else:
        msg = "Porcentaje de Gibbs: " + str(gibbs) + "%" 
   
    # Plotting
    plt.plot(vector_t, fourier_series,'y', label='Serie de Fourier')
    plt.plot(vector_t, signal, ',r')
    plt.title('Serie de Fourier para Tren de Pulsos')
    red_patch = mpatches.Patch(color='red', label='Tren de Pulsos')
    yellow_patch = mpatches.Patch(color='yellow', label='Serie de Fourier')
    plt.legend(handles=[red_patch, yellow_patch], bbox_to_anchor=(0.6, 0.8), 
               loc='upper left')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid()
    plt.savefig("./static/img/series.png")
    plt.close()
    
    # Return values
    return {"harmonics": round(n_harmonics), "error": round(ms_error, 4), "msg": msg, "gibbs": gibbs}

         
def sincMainFunction (time, arg, method, value, fs = 44100):
    # Building signal
    vector_t = np.linspace(-time/2, time/2, round(time*fs))    
    signal = sincFunction(arg, time, fs)
    
    # Choosing method
    if method == 'Error [%]':
        stop_at_error = True
    elif method == 'Armónicos [n]':
        stop_at_error = False
        value = int(value)
    
    # Building Fourier Series
    fourier_tuple = fourierSeries(signal, time, stop_at_error, value, fs)
    fourier_series = fourier_tuple[0]
    n_harmonics = fourier_tuple[1]
    ms_error = fourier_tuple[2]
    
    # Plotting
    plt.plot(vector_t, fourier_series,'y')
    plt.plot(vector_t, signal, 'r')
    plt.title('Serie de Fourier para función Sinc')
    red_patch = mpatches.Patch(color='red', label='Función Sinc')
    yellow_patch = mpatches.Patch(color='yellow', label='Serie de Fourier')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.legend(handles=[red_patch, yellow_patch], bbox_to_anchor=(0.6, 0.8), 
               loc='upper left')
    plt.grid()
    plt.savefig("./static/img/series.png")
    plt.close()
    
    # Return values
    return {"harmonics": n_harmonics, "error": round(ms_error, 6)}

#-------------------------------TREN DE PULSOS-------------------------------#

# freq = 2
# time = 2
# method = "Armónicos [n]"
# value = 10
# method = "Error [%]"
# value = 0.1
# pulseMainFunction(time, freq, method, value)

#-------------------------------SENAL CONTINUA-------------------------------#

# freq = 2
# time = 2
# method = "Armónicos [n]"
# value = 10
# method = "Error [%]"
# value = 0.1
# sincMainFunction(time, arg, method, value)
