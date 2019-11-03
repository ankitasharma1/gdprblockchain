class MedicalRecord:
    def __init__(self):
        self.name = None
        self.patient_id = None
        self.hospital = None
        self.date = None
        self.notes = None
        self.signature = None

    def __str__(self):
        name = str(self.name)
        patient_id = str(self.patient_id)
        hospital = str(self.hospital)
        date = str(self.date)
        notes = str(self.notes)
        signature = str(self.signature)
        result = name + patient_id + hospital + date + notes + signature
        return result
