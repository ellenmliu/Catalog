import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///categoryitem.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

category_json = json.loads("""{
  "users": [
    {
      "name": "RoboBarita",
      "email": "tinnyTim@udacity.com",
      "picture": "https://pbs.twimg.com/profile_images/2671170543/\
             18debd694829ed78203a5a36dd364160_400x400.png"
    }
  ],
  "categories": [
    {
      "name": "Soccer",
      "items": [
        {
          "name": "Soccer Ball",
          "description": "Can't play soccer without a ball",
          "user_id": 1
        },
        {
          "name": "Cleats",
          "description": "Helps with grip",
          "user_id": 1
        }
      ]
    },
    {
      "name": "Basketball",
      "items": [
        {
          "name": "Basketball",
          "description": "Signed by Jordan himself",
          "user_id": 1
        },
        {
          "name": "Shoes",
          "description": "Got them hops",
          "user_id": 1
        }
      ]
    },
    {
      "name": "Baseball",
      "items": [
        {
          "name": "Bat",
          "description": "Hit that homerun",
          "user_id": 1
        },
        {
          "name": "Cap",
          "description": "Get the look of a baseball player",
          "user_id": 1
        }
      ]
    },
    {
      "name": "Badminton",
      "items": [
        {
          "name": "Raquet",
          "description": "Strong and light",
          "user_id": 1
        },
        {
          "name": "Net",
          "description": "Play anywhere",
          "user_id": 1
        }
      ]
    },
    {
      "name": "Skating",
      "items": [
        {
          "name": "Skates",
          "description": "Fastest skates around",
          "user_id": 1
        },
        {
          "name": "Helmet",
          "description": "Stay safe",
          "user_id": 1
        }
      ]
    },
    {
      "name": "Hockey",
      "items": [
        {
          "name": "Hockey Stick",
          "description": "Get some goals",
          "user_id": 1
        },
        {
          "name": "Knee pads",
          "description": "Protection is key",
          "user_id": 1
        }
      ]
    },
    {
      "name": "Snowboarding",
      "items": [
        {
          "name": "Googles",
          "description": "The whites of the snow won't stop you",
          "user_id": 1
        },
        {
          "name": "Snowboard",
          "description": "Customizable",
          "user_id": 1
        }
      ]
    }
  ]
}""")


# Adding Users
for u in category_json['users']:
    newUser = User(
        name=str(u['name']),
        email=str(u['email']),
        picture=str(u['picture'])
    )
    session.add(newUser)
    session.commit()

# Adding categories and the items
for c in category_json['categories']:
    newCategory = Category(name=str(c['name']))
    session.add(newCategory)
    session.commit()
    if c['items']:
        for i in c['items']:
            newItem = Item(
                name=str(i['name']),
                description=str(i['description']),
                category=newCategory,
                user_id=1
            )
            session.add(newItem)
            session.commit()


print "All items have been added!"
