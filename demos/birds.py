import pysndlib.clm as CLM
import pysndlib.sndlib as LIB
import pathlib

# Create directory under this notebook to hold the audio files.
audiodir = './birdcalls/'
pathlib.Path(audiodir).mkdir(exist_ok=True)

#==================================================================================
# The code below is a faithful translation of Bill Schottstedaet's 'bird.scm' file 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================


main_amp = [0.0, 0.0, .25, 1.0, .60, .70, .75, 1.0, 1.0, 0.0]
bird_tap = [0.0, 0.0, .01, 1.0, .99, 1.0, 1.0, 0.0]
bird_amp = [0.0, 0.0, .25, 1.0, .75, 1.0, 1.0, 0.0]


def bird(start, dur, frequency, freqskew, amplitude, freq_envelope, amp_envelope):
    gls_env = CLM.make_env(freq_envelope, scaler=CLM.hz2radians(freqskew), duration=dur)
    os = CLM.make_oscil(frequency)
    amp_env = CLM.make_env(amp_envelope, scaler=amplitude, duration=dur)
    beg = CLM.seconds2samples(start)
    end = CLM.seconds2samples(start + dur)
    for i in range(beg, end):
        CLM.outa(i, CLM.env(amp_env) * CLM.oscil(os, CLM.env(gls_env)))


def bigbird(start, dur, frequency, freqskew, amplitude, freq_envelope, amp_envelope, partials):
    gls_env = CLM.make_env(freq_envelope, scaler=CLM.hz2radians(freqskew), duration=dur)
    os = CLM.make_polywave(frequency, partials=CLM.normalize_partials(partials))
    amp_env = CLM.make_env(amp_envelope, scaler=amplitude, duration=dur)
    beg = CLM.seconds2samples(start)
    end = CLM.seconds2samples(start + dur)
    for i in range(beg, end):
        CLM.outa(i, CLM.env(amp_env) * CLM.polywave(os, CLM.env(gls_env)))
        

def orchard_oriole(beg):
    oriup =  [0.0, 0.0, 1.0, 1.0]
    oridwn = [0.0, 1.0, 1.0, 0.0]
    oriupdwna = [0.0, 0.0, .60, 1.0, 1.0, .60]
    oriupdwnb = [0.0, .50, .30, 1.0, 1.0, .0]
    oriamp = [0.0, 0.0, .10, 1.0, 1.0, .0]
    beg = beg - .38
    bird(beg + .38, .03, 3700, 100, .05, oridwn, main_amp)
    bird(beg + .41, .05, 2500, 1000, .1, oriup, main_amp)
    bigbird(beg + .5, .1, 2000, 800, .2, oriupdwna, main_amp,
                [1, 1, 2, .02, 3, .05])
    bird(beg + .65, .03, 3900, 1200, .1, oridwn, main_amp)
    bigbird(beg + .7, .21, 2000, 1200, .15,
                [0.0, .90, .15, 1.0, .40, .30, .60, .60, .85, 0.0, 1.0, .0],
                main_amp, [1, 1, 2, .05])
    bird(beg + 1.0, .05, 4200, 1000, .1, oridwn, main_amp)
    orimid = [0.0, 1.0, .05, .50, .10, 1.0, .25, 0.0, .85, .50, 1.0, .0]
    bigbird(beg + 1.1, .1, 2000, 1000, .25, orimid, main_amp,
                [1, 1, 2, .05])
    bigbird(beg + 1.3, .1, 2000, 1000, .25, orimid, main_amp,
                [1, 1, 2, .05])
    bird(beg + 1.48, .1, 2300, 3200, .1, oriupdwnb, oriamp)
    bird(beg + 1.65, .03, 1800, 300, .05, oriup, main_amp)
    bird(beg + 1.7, .03, 2200, 100, .04, oridwn, main_amp)
    bird(beg + 1.8, .07, 2500, 2000, .15, oriupdwnb, oriamp)
    bigbird(beg + 1.92, .2, 2400, 1200, .25,
                [0.0, .30, .25, 0.0, 1.0, 1.0], main_amp, [1, 1, 2, .04])
    bird(beg + 2.2, .02, 2200, 3000, .04, oriup, main_amp)
    bird(beg + 2.28, .02, 2200, 3000, .04, oriup, main_amp)
    bigbird(beg + 2.4, .17, 2000, 1000, .2, oriupdwna, oriamp,
                [1, 1, 2, .04])


def cassins_kingbird(beg):
    kingfirst = [0.0, .30, .45, 1.0, .90, .10, 1.0, .0]
    kingsecond = [
        0.0, 0.0, .02, .50, .04, 0.0, .06, .55, .08, .05, .10, .60, .12, .05,
        .14, .65, .16, .10, .18, .70, .20, .10, .22, .75, .24, .15, .26, .80,
        .28, .20, .30, .85, .32, .25, .34, .90, .36, .30, .38, .95, .40, .40,
        .42, 1.0, .44, .50, .46, 1.0, .48, .45, .50, 1.0, .52, .50, .54, 1.0,
        .56, .40, .58, .95, .60, .40, .62, .90, .64, .40, .66, .85, .68, .35,
        .70, .80, .72, .30, .74, .75, .76, .25, .78, .70, .80, .20, .82, .65,
        .84, .10, .86, .60, .88, 0.0, .90, .55, .92, 0.0, .94, .50, .96, 0.0,
        1.0, .40]
    beg = beg - .03
    bigbird(beg + .03, .04, 1700, 1200, .15, kingfirst, main_amp,
                [1, 1, 2, .5, 3, 0, 4, .2])
    bigbird(beg + .12, .18, 1700, 900, .25, kingsecond, main_amp,
                [1, 1, 2, .01, 3, 0, 4, .1])


def chipping_sparrow(beg):
    chip_up = [0.0, .80,.15, 1.0, .75, .30, 1.0, 0.0]
    for t in [0, .05, .06, .12, .18, .24, .30, .36, 
                .42, .48, .54, .60, .66, .72, .78, .84, .90, .96]:
        bird(beg+t, .05, 4000, 2400, .2, chip_up, main_amp)


def bobwhite(beg):
    bobup1 = [0.0, 0.0, .40, 1.0, 1.0, 1.0]
    bobup2 = [0.0, 0.0, .65, .50, 1.0, 1.0]
    beg = beg - .4
    bigbird(beg + .4, .2, 1800, 200, .1, bobup1, main_amp, [1, 1, 2, .02])
    bigbird(beg + 1, .20, 1800, 1200, .2, bobup2, main_amp, [1, 1, 2, .02])


def western_meadowlark(beg):
    down_skw = [0.0, 1.0, .40, .40, 1.0, .0]
    fas_down = [0.0, 1.0, 1.0, .0]	
    beg = beg - .8
    bigbird(beg + 0.8, 0.1, 2010.000, 0.0, 0.1, [0.0, 0.0, 1.0, 0.0], main_amp, [1, 1, 2, 0.04])
    bigbird(beg + 1.1, .15, 3000.000, 100.000, .110, down_skw, main_amp, [1, 1, 2, .04])
    bigbird(beg + 1.3, .25, 2000.000, 150.000, .200, down_skw, main_amp, [1, 1, 2, .04])
    bigbird(beg + 1.65, .15, 3010.000, 250.000, .110, down_skw, main_amp, [1, 1, 2, .04])
    bigbird(beg + 1.85, .10, 2200.000, 150.000, .110, down_skw, main_amp, [1, 1, 2, .04])
    bigbird(beg + 2.0, .10, 3200.000, 1400.000, .110, fas_down, main_amp, [1, 1, 2, .04])
    bigbird(beg + 2.2, .05, 2000.000, 200.000, .110, fas_down, main_amp, [1, 1, 2, .04])
    bigbird(beg + 2.3, .10, 1600.000, 0.000, .110, fas_down, main_amp, [1, 1, 2, .04])


def scissor_tailed_flycatcher(beg):
    bigbird(beg, .05, 1800, 1800, .2, [0.0, 0.0, .40, 1.0, .60, 1.0, 1.0, .0],
                main_amp, [1, .5, 2, 1, 3, .5, 4, .1, 5, .01])


def great_horned_owl(beg):
    bigbird(beg, .1, 300, 0, .1, main_amp, main_amp, [1, 1, 3, .02, 7, .01])
    bigbird(beg + .3, .4, 293, 6, .1, [0.0, 1.0, 1.0, .0], main_amp, [1, 1, 3, .02, 7, .01])
    owlup = [0.0, 0.0, .30, 1.0, 1.0, 1.0]
    bigbird(beg + 1.45, .35, 293, 7, .1, owlup, main_amp, [1, 1, 3, .02, 7, .01])
    bigbird(beg + 2.2, .2, 300, 0, .1, owlup, main_amp, [1, 1, 3, .02, 7, .01])


def black_throated_gray_warbler(beg):
    grayone = [0.0, .50, .02, .60, .04, .45, .06, .62, .08, .40, .10, .65, .12,
               .35, .14, .70, .18, .30, .20, .70, .22, .30, .24, .70, .25, .20,
               .30, .80, .35, .10, .40, .90, .45, 0.0, .50, 1.0, .55, 0.0, .60,
               1.0, .65, 0.0, .70, 1.0, .75, 0.0, .80, 1.0, .85, 0.0, .90, 1.0,
               .95, 0.0, 1.0, .50]
    graytwo = [0.0, 0.0, .01, .40, .02, 0.0, .03, .40, .04, 0.0, .05, .40, .06,
               0.0, .07, .40, .08, 0.0, .09, .40, .10, 0.0, .25, .80, .40, .30,
               .55, 1.0, .70, 0.0, .85, .80, 1.0, .40]
    grayfour = [0.0, 0.0, 1.0, 1.0]
    bird(beg,       .12, 3700, 600, .05, grayone, main_amp)
    bird(beg + .18, .08, 3000, 800, .07, graytwo, main_amp)
    bird(beg + .28, .12, 3700, 600, .12, grayone, main_amp)
    bird(beg + .44, .08, 3000, 800, .15, graytwo, main_amp)
    bird(beg + .54, .12, 3700, 600, .20, grayone, main_amp)
    bird(beg + .72, .08, 3000, 800, .25, graytwo, main_amp)
    bird(beg + .82, .12, 3700, 600, .25, grayone, main_amp)
    bird(beg + .96, .2, 3000, 2000, .2,
             [0.0, 1.0, .01, .60, .02, 1.0, .03, .60, .04, 1.0,
            .05, .60, .06, 1.0, .07, .60, .08, 1.0, .09, .60,
            .10, 1.0, .11, .60, .12, 1.0, .13, .60, .14, 1.0,
            .15, .60, .16, 1.0, .17, .60, .18, 1.0, .19, .60,
            .20, 1.0, .21, .55, .22, 1.0, .23, .50, .24, 1.0, 
            .25, .50, .26, 1.0, .27, .50, .28, 1.0, .29, .50,
            .30, 1.0, .31, .50, .32, 1.0, .33, .50, .34, 1.0,
            .35, .50, .36, 1.0, .37, .50, .38, 1.0, .39, .50,
            .40, 1.0, .41, .50, .42, 1.0, .43, .50, .44, 1.0,
            .45, .50, .46, 1.0, .47, .50, .48, 1.0, .49, .50,
            .50, 1.0, .51, .50, .52, 1.0, .53, .50, .54, 1.0,
            .55, .50, .56, 1.0, .57, .50, .58, 1.0, .59, .50,
            .60, 1.0, 1.0, .0],
            main_amp)
    bird(beg + 1.2, .02, 4500, 500, .05, grayfour, main_amp)
    bird(beg + 1.25, .02, 4200, 800, .05, grayfour, main_amp)
    bird(beg + 1.3, .02, 4000, 900, .05, grayfour, main_amp)


def yellow_warbler(beg):
    yellow_swirl = [0.0, 1.0, .05, 1.0, .60, 0.0, .80, .30, 1.0, .10]
    yellow_down = [0.0, 1.0, 1.0, .0]
    swirl_amp = [0.0, 0.0, .90, 1.0, 1.0, .0]  
    bird(beg, 0.05, 5600, 400, 0.05, [0.0, 0.0, 0.6, 1.0, 1.0, 0.5], main_amp)
    bird(beg + .23, .12, 5000, 1500, .15, yellow_swirl, swirl_amp)
    bird(beg + .45, .13, 5000, 1700, .17, yellow_swirl, swirl_amp)
    bird(beg + .62, .16, 5000, 2000, .20, yellow_swirl, swirl_amp)
    bird(beg + .85, .15, 5000, 2000, .20, yellow_swirl, swirl_amp)
    bird(beg + 1.05, .075, 3700, 1000, .20, yellow_down, main_amp)
    bird(beg + 1.15, .075, 3700, 800, .15, yellow_down, main_amp)
    bird(beg + 1.25, .075, 3700, 800, .15, yellow_down, main_amp)
    bird(beg + 1.4, .2, 3700, 2000, .2, [
        0.0, 0.0, .30, .20, .80, .70, 1.0, 1.0], swirl_amp)

            
def black_necked_stilt(beg):
    '''
	have to guess about upper partials (cut off by spectrograph)
	"birds" book has piping sound coming back down whereas "songs
	of western birds" just shows it going up.
	'''
    upamp = [0.0, 0.0, .90, 1.0, 1.0, .0]
    rampup = [0.0, 0.0, .50, 1.0, 1.0, .20]
    partialenv = [1, .5,  2, 1, 3, .75, 4, .5,  5, .1]
    bigbird(beg,       .1, 900, 100, .2, rampup, upamp, partialenv)
    bigbird(beg + .30, .1, 900, 200, .2, rampup, upamp, partialenv)
    bigbird(beg + .60, .1, 900, 250, .2, rampup, upamp, partialenv)
         
     
def chestnut_sided_warbler(beg):
    ycurve = [0.0, 1.0, .30, .50, .60, 1.0, .80, .20, 1.0, .0]
    vcurve = [0.0, .20, .50, 1.0, 1.0, .0]
    louder = [0.0, 0.0, .90, 1.0, 1.0, .0]
    beg = beg - .1
    bigbird(beg + .1, .1, 4050, 1200, .05, ycurve, main_amp, [1, 1, 2, .1])
    bigbird(beg + .25, .03, 3900, 300, .075, vcurve, main_amp, [1, 1, 2, .1])
    bigbird(beg + .3, .1, 4050, 1200, .15, ycurve, louder, [1, 1, 2, .1])
    bigbird(beg + .42, .03, 3800, 500, .1, vcurve, main_amp, [1, 1, 2, .1])
    bigbird(beg + .5, .1, 4000, 1200, .2, ycurve, bird_tap, [1, 1, 2, .1])
    bigbird(beg + .65, .03, 3800, 500, .15, vcurve, main_amp, [1, 1, 2, .1])
    bigbird(beg + .72, .1, 4000, 1200, .2, ycurve, bird_tap, [1, 1, 2, .1])
    bigbird(beg + .85, .03, 3800, 500, .15, vcurve, main_amp, [1, 1, 2, .1])
    bigbird(beg + .91, .1, 4000, 1200, .2, ycurve, bird_tap, [1, 1, 2, .1])
    wcurve = [0.0, .50, .15, 0.0, .45, .10, .60, 1.0, .70, .90, 1.0, .90,]
    wamp = [0.0, 0.0, .10, 1.0, .40, .10, .50, .90, .60, .10, .70, 1.0, 1.0, .0]
    bigbird(beg + 1.05, .12, 3800, 2200, .15, wcurve, wamp, [1, 1, 2, .1])
    bigbird(beg + 1.20, .12, 3800, 2200, .15, wcurve, wamp, [1, 1, 2, .1])
    bigbird(beg + 1.35, .12, 2500, 2200, .25, [0.0, 0.0, .95, 1.0, 1.0, 1.0],
            louder, [1, 1, 2, .1])
    bigbird(beg + 1.50, .12, 2500, 4000, .15, [0.0, 1.0, .25, .30, .60, .15, 1.0, .0],
            main_amp, [1, 1, 2, .1])


def grasshopper_sparrow(beg):
    grasstwo = [0.0, 0.0, .10, 1.0, .20, 0.0, .30, 1.0, .40, 0.0, .50, 1.0,
                .60, 0.0, .70, 1.0, .80, 0.0, .90, 1.0, 1.0, .0]
    bird(beg,       .01, 8000, 100, .1, grasstwo, main_amp)
    bird(beg + .11, .01, 5700, 300, .1, grasstwo, main_amp)
    bird(beg + .43, .01, 3900, 100, .1, grasstwo, main_amp)
    bird(beg + .51, 1.4, 6000, 2500, .2, [
        0.0, .50, .02, .80, .04, .30, .06, .80, .07, .10, .08, .90, .10, 0.0,
        .11, .90, .12, 0.0, .13, .90, .14, .10, .15, 1.0, .16, .10, .17, 1.0,
        .18, .10, .19, 1.0, .20, .10, .21, 1.0, .22, .10, .23, 1.0, .24, .10,
        .25, 1.0, .26, .10, .27, 1.0, .28, .10, .29, 1.0, .30, .10, .31, 1.0,
        .32, .10, .33, 1.0, .34, .10, .35, 1.0, .36, .10, .37, 1.0, .38, .10,
        .39, 1.0, .40, .10, .41, 1.0, .42, .10, .43, 1.0, .44, .10, .45, 1.0,
        .46, .10, .47, 1.0, .48, .10, .49, 1.0, .50, .10, .51, 1.0, .52, .10,
        .53, 1.0, .54, .10, .55, 1.0, .56, .10, .57, 1.0, .58, .10, .59, 1.0,
        .60, .10, .61, 1.0, .62, .10, .63, 1.0, .64, .10, .65, 1.0, .66, .10,
        .67, 1.0, .68, .10, .69, 1.0, .70, .10, .71, 1.0, .72, .10, .73, 1.0,
        .74, .10, .75, 1.0, .76, .10, .77, 1.0, .78, .10, .79, 1.0, .80, .10,
        .81, 1.0, .82, .10, .83, 1.0, .84, .10, .85, 1.0, .86, .10, .87, 1.0,
        .88, .10, .89, 1.0, .90, .10, .91, 1.0, .92, .10, .93, 1.0, .94, .10,
        .95, 1.0, .96, .10, .97, 1.0, .98, .10, 1.0, 1.0], main_amp)


def swamp_sparrow(beg):
    swamp_up = [0.0, 0.0, .60, .70, 1.0, 1.0]
    swamp_down = [0.0, 1.0, .50, .50, .60, .60, 1.0, .0]
    bird(beg,  .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .035, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .08, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .1, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .135, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .18, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .2, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .235, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .28, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .3, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .335, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .38, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .4, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .435, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .48, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .5, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .535, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .58, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .6, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .635, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .68, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .7, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .735, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .78, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .8, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .835, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .88, .025, 3700, 0, .1, main_amp, main_amp)
    bird(beg + .9, .02, 3900, 200, .3, swamp_up, main_amp)
    bird(beg + .935, .035, 3200, 3000, .1, swamp_down, main_amp)
    bird(beg + .98, .025, 3700, 0, .1, main_amp, main_amp)
         

def golden_crowned_sparrow(beg):
    goldone = [0.0, 1.0, .25, .20, 1.0, .0] #	these have as different song around here.
    bird(beg,        .5, 4300, 1000, .15, goldone, main_amp)
    bird(beg + 0.7, .45, 3300, 200, .15, goldone, main_amp)
    bird(beg + 1.15, .4, 3800, 100, .15, [
        0.0, .90, .05, 1.0, .10, .40, 1.0, .0], main_amp)
    bird(beg + 1.6, .3, 3800, 100, .1, [
        0.0, .50, .10, 0.0, .20, 1.0, .30, 0.0, .40, 1.0, .50, 0.0, .60, 1.0,
        .70, 0.0, .80, 1.0, .90, 0.0, 1.0, .50], main_amp)
                

def indigo_bunting(beg):
    buntdwn = [0.0, 1.0, 1.0, .0]
    buntv = [0.0, 0.0, .50, 1.0, 1.0, .0]
    bunty = [0.0, 1.0, .50, 0.0, 1.0, .90]
    buntn = [0.0, .80, .30, 1.0, .70, .20, 1.0, .0]
    buntup = [0.0, 0.0, 1.0, 1.0]
    beg = (beg - .4)
    bird(beg + .4, .08, 3000, 700, .25, buntdwn, main_amp)
    bird(beg + .52, .02, 6200, 1000, .05, buntdwn, main_amp)
    bird(beg + .55, .15, 3500, 2300, .1, buntv, main_amp)
    bird(beg + .74, .02, 6200, 1800, .05,
             [0.0, 1.0, .10, .50, .25, .90, 1.0, .0], main_amp)
    bird(beg + .80, .15, 3400, 2300, .1, buntv, main_amp)
    bird(beg + 1.00, .1, 3400, 800, .2, buntv, main_amp)
    bird(beg + 1.13, .03, 4100, 2000, .05, buntdwn, main_amp)
    bird(beg + 1.25, .08, 3400, 800, .2, buntv, main_amp)
    bird(beg + 1.40, .03, 4100, 2000, .05, buntdwn, main_amp)
    bird(beg + 1.5, .07, 3700, 300, .1, buntdwn, main_amp)
    bird(beg + 1.6, .1,  4100, 2200, .15, bunty, main_amp)
    bird(beg + 1.72, .05, 3700, 300, .1, buntdwn, main_amp)
    bird(beg + 1.81, .1,  4100, 2200, .15, bunty, main_amp)
    bird(beg + 1.94, .07, 5200, 1800, .2, buntn, main_amp)
    bird(beg + 2.05, .08, 3000, 1500, .15, buntup, main_amp)
    bird(beg + 2.20, .07, 5200, 1800, .2, buntn, main_amp)
    bird(beg + 2.33, .08, 3000, 1500, .15, buntup, main_amp)
    bird(beg + 2.43, .07, 5200, 1800, .1, buntn, main_amp)
    bird(beg + 2.51, .08, 3000, 1500, .10, buntup, main_amp)


def hooded_warbler(beg):
    hoodup = [0.0, 0.0, 1.0, 1.0]
    hooddown = [0.0, 1.0, 1.0, .0]
    beg = (beg - .6)
    bird(beg + .6, .03, 3900, 1600, .05, hooddown, main_amp)
    bird(beg + .64, .03, 3900, 1700, .05, hooddown, main_amp)
    bird(beg + .8, .03, 3900, 2000, .10, hooddown, main_amp)
    bird(beg + .84, .03, 3900, 2000, .10, hooddown, main_amp)
    bird(beg + .93, .03, 3900, 2100, .15, hooddown, main_amp)
    bird(beg + .97, .03, 3900, 2100, .15, hooddown, main_amp)
    bird(beg + 1.05, .03, 3900, 2100, .05, hooddown, main_amp)
    bird(beg + 1.09, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.17, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.21, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.39, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.51, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.43, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.55, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.63, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.67, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.75, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.80, .03, 3900, 2100, .2, hooddown, main_amp)
    bird(beg + 1.90, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 1.98, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 2.05, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 2.13, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 2.21, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 2.29, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 2.37, .04, 3000, 1000, .15, hoodup, main_amp)
    bird(beg + 2.45, .04, 3000, 1000, .15, hoodup, main_amp)
         
     
def american_widgeon(beg):
    widgeon = [0.0, 0.0, .50, 1.0, 1.0, .0]
    bigbird(beg,       .07, 1900, 300, .15, widgeon, widgeon, [1, 1, 2, .02])
    bigbird(beg + .1,  .11, 1700, 1400, .25, widgeon, widgeon, [1, .7, 2, 1, 3, .02])
    bigbird(beg + .25, .07, 1900, 300, .15, widgeon, widgeon, [1, 1, 2, .02])
         
     
def louisiana_waterthrush(beg):
    water_four = [0.0, 0.0, 1.0, 1.0]
    water_damp = [0.0, 0.0, .90, 1.0, 1.0, .0]
    water_one = [0.0, .80, .35, .40, .45, .90, .50, 1.0, .75, 1.0, 1.0, .10]
    water_amp = [0.0, 0.0, .35, 1.0, .50, .20, .90, 1.0, 1.0, .0]
    bird(beg, .17, 4100, 2000, .2, water_one, water_amp)
    bird(beg + .32, .18, 4050, 2050, .3, water_one, water_amp)
    bird(beg + .64, .20, 4000, 1900, .25, water_one, water_amp)
    bird(beg + .9, .2, 3900, 2000, .3,
             [0.0, 1.0, .40, 0.0, .60, .10, 1.0, .80], bird_tap)
    bird(beg + 1.25, 0.12, 3000, 3000, 0.25,
             [0.0, 1.0, 0.95, 0.0, 1.0, 0.0], water_damp)
    bird(beg + 1.4, .1, 2700, 1500, .2, water_four, water_damp)
    water_five = [0.0, 1.0, 1.0, .0]
    bird(beg + 1.65, .02, 5200, 1000, .1, water_five, main_amp)
    bird(beg + 1.7, .035, 3200, 1000, .1, water_four, water_damp)
         
     
def robin(beg):
    bigbird(beg,       .06, 2000, 800, .15, [
        0.0, 0.0, .12, .70, .30, 0.0, .70, 1.0, 1.0, .50], main_amp, [1, 1, 2, .1])
    bigbird(beg + .11, .10, 2000, 900, .15, [
        0.0, .10, .08, .70, .30, 0.0, .35, 1.0, .40, .30, 1.0, .30], main_amp, [1, 1, 2, .1])
    bigbird(beg + .59, .24, 2000, 2000, .25, [
        0.0, 0.0, .10, 1.0, .20, .70, .35, .70, .65, .30,
        .70, .50, .80, 0.0, .90, .20, 1.0, .0], main_amp, [1, 1, 2, .1])
    bigbird(beg + 1.18, .13, 1900, 1600, .20, [
        0.0, .20, .25, 1.0, .60, .70, .90, 0.0, 1.0, .10], main_amp, [1, 1, 2, .1])
    bigbird(beg + 1.35, .11, 2200, 1200, .25, [0.0, 1.0, 1.0, .0], main_amp, [1, 1, 2, .1])
    bigbird(beg + 1.86, .21, 1950, 2000, .15, [
        0.0, .50, .10, 0.0, .20, 1.0, .30, 0.0, .40,
        1.0, .50, 0.0, .60, 1.0, .70, .50, 1.0, .20], main_amp, [1, 1, 2, .1])


def solitary_vireo(beg):
    bird(beg, .4, 1800, 1200, .2, [
        0.0, .20, .03, .30, .06, .10, .10, .50, .13, .40, .16, .80, .19, .50, 
        .22, .90, .25, .60, .28, 1.0, .31, .60, .34, 1.0, .37, .50, .41, .90,
        .45, .40, .49, .80, .51, .40, .54, .75, .57, .35, .60, .70, .63, .30,
        .66, .60, .69, .25, .72, .50, .75, .20, .78, .30, .82, .10, .85, .30,
        .88, .05, .91, .30, .94, 0.0, .95, .30, .99, 0.0, 1.0, .10],
	    main_amp)
         
     
def pigeon_hawk(beg):
    hupdown = [0.0, 0.0, .30, 1.0, .70, 1.0, 1.0, .0]
    bigbird(beg,       .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .12, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .13, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .25, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .26, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .38, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .39, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .51, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .52, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .64, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .65, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .77, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .78, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + .90, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + .91, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.03, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.04, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.16, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.17, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.29, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.30, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.42, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.43, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.55, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.56, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.68, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.69, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
    bigbird(beg + 1.81, .01, 2050, 0, .1, main_amp, main_amp, [1, .5, 2, 1])
    bigbird(beg + 1.82, .1, 1900, 200, .2, hupdown, main_amp, [1, .7, 2, 1])
         
     
def cerulean_warbler(beg):
    w_up = [0.0, 0.0, 1.0, 1.0]
    beg = beg - .27
    w_down = [0.0, 1.0, 1.0, .0]
    bird(beg + .27, .05, 3000, 1000, .05, w_down, main_amp)
    bird(beg + .33, .05, 3000, 800, .075, w_up, main_amp)
    bird(beg + .41, .01, 3200, 700, .07, w_down, main_amp)
    bird(beg + .42, .01, 3200, 700, .08, w_down, main_amp)
    bird(beg + .43, .06, 3200, 700, .09, w_down, main_amp)
    bird(beg + .51, .06, 3200, 500, .1, w_up, main_amp)
    trill = [0.0, .80, .10, 1.0, .25, .50, .40, 1.0, .55, .50, .70, 1.0, 1.0, .0]
    bird(beg + .6, .10, 3000, 1200, .2, trill, main_amp)
    bird(beg + .72, .05, 3000, 800, .2, w_up, main_amp)
    bird(beg + .8, .10, 3000, 1200, .2, trill, main_amp)
    bird(beg + .92, .05, 3000, 800, .2, w_up, main_amp)
    bird(beg + 1.00, .01, 3900, 600, .1, w_up, main_amp)
    bird(beg + 1.01, .01, 3910, 800, .1, w_up, main_amp)
    bird(beg + 1.02, .01, 3940, 500, .1, w_up, main_amp)
    bird(beg + 1.03, .01, 4000, 500, .1, w_up, main_amp)
    bird(beg + 1.04, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.05, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.06, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.07, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.08, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.09, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.10, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.11, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.12, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.13, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.14, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.15, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.16, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.17, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.18, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.19, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.20, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.21, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.22, .01, 3900, 1000, .1, w_up, main_amp)
    bird(beg + 1.23, .01, 3900, 1200, .1, w_up, main_amp)
    bird(beg + 1.24, .01, 3900, 1200, .1, w_up, main_amp)
    bird(beg + 1.25, .01, 3900, 1200, .1, w_up, main_amp)
    bird(beg + 1.26, .01, 3900, 1200, .1, w_up, main_amp)
    bird(beg + 1.27, .01, 3900, 1400, .1, w_up, main_amp)
    bird(beg + 1.28, .01, 3900, 1400, .1, w_up, main_amp)
    bird(beg + 1.29, .01, 3900, 1400, .1, w_up, main_amp)
    bird(beg + 1.30, .01, 3900, 1400, .1, w_up, main_amp)
         
     
def nashville_warbler(beg):
    nash_blip = [0.0, .60, .35, 1.0, 1.0, .0]
    nash_down = [0.0, .90, .05, 1.0, .10, .90, .65, .50, 1.0, .0]
    nash_up = [0.0, 0.0, .15, .20, .25, .05, .90, .95, 1.0, 1.0]
    nash_amp = [0.0, 0.0, .80, 1.0, 1.0, .0]
    beg = beg - .15
    bird(beg + .15, .025, 3900, 300, .3, nash_blip, main_amp)
    bird(beg + .24, .16, 4200, 3800, .15, nash_down, nash_amp)
    bird(beg + .42, .025, 3900, 300, .3, nash_blip, main_amp)
    bird(beg + .55, .14, 4300, 3700, .15, nash_down, nash_amp)
    bird(beg + .75, .03, 3950, 350, .3, nash_blip, main_amp)
    bird(beg + .81, .17, 4200, 3900, .175, nash_down, main_amp)
    bird(beg + 1.0, .02, 3800, 400, .25, nash_blip, main_amp)
    bird(beg + 1.11, .14, 4200, 3800, .165, nash_down, nash_amp)
    bird(beg + 1.3, .03, 3750, 300, .2, nash_blip, main_amp)
    bird(beg + 1.4, .11, 4200, 3700, .1, nash_down, main_amp)
    bird(beg + 1.57, .1, 3800, 2200, .1, nash_up, main_amp)
    bird(beg + 1.7, .1, 3800, 2150, .125, nash_up, main_amp)
    bird(beg + 1.85, .075, 3900, 1800, .1, nash_up, nash_amp)
         
     
def eastern_phoebe(beg):
    phoebe_amp = [0.0, 0.0, .10, 1.0, 1.0, .0]
    bird(beg, .225, 3000, 1300, .3, [
        0.0, 0.0, .30, .30, .35, .50, .55, .40, .70, .80, .75, .70,
        .80, 1.0, .95, .90, 1.0, .0], main_amp)
    bird(beg + .35, .12, 3000, 500, .1, [
        0.0, 0.0, .50, 1.0, 1.0, .0], phoebe_amp)
    bird(beg + .4, .10, 3000, 1500, .2, [
        0.0, 0.0, .10, .40, .80, 1.0, 1.0, .10], phoebe_amp)
    bird(beg + .55, .05, 3000, 1400, .2,
             [0.0, 1.0, .50, .70, 1.0, .0], phoebe_amp)
         
     
def painted_bunting(beg):
    b_one = [0.0, 0.0, 1.0, 1.0]
    beg = beg - .05
    bird(beg + .05, .10, 3100, 900, .05, b_one, [0.0, 0.0, .90, 1.0, 1.0, .0])
    bird(beg + .21, .07, 4100, 700, .15, [0.0, 1.0, 1.0, .0], main_amp)
    bird(beg + .36, .12, 3700, 1000, .20, [0.0, 0.0, .50, 1.0, 1.0, .0], main_amp)
    bird(beg + .52, .08, 2300, 1600, .15,
	      [0.0, .70, .15, 0.0, .40, 1.0, .80, 1.0, 1.0, .50],
	      [0.0, 0.0, .10, .50, .15, 0.0, .40, 1.0, .90, 1.0, 1.0, .0])
    bird(beg + .68, .1, 4000, 1000, .25, b_one, bird_tap)
    bird(beg + .8, .12, 2300, 1700, .2, [0.0, 1.0, .25, .40, .75, .50, 1.0, .0], main_amp)
    bird(beg + .96, .15, 3800, 2200, .3,
	      [0.0, .30, .40, .40, .50, 1.0, .60, .20, 1.0, .0],
	      [0.0, 0.0, .05, 1.0, .30, 1.0, .50, .30, .90, 1.0, 1.0, .0])
    bird(beg + 1.18, .1, 2300, 1600, .15, [
        0.0, .40, .25, 0.0, .35, 1.0, .50, 0.0, .65, 1.0, .75, 0.0, .85, 1.0, 1.0, .0], main_amp)
    b_eleven = [0.0, 1.0, 1.0, .0]
    bird(beg + 1.3, .02, 3200, 1000, .1, b_eleven, main_amp)
    bird(beg + 1.33, .02, 3200, 1000, .1, b_eleven, main_amp)
    bird(beg + 1.36, .02, 3200, 1000, .1, b_eleven, main_amp)
    bird(beg + 1.40, .03, 4000, 2000, .12,
	      [0.0, 0.0, .50, 1.0, 1.0, .50],
	      [0.0, 0.0, .05, 1.0, .30, .20, .60, .20, .90, 1.0, 1.0, .0])
    bird(beg + 1.47, .1, 2300, 1700, .2,
	      [0.0, .30, .30, 1.0, .60, .30, 1.0, .0],
	      [0.0, 0.0, .10, .50, .50, .50, .90, 1.0, 1.0, .0])
         
     
def western_flycatcher(beg):
    f_one = [0.0, 0.0, .10, 1.0, .20, .40, .95, .10, 1.0, .0]
    a_one = [0.0, 0.0, .10, .20, .20, .10, .30, 1.0, .90, 1.0, 1.0, .0]
    f_two = [0.0, .50, .25, 1.0, .50, 0.0, .60, 0.0, .95, .30, 1.0, .60]
    a_two = [0.0, 0.0, .10, 1.0, .20, 1.0, .50, .10, .60, .10, .90, 1.0, 1.0, .0]
    bigbird(beg,      .2, 2000, 2200, .2, f_one, a_one, [1, 1, 2, .02, 3, .1, 4, .01])
    bigbird(beg + .3, .2, 2000, 1100, .2, f_two, a_two, [1, 1, 2, .02, 3, .1, 4, .01])
         
     
def bachmans_sparrow(beg):
    sup = [0.0, .10, .35, 0.0, 1.0, 1.0]
    sdwn = [0.0, 1.0, .40, .50, 1.0, .0]
    bird(beg,  .51, 4900, 200, .3, [0.0, 1.0, .10, .50, .90, .50, 1.0, .0], main_amp)
    bird(beg + .52, .015, 3800, 200, .1, sup, main_amp)
    bird(beg + .52, .015, 3750, 250, .1, sup, main_amp)
    bird(beg + .54, .015, 3600, 300, .1, sup, main_amp)
    bird(beg + .56, .015, 3500, 250, .1, sup, main_amp)
    bird(beg + .58, .015, 3400, 200, .1, sup, main_amp)
    bird(beg + .60, .015, 3200, 200, .1, sup, main_amp)
    bird(beg + .62, .015, 3800, 100, .1, sup, main_amp)
    bird(beg + .65, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + .73, .03, 5000, 1000, .1, sdwn, main_amp)
    bird(beg + .80, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + .88, .03, 5000, 1000, .1, sdwn, main_amp)
    bird(beg + .95, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + 1.03, .03, 5000, 1000, .1, sdwn, main_amp)
    bird(beg + 1.10, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + 1.18, .03, 5000, 1000, .1, sdwn, main_amp)
    bird(beg + 1.25, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + 1.33, .03, 5000, 1000, .1, sdwn, main_amp)
    bird(beg + 1.40, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + 1.48, .03, 5000, 1000, .1, sdwn, main_amp)
    bird(beg + 1.55, .07, 3000, 750, .2, sup, main_amp)
    bird(beg + 1.63, .03, 5000, 1000, .1, sdwn, main_amp)
    supn = [0.0, 0.0, 1.0, 1.0]
    bird(beg + 2.8, .06, 4000, 1700, .1, supn, main_amp)
    bird(beg + 2.87, .01, 5200, 0, .2, supn, main_amp)
    bird(beg + 2.9, .06, 4000, 1700, .1, supn, main_amp)
    bird(beg + 2.97, .01, 5200, 0, .2, supn, main_amp)
    bird(beg + 3.0, .06, 4000, 1700, .1, supn, main_amp)
    bird(beg + 3.07, .01, 5200, 0, .2, supn, main_amp)
    bird(beg + 3.1, .06, 4000, 1700, .1, supn, main_amp)
    bird(beg + 3.17, .01, 5200, 0, .2, supn, main_amp)
    bird(beg + 3.2, .06, 4000, 1700, .1, supn, main_amp)
    bird(beg + 3.27, .01, 5200, 0, .2, supn, main_amp)
    slast = [0.0, 1.0, .25, 0.0, .75, .40, 1.0, .50]
    bird(beg + 3.4, .15, 3000, 1000, .2, slast, main_amp)
    bird(beg + 3.6, .15, 3000, 1000, .2, slast, main_amp)
    bird(beg + 3.8, .15, 3000, 1000, .2, slast, main_amp)
    bird(beg + 4.0, .15, 3000, 1000, .2, slast, main_amp)
    bird(beg + 4.2, .15, 3000, 1000, .2, slast, main_amp)
    bird(beg + 4.4, .15, 3000, 1000, .2, slast, main_amp)
         
     
def cedar_waxwing(beg):
    bird(beg, .50, 6000, 800, .2,
            [0.0, 0.0, .25, .70, .70, 1.0, .90, 1.0, 1.0, .20],
	        [0.0, 0.0, .20, 1.0, .40, 1.0, 1.0, .0])
         

def bairds_sparrow(beg):
    bairdend = [0.0, 0.0, .25, 1.0, .50, 0.0, .75, 1.0, 1.0, .0]
    bairdstart = [0.0, .50, .05, 1.0, .10, 0.0, .15, 1.0, .20, 0.0, .25, 1.0,
                  .30, 0.0, .35, 1.0, .40, 0.0, .45, 1.0,
                  .50, 0.0, .55, 1.0, .60, 0.0, .65, 1.0, .70, 0.0, .75, 1.0,
                  .80, 0.0, .85, 1.0, .90, 0.0, .95, 1.0, 1.0, .0]
    bird(beg, .09, 6500, 1500, .2, bairdstart, main_amp)
    bird(beg + .22, .01, 5900, 100, .2, bairdend, main_amp)
    bird(beg + .25, .09, 6000, 1000, .2, bairdstart, main_amp)
    bird(beg + .45, .01, 4200, 100, .2, bairdend, main_amp)
    bird(beg + .50, .08, 4200, 600, .2, bairdstart, main_amp)
    bird(beg + .59, .01, 4400, 100, .2, bairdend, main_amp)
    bird(beg + .60, .01, 4400, 100, .2, bairdend, main_amp)
    bird(beg + .68, .07, 5400, 700, .2, bairdstart, main_amp)
    bird(beg + .75, .01, 4200, 100, .2, bairdend, main_amp)
    bird(beg + .79, .01, 4400, 100, .2, bairdend, main_amp)
    bird(beg + .83, .01, 4200, 100, .19, bairdend, main_amp)
    bird(beg + .87, .01, 4400, 100, .19, bairdend, main_amp)
    bird(beg + .91, .01, 4200, 100, .18, bairdend, main_amp)
    bird(beg + .95, .01, 4400, 100, .18, bairdend, main_amp)
    bird(beg + .99, .01, 4200, 100, .17, bairdend, main_amp)
    bird(beg + 1.03, .01, 4400, 100, .17, bairdend, main_amp)
    bird(beg + 1.07, .01, 4200, 100, .16, bairdend, main_amp)
    bird(beg + 1.11, .01, 4400, 100, .16, bairdend, main_amp)
    bird(beg + 1.15, .01, 4200, 100, .15, bairdend, main_amp)
    bird(beg + 1.19, .01, 4400, 100, .15, bairdend, main_amp)
    bird(beg + 1.23, .01, 4200, 100, .14, bairdend, main_amp)
    bird(beg + 1.27, .01, 4400, 100, .14, bairdend, main_amp)
    bird(beg + 1.31, .01, 4200, 100, .13, bairdend, main_amp)
    bird(beg + 1.35, .01, 4400, 100, .13, bairdend, main_amp)
    bird(beg + 1.39, .01, 4200, 100, .12, bairdend, main_amp)
    bird(beg + 1.43, .01, 4400, 100, .12, bairdend, main_amp)
    bird(beg + 1.47, .01, 4200, 100, .11, bairdend, main_amp)
    bird(beg + 1.51, .01, 4400, 100, .11, bairdend, main_amp)
    bird(beg + 1.55, .01, 4200, 100, .10, bairdend, main_amp)
    bird(beg + 1.59, .01, 4400, 100, .10, bairdend, main_amp)
    bird(beg + 1.63, .01, 4200, 100, .09, bairdend, main_amp)
    bird(beg + 1.67, .01, 4400, 100, .09, bairdend, main_amp)
    bird(beg + 1.71, .01, 4200, 100, .08, bairdend, main_amp)
    bird(beg + 1.75, .01, 4400, 100, .08, bairdend, main_amp)
    bird(beg + 1.79, .01, 4200, 100, .07, bairdend, main_amp)
    bird(beg + 1.83, .01, 4400, 100, .07, bairdend, main_amp)
    bird(beg + 1.87, .01, 4200, 100, .06, bairdend, main_amp)
    bird(beg + 1.92, .01, 4400, 100, .06, bairdend, main_amp)
    bird(beg + 1.97, .01, 4200, 100, .05, bairdend, main_amp)
         
     
def kentucky_warbler(beg):
    kenstart	 = [0.0, .30, .50, 1.0, 1.0, .0]
    kendwn = [0.0, .90, .10, 1.0, 1.0, .0]
    kentrill = [0.0, 1.0, .25, 0.0, .50, 0.0, .75, 1.0, 1.0, .0]
    beg = beg - .6
    bigbird(beg + .6, .02, 3800, 200, .05, kenstart, main_amp, [1, 1, 2, .03])
    bigbird(beg + .65, .03, 4300, 200, .15, [0.0, 0.0, 1.0, 1.0], main_amp, [1, 1, 2, .1])
    bigbird(beg + .73, .02, 3200, 100, .1, kendwn, main_amp, [1, 1, 2, .1])
	
    bigbird(beg + .75, .05, 3000, 800, .15, kenstart, main_amp, [1, 1, 2, .01])
    bigbird(beg + .82, .06, 3100, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + .90, .06, 3200, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + .98, .05, 4600, 100, .2, kentrill, main_amp, [1, 1, 2, .1])
	
    bigbird(beg + 1.10, .05, 2900, 800, .15, kenstart, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.17, .06, 3000, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.25, .06, 3100, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.33, .05, 4600, 100, .2, kentrill, main_amp, [1, 1, 2, .1])
	
    bigbird(beg + 1.43, .05, 2800, 800, .15, kenstart, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.50, .05, 2700, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.57, .06, 2800, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.64, .05, 4600, 100, .2, kentrill, main_amp, [1, 1, 2, .1])
	
    bigbird(beg + 1.75, .05, 2700, 800, .15, kenstart, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.81, .05, 2600, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.88, .06, 2600, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 1.97, .05, 4600, 100, .2, kentrill, main_amp, [1, 1, 2, .1])
	
    bigbird(beg + 2.05, .05, 2700, 800, .15, kenstart, main_amp, [1, 1, 2, .01])
    bigbird(beg + 2.12, .06, 2600, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 2.20, .05, 4600, 100, .2, kentrill, main_amp, [1, 1, 2, .1])
	
    bigbird(beg + 2.30, .05, 2800, 800, .15, kenstart, main_amp, [1, 1, 2, .01])
    bigbird(beg + 2.37, .06, 2700, 1200, .1, kendwn, main_amp, [1, 1, 2, .01])
    bigbird(beg + 2.45, .05, 4700, 100, .25, kentrill, main_amp, [1, 1, 2, .1])

  
def rufous_sided_towhee(beg):
    towhee_two = [0.0, 0.0, 1.0, 1.0]
    towhee_three = [0.0, 1.0, 1.0, .0]
    beg = beg - .25
    towhee_one = [0.0, .10, .02, .05, .04, .15, .06, .05, .08, .20, .10, .04, .12, .25, .14,
                  .03, .16, .30, .18, .02, .20, .35, .22, .01, .24,
                  .40, .26, 0.0, .28, .45, .30, 0.0, .32, .50, .34, 0.0, .36, .50, .80, 1.0, 1.0, .0]
    bigbird(beg + .25, .13, 1400, 1100, .2, towhee_one, main_amp, [1, .03, 2, 1, 3, .03])
    bigbird(beg + .45, .13, 1400, 1100, .2, towhee_one, main_amp, [1, .03, 2, 1, 3, .03])
    bigbird(beg + .60, .13, 1400, 1100, .2, towhee_one, main_amp, [1, .03, 2, 1, 3, .03])
    bigbird(beg + .75, .10, 1400, 1100, .2, towhee_one, main_amp, [1, .03, 2, 1, 3, .03])
	
    bird(beg + .88, .01, 5100, 2000, .1, towhee_two, main_amp)
    bird(beg + .895, .01, 5100, 1600, .1, towhee_two, main_amp)
    bird(beg + .91, .01, 5100, 1000, .1, towhee_two, main_amp)
    bird(beg + .93, .01, 3000, 1200, .1, towhee_three, main_amp)
	
    bird(beg + .945, .01, 5100, 2000, .09, towhee_two, main_amp)
    bird(beg + .96, .01, 5100, 1600, .09, towhee_two, main_amp)
    bird(beg + .975, .01, 5100, 1000, .09, towhee_two, main_amp)
    bird(beg + .995, .01, 3000, 1200, .09, towhee_three, main_amp)
	
    bird(beg + 1.01, .01, 5100, 2000, .1, towhee_two, main_amp)
    bird(beg + 1.025, .01, 5100, 1600, .1, towhee_two, main_amp)
    bird(beg + 1.04, .01, 5100, 1000, .1, towhee_two, main_amp)
    bird(beg + 1.06, .01, 3000, 1200, .1, towhee_three, main_amp)
	
    bird(beg + 1.075, .01, 5100, 2000, .09, towhee_two, main_amp)
    bird(beg + 1.09, .01, 5100, 1600, .09, towhee_two, main_amp)
    bird(beg + 1.105, .01, 5100, 1000, .09, towhee_two, main_amp)
    bird(beg + 1.125, .01, 3000, 1200, .09, towhee_three, main_amp)
	
    bird(beg + 1.14, .01, 5100, 2000, .08, towhee_two, main_amp)
    bird(beg + 1.155, .01, 5100, 1600, .08, towhee_two, main_amp)
    bird(beg + 1.17, .01, 5100, 1000, .08, towhee_two, main_amp)
    bird(beg + 1.19, .01, 3000, 1200, .08, towhee_three, main_amp)
	
    bird(beg + 1.205, .01, 5100, 2000, .08, towhee_two, main_amp)
    bird(beg + 1.220, .01, 5100, 1600, .08, towhee_two, main_amp)
    bird(beg + 1.235, .01, 5100, 1000, .08, towhee_two, main_amp)
    bird(beg + 1.255, .01, 3000, 1200, .08, towhee_three, main_amp)
	
    bird(beg + 1.27, .01, 5100, 2000, .07, towhee_two, main_amp)
    bird(beg + 1.285, .01, 5100, 1600, .07, towhee_two, main_amp)
    bird(beg + 1.30, .01, 5100, 1000, .07, towhee_two, main_amp)
    bird(beg + 1.32, .01, 3000, 1200, .07, towhee_three, main_amp)
	
    bird(beg + 1.335, .01, 5100, 2000, .06, towhee_two, main_amp)
    bird(beg + 1.350, .01, 5100, 1600, .06, towhee_two, main_amp)
    bird(beg + 1.365, .01, 5100, 1000, .06, towhee_two, main_amp)
    bird(beg + 1.385, .01, 3000, 1200, .06, towhee_three, main_amp)
	
    bird(beg + 1.400, .01, 5100, 2000, .05, towhee_two, main_amp)
    bird(beg + 1.415, .01, 5100, 1600, .05, towhee_two, main_amp)
    bird(beg + 1.430, .01, 5100, 1000, .05, towhee_two, main_amp)
    bird(beg + 1.45, .01, 3000, 1200, .05, towhee_three, main_amp)
	
    bird(beg + 1.465, .01, 5100, 2000, .03, towhee_two, main_amp)
    bird(beg + 1.480, .01, 5100, 1600, .03, towhee_two, main_amp)
    bird(beg + 1.495, .01, 5100, 1000, .03, towhee_two, main_amp)
    bird(beg + 1.515, .01, 3000, 1200, .03, towhee_three, main_amp)

  
def prothonotary_warbler(beg):
    pro_one = [0.0, .10, .20, 0.0, 1.0, 1.0]
    pro_two = [0.0, 0.0, 1.0, 1.0]
    pro_amp = [0.0, 0.0, .20, 1.0, .40, .50, 1.0, .0]
    beg = beg - .76
    bird(beg + .76, .08, 3000, 3000, .05, pro_one, pro_amp)
    bird(beg + .85, .05, 4000, 2500, .06, pro_two, bird_amp)
    bird(beg + 1.02, .09, 3000, 3000, .10, pro_one, pro_amp)
    bird(beg + 1.12, .05, 4000, 2500, .10, pro_two, bird_amp)
    bird(beg + 1.26, .08, 3000, 3000, .15, pro_one, pro_amp)
    bird(beg + 1.35, .05, 4000, 2500, .16, pro_two, bird_amp)
    bird(beg + 1.54, .08, 3000, 3000, .20, pro_one, pro_amp)
    bird(beg + 1.63, .05, 4000, 2500, .19, pro_two, bird_amp)
    bird(beg + 1.80, .08, 3000, 3000, .20, pro_one, pro_amp)
    bird(beg + 1.89, .05, 4000, 2500, .16, pro_two, bird_amp)
    bird(beg + 2.03, .08, 3000, 3000, .15, pro_one, pro_amp)
    bird(beg + 2.12, .05, 4000, 2500, .10, pro_two, bird_amp)
    bird(beg + 2.30, .08, 3000, 3000, .10, pro_one, pro_amp)
    bird(beg + 2.39, .05, 4000, 2500, .06, pro_two, bird_amp)
            
     
def audubons_warbler(beg):
    w_up =[0.0, 0.0, 1.0, 1.0]
    w_down = [0.0, 1.0, 1.0, .0]
    w_updown = [0.0, .10, .50, 1.0, 1.0, .0]
    beg = beg - .75
    bird(beg + .75, .04, 2400, 200, .05, w_down, bird_amp)
    bird(beg + .83, .03, 3200, 200, .1, w_up, bird_amp)
    bird(beg + .90, .04, 2500, 300, .15, w_up, bird_amp)
    bird(beg + .97, .04, 2300, 600, .15, w_down, bird_amp)
    bird(beg + 1.02, .03, 3500, 400, .20, w_up, bird_amp)
    bird(beg + 1.06, .04, 2300, 1200, .10, w_up, bird_amp)
    bird(beg + 1.13, .05, 2300, 1200, .15, w_down, bird_amp)
    bird(beg + 1.22, .02, 3200, 800, .25, w_up, bird_amp)
    bird(beg + 1.25, .08, 2400, 600, .20, w_updown, bird_amp)
    bird(beg + 1.35, .02, 2200, 400, .10, w_up, bird_amp)
    bird(beg + 1.38, .07, 2400, 1400, .15, w_down, bird_amp)
    bird(beg + 1.47, .03, 3000, 800, .20, w_up, bird_amp)
    bird(beg + 1.50, .03, 2500, 400, .10, w_updown, bird_amp)
    bird(beg + 1.55, .01, 2300, 100, .05, w_up, bird_amp)
    bird(beg + 1.56, .06, 2200, 1400, .15, w_down, bird_amp)
    bird(beg + 1.65, .03, 3100, 800, .10, w_up, bird_amp)
    bird(beg + 1.70, .07, 2800, 800, .15, w_updown, bird_amp)
    bird(beg + 1.79, .06, 2400, 1000, .10, w_down, bird_amp)
    w_end = [0.0, 0.0, .15, 1.0, .45, .90, .50, 0.0, .55, 1.0, .90, .90, 1.0, .10]
    bird(beg + 1.86, .14, 3100, 900, .25, w_end, bird_amp)
    bird(beg + 2.02, .12, 3200, 800, .20, w_end, bird_amp)


def lark_bunting(beg):
    b_down = [0.0, 1.0, 1.0, .0]
    b_up = [0.0, 0.0, 1.0, 1.0]
    beg = beg - .1
    bird(beg + .1, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + .2, .12, 3700, 400, .2, b_up, bird_amp)
    bird(beg + .4, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + .45, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + .51, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + .6, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + .65, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + .71, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + .8, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + .85, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + .91, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + 1.0, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + 1.05, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + 1.11, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + 1.2, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + 1.25, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + 1.31, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + 1.4, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + 1.45, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + 1.51, .03, 1800, 100, .1, b_up, bird_amp)
    bird(beg + 1.6, .03, 4100, 500, .15, b_down, bird_amp)
    bird(beg + 1.65, .05, 2000, 400, .20, b_down, bird_amp)
    bird(beg + 1.71, .03, 1800, 100, .1, b_up, bird_amp)
         
    
def eastern_bluebird(beg):
    blue_one = [0.0, 0.0, 1.0, 1.0]
    beg = beg - .75
    bird(beg + .75, .02, 2000, 1600, .1, blue_one, bird_amp)
    bird(beg + .80, .02, 2000, 1600, .1, blue_one, bird_amp)
    bird(beg + .86, .02, 2000, 1600, .1, blue_one, bird_amp)
    bird(beg + 1.00, .13, 2000, 1400, .2, [0.0, 1.0, 1.0, .0], bird_amp)
    bird(beg + 1.20, .24, 2000, 800, .2, [
        0.0, .60, .10, 1.0, .20, 0.0, .25, 1.0, .30, 0.0, .35, 1.0, .40,
        0.0, .45, 1.0, .50, 0.0, .75, 1.0, 1.0, .0], bird_amp)
    bird(beg + 1.68, .03, 2200, 400, .1, blue_one, bird_amp)
    bird(beg + 1.72, .10, 1950, 100, .15, [0.0, 0.0, .50, 1.0, 1.0, .0], bird_amp)
    bird(beg + 1.96, .15, 2000, 600, .20, [
        0.0, .50, .10, 1.0, .20, 0.0, .35, 1.0, .50, 0.0, .65, 1.0, 
        .80, 0.0, .95, 1.0, 1.0, .50], bird_amp)
         

def chuck_wills_widow(beg):
    bird(beg, .03, 1000, 800, .1, [0.0, 1.0, 1.0, .0], bird_amp)
    bird(beg + .27, .20, 1000, 1000, .2, [
        0.0, 0.0, .10, .10, .25, 1.0, .50, .30, .80, .70, 1.0, .0], bird_amp)
    bird(beg + .51, .29, 900, 1100, .2, [
        0.0, .20, .30, 1.0, .50, .30, .60, .70, .90, .10, 1.0, .0], bird_amp)
         
     
def blue_gray_gnatcatcher(beg):
    gskw1 = [0.0, 0.0, .15, 1.0, .75, .80, .90, 1.0, 1.0, .70]
    gskw2 = [0.0, 0.0, .25, 1.0, .75, .70, 1.0, .0]
    beg = beg - .5
    bigbird(beg + .5, .20, 4000, 1000, .2, gskw1, bird_amp, [1, .4, 2, 1, 3, .1])
    bigbird(beg + .8, .13, 4000, 800, .2, gskw2, bird_amp, [1, .4, 2, 1, 3, .2])

    bigbird(beg + 1.4, .25, 4000, 800, .2, gskw2, bird_amp, [1, .4, 2, 1, 3, .3])
    bigbird(beg + 1.80, .17, 4000, 900, .2, gskw1, bird_amp, [1, .4, 2, 1, 3, .3])
    bigbird(beg + 2.00, .17, 4000, 700, .2, gskw1, bird_amp, [1, .4, 2, 1, 3, .3])
    bigbird(beg + 2.20, .17, 4000, 800, .2, gskw2, bird_amp, [1, .4, 2, 1, 3, .3])
                  
    
def black_throated_sparrow(beg):
    black_up = [0.0, 0.0, 1.0, 1.0]
    black_amp = [0.0, 0.0, .50, 1.0, 1.0, .0]
    beg = beg - .8
    black_down = [0.0, 1.0, 1.0, .0]
    bird(beg + .8, .02, 2200, 1000, .1, black_down, bird_amp)
    bird(beg + .83, .01, 3000, 200, .05, black_up, bird_amp)
    bird(beg + .96, .02, 5800, 500, .05, black_up, bird_amp)
    bird(beg + 1.00, .02, 4000, 200, .05, black_up, bird_amp)
    bird(beg + 1.04, .10, 2100, 1700, .15, black_down,
           [0.0, 0.0, .75, 1.0, 1.0, .0])
    bird(beg + 1.15, .05, 5700, 400, .25, black_up, bird_amp)
    bird(beg + 1.25, .25, 2000, 900, .2, [
        0.0, 0.0, .03, .70, .06, 0.0, .09, .75, .12, 0.0, .15, .80, .18, .05,
        .21, .85, .24, .10, .27, .90, .30, .10, .33, 1.0, .36, .10, .39, 1.0,
        .42, .10, .45, 1.0, .48, .10, .51, 1.0, .54, .10, .57, 1.0, .60, .10,
        .63, 1.0, .66, .10, .69, 1.0, .72, .10, .75, 1.0, .78, .10, .81, 1.0,
        .84, .10, .87, 1.0, .90, 0.0, .93, .95, .96, 0.0, 1.0, .90], bird_amp)
    bird(beg + 1.52, .05, 5600, 400, .15, [0.0, 0.0, .50, 1.0, 1.0, .20], bird_amp)
    bird(beg + 1.6, .04, 3900, 1100, .15, black_up, bird_amp)
    bird(beg + 1.66, .01, 1900, 100, .10, black_up, black_amp)
    bird(beg + 1.69, .01, 3600, 300, .10, black_up, black_amp)
    bird(beg + 1.71, .03, 3900, 1000, .15, black_up, black_amp)
    bird(beg + 1.74, .02, 5000, 100, .20, black_up, black_amp)
    bird(beg + 1.76, .01, 1900, 100, .10, black_up, black_amp)
    bird(beg + 1.78, .01, 3600, 300, .10, black_up, black_amp)
    bird(beg + 1.80, .03, 3900, 1000, .15, black_up, black_amp)
    bird(beg + 1.83, .02, 5000, 100, .20, black_up, black_amp)
    bird(beg + 1.85, .01, 1900, 100, .10, black_up, black_amp)
    bird(beg + 1.87, .01, 3600, 300, .10, black_up, black_amp)
    bird(beg + 1.89, .03, 3900, 1000, .15, black_up, black_amp)
    bird(beg + 1.92, .02, 5000, 100, .20, black_up, black_amp)
    bird(beg + 1.94, .01, 1900, 100, .10, black_up, black_amp)
    bird(beg + 1.96, .01, 3600, 300, .10, black_up, black_amp)
    bird(beg + 1.98, .03, 3900, 1000, .15, black_up, black_amp)
    bird(beg + 2.01, .02, 5000, 100, .20, black_up, black_amp)
    bird(beg + 2.03, .01, 1900, 100, .10, black_up, black_amp)
    bird(beg + 2.05, .01, 3600, 300, .10, black_up, black_amp)
    bird(beg + 2.07, .03, 3900, 1000, .15, black_up, black_amp)
    bird(beg + 2.10, .02, 5000, 100, .20, black_up, black_amp)
    bird(beg + 2.13, .01, 1900, 100, .10, black_up, black_amp)
    bird(beg + 2.16, .03, 3800, 300, .1, black_up, bird_amp)


def black_chinned_sparrow(beg):
    chin_up = [0.0, 0.0, 1.0, 1.0]
    beg = beg - .6
    bird(beg + .6, .2, 4200, 100, .1, chin_up, bird_amp)
    chin_up2 = [0.0, 0.0, .30, .20, 1.0, 1.0]
    bird(beg + 1.0,  .09, 3800, 2000, .1, chin_up2, bird_amp)
    bird(beg + 1.25, .08, 3900, 1700, .12, chin_up2, bird_amp)
    bird(beg + 1.40, .08, 3600, 2300, .13, chin_up, bird_amp)
    bird(beg + 1.50, .11, 3100, 2800, .14, chin_up, bird_amp)
    bird(beg + 1.65, .07, 2900, 2700, .15, chin_up, bird_amp)
    bird(beg + 1.74, .07, 2900, 2700, .15, chin_up, bird_amp)
    bird(beg + 1.82, .07, 3000, 2300, .13, chin_up, bird_amp)
    bird(beg + 1.89, .07, 3200, 2000, .10, chin_up, bird_amp)
    bird(beg + 1.97, .05, 3200, 1500, .10, chin_up, bird_amp)
    bird(beg + 2.04, .04, 3400, 1000, .07, chin_up, bird_amp)
    bird(beg + 2.10, .03, 3600, 700, .05, chin_up, bird_amp)
    bird(beg + 2.15, .03, 3800, 300, .05, chin_up, bird_amp)
    bird(beg + 2.19, .02, 3900, 100, .03, chin_up, bird_amp)
    bird(beg + 2.22, .01, 3900, 100, .01, chin_up, bird_amp)
    bird(beg + 2.24, .01, 3900, 100, .01, chin_up, bird_amp)


def various_gull_cries_from_end_of_colony_5(beg):
    gullstart = [0, 0, 10, 1, 20, .5000, 40, .6000, 60, .5000, 100, 0]
    gullend = [0, 0, 5, 1, 10, .5000, 90, .4000, 100, 0]
    gull_frq = [1,  .1,  2,  1,  3,  .1,  4,  .01,  5,  .09,  6,  .01,  7,  .01]
    beg =  beg - .25
    bigbird(beg + .250, .80,  1180,  1180,  .08, gullend, bird_amp, gull_frq)
    bigbird(beg + 1.500, .90,  1180,  1180,  .07, gullend, bird_amp, gull_frq)
    bigbird(beg + 2.750, 1.0,  1050,  1050,  .08, gullend, bird_amp, gull_frq)
    bigbird(beg + 4.800, .05,  1180, 1180,  .06, gullstart, bird_amp, gull_frq)
    bigbird(beg + 4.950, .10,  1180, 1180,  .08, gullstart, bird_amp, gull_frq)
    bigbird(beg + 5.150, .10,  1180, 1180,  .09, gullstart, bird_amp, gull_frq)
    bigbird(beg + 5.350, .10,  1180, 1180,  .1,
                [0, 0, 10, 1, 30, .5000, 80, .5000, 100, 0], bird_amp, gull_frq)
    bigbird(beg + 5.450, .40,  1050,  1050,  .1, gullend, bird_amp, gull_frq)
    bigbird(beg + 6.250, .80,  1050,  1050,  .1, gullend, bird_amp, gull_frq)
    bigbird(beg + 7.450, 1.80,  1050,  1050,  .1, gullend, bird_amp, gull_frq)

# Bill's original bird score
birdcalls = [
    [orchard_oriole, 0],
    [cassins_kingbird, 3],
    [chipping_sparrow, 6],
    [bobwhite, 9],
    [western_meadowlark, 12],
    [scissor_tailed_flycatcher, 15],
    [great_horned_owl, 18],
    [black_throated_gray_warbler, 21],
    [yellow_warbler, 24],
    [black_necked_stilt, 27],
    [chestnut_sided_warbler, 30],
    [grasshopper_sparrow,   33],
    [swamp_sparrow, 36],
    [golden_crowned_sparrow, 39],
    [indigo_bunting, 42],
    [hooded_warbler, 45],
    [american_widgeon, 48],
    [louisiana_waterthrush, 51],
    [robin, 54],
    [solitary_vireo, 57],
    [pigeon_hawk, 61],
    [cerulean_warbler, 64],
    [nashville_warbler, 67],
    [eastern_phoebe, 70],
    [painted_bunting, 73],
    [western_flycatcher, 76],
    [bachmans_sparrow, 79],
    [cedar_waxwing, 82],
    [bairds_sparrow, 85],
    [kentucky_warbler, 88],
    [rufous_sided_towhee, 91],
    [prothonotary_warbler, 94],
    [audubons_warbler, 97],
    [lark_bunting, 100],
    [eastern_bluebird, 103],
    [chuck_wills_widow, 106],
    [blue_gray_gnatcatcher, 109],
    [black_throated_sparrow, 112],
    [black_chinned_sparrow, 115],
    [various_gull_cries_from_end_of_colony_5, 118]
    ]
    
#==================================================================================
# THE REMAINDER OF THIS FILE IS JUST SUPPORT CODE FOR BUILDING THE NOTEBOOK

def birdcode(birdname):
    """Parse out the text code for a given bird defined in this file."""
    bird, text = False, ""
    with open("birds.py") as file:
        for line in file:
            if line.startswith("def"):
                x = line.split()
                if len(x) > 1 and x[0] == "def" and x[1].startswith(birdname):
                    text = line
                    bird = True
            elif bird and len(line) == 0 or line[0] in [" ", "#", "\t"]:
                if line[0] != "#":
                    text += line
            elif bird:
                break
    return text
                

def birdcall(birdfunc, play=True, speed=1):
    """Perform one bird call."""
    if not .125 <= speed <= 1:
        raise ValueError(f"birdcall(): Audio speed '{speed}' not between .125 and 1.")
    path = pathlib.Path(audiodir) / (birdfunc.__name__ + ".wav")
    if speed == 1:
        with CLM.Sound(str(path), play=True):
            birdfunc(0)
    elif not path.exists():
        raise Exception("birdcall(): Generate with speed=1 before reducing.")
    else:
        # No way to replay at lower srate so copy the audio to a new file
        # and set its header to the slower srate.
        array, srate = CLM.file2ndarray(str(path))
        path = path.with_name(birdfunc.__name__ + "_" + str(speed) + ".wav")
        with CLM.Sound(str(path), play=True, srate=int(srate*speed)):
            for i in range(len(array[0])):
                CLM.outa(i,array[0][i])
    print("path:", str(path))


def allbirdcalls():
    """Performs the original score from Bill's bird.scm"""
    path = pathlib.Path(audiodir) / "allbirdcalls.wav"
    with CLM.Sound(str(path), play=True):
        for bird,time in birdcalls:
            bird(time)
    print("path:", str(path))

##=========================================================================
## SOURCES FOR GENERATING THE CELLS IN THE NOTEBOOK
# funcnames='''orchard_oriole
# cassins_kingbird
# chipping_sparrow
# bobwhite
# western_meadowlark
# scissor_tailed_flycatcher
# great_horned_owl
# black_throated_gray_warbler
# yellow_warbler
# black_necked_stilt
# chestnut_sided_warbler
# grasshopper_sparrow
# swamp_sparrow
# golden_crowned_sparrow
# indigo_bunting
# hooded_warbler
# american_widgeon
# louisiana_waterthrush
# robin
# solitary_vireo
# pigeon_hawk
# cerulean_warbler
# nashville_warbler
# eastern_phoebe
# painted_bunting
# western_flycatcher
# bachmans_sparrow
# cedar_waxwing
# bairds_sparrow
# kentucky_warbler
# rufous_sided_towhee
# prothonotary_warbler
# audubons_warbler
# lark_bunting
# eastern_bluebird
# chuck_wills_widow
# blue_gray_gnatcatcher
# black_throated_sparrow
# black_chinned_sparrow
# various_gull_cries_from_end_of_colony_5'''

# sitenames='''https://www.allaboutbirds.org/guide/orchard_oriole
# https://www.allaboutbirds.org/guide/cassins_kingbird
# https://www.allaboutbirds.org/guide/chipping_sparrow
# https://www.allaboutbirds.org/guide/northern_bobwhite
# https://www.allaboutbirds.org/guide/western_meadowlark
# https://www.allaboutbirds.org/guide/scissor-tailed_flycatcher
# https://www.allaboutbirds.org/guide/great_horned_owl
# https://www.allaboutbirds.org/guide/black-throated_gray_warbler
# https://www.allaboutbirds.org/guide/yellow_warbler
# https://www.allaboutbirds.org/guide/black-necked_stilt
# https://www.allaboutbirds.org/guide/chestnut-sided_warbler
# https://www.allaboutbirds.org/guide/grasshopper_sparrow
# https://www.allaboutbirds.org/guide/swamp_sparrow
# https://www.allaboutbirds.org/guide/golden-crowned_sparrow
# https://www.allaboutbirds.org/guide/indigo_bunting
# https://www.allaboutbirds.org/guide/hooded_warbler
# https://www.allaboutbirds.org/guide/american_widgeon
# https://www.allaboutbirds.org/guide/louisiana_waterthrush
# https://www.allaboutbirds.org/guide/american_robin
# https://www.allaboutbirds.org/guide/Blue-headed_Vireo
# https://www.allaboutbirds.org/guide/merlin
# https://www.allaboutbirds.org/guide/cerulean_warbler
# https://www.allaboutbirds.org/guide/nashville_warbler
# https://www.allaboutbirds.org/guide/eastern_phoebe
# https://www.allaboutbirds.org/guide/painted_bunting
# https://www.allaboutbirds.org/guide/western_flycatcher
# https://www.allaboutbirds.org/guide/bachmans_sparrow
# https://www.allaboutbirds.org/guide/cedar_waxwing
# https://www.allaboutbirds.org/guide/bairds_sparrow
# https://www.allaboutbirds.org/guide/kentucky_warbler
# https://www.allaboutbirds.org/guide/Eastern_Towhee
# https://www.allaboutbirds.org/guide/prothonotary_warbler
# https://www.allaboutbirds.org/guide/Yellow-rumped_Warbler
# https://www.allaboutbirds.org/guide/lark_bunting
# https://www.allaboutbirds.org/guide/eastern_bluebird
# https://www.allaboutbirds.org/guide/Chuck-wills-widow
# https://www.allaboutbirds.org/guide/blue-gray_gnatcatcher
# https://www.allaboutbirds.org/guide/black-throated_sparrow
# https://www.allaboutbirds.org/guide/black-chinned_sparrow
# <nosite>'''

##=========================================================================
# FUNCTIONS FOR CREATING BIRD CELL CONTENT FOR THE NOTEBOOK
# def menuitem(funcname):
#     '''menu link to a bird at top of file (markdown cell)'''
#     birdname = " ".join(b.capitalize() for b in funcname.split('_'))
#     return f"[{birdname}](#{funcname}) |"

# def topcell(funcname):
#     '''bird name (markdown cell)''' 
#     birdname = " ".join(b.capitalize() for b in funcname.split('_'))
#     return f'''----
# <a id='{funcname}'></a>
# ### {birdname}'''

# def visitcell(funcname, sitename):
#     '''go to website (markdown cell)'''
#     birdname = " ".join(b.capitalize() for b in funcname.split('_'))
#     return f"[Visit the {birdname} webpage]({sitename}) at the Cornell Lab of Ornithology."

# def viewcell(funcname):
#     '''view code (markdown cell)'''
#     return f"View the `{funcname}()` instrument code:"

# def codecell(funcname):
#     '''display source code (code cell)'''
#     return f"Code(birds.birdcode('{funcname}'), language='python')"

# def listencell(funcname):
#     '''listen to bird (markdown cell)'''
#     return f"Listen to the `{funcname}()` instrument call:"

# def audiocell(funcname):
#     '''generate audio (code cell)'''
#     return f"birds.birdcall(birds.{funcname})"

# #for func in funcnames:  print(menuitem(func))

# THIS CODE GENERATES THE CONTENT OF THE FIVE CELLS FOR EACH BIRD (SEE BELOW)
# filename = "cells.text"
# with open(filename, 'w') as file: 
#     for func,site in zip(funcnames,sitenames):
#         file.write(topcell(func))
#         file.write("\n")
#         file.write(visitcell(func,site))
#         file.write("\n")
#         file.write(viewcell(func))
#         file.write("\n")
#         file.write(codecell(func))
#         file.write("\n")
#         file.write(listencell(func))
#         file.write("\n")
#         file.write(audiocell(func))
#         file.write("\n")
#         file.write("=====================================\n\n")
