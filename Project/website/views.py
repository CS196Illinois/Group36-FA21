from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *

import pandas as pd
import os

# Create your views here.

def home(request):
    return render(request, 'index.html', {})

def routing(request):
    form = SearchForm(request.POST)
    if request.method == 'POST':
        print(form)
        if form.is_valid():
            search_type = form.cleaned_data['search_term']
        else:
            print(form.cleaned_data)
            return HttpResponse("Invalid form")
        if search_type == 'Symptom':
            symptom_search(request)
    return HttpResponse("Invalid form")

def symptom_search(request):
  if request.method == 'POST':
      form = SearchForm(request.POST)
      print(form.errors)
      if form.is_valid():
          search_term = form.cleaned_data['search_input']
      else:
          return HttpResponse("Invalid form input")
      search_term = search_term.split(',')
      for i in range(len(search_term)):
          search_term[i] = search_term[i].strip().replace(' ', '_')

      main_dataset = pd.read_csv(os.path.join('app/data/dataset.csv'))
      main_dataset.set_index('Disease', inplace=True)
      map_of_diseases = {}
      containsAll = True
      for index, row in main_dataset.iterrows():
          containsAll = True
          for term in search_term:
              if not row.str.contains(term).any():
                  containsAll = False
                  break
          if containsAll:
            map_of_diseases[index] = ", ".join([s.replace('_', ' ') for s in row.to_list() if pd.notna(s)])
              
      tuples = zip(map_of_diseases.keys(), map_of_diseases.values())
      return render(request, 'search.html', {'diseases': tuples, 'path': '/search-symptoms/'})
  return render(request, 'search.html', {'diseases': [], 'symptoms': [], 'path': '/search-symptoms/'})

def search_disease(request):
  if request.method == 'POST':
      form = SearchForm(request.POST)
      if form.is_valid():
        search_term = form.cleaned_data['search_term']
      main_dataset = pd.read_csv(os.path.join('app/data/dataset.csv'))
      main_dataset.set_index('Disease', inplace=True)
      for index, row in main_dataset.iterrows():
        if index.lower() == search_term.lower():
            tuples = [(index, ", ".join([s.replace('_', ' ') for s in row.to_list() if pd.notna(s)]))]
            print(tuples)
            return render(request, 'search.html', {'diseases': tuples, 'path': '/search-diseases/'})
        # if index equals the search term
        # {‘symptoms’: list_goes_here}

  return render(request, 'search.html', {'diseases': [], 'path': '/search-diseases/'})
