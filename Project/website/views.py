from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *

import pandas as pd
import os
import requests

# Create your views here.

def home(request):
    return render(request, 'index.html', {})

def routing(request):
    form = SearchForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            search_type = form.cleaned_data['search_term']
            search_word = form.cleaned_data['search_input']
        else:
            print(form.cleaned_data)
            return HttpResponse("Invalid form")
        if search_type == 'Symptoms':
            return render(request, 'search.html', symptom_search_logic(search_word))
        if search_type == 'Disease':
            return render(request, 'search.html', search_disease_logic(search_word))
        if search_type == 'Hospital':
            return render(request, 'search.html', hospital_search_logic(search_word))
    return HttpResponse("Invalid form")

def symptom_search(request):
  if request.method == 'POST':
      form = ResultsPageForm(request.POST)
      print(form.errors)
      if form.is_valid():
        search_term = form.cleaned_data['search_input']
        return render(request, 'search.html', symptom_search_logic(search_term))
      else:
          return HttpResponse("Invalid form input")
  return render(request, 'search.html', {'diseases': [], 'symptoms': [], 'path': '/search-symptoms/'})
      
def symptom_search_logic(search_term):
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
            map_of_diseases[index] = "Symptoms: " + ", ".join([s.replace('_', ' ') for s in row.to_list() if pd.notna(s)])
            
    tuples = zip(map_of_diseases.keys(), map_of_diseases.values())
    return {'diseases': tuples, 'path': '/search-symptoms/'}

def search_disease(request):
  if request.method == 'POST':
      form = ResultsPageForm(request.POST)
      if form.is_valid():
        search_term = form.cleaned_data['search_input']
        return render(request, 'search.html', search_disease_logic(search_term))
      else:
          print(form.cleaned_data)
          return HttpResponse("Invalid Form")
  return render(request, 'search.html', {'diseases': [], 'path': '/search-diseases/'})
        # if index equals the search term
        # {‘symptoms’: list_goes_here}

def search_disease_logic(search_term):
    main_dataset = pd.read_csv(os.path.join('app/data/dataset.csv'))
    main_dataset.set_index('Disease', inplace=True)
    for index, row in main_dataset.iterrows():
        if index.lower() == search_term.lower():
            tuples = [(index, "Symptoms: " + ", ".join([s.replace('_', ' ') for s in row.to_list() if pd.notna(s)]))]
            return {'diseases': tuples, 'path': '/search-diseases/'}
    return {}

def hospital_search(request):
  if request.method == 'POST':
      form = SearchForm(request.POST)
      print(form.errors)
      if form.is_valid():
          search_term = form.cleaned_data['search_input']
      else:
          return HttpResponse("Invalid form input")
      
      return render(request, 'clinics.html', hospital_search_logic(search_term))
  return render(request, 'clinics.html', {'diseases': [], 'path': '/search-clinics/'})
    
def hospital_search_logic(search_input):
    tuples = []
    result = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyD8lesvuvvaM9NYaTipX2oDlDbMy1VKJbY&cx=017576662512468239146:omuauf_lfve&q=hospitals near me")

    r = result.json()

    print(r)

    for i in r['items']:
        title = f"<a href=\"{i['link']}\">{i['title']}</a>"
        t = (title, i['snippet'])
        tuples.append(t)
    return {'diseases': tuples, 'path': '/search-clinics/'}
