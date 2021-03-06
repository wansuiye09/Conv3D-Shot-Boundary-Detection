import glob
import numpy as np 
from math import ceil
from clip_editor import shift_channel,shift_hue,bw,blur,artifical_flash,fade
from moviepy.editor import VideoFileClip

#different processes to edit shots and augment dataset
process=[shift_channel,shift_hue,bw,blur,artifical_flash,fade,fade]

#shot generator to create an augmented video dataset
def clip_generator(sample_vid_set,samples=10,split=.5,prob_process=.5,is_rand_sample=True):
    sample_count=0;sample=0
    process_len=len(process)
    sample_len=len(sample_vid_set)
    while (sample_count<samples):
        sample_count+=1
        if is_rand_sample:
            sample_rand=int(np.random.rand()*sample_len)-1
            #accounting for same spawn
            while sample == sample_rand:
                sample_rand=int(np.random.rand()*sample_len)-1
                print("same spawn ({},{}) changed to ({},{})".format(sample,sample,sample,sample_rand))
            sample=sample_rand
        else:
            sample = sample_count-1

        sample_vid=sample_vid_set[sample]
        try:
            clip = VideoFileClip(sample_vid,audio=True)
        except:
            print('could not load video '+ sample_vid); continue

        if np.random.rand()>=split:
            array_process=np.random.random(process_len)
            for _id,i in enumerate(array_process):
                if i>prob_process:
                    try:
                        clip=process[_id](clip)
                    except:
                        print("something went wrong..."); continue
        yield(sample_count,clip)
        







