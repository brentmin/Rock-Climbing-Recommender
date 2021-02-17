from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.validators import URLValidator

from .forms import RecInputForm

import ast

import sys
sys.path.append('../../..')

def template(form=None, rec="", latitude=33.8734, longitude=-115.9010, results=[]):
    """
    TODO

    TODO
    """
    template_default = {
        "form": form,
        "recommendations": rec,
        "latitude": latitude,
        "longitude": longitude,
        "results": results
    }

    return template_default

def bootstrap4_index(request):
    # enter the if if the button is pressed on the website
    if(request.method == "POST"):

        form = RecInputForm(request.POST)

        if(form.is_valid()):

            # run the secondary validation code
            inputs = secondary_validation(request)

            # if there are errors, then the bool flag would be true
            if(inputs[1]):
                return render(request, 'index.html', template(form, inputs[1], 
                    inputs[0]["location"][0], inputs[0]["location"][1]))

            # run the main code
            from run import main
            results = main(inputs[0])

            # transform the return dictionary into the proper format for django templates
            trans_results = format_django(results)

            # return the value of the main code
            return render(request, 'index.html', template(form, "", inputs[0]["location"][0], 
                inputs[0]["location"][1], trans_results))

        return render(request, 'index.html', template(form))

    form = RecInputForm()
    return render(request, 'index.html', template(form))

def format_django(results):
    """
    Take the output of the recommender and modify it so that django can automatically put it into
    table form

    :param:     results     The output of the recommender

    :return:    [{"name", "url"}, etc.]     The input recommendations formatted such that django
                                            template and correctly put them into a table
    """
    formatted = []
    for key, value in ast.literal_eval(results)["name"].items():
        formatted.append({
            "name": value,
            "url": f"https://www.mountainproject.com/route/{key}"
        })

    return formatted


def secondary_validation(request):  
    """
    This function runs some secondary validation code that I could not integrate into django
    without it messing up the website style

    :param:     request     The POST request

    :return:    (dict, str)     The dict contains the input to the main function, and the string 
                                contains the error message (can be "")
    """
    # store error string here if necessary
    error_str = ""

    # get the url
    url = request.POST.get("url")

    # validate the url structure
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        error_str += f"Mountain Project URL ({url}) is not a valid user page.\n"

    # validate that the url contains both "mountainproject.com" and "user"
    if((not error_str) and (("mountainproject.com" not in url) or ("user" not in url))):
        error_str += f"Mountain Project URL ({url}) is not a valid user page.\n"

    # get the boulder grades
    bl = int(request.POST.get("boulder_lower"))
    bu = int(request.POST.get("boulder_upper"))

    # validate the boulder grades
    if(bl > bu):
        error_str += f"Lowest Boulder Grade (V{bl}) should be less than or equal to Highest " \
            f"Boulder Grade (V{bu}).\n"

    # get the route grades
    rl = route_to_int(request.POST.get("route_lower"))
    ru = route_to_int(request.POST.get("route_upper"))

    # validate the route grades
    if(rl is None):
        error_str += f"Lowest Route Grade (5.{request.POST.get('route_lower')}) is an invalid " \
            "difficulty.\n"
    if(ru is None):
        error_str += f"Highest Route Grade (5.{request.POST.get('route_upper')}) is an invalid " \
            "difficulty.\n"
    if((rl is not None) and (ru is not None)):
        if(rl > ru):
            error_str += f"Lowest Route Grade (5.{request.POST.get('route_lower')}) should be " \
                f"less than or equal to Highest Route Grade " \
                f"(5.{request.POST.get('route_upper')}).\n"

    # create the config dictionary to pass into main
    inputs = {
        "user_url": request.POST.get("url"),
        "location": [request.POST.get("latitude"), request.POST.get("longitude")],
        "recommender": request.POST.get("rec"),
        "num_recs": request.POST.get("num_recs"),
        "difficulty_range": {
            "boulder": [bl, bu],
            "route": [rl, ru]
        }
    }
    return (inputs, error_str)

def route_to_int(route_str):
    """
    This function takes a route string and turns it into an integer

    :param:     route_str   The stuff after the "5.". Can be anything from "1" to "15d"

    :return:    int         An integer representation of the grade
    """
    mapping = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10a", "10b", "10c", "10d", "11a", 
        "11b", "11c", "11d", "12a", "12b", "12c", "12d", "13a", "13b", "13c", "13d", "14a", "14b", 
        "14c", "14d", "15a", "15b", "15c", "15d"]

    try:
        return mapping.index(route_str.lower())
    except ValueError:
        return None
