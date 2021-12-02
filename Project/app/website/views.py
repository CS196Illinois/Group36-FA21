from django.http import request
from django.shortcuts import render

import pandas as pd


# Create your views here.
# do something
def search(request):
  if request.method == 'POST':
      form = SearchForm(request.POST)
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
