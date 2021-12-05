from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *

import pandas as pd
import os

# Create your views here.

def home(request):
    return render(request, 'index.html', {})


def search(request):
  if request.method == 'POST':
      form = SymptomsForm(request.POST)
      print(form.errors)
      if form.is_valid():
          search_term = form.cleaned_data['symptom_search']
      else:
          return HttpResponse("Invalid form input")
      main_dataset = pd.read_csv(os.path.join('app/data/dataset.csv'))
      main_dataset.set_index('Disease', inplace=True)
      map_of_diseases = {}
      for index, row in main_dataset.iterrows():
          if row.str.contains(search_term).any():
              map_of_diseases[index] = ", ".join([s.replace('_', ' ') for s in row.to_list() if pd.notna(s)])
              
      tuples = zip(map_of_diseases.keys(), map_of_diseases.values())
      return render(request, 'search.html', {'diseases': tuples})

  return render(request, 'search.html', {'diseases': [], 'symptoms': []})

def search_disease(request):
  if request.method == 'POST':
      form = DiseasesForm(request.POST)
      if form.is_valid():
          search_term = form.cleaned_data['search']
      main_dataset = pd.read_csv(os.path.join('app/data/dataset.csv'))
      for index, row in main_dataset.iterrows():
        if index.str.contains(search_term):
            return render(request, 'search.html', {'symptoms': row})
        # if index equals the search term
        # {‘symptoms’: list_goes_here}

  return render(request, 'search.html', {'symptoms': []})
