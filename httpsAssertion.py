import sys
import os
import slack
from dotenv import load_dotenv
from urllib import request, error

######## FUNCTIONS ########
load_dotenv()


def checkURLStatus(dataFromRequest):
    for url in dataFromRequest:
        if url[1] != 200:
            return False
    return True


# Add more information if return status is 0 or 1
def buildWarning(report, status):
    if status == 0:
        report = report + " (Not valid URL - Unhandled error)"
    elif status == 1:
        report = report + " (Service not found)"

    # Make failures display in bold
    report = '*' + report + '*'

    return report + ":bangbang:"


def buildReport(dataFromRequest):
    message = ":warning: *Status Summary* :warning:\n"
    if checkURLStatus(dataFromRequest):
        message = ":heavy_check_mark: *Status Summary* :heavy_check_mark:\n"
    for url in dataFromRequest:
        urlReport = url[0] + " - StatusCode: " + str(url[1])

        if url[1] != 200:
            urlReport = buildWarning(urlReport, url[1])

        message = message + '\n' + urlReport
    return message


def getHttpsStatus(url):
    try:
        status = request.urlopen(url)
    except error.HTTPError as e:
        print("ERROR! HTTPError -> " + url + ": " + str(e.code))
        return url, e.code
    except error.URLError as e:
        if hasattr(e, 'code'):
            print("ERROR! URLError -> " + url + ": " + str(e.code))
            return url, e.code
        else:
            print("ERROR! URLError: No Service Found -> " + url)
            return url, 1
    except:
        print("ERROR - Unhandled error")
        return url, 0

    return url, status.getcode()


def getLandingURLs():
    text_file = open("landingURLs.txt", "r")
    landingURLs = text_file.read().split('\n')

    # Remove last element if being ''
    if landingURLs[-1] == '':
        landingURLs.pop()
        # landingURLs = landingURLs[:-1]

    text_file.close()
    return landingURLs


def sendSlackAlert(report):
    sc = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    sc.chat_postMessage(
        channel=os.environ['SLACK_CHANNEL'],
        text=report,
        username=os.environ['SLACK_USERNAME'],
        icon_emoji=':robot_face:'
    )
    return True


######## MAIN ########

landingURLs = getLandingURLs()

statusFromURLs = list(map(getHttpsStatus, landingURLs))

report = buildReport(statusFromURLs)

sendSlackAlert(report)
