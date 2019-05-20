"""bulk_news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import view

urlpatterns = [
	url('npr_download/', view.npr_download),
	url('theatlantic_download/', view.theatlantic_download),
	url('interestingengineering_industry_download/', view.interestingengineering_industry_download),

    url('usnews_national_news_download/', view.usnews_national_news_download),
    # url('usnews_business_download/', view.usnews_business_download),
    # url('usnews_technology_download/', view.usnews_technology_download),

    url('washingtonpost_download/', view.washingtonpost_download),
    url('wsj_opinion_download/', view.wsj_opinion_download),
    url('theguardian_download/', view.theguardian_download),
    url('financial_times_download/', view.financial_times_download),
    url('csmonitor_download/', view.csmonitor_download),
    url('newscientist_download/', view.newscientist_download),
    url('nature_download/', view.nature_download),
    url('history_download/', view.history_download),
    url(r'^$', view.index),
]
