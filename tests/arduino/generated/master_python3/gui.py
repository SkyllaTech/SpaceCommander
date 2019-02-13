#! /usr/bin/env python3

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import serial.tools.list_ports

from spacecommands import MasterBase

port_info_format_str = "<big><b>Device Information</b></big>\n<b>Name:</b> {name}\n<b>Device:</b> {device}\n<b>Description:</b> {desc}\n<b>Product:</b> {product}\n<b>Manufacturer:</b> {manufacturer}\n<b>Vendor ID:</b> {vid}\n<b>Product ID:</b> {pid}\n<b>Serial Number:</b> {sn}"


def get_available_serial_ports():
    return list(serial.tools.list_ports.comports())


class Window(Gtk.Window):
    def __init__(self):
        super(Window, self).__init__(title='SpaceCommander')

        self.nb = Gtk.Notebook()
        self.add(self.nb)

        self.nb.append_page(self.layout_connection(), Gtk.Label("Connection"))
        self.nb.append_page(self.layout_command(), Gtk.Label("Commands"))

    def layout_connection(self):
        # Serial port select
        port_select_box = Gtk.HBox()
        self.active_port = ""
        self.port_combobox = Gtk.ComboBoxText()
        self.port_combobox.set_entry_text_column(0)
        self.port_combobox.connect('changed', self.set_active_port)
        port_select_box.add(self.port_combobox)

        self.refresh_port_list(self)
        refresh = Gtk.Button(label="Refresh")
        refresh.connect('clicked', self.refresh_port_list)
        port_select_box.add(refresh)

        connect = Gtk.Button(label="Connect")
        connect.connect('clicked', self.connect_serial)
        port_select_box.add(connect)

        # Serial port info
        self.port_info = Gtk.Label()
        self.port_info.set_justify(Gtk.Justification.LEFT)
        self.set_port_info()

        port_box = Gtk.VBox()
        port_box.add(port_select_box)
        port_box.add(self.port_info)

        # Connection version info
        version_box = Gtk.VBox()
        master_version = Gtk.Label("Master Version: 0xdfdf2feba025bd44")
        self.slave_version = Gtk.Label("Slave Version: ")
        version_box.add(master_version)
        version_box.add(self.slave_version)

        connection_box = Gtk.HBox()
        connection_box.add(port_box)
        connection_box.add(version_box)

        return connection_box

    def layout_command(self):
        # Command tab
        command_box = Gtk.VBox()

        # Command Select
        command_select = Gtk.HBox()

        command_combobox = Gtk.ComboBoxText()
        command_combobox.set_entry_text_column(0)
        command_combobox.connect('changed', self.set_active_command)

        command_execute = Gtk.Button(label="Execute")
        command_execute.connect('clicked', self.execute_command)
        command_select.add(command_combobox)
        command_select.add(command_execute)

        # Command parameters stack
        self.active_command = ""
        self.command_dict = {}
        self.command_stack = Gtk.Stack()
        command_combobox.append_text('send_byte')
        self.command_dict['send_byte'] = {}
        self.command_stack.add_named(self.layout_command_send_byte(), 'send_byte')
        command_combobox.append_text('recv_byte')
        self.command_dict['recv_byte'] = {}
        self.command_stack.add_named(self.layout_command_recv_byte(), 'recv_byte')
        command_combobox.append_text('echo')
        self.command_dict['echo'] = {}
        self.command_stack.add_named(self.layout_command_echo(), 'echo')

        command_box.add(command_select)
        command_box.add(self.command_stack)

        return command_box

    def refresh_port_list(self, widget):
        print("Refreshing port list")
        self.port_combobox.remove_all()
        ports = get_available_serial_ports()
        self.port_list = dict((p.name, p) for p in ports)
        for port in list(self.port_list.keys()):
            self.port_combobox.append_text(port)

    def set_active_port(self, combo):
        port = combo.get_active_text()
        print("Setting active port to:", port)
        if port:
            self.active_port = self.port_list[port]
            self.set_port_info()

    def set_port_info(self):
        if self.active_port:
            self.port_info.set_markup(port_info_format_str.format(
                name=self.active_port.name,
                device=self.active_port.device,
                desc=self.active_port.description,
                product=self.active_port.product,
                manufacturer=self.active_port.manufacturer,
                vid=self.active_port.vid,
                pid=self.active_port.pid,
                sn=self.active_port.serial_number
            ))
        else:
            self.port_info.set_markup(port_info_format_str.format(
                name="", device="", desc="", product="",
                manufacturer="", vid="", pid="", sn=""
            ))

    def connect_serial(self, widget):
        print("Connecting to port:", self.active_port.name)
        self.master = MasterBase(self.active_port.device)
        self.master.begin()
        version = self.master.get_hash()
        self.slave_version = Gtk.Label("Slave Version: {}".format(version))

    def disconnect_serial(self):
        print("Disconnecting from port:", self.active_port.name)
        self.master.close()
        self.slave_version = Gtk.Label("Slave Version: ")

    def execute_command(self, widget):
        print("Executing command:", self.active_command)
        input_args = [e.get_text() for e in self.command_dict[self.active_command]['inputs']]
        print(input_args)

    def set_active_command(self, combo):
        command = combo.get_active_text()
        print("Setting active command to:", command)
        self.active_command = command
        self.command_stack.set_visible_child_name(command)

    def layout_command_send_byte(self):
        self.command_dict['send_byte']['inputs'] = []
        self.command_dict['send_byte']['outputs'] = []
        command_page = Gtk.Grid()
        # Inputs
        input_label = Gtk.Label()
        input_label.set_markup("<b>Inputs</b>")
        command_page.attach(input_label, 0, 0, 2, 1)
        b_label = Gtk.Label("b")
        command_page.attach(b_label, 0, 1, 1, 1)
        b_entry = Gtk.Entry()
        command_page.attach(b_entry, 0, 2, 1, 1)
        self.command_dict['send_byte']['inputs'].append(b_entry)
        # Outputs
        output_label = Gtk.Label()
        output_label.set_markup("<b>Outputs</b>")
        command_page.attach(output_label, 0, 3, 2, 1)
        return command_page

    def layout_command_recv_byte(self):
        self.command_dict['recv_byte']['inputs'] = []
        self.command_dict['recv_byte']['outputs'] = []
        command_page = Gtk.Grid()
        # Inputs
        input_label = Gtk.Label()
        input_label.set_markup("<b>Inputs</b>")
        command_page.attach(input_label, 0, 0, 2, 1)
        # Outputs
        output_label = Gtk.Label()
        output_label.set_markup("<b>Outputs</b>")
        command_page.attach(output_label, 0, 3, 2, 1)
        b_label = Gtk.Label("b")
        command_page.attach(b_label, 0, 4, 1, 1)
        b_entry = Gtk.Entry()
        command_page.attach(b_entry, 0, 5, 1, 1)
        self.command_dict['recv_byte']['outputs'].append(b_entry)
        return command_page

    def layout_command_echo(self):
        self.command_dict['echo']['inputs'] = []
        self.command_dict['echo']['outputs'] = []
        command_page = Gtk.Grid()
        # Inputs
        input_label = Gtk.Label()
        input_label.set_markup("<b>Inputs</b>")
        command_page.attach(input_label, 0, 0, 2, 1)
        send_string_label = Gtk.Label("send_string")
        command_page.attach(send_string_label, 0, 1, 1, 1)
        send_string_entry = Gtk.Entry()
        command_page.attach(send_string_entry, 0, 2, 1, 1)
        self.command_dict['echo']['inputs'].append(send_string_entry)
        # Outputs
        output_label = Gtk.Label()
        output_label.set_markup("<b>Outputs</b>")
        command_page.attach(output_label, 0, 3, 2, 1)
        recv_string_label = Gtk.Label("recv_string")
        command_page.attach(recv_string_label, 0, 4, 1, 1)
        recv_string_entry = Gtk.Entry()
        command_page.attach(recv_string_entry, 0, 5, 1, 1)
        self.command_dict['echo']['outputs'].append(recv_string_entry)
        return command_page



def run():
    window = Window()
    window.show_all()
    window.connect('delete-event', Gtk.main_quit)
    Gtk.main()


if __name__ == '__main__':
    run()


    # def on_choose_root(self, widget):
    #     file_dialog = Gtk.FileChooserDialog("Save File",
    #                                         self,
    #                                         Gtk.FileChooserAction.SELECT_FOLDER,
    #                                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
    #                                          Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    #     resp = file_dialog.run()
    #     if resp == Gtk.ResponseType.OK:
    #         self.project_root = file_dialog.get_filename()
    #     file_dialog.destroy()

    # def on_generate(self, widget):
    #     if self.project_root is None:
    #         pass # TODO: show dialog saying project root must be set

    #     os.chdir(self.project_root)
    #     output = main.generate_templates(*main.load_config('commands.yaml'))
    #     for i in range(self.nb.get_n_pages()):
    #         self.nb.remove_page(-1)
    #     for k, v in output.items():
    #         tv = Gtk.TextView()
    #         tv.get_buffer().set_text(v)
    #         tv.set_editable(False)
    #         tv.set_monospace(True)
    #         tv.modify_font(Pango.FontDescription('Monospace 9'))
    #         sw = Gtk.ScrolledWindow()
    #         sw.add(tv)
    #         self.nb.append_page(sw, Gtk.Label(k))
    #     self.nb.set_size_request(400, 400)
    #     self.nb.show_all()
