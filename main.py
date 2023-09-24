import IPython
import numpy as np
import essentia
import essentia.standard as es
from tempfile import TemporaryDirectory


def main():
  # Loading an audio file.
  audio = es.MonoLoader(filename='base_audio/10To8DrumLoop.wav')()

  # Compute beat positions and BPM.
  # od_hfc = es.OnsetDetection(method='hfc')
  rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
  bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

  # w = es.Windowing(type='hann')
  # fft = es.FFT() # Outputs a complex FFT vector.
  # c2p = es.CartesianToPolar() # Converts it into a pair of magnitude and phase vectors.

  # # Compute both ODF frame by frame. Store results to a Pool.
  # pool = essentia.Pool()
  # for frame in es.FrameGenerator(audio, frameSize=1024, hopSize=512):
  #     magnitude, phase = c2p(fft(w(frame)))
  #     pool.add('odf.hfc', od_hfc(magnitude, phase))
  # onsets = es.Onsets()
  # onsets_hfc = onsets(essentia.array([pool['odf.hfc']]), [1])

  totalBeats = 0
  measureLength = ((8 * (60 / bpm)) + (60 / bpm))

  for beatPos in beats:
    if beatPos <= measureLength:
      totalBeats += 1
    else:
      break

  print(f"BPM: {bpm:.0f}")
  print(f"Beat positions (sec.): {beats}")
  print(f"Beat estimation confidence: {beats_confidence:.5f}")
  print(f"The final time signature is: {totalBeats}/8 ± 2/8")

  # Mark beat positions in the audio and write it to a file.
  # Use beeps instead of white noise to mark them, as it is more distinctive.
  marker = es.AudioOnsetsMarker(onsets=beats, type='beep')
  marked_audio = marker(audio)

  # silence = [0.] * len(audio)
  # beeps_hfc = es.AudioOnsetsMarker(onsets=onsets_hfc, type='beep')(silence)
  # audio_hfc = es.StereoMuxer()(audio, beeps_hfc)

  # Write to an audio file in a temporary directory.
  # temp_dir = TemporaryDirectory()
  es.MonoWriter(filename='marked_audio/10To8DrumLoopMarked.wav', format="wav")(marked_audio)
  # es.AudioWriter(filename='marked_audio/BristlemouthSampleOnsets.wav', format="wav")(audio_hfc)

  # IPython.display.Audio(temp_dir.name + 'BristlemouthFull.wav')


if __name__ == "__main__":
  main()
