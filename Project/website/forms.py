from django import forms


class SymptomsForm(forms.Form):
    # symptoms = forms.CharField(label="symptoms")
    symptom_search = forms.CharField(label='symptoms', max_length=100)

    def symptom_message(self):
        symptom_search = self.cleaned_data.get('symptoms')

        return symptom_search

class DiseasesForm(forms.Form):
    # diseases = forms.CharField(label="diseases")
    disease_search = forms.CharField(label='diseases', max_length=100)

    def disease_message(self):
        disease_search = self.cleaned_data.get('diseases')

        return disease_search

class ClinicsForm(forms.Form):
    # clinics = forms.CharField(label="clinics")
    clinic_search = forms.CharField(label='clinics', max_length=100)

    def clinic_message(self):
        clinic_search = self.cleaned_data.get('search_term')

        return clinic_search

class HospitalsForm(forms.Form):
    # hospitals = forms.CharField(label="hospitals")
    hospital_search = forms.CharField(label='hospitals', max_length=100)

    def hospital_message(self):
        hospital_search = self.cleaned_data.get('hospitals')

        return hospital_search