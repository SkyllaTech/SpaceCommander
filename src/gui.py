#! /usr/bin/env python3

import main
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Gdl', '3')
from gi.repository import Gtk, GObject, Gdk, cairo as gi_cairo, Pango, PangoCairo, Gdl

class Window(Gtk.Window):
    def on_choose_root(self, widget):
        file_dialog = Gtk.FileChooserDialog("Save File",
                                            self,
                                            Gtk.FileChooserAction.SELECT_FOLDER,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        resp = file_dialog.run()
        if resp == Gtk.ResponseType.OK:
            self.project_root = file_dialog.get_filename()
        file_dialog.destroy()

    def on_generate(self, widget):
        if self.project_root is None:
            pass # TODO: show dialog saying project root must be set

        os.chdir(self.project_root)
        output = main.generate_templates(*main.load_config('commands.yaml'))
        for i in range(self.nb.get_n_pages()):
            self.nb.remove_page(-1)
        for k, v in output.items():
            tv = Gtk.TextView()
            tv.get_buffer().set_text(v)
            tv.set_editable(False)
            tv.set_monospace(True)
            tv.modify_font(Pango.FontDescription('Monospace 9'))
            sw = Gtk.ScrolledWindow()
            sw.add(tv)
            self.nb.append_page(sw, Gtk.Label(k))
        self.nb.set_size_request(400, 400)
        self.nb.show_all()

    def __init__(self):
        super(Window, self).__init__(title='SpaceCommander')

        vbox = Gtk.VBox()
        self.add(vbox)

        hbox = Gtk.HBox(valign='start', vexpand=False)
        vbox.pack_start(hbox, False, True, 0)
        choose_root_button = Gtk.Button('Choose Project Directory')
        choose_root_button.connect('clicked', self.on_choose_root)
        hbox.add(choose_root_button)
        generate_button = Gtk.Button('Generate')
        generate_button.connect('clicked', self.on_generate)
        hbox.add(generate_button)

        self.nb = Gtk.Notebook()
        vbox.pack_start(self.nb, True, True, 0)

def run():
    window = Window()
    window.show_all()
    window.connect('delete-event', Gtk.main_quit)
    Gtk.main()

if __name__ == '__main__':
    run()
