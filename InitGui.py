# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 - Harry van Langen <hvlanalysis@gmail.com>        *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__Title__ = "fcES"
__Author__ = "HarryvL"
__Url__ = "https://github.com/HarryvL/fcES-workbench"
__Version__ = "0.1.0"
__Date__ = "2024/12/18"
__Comment__ = "first release"
__Forum__ = "https://forum.freecad.org/viewtopic.php?t=85474"
__Status__ = "initial development"
__Requires__ = "freecad version 0.19 or higher"
__Communication__ = "https://forum.freecad.org/viewtopic.php?t=85474"

import os
import sys
import dummyES
import FreeCAD
import FreeCADGui
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QTableWidgetItem

global FCmw
global QtWidgets, QtGui, QtCore, QTableWidgetItem

FCmw = FreeCADGui.getMainWindow()
global dir_name
dir_name = os.path.dirname(dummyES.file_path())
global double_validator
double_validator = QtGui.QDoubleValidator()
global int_validator
int_validator = QtGui.QIntValidator()
# global res_show
# res_show = FreeCAD.getHomePath() + "Mod/Fem/Resources/ui/ResultShow.ui"
global source_code_path
source_code_path = os.path.join(dir_name, 'source code')

sys.path.append(source_code_path)


class fcESWorkbench(Workbench):
    Icon = os.path.join(dir_name, "icons", "fcFEM.svg")
    MenuText = "fcES workbench"
    ToolTip = "Beams on elastic foundation / Axi-symmetric silos"

    def __init__(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        self.appendToolbar("fcES", [])
        self.appendMenu("fcES", [])
        self.palette_warning = QtGui.QPalette()
        self.palette_warning.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
        self.palette_standard = QtGui.QPalette()
        self.palette_standard.setColor(QtGui.QPalette.Base, QtGui.QColor("white"))
        # self.palette.setColor(QtGui.QPalette.Text, QtGui.QColor("red"))

    def Activated(self):
        global fcES_window

        import dummyES
        self.dir_name = os.path.dirname(dummyES.file_path())
        self.doc = FreeCAD.activeDocument()
        if self.doc is None:
            self.doc = FreeCAD.newDocument("fcES")
        self.file_name = self.doc.Label
        self.macro_file_path = os.path.join(self.dir_name, "source code", "fcES.FCMacro")

        class DocObserver(object):  # document Observer
            def __init__(self, workbench_instance):
                self.workbench_instance = workbench_instance

            def slotActivateDocument(self, doc):
                if FreeCAD.activeDocument().Label[0:7] != "Unnamed":
                    self.workbench_instance.save_clicked()
                    self.workbench_instance.file_name = FreeCAD.activeDocument().Label
                    print(self.workbench_instance.file_name)
                    self.analysis_type = self.workbench_instance.analysis_type_default
                    self.workbench_instance.node_obj = {}
                    self.workbench_instance.beam_obj = {}
                    self.workbench_instance.tank_obj = {}
                    self.workbench_instance.open_file()
                    self.workbench_instance.fill_UI()

            def slotFinishSaveDocument(self, doc, prop):
                self.workbench_instance.save_clicked()  # save under old file name
                self.workbench_instance.file_name = doc.Label
                self.workbench_instance.save_clicked()  # save under new file name

        self.obs = DocObserver(self)
        FreeCAD.addDocumentObserver(self.obs)

        ui_Path = os.path.join(self.dir_name, "user_interface", "fcES.ui")

        fcES_window = FreeCADGui.PySideUic.loadUi(ui_Path)

        fcES_window.startBtn.clicked.connect(self.start_clicked)
        fcES_window.saveBtn.clicked.connect(self.save_clicked)
        fcES_window.beamBtn.clicked.connect(self.btn_state)
        fcES_window.tankBtn.clicked.connect(self.btn_state)
        fcES_window.tendonBtn.clicked.connect(self.btn_state)
        #
        fcES_window.num_el.textChanged.connect(self.num_el_changed)
        fcES_window.tendon_load.textChanged.connect(self.tendon_load_changed)
        fcES_window.node_prop.cellChanged.connect(self.node_cell_changed)
        fcES_window.beam_prop.cellChanged.connect(self.beam_cell_changed)
        fcES_window.tank_prop.cellChanged.connect(self.tank_cell_changed)
        #
        fcES_window.num_el.setValidator(int_validator)

        self.analysis_type_default = "beam"
        self.num_el_default = 1
        self.tendon_load_default = 0.0
        self.node_object_default = {1: ["0.0", "n", "n", "0.0", "0.0"], 2: ["1.0", "n", "n", "0.0", "0.0"]}
        self.beam_object_default = {1: ["1.0", "1.0", "0.0", "0.0"]}
        self.tank_object_default = {1: ["1.0", "1.0", "1.0", "0.3", "0.0", "0.0"]}

        self.analysis_type = self.analysis_type_default
        self.node_obj = self.node_object_default.copy()
        self.beam_obj = self.beam_object_default.copy()
        self.tank_obj = self.tank_object_default.copy()
        self.tendon_load = self.tendon_load_default

        fcES_window.beam_tank.setCurrentIndex(0)

        self.open_file()
        self.fill_UI()

        FCmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, fcES_window.dw)

        fcES_window.dw.setMaximumWidth(550)

    def node_cell_changed(self, r, c):
        if c == 1 or c == 2:
            if fcES_window.node_prop.item(r, c).text() not in ["y", "n"]:
                fcES_window.node_prop.setItem(r, c, QTableWidgetItem("n"))
        else:
            try:
                float(fcES_window.node_prop.item(r, c).text())
            except ValueError:
                fcES_window.node_prop.setItem(r, c, QTableWidgetItem("0.0"))
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise
        self.node_obj[r + 1][c] = fcES_window.node_prop.item(r, c).text()

    def beam_cell_changed(self, r, c):
        try:
            float(fcES_window.beam_prop.item(r, c).text())
        except ValueError:
            fcES_window.beam_prop.setItem(r, c, QTableWidgetItem("0.0"))
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        self.beam_obj[r + 1][c] = fcES_window.beam_prop.item(r, c).text()

    def tank_cell_changed(self, r, c):
        try:
            float(fcES_window.tank_prop.item(r, c).text())
        except ValueError:
            fcES_window.tank_prop.setItem(r, c, QTableWidgetItem("0.0"))
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        self.tank_obj[r + 1][c] = fcES_window.tank_prop.item(r, c).text()

    def Deactivated(self):
        try:
            if fcES_window.dw.isVisible():
                fcES_window.dw.setVisible(False)
        except Exception:
            None

        FreeCAD.removeDocumentObserver(self.obs)

    def start_clicked(self):
        self.save_clicked()

        try:
            rv = FCmw.findChild(QtWidgets.QTextEdit, "Report view")
            rv.clear()
        except Exception:
            None

        FreeCADGui.Selection.clearSelection()

        fcES_macro = open(self.macro_file_path).read()
        print(self.macro_file_path)
        exec(fcES_macro)

    def quit_clicked(self):
        self.Deactivated()

    def save_clicked(self):
        inp_file_path = os.path.join(self.dir_name, "control files", self.file_name + '.inp')

        with open(inp_file_path, "w") as file:
            # Write `analysis_type` and `num_el`
            file.write(f"analysis_type = {self.analysis_type}\n")
            file.write(f"num_el = {self.num_el}\n")

            # Write `node_obj` entries with "node" prefix
            # print("nod_obj", self.node_obj)
            for key, values in self.node_obj.items():
                file.write(f"node {key}: {' '.join(map(str, values))}\n")

            # Write `beam_obj` entries with "beam" prefix
            for key, values in self.beam_obj.items():
                file.write(f"beam {key}: {' '.join(map(str, values))}\n")

            # Write `tank_obj` entries with "tank" prefix
            for key, values in self.tank_obj.items():
                file.write(f"tank {key}: {' '.join(map(str, values))}\n")

            file.write(f"tendon_load = {self.tendon_load}\n")


    def open_file(self):
        inp_file_path = os.path.join(self.dir_name, "control files", self.file_name + '.inp')
        print("open file:", inp_file_path)
        try:
            with open(inp_file_path, "r") as file:
                lines = file.readlines()
            if lines:
                self.analysis_type = lines[0].split("=")[1].strip()
                self.num_el = int(lines[1].split("=")[1].strip())

                if self.analysis_type == "beam":
                    fcES_window.beam_tank.setCurrentIndex(0)
                else:
                    fcES_window.beam_tank.setCurrentIndex(1)

                # Parse remaining lines
                for line in lines[2:]:
                    line = line.strip()
                    if line.startswith("node"):
                        key, values = line.split(":")
                        key = int(key.split()[1])  # Extract the node number
                        self.node_obj[key] = values.strip().split()
                    elif line.startswith("beam"):
                        key, values = line.split(":")
                        key = int(key.split()[1])  # Extract the beam number
                        self.beam_obj[key] = values.strip().split()
                    elif line.startswith("tank"):
                        key, values = line.split(":")
                        key = int(key.split()[1])  # Extract the tank number
                        self.tank_obj[key] = values.strip().split()
                    elif line.startswith("tendon_load"):
                        self.tendon_load = float(line.split("=")[1].strip())


        except FileNotFoundError:
            self.analysis_type = self.analysis_type_default
            self.num_el = self.num_el_default
            self.tendon_load = self.tendon_load_default
            self.node_obj = self.node_object_default
            self.beam_obj = self.beam_object_default
            self.tank_obj = self.tank_object_default

    def num_el_changed(self):
        val = fcES_window.num_el.text()
        num_el_old = self.num_el
        if val == "" or val == "-" or float(val) <= 0.0:
            val = "1"
            self.num_el = int(val)
            fcES_window.num_el.setText("1")
        if int(val) != self.num_el:
            self.num_el = int(val)
        fcES_window.node_prop.setRowCount(self.num_el + 1)
        fcES_window.beam_prop.setRowCount(self.num_el)
        fcES_window.tank_prop.setRowCount(self.num_el)
        if self.num_el > num_el_old:
            for el in range(num_el_old, self.num_el):
                self.node_obj[el + 2] = self.node_obj[el + 1].copy()
                self.beam_obj[el + 1] = self.beam_obj[el].copy()
                self.tank_obj[el + 1] = self.tank_obj[el].copy()
        elif self.num_el < num_el_old:
            for el in range(self.num_el, num_el_old):
                del self.node_obj[el + 2]
                del self.beam_obj[el + 1]
                del self.tank_obj[el + 1]
        self.fill_UI()

    def tendon_load_changed(self):
        val = fcES_window.tendon_load.text()
        if val == "" or val == "-" or float(val) < 0.0:
            val = "0.0"
        self.tendon_load = float(val)

    def btn_state(self):
        if fcES_window.beamBtn.isChecked():
            self.analysis_type = "beam"
            fcES_window.beam_tank.setCurrentIndex(0)
        if fcES_window.tankBtn.isChecked():
            self.analysis_type = "tank"
            fcES_window.beam_tank.setCurrentIndex(1)
        if fcES_window.tendonBtn.isChecked():
            self.analysis_type = "tendon"
            fcES_window.beam_tank.setCurrentIndex(1)

    def fill_UI(self):
        if self.analysis_type == "beam":
            fcES_window.beamBtn.setChecked(True)
        elif self.analysis_type == "tank":
            fcES_window.tankBtn.setChecked(True)
        else:
            fcES_window.tendonBtn.setChecked(True)

        fcES_window.num_el.setText(str(self.num_el))
        if self.analysis_type != "beam":
            fcES_window.tendon_load.setText(str(self.tendon_load))
        for node in self.node_obj:
            for col, val in enumerate(self.node_obj[node]):
                fcES_window.node_prop.setItem(node - 1, col, QTableWidgetItem(self.node_obj[node][col]))
        for beam in self.beam_obj:
            for col, val in enumerate(self.beam_obj[beam]):
                fcES_window.beam_prop.setItem(beam - 1, col, QTableWidgetItem(self.beam_obj[beam][col]))
        for tank in self.tank_obj:
            for col, val in enumerate(self.tank_obj[tank]):
                fcES_window.tank_prop.setItem(tank - 1, col, QTableWidgetItem(self.tank_obj[tank][col]))


FreeCADGui.addWorkbench(fcESWorkbench)
