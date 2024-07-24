# Book Recommendation

This simple app allows authenticated users to rate books and then get suggestion for their favorite genre.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install
```

Check the setting.py file to configure DATABASE connection settings.

## Usage

You need to get an access token by sending a post request to **/api/login** endpoint.
The generated token should be the value of Authorization header, like the following:
**JWT yourtoken**

Then you can send a your requests to available endpoints described below:

| Endpoint              | HTTP Method  | Description       |
| :-------------------  | :------:     | :---------------- |
| /api/book/list        |   GET        | List all books                                                          |
| /api/review/add       |   POST       | Create a review record for the given book with a rating between 1 and 5 |
| /api/review/update    |  PATCH       | Update rating for an existing review                                    |
| /api/review/delete    |  DELETE      | Delete a review for the given book                                      |
| /api/suggest          |  DELETE      | Suggest a list of books based on user's favorite genre                  |

## License

[MIT](https://choosealicense.com/licenses/mit/)
