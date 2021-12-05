from django.http import request
from django.shortcuts import render
from .forms import SymptomsForm

import pandas as pd


# Create your views here.
# do something
def search(request):
  if request.method == 'POST':
      form = SymptomsForm(request.POST)
      if form.is_valid():
          search_term = form.cleaned_data['search']
      main_dataset = pd.read_csv('../../../Research/ramarao2/dataset.csv')
      main_dataset.set_index('Disease', inplace=True)
      map_of_diseases = {}
      for index, row in main_dataset.iterrows():
          if row.str.contains(search_term):
              map_of_diseases[index] = row.to_list()
      return render(request, 'search.html', {'diseases': map_of_diseases.keys(), 'symptoms': map_of_diseases.values()})

  return render(request, 'search.html', {'diseases': [], 'symptoms': []})

def search(request):
  if request.method == 'POST':
      form = DiseasesForm(request.POST)
      if form.is_valid():
          search_term = form.cleaned_data['search']
      main_dataset = pd.read_csv('../../../Research/ramarao2/dataset.csv')
      for index, row in main_dataset.iterrows():
        if index.str.contains(search_term):
            return render(request, 'search.html', {'symptoms': row})
        # if index equals the search term
        # {‘symptoms’: list_goes_here}

  return render(request, 'search.html', {'symptoms': []})
