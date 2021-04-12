import os
import sys

SAMPLE_DURATION = 20

if (len(sys.argv) < 2):
	print "No input file name provided"
	exit()

input_audio = sys.argv[1]
temp_file = 'temp_out'

command = 'mp3info -p "%S" ' + input_audio + ' > ' + temp_file
command = 'mp3info -p "%S" {0} > {1}'.format(input_audio, temp_file)

os.system(command)

file = open(temp_file)
total_sec = int(file.read())
file.close()
os.remove(temp_file)

one_sample_duration_sec = 60 * SAMPLE_DURATION
sampled_duration = 0
i = 0

while sampled_duration < total_sec:
	out_file = '{0}_{1}.mp3'.format(input_audio[:-4], i)
	command = "ffmpeg -i {0} -ss {1} -t {2} -c copy {3}".format(input_audio, sampled_duration, one_sample_duration_sec, out_file)
	os.system(command)
	sampled_duration += one_sample_duration_sec
	i += 1