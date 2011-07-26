#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import alsaaudio
import gtk

UI_FILE = 'gui.glade'

class VolumeControl:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.speaker_level = self.builder.get_object('speaker_level')
        self.microphone_level = self.builder.get_object('microphone_level')
        self.button = self.builder.get_object('button')

        pcm = alsaaudio.Mixer()
        mic = alsaaudio.Mixer('Capture')

        self.speaker_level.set_value(pcm.getvolume()[0])
        self.microphone_level.set_value(mic.getvolume()[0])

        window = self.builder.get_object('window')
        window.show_all()

    def on_speaker_value_change(self, scale, *args):
        pcm = alsaaudio.Mixer()
        pcm.setvolume(int(self.speaker_level.get_value()))
        print int(self.speaker_level.get_value())

    def on_microphone_value_change(self, scale, *args):
        mic = alsaaudio.Mixer('Capture')
        mic.setvolume(int(self.microphone_level.get_value()),0)
        mic.setvolume(int(self.microphone_level.get_value()),1)
        print int(self.microphone_level.get_value())

    def destroy(self, window):
        gtk.main_quit()

def main():
    app = VolumeControl()
    gtk.main()

if __name__ == '__main__':
    main()
