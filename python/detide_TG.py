
import os
import numpy
import matplotlib.pyplot as plt
import TG_DART_tools as TG

download_data = True
save_detided_txt = True
save_plot = True

TGdir = os.path.abspath('../TideGauges')

def detide_all():

    print "download_data = ",download_data
    print "save_detided_txt = ",save_detided_txt
    print "save_plot = ",save_plot

    p = {k:TG.periods[k] for k in TG.constituents_hawaii}
    print "Detiding using only harmonic constituents \n  %s" % p.keys()

    plt.figure(1,figsize=(10,10))
    plt.figure(2,figsize=(10,10))

    for k,gaugeno in enumerate([1612340, 1615680, 1617760]):

        fname = os.path.join(TGdir, "TG_%s_raw.csv" % gaugeno)

        if download_data:
            TG.get_coops_gauge(gaugeno, "20110311","20110313",file_name=fname, 
                        verbose=True)

        t,tsec,eta,pred,res = TG.read_tide_gauge(fname, 
                "05:46:24 UTC on March 11, 2011")
        print "Read data from ",fname

        thours = tsec / 3600.
        eta_fit, eta_offset, eta_amplitude, eta_phase= \
                TG.fit_tide_harmonic(thours, eta, periods=p, t0=0, svd_tol=1e-5)

        if save_detided_txt:
            fname = os.path.join(TGdir, "TG_%s_detided.txt" % gaugeno)
            d = numpy.vstack((tsec, eta-eta_fit)).T
            numpy.savetxt(fname, d)

        plt.figure(1)
        plt.subplot(3,1,k+1)
        plt.plot(thours,eta,'b',label='raw data')
        plt.plot(thours,eta_fit,'k',label='fit to tide')
        plt.legend()
        plt.title("TG %s" % gaugeno)
        if k==2:
            plt.xlabel('Hours post quake')

        plt.figure(2)
        plt.subplot(3,1,k+1)
        plt.plot(thours,eta-eta_fit,'b')
        plt.xlim(6,20)
        plt.title("Detided data TG %s" % gaugeno)
        if k==2:
            plt.xlabel('Hours post quake')

    plt.show()
    if save_plot:
        fname = os.path.join(TGdir, "TG_raw.png")
        plt.figure(1)
        plt.savefig(fname)
        print "Created ",fname
        fname = os.path.join(TGdir, "TG_detided.png")
        plt.figure(2)
        plt.savefig(fname)
        print "Created ",fname

if __name__ == "__main__":
    detide_all()
