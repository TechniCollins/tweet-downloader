from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Hashtag, Endpoint, Tweet, Volume

from django.core.management import call_command

import csv


def hashtagsEditor(request):
    hashtags = Hashtag.objects.all().prefetch_related("endpoint")
    standard_hashtags = hashtags.filter(endpoint__name="standard")
    academic_hashtags = hashtags.filter(endpoint__name="academic", enabled=True)

    endpoints = Endpoint.objects.all()

    if request.method == 'POST':
        name = request.POST.get("name")
        endpoint = endpoints.get(name=request.POST.get("endpoint"))

        hashtag_object = Hashtag.objects.get_or_create(
            name=name,
            endpoint=endpoint,
        )

        # if no object was created, it means it already
        # exists. In this case, update the enabled attribute
        # to True
        if not hashtag_object[1]:
            hashtag_object[0].enabled = True
            hashtag_object[0].save()

        return redirect('/')

    elif request.method == 'GET':
        hashtag_id = request.GET.get("hashtag_id")
        enabled = request.GET.get("enabled")

        if hashtag_id and enabled:
            instance = Hashtag.objects.get(id=hashtag_id)

            if enabled.lower() == "true":
                instance.enabled = True
            else:
                instance.enabled = False

            instance.save()

            return redirect('/')

    context = {
        "standard_hashtags": standard_hashtags,
        "academic_hashtags": academic_hashtags
    }

    return render(request, 'index.html', context)


def dateToTimestamp(date, time_string):
    return f"{date}T{time_string}Z"


def fullArchive(request):
    start = request.POST.get("startDate")
    end = request.POST.get("endDate")
    get_replies = True if request.POST.get("getReplies", "").lower() == "on" else False
    include_retweets = True if request.POST.get("includeRetweets", "").lower() == "on" else False

    command_arguments = {
        "endpoint": "academic",
        "start_time": dateToTimestamp(start, "00:00:00"),
        "end_time": dateToTimestamp(end, "23:59:59")
    }

    if get_replies:
        command_arguments["get_replies"] = True

    if include_retweets:
        command_arguments["include_retweets"] = True

    # Call command
    call_command('get_tweets', **command_arguments)

    return HttpResponse("Search ended successfully")


def renderCSV(headers, queryset, filename):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'},
    )

    writer = csv.writer(response)

    # Write first row (Headers)
    writer.writerow(headers)

    for row in queryset:
        writer.writerow([row[field] for field in headers])

    return response

def exportData(request):
    fromdate = request.POST.get("fromdate")
    todate = request.POST.get("todate")
    hashtag = Hashtag.objects.get(id=request.POST.get("hashtag"))
    download = request.POST.get("download")

    if download == "volumes":
        volume_fields = ["hashtag__name", "start_time", "end_time", "tweet_count"]
        return renderCSV(
            ["hashtag__name", "start_time", "end_time", "tweet_count"],
            Volume.objects.filter(hashtag=hashtag).values(*volume_fields),
            f"volumes_{hashtag.name}.csv"
        )
    else:
        # Render tweets CSV
        fields = [f.name for f in Tweet._meta.fields]
        queryset = Tweet.objects.filter(
            tweethashtagmap__hashtag=hashtag,
            created_at__range=(fromdate, todate)
        ).values(*fields)

        return renderCSV(fields, queryset, "tweets.csv")
