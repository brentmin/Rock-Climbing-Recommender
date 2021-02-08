from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import RecInputForm

import sys
sys.path.append('../../..')

def bootstrap4_index(request):
    # enter the if if the button is pressed on the website
    if(request.method == "POST"):
        # # import the main function and run it with the selected options
        # from run import main
        # config = {"mongodb": True, "top_pop": True}
        # # result = main(config)

        # test = {"user_url": request.POST.get("user_url"),
        #     "lat": request.POST.get("lat"),
        #     "long": request.POST.get("long"),
        #     "num_rec": request.POST.get("num-rec"),
        #     "recommenders": [request.POST.get("top-pop"), request.POST.get("other-rec")]}

        # # return the template but with the returned contents of main
        # return render(request, 'index.html', {"test": test})

        form = RecInputForm(request.POST)

        if(form.is_valid()):

            # create the config dictionary to pass into amin
            inputs = {
                "user_url": request.POST.get("url"),
                "location": [request.POST.get("latitude"), request.POST.get("longitude")],
                "recommender": request.POST.get("rec")
            }

            # run the main code
            from run import main
            result = main(inputs)

            # return the value of the main code
            return render(request, 'index.html', {"form": form, "recommendations": result})

        else:
            form = RecInputForm()

        return render(request, 'index.html', {"form": form, "recommendations": "bad submit"})

    form = RecInputForm()
    return render(request, 'index.html', {"form": form, "recommendations": "initial open"})
