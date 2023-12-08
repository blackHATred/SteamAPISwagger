import json


def main():
    # Загружаем API Steam
    with open('api.json') as f:
        api = json.load(f)
    paths = {}

    default_responses = {
        "200": {
            "description": "Успешно"
        },
        "400": {
            "description": "Некорректные данные или переданы не все поля"
        },
        "403": {
            "description": "Невалидный API ключ"
        }
    }
    for key1 in api:
        print(key1)
        for key2 in api[key1]:
            print(f"\t{key2}")
            params = api[key1][key2]
            print(f"\t\t{params}")
            paths[f"/{key1}/{key2}/v{params['version']}"] = {
                params.get("httpmethod", "get").lower(): {
                    "responses": default_responses,
                    "parameters": [
                        {
                            "name": param.get("name"),
                            "in": "query",
                            "description": param.get("description", "Описание не приведено"),
                            "required": not param.get("optional"),
                            "schema": {
                                "format": param.get("type")
                            }
                        } for param in params["parameters"]
                    ],
                    "description": params.get("description", "Описание не приведено"),
                    "tags": [key1]
                }
            }

    swagger = {
        'openapi': '3.0.0',
        'info': {
            'title': 'Steam API',
            'description': 'API для работы с Steam',
            'version': '1.0.0',
        },
        'servers': [
            {
                'url': 'https://api.steampowered.com'
            },
            {
                'url': 'https://partner.steam-api.com'
            }
        ],
        'paths': paths,
        'tags': [{"name": key} for key in api.keys()],
        'externalDocs': {
            'url': 'https://partner.steamgames.com/doc/webapi',
            'description': 'Оригинальный референс на API. Там перечислены не все методы!'
        }
    }
    with open('dist/swagger.json', 'w') as f:
        json.dump(swagger, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
