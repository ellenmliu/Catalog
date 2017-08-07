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



# Add User
##User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
##             picture='https://pbs.twimg.com/profile_images/2671170543/\
##             18debd694829ed78203a5a36dd364160_400x400.png')
##session.add(User1)
##session.commit()
##
### Add Categories
##category1 = Category(name="Soccer")
##
##session.add(category1)
##session.commit()
##
##category2 = Category(name="Basketball")
##
##session.add(category2)
##session.commit()
##
##category3 = Category(name="Baseball")
##
##session.add(category3)
##session.commit()
##
##category4 = Category(name="Badminton")
##
##session.add(category4)
##session.commit()
##
##category5 = Category(name="Skating")
##
##session.add(category5)
##session.commit()
##
##category6 = Category(name="Hockey")
##
##session.add(category6)
##session.commit()
##
##category7 = Category(name="Snow Boarding")
##
##session.add(category7)
##session.commit()
##
### Add Items
##item1 = Item(name="Soccer Ball",
##             description="Can't play soccer without a ball",
##             category=category1,
##             user_id=1)
##
##session.add(item1)
##session.commit()
##
##item2 = Item(name="Cleats",
##             description="Helps with grip",
##             category=category1,
##             user_id=1)
##
##session.add(item2)
##session.commit()
##
##item3 = Item(name="Shin Guards",
##             description="Got to protect the shins",
##             category=category1,
##             user_id=1)
##
##session.add(item3)
##session.commit()
##
##item4 = Item(name="Basketball",
##             description="Shoot like Curry",
##             category=category2,
##             user_id=1)
##
##session.add(item4)
##session.commit()
##
##item5 = Item(name="Basketball Shoes",
##             description="Hops like Jordan",
##             category=category2,
##             user_id=1)
##
##session.add(item5)
##session.commit()
##
##item6 = Item(name="Basketball Jersey",
##             description="Feel like Kobe",
##             category=category2,
##             user_id=1)
##
##session.add(item6)
##session.commit()
##
##item7 = Item(name="Baseball Jersey",
##             description="Dress up for the baseball season",
##             category=category3,
##             user_id=1)
##
##session.add(item7)
##session.commit()
##
##item8 = Item(name="Bat",
##             description="Them homeruns don't come easy",
##             category=category3,
##             user_id=1)
##
##session.add(item8)
##session.commit()
##
##item9 = Item(name="Raquet",
##             description="Keep it light and powerful",
##             category=category4,
##             user_id=1)
##
##session.add(item9)
##session.commit()
##
##item10 = Item(name="Grip",
##              description="No blister zone",
##              category=category4,
##              user_id=1)
##
##session.add(item10)
##session.commit()
##
##item11 = Item(name="Roller Skates",
##              description="Figure eights on ground",
##              category=category5,
##              user_id=1)
##
##session.add(item11)
##session.commit()
##
##item12 = Item(name="Hockey Skates",
##              description="Figure eights on ice",
##              category=category6,
##              user_id=1)
##
##session.add(item12)
##session.commit()
##
##item13 = Item(name="Snowboard",
##              description="Faster than ever",
##              category=category7,
##              user_id=1)
##
##session.add(item13)
##session.commit()

for u in category_json['users']:
  newUser = User(
    name=str(u['name']),
    email=str(u['email']),
    picture=str(u['picture'])
  )
  session.add(newUser)
  session.commit()


              
                 

print "All items have been added!"
