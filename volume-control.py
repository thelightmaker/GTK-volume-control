#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import gtk

UI_FILE = os.path.join(sys.path[0]) + '/gui.glade'

class VolumeControl:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.speaker_level = self.builder.get_object('speaker_level')
        self.microphone_level = self.builder.get_object('microphone_level')
        self.button = self.builder.get_object('button')

        _head_volume = os.popen( 'pacmd list-sinks | $(which tr) -d "\t" | $(which grep) -E "\* index|^volume:" | $(which grep) -A1 "index" | $(which grep) "volume"' ).read()
        _head_volume = str.split(_head_volume)[2][:-1]

        _mic_volume = os.popen( 'pacmd list-sources | $(which tr) -d "\t" | $(which grep) -E "\* index|^volume:" | $(which grep) -A1 "index" | $(which grep) "volume"' ).read()
        _mic_volume = str.split(_mic_volume)[2][:-1]

        self.speaker_level.set_value(int(_head_volume))
        self.microphone_level.set_value(int(_mic_volume))

        window = self.builder.get_object('window')
        window.show_all()

    def on_speaker_value_change(self, scale, *args):
        _head_card = os.popen( 'pacmd list-sinks | $(which grep) "* index"' ).read()
        _head_card = str.split(_head_card)[2]

        _head_volume = 'pacmd set-sink-volume ' + str(_head_card) + ' ' + str(int(self.speaker_level.get_value()) * 65537 / 100) + ' > /dev/null'
        print _head_volume
        _head_volume = os.popen(_head_volume)

    def on_microphone_value_change(self, scale, *args):
        _mic_card = os.popen( 'pacmd list-sources | $(which grep) "* index"' ).read()
        _mic_card = str.split(_mic_card)[2]

        _mic_volume = 'pacmd set-source-volume ' + str(_mic_card) + ' ' + str(int(self.microphone_level.get_value()) * 65537 / 100) + ' > /dev/null'
        _mic_volume = os.popen(_mic_volume)

    def destroy(self, window):
        gtk.main_quit()

def main():
    app = VolumeControl()
    gtk.main()

if __name__ == '__main__':
    main()
