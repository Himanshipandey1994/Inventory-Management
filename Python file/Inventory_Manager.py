# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5 import QtWidgets
from PyQt5.QtCore import*
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

from os import path
from PyQt5.uic import loadUiType


FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))

import sqlite3

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.Handel_Buttons()  # Call the method here after the UI setup
        self.fetch_references()
        self.fetch_min_holes()
        self.fetch_max_holes()
        self.fetch_part_types()
        self.fetch_min_holes_reference()
        self.fetch_max_holes_reference()


    def Handel_Buttons(self):
        self.refresh_btn_2.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.search_table)
        self.display_btn.clicked.connect(self.display_data)
        self.update_btn.clicked.connect(self.update_table)
        self.delete_btn.clicked.connect(self.delete_data)
        self.add_btn.clicked.connect(self.add_data)
        self.check_btn.clicked.connect(self.fetch_top_min_count_references)
        
    def GET_DATA(self):
        
        db=sqlite3.connect("parts.db")
        cursor=db.cursor()
        
        command=''' SELECT * from partstable '''
        
        result = cursor.execute(command)
        
        self.table.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                
    def search_table(self):
        count_value = self.count_filter_txt.value()

        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT * FROM partstable WHERE count <= ? '''
        
        result = cursor.execute(command, (count_value,))

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                
    def display_data(self):
        id_value = self.id.text()

        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT * FROM partstable WHERE id = ? '''
        result = cursor.execute(command, (id_value,))
        row_data = result.fetchone()

        if row_data:
            self.reference.setText(row_data[1])
            self.part_name.setText(row_data[2])
            self.min_area.setText(str(row_data[3]))
            self.max_area.setText(str(row_data[4]))
            self.number_of_holes.setText(str(row_data[5]))
            self.min_diameter.setText(str(row_data[6]))
            self.max_diameter.setText(str(row_data[7]))
            self.count.setValue(row_data[8])
        else:
            # Clear all QLineEdit and QSpinBox if ID not found
            self.reference.clear()
            self.part_name.clear()
            self.min_area.clear()
            self.max_area.clear()
            self.number_of_holes.clear()
            self.min_diameter.clear()
            self.max_diameter.clear()
            self.count.setValue(0)
            
    def update_table(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        ID = self.id.text()
        Reference = self.reference.text()
        PartName = self.part_name.text()
        MinArea = self.min_area.text()
        MaxArea = self.max_area.text()
        NumberofHoles = self.number_of_holes.text()
        MinDiameter = self.min_diameter.text()
        MaxDiameter = self.max_diameter.text()
        Count = self.count.value()

        command = ''' UPDATE partstable SET Reference=?, PartName=?, MinArea=?, MaxArea=?, NumberofHoles=?, MinDiameter=?, MaxDiameter=?, Count=? WHERE ID=? '''
        cursor.execute(command, (Reference, PartName, MinArea, MaxArea, NumberofHoles, MinDiameter, MaxDiameter, Count, ID))
        
        db.commit()
        db.close()
        
    def delete_data(self):
    
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
    
        ID = self.id.text()
        Reference = self.reference.text()
        PartName = self.part_name.text()
        MinArea = self.min_area.text()
        MaxArea = self.max_area.text()
        NumberofHoles = self.number_of_holes.text()
        MinDiameter = self.min_diameter.text()
        MaxDiameter = self.max_diameter.text()
        Count = self.count.value()
    
        command = ''' DELETE FROM partstable WHERE Reference=? AND PartName=? AND MinArea=? AND MaxArea=? AND NumberofHoles=? AND MinDiameter=? AND MaxDiameter=? AND Count=? AND ID=? '''
        cursor.execute(command, (Reference, PartName, MinArea, MaxArea, NumberofHoles, MinDiameter, MaxDiameter, Count, ID))
        
        db.commit()
        db.close()
        
    def add_data(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
    
        ID = self.id.text()
        Reference = self.reference.text()
        PartName = self.part_name.text()
        MinArea = self.min_area.text()
        MaxArea = self.max_area.text()
        NumberofHoles = self.number_of_holes.text()
        MinDiameter = self.min_diameter.text()
        MaxDiameter = self.max_diameter.text()
        Count = self.count.value()
        
        command = ''' INSERT INTO partstable (Reference, PartName, MinArea, MaxArea, NumberOfHoles, MinDiameter, MaxDiameter, Count, ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?) '''
        cursor.execute(command, (Reference, PartName, MinArea, MaxArea, NumberofHoles, MinDiameter, MaxDiameter, Count, ID))
        
        db.commit()
        db.close()
        
    def fetch_references(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
    
        command = '''SELECT COUNT(DISTINCT Reference) FROM partstable'''
        cursor.execute(command)
        result = cursor.fetchone()
    
        if result:
            num_references = result[0]
            self.LBL_REF_NBR.setText(str(num_references))
        else:
            self.LBL_REF_NBR.setText("No references found")
            

            db.close()
            
    def fetch_min_holes(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT MIN(NumberofHoles) FROM partstable'''
        cursor.execute(command)
        result = cursor.fetchone()
    
        if result:
            min_holes = result[0]
            self.lbl_min_holes.setText(str(min_holes))
        else:
            self.lbl_min_holes.setText("No Minimum Number of Holes")

            db.close()
            
    def fetch_max_holes(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT MAX(NumberofHoles) FROM partstable'''
        cursor.execute(command)
        result = cursor.fetchone()
    
        if result:
            max_holes = result[0]
            self.lbl_max_holes.setText(str(max_holes))
        else:
            self.lbl_max_holes.setText("No Maximum Number of Holes")

            db.close()
            
    def fetch_part_types(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT COUNT(DISTINCT PartName) FROM partstable'''
        cursor.execute(command)
        result = cursor.fetchone()
    
        if result:
            parts_nmbr = result[0]
            self.lbl_parts_nmbr.setText(str(parts_nmbr))
        else:
            self.lbl_parts_nmbr.setText("No Parts")

            db.close()

    def fetch_min_holes_reference(self):
          
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT Reference FROM partstable WHERE NumberofHoles = (SELECT MIN(NumberofHoles) FROM partstable)'''
        cursor.execute(command)
        result = cursor.fetchone()
        
        if result:
            min_diameter_ref = result[0]
            self.lbl_min_holes2.setText(str(min_diameter_ref))
        else:
            self.lbl_min_holes2.setText("Reference of Minimum NumberofHoles: N/A")

            db.close()
            
    def fetch_max_holes_reference(self):
          
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT Reference FROM partstable WHERE NumberofHoles = (SELECT MAX(NumberofHoles) FROM partstable)'''
        cursor.execute(command)
        result = cursor.fetchone()
        
        if result:
            max_diameter_ref = result[0]
            self.lbl_max_holes2.setText(str(max_diameter_ref))
        else:
            self.lbl_max_holes2.setText("Reference of Maximum NumberofHoles: N/A")

            db.close()
            
    def fetch_top_min_count_references(self):
        
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        command = '''SELECT Reference, PartName, Count FROM partstable ORDER BY Count ASC LIMIT 3'''
        result = cursor.execute(command)
        
        self.table2.setRowCount(0)
        
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

          
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()