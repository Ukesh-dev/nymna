import requests


class OneSignalNotification:
    @staticmethod
    def send_request(request):
        try:
            response = requests.post(
                "https://onesignal.com/api/v1/notifications",
                json=request,
                headers={
                    "Authorization": "Basic YTY2ZjdkNmQtNDE5Yi00NmU4LThlNzUtZWYyNWJmMGIxYzgx",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send notification: {str(e)}")

    @staticmethod
    def send(args):
        body = {
            "app_id": "b45d498d-4c33-417e-b842-d6009d3873cd",
            "contents": {"en": args.get('message', '')},
            "headings": {"en": args.get('title', '')},
            "content_available": True,
            # "isIos": True,
            "isAndroid": True,
            # "isAnyWeb": True,
            "priority": 10,
            "included_segments": ["All"]
        }

        if args.get('data'):
            body['data'] = args['data']

        if args.get('image'):
            body['big_picture'] = args['image']
            body['huawei_big_picture'] = args['image']
            body['chrome_web_image'] = args['image']

        if args.get('url'):
            body['url'] = args['url']

        if args.get('players'):
            body['include_player_ids'] = args['players']
            del body['included_segments']

        return OneSignalNotification.send_request(body)