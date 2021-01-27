from django.shortcuts import render

import sys
sys.path.append('../../..')

def bootstrap4_index(request):
    # enter the if if the button is pressed on the website
    if(request.method == "POST" and "run_script" in request.POST):
        # import the main function and run it with the selected options
        from run import main
        config = {"mongodb": True, "top_pop": True}
        result = main(config)

        # return the template but with the returned contents of main
        return render(request, 'index.html', {"test": result})

    return render(request, 'index.html', {"test": "click above button to see the top 10 most popular routes"})
