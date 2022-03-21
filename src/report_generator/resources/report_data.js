var report = {
    "start_time": 1648423446.2535732,
    "end_time": 1648423450.644001,
    "entries": {
        "my-book": {
            "key": "my-book",
            "type": "book",
            "file_path": "files/my.bib",
            "line_number": 1,
            "fields": {
                "author": "John Doe",
                "pages": 100,
                "isbn": "123456789"
            }
        },
        "my-article": {
            "key": "my-article",
            "type": "article",
            "file_path": "files/my.bib",
            "line_number": 10,
            "fields": {
                "author": "John Doe",
                "pages": 100,
                "isbn": "123456789"
            }
        },
        "something-key": {
            "key": "something-key",
            "type": "article",
            "file_path": "files/my.bib",
            "line_number": 15,
            "fields": {
                "author": "John Doe",
                "pages": 100,
                "isbn": "123456789"
            }
        },
    },
    "failures": [
        {
            "type": "entry",
            "entry_key": "my-book",
            "message": "Entry 'my-book' already exists",
            "hints": [
                {
                    "title": "Something example",
                    "recommendation": "Something example",
                    "reason": "Something example",
                    "phase": "Something example"
                }
            ]
        },
        {
            "type": "fileline",
            "file_path": "files/my.bib",
            "line_number": 1,
            "message": "Entry 'my-book' already existshawegawehgkhllkawegheawtklkwaegfff",
        }
    ]
}
