from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',

    url(r'^ping/', 'ping'),
    url(r'^whosefaceisinthis/', 'whosefaceisinthis'),
    url(r'^whosevoiceisinthis/', 'whosevoiceisinthis'),
)
