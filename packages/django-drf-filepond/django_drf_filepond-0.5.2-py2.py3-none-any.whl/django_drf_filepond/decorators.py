# This module contains function dectorators used in django-drf-filepond
#
# drf_filepond_require_settings: used to mark that a function requires
#    one or more settings to be set for it to be able to run correctly.
#


# A decorator used to specify that a function requires one or more Django
# settings to be set for it to be able to run. If the specified settings are
# undefined 
#
def drf_filepond_require_settings(func, the_settings, op):
