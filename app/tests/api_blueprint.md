FORMAT: 1A
HOST: http://polls.apiblueprint.org/

# Project CN

## Users [/users]

### List all users [GET]
Access: Admins

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": [
                {
                    "id": "507f1f77bcf86cd799439012",
                    "type": "admin",
                    "username": "john",
                    "usernameSet": true,
                    "emailAddress": "john.the.admin.91230+5@gmail.com,
                    "bio": "I am an admin",
                    "score": 12499,
                    "createdAt": "2018-02-04 17:15:13",
                    "lastLoginAt": "2018-02-04 17:15:13"
                },
                {
                    "id": "507f1f77bcf86cd799439011",
                    "type": "user",
                    "username": "runningpidgeon",
                    "usernameSet": false,
                    "emailAddress": null,
                    "bio": "I am a developer",
                    "score": 4918,
                    "createdAt": "2018-01-01 17:15:13",
                    "lastLoginAt": "2018-01-01 17:15:13"
                }
            ]
        }

### Create a new user [POST]
Access: Admins

+ Attributes
    + type (string) - Type of user (user|admin|moderator)
    + username (string) - Username
    + usernameSet (boolean) - Has the username been permanently set?
    + emailAddress (string) - Email address (nullable)
    + bio (string) - Description of the user

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "type": "user",
                "username": "bob_marley",
                "usernameSet": true,
                "emailAddress": null,
                "bio": "I am a developer"
            }

+ Response 201 (application/json)

        {
            "meta": {
                "code": "201",
                "message": "ok"
            },
            "response": {
                "id": "507f1f77bcf86cd799439011",
                "type": "user",
                "username": "bob_marley",
                "usernameSet": true,
                "emailAddress": null,
                "bio": "I am a developer",
                "score": 4918,
                "createdAt": "2018-01-01 17:15:12",
                "lastLoginAt": "2018-01-01 17:15:13"
            }
        }

### Register or login [POST /users/auth]
Access: Users/Admins (requires authorization header, after Auth0 callback)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "created"
            },
            "response": {
                "id": "507f1f77bcf86cd799439011",
                "type": "user",
                "username": "movingblizzard",
                "usernameSet": false,
                "emailAddress": null,
                "bio": "",
                "score": 0,
                "createdAt": "2018-02-10 17:15:12",
                "lastLoginAt": "2018-02-10 17:15:12"
            }
        }


## User [/users/{id}]

+ Parameters
    + id (string) - ID of the User (or "me" to fetch/use own user)

### Get a user [GET]
Access: Users (limited info from other users), Admins (any ID)

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "id": "507f1f77bcf86cd799439011",
                "type": "user",
                "username": "bob_marley",
                "usernameSet": true,
                "emailAddress": null,
                "bio": "I am a developer",
                "score": 4918,
                "createdAt": "2018-01-01 17:15:13",
                "lastLoginAt": "2018-01-01 17:15:13"
            }
        }

### Modify a user [POST]
Access: Users (only own user), Admins (any ID)

+ Attributes
    + username (string) - Username (can only be set once)
    + emailAddress (string) - Email address (nullable)
    + bio (string) - Description of the user

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "username": "bob_marley",
                "emailAddress": "bob.marley.1234123@gmail.com",
                "bio": "I am a developer"
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "id": "507f1f77bcf86cd799439011",
                "type": "user",
                "username": "bob_marley",
                "usernameSet": true,
                "emailAddress": null,
                "bio": "I am a developer",
                "score": 4918,
                "createdAt": "2018-01-01 17:15:13",
                "lastLoginAt": "2018-01-01 17:14:12"
            }
        }

### Delete a user [DELETE]
Access: Users (only own user), Admins (any ID)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "deleted"
            }
        }

### Get list of notifications for a user [GET /users/{id}/notifications]
Access: Users (only for own user), Admins (any ID)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": [
                {
                    "id": "dO9vk1aSi941Fo1fFazF9kggAf",
                    "user": {
                        "id": "507f1f77bcf86cd799439011",
                        "username": "bob_marley"
                    },
                    "title": "Greg has upvoted your post",
                    "message": "Greg upvoted your post from the 17th of December titled: XYZ",
                    "comment": null,
                    "article": {
                        "id": "D0fjAi391Fao3Fa91Fos98f",
                        "title": "XYZ"
                    },
                    "createdAt": "2017-05-06 17:15:10",
                    "read": true
                }
            ]
        }


## Articles [/articles]

### Get list of articles (default = ranked) [GET]
Access: Anyone

+ Attributes
    + q (string) - Wildcard search (optional)
    + coins (string) - Comma-separated list of coin index names to search for
    + user (string) - User ID to filter for (e.g. "get all my own posts")
    + type (string) - Type of list to use (new|ranked), default is "ranked"

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": [
                {
                    "id": "507f1f77bcCx6cd799439021",
                    "title": "Google search is empowering the world",
                    "description": null,
                    "link": "https://google.com",
                    "type": "link",
                    "user": {
                        "id": "507f1f77bcf86cd799439011",
                        "username": "bob_marley"
                    },
                    "rankScore": 352,
                    "flags": 1,
                    "createdAt": "2018-01-01 17:15:12",
                    "comments": 3
                },
                {
                   "id": "107f1f87bcCx6cd799439022",
                    "title": "An interesting cat",
                    "description": "Don't eat the plant please",
                    "link": null,
                    "type": "article",
                    "user": {
                        "id": "507f1f77bcf86cd799439011",
                        "username": "bob_marley"
                    },
                    "rankScore": 350,
                    "flags": 0,
                    "createdAt": "2018-01-01 17:15:12",
                    "comments": 0
                }
            ]
        }

### Post a new article [POST]
Access: Users, Admins

+ Attributes
    + title (string) - Title of the article or link
    + description (string) - Description (for posts only, nullable)
    + link (string) - URL (nullable)
    + type (string) - Type of article (link|post)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "title": "Google search is empowering the world",
                "description": null,
                "link": "https://google.com",
                "type": "link"
            }

+ Response 201 (application/json)

        {
            "meta": {
                "code": "201",
                "message": "ok"
            },
            "response": {
                "id": "507f1f77bcCx6cd799439021",
                "title": "Google search is empowering the world",
                "description": null,
                "link": "https://google.com",
                "type": "link",
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "username": "bob_marley"
                },
                "rankScore": 352,
                "flags": 0,
                "createdAt": "2018-01-01 17:15:12",
                "comments": [
                ]
            }
        }


## Article [/articles/{id}]

+ Parameters
    + id (string) - ID of the Article

### Get the contents of an article [GET]
Access: Anyone

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "id": "507f1f77bcCx6cd799439021",
                "title": "Google search is empowering the world",
                "description": null,
                "link": "https://google.com",
                "type": "link",
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "username": "bob_marley"
                },
                "rankScore": 352,
                "flags": 0,
                "createdAt": "2018-01-01 17:15:12",
                "comments": [
                    {
                        "id": "207f1fZ7bfCx6cd7g9439021",
                        "message": "I don't believe the answer is to ban cats from eating plants.",
                        "user": {
                            "id": "507f1f77bcf86cd799439011",
                            "username": "bob_marley"
                        },
                        "votes": 5,
                        "flags": 0,
                        "createdAt": "2018-01-01 17:15:12",
                        "deletedAt": null,
                        "children": [
                            {
                                "id": "42zF1fBzbfCx6cd7g9439021",
                                "message": "What the fuck are you talking about dude?",
                                "user": {
                                    "id": "307f1f77bcf86cd7994390d1",
                                    "username": "throwaway19"
                                },
                                "votes": 0,
                                "flags": 1,
                                "createdAt": "2018-01-02 17:15:12",
                                "deletedAt": null,
                                "children": []
                            }
                        ]
                    }
                ]
            }
        }

### Modify article [POST]
Access: Users (own articles only), Admins (any article)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "title": "Google search is allowing people to find things",
                "description": "Incredible content!,
                "link": "https://google.com"
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                {
                    "id": "507f1f77bcCx6cd799439021",
                    "title": "Google search is allowing people to find things",
                    "description": null,
                    "link": "https://google.com",
                    "type": "link",
                    "user": {
                        "id": "507f1f77bcf86cd799439011",
                        "username": "bob_marley"
                    },
                    "score": 352,
                    "flags": 0,
                    "createdAt": "2018-01-01 17:15:12",
                    "comments": [
                    ]
                }
            }
        }

### Delete article [DELETE]
Access: Users (own articles only), Admins (any article)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "deleted"
            }
        }

### Upvote/downvote an article [POST /articles/{id}/vote]
Access: Users, Admins

+ Attributes
    + type (string) - Type of vote (upvote|downvote|unvote)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "type": "upvote"
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "updated"
            }
        }

### Flag/unflag an article as inappropriate/spam [POST /articles/{id}/flag POST]
Access: Users, Admins

+ Attributes
    + type (string) - Type of flag (flag|unflag)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "type": "flag"
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "updated"
            }
        }


## Comments [/articles/{id}/comments]

+ Parameters
    + id (string) - ID of the Article

### Post a new comment on the article [POST]
Access: Users, Admins

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "message": "Stop eating my plants Bob.",
                "articleId": "507f1f77bcCx6cd799439021"
            }

+ Response 201 (application/json)

        {
            "meta": {
                "code": "201",
                "message": "ok"
            },
            "response": {
                "id": "207f1fZ7bfCx6cd7g9439021",
                "message": "I don't believe the answer is to ban cats from eating plants.",
                "article": {
                    "id": "507f1f77bcCx6cd799439021",
                    "title": "Google search is empowering the world"
                },
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "username": "bob_marley"
                },
                "votes": 5,
                "flags": 0,
                "createdAt": "2018-01-01 17:15:12",
                "deletedAt": null
            }
        }


## Comment [/articles/{id}/comments/{comment_id}]

+ Parameters
    + id (string) - ID of the Article
    + comment_id (string) - ID of the Comment

### Returns a comment (and it's children) based on ID [GET]
Access: Anyone

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "id": "207f1fZ7bfCx6cd7g9439021",
                "message": "I don't believe the answer is to ban cats from eating plants.",
                "article": {
                    "id": "507f1f77bcCx6cd799439021",
                    "title": "Google search is empowering the world"
                },
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "username": "bob_marley"
                },
                "votes": 5,
                "flags": 0,
                "createdAt": "2018-01-01 17:15:12",
                "deletedAt": null,
                "children": []
            }
        }

### Modify a comment [POST]
Access: Users (own comments only), Admins (any comment)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "message": "I don't believe the answer is to eat cats instead of plants."
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "id": "207f1fZ7bfCx6cd7g9439021",
                "message": "I don't believe the answer is to eat cats instead of plants.",
                "article": {
                    "id": "507f1f77bcCx6cd799439021",
                    "title": "Google search is empowering the world"
                },
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "username": "bob_marley"
                },
                "votes": 5,
                "flags": 0,
                "createdAt": "2018-01-01 17:15:12",
                "deletedAt": null
            }
        }

### Delete a comment [DELETE]
Access: Users (own comments only), Admins (any comment).
Comments with replies or votes will be soft-deleted

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "deleted"
            }
        }

### Upvote/downvote a comment [POST /articles/{id}/comments/{comment_id}/vote]
Access: Users, Admins

+ Attributes
    + type (string) - Type of vote (upvote|downvote|unvote)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "type": "unvote"
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "updated"
            }
        }

### Flag/unflag a comment as inappropriate/spam [POST /articles/{id}/comments/{comment_id}/flag]
Access: Users, Admins

+ Attributes
    + type (string) - Type of flag (flag|unflag)

+ Request (application/json)

    + Headers

            Authorization: Bearer xyz

    + Body

            {
                "type": "unflag"
            }

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": {
                "status": "updated"
            }
        }


## Reports [/reports]

### Get trends for the top/trending coins [GET /reports/cointrend]
Access: Anyone

+ Response 200 (application/json)

        {
            "meta": {
                "code": "200",
                "message": "ok"
            },
            "response": [
                {
                    "Status": "TODO"
                }
            ]
        }
