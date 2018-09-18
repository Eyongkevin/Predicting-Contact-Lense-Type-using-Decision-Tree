import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import model

# In PyQt5, QApplication is located in PyQt5.QtWidgets.
from PyQt5.QtWidgets import (QApplication,QPushButton,QDoubleSpinBox,QGridLayout, QLabel,QDialog, QTextBrowser, QLineEdit, QVBoxLayout,QHBoxLayout, QComboBox)


class Predict_Form(QDialog):
	def __init__(self, parent=None):
		super(Predict_Form, self).__init__(parent)
		self.model = model.model()

		# Get classifier and label
		self.classifier = self.model.grabTree('lense_classifier_checkpoint.txt')
		self.label = self.model.grabLabel()

		# Entries to be used in comboboxes
		age = ['young','pre','presbyopic']
		prescript = ['myope','hyper']
		astigmatic = ['no','yes']
		tearRate = ['reduced','normal']


		# Create all labels
		LenseLabel = QLabel("<font color=blue size=3><b>Lense Predictor Using Machine Learning</b></font>")
		self.ageLabel = QLabel("<font color=brown size=1><b>Age</b></font>")
		self.prescriptLabel = QLabel("<font color=brown size=1><b>Prescript</b></font>")
		self.astigmaticLabel = QLabel("<font color=brown size=1><b>Astigmatic</b></font>")
		self.tearRateLabel = QLabel("<font color=brown size=1><b>Tear Rate</b></font>")
		self.predictLabel = QLabel("<font color=green size=2><b> </b></font>")


		# create combobox for each label
		self.ageCombobox = QComboBox()
		self.prescriptCombobox = QComboBox()
		self.astigmaticCombobox = QComboBox()
		self.tearRateCombobox = QComboBox()

		# create push button
		self.button = QPushButton("Predict")

		# Add items to comboboxes
		self.ageCombobox.addItems(age)
		self.prescriptCombobox.addItems(prescript)
		self.astigmaticCombobox.addItems(astigmatic)
		self.tearRateCombobox.addItems(tearRate)


		# Create layouts, this has nested layouts
		grid = QGridLayout()
		# Position the label comboboxes
		grid.addWidget(self.ageLabel, 1,0)
		grid.addWidget(self.ageCombobox, 1,1)

		grid.addWidget(self.prescriptLabel, 2,0)
		grid.addWidget(self.prescriptCombobox, 2,1)

		grid.addWidget(self.astigmaticLabel, 3,0)
		grid.addWidget(self.astigmaticCombobox, 3,1)

		grid.addWidget(self.tearRateLabel, 4,0)
		grid.addWidget(self.tearRateCombobox, 4,1)


		layoutV = QVBoxLayout()
		layoutV.addWidget(LenseLabel)

		layoutH = QHBoxLayout()
		layoutV.addLayout(layoutH)
		layoutH.addLayout(grid)


		layoutV2 = QVBoxLayout()
		layoutV2.addWidget(self.predictLabel)
		layoutV2.addWidget(self.button)

		layoutH.addStretch()
		layoutH.addLayout(layoutV2)


		self.setLayout(layoutV)

		self.setWindowTitle("Lense Predictor")

		# Connect the button clicked signal to a slot
		self.button.clicked.connect(self.buttonClick)

	def buttonClick(self):
		# Get all combobox texts
		age = self.ageCombobox.currentText()
		prescript = self.prescriptCombobox.currentText()
		astigmatic = self.astigmaticCombobox.currentText()
		tearRate = self.tearRateCombobox.currentText()

		# Predict
		predict = self.model.classify(self.classifier, self.label, [age, prescript, astigmatic, tearRate])
		# Show result
		self.predictLabel.setText("<font color=green size=2><b>"+ predict +"</b></font>")



app = QApplication(sys.argv)
form = Predict_Form()
form.show()
app.exec_()