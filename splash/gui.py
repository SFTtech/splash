#!/usr/bin/env python3

"""
gui functionality for splash.
allows speedreading with an interactive gui.
"""

from gi.repository import (GObject as gobject,
                           Gtk as gtk,
                           Pango as pango,
                           PangoCairo as pangocairo)

import math
import os

from . import splash


class SplashViewer:
    """
    gtk3 gui for speedreading.
    Contains all the state and handling for the gtk actions.
    """

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__),
                                                "layout.glade"))
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window0")
        self.window.resize(300, 200)
        self.window.set_position(gtk.WindowPosition.CENTER)
        self.draw_size = (0, 0)

        self.window.show_all()

        self.font = "Sans Bold 27"

        self.splash = splash.Splash(["..."])

        self.current_word = "..."
        self.current_center = 1
        self.playing = False

        self.wpm = 50  # TODO: make adjustable
        self.timer = None

    def run(self):
        """
        run the gtk main loop
        """
        gtk.main()

    def open_about(self, origin):
        """
        show the about window
        """
        dialog = self.builder.get_object("aboutdialog0")
        dialog.show()

    def close_about(self, *args):
        """
        hide the about window"
        """
        dialog = self.builder.get_object("aboutdialog0")
        dialog.hide()

    def delete_window(self, *args):
        """
        stop the gtk main loop when closing the window.
        """
        gtk.main_quit(args)

    def play(self, _):
        """
        activate playback of words for reading.
        """
        if not self.splash:
            print("No text file loaded")

        # already playing
        if self.playing:
            print("already reading")
            return

        self.playing = True
        self.advance_word()

    def pause(self, _):
        """
        suspend playing and allow continuation later.
        """
        self.playing = False

    def advance_word(self, event=None):
        """
        show the next word of the text.
        """
        if not self.splash:
            self.playing = False
            return False

        end, word, center, delay = self.splash.advance(self.wpm)

        if not end:
            self.current_word = word
            self.update_canvas()
            self.current_center = center
        else:
            self.playing = False

        # queue the next update
        if self.playing:
            print("adding timer with delay %s" % delay)
            self.timer = gobject.timeout_add(delay, self.advance_word, None)

        # destroy the previous timer to not trigger again:
        return False

    def back(self, origin):
        """
        reset the reading progress and start over.
        """
        self.playing = False
        self.splash = None

    def canvas_draw(self, widget, cr):
        """
        draw the word centered in the window.
        """
        w, h = self.draw_size

        # center of the text
        cx, cy = w/2., h/2.

        # circle
        cr.set_line_width(9)
        cr.set_source_rgb(1.0, 1.0, 1.0)

        ctx = pangocairo.create_context(cr)
        layout = pango.Layout.new(ctx)
        prefixlayout = pango.Layout.new(ctx)

        desc = pango.font_description_from_string(self.font)
        for l in (layout, prefixlayout):
            l.set_font_description(desc)

        txt = self.current_word

        center = self.current_center
        if len(txt) > 0:
            markup = "%s<span foreground='red'>%s</span>%s" % tuple(
                t.replace("<", "&lt;").replace(">", "&gt;")
                for t in (txt[:center],
                          txt[center],
                          txt[center+1:]))
            prefix = txt[:center]
        else:
            markup = ""
            prefix = ""

        e, attr, txt, accel = pango.parse_markup(markup, -1, '\x00')
        layout.set_text(txt, -1)
        layout.set_attributes(attr)
        prefixlayout.set_text(prefix, -1)

        pangocairo.update_layout(cr, layout)
        pangocairo.update_layout(cr, prefixlayout)

        # text metrics
        _, txth = (x/1024. for x in layout.get_size())
        prew, _ = (x/1024. for x in prefixlayout.get_size())

        cr.move_to(cx - (prew), cy - txth/2)

        # render the text
        pangocairo.show_layout(cr, layout)

    def draw_size_change(self, widget, rectangle):
        """
        when the window size changes, update the stored dimensions.
        """
        self.draw_size = (rectangle.width, rectangle.height)

    def open_text(self, origin):
        """
        a new text was opened
        """

        chooser = gtk.FileChooserDialog(title="Open file to read...",
                                        action=gtk.FileChooserAction.OPEN,
                                        buttons=(gtk.STOCK_CANCEL,
                                                 gtk.ResponseType.CANCEL,
                                                 gtk.STOCK_OPEN,
                                                 gtk.ResponseType.OK))
        for ff in ("textfilefilter", "anyfilefilter"):
            filefilter = self.builder.get_object(ff)
            chooser.add_filter(filefilter)

        response = chooser.run()
        if response == gtk.ResponseType.OK:
            file_name = chooser.get_filename()
            print("opening %s" % file_name)

            self.splash = splash.Splash(open(file_name))
        elif response == gtk.ResponseType.CANCEL:
            print("canceling")

        chooser.destroy()

    def open_state(self, origin):
        """
        open some reading state
        """
        pass

    def save_state(self, origin):
        """
        save some reading state
        """

        chooser = gtk.FileChooserDialog(title="Save reading state...",
                                        action=gtk.FileChooserAction.SAVE,
                                        buttons=(gtk.STOCK_CANCEL,
                                                 gtk.ResponseType.CANCEL,
                                                 gtk.STOCK_SAVE,
                                                 gtk.ResponseType.OK))

        response = chooser.run()

    def update_canvas(self):
        """
        when the window requires redrawing,
        this method is called.
        """
        canvas = self.builder.get_object("drawingarea0")
        canvas.queue_draw()


def main():
    """
    create the window and display it.
    """

    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    v = SplashViewer()
    v.run()


if __name__ == "__main__":
    main()
