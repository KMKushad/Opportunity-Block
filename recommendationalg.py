import random 

subjects = ["Algebra", "Calculus", "Geometry", "Physics", "Chemistry", "Engineering", "Biology", "Coding", "English", "History", "Geography", "French", "Spanish", "Chinese", "Latin"]
words = ["exciting", "life-changing", "mediocre", "novel", "worthless", "wonderful"]


def generate_posts():
    posts = []
    for _ in range(30):
        subject1 = random.choice(subjects)
        subject2 = random.choice(subjects) 
        while subject1 == subject2:
            subject2 = random.choice(subjects)
        subject3 = random.choice(subjects)
        while subject3 == subject1 or subject3 == subject2:
            subject3 = random.choice(subjects)
        
        title = f"A {random.choice(words)} Opportunity to explore the intersection of {subject1}, {subject2}, and {subject3}."

        posts.append({"title" : title, "weights" : {subject1 : 0.5, subject2 : 0.3, subject3 : 0.2}})

    return posts

#this will likely take in 2 dictionaries:
    #user contains a dict in a dict with all the user's weights towards certain subjects
    #post contains the weight information for each Opportunity
    #action is just like/dislike

def update_weights(user, post, action):
    