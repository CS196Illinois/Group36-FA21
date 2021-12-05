from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import SymptomsForm

import pandas as pd
import os

# Create your views here.

def home(request):
    return render(request, 'index.html', {})


def search(request):
  if request.method == 'POST':
      form = SymptomsForm(request.POST)
      if form.is_valid():
          search_term = form.cleaned_data['search']
      else:
          return HttpResponse("Invalid form input")
      main_dataset = pd.read_csv(os.path.join('app/data/dataset.csv'))
      main_dataset.set_index('Disease', inplace=True)
      map_of_diseases = {}
      for index, row in main_dataset.iterrows():
          if row.str.contains(search_term):
              map_of_diseases[index] = row.to_list()
      tuples = zip(map_of_diseases.keys(), map_of_diseases.values())
      return render(request, 'search.html', {'diseases': tuples})

  return render(request, 'search.html', {'diseases': [], 'symptoms': []})