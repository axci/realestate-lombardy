from django.shortcuts import render
from scraper.models import Apartment
from scraper.forms import ApartmentForm
import subprocess
import plotly.express as px
import folium  # geo maps
from folium.plugins import FastMarkerCluster
from django.db.models import Sum, Count

# Create your views here.
def price_to_area(request):
    apartments = Apartment.objects.all()


    # FORM FILTER
    price_start = request.GET.get('price_from')
    price_end = request.GET.get('price_to')
    area_start = request.GET.get('area_from')
    area_end = request.GET.get('area_to')
    condition = request.GET.get('condition')
    typology = request.GET.get('typology')

    
    if price_start:
        apartments = apartments.filter(price__gte=price_start)
    if price_end:
        apartments = apartments.filter(price__lte=price_end)
    if area_start:
        apartments = apartments.filter(area__gte=area_start)
    if area_end:
        apartments = apartments.filter(area__gte=area_end)
    if condition:
        apartments = apartments.filter(condition=condition)
    if typology:
        apartments = apartments.filter(typology=typology)

    number_of_results = apartments.count()

    
    # Create a dictionary with provincies: av.price/m2
    provincies = apartments.values_list('province', flat=True).distinct()
    province_price = apartments.values('province').annotate(total_amount = Sum('price') / Sum('area')) 
    province_price_dict = {item['province']: item['total_amount'] for item in province_price} 
    province_price_dict = dict(sorted(province_price_dict.items(), key=lambda x: x[1], reverse=True))
    
    # Create a dictionary with cities: av.price/m2
    cities = apartments.values_list('city', flat=True).distinct()
    #city_price = apartments.values('city').annotate(total_amount = Sum('price') / Sum('area'))
    city_price = apartments.values('city').annotate(area_count=Count('city')).filter(area_count__gte=5).annotate(total_amount=Sum('price')/Sum('area'))
    city_price_dict = {item['city']: item['total_amount'] for item in city_price} 
    city_price_dict = dict(sorted(city_price_dict.items(), key=lambda x: x[1], reverse=False))
    # dictionary of top 10 elements
    cities_top = dict(list(city_price_dict.items())[-20:])

    # Folium Map
    center = [45.4667971, 9.5904984]
    m = folium.Map(location=center, zoom_start=8, )

    latitudes = [apartment.latitude for apartment in apartments]
    longitudes = [apartment.longitude for apartment in apartments]
    FastMarkerCluster(data=list(zip(latitudes, longitudes))).add_to(m)
    




    # Chart in plotly for Provinces
    fig1 = px.bar(
        x=province_price_dict.keys(), 
        y=province_price_dict.values(),         
        title='By Province', 
        labels={'x':'', 'y':'€/m<sup>2</sup>'},
        width=580,
        height=580,
        
        )

    fig1.update_layout(
        margin=dict(r=5),
        plot_bgcolor='#fff',
        paper_bgcolor='#f9e0ae',
        )
    
    fig1.update_traces(marker=dict(color='#c24914'),)
    fig1.update_yaxes(gridcolor='#f9e0ae')

    

    # Chart in plotly for Cities. Top 10
    fig2 = px.bar(
        x=cities_top.values(), 
        y=cities_top.keys(),         
        title='Top 20 Cities', 
        labels={'x':'City', 'y':'€/m<sup>2</sup>'},
        hover_data = [cities_top.values()],
        width=580,
        height=580,
        )
    
    fig2.update_layout(
        margin=dict(r=10),
        plot_bgcolor='#fff',
        paper_bgcolor='#f9e0ae',

        )

    fig2.update_traces(marker=dict(color='#c24914'),)
    fig2.update_xaxes(gridcolor='#f9e0ae')
    

    webscrape = subprocess.call(["python", "manage.py", "scraper"])

    context = {
        'form': ApartmentForm(), 
        'results': number_of_results, 
        'chart1': fig1.to_html(), 
        'chart2': fig2.to_html(), 
        'chart_map': m._repr_html_(),
        'scrape': webscrape,
        }

    return render(request, 'scraper/index.html', context)