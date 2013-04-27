from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import modshogun as sg
import numpy as np
import json


def index(request):
    return render_to_response("demos/digit/index.html", context_instance=RequestContext(request))

def run_binary(request):
    points = json.loads(request.GET["points"])
    C = json.loads(request.GET["C"])
    width = json.loads(request.GET["width"])
    height = json.loads(request.GET["height"])

    try:
        features, labels = _get_binary_features(points)
    except ValueError as e:
        return HttpResponse(json.dumps({"status": e.message}))

    try:
        kernel = _get_kernel(request, features)
    except ValueError as e:
        return HttpResponse(json.dumps({"status": e.message}))

    try:
        x, y, z = classify(sg.LibSVM, features, labels, kernel, x_size=width, y_size=height, C=C)
    except Exception as e:
        return HttpResponse(json.dumps({"status": repr(e)}))

    data = {"status": "ok", "domain": [-1, 1], "max": np.max(z), "min": np.min(z), "z": z.tolist()}

    return HttpResponse(json.dumps(data))


def _get_binary_features(a):
    pass


def _get_kernel(a):
    pass


def classify(a):
    pass
