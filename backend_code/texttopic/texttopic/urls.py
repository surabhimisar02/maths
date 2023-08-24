"""texttopic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_picture/', views.convert_text_q_to_picture_q),
    path('get_picture_2/', views.convert_pictorial_text_q_to_picture_q),
    path('counting_pictures/', views.counting_pictures),
    path('random_operations_ques_generator/', views.rand_ques_generator),
    path('random_operations_ques_generator_with_exp/', views.rand_ques_generator_with_text_explanation),
    path('fraction_question_generator/', views.fraction_question_generator),
    path('obtaining_objects/', views.obtaining_objects),
    path('LCM_numbers/', views.LCM_numbers),
    path('identifying_shapes/', views.identifying_shapes),
    path('measuring_angles/', views.measure_angle),
    path('identifying_angles/', views.identifying_angle),
    path('displaying_angles/', views.display_angle),
    path('naming_figures/', views.naming_fig),
    path('naming_figures_single_question/', views.naming_fig_single_ques),
    path('convert_text_to_text/', views.txt_to_txt),
    path('convert_text_to_speech/', views.text_to_speech),
   path('get_q/', views.image_q),

]
